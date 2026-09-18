#!/usr/bin/env python3
"""Lazily provision the pinned Crawlee runtime used by data-collection-pipeline.

The runtime is isolated from the caller's Python environment. Core acquisition
installs only Crawlee itself. Browser dependencies and the Chromium runtime are
installed only through the explicit browser escalation mode.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import venv

SUPPORTED_CRAWLEE_VERSION = "1.10.1"
CORE_REQUIREMENT = f"crawlee=={SUPPORTED_CRAWLEE_VERSION}"
BROWSER_REQUIREMENT = f"crawlee[playwright]=={SUPPORTED_CRAWLEE_VERSION}"
MIN_PYTHON = (3, 10)


def default_runtime_dir() -> Path:
    root = os.environ.get("LIVINGWARE_RUNTIME_CACHE")
    if root:
        return Path(root).expanduser() / "data-collection" / f"crawlee-{SUPPORTED_CRAWLEE_VERSION}"
    return Path.home() / ".cache" / "livingware-engineer" / "data-collection" / f"crawlee-{SUPPORTED_CRAWLEE_VERSION}"


def venv_python(runtime_dir: Path) -> Path:
    if os.name == "nt":
        return runtime_dir / "venv" / "Scripts" / "python.exe"
    return runtime_dir / "venv" / "bin" / "python"


def run(cmd: list[str], *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, env=env)


def installed_crawlee_version(python: Path) -> str | None:
    code = (
        "import importlib.metadata as m;"
        "\ntry: print(m.version('crawlee'))"
        "\nexcept m.PackageNotFoundError: raise SystemExit(7)"
    )
    result = run([str(python), "-c", code])
    if result.returncode == 7:
        return None
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "failed to query Crawlee version")
    return result.stdout.strip()


def module_available(python: Path, module: str) -> bool:
    result = run([
        str(python),
        "-c",
        f"import importlib.util,sys; sys.exit(0 if importlib.util.find_spec({module!r}) else 9)",
    ])
    return result.returncode == 0


def verify_core(python: Path) -> None:
    result = run([
        str(python),
        "-c",
        "from crawlee.crawlers import FileDownloadCrawler; print(FileDownloadCrawler.__name__)",
    ])
    if result.returncode != 0 or "FileDownloadCrawler" not in result.stdout:
        raise RuntimeError(result.stderr.strip() or "Crawlee FileDownloadCrawler verification failed")


def verify_browser_extra(python: Path) -> None:
    result = run([
        str(python),
        "-c",
        "from crawlee.crawlers import PlaywrightCrawler; import playwright; print(PlaywrightCrawler.__name__)",
    ])
    if result.returncode != 0 or "PlaywrightCrawler" not in result.stdout:
        raise RuntimeError(result.stderr.strip() or "Crawlee Playwright extra verification failed")


def ensure_venv(runtime_dir: Path) -> tuple[Path, bool]:
    python = venv_python(runtime_dir)
    if python.is_file():
        return python, False
    (runtime_dir / "venv").parent.mkdir(parents=True, exist_ok=True)
    venv.EnvBuilder(with_pip=True, clear=False).create(runtime_dir / "venv")
    python = venv_python(runtime_dir)
    if not python.is_file():
        raise RuntimeError(f"venv Python missing after creation: {python}")
    return python, True


def pip_install(python: Path, requirement: str) -> None:
    result = run([
        str(python),
        "-m",
        "pip",
        "install",
        "--disable-pip-version-check",
        requirement,
    ])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"failed to install {requirement}")


def install_chromium(python: Path, browser_dir: Path) -> None:
    browser_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["PLAYWRIGHT_BROWSERS_PATH"] = str(browser_dir)
    result = run([str(python), "-m", "playwright", "install", "chromium"], env=env)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "failed to install Playwright Chromium runtime")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("core", "browser"), default="core")
    parser.add_argument("--runtime-dir", type=Path, default=default_runtime_dir())
    parser.add_argument("--plan", action="store_true", help="Describe the lazy install without modifying the runtime.")
    parser.add_argument("--check-only", action="store_true", help="Verify the selected runtime is already ready; do not install.")
    parser.add_argument(
        "--skip-browser-binary",
        action="store_true",
        help="Browser mode only: install/verify the Playwright Python extra but do not download Chromium.",
    )
    args = parser.parse_args()

    if sys.version_info < MIN_PYTHON:
        print(json.dumps({
            "state": "UNSUPPORTED_PYTHON",
            "required_python": ">=3.10",
            "actual_python": ".".join(map(str, sys.version_info[:3])),
        }, sort_keys=True))
        return 5

    runtime_dir = args.runtime_dir.expanduser().resolve()
    python = venv_python(runtime_dir)
    requirement = CORE_REQUIREMENT if args.mode == "core" else BROWSER_REQUIREMENT
    browser_dir = runtime_dir / "browsers"

    plan = {
        "state": "PLAN",
        "mode": args.mode,
        "crawlee_version": SUPPORTED_CRAWLEE_VERSION,
        "requirement": requirement,
        "runtime_dir": str(runtime_dir),
        "python_executable": str(python),
        "browser_extra": args.mode == "browser",
        "browser_binary_requested": args.mode == "browser" and not args.skip_browser_binary,
        "playwright_browsers_path": str(browser_dir) if args.mode == "browser" else None,
    }
    if args.plan:
        print(json.dumps(plan, sort_keys=True))
        return 0

    if args.check_only:
        if not python.is_file():
            print(json.dumps({**plan, "state": "MISSING_RUNTIME"}, sort_keys=True))
            return 4
        version = installed_crawlee_version(python)
        if version != SUPPORTED_CRAWLEE_VERSION:
            print(json.dumps({
                **plan,
                "state": "VERSION_MISMATCH" if version else "MISSING_CRAWLEE",
                "installed_version": version,
            }, sort_keys=True))
            return 4
        try:
            verify_core(python)
            if args.mode == "browser":
                verify_browser_extra(python)
                if not args.skip_browser_binary and not browser_dir.exists():
                    print(json.dumps({**plan, "state": "MISSING_BROWSER_BINARY", "installed_version": version}, sort_keys=True))
                    return 4
        except RuntimeError as exc:
            print(json.dumps({**plan, "state": "CAPABILITY_MISMATCH", "error": str(exc)}, sort_keys=True))
            return 4
        print(json.dumps({**plan, "state": "READY", "installed_version": version}, sort_keys=True))
        return 0

    python, created = ensure_venv(runtime_dir)
    before = installed_crawlee_version(python)
    installed = False

    if args.mode == "core":
        if before != SUPPORTED_CRAWLEE_VERSION:
            pip_install(python, CORE_REQUIREMENT)
            installed = True
    else:
        # Browser mode is an explicit escalation. Installing the extra also
        # ensures the pinned Crawlee core remains at the supported version.
        if before != SUPPORTED_CRAWLEE_VERSION or not module_available(python, "playwright"):
            pip_install(python, BROWSER_REQUIREMENT)
            installed = True

    after = installed_crawlee_version(python)
    if after != SUPPORTED_CRAWLEE_VERSION:
        raise RuntimeError(
            f"Crawlee version verification failed: expected {SUPPORTED_CRAWLEE_VERSION}, got {after!r}"
        )

    verify_core(python)
    browser_binary_installed = False
    if args.mode == "browser":
        verify_browser_extra(python)
        if not args.skip_browser_binary:
            install_chromium(python, browser_dir)
            browser_binary_installed = True

    print(json.dumps({
        **plan,
        "state": "READY",
        "created_runtime": created,
        "installed_dependency": installed,
        "installed_version": after,
        "browser_binary_installed": browser_binary_installed,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
