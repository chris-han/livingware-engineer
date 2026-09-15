#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATHS = [
    ".codex-plugin",
    "CODE_OF_CONDUCT.md",
    "LICENSE",
    "README.md",
    "assets",
    "skills",
]
FORBIDDEN_PREFIXES = (
    "superpowers/", ".agents/", "hooks/", ".git", ".pytest_cache", ".ruff_cache",
    "scripts/", "tests/", "docs/", "evals/", "lib/", ".claude", ".cursor",
    ".kimi", ".opencode", ".pi",
)
FORBIDDEN_FILES = {
    "package.json", "AGENTS.md", "CLAUDE.md", "GEMINI.md", "RELEASE-NOTES.md", "CHANGELOG.md"
}


def die(message: str) -> "NoReturn":
    raise SystemExit(f"ERROR: {message}")


def run(*args: str, cwd: Path | None = None, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=cwd, check=True, text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Package the Livingware Engineer Codex plugin")
    p.add_argument("--output")
    p.add_argument("--format", choices=("zip", "tar.gz", "tgz"))
    p.add_argument("--metadata-source")
    p.add_argument("--ref", default="HEAD")
    p.add_argument("--allow-dirty", action="store_true")
    p.add_argument("--keep-stage", action="store_true")
    return p.parse_args()


def infer_format(output: str | None, explicit: str | None) -> str:
    normalized = "tar.gz" if explicit == "tgz" else explicit
    inferred = None
    if output:
        if output.endswith((".tar.gz", ".tgz")):
            inferred = "tar.gz"
        elif output.endswith(".zip"):
            inferred = "zip"
    if normalized and inferred and normalized != inferred:
        die(f"--output extension does not match --format {normalized}: {output}")
    return normalized or inferred or "zip"


def ensure_repo(ref: str, allow_dirty: bool) -> None:
    if not (ROOT / ".git").is_dir():
        die(f"repo root is not a git checkout: {ROOT}")
    try:
        run("git", "rev-parse", "--verify", f"{ref}^{{commit}}", cwd=ROOT, capture=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        die(f"git ref does not resolve to a commit: {ref}")
    if not allow_dirty:
        status = run("git", "status", "--porcelain", "--untracked-files=all", cwd=ROOT, capture=True).stdout
        if status.strip():
            sys.stderr.write("Working tree has uncommitted changes:\n")
            for line in status.splitlines():
                sys.stderr.write(f"  {line}\n")
            die(f"commit or stash changes first, or pass --allow-dirty to package {ref} anyway")


def default_metadata_source() -> Path:
    base = ROOT.parent / "_tmp" / "sup-codex-packaging"
    for candidate in (base / "superpowers", base / "superpowers.zip", base / "superpowers.tar.gz"):
        if candidate.exists():
            return candidate
    die("no metadata source found; pass --metadata-source <prior package dir, zip, or tar.gz>")


def safe_extract_zip(source: Path, destination: Path) -> None:
    with zipfile.ZipFile(source) as zf:
        for info in zf.infolist():
            target = destination / info.filename
            resolved = target.resolve()
            if destination.resolve() not in (resolved, *resolved.parents):
                die(f"unsafe zip path: {info.filename}")
        zf.extractall(destination)


def safe_extract_tar(source: Path, destination: Path) -> None:
    with tarfile.open(source, "r:gz") as tf:
        for member in tf.getmembers():
            resolved = (destination / member.name).resolve()
            if destination.resolve() not in (resolved, *resolved.parents):
                die(f"unsafe tar path: {member.name}")
        tf.extractall(destination)


def metadata_root(source: Path, work: Path) -> Path:
    if source.is_dir():
        root = source.resolve()
    elif source.is_file() and source.name.endswith((".tar.gz", ".tgz")):
        safe_extract_tar(source, work)
        root = work
    elif source.is_file() and source.suffix == ".zip":
        safe_extract_zip(source, work)
        root = work
    else:
        die(f"metadata source must be a directory, .zip, or .tar.gz: {source}")
    if (root / "skills").is_dir():
        return root
    for p in root.glob("*/*/skills"):
        if p.is_dir():
            return p.parent
    for p in root.glob("*/skills"):
        if p.is_dir():
            return p.parent
    die(f"metadata source does not contain a skills/ directory: {source}")


def export_git_tree(ref: str, stage: Path) -> None:
    cmd = ["git", "-c", "tar.umask=0022", "archive", "--format=tar", ref, "--", *SOURCE_PATHS]
    try:
        proc = subprocess.run(cmd, cwd=ROOT, check=True, stdout=subprocess.PIPE)
    except FileNotFoundError:
        die("git not found in PATH")
    with tarfile.open(fileobj=io.BytesIO(proc.stdout), mode="r:") as tf:
        tf.extractall(stage)


def read_version(stage: Path) -> str:
    try:
        data = json.loads((stage / ".codex-plugin" / "plugin.json").read_text())
        version = data.get("version")
    except Exception as exc:
        die(f"could not read version from .codex-plugin/plugin.json: {exc}")
    if not version:
        die("could not read version from .codex-plugin/plugin.json")
    return str(version)


def seed_metadata(stage: Path, metadata: Path) -> int:
    skills = sorted(p for p in (stage / "skills").iterdir() if p.is_dir())
    missing = []
    for skill_dir in skills:
        src = metadata / "skills" / skill_dir.name / "agents" / "openai.yaml"
        if not src.is_file():
            missing.append(skill_dir.name)
            continue
        dst = skill_dir / "agents" / "openai.yaml"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    if missing:
        for skill in missing:
            sys.stderr.write(f"Missing OpenAI agent metadata for skill: {skill}\n")
        die("metadata source is incomplete")
    return len(skills)


def entries(stage: Path) -> list[Path]:
    return sorted(stage.rglob("*"), key=lambda p: p.relative_to(stage).as_posix())


def write_zip(stage: Path, output: Path) -> None:
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in entries(stage):
            rel = path.relative_to(stage).as_posix()
            mode = stat.S_IMODE(path.stat().st_mode)
            zi = zipfile.ZipInfo(rel + ("/" if path.is_dir() else ""), (1980, 1, 1, 0, 0, 0))
            zi.create_system = 3
            zi.external_attr = (mode & 0xFFFF) << 16
            if path.is_dir():
                zi.external_attr |= 0x10
                zf.writestr(zi, b"")
            else:
                zi.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(zi, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def write_tar(stage: Path, output: Path) -> None:
    with tarfile.open(output, "w:gz", format=tarfile.USTAR_FORMAT, compresslevel=9) as tf:
        for path in entries(stage):
            rel = path.relative_to(stage).as_posix()
            info = tf.gettarinfo(str(path), arcname=rel)
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.mtime = 0
            if path.is_file():
                with path.open("rb") as fh:
                    tf.addfile(info, fh)
            else:
                tf.addfile(info)


def archive_paths(output: Path, fmt: str) -> list[str]:
    if fmt == "zip":
        with zipfile.ZipFile(output) as zf:
            names = [n.rstrip("/") for n in zf.namelist()]
    else:
        with tarfile.open(output, "r:gz") as tf:
            names = [m.name.rstrip("/") for m in tf.getmembers()]
    return [n for n in names if n]


def validate_paths(paths: list[str]) -> None:
    bad = []
    for p in paths:
        if p in FORBIDDEN_FILES or p.startswith(FORBIDDEN_PREFIXES):
            bad.append(p)
    if bad:
        for p in bad:
            sys.stderr.write(f"  {p}\n")
        die("archive contains source-only paths")


def main() -> int:
    args = parse_args()
    if shutil.which("git") is None:
        die("git not found in PATH")
    fmt = infer_format(args.output, args.format)
    ensure_repo(args.ref, args.allow_dirty)
    source = Path(args.metadata_source).expanduser() if args.metadata_source else default_metadata_source()

    keep = None
    tmp = tempfile.TemporaryDirectory(prefix="livingware-codex-package.")
    work = Path(tmp.name)
    stage = work / "payload"
    metadata_work = work / "metadata"
    stage.mkdir()
    metadata_work.mkdir()
    try:
        meta = metadata_root(source, metadata_work)
        export_git_tree(args.ref, stage)
        version = read_version(stage)
        skill_count = seed_metadata(stage, meta)
        if args.output:
            output = Path(args.output).expanduser().resolve()
        else:
            suffix = ".zip" if fmt == "zip" else ".tar.gz"
            output = (ROOT.parent / "_tmp" / "sup-codex-packaging" / f"superpowers-{version}{suffix}").resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        if output.exists():
            output.unlink()
        if fmt == "zip":
            write_zip(stage, output)
        else:
            write_tar(stage, output)
        paths = archive_paths(output, fmt)
        validate_paths(paths)
        checksum = hashlib.sha256(output.read_bytes()).hexdigest()
        print(f"Archive: {output}")
        print(f"Format:  {fmt}")
        print(f"Version: {version}")
        print(f"Entries: {len(paths)}")
        print(f"Skills:  {skill_count}")
        print(f"SHA-256: {checksum}")
        if args.keep_stage:
            keep = work
            print(f"Keeping staging directory: {work}", file=sys.stderr)
            tmp.cleanup = lambda: None  # type: ignore[method-assign]
        return 0
    finally:
        if keep is None:
            tmp.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
