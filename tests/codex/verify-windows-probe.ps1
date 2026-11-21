# Run in a real Windows PowerShell session, not CodexSandboxOnline.
param(
    [Parameter(Mandatory=$true)][string]$Python,
    [Parameter(Mandatory=$true)][string]$ExpectedCommit,
    [string]$Bash = "$env:ProgramFiles\Git\bin\bash.exe"
)
$ErrorActionPreference = 'Stop'
$Python = (Resolve-Path -LiteralPath $Python).Path
$Bash = (Resolve-Path -LiteralPath $Bash).Path
$probe = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot 'probe-isolation.sh')).Path
$repo = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../..')).Path
$git = (Resolve-Path -LiteralPath "$env:ProgramFiles\Git\cmd\git.exe").Path
$actualCommit = (& $git -C $repo rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $actualCommit -ne $ExpectedCommit) { throw "Unexpected qualification commit: $actualCommit" }
& $git -C $repo diff --quiet HEAD -- tests/codex/probe-isolation.sh tests/codex/verify-windows-probe.ps1 tests/codex/live-progressive-skill-probe.sh tests/codex/live-ia-via-mvl-probe.sh
if ($LASTEXITCODE -ne 0) { throw 'Qualification source files differ from HEAD' }
Write-Output "WINDOWS PROBE QUALIFICATION COMMIT: $actualCommit"
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
    # Exercise the real progressive caller, with its source on the checkout's
    # drive and private state on the system temporary drive.
    checkout = pathlib.Path(probe).resolve().parents[2]
    assert checkout.drive.lower() != root.drive.lower(), (
        'Cross-drive qualification requires the checkout and TEMP on different drives', checkout, root)
    fake_py = root / 'fake-codex.py'
    fake_py.write_text('''import json, os, pathlib, sys
if '--version' in sys.argv:
    print('codex fixture')
    raise SystemExit(0)
project = pathlib.Path(sys.argv[sys.argv.index('-C') + 1])
(project / 'generated').write_text('isolated')
print(json.dumps({'text': 'OK root cause investigation regression test implementation change fix evidence claim ready'}))
''')
    fake_sh = root / 'fake-codex.sh'
    fake_sh.write_text('#!/usr/bin/env bash\nexec "$CODEX_PROBE_PYTHON" "$LW_FAKE_PY" "$@"\n')
    with tempfile.TemporaryDirectory(prefix='livingware-cross-drive-', dir=str(checkout.parent)) as source_dir:
        project = pathlib.Path(source_dir)
        (project / 'keep').write_text('original')
        live_source = r'''set -u
SCRIPT=$(cygpath -u "$1"); PROFILE=$(cygpath -u "$2"); PRIVATE=$(cygpath -u "$3")
PROJECT=$(cygpath -u "$4"); FAKE=$(cygpath -u "$5"); OUTPUT=$(cygpath -u "$6")
chmod +x "$FAKE"
export HOME="$PROFILE" CODEX_HOME="$PROFILE/.codex" TMPDIR="$PRIVATE"
export CODEX_PROBE_PYTHON="$7" LW_FAKE_PY="$8" CODEX_BIN="$FAKE"
export CODEX_PROBE_WORKDIR="$PROJECT" CODEX_PROBE_OUTPUT_DIR="$OUTPUT"
export CODEX_PROBE_RETRIES=1 CODEX_PROBE_TIMEOUT=10 CODEX_PROBE_BACKOFF=0 CODEX_PROBE_KEEP_TEMP=0
exec bash "$SCRIPT"
'''
        live = subprocess.run([bash, '--noprofile', '--norc', '-c', live_source, '_',
                               str(checkout / 'tests/codex/live-progressive-skill-probe.sh'),
                               str(profile), str(temp), str(project), str(fake_sh),
                               str(root / 'output'), python, str(fake_py)],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90)
        assert live.returncode == 0, (live.returncode, live.stderr.decode(errors='replace'))
        assert (project / 'keep').read_text() == 'original' and not (project / 'generated').exists()
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
