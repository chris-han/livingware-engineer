# Shared private Codex state for live probes; sourced by the calling script.
# Each invocation owns its fixture and writable Codex state. Copy only the
# inputs needed by a live session, never the user's sessions or recovery data.
SOURCE_CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
CODEX_BIN="$(command -v "$CODEX_BIN")" || { echo "ERROR: Codex CLI not found" >&2; exit 2; }
umask 077
TEMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/livingware-codex-probe-XXXXXXXX")" || exit 2
cleanup() {
  # Retained debugging state must not retain copied authentication.
  if [[ -d "$TEMP_ROOT/codex" && ! -L "$TEMP_ROOT/codex" ]]; then
    rm -f "$TEMP_ROOT/codex/auth.json"
  fi
  if [[ "${CODEX_PROBE_KEEP_TEMP:-0}" == 1 ]]; then
    echo "Retained probe state: $TEMP_ROOT" >&2
  else
    rm -rf "$TEMP_ROOT"
  fi
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
trap 'exit 129' HUP

# A detached watcher removes our private directory even if the shell is killed
# without running its EXIT trap. It never scans or removes other directories.
python3 - "$BASHPID" "$TEMP_ROOT" "${CODEX_PROBE_KEEP_TEMP:-0}" "$TIMEOUT_SECONDS" <<'PY' || exit 2
import os, subprocess, sys
watcher = r'''import os, shutil, sys, time
pid, root, keep, timeout = int(sys.argv[1]), sys.argv[2], sys.argv[3], int(sys.argv[4])
device, inode = int(sys.argv[5]), int(sys.argv[6])
def start_time():
    try:
        with open('/proc/%s/stat' % pid) as f:
            return f.read().split(') ', 1)[1].split()[19]
    except (OSError, IndexError): return None
identity = start_time()
def alive():
    try:
        os.kill(pid, 0)
        try:
            with open('/proc/%s/stat' % pid) as f:
                fields = f.read().split(') ', 1)[1].split()
                if fields[0] == 'Z' or (identity is not None and fields[19] != identity): return False
        except (OSError, IndexError): pass
        return True
    except ProcessLookupError: return False
    except PermissionError: return True
while alive(): time.sleep(1)
def owns_root():
    try:
        stat = os.stat(root, follow_symlinks=False)
        return (stat.st_dev, stat.st_ino) == (device, inode)
    except FileNotFoundError: return False
def remove_auth():
    codex = os.path.join(root, 'codex')
    if os.path.islink(codex): return
    try: os.remove(os.path.join(codex, 'auth.json'))
    except FileNotFoundError: pass
# A child can outlive a killed parent and recreate files after immediate
# cleanup. timeout's kill-after bounds that window. Normal EXIT cleanup has
# already removed the directory, in which case the watcher exits immediately.
if not owns_root(): sys.exit(0)
remove_auth()
for _ in range(timeout + 6):
    if not owns_root(): sys.exit(0)
    time.sleep(1)
if not owns_root(): sys.exit(0)
remove_auth()
if keep != '1': shutil.rmtree(root, ignore_errors=True)
'''
stat = os.stat(sys.argv[2], follow_symlinks=False)
subprocess.Popen([sys.executable, '-c', watcher, *sys.argv[1:], str(stat.st_dev), str(stat.st_ino)],
                 stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                 stderr=subprocess.DEVNULL, start_new_session=True, close_fds=True)
PY

mkdir -p "$TEMP_ROOT/home" "$TEMP_ROOT/codex" "$TEMP_ROOT/tmp" "$TEMP_ROOT/xdg-config" "$TEMP_ROOT/xdg-cache" "$TEMP_ROOT/xdg-data" "$TEMP_ROOT/xdg-state" "$TEMP_ROOT/xdg-runtime" || exit 2
for item in config.toml auth.json AGENTS.md agents rules plugins skills packages; do
  if [[ -e "$SOURCE_CODEX_HOME/$item" ]]; then
    cp -RL "$SOURCE_CODEX_HOME/$item" "$TEMP_ROOT/codex/$item" || exit 2
  fi
done
# Configured Git marketplaces are resolved relative to CODEX_HOME. Copy the
# snapshots, but not transient staging directories or their lock files.
if [[ -d "$SOURCE_CODEX_HOME/.tmp/marketplaces" ]]; then
  mkdir -p "$TEMP_ROOT/codex/.tmp/marketplaces" || exit 2
  for item in "$SOURCE_CODEX_HOME"/.tmp/marketplaces/*; do
    [[ -d "$item" ]] || continue
    cp -RL "$item" "$TEMP_ROOT/codex/.tmp/marketplaces/" || exit 2
  done
fi
export HOME="$TEMP_ROOT/home" CODEX_HOME="$TEMP_ROOT/codex"
export XDG_CONFIG_HOME="$TEMP_ROOT/xdg-config" XDG_CACHE_HOME="$TEMP_ROOT/xdg-cache" XDG_DATA_HOME="$TEMP_ROOT/xdg-data"
export XDG_STATE_HOME="$TEMP_ROOT/xdg-state" XDG_RUNTIME_DIR="$TEMP_ROOT/xdg-runtime" TMPDIR="$TEMP_ROOT/tmp"
