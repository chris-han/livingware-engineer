#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SOURCE="$ROOT/scripts/bump-version.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

FIXTURE="$TMP/repo"
mkdir -p "$FIXTURE/scripts" "$FIXTURE/plugin" "$TMP/bin"
cp "$SOURCE" "$FIXTURE/scripts/bump-version.sh"

cat > "$FIXTURE/.version-bump.json" <<'JSON'
{
  "version": "1.2.3",
  "files": [
    {"path": ".version-bump.json", "field": "version"},
    {"path": "package.json", "field": "version"},
    {"path": "plugin/plugin.json", "field": "meta.0.version"}
  ],
  "audit": {
    "exclude": ["RELEASE-NOTES.md", "docs"]
  }
}
JSON

cat > "$FIXTURE/package.json" <<'JSON'
{
  "name": "fixture",
  "version": "1.2.3"
}
JSON

cat > "$FIXTURE/plugin/plugin.json" <<'JSON'
{
  "meta": [
    {"version": "1.2.3"}
  ]
}
JSON

cat > "$TMP/bin/jq" <<'SH'
#!/usr/bin/env bash
echo "FAIL: jq must not be invoked" >&2
exit 97
SH
chmod +x "$TMP/bin/jq"

# Keep normal host tools available, but guarantee any jq lookup hits the failing shim.
export PATH="$TMP/bin:$PATH"

bash "$FIXTURE/scripts/bump-version.sh" --check > "$TMP/check.log"
grep -Fq "All declared files are in sync at 1.2.3" "$TMP/check.log"

bash "$FIXTURE/scripts/bump-version.sh" --audit > "$TMP/audit.log"
grep -Fq "Audit: scanning repo for version string '1.2.3'" "$TMP/audit.log"

bash "$FIXTURE/scripts/bump-version.sh" 2.3.4 > "$TMP/bump.log"
grep -Fq "All declared files are in sync at 2.3.4" "$TMP/bump.log"

python3 - "$FIXTURE" <<'PY'
import json
from pathlib import Path
import sys

root = Path(sys.argv[1])
assert json.loads((root / ".version-bump.json").read_text())["version"] == "2.3.4"
assert json.loads((root / "package.json").read_text())["version"] == "2.3.4"
assert json.loads((root / "plugin/plugin.json").read_text())["meta"][0]["version"] == "2.3.4"
PY

echo "PASS: version check/audit/bump require Python only; jq is not invoked"
