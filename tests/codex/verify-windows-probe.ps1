# Run in a real Windows PowerShell session, not CodexSandboxOnline.
param(
    [Parameter(Mandatory=$true)][string]$Python,
    [string]$Bash = "$env:ProgramFiles\Git\bin\bash.exe"
)
$ErrorActionPreference = 'Stop'
$Python = (Resolve-Path -LiteralPath $Python).Path
$Bash = (Resolve-Path -LiteralPath $Bash).Path
$probe = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot 'probe-isolation.sh')).Path
$env:LW_QUAL_BASH = $Bash
$env:LW_QUAL_PYTHON = $Python
$env:LW_QUAL_PROBE = $probe
$work = Join-Path ([IO.Path]::GetTempPath()) ('livingware-windows-qualification-' + [guid]::NewGuid())
New-Item -ItemType Directory -Path $work | Out-Null
try {
    $driver = Join-Path $work 'qualify.py'
    @'
import concurrent.futures, json, os, pathlib, subprocess, sys, tempfile, time
bash, python, probe = (os.environ[k] for k in ('LW_QUAL_BASH','LW_QUAL_PYTHON','LW_QUAL_PROBE'))
assert sys.version_info >= (3, 8)
with tempfile.TemporaryDirectory(prefix='livingware qualification ') as tmp:
    root = pathlib.Path(tmp)
    profile = root / 'disposable profile'
    codex = profile / '.codex'
    codex.mkdir(parents=True)
    (codex / 'config.toml').write_text('fixture\n')
    (codex / 'auth.json').write_text('fixture auth')
    temp = root / 'private temp'
    temp.mkdir()
    source = r'''set -u
PROBE_PATH=$(cygpath -u "$1")
SOURCE_PROFILE=$(cygpath -u "$2")
TEST_TEMP=$(cygpath -u "$3")
READY=$(cygpath -u "$4")
export HOME="$SOURCE_PROFILE" CODEX_HOME="$SOURCE_PROFILE/.codex" TMPDIR="$TEST_TEMP"
export CODEX_PROBE_PYTHON="$5" CODEX_PROBE_KEEP_TEMP="$6"
CODEX_BIN=bash TIMEOUT_SECONDS=2
source "$PROBE_PATH"
printf '%s' "$TEMP_ROOT" > "$READY"
printf '%s' "$PROBE_PID" > "$READY.pid"
"$PYTHON_BIN" -c 'import json,os,sys,time; p=sys.argv[1]; open(p,"w").write(json.dumps({k:os.environ[k] for k in ("CODEX_HOME","HOME","XDG_CONFIG_HOME","XDG_CACHE_HOME","XDG_DATA_HOME","XDG_STATE_HOME","XDG_RUNTIME_DIR","TMPDIR","TEMP","TMP")})); time.sleep(int(sys.argv[2])); open(os.path.join(os.environ["CODEX_HOME"],"late"),"w").write("late") if int(sys.argv[2]) else None' "$READY.env" "$7"
exit "$8"
'''
    def start(name, keep='0', delay='0', rc='0'):
        ready = root / (name + '.ready')
        p = subprocess.Popen([bash, '--noprofile', '--norc', '-c', source, '_', probe, str(profile), str(temp), str(ready), python, keep, delay, rc], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p, ready
    def wait_ready(p, ready):
        deadline = time.monotonic() + 20
        while not ready.exists() and p.poll() is None and time.monotonic() < deadline: time.sleep(.05)
        if not ready.exists():
            p.terminate()
            raise AssertionError('probe did not start: ' + p.communicate(timeout=10)[1].decode(errors='replace'))
        return pathlib.Path(subprocess.check_output([bash, '-c', 'cygpath -w "$1"', '_', ready.read_text()], text=True).strip())
    def wait_removed(path):
        deadline = time.monotonic() + 20
        while path.exists() and time.monotonic() < deadline: time.sleep(.1)
        assert not path.exists(), 'private state survived: ' + str(path)
    def normal(name, keep='0', rc='0'):
        p, ready = start(name, keep, '0', rc)
        path = wait_ready(p, ready)
        out, err = p.communicate(timeout=30)
        assert p.returncode == int(rc), (p.returncode, err.decode(errors='replace'))
        env = json.loads(pathlib.Path(str(ready) + '.env').read_text())
        for k, v in env.items():
            assert os.path.commonpath((str(pathlib.Path(v).resolve()), str(path.resolve()))) == str(path.resolve()), (k, v, path)
        if keep == '1':
            assert path.exists() and not (path / 'codex' / 'auth.json').exists()
        else: wait_removed(path)
        return path
    normal('normal')
    normal('failure', rc='7')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        paths = list(pool.map(normal, ('concurrent1', 'concurrent2')))
    assert paths[0] != paths[1]
    normal('retained', keep='1')
    p, ready = start('terminated', delay='4')
    path = wait_ready(p, ready)
    deadline = time.monotonic() + 10
    while not pathlib.Path(str(ready) + '.env').exists() and time.monotonic() < deadline: time.sleep(.05)
    assert pathlib.Path(str(ready) + '.env').exists()
    pidfile = pathlib.Path(str(ready) + '.pid')
    deadline = time.monotonic() + 10
    while not pidfile.exists() and time.monotonic() < deadline: time.sleep(.05)
    subprocess.run(['taskkill', '/PID', pidfile.read_text(), '/F'], check=True, stdout=subprocess.DEVNULL)
    p.wait(timeout=10)
    wait_removed(path)
    assert (codex / 'config.toml').read_text() == 'fixture\n'
    assert (codex / 'auth.json').read_text() == 'fixture auth'
print('WINDOWS PROBE ISOLATION QUALIFICATION: PASS')
'@ | Set-Content -LiteralPath $driver -Encoding UTF8
    & $Python $driver
    if ($LASTEXITCODE -ne 0) { throw "Windows qualification failed with exit code $LASTEXITCODE" }
} finally {
    Remove-Item -LiteralPath $work -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item Env:LW_QUAL_BASH, Env:LW_QUAL_PYTHON, Env:LW_QUAL_PROBE -ErrorAction SilentlyContinue
}
