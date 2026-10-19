#!/usr/bin/env python3
"""Install or update public skills, plugins and local configuration (Python 3.11+)."""
import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

import plugin_setup

if sys.version_info < (3, 11):
    sys.exit("Python 3.11+ is required. Try python3.14 manage.py, or set PYTHON for the shell scripts.")
import tomllib

ROOT = Path(__file__).resolve().parent
REQUIREMENTS = ROOT / "skills/requirements.json"
PLUGINS = ROOT / "plugins.json"


def files(directory):
    for path in sorted(directory.rglob("*")):
        if any(part in (".git", "__pycache__") for part in path.relative_to(directory).parts):
            continue
        if path.is_symlink():
            raise ValueError(f"Symlinks inside a skill are not supported: {path}")
        if path.is_file() and path.suffix != ".pyc":
            yield path


def fingerprint(directory):
    digest = hashlib.sha256()
    for path in files(directory):
        digest.update(path.relative_to(directory).as_posix().encode() + b"\0")
        digest.update(str(path.stat().st_mode & 0o111).encode() + b"\0")
        digest.update(path.read_bytes() + b"\0")
    return digest.hexdigest()


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        try:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
            handle.close()
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)


def requirements():
    data = json.loads(REQUIREMENTS.read_text(encoding='utf-8'))
    for name, source in data.items():
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
            raise ValueError(f"Invalid skill name: {name}")
        if not isinstance(source, str) or not source or source.startswith("-"):
            raise ValueError(f"Invalid skill source: {name}")
    return data


def fetch_skills(specs, temporary):
    groups = {}
    for name, source in specs.items():
        groups.setdefault(source, []).append(name)
    staged = {}
    for source, names in groups.items():
        print(f"Fetch latest skills: {', '.join(names)}", flush=True)
        result = subprocess.run(
            [shutil.which('npx.cmd' if sys.platform == 'win32' else 'npx') or 'npx', '--yes', 'skills@latest', 'add', source, '--skill', *names,
             '--agent', 'codex', '--copy', '--yes'],
            cwd=temporary, env={**os.environ, 'DISABLE_TELEMETRY': '1'},
            capture_output=True, text=True, encoding='utf-8', errors='replace')
        if result.returncode:
            raise ValueError(f"skills CLI failed for {source}:\n{result.stdout}\n{result.stderr}")
        for name in names:
            path = temporary / '.agents/skills' / name
            if path.is_symlink() or not (path / 'SKILL.md').is_file():
                raise ValueError(f"skills CLI did not install {name}")
            list(files(path))  # Validate staged files before changing the destination.
            staged[name] = path
    return staged


def apply_install(home, targets):
    backup = home / "backups/codex-config" / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    changed = []
    try:
        for target, source, link in targets:
            if link:
                if target.is_symlink() and target.resolve() == source.resolve():
                    continue
            elif not target.is_symlink():
                if isinstance(source, bytes) and target.is_file() and target.read_bytes() == source:
                    continue
                if isinstance(source, Path) and target.is_dir():
                    try:
                        if fingerprint(target) == fingerprint(source):
                            continue
                    except ValueError:
                        pass  # An existing directory with symlinks must be backed up and replaced.
            print(f"Install {target}")
            saved = None
            if target.exists() or target.is_symlink():
                saved = backup / target.relative_to(home)
                saved.parent.mkdir(parents=True, exist_ok=True)
                target.rename(saved)
                print(f"  backup: {saved}")
            changed.append((target, saved))
            target.parent.mkdir(parents=True, exist_ok=True)
            if link:
                target.symlink_to(source, target_is_directory=source.is_dir())
            elif isinstance(source, bytes):
                atomic_write(target, source)
            else:
                shutil.copytree(source, target)
    except OSError:
        for target, saved in reversed(changed):
            if target.is_symlink() or target.is_file():
                target.unlink()
            elif target.exists():
                shutil.rmtree(target)
            if saved is not None:
                saved.rename(target)
        raise


