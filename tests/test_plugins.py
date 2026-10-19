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
        (self.home / 'config.toml').write_text('[plugins."browser@openai-bundled"]\nenabled = true\n')
        self.specs = {
            'codex_version': '0.162.1',
            'marketplaces': {
                'demo': {'type': 'git', 'source': 'https://example.invalid/demo.git', 'ref': 'main'},
                'openai-bundled': {'type': 'runtime'},
                'openai-curated-remote': {'type': 'remote'},
            },
            'plugins': {
                'tool@demo': {'version': '1.0', 'enabled': True},
                'drive@openai-curated-remote': {'version': '3.0', 'enabled': True},
            },
            'app_plugins': {'browser@openai-bundled': {'enabled': True}},
        }

    def test_render_uses_destination_runtime_paths_and_exact_plugin_ids(self):
        roots = {'openai-bundled': str(self.home / 'app runtime')}
        text = self.module.config_sections(self.specs, roots)
        import tomllib
        data = tomllib.loads(text)
        self.assertEqual(data['marketplaces']['openai-bundled']['source'], roots['openai-bundled'])
        self.assertEqual(set(data['plugins']), {'tool@demo', 'drive@openai-curated-remote', 'browser@openai-bundled'})
        self.assertNotIn('/Users/mdy', text)

    def test_cli_without_app_runtime_still_selects_all_common_plugins(self):
        calls = []
        def cli(home, *args):
            calls.append(args)
            return {'marketplaces': []}
        with patch.object(self.module, 'cli', side_effect=cli):
            selected, roots = self.module.resolve(self.home, self.specs)
        self.assertEqual(roots, {})
        self.assertEqual(set(selected['plugins']), {'tool@demo', 'drive@openai-curated-remote'})
        self.assertEqual(selected['app_plugins'], {})
        self.assertIn('browser@openai-bundled', self.specs['app_plugins'])
        self.assertTrue(all('add' not in args for args in calls))

    def test_app_environment_applies_only_preferences_offered_by_its_catalog(self):
        self.specs['marketplaces']['openai-primary-runtime'] = {'type': 'runtime'}
        self.specs['app_plugins']['documents@openai-primary-runtime'] = {'enabled': True}
        self.specs['app_plugins']['code-review@openai-bundled'] = {'enabled': True}
        self.specs['app_plugins']['browser@openai-bundled']['enabled'] = False
        rows = [{'name': 'openai-bundled', 'root': str(self.home)}]
        catalog = self.home / '.agents/plugins/marketplace.json'
        catalog.parent.mkdir(parents=True)
        catalog.write_text(json.dumps({'name': 'openai-bundled', 'plugins': [
            {'name': 'browser', 'source': {'source': 'local', 'path': './plugins/browser'},
             'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}}]}))
        def cli(home, *args):
            if args == ('marketplace', 'list'):
                return {'marketplaces': rows}
            raise AssertionError(args)
        with patch.object(self.module, 'cli', side_effect=cli):
            selected, roots = self.module.resolve(self.home, self.specs)
        self.assertEqual(selected['app_plugins'], {'browser@openai-bundled': {'enabled': False}})
        self.assertEqual(roots, {'openai-bundled': str(self.home)})
        issues = self.module.differences(selected, [
            {'pluginId': 'tool@demo', 'enabled': True},
            {'pluginId': 'drive@openai-curated-remote', 'enabled': True},
        ])
        self.assertEqual(issues, ['browser@openai-bundled: missing'])

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
                item = (self.specs['plugins'] | self.specs['app_plugins'])[plugin_id]
                installed.append({'pluginId': plugin_id, 'installed': True, **item})
                return {'pluginId': plugin_id}
            if args[0] == 'list':
                return {'installed': copy.deepcopy(installed), 'available': []}
            raise AssertionError(args)
        with patch.object(self.module, 'cli', side_effect=cli):
            self.module.install(self.home, self.specs)
        self.assertIn(('marketplace', 'add', 'https://example.invalid/demo.git', '--ref', 'main'), calls)
        self.assertEqual({args[1] for args in calls if args[0] == 'add'}, {'tool@demo', 'drive@openai-curated-remote'})
        self.assertEqual(self.module.differences({**self.specs, 'app_plugins': {}}, installed), [])

    def test_app_catalog_in_destination_home_is_found_without_cli_registration(self):
        root = self.home / '.tmp/bundled-marketplaces/openai-bundled'
        catalog = root / '.agents/plugins/marketplace.json'
        catalog.parent.mkdir(parents=True)
        catalog.write_text(json.dumps({'name': 'openai-bundled', 'plugins': [
            {'name': 'browser', 'source': {'source': 'local', 'path': './plugins/browser'},
             'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}}]}))
        def cli(home, *args):
            if args == ('marketplace', 'list'):
                return {'marketplaces': []}
            raise AssertionError(args)
        with patch.object(self.module, 'cli', side_effect=cli):
            selected, roots = self.module.resolve(self.home, self.specs)
        self.assertEqual(roots, {'openai-bundled': str(root)})
        self.assertEqual(selected['app_plugins'], {'browser@openai-bundled': {'enabled': True}})

    def test_app_preferences_cannot_accidentally_become_common_dependencies(self):
        self.specs['plugins'].update(self.specs.pop('app_plugins'))
        with self.assertRaisesRegex(ValueError, 'app_plugins'):
            self.module.validate(self.specs)

    def test_check_rejects_an_app_preference_that_was_not_applied(self):
        (self.home / 'config.toml').write_text('[plugins."browser@openai-bundled"]\nenabled = false\n')
        installed = [{'pluginId': selector, 'enabled': True} for selector in
                     ('tool@demo', 'drive@openai-curated-remote', 'browser@openai-bundled')]
        with patch.object(self.module, 'cli', return_value={'installed': installed}):
            with self.assertRaisesRegex(ValueError, 'App preference browser@openai-bundled'):
                self.module.check(self.home, self.specs)

    def test_check_accepts_new_versions_but_reports_missing_or_disabled_plugins(self):
        installed = [{'pluginId': k, 'installed': True, **v} for k, v in (self.specs['plugins'] | self.specs['app_plugins']).items()]
        installed[0]['version'] = '9.0'
        self.assertEqual(self.module.differences(self.specs, installed), [])
        installed.pop()
        installed[1]['enabled'] = False
        self.assertEqual(len(self.module.differences(self.specs, installed)), 2)

    def test_existing_plugins_are_refreshed_even_with_unchanged_version(self):
        calls = []
        installed = [{'pluginId': k, 'installed': True, **v} for k, v in (self.specs['plugins'] | self.specs['app_plugins']).items()]
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
        self.assertEqual({args[1] for args in calls if args[0] == 'add'}, {'tool@demo', 'drive@openai-curated-remote'})

    def test_upgrade_errors_stop_before_installing_plugins(self):
        with patch.object(self.module, 'cli', side_effect=[{'marketplaceName': 'demo'}, {'errors': ['fetch failed']}]) as cli:
            with self.assertRaisesRegex(ValueError, 'fetch failed'):
                self.module.install(self.home, self.specs)
            self.assertEqual(cli.call_count, 2)

    def test_switch_from_pinned_marketplace_uses_native_reregistration(self):
        self.specs['plugins'] = {'tool@demo': {'enabled': True}}
        self.specs['app_plugins'] = {}
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
        with patch.object(self.module.subprocess, 'run', side_effect=run), \
                patch.object(self.module.shutil, 'which', return_value='/installed/codex'):
            self.module.cli(self.home, 'add', 'tool@demo')
        self.assertEqual(captured['env']['CODEX_HOME'], str(self.home))
        self.assertEqual(captured['command'], ['/installed/codex', 'plugin', 'add', 'tool@demo', '--json'])

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
        self.assertEqual(data['app_plugins'], {'browser@openai-bundled': {'enabled': True}})
        self.assertNotIn('/Users/', json.dumps(data))
        self.assertNotIn('account-private-id', json.dumps(data))

    def test_snapshot_from_cli_keeps_other_environments_app_preferences(self):
        rows = [{'pluginId': 'tool@demo', 'enabled': True,
                 'marketplaceSource': {'sourceType': 'git', 'source': 'https://example.invalid/demo.git'}}]
        with patch.object(self.module, 'cli', return_value={'installed': rows}):
            data = self.module.snapshot(self.home, self.specs)
        self.assertEqual(data['app_plugins'], {'browser@openai-bundled': {'enabled': True}})
        self.assertEqual(data['marketplaces']['openai-bundled'], {'type': 'runtime'})
        self.assertNotIn('browser@openai-bundled', data['plugins'])


if __name__ == '__main__':
    unittest.main()
