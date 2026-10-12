"""Verify the Asimov reference package can be read without a separate skill."""
from __future__ import annotations

import re
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "skills" / "frontend-design"


def reference_closure(package: Path) -> set[Path]:
    pending = [package / "SKILL.md"]
    visited: set[Path] = set()
    while pending:
        path = pending.pop().resolve()
        if path in visited:
            continue
        if not path.is_file():
            raise FileNotFoundError(path)
        path.relative_to(package.resolve())
        visited.add(path)
        for target in re.findall(r"\]\(([^)]+\.md)(?:#[^)]*)?\)", path.read_text(encoding="utf-8")):
            if "://" not in target and not target.startswith("#"):
                pending.append(path.parent / target)
    return visited


class AsimovReferencePackageTests(unittest.TestCase):
    def test_frontend_entry_reaches_alignment_and_regional_guidance(self):
        reachable = reference_closure(PACKAGE)
        for filename in ("asimov-alignment.md", "asimov-left-navigation.md"):
            self.assertIn((PACKAGE / "references" / filename).resolve(), reachable)
        self.assertFalse((ROOT / "skills" / "asimov-ui-design" / "SKILL.md").exists())

    def test_missing_regional_reference_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "frontend-design"
            shutil.copytree(PACKAGE, package)
            (package / "references" / "asimov-left-navigation.md").unlink()
            with self.assertRaises(FileNotFoundError):
                reference_closure(package)

    def test_reference_cannot_escape_the_package(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "frontend-design"
            package.mkdir()
            outside = Path(directory) / "outside.md"
            outside.write_text("external dependency", encoding="utf-8")
            (package / "SKILL.md").write_text("[dependency](../outside.md)", encoding="utf-8")
            with self.assertRaises(ValueError):
                reference_closure(package)


if __name__ == "__main__":
    unittest.main()