def install(home, dry_run=False):
    home = home.expanduser().absolute()
    if home.resolve() == ROOT:
        raise ValueError("The repository cannot also be CODEX_HOME; clone it separately.")
    if (home / "skills").resolve().is_relative_to(ROOT):
        raise ValueError("The skills destination points inside the repository; use a separate directory.")
    specs = requirements()
    plugins = plugin_setup.validate(json.loads(PLUGINS.read_text(encoding='utf-8')))
    custom = {p.parent.name: p.parent for p in sorted((ROOT / "skills/custom").glob("*/SKILL.md"))}
    if custom.keys() & specs.keys():
        raise ValueError(f"Duplicate skill names: {sorted(custom.keys() & specs.keys())}")
    config = (ROOT / "config.toml").read_text(encoding='utf-8')
    instructions = (ROOT / "AGENTS.md").read_bytes()
    if {'notify', 'plugins', 'marketplaces'} & tomllib.loads(config).keys():
        raise ValueError("config.toml must omit notify/plugins/marketplaces; the installer generates them.")
    command = [sys.executable, str(home / "notify.py"), "--codex-home", str(home)]
    config = "notify = " + json.dumps(command, ensure_ascii=False) + "\n\n" + config
    tomllib.loads(config)
    if dry_run:
        print(f"Would replace {home / 'config.toml'} and {home / 'AGENTS.md'} and link notify.py")
        for name in custom:
            print(f"Would link local skill: {name}")
        for name, source in specs.items():
            print(f"Would fetch latest {name} from {source} into {home / 'skills' / name}")
        for selector in plugins['plugins']:
            print(f"Would install/update common plugin: {selector}")
        for selector in plugins.get('app_plugins', {}):
            print(f"Would apply app preference when offered by this environment's catalog: {selector}")
        print("Existing conflicting files would be backed up. No network access or writes performed.")
        return
    plugins, runtime = plugin_setup.resolve(home, plugins)
    config += '\n' + plugin_setup.config_sections(plugins, runtime)
    tomllib.loads(config)
    # Finish skill downloads and validation before touching the user's configuration.
    with tempfile.TemporaryDirectory(prefix="codex-config-install-") as directory:
        staged = fetch_skills(specs, Path(directory))
        link = sys.platform != 'win32'
        targets = [(home / "config.toml", config.encode(), False),
                   (home / "AGENTS.md", instructions, False),
                   (home / "notify.py", ROOT / "notify.py" if link else (ROOT / "notify.py").read_bytes(), link)]
        targets += [(home / "skills" / name, source, link) for name, source in custom.items()]
        targets += [(home / "skills" / name, source, False) for name, source in staged.items()]
        apply_install(home, targets)
    plugin_setup.install(home, plugins)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ('install', 'update'):
        installer = commands.add_parser(command, help='Fetch latest skills/plugins and apply config; back up existing files')
        installer.add_argument('--codex-home', type=Path, default=Path(os.environ.get('CODEX_HOME', '~/.codex')))
        installer.add_argument('--dry-run', action='store_true')
    exporter = commands.add_parser('snapshot-plugins', help='Record currently installed plugins without copying credentials or caches')
    exporter.add_argument('--codex-home', type=Path, default=Path(os.environ.get('CODEX_HOME', '~/.codex')))
    checker = commands.add_parser('check-plugins', help='Compare this environment with the recorded plugins')
    checker.add_argument('--codex-home', type=Path, default=Path(os.environ.get('CODEX_HOME', '~/.codex')))
    args = parser.parse_args()
    try:
        if args.command in ("install", "update"):
            install(args.codex_home, args.dry_run)
        elif args.command == 'snapshot-plugins':
            previous = plugin_setup.validate(json.loads(PLUGINS.read_text(encoding='utf-8')))
            data = plugin_setup.snapshot(args.codex_home.expanduser().absolute(), previous)
            atomic_write(PLUGINS, (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode())
            print(f"Recorded {len(data['plugins'])} common plugins and {len(data['app_plugins'])} app preferences in {PLUGINS}")
        else:
            home = args.codex_home.expanduser().absolute()
            plugins = plugin_setup.validate(json.loads(PLUGINS.read_text(encoding='utf-8')))
            plugins, _ = plugin_setup.resolve(home, plugins)
            plugin_setup.check(home, plugins)
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
