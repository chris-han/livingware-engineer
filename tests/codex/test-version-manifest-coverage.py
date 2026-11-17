#!/usr/bin/env python3
"""Check every distributed Livingware version, even if the bump config is incomplete."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = {
    ".version-bump.json": "version",
    "package.json": "version",
    ".codex-plugin/plugin.json": "version",
    ".claude-plugin/plugin.json": "version",
    ".claude-plugin/marketplace.json": "plugins.0.version",
    ".cursor-plugin/plugin.json": "version",
    ".devin-plugin/plugin.json": "version",
    ".kimi-plugin/plugin.json": "version",
    "gemini-extension.json": "version",
    ".hermes-plugin/plugin.yaml": "version",
}


def check_inventory(files):
    entries = [(item["path"], item["field"]) for item in files]
    assert len(entries) == len(set(entries)), "duplicate version declarations"
    assert dict(entries) == EXPECTED, "release inventory omitted or changed a distribution manifest"


def read_version(path, field):
    source = (ROOT / path).read_text(encoding="utf-8")
    if path.endswith(".json"):
        value = json.loads(source)
        for part in field.split("."):
            value = value[int(part)] if part.isdigit() else value[part]
        return value
    if path.endswith(".yaml") and field == "version":
        values = [line.partition(":")[2].strip().strip("'\\\"")
                  for line in source.splitlines() if line.startswith("version:")]
        assert len(values) == 1, "YAML version must be a unique top-level scalar"
        return values[0]
    raise AssertionError(f"unsupported version field: {path} {field}")


def check_values(values, version):
    for path, value in values.items():
        assert value == version, f"{path}: {value!r} != {version!r}"


def main():
    config = json.loads((ROOT / ".version-bump.json").read_text(encoding="utf-8"))
    check_inventory(config["files"])
    version = config["version"]
    assert re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?", version)
    actual = {path: read_version(path, field) for path, field in EXPECTED.items()}
    check_values(actual, version)

    # These negative controls reproduce the missing-Codex-manifest incident.
    missing = [i for i in config["files"] if i["path"] != ".codex-plugin/plugin.json"]
    try:
        check_inventory(missing)
    except AssertionError:
        pass
    else:
        raise AssertionError("missing Codex manifest was accepted")
    wrong = dict(actual)
    wrong[".codex-plugin/plugin.json"] = "0.0.0"
    try:
        check_values(wrong, version)
    except AssertionError:
        pass
    else:
        raise AssertionError("stale Codex manifest was accepted")
    print(f"PASS: {len(EXPECTED)} distribution versions match {version}; negative controls rejected")


if __name__ == "__main__":
    main()
