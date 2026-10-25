"""Gemini extension metadata and public MCP pin validation."""
import json
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]

class GeminiExtensionTests(unittest.TestCase):
    def test_manifest_and_context(self):
        data = json.loads((ROOT/'gemini-extension.json').read_text())
        self.assertEqual(data['name'], 'cription')
        server = data['mcpServers']['cription']
        self.assertEqual(server['command'], 'uvx')
        self.assertEqual(server['args'], ['--from', 'git+https://github.com/msandroid/cription-mcp@v0.5.0', 'cription-mcp'])
        self.assertIn('transcribe_audio', (ROOT/'GEMINI.md').read_text())
        self.assertNotIn('industry-workflows', (ROOT/'GEMINI.md').read_text())
