"""Single frontend-design skill: Impeccable 4.9.2 base with Livingware IA extensions."""
from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "skills" / "frontend-design" / "SKILL.md"
TOOLKIT = ROOT / "skills" / "impeccable"
PROVENANCE = TOOLKIT / "UPSTREAM.md"
UPSTREAM_COMMIT = "d41d9860b0094dcb68030657da63461212835aaa"


def test_single_discoverable_frontend_skill_and_version() -> None:
    text = FRONTEND.read_text(encoding="utf-8")
    assert re.search(r"^name: frontend-design$", text, re.M)
    assert re.search(r"^version: 4\.9\.2$", text, re.M)
    assert not (TOOLKIT / "SKILL.md").exists()
    assert "not a two-skill handoff" in text
    assert "Impeccable" in text
    assert "Semantier" not in text  # No project-specific design authority in core.


def test_livingware_ia_gap_is_preserved_without_duplicate_skill() -> None:
    text = FRONTEND.read_text(encoding="utf-8")
    for phrase in (
        "IA-Before-UI",
        "GO_FOR_UI | REVISE_IA | NOT_APPLICABLE",
        "Fix → Infer → Recommend → Ask",
        "canonical owner",
        "Evidence continuity",
        "P06/C41–C46",
        "Asimov alignment",
        "corner geometry",
        "IA/UX source evidence",
        "Verification Impact Analysis",
    ):
        assert phrase.lower() in text.lower(), phrase
    assert "one discoverable skill" in text
    assert "without independent evidence" in text


def test_upstream_492_assets_and_attribution() -> None:
    text = PROVENANCE.read_text(encoding="utf-8")
    root = FRONTEND.read_text(encoding="utf-8")
    assert UPSTREAM_COMMIT in text
    assert "4.9.2" in text
    assert "Imported toolkit file count: 62" in text
    assert "Apache License" in (TOOLKIT / "LICENSE.upstream").read_text()
    assert (TOOLKIT / "NOTICE.upstream").read_text().strip()
    launcher = TOOLKIT / "scripts" / "impeccable"
    assert launcher.is_file()
    assert os.access(launcher, os.X_OK), "upstream shell launcher must stay executable"
    assert (TOOLKIT / "scripts" / "impeccable.cmd").is_file()
    assert (TOOLKIT / "scripts" / "VERSION").is_file()
    assert (TOOLKIT / "scripts" / "engine-checksums.txt").is_file()
    assert (TOOLKIT / "reference" / "generate.md").is_file()
    assert (TOOLKIT / "reference" / "critique-rubric.md").is_file()
    assert "<toolkit-base-dir>/scripts/impeccable" in root
    assert not (TOOLKIT / "scripts" / "context.mjs").exists(), "do not invoke retired 4.1.2 tools"


def test_frontend_skill_local_markdown_links_resolve() -> None:
    content = FRONTEND.read_text(encoding="utf-8")
    for link in re.findall(r"\]\(([^)]+)\)", content):
        if link.startswith(("https:", "http:", "#")):
            continue
        target = (FRONTEND.parent / link.split("#")[0]).resolve()
        assert target.is_relative_to(ROOT.resolve()), link
        assert target.is_file(), link
