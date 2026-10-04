"""Delivery failures, valid evidence preservation, and exhaustive date oracles."""

import copy
import itertools
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from test_skill_helpers import SCRIPTS, fixture, months, records


class EvidenceDeliveryTests(unittest.TestCase):
    def test_malformed_source_urls_are_rejected(self):
        for url in (
            "https://user@",
            "https://example.org:wrong",
            "https://example.org:65536",
            "https://exa mple.org",
            "https://example.org\\fake",
            "https://example.org\n/fake",
        ):
            data = fixture()
            data["sources"][0]["url"] = url
            with self.subTest(url=url):
                self.assertTrue(records.validate(data))

    def test_valid_source_urls_are_preserved(self):
        for url in (
            "https://example.org/article?q=education%20history#section",
            "https://例子.中国/履历",
            "http://example.org:8080/profile",
            "https://[2001:db8::1]/profile",
        ):
            data = fixture()
            data["sources"][0]["url"] = url
            before = copy.deepcopy(data)
            with self.subTest(url=url):
                self.assertEqual(records.validate(data), [])
                self.assertEqual(data, before)

    def test_empty_known_values_are_rejected(self):
        for value in ("", "   ", [], {}):
            data = fixture()
            data["cases"][0]["fields"]["undergraduate_school"].update(
                value=value,
                status="documented",
                source_ids=["S1"],
                evidence=[{"source_id": "S1", "locator": "school"}],
            )
            with self.subTest(value=value):
                self.assertTrue(records.validate(data))
        # Empty placeholders differ from an explicitly reported zero or false.
        for name, value in (
            ("work_duration_before_application", 0),
            ("has_prior_masters", False),
        ):
            data = fixture()
            data["cases"][0]["fields"][name] = {
                "value": value,
                "status": "self_reported",
                "source_ids": ["S1"],
                "evidence": [{"source_id": "S1", "locator": "explicit statement"}],
            }
            with self.subTest(name=name, value=value):
                self.assertEqual(records.validate(data), [])

    def test_conflict_alternatives_must_have_content(self):
        for value in ("", "   ", [], {}):
            data = fixture()
            data["archetypes"] = []
            data["cases"][0]["fields"]["undergraduate_school"].update(
                value=None,
                status="conflicting",
                source_ids=["S1"],
                evidence=[{"source_id": "S1", "locator": "school"}],
            )
            data["cases"][0]["conflicts"] = [
                {
                    "field": "undergraduate_school",
                    "values": [
                        {
                            "value": alternative,
                            "source_ids": ["S1"],
                            "evidence": [{"source_id": "S1", "locator": "school"}],
                        }
                        for alternative in (value, "School B")
                    ],
                }
            ]
            with self.subTest(value=value):
                self.assertTrue(records.validate(data))

    def test_cli_reports_excessive_nesting_without_traceback(self):
        content = '{"note":' + "[" * 2000 + "0" + "]" * 2000 + "}"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "deep.json"
            path.write_text(content, encoding="utf-8")
            for tool in ("validate_cases", "work_months"):
                with self.subTest(tool=tool):
                    result = subprocess.run(
                        [sys.executable, str(SCRIPTS / f"{tool}.py"), str(path)],
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(result.returncode, 1)
                    self.assertNotIn("Traceback", result.stderr)
                    self.assertTrue(result.stderr.strip())


class ExhaustiveIntervalTests(unittest.TestCase):
    def test_25350_pairs_at_year_boundary(self):
        def date(number):
            number += 11
            return f"{2000 + number // 12:04d}-{number % 12 + 1:02d}"

        # A small complete domain catches relationships a random corpus can miss.
        intervals = [
            {"start": start, "end": end, "end_inclusive": inclusive}
            for start in range(5)
            for end in range(start, 6)
            for inclusive in (True, False, None)
        ] + [{"start": start, "end": None} for start in range(5)]
        checked = 0
        for cutoff, pair in itertools.product(
            range(6), itertools.product(intervals, repeat=2)
        ):
            certain, possible = set(), set()
            for item in pair:
                # Enumerate each month directly, independently of the merge algorithm.
                for month in range(cutoff):
                    if month < item["start"]:
                        continue
                    end = item["end"]
                    if end is None or month < end:
                        certain.add(month)
                        possible.add(month)
                    elif month == end:
                        if item.get("end_inclusive") is True:
                            certain.add(month)
                        if item.get("end_inclusive") is not False:
                            possible.add(month)
            supplied = [
                dict(
                    item,
                    start=date(item["start"]),
                    end=None if item["end"] is None else date(item["end"]),
                )
                for item in pair
            ]
            data = {"cutoff": date(cutoff), "intervals": supplied}
            result = months.calculate(data)
            self.assertEqual(
                (result["min_months"], result["max_months"]),
                (len(certain), len(possible)),
                data,
            )
            # Reordering and repeated evidence must not increase employment duration.
            data["intervals"] = list(reversed(supplied)) + supplied
            self.assertEqual(months.calculate(data), result)
            checked += 1
        self.assertEqual(checked, 25350)
