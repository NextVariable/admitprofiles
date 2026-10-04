"""Adversarial record tests and deterministic date-calculation tests."""

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/admission-intelligence/scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


records = load("validate_cases")
months = load("work_months")


def fixture():
    fields = {
        k: {"value": None, "status": "unknown", "source_ids": [], "evidence": []}
        for k in records.FIELDS
    }
    fields["enrollment_status"] = {
        "value": "enrolled",
        "status": "documented",
        "source_ids": ["S1"],
        "evidence": [{"source_id": "S1", "locator": "student introduction"}],
    }
    return {
        "schema_version": "1.1",
        "scope": {
            "institution": "Synthetic University",
            "program": "Synthetic Program",
        },
        "researched_on": "2026-10-05",
        "sources": [
            {
                "id": "S1",
                "url": "https://example.org/student",
                "title": "Synthetic test only",
                "source_type": "official_profile",
                "accessed_on": "2026-10-05",
                "access_state": "full_text",
                "locator": "student introduction",
            }
        ],
        "cases": [
            {
                "id": "C1",
                "identity_link": {
                    "basis": "synthetic direct link",
                    "source_ids": ["S1"],
                    "evidence": [
                        {"source_id": "S1", "locator": "student introduction"}
                    ],
                },
                "fields": fields,
                "experiences": [],
                "conflicts": [],
            }
        ],
        "archetypes": [
            {
                "label": "test only",
                "status": "inferred",
                "case_ids": ["C1"],
                "source_ids": ["S1"],
                "evidence": [{"source_id": "S1", "locator": "student introduction"}],
            }
        ],
    }


