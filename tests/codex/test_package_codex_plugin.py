#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "package-codex-plugin.sh"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"  [PASS] {message}")


def portable_env(tmp: Path) -> dict[str, str]:
    bindir = tmp / "portable-bin"
    bindir.mkdir()
    for name in ("python3", "git"):
        target = shutil.which(name)
        if not target:
            raise AssertionError(f"required test prerequisite missing: {name}")
        (bindir / name).symlink_to(target)
    env = os.environ.copy()
    env["PATH"] = str(bindir)
    return env


def write_metadata_fixture(root: Path) -> None:
    for skill in sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir()):
        dst = root / "skills" / skill / "agents" / "openai.yaml"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(
            f'interface:\n  display_name: "{skill}"\n  short_description: "Fixture metadata for {skill}"\n'
        )


def run_package(env: dict[str, str], metadata: Path, output: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(SCRIPT), "--allow-dirty", "--metadata-source", str(metadata), "--output", str(output), *extra],
        cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )


def zip_paths(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as zf:
        return sorted(n.rstrip("/") for n in zf.namelist() if n.rstrip("/"))


def tar_paths(path: Path) -> list[str]:
    with tarfile.open(path, "r:gz") as tf:
        return sorted(m.name.rstrip("/") for m in tf.getmembers() if m.name.rstrip("/"))


def main() -> int:
    print("Codex package archive portability tests")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        env = portable_env(tmp)
        require(shutil.which("jq", path=env["PATH"]) is None, "test PATH excludes jq")
        require(shutil.which("unzip", path=env["PATH"]) is None, "test PATH excludes unzip")
        require(shutil.which("zip", path=env["PATH"]) is None, "test PATH excludes zip CLI")
        require(shutil.which("tar", path=env["PATH"]) is None, "test PATH excludes tar CLI")
        require(shutil.which("shasum", path=env["PATH"]) is None, "test PATH excludes shasum")

        metadata = tmp / "metadata"
        write_metadata_fixture(metadata)
        out_zip = tmp / "livingware.zip"
        result = run_package(env, metadata, out_zip)
        require(result.returncode == 0, f"package script succeeds with git + python3 only\n{result.stdout}")
        require(out_zip.is_file(), "package script writes ZIP archive")
        require("Format:  zip" in result.stdout, "package script reports ZIP format")
        require("SHA-256:" in result.stdout, "package script reports SHA-256")

        paths = zip_paths(out_zip)
        require(".codex-plugin/plugin.json" in paths, "archive includes Codex manifest")
        require("skills/brainstorming/SKILL.md" in paths, "archive includes skills")
        require("skills/brainstorming/agents/openai.yaml" in paths, "archive includes OpenAI metadata")
        require(not any(p.startswith("tests/") or p.startswith("docs/") or p.startswith("scripts/") for p in paths), "archive excludes source-only paths")

        with zipfile.ZipFile(out_zip) as zf:
            manifest = json.loads(zf.read(".codex-plugin/plugin.json"))
            require(manifest["name"] == "livingware-engineer", "archive preserves plugin identity")
            require(manifest["version"] == json.loads((ROOT / "package.json").read_text())["version"], "archive preserves current version")
            require({i.date_time for i in zf.infolist()} == {(1980, 1, 1, 0, 0, 0)}, "ZIP timestamps are deterministic")
            mode = (zf.getinfo("skills/subagent-driven-development/scripts/task-brief").external_attr >> 16) & 0o777
            require(mode & stat.S_IXUSR != 0, "ZIP preserves executable script mode")

        out_tar = tmp / "livingware.tar.gz"
        tar_result = run_package(env, metadata, out_tar, "--format", "tar.gz")
        require(tar_result.returncode == 0, f"package script writes tar.gz with git + python3 only\n{tar_result.stdout}")
        require("Format:  tar.gz" in tar_result.stdout, "package script reports tar.gz format")
        require(tar_paths(out_tar) == paths, "ZIP and tar.gz contain identical paths")
        with tarfile.open(out_tar, "r:gz") as tf:
            require({m.mtime for m in tf.getmembers()} == {0}, "tar.gz timestamps are deterministic")
            task = tf.getmember("skills/subagent-driven-development/scripts/task-brief")
            require(task.mode & stat.S_IXUSR != 0, "tar.gz preserves executable script mode")

        metadata_zip = tmp / "metadata.zip"
        with zipfile.ZipFile(metadata_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for p in sorted(metadata.rglob("*")):
                if p.is_file():
                    zf.write(p, p.relative_to(metadata).as_posix())
        from_zip = tmp / "from-metadata-zip.zip"
        zip_source_result = run_package(env, metadata_zip, from_zip)
        require(zip_source_result.returncode == 0, "package script accepts ZIP metadata source without unzip")
        require(zip_paths(from_zip) == paths, "ZIP metadata source preserves archive path contract")

        metadata_tar = tmp / "metadata.tar.gz"
        with tarfile.open(metadata_tar, "w:gz") as tf:
            for p in sorted(metadata.rglob("*")):
                tf.add(p, arcname=p.relative_to(metadata).as_posix())
        from_tar = tmp / "from-metadata-tar.zip"
        tar_source_result = run_package(env, metadata_tar, from_tar)
        require(tar_source_result.returncode == 0, "package script accepts tar.gz metadata source without tar CLI")
        require(zip_paths(from_tar) == paths, "tar.gz metadata source preserves archive path contract")

    print("All Codex package portability tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
