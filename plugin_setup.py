"""Reproduce plugin selections through the official Codex CLI, without copying caches."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import tomllib

RUNTIME_MARKETPLACES = {'openai-bundled', 'openai-primary-runtime', 'openai-bundled-alpha'}


def validate(data):
    for name, spec in data['marketplaces'].items():
        if not re.fullmatch(r'[a-z0-9][a-z0-9_-]*', name):
            raise ValueError(f'Invalid marketplace: {name}')
        if spec['type'] == 'git':
            if not spec['source'].startswith(('https://', 'ssh://', 'git@')):
                raise ValueError(f'Marketplace source must be a portable Git URL: {name}')
            if 'ref' in spec and (not isinstance(spec['ref'], str) or not spec['ref'] or spec['ref'].startswith('-')):
                raise ValueError(f'Invalid marketplace branch: {name}')
        elif spec['type'] not in ('runtime', 'remote'):
            raise ValueError(f'Unsupported marketplace type: {name}')
    for group in ('plugins', 'app_plugins'):
        for selector, spec in data.get(group, {}).items():
            if not re.fullmatch(r'[a-z0-9][a-z0-9_-]*@[a-z0-9][a-z0-9_-]*', selector):
                raise ValueError(f'Invalid plugin selector: {selector}')
            name = selector.split('@')[1]
            if name not in data['marketplaces']:
                raise ValueError(f'Missing marketplace for {selector}')
            if (data['marketplaces'][name]['type'] == 'runtime') != (group == 'app_plugins'):
                raise ValueError(f'{selector}: app/runtime preferences belong in app_plugins; other plugins belong in plugins')
            if not isinstance(spec['enabled'], bool):
                raise ValueError(f'Invalid plugin enabled state: {selector}')
    return data


def cli(home, *args):
    executable = shutil.which('codex.exe' if os.name == 'nt' else 'codex') or shutil.which('codex.cmd') or 'codex'
    result = subprocess.run([executable, 'plugin', *args, '--json'],
                            env={**os.environ, 'CODEX_HOME': str(home)},
                            capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode or 'failed to list remote marketplace' in result.stderr.lower():
        raise ValueError(f"codex plugin {' '.join(args)}: {result.stderr.strip()}")
    return json.loads(result.stdout)


def runtime_roots(home, specs):
    required = {selector.split('@')[1] for selector in specs.get('app_plugins', {})}
    if not required:
        return {}
    rows = cli(home, 'marketplace', 'list')['marketplaces']
    roots = {item['name']: item['root'] for item in rows
             if item['name'] in required and Path(item['root']).is_dir()}
    cache = Path(os.environ.get('XDG_CACHE_HOME', Path.home() / '.cache'))
    for name in required - roots.keys():
        root = (cache / 'codex-runtimes/codex-primary-runtime/plugins' / name if name == 'openai-primary-runtime'
                else home / '.tmp/bundled-marketplaces' / name)
        if (root / '.agents/plugins/marketplace.json').is_file():
            roots[name] = str(root)
    return roots


def resolve(home, specs):
    roots = runtime_roots(home, specs)
    available = set()
    # Desktop-only entries can be absent from CLI inventories; use the app-owned catalog.
    for name, root in roots.items():
        catalog = json.loads((Path(root) / '.agents/plugins/marketplace.json').read_text(encoding='utf-8'))
        if catalog['name'] != name:
            raise ValueError(f'App marketplace name mismatch: expected {name}')
        available.update(f'{item["name"]}@{name}' for item in catalog['plugins']
                         if item.get('policy', {}).get('installation') != 'NOT_AVAILABLE')
    selected = {}
    for selector, spec in specs.get('app_plugins', {}).items():
        if selector in available:
            selected[selector] = spec
        else:
            print(f'App preference retained for another environment/release: {selector}')
    print(f'Targets: {len(specs["plugins"])} common plugins, {len(selected)} app-plugin preferences.')
    return {**specs, 'app_plugins': selected}, roots


def config_sections(specs, roots):
    sections = []
    for name, root in sorted(roots.items()):
        sections.append(f'[marketplaces.{json.dumps(name)}]\nsource_type = "local"\nsource = {json.dumps(root)}')
    for selector, spec in sorted((specs['plugins'] | specs.get('app_plugins', {})).items()):
        sections.append(f'[plugins.{json.dumps(selector)}]\nenabled = {str(spec["enabled"]).lower()}')
    return '\n\n'.join(sections) + '\n'


def differences(specs, installed):
    actual = {item['pluginId']: item for item in installed if item.get('installed', True)}
    result = []
    for selector, expected in (specs['plugins'] | specs.get('app_plugins', {})).items():
        current = actual.get(selector)
        if current is None:
            result.append(f'{selector}: missing')
        elif current['enabled'] != expected['enabled']:
            result.append(f'{selector}: expected enabled={expected["enabled"]}, found enabled={current["enabled"]}')
    return result


def check(home, specs):
    issues = differences({**specs, 'app_plugins': {}}, cli(home, 'list')['installed'])
    if specs.get('app_plugins'):
        settings = tomllib.loads((home / 'config.toml').read_text(encoding='utf-8')).get('plugins', {})
        actual = [{'pluginId': selector, 'enabled': setting.get('enabled', True)} for selector, setting in settings.items()]
        issues += ['App preference ' + issue for issue in differences({'plugins': specs['app_plugins']}, actual)]
    if issues:
        raise ValueError('Plugin environment differs from plugins.json:\n' + '\n'.join(issues))
    print(f'Verified {len(specs["plugins"])} common plugin installations and '
          f'{len(specs.get("app_plugins", {}))} app-plugin settings.')


def install(home, specs):
    plugins = specs['plugins'] | specs.get('app_plugins', {})
    if not plugins:
        return
    for name, spec in specs['marketplaces'].items():
        if spec['type'] == 'git':
            print(f'Refresh marketplace: {name}', flush=True)
            ref_args = ['--ref', spec['ref']] if spec.get('ref') else []
            try:
                result = cli(home, 'marketplace', 'add', spec['source'], *ref_args)
            except ValueError as error:
                if f"marketplace '{name}' is already added from a different source" not in str(error):
                    raise
                # The native CLI requires re-registration when switching from a pinned ref.
                cli(home, 'marketplace', 'remove', name)
                result = cli(home, 'marketplace', 'add', spec['source'], *ref_args)
            if result['marketplaceName'] != name:
                raise ValueError(f'Marketplace name mismatch: expected {name}')
            result = cli(home, 'marketplace', 'upgrade', name)
            if result.get('errors'):
                raise ValueError(f'Marketplace refresh failed: {result["errors"]}')
    for selector in specs['plugins']:
        print(f'Install/update plugin: {selector}', flush=True)
        cli(home, 'add', selector)
    # CLI installs may enable newly added plugins. Restore the recorded states only.
    path = home / 'config.toml'
    if path.exists():
        config = path.read_text(encoding='utf-8')
        for selector, spec in plugins.items():
            header = f'[plugins.{json.dumps(selector)}]'
            pattern = r'(' + re.escape(header) + r'\s*\n\s*enabled\s*=\s*)(true|false)'
            config = re.sub(pattern, lambda match: match[1] + str(spec['enabled']).lower(), config)
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=home, delete=False) as handle:
            temporary = Path(handle.name)
            try:
                handle.write(config)
                handle.close()
                temporary.replace(path)
            finally:
                temporary.unlink(missing_ok=True)
    check(home, specs)


def snapshot(home, previous=None):
    installed = cli(home, 'list')['installed']
    if not installed:
        raise ValueError('No installed plugins returned; refusing to replace the snapshot.')
    app_plugins = dict((previous or {}).get('app_plugins', {}))
    data = {'marketplaces': {selector.split('@')[1]: {'type': 'runtime'} for selector in app_plugins},
            'plugins': {}, 'app_plugins': app_plugins}
    for item in sorted(installed, key=lambda p: p['pluginId']):
        selector = item['pluginId']
        name = selector.split('@')[1]
        if name not in data['marketplaces']:
            source = item.get('marketplaceSource') or {}
            if name in RUNTIME_MARKETPLACES:
                spec = {'type': 'runtime'}
            elif item.get('source', {}).get('source') == 'remote':
                spec = {'type': 'remote'}
            elif source.get('sourceType') == 'git':
                spec = {'type': 'git', 'source': source['source']}
            else:
                raise ValueError(f'Cannot export machine-local marketplace {name}; provide a Git source first.')
            data['marketplaces'][name] = spec
        group = 'app_plugins' if data['marketplaces'][name]['type'] == 'runtime' else 'plugins'
        data[group][selector] = {'enabled': item['enabled']}
    path = home / 'config.toml'
    if path.is_file():
        for selector, setting in tomllib.loads(path.read_text(encoding='utf-8')).get('plugins', {}).items():
            name = selector.split('@')[-1]
            if name in RUNTIME_MARKETPLACES:
                data['marketplaces'][name] = {'type': 'runtime'}
                data['app_plugins'][selector] = {'enabled': setting.get('enabled', True)}
    return validate(data)
