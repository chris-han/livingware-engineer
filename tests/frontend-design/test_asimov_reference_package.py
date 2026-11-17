"""Verify Livingware IA references remain reachable with one frontend skill."""
from __future__ import annotations

import re
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "skills" / "frontend-design"


def reference_closure(package: Path, *, check_external: bool = True) -> set[Path]:
    """Follow frontend-owned references; validate (but do not recurse into) other owners."""
    pending = [package / "SKILL.md"]
    visited: set[Path] = set()
    project_root = package.parent.parent.resolve()
    package_root = package.resolve()
    while pending:
        path = pending.pop().resolve()
        if path in visited:
            continue
        if not path.is_file():
            raise FileNotFoundError(path)
        path.relative_to(project_root)  # No links outside the declared repository.
        visited.add(path)
        for ref in re.findall(r"\]\(([^)]+\.md)(?:#[^)]*)?\)", path.read_text(encoding="utf-8")):
            if "://" in ref or ref.startswith("#"):
                continue
            target = (path.parent / ref).resolve()
            target.relative_to(project_root)
            if target.is_relative_to(package_root):
                if not target.is_file():
                    raise FileNotFoundError(target)
                pending.append(target)
            elif check_external:
                if not target.is_file():
                    raise FileNotFoundError(target)
                visited.add(target)
    return visited


class AsimovReferencePackageTests(unittest.TestCase):
    def test_frontend_entry_reaches_alignment_and_regional_guidance(self):
        reachable = reference_closure(PACKAGE)
        for filename in (
            "asimov-alignment.md", "asimov-left-navigation.md", "asimov-canvas-header.md",
            "ia-ux-principles.md", "ia-ux-checklist.md", "ia-ux-evidence.md",
            "corner-geometry.md",
        ):
            self.assertIn((PACKAGE / "references" / filename).resolve(), reachable)
        self.assertFalse((ROOT / "skills" / "asimov-ui-design" / "SKILL.md").exists())
        self.assertFalse((ROOT / "skills" / "impeccable" / "SKILL.md").exists())

    def test_missing_regional_reference_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "repo" / "skills" / "frontend-design"
            package.parent.mkdir(parents=True)
            shutil.copytree(PACKAGE, package)
            (package / "references" / "asimov-left-navigation.md").unlink()
            with self.assertRaises(FileNotFoundError):
                reference_closure(package, check_external=False)

    def test_reference_cannot_escape_the_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "repo" / "skills" / "frontend-design"
            package.mkdir(parents=True)
            (Path(directory) / "outside.md").write_text("external dependency", encoding="utf-8")
            (package / "SKILL.md").write_text("[dependency](../../../outside.md)", encoding="utf-8")
            with self.assertRaises(ValueError):
                reference_closure(package, check_external=False)


if __name__ == "__main__":
    unittest.main()
