"""Reproduce plugin selections through the official Codex CLI, without copying caches."""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

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
    for selector, spec in data['plugins'].items():
        if not re.fullmatch(r'[a-z0-9][a-z0-9_-]*@[a-z0-9][a-z0-9_-]*', selector):
            raise ValueError(f'Invalid plugin selector: {selector}')
        if selector.split('@')[1] not in data['marketplaces']:
            raise ValueError(f'Missing marketplace for {selector}')
        if not isinstance(spec['enabled'], bool):
            raise ValueError(f'Invalid plugin enabled state: {selector}')
    return data


def cli(home, *args):
    result = subprocess.run(['codex', 'plugin', *args, '--json'],
                            env={**os.environ, 'CODEX_HOME': str(home)},
                            capture_output=True, text=True)
    if result.returncode or 'failed to list remote marketplace' in result.stderr.lower():
        raise ValueError(f"codex plugin {' '.join(args)}: {result.stderr.strip()}")
    return json.loads(result.stdout)


def runtime_roots(home, specs):
    required = {name for name, spec in specs['marketplaces'].items() if spec['type'] == 'runtime'}
    if not required:
        return {}
    rows = cli(home, 'marketplace', 'list')['marketplaces']
    roots = {item['name']: item['root'] for item in rows if item['name'] in required and Path(item['root']).is_dir()}
    missing = required - roots.keys()
    if missing:
        raise ValueError('Missing app/runtime marketplaces: ' + ', '.join(sorted(missing)) +
                         '. Start the Codex desktop app with this CODEX_HOME, then retry; no settings were replaced.')
    return roots


def config_sections(specs, roots):
    sections = []
    for name, root in sorted(roots.items()):
        sections.append(f'[marketplaces.{json.dumps(name)}]\nsource_type = "local"\nsource = {json.dumps(root)}')
    for selector, spec in sorted(specs['plugins'].items()):
        sections.append(f'[plugins.{json.dumps(selector)}]\nenabled = {str(spec["enabled"]).lower()}')
    return '\n\n'.join(sections) + '\n'


def differences(specs, installed):
    actual = {item['pluginId']: item for item in installed if item.get('installed', True)}
    result = []
    for selector, expected in specs['plugins'].items():
        current = actual.get(selector)
        if current is None:
            result.append(f'{selector}: missing')
        elif current['enabled'] != expected['enabled']:
            result.append(f'{selector}: expected enabled={expected["enabled"]}, found enabled={current["enabled"]}')
    return result


def check(home, specs):
    issues = differences(specs, cli(home, 'list')['installed'])
    if issues:
        raise ValueError('Plugin environment differs from plugins.json:\n' + '\n'.join(issues))
    print(f'All {len(specs["plugins"])} plugins are installed with the requested enabled states.')


def install(home, specs):
    if not specs['plugins']:
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
        config = path.read_text()
        for selector, spec in specs['plugins'].items():
            header = f'[plugins.{json.dumps(selector)}]'
            pattern = r'(' + re.escape(header) + r'\s*\n\s*enabled\s*=\s*)(true|false)'
            config = re.sub(pattern, lambda match: match[1] + str(spec['enabled']).lower(), config)
        with tempfile.NamedTemporaryFile(mode='w', dir=home, delete=False) as handle:
            temporary = Path(handle.name)
            try:
                handle.write(config)
                handle.close()
                temporary.replace(path)
            finally:
                temporary.unlink(missing_ok=True)
    check(home, specs)


def snapshot(home):
    installed = cli(home, 'list')['installed']
    if not installed:
        raise ValueError('No installed plugins returned; refusing to replace the snapshot.')
    data = {'marketplaces': {}, 'plugins': {}}
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
        data['plugins'][selector] = {'enabled': item['enabled']}
    return validate(data)
