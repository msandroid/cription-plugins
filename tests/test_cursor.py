import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('install_cursor', ROOT / 'scripts/install_cursor.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class CursorPluginTests(unittest.TestCase):
    def test_manifest_and_marketplace_resolve(self):
        market = json.loads((ROOT / '.cursor-plugin/marketplace.json').read_text())
        self.assertEqual(len(market['plugins']), 1)
        entry = market['plugins'][0]
        plugin = ROOT / entry['source']
        manifest = json.loads((plugin / '.cursor-plugin/plugin.json').read_text())
        self.assertEqual(entry['name'], manifest['name'])
        self.assertEqual(entry['version'], manifest['version'])
        config = json.loads((plugin / manifest['mcpServers']).read_text())
        self.assertEqual(config, json.loads((plugin / '.mcp.json').read_text()))
        for path in manifest['skills']:
            self.assertTrue((plugin / path / 'SKILL.md').is_file())

    def test_install_is_idempotent_preserves_other_plugins_and_excludes_unreleased_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / 'local/cription'
            other = Path(tmp) / 'local/other/important.txt'
            other.parent.mkdir(parents=True); other.write_text('preserve')
            source = ROOT / 'plugins/cription'
            installer.install(destination, source, '/Python With Spaces/uvx')
            self.assertIsNone(installer.install(destination, source, '/Python With Spaces/uvx'))
            config = json.loads((destination / 'mcp.json').read_text())
            self.assertEqual(config['mcpServers']['cription']['command'], '/Python With Spaces/uvx')
            self.assertEqual({p.name for p in (destination / 'skills').iterdir()}, set(installer.SKILLS))
            self.assertEqual(other.read_text(), 'preserve')
            (destination / 'local-change.txt').write_text('custom')
            with self.assertRaises(ValueError):
                installer.install(destination, source, '/uvx')
            backup = installer.install(destination, source, '/uvx', replace=True)
            self.assertEqual((backup / 'local-change.txt').read_text(), 'custom')
            self.assertFalse((destination / 'local-change.txt').exists())
            self.assertEqual(other.read_text(), 'preserve')

    def test_symlink_install_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'cription'; path.symlink_to(ROOT / 'plugins/cription')
            with self.assertRaises(ValueError):
                installer.install(path, ROOT / 'plugins/cription', '/uvx', replace=True)
