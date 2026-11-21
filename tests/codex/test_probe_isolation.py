#!/usr/bin/env python3
"""Regression tests for the live probe's local state boundaries."""
import concurrent.futures
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest

SCRIPT = Path(__file__).with_name('live-progressive-skill-probe.sh')
IA_SCRIPT = SCRIPT.with_name('live-ia-via-mvl-probe.sh')
EVAL_SCRIPT = SCRIPT.parents[1] / 'eval-skills' / 'live-skill-runtime-eval.sh'


class ProbeIsolation(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='livingware-isolation-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.home = self.root / 'user'
        self.codex = self.home / '.codex'
        self.codex.mkdir(parents=True)
        self.original = b'# user configuration\n[projects."/existing"]\ntrust_level = "trusted"\n'
        (self.codex / 'config.toml').write_bytes(self.original)
        (self.codex / 'auth.json').write_text('{"fixture": true}')
        (self.codex / 'plugins' / 'cache').mkdir(parents=True)
        (self.codex / 'plugins' / 'cache' / 'fixture').write_text('plugin')
        (self.codex / '.tmp' / 'marketplaces' / 'fixture').mkdir(parents=True)
        (self.codex / '.tmp' / 'marketplaces' / 'fixture' / 'manifest').write_text('marketplace')
        self.fake = self.root / 'codex'
        self.fake.write_text('''#!/usr/bin/env python3
import json, os, pathlib, subprocess, sys, time
if '--version' in sys.argv:
    if os.environ.get('PROBE_TEST_VERSION_WRITES'):
        with open(pathlib.Path(os.environ['CODEX_HOME']) / 'config.toml', 'a') as f: f.write('\\n# version write\\n')
    print('codex test double')
    sys.exit(0)
home = pathlib.Path(os.environ['CODEX_HOME'])
assert (home / 'auth.json').exists()
assert (home / 'plugins/cache/fixture').read_text() == 'plugin'
assert (home / '.tmp/marketplaces/fixture/manifest').read_text() == 'marketplace'
with open(home / 'config.toml', 'a') as f: f.write('\\n# trust change\\n')
with open(os.environ['PROBE_TEST_LOG'], 'a') as f: f.write(json.dumps({'codex': str(home), 'home': os.environ['HOME'], 'cwd': sys.argv[sys.argv.index('-C') + 1]}) + '\\n')
if os.environ.get('PROBE_TEST_MUTATE'):
    project = pathlib.Path(sys.argv[sys.argv.index('-C') + 1])
    assert (project / 'keep').read_text() == 'dirty'
    assert subprocess.run(['/usr/bin/git', '-C', str(project), 'rev-parse', '--show-toplevel'],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    (project / 'generated').write_text('isolated')
if os.environ.get('PROBE_TEST_ORPHAN'):
    time.sleep(2)
    home.mkdir(parents=True, exist_ok=True)
    (home / 'late-write').write_text('late')
if os.environ.get('PROBE_TEST_SLEEP'): time.sleep(30)
if os.environ.get('PROBE_TEST_FAIL'): sys.exit(1)
print(json.dumps({'text': 'OK root cause investigation regression test implementation change fix evidence claim ready IA-before-UI GO_FOR_UI REVISE_IA R3 semantic owner NOT_APPLICABLE R0 duplicate stop'}))
''')
        self.fake.chmod(0o755)
        self.temp = self.root / 'tmp'
        self.temp.mkdir()
        self.log = self.root / 'calls.jsonl'
        self.env = dict(os.environ, HOME=str(self.home), CODEX_HOME=str(self.codex),
                        TMPDIR=str(self.temp), CODEX_BIN=str(self.fake),
                        CODEX_PROBE_OUTPUT_DIR=str(self.root / 'output'),
                        CODEX_PROBE_RETRIES='1', CODEX_PROBE_TIMEOUT='2',
                        CODEX_PROBE_BACKOFF='0', CODEX_PROBE_KEEP_TEMP='0',
                        CODEX_PROBE_WORKDIR='', PROBE_TEST_LOG=str(self.log))

    def run_probe(self, **overrides):
        return subprocess.run(['bash', str(SCRIPT)], env=dict(self.env, **overrides),
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)

    def assert_user_unchanged(self):
        self.assertEqual((self.codex / 'config.toml').read_bytes(), self.original)
        self.assertEqual((self.codex / 'plugins/cache/fixture').read_text(), 'plugin')
        self.assertEqual((self.codex / 'auth.json').read_text(), '{"fixture": true}')

    def test_explicit_interpreter_is_used_and_invalid_one_fails(self):
        wrapper = self.root / 'chosen-python'
        log = self.root / 'python-used'
        wrapper.write_text('#!/bin/sh\necho invoked >> "' + str(log) + '"\nexec "' + sys.executable + '" "$@"\n')
        wrapper.chmod(0o755)
        result = self.run_probe(CODEX_PROBE_PYTHON=str(wrapper))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(log.exists())
        result = self.run_probe(CODEX_PROBE_PYTHON=str(self.root / 'missing-python'))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Python 3.8 or newer is required', result.stderr)
        self.assert_user_unchanged()

    def test_repeated_and_concurrent_runs(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: self.run_probe(), range(2)))
        results.append(self.run_probe())
        for result in results:
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_user_unchanged()
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertEqual(len(calls), 12)
        self.assertEqual(len({x['codex'] for x in calls}), 3)
        self.assertTrue(all(x['codex'] != str(self.codex) and x['home'] != str(self.home) for x in calls))
        self.assertFalse(list(self.temp.iterdir()))
        self.assertEqual(len(list((self.root / 'output').glob('*/summary.tsv'))), 3)

    def test_failure_and_retention(self):
        result = self.run_probe(PROBE_TEST_FAIL='1')
        self.assertNotEqual(result.returncode, 0)
        self.assert_user_unchanged()
        self.assertFalse(list(self.temp.iterdir()))
        self.run_probe(CODEX_PROBE_KEEP_TEMP='1')
        self.assert_user_unchanged()
        self.assertEqual(len(list(self.temp.iterdir())), 1)
        self.assertFalse(list(self.temp.glob('*/codex/auth.json')))

    def test_concurrent_eval_wrappers_use_their_own_summary(self):
        env = dict(self.env, LIVINGWARE_EVAL_RAW_DIR=str(self.root / 'raw'),
                   LIVINGWARE_EVAL_OUTPUT_DIR=str(self.root / 'eval'), PROBE_TEST_VERSION_WRITES='1')
        def run(_):
            return subprocess.run(['bash', str(EVAL_SCRIPT)], env=env, text=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(run, range(2)))
        for result in results:
            self.assertEqual(result.returncode, 0, result.stderr)
        reports = list((self.root / 'eval').glob('*/eval-run.json'))
        self.assertEqual(len(reports), 2)
        self.assertTrue(all(json.loads(p.read_text())['runtime_pins']['codex_cli_version'] == 'codex test double'
                            for p in reports))
        self.assertEqual(len(list((self.root / 'raw').glob('*/*/summary.tsv'))), 2)
        self.assert_user_unchanged()

    def test_concurrent_ia_probes_are_isolated(self):
        def run(_):
            return subprocess.run(['bash', str(IA_SCRIPT)], env=self.env, text=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(run, range(2)))
        for result in results:
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_user_unchanged()
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertEqual(len(calls), 6)
        self.assertEqual(len({x['codex'] for x in calls}), 2)
        self.assertTrue(all(x['codex'] != str(self.codex) and x['home'] != str(self.home) for x in calls))
        self.assertFalse(list(self.temp.iterdir()))
        self.assertEqual(len(list((self.root / 'output').glob('*/summary.tsv'))), 2)

    def test_supplied_workdir_is_never_removed(self):
        project = self.root / 'user-project'
        project.mkdir()
        (project / 'keep').write_text('untouched')
        result = self.run_probe(CODEX_PROBE_WORKDIR=str(project))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((project / 'keep').read_text(), 'untouched')
        self.assertFalse(list(self.temp.iterdir()))

    def test_supplied_git_workdir_is_snapshotted_for_concurrent_runs(self):
        project = self.root / 'source-project'
        project.mkdir()
        def git(*args):
            subprocess.run(['/usr/bin/git', '-C', str(project), *args], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        git('init', '-q')
        git('config', 'user.email', 'test@example.invalid')
        git('config', 'user.name', 'Test')
        (project / 'keep').write_text('committed')
        git('add', 'keep')
        git('commit', '-qm', 'baseline')
        (project / 'keep').write_text('dirty')
        nested = project / 'nested'
        nested.mkdir()
        (nested / 'keep').write_text('dirty')
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda path: self.run_probe(CODEX_PROBE_WORKDIR=str(path),
                                                                 PROBE_TEST_MUTATE='1'),
                                    (project, nested)))
        for result in results:
            self.assertEqual(result.returncode, 0, result.stderr)
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertEqual(len({x['cwd'] for x in calls}), 2)
        self.assertEqual((project / 'keep').read_text(), 'dirty')
        self.assertFalse((project / 'generated').exists())
        self.assertFalse((nested / 'generated').exists())
        self.assert_user_unchanged()
        self.assertFalse(list(self.temp.iterdir()))

    def test_interrupted_run_is_cleaned(self):
        env = dict(self.env, PROBE_TEST_SLEEP='1', CODEX_PROBE_TIMEOUT='2')
        p = subprocess.Popen(['bash', str(SCRIPT)], env=env, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, start_new_session=True)
        try:
            deadline = time.monotonic() + 12
            while not self.log.exists() and time.monotonic() < deadline:
                time.sleep(.05)
            self.assertTrue(self.log.exists())
            os.killpg(p.pid, signal.SIGKILL)
            p.wait(timeout=5)
            deadline = time.monotonic() + 10
            while list(self.temp.iterdir()) and time.monotonic() < deadline:
                time.sleep(.1)
            self.assertFalse(list(self.temp.iterdir()))
            self.assert_user_unchanged()
        finally:
            if p.poll() is None:
                os.killpg(p.pid, signal.SIGKILL)
                p.wait()

    def test_killed_parent_does_not_leave_child_recreated_state(self):
        env = dict(self.env, PROBE_TEST_ORPHAN='1', CODEX_PROBE_TIMEOUT='4')
        p = subprocess.Popen(['bash', str(SCRIPT)], env=env, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, start_new_session=True)
        try:
            deadline = time.monotonic() + 10
            while not self.log.exists() and time.monotonic() < deadline:
                time.sleep(.05)
            self.assertTrue(self.log.exists())
            os.kill(p.pid, signal.SIGKILL)
            p.wait(timeout=5)
            time.sleep(3)
            deadline = time.monotonic() + 10
            while list(self.temp.iterdir()) and time.monotonic() < deadline:
                time.sleep(.1)
            self.assertFalse(list(self.temp.iterdir()))
            self.assert_user_unchanged()
        finally:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass


class ActualUserConfig(unittest.TestCase):
    def test_repeated_runs_leave_actual_config_byte_for_byte_unchanged(self):
        user_codex = Path.home() / '.codex'
        config = user_codex / 'config.toml'
        if not config.is_file():
            self.skipTest('no user Codex configuration')
        before = config.read_bytes()
        with tempfile.TemporaryDirectory(prefix='livingware-user-config-test-') as tmp:
            root = Path(tmp)
            executable = root / 'codex'
            executable.write_text('''#!/usr/bin/env python3
import json, os, pathlib, sys
home = pathlib.Path(os.environ['CODEX_HOME']).resolve()
if home == pathlib.Path(os.environ['PROTECTED_CODEX_HOME']).resolve(): sys.exit(98)
with open(home / 'config.toml', 'a') as f: f.write('\\n# simulated trust write\\n')
print(json.dumps({'text': 'OK root cause investigation regression test implementation change fix evidence claim ready IA-before-UI GO_FOR_UI REVISE_IA R3 semantic owner NOT_APPLICABLE R0 duplicate stop'}))
''')
            executable.chmod(0o755)
            env = dict(os.environ, CODEX_HOME=str(user_codex), PROTECTED_CODEX_HOME=str(user_codex),
                       CODEX_BIN=str(executable), TMPDIR=tmp, CODEX_PROBE_OUTPUT_DIR=str(root / 'out'),
                       CODEX_PROBE_RETRIES='1', CODEX_PROBE_TIMEOUT='2', CODEX_PROBE_BACKOFF='0',
                       CODEX_PROBE_KEEP_TEMP='0', CODEX_PROBE_WORKDIR='')
            for script in (SCRIPT, IA_SCRIPT):
                for _ in range(2):
                    result = subprocess.run(['bash', str(script)], env=env, text=True,
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(config.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
