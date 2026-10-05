"""A benchmark check must fail closed on missing runs and wrong decisions."""

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check_decisions.py")


class DecisionChecksTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        packet = b'{"items":[{"id":"T01"}]}'
        (self.root / "packet.json").write_bytes(packet)
        self.write(
            "oracle.json",
            {
                "packet_sha256": hashlib.sha256(packet).hexdigest(),
                "expected": {"T01": "no"},
            },
        )
        self.write(
            "execution.json",
            {
                "independent_sessions": [{"output": "model-run1.json"}],
                "same_context_repeats": [],
            },
        )
        self.rows = [
            {"id": "T01", "decision": "no", "rationale": "Insufficient source evidence"}
        ]
        self.write("model-run1.json", {"rows": self.rows})

    def write(self, name, value):
        (self.root / name).write_text(json.dumps(value))

    def run_check(self):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(self.root)],
            capture_output=True,
            text=True,
        )

    def test_valid_complete_run(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["scores"][0]["matched"], 1)

    def test_wrong_decision_fails_with_failed_id(self):
        self.rows[0]["decision"] = "yes"
        self.write("model-run1.json", {"rows": self.rows})
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["scores"][0]["failures"], ["T01"])

    def test_missing_run_fails(self):
        (self.root / "model-run1.json").unlink()
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing=", result.stderr)

    def test_unlisted_run_fails(self):
        self.write("extra-run1.json", {"rows": self.rows})
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("extra=", result.stderr)

    def test_duplicate_question_fails(self):
        self.write("model-run1.json", {"rows": self.rows * 2})
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate", result.stderr)

    def test_input_tampering_fails(self):
        (self.root / "packet.json").write_text("{}")
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("input changed", result.stderr)
