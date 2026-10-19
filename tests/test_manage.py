import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ManageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.repo = base / 'config'
        self.repo.mkdir()
        shutil.copy2(ROOT / 'manage.py', self.repo)
        shutil.copy2(ROOT / 'plugin_setup.py', self.repo)
        (self.repo / 'plugins.json').write_text(json.dumps({'codex_version': 'test', 'marketplaces': {}, 'plugins': {}}))
        (self.repo / 'config.toml').write_text('model = "shared"\n')
        (self.repo / 'notify.py').write_text('# notification script\n')
        custom = self.repo / 'skills/custom/mine'
        custom.mkdir(parents=True)
        (custom / 'SKILL.md').write_text('custom\n')
        self.home = base / 'codex home 日本語'
        self.remote = base / 'remote'
        self.remote.mkdir()
        (self.remote / 'demo').mkdir()
        (self.remote / 'demo/SKILL.md').write_text('original v2\n')
        self.requirements = self.repo / 'skills/requirements.json'
        self.requirements.write_text(json.dumps({'demo': str(self.remote)}))
        self.bin = base / 'bin'
        self.bin.mkdir()
        npx = self.bin / 'npx'
        npx.write_text(f'''#!{sys.executable}
import pathlib, shutil, sys
assert sys.argv[1:4] == ['--yes', 'skills@latest', 'add']
assert sys.argv[5:] == ['--skill', 'demo', '--agent', 'codex', '--copy', '--yes']
source = pathlib.Path(sys.argv[4]) / 'demo'
shutil.copytree(source, pathlib.Path.cwd() / '.agents/skills/demo', symlinks=True)
''')
        npx.chmod(0o755)
        (self.remote / 'demo/SKILL.md').write_text('original v2\n')

    def run_manage(self, command, *args):
        options = ['--codex-home', str(self.home)] if command in ('install', 'update') else []
        return subprocess.run([sys.executable, str(self.repo / 'manage.py'), command, *options, *args],
                              capture_output=True, text=True, env={**os.environ, 'PATH': str(self.bin) + os.pathsep + os.environ['PATH']})

    def test_latest_install_replaces_fork_and_preserves_backup(self):
        old = self.home / 'skills/demo'
        old.mkdir(parents=True)
        (old / 'SKILL.md').write_text('my old fork\n')
        (old / 'extra.txt').write_text('old customization')
        (self.home / 'config.toml').write_text('model = "previous"\n')
        (self.home / 'auth.json').write_text('untouched')
        (self.home / 'skills/unrelated').mkdir()
        result = self.run_manage('install')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((old / 'SKILL.md').read_text(), 'original v2\n')
        self.assertFalse((old / 'extra.txt').exists())
        self.assertFalse(old.is_symlink())
        self.assertTrue((self.home / 'skills/mine').is_symlink())
        config = tomllib.loads((self.home / 'config.toml').read_text())
        self.assertEqual(config['model'], 'shared')
        self.assertEqual(config['notify'][0], sys.executable)
        self.assertEqual((self.home / 'auth.json').read_text(), 'untouched')
        self.assertTrue((self.home / 'skills/unrelated').exists())
        backups = list(self.home.glob('backups/codex-config/*'))
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / 'skills/demo/SKILL.md').read_text(), 'my old fork\n')
        self.assertEqual(self.run_manage('install').returncode, 0)
        self.assertEqual(list(self.home.glob('backups/codex-config/*')), backups)
        self.assertFalse((self.repo / 'skills/upstream').exists())

    def test_dry_run_is_offline_and_writes_nothing(self):
        shutil.rmtree(self.remote)
        result = self.run_manage('install', '--dry-run')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.home.exists())

    def test_update_fetches_and_applies_latest_without_changing_requirements(self):
        before = self.requirements.read_bytes()
        self.assertEqual(self.run_manage('install').returncode, 0)
        (self.remote / 'demo/SKILL.md').write_text('new upstream content\n')
        result = self.run_manage('update')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.home / 'skills/demo/SKILL.md').read_text(), 'new upstream content\n')
        self.assertEqual(self.requirements.read_bytes(), before)

    def test_failed_fetch_leaves_existing_config_untouched(self):
        self.home.mkdir()
        config = self.home / 'config.toml'
        config.write_text('model = "previous"\n')
        shutil.rmtree(self.remote)
        result = self.run_manage('install')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(config.read_text(), 'model = "previous"\n')
        self.assertFalse((self.home / 'backups').exists())

    def test_apply_failure_restores_config_and_notify(self):
        self.home.mkdir()
        (self.home / 'config.toml').write_text('model = "previous"\n')
        (self.home / 'notify.py').write_text('previous notifier\n')
        (self.home / 'skills').write_text('blocks directory creation\n')
        result = self.run_manage('install')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.home / 'config.toml').read_text(), 'model = "previous"\n')
        self.assertEqual((self.home / 'notify.py').read_text(), 'previous notifier\n')
        self.assertEqual((self.home / 'skills').read_text(), 'blocks directory creation\n')

    def test_rejects_path_escape_and_duplicate_name_before_install(self):
        data = json.loads(self.requirements.read_text())
        data['../outside'] = data.pop('demo')
        self.requirements.write_text(json.dumps(data))
        result = self.run_manage('install')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.home.exists())
        data['demo'] = data.pop('../outside')
        data['mine'] = data.pop('demo')
        self.requirements.write_text(json.dumps(data))
        result = self.run_manage('install')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Duplicate', result.stderr)
        self.assertFalse(self.home.exists())

    def test_upstream_symlink_is_rejected(self):
        (self.remote / 'demo/escape').symlink_to('/tmp')
        data = json.loads(self.requirements.read_text())
        self.requirements.write_text(json.dumps(data))
        result = self.run_manage('install')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.home.exists())

    def test_install_rejects_repository_as_home(self):
        self.home = self.repo
        result = self.run_manage('install')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('repository', result.stderr)

    def test_ancestor_symlink_cannot_move_custom_source(self):
        self.home.mkdir()
        (self.home / 'skills').symlink_to(self.repo / 'skills/custom')
        result = self.run_manage('install')
        self.assertNotEqual(result.returncode, 0)
        source = self.repo / 'skills/custom/mine'
        self.assertFalse(source.is_symlink())
        self.assertEqual((source / 'SKILL.md').read_text(), 'custom\n')
        self.assertFalse((self.home / 'config.toml').exists())

    def test_upstream_executable_bit_change_is_installed(self):
        script = self.remote / 'demo/run.sh'
        script.write_text('#!/bin/sh\nexit 0\n')
        script.chmod(0o644)
        data = json.loads(self.requirements.read_text())
        self.requirements.write_text(json.dumps(data))
        self.assertEqual(self.run_manage('install').returncode, 0)
        script.chmod(0o755)
        self.requirements.write_text(json.dumps(data))
        result = self.run_manage('install')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.home / 'skills/demo/run.sh').stat().st_mode & 0o111, 0o111)


if __name__ == '__main__':
    unittest.main()
