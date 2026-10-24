#!/usr/bin/env python3
"""Install the native Cursor plugin into Cursor's documented local plugin folder."""
import argparse
import datetime
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

SKILLS = ('transcribe', 'summarize-transcript', 'cription-notes')


def find_uvx():
    binary = shutil.which('uvx')
    if binary:
        return str(Path(binary).absolute())
    for path in (Path.home() / '.local/bin/uvx', Path('/opt/homebrew/bin/uvx'), Path('/usr/local/bin/uvx')):
        if path.is_file() and os.access(path, os.X_OK):
            return str(path.absolute())
    raise ValueError('Install uv first (brew install uv), then rerun this script')


def install(destination, source, uvx, replace=False):
    destination, source = Path(destination), Path(source)
    files = [Path('.cursor-plugin/plugin.json'), Path('mcp.json')]
    files += [Path('skills') / name / 'SKILL.md' for name in SKILLS]
    contents = {path: (source / path).read_text(encoding='utf-8') for path in files}
    manifest = json.loads(contents[Path('.cursor-plugin/plugin.json')])
    if manifest['name'] != 'cription' or manifest['skills'] != ['./skills/' + name for name in SKILLS]:
        raise ValueError('Unexpected Cursor plugin manifest')
    config = json.loads(contents[Path('mcp.json')])
    config['mcpServers']['cription']['command'] = uvx
    contents[Path('mcp.json')] = json.dumps(config, indent=2) + '\n'
    if destination.is_symlink():
        raise ValueError('Refusing to replace a plugin symlink: %s' % destination)
    if destination.exists():
        actual = {p.relative_to(destination) for p in destination.rglob('*') if p.is_file()}
        if actual == set(files) and all((destination / p).read_text(encoding='utf-8') == text for p, text in contents.items()):
            return None
        if not replace:
            raise ValueError('Plugin already exists; use --replace to update it with a backup')
    destination.parent.mkdir(parents=True, exist_ok=True)
    backup = None
    with tempfile.TemporaryDirectory(prefix='.cription-stage-', dir=str(destination.parent.parent)) as tmp:
        stage = Path(tmp) / 'cription'
        for path, text in contents.items():
            target = stage / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding='utf-8')
        if destination.exists():
            backups = destination.parent.parent / 'backups'
            backups.mkdir(exist_ok=True)
            backup = backups / ('cription-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
            destination.rename(backup)
        try:
            stage.rename(destination)
        except OSError:
            if backup:
                backup.rename(destination)
            raise
    return backup


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replace', action='store_true', help='Back up and replace an existing local Cription plugin')
    args = parser.parse_args(argv)
    try:
        source = Path(__file__).resolve().parents[1] / 'plugins/cription'
        destination = Path.home() / '.cursor/plugins/local/cription'
        standalone = Path.home() / '.cursor/mcp.json'
        if standalone.exists():
            data = json.loads(standalone.read_text(encoding='utf-8'))
            if 'cription' in data.get('mcpServers', {}):
                raise ValueError('Standalone Cription MCP is already configured in ~/.cursor/mcp.json. Remove only its cription entry before installing the plugin to avoid duplicate tools')
        backup = install(destination, source, find_uvx(), args.replace)
        print('Cursor plugin installed: %s' % destination)
        if backup:
            print('Backup: %s' % backup)
        print('Restart Cursor or run Developer: Reload Window. In Customize, confirm Cription, three skills and eight MCP tools. Local plugin imports must be allowed by your administrator.')
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print('install_cursor: %s' % error, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
