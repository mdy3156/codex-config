import copy
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


class PluginTests(unittest.TestCase):
    def setUp(self):
        path = Path(__file__).resolve().parents[1] / 'plugin_setup.py'
        self.assertTrue(path.is_file(), 'Plugin installation support is required')
        spec = importlib.util.spec_from_file_location('plugin_setup', path)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.specs = {
            'codex_version': '0.162.1',
            'marketplaces': {
                'demo': {'type': 'git', 'source': 'https://example.invalid/demo.git', 'ref': 'main'},
                'openai-bundled': {'type': 'runtime'},
                'openai-curated-remote': {'type': 'remote'},
            },
            'plugins': {
                'tool@demo': {'version': '1.0', 'enabled': True},
                'browser@openai-bundled': {'version': '2.0', 'enabled': True},
                'drive@openai-curated-remote': {'version': '3.0', 'enabled': True},
            },
        }

    def test_render_uses_destination_runtime_paths_and_exact_plugin_ids(self):
        roots = {'openai-bundled': str(self.home / 'app runtime')}
        text = self.module.config_sections(self.specs, roots)
        import tomllib
        data = tomllib.loads(text)
        self.assertEqual(data['marketplaces']['openai-bundled']['source'], roots['openai-bundled'])
        self.assertEqual(set(data['plugins']), set(self.specs['plugins']))
        self.assertNotIn('/Users/mdy', text)

    def test_missing_runtime_stops_before_mutating_commands(self):
        calls = []
        def cli(home, *args):
            calls.append(args)
            return {'marketplaces': []}
        with patch.object(self.module, 'cli', side_effect=cli):
            with self.assertRaisesRegex(ValueError, 'openai-bundled'):
                self.module.runtime_roots(self.home, self.specs)
        self.assertTrue(all('add' not in args for args in calls))

    def test_installs_missing_plugins_with_native_commands_and_checks_result(self):
        calls = []
        installed = []
        def cli(home, *args):
            self.assertEqual(home, self.home)
            calls.append(args)
            if args[:2] == ('marketplace', 'add'):
                return {'marketplaceName': 'demo'}
            if args[:2] == ('marketplace', 'upgrade'):
                return {'errors': []}
            if args[0] == 'add':
                plugin_id = args[1]
                item = self.specs['plugins'][plugin_id]
                installed.append({'pluginId': plugin_id, 'installed': True, **item})
                return {'pluginId': plugin_id, 'version': item['version']}
            if args[0] == 'list':
                return {'installed': copy.deepcopy(installed), 'available': []}
            raise AssertionError(args)
        with patch.object(self.module, 'cli', side_effect=cli):
            self.module.install(self.home, self.specs)
        self.assertIn(('marketplace', 'add', 'https://example.invalid/demo.git', '--ref', 'main'), calls)
        self.assertEqual({args[1] for args in calls if args[0] == 'add'}, set(self.specs['plugins']))
        self.assertEqual(self.module.differences(self.specs, installed), [])

    def test_check_accepts_new_versions_but_reports_missing_or_disabled_plugins(self):
        installed = [{'pluginId': k, 'installed': True, **v} for k, v in self.specs['plugins'].items()]
        installed[0]['version'] = '9.0'
        self.assertEqual(self.module.differences(self.specs, installed), [])
        installed.pop()
        installed[1]['enabled'] = False
        self.assertEqual(len(self.module.differences(self.specs, installed)), 2)

    def test_existing_plugins_are_refreshed_even_with_unchanged_version(self):
        calls = []
        installed = [{'pluginId': k, 'installed': True, **v} for k, v in self.specs['plugins'].items()]
        def cli(home, *args):
            calls.append(args)
            if args[:2] == ('marketplace', 'add'):
                return {'marketplaceName': 'demo'}
            if args[:2] == ('marketplace', 'upgrade'):
                return {'errors': []}
            return {'installed': installed}
        with patch.object(self.module, 'cli', side_effect=cli):
            self.module.install(self.home, self.specs)
        self.assertIn(('marketplace', 'upgrade', 'demo'), calls)
        self.assertEqual({args[1] for args in calls if args[0] == 'add'}, set(self.specs['plugins']))

    def test_upgrade_errors_stop_before_installing_plugins(self):
        with patch.object(self.module, 'cli', side_effect=[{'marketplaceName': 'demo'}, {'errors': ['fetch failed']}]) as cli:
            with self.assertRaisesRegex(ValueError, 'fetch failed'):
                self.module.install(self.home, self.specs)
            self.assertEqual(cli.call_count, 2)

    def test_switch_from_pinned_marketplace_uses_native_reregistration(self):
        self.specs['plugins'] = {'tool@demo': {'enabled': True}}
        installed = [{'pluginId': 'tool@demo', 'enabled': True}]
        conflict = ValueError("marketplace 'demo' is already added from a different source; remove it before adding this source")
        with patch.object(self.module, 'cli', side_effect=[conflict, {}, {'marketplaceName': 'demo'},
                                                         {'errors': []}, {}, {'installed': installed}]) as cli:
            self.module.install(self.home, self.specs)
        self.assertEqual(cli.call_args_list[1].args, (self.home, 'marketplace', 'remove', 'demo'))

    def test_inventory_warning_does_not_become_complete_snapshot(self):
        import subprocess
        result = subprocess.CompletedProcess([], 0, '{"installed": []}', 'Warning: failed to list remote marketplace plugins')
        with patch.object(self.module.subprocess, 'run', return_value=result):
            with self.assertRaisesRegex(ValueError, 'failed to list'):
                self.module.cli(self.home, 'list')

    def test_cli_sets_only_the_requested_codex_home(self):
        import subprocess
        result = subprocess.CompletedProcess([], 0, '{}', '')
        captured = {}
        def run(command, **kwargs):
            captured.update(command=command, **kwargs)
            return result
        with patch.object(self.module.subprocess, 'run', side_effect=run):
            self.module.cli(self.home, 'add', 'tool@demo')
        self.assertEqual(captured['env']['CODEX_HOME'], str(self.home))
        self.assertEqual(captured['command'], ['codex', 'plugin', 'add', 'tool@demo', '--json'])

    def test_export_omits_machine_paths_and_version_pins(self):
        rows = [
            {'pluginId': 'browser@openai-bundled', 'version': '2.0', 'enabled': True,
             'source': {'source': 'local', 'path': '/Users/someone/private/cache/browser'}},
            {'pluginId': 'tool@demo', 'version': '1.0', 'enabled': True,
             'marketplaceSource': {'sourceType': 'git', 'source': 'https://example.invalid/demo.git'}},
            {'pluginId': 'drive@openai-curated-remote', 'version': '3.0', 'enabled': True,
             'source': {'source': 'remote', 'id': 'account-private-id'}},
        ]
        def cli(home, *args):
            if args[0] == 'list':
                return {'installed': rows}
            return {'marketplaces': [{'name': 'demo', 'root': '/machine/cache/demo'}]}
        with patch.object(self.module, 'cli', side_effect=cli), patch.object(
                self.module.subprocess, 'check_output', side_effect=['codex-cli 0.162.1\n', 'a' * 40 + '\n']):
            data = self.module.snapshot(self.home)
        self.assertEqual(data['marketplaces']['demo']['source'], 'https://example.invalid/demo.git')
        self.assertNotIn('revision', json.dumps(data))
        self.assertNotIn('version', json.dumps(data))
        self.assertEqual(set(data['plugins']), set(self.specs['plugins']))
        self.assertNotIn('/Users/', json.dumps(data))
        self.assertNotIn('account-private-id', json.dumps(data))


if __name__ == '__main__':
    unittest.main()