class RecordTests(unittest.TestCase):
    def test_valid_minimal_record(self):
        self.assertEqual(records.validate(fixture()), [])

    def test_unknown_zero_is_rejected(self):
        data = fixture()
        data["cases"][0]["fields"]["work_duration_before_application"]["value"] = 0
        self.assertTrue(any("unknown value" in e for e in records.validate(data)))

    def test_dangling_source(self):
        data = fixture()
        data["cases"][0]["fields"]["enrollment_status"]["source_ids"] = ["S9"]
        self.assertTrue(any("unknown source" in e for e in records.validate(data)))

    def test_duplicate_source_id(self):
        data = fixture()
        data["sources"].append(copy.deepcopy(data["sources"][0]))
        self.assertTrue(any("duplicate id" in e for e in records.validate(data)))

    def test_missing_field_locator(self):
        data = fixture()
        data["cases"][0]["fields"]["enrollment_status"]["evidence"] = []
        self.assertTrue(
            any("field-specific locator" in e for e in records.validate(data))
        )

    def test_failed_source_cannot_support_claim(self):
        data = fixture()
        data["sources"][0]["access_state"] = "failed"
        self.assertTrue(any("inaccessible source" in e for e in records.validate(data)))

    def test_snippet_not_documented(self):
        data = fixture()
        data["sources"][0]["access_state"] = "snippet_only"
        self.assertTrue(any("snippet-only" in e for e in records.validate(data)))

    def test_rejection_not_admitted_group(self):
        data = fixture()
        data["cases"][0]["fields"]["enrollment_status"]["value"] = "rejected"
        self.assertTrue(any("no usable" in e for e in records.validate(data)))

    def test_online_exclusion(self):
        data = fixture()
        data["cases"][0]["excluded_from_on_campus_distribution"] = True
        self.assertTrue(any("excluded" in e for e in records.validate(data)))

    def test_dangling_group_case(self):
        data = fixture()
        data["archetypes"][0]["case_ids"] = ["C9"]
        self.assertTrue(any("unknown case" in e for e in records.validate(data)))

    def test_unpreserved_conflict(self):
        data = fixture()
        data["cases"][0]["fields"]["enrollment_status"]["status"] = "conflicting"
        self.assertTrue(any("two preserved" in e for e in records.validate(data)))

    def test_identical_conflict_alternatives_rejected(self):
        data = fixture()
        f = data["cases"][0]["fields"]["undergraduate_school"]
        f.update(
            status="conflicting",
            source_ids=["S1"],
            evidence=[{"source_id": "S1", "locator": "school"}],
        )
        alternative = {
            "value": "same",
            "source_ids": ["S1"],
            "evidence": [{"source_id": "S1", "locator": "school"}],
        }
        data["cases"][0]["conflicts"] = [
            {
                "field": "undergraduate_school",
                "values": [alternative, copy.deepcopy(alternative)],
            }
        ]
        self.assertTrue(any("two preserved" in e for e in records.validate(data)))

    def test_calculation_requires_boundary(self):
        data = fixture()
        data["cases"][0]["fields"]["work_duration_before_application"] = {
            "value": 12,
            "status": "calculated",
            "source_ids": ["S1"],
            "evidence": [{"source_id": "S1", "locator": "dates"}],
        }
        self.assertTrue(
            any("cutoff and calculation" in e for e in records.validate(data))
        )

    def test_malformed_nested_records_return_errors(self):
        for location in ("archetypes", "experiences", "conflicts"):
            data = fixture()
            if location == "archetypes":
                data[location] = [None]
            else:
                data["cases"][0][location] = [None]
            with self.subTest(location=location):
                self.assertTrue(records.validate(data))

    def test_inferred_admission_not_group_evidence(self):
        data = fixture()
        data["cases"][0]["fields"]["enrollment_status"]["status"] = "inferred"
        self.assertTrue(any("admission status" in e for e in records.validate(data)))

    def test_identity_connection_required(self):
        data = fixture()
        del data["cases"][0]["identity_link"]
        self.assertTrue(any("identity_link" in e for e in records.validate(data)))

    def test_unrelated_group_source_rejected(self):
        data = fixture()
        source = copy.deepcopy(data["sources"][0])
        source["id"] = "S2"
        data["sources"].append(source)
        data["archetypes"][0].update(
            source_ids=["S2"],
            evidence=[{"source_id": "S2", "locator": "unrelated person"}],
        )
        self.assertTrue(any("member case" in e for e in records.validate(data)))

    def test_blank_locator_rejected(self):
        data = fixture()
        data["cases"][0]["fields"]["enrollment_status"]["evidence"][0]["locator"] = "  "
        self.assertTrue(records.validate(data))

    def test_invalid_date_rejected(self):
        data = fixture()
        data["sources"][0]["accessed_on"] = "2026-02-30"
        self.assertTrue(any("date" in e for e in records.validate(data)))

    def test_incomplete_unknown_references_rejected(self):
        data = fixture()
        data["cases"][0]["fields"]["undergraduate_school"]["source_ids"] = ["S1"]
        self.assertTrue(
            any("field-specific locator" in e for e in records.validate(data))
        )

    def test_cli_rejects_duplicate_keys_and_nan(self):
        for content in ('{"scope":{},"scope":{}}', '{"value":NaN}'):
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / "bad.json"
                path.write_text(content)
                result = subprocess.run(
                    [sys.executable, str(SCRIPTS / "validate_cases.py"), str(path)],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 1)
                self.assertIn("Invalid case record", result.stderr)

    def test_malformed_url_returns_error(self):
        data = fixture()
        data["sources"][0]["url"] = "https://[broken"
        self.assertTrue(records.validate(data))

    def test_nested_wrong_types_return_errors(self):
        for location in ("scope", "sources", "cases", "archetypes"):
            for value in (None, True, 3, "bad"):
                data = fixture()
                data[location] = value
                with self.subTest(location=location, value=value):
                    self.assertTrue(records.validate(data))

    def test_cli_from_another_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "valid.json"
            content = json.dumps(fixture())
            path.write_text(content)
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "validate_cases.py"), str(path)],
                cwd=folder,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0)
            self.assertEqual(path.read_text(), content)

    def test_orphan_conflict_rejected(self):
        data = fixture()
        alternative = {
            "value": "a",
            "source_ids": ["S1"],
            "evidence": [{"source_id": "S1", "locator": "school"}],
        }
        data["cases"][0]["conflicts"] = [
            {"field": "missing_field", "values": [alternative]}
        ]
        self.assertTrue(any("conflicting status" in e for e in records.validate(data)))

    def test_exclusion_flag_not_string(self):
        data = fixture()
        data["cases"][0]["excluded_from_on_campus_distribution"] = "false"
        self.assertTrue(any("boolean" in e for e in records.validate(data)))

    def test_program_conflict_sources_validated(self):
        data = fixture()
        data["program_conflicts"] = [
            {
                "field": "cycle",
                "alternatives": ["2025", "2027"],
                "resolution": "unresolved",
                "source_ids": ["S9"],
                "evidence": [{"source_id": "S9", "locator": "FAQ"}],
            }
        ]
        self.assertTrue(any("unknown source" in e for e in records.validate(data)))

    def test_program_conflict_alternatives_preserved(self):
        data = fixture()
        data["program_conflicts"] = [
            {
                "field": "cycle",
                "alternatives": ["same", "same"],
                "resolution": "unresolved",
                "source_ids": ["S1"],
                "evidence": [{"source_id": "S1", "locator": "FAQ"}],
            }
        ]
        self.assertTrue(any("two distinct" in e for e in records.validate(data)))

    def test_cli_invalid_json(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.json"
            path.write_text("{")
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "validate_cases.py"), str(path)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("Invalid case record", result.stderr)


