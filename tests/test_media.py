"""A portfolio graphic must not imply evidence its input does not establish."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from demo.__main__ import FIXTURES
from demo.workflows import run_demo
from scripts import render_portfolio_media as media
from scripts.render_demo_walkthrough import load_workflow
from test_workflows import NOW


class MediaEvidenceTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        for workflow, source in FIXTURES.items():
            run_demo(workflow, source, self.root / 'output/demo' / workflow, NOW)
            run_demo(workflow, source, self.root / 'output/blocked' / workflow, NOW, blocked=True)

    def render(self):
        with patch.object(media, 'ROOT', self.root), patch.object(media, 'OUT', self.root / 'images'):
            media.preview(False)

    def change_blocked(self, mutate):
        path = self.root / 'output/blocked/avaya/evidence.json'
        evidence = json.loads(path.read_text(encoding='utf-8'))
        mutate(evidence)
        path.write_text(json.dumps(evidence), encoding='utf-8')

    def test_actual_demo_evidence_generates_preview(self):
        self.render()
        output = (self.root / 'images/demo-preview.svg').read_text(encoding='utf-8')
        self.assertIn('14 total records', output)
        self.assertIn('9 total records', output)

    def test_changed_input_cannot_render_retention_claim(self):
        self.change_blocked(lambda evidence: evidence.update(input_unchanged=False))
        with self.assertRaisesRegex(RuntimeError, 'input remained unchanged'):
            self.render()
        self.assertFalse((self.root / 'images/demo-preview.svg').exists())

    def test_other_blocked_reason_cannot_render_tamper_claim(self):
        self.change_blocked(lambda evidence: evidence['workbooks'][0].update(reason='Invalid input schema'))
        with self.assertRaisesRegex(RuntimeError, 'content rejection and retention'):
            self.render()
        self.assertFalse((self.root / 'images/demo-preview.svg').exists())

    def test_walkthrough_reads_generated_values(self):
        result = load_workflow(self.root, 'avaya')
        self.assertEqual([sheet['row_count'] for sheet in result['sheets']], [1, 13])
        self.assertEqual(result['sheets'][1]['rows'][0][0], '2026-08-04 09:00:00')
        run_demo('avaya', FIXTURES['avaya'], self.root / 'output/demo/avaya', NOW)
        repeat = load_workflow(self.root, 'avaya')
        self.assertEqual(repeat['evidence']['demo']['status'], 'NO_CHANGE')

    def test_walkthrough_rejects_changed_artifact(self):
        path = self.root / 'output/blocked/avaya/2026-08.xlsx'
        path.write_bytes(path.read_bytes() + b'changed since evidence capture')
        with self.assertRaisesRegex(ValueError, 'changed since evidence capture'):
            load_workflow(self.root, 'avaya')
