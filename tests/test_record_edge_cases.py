"""Evidence constraints found during the independent architecture audit."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from test_skill_helpers import SCRIPTS, fixture, records


class RecordEdgeCases(unittest.TestCase):
    def test_blank_or_boolean_calculation_is_not_a_method(self):
        for calculation in ("   ", True):
            data = fixture()
            data["cases"][0]["fields"]["work_duration_before_application"].update(
                value=12,
                status="calculated",
                source_ids=["S1"],
                evidence=[{"source_id": "S1", "locator": "work dates"}],
                cutoff="2025-01",
                calculation=calculation,
            )
            with self.subTest(calculation=calculation):
                self.assertTrue(records.validate(data))

    def test_nested_overflowing_number_is_rejected(self):
        data = fixture()
        data["cases"][0]["fields"]["undergraduate_school"]["note"] = {
            "overflow": json.loads("1e309")
        }
        self.assertTrue(records.validate(data))

    def test_cli_rejects_overflowing_json_number(self):
        data = fixture()
        data["cases"][0]["fields"]["undergraduate_school"]["note"] = {
            "overflow": "OVERFLOW"
        }
        content = json.dumps(data).replace('"OVERFLOW"', "1e309")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "overflow.json"
            path.write_text(content, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "validate_cases.py"), str(path)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("non-finite", result.stderr)

    def test_unknown_field_cannot_be_sole_member_source(self):
        data = fixture()
        source = copy.deepcopy(data["sources"][0])
        source["id"] = "S2"
        data["sources"].append(source)
        data["cases"][0]["fields"]["undergraduate_school"].update(
            source_ids=["S2"],
            evidence=[{"source_id": "S2", "locator": "unknown school"}],
        )
        data["archetypes"][0].update(
            source_ids=["S2"],
            evidence=[{"source_id": "S2", "locator": "unknown school"}],
        )
        self.assertTrue(records.validate(data))


class MonthJsonEdgeCases(unittest.TestCase):
    def test_month_cli_rejects_overflow_even_in_optional_note(self):
        content = '{"cutoff":"2021-01","intervals":[],"note":{"value":1e309}}'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "overflow.json"
            path.write_text(content, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "work_months.py"), str(path)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("non-finite", result.stderr)