class MonthTests(unittest.TestCase):
    def run_calc(self, intervals, cutoff="2021-01"):
        return months.calculate({"cutoff": cutoff, "intervals": intervals})

    def test_overlap_not_double_counted(self):
        result = self.run_calc(
            [
                {"start": "2020-01", "end": "2020-07", "end_inclusive": False},
                {"start": "2020-04", "end": "2020-10", "end_inclusive": False},
            ]
        )
        self.assertEqual((result["min_months"], result["max_months"]), (9, 9))

    def test_unspecified_end_returns_range(self):
        result = self.run_calc(
            [{"start": "2020-01", "end": "2020-07", "end_inclusive": None}]
        )
        self.assertEqual((result["min_months"], result["max_months"]), (6, 7))

    def test_cutoff_clips_current_job(self):
        result = self.run_calc([{"start": "2020-10", "end": None}])
        self.assertEqual(result["min_months"], 3)

    def test_future_job_is_excluded(self):
        self.assertEqual(
            self.run_calc([{"start": "2021-02", "end": "2021-09"}])["max_months"], 0
        )

    def test_future_ongoing_job_is_excluded(self):
        self.assertEqual(
            self.run_calc([{"start": "2021-02", "end": None}])["max_months"], 0
        )

    def test_year_only_rejected(self):
        with self.assertRaises(ValueError):
            self.run_calc([{"start": "2020", "end": "2020-07"}])

    def test_reversed_interval_rejected(self):
        with self.assertRaises(ValueError):
            self.run_calc([{"start": "2020-07", "end": "2020-01"}])

    def test_adjacent_inclusive_ranges_union(self):
        result = self.run_calc(
            [
                {"start": "2020-01", "end": "2020-03", "end_inclusive": True},
                {"start": "2020-04", "end": "2020-06", "end_inclusive": True},
            ]
        )
        self.assertEqual(result["min_months"], 6)

    def test_duplicate_intervals_idempotent(self):
        item = {"start": "2020-02", "end": "2020-06", "end_inclusive": True}
        self.assertEqual(self.run_calc([item]), self.run_calc([item, item]))

    def test_interval_union_matches_independent_month_set(self):
        import random

        rng = random.Random(42)
        for _ in range(200):
            intervals = []
            expected = set()
            for _ in range(rng.randrange(1, 8)):
                start = rng.randrange(1, 13)
                end = rng.randrange(start, 13)
                intervals.append(
                    {
                        "start": f"2020-{start:02d}",
                        "end": f"2020-{end:02d}",
                        "end_inclusive": True,
                    }
                )
                expected.update(range(start, end + 1))
            result = self.run_calc(intervals)
            self.assertEqual(
                (result["min_months"], result["max_months"]),
                (len(expected), len(expected)),
            )

    def test_cli_readonly_and_output(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "input.json"
            content = json.dumps(
                {"cutoff": "2021-01", "intervals": [{"start": "2020-01", "end": None}]}
            )
            path.write_text(content)
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "work_months.py"), str(path)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout)["min_months"], 12)
            self.assertEqual(path.read_text(), content)


if __name__ == "__main__":
    unittest.main()
