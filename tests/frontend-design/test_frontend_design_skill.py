from __future__ import annotations

import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND_SKILL = ROOT / "skills" / "frontend-design" / "SKILL.md"
IMPECCABLE_ROOT = ROOT / "skills" / "impeccable"
UPSTREAM = IMPECCABLE_ROOT / "UPSTREAM.md"
UPSTREAM_COMMIT = "b0594c72d18006b5865c70eb3a97e8b04064e600"


def _tree_digest(root: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    ignored = {"UPSTREAM.md", "LICENSE.upstream", "NOTICE.upstream"}
    files = sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and path.name not in ignored
    )
    for path in files:
        relative = path.relative_to(root).as_posix()
        digest.update(f"{relative}\0".encode("utf-8"))
        digest.update(path.read_bytes())
    return len(files), digest.hexdigest()


def test_frontend_design_skill_exists_and_is_project_generic():
    text = FRONTEND_SKILL.read_text(encoding="utf-8")
    lower = text.lower()

    assert "name: frontend-design" in text
    assert "use when" in lower
    assert "design.md" in lower
    assert "impeccable" in lower
    assert "project design authority" in lower
    assert "semantier" not in lower


def test_frontend_design_skill_preserves_existing_design_system_before_generic_taste():
    text = FRONTEND_SKILL.read_text(encoding="utf-8")

    assert "DESIGN.md wins" in text
    assert "Do not replace an existing design system" in text
    assert "REQUIRED SUB-SKILL" in text
    assert "impeccable" in text
    assert "consistency objectives" in text


def test_impeccable_snapshot_is_pinned_and_attributed():
    skill = (IMPECCABLE_ROOT / "SKILL.md").read_text(encoding="utf-8")
    provenance = UPSTREAM.read_text(encoding="utf-8")
    license_text = (IMPECCABLE_ROOT / "LICENSE.upstream").read_text(encoding="utf-8")
    notice_text = (IMPECCABLE_ROOT / "NOTICE.upstream").read_text(encoding="utf-8")

    assert "name: impeccable" in skill
    assert "https://github.com/pbakaus/impeccable" in provenance
    assert UPSTREAM_COMMIT in provenance
    assert "Apache License" in license_text
    assert "Version 2.0" in license_text
    assert notice_text.strip()


def test_impeccable_snapshot_matches_recorded_digest():
    provenance = UPSTREAM.read_text(encoding="utf-8")
    count_match = re.search(r"Imported file count: `([0-9]+)`", provenance)
    digest_match = re.search(r"Tree SHA256: `([0-9a-f]{64})`", provenance)
    assert count_match and digest_match

    count, digest = _tree_digest(IMPECCABLE_ROOT)
    assert count == int(count_match.group(1))
    assert digest == digest_match.group(1)
