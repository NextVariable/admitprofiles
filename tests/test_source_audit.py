"""Coverage regressions prevent omission, duplicate approval, or history rewrite."""

import copy
import importlib.util
import json
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "source_audit", Path(__file__).with_name("check_source_audit.py")
)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class SourceAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = json.loads((audit.AUDIT / "inventory.json").read_text())
        cls.reviews = [
            json.loads((audit.AUDIT / f"{name}.json").read_text())
            for name in ("berkeley", "brown", "cmu", "northwestern")
        ]

    def test_complete_frozen_audit(self):
        self.assertEqual(audit.check(self.inventory, self.reviews, audit.ROOT), [])

    def test_omission_is_rejected(self):
        reviews = copy.deepcopy(self.reviews)
        reviews[0]["units"].pop()
        self.assertTrue(
            any(
                "Missing audit unit" in e
                for e in audit.check(self.inventory, reviews, audit.ROOT)
            )
        )

    def test_duplicate_is_rejected(self):
        reviews = copy.deepcopy(self.reviews)
        reviews[0]["units"].append(reviews[0]["units"][0])
        self.assertTrue(
            any(
                "Duplicate audit unit" in e
                for e in audit.check(self.inventory, reviews, audit.ROOT)
            )
        )

    def test_history_digest_change_is_rejected(self):
        inventory = copy.deepcopy(self.inventory)
        inventory["files"][0]["sha256"] = "0" * 64
        self.assertTrue(
            any(
                "Historical file changed" in e
                for e in audit.check(inventory, self.reviews, audit.ROOT)
            )
        )

    def test_supported_claim_without_locator_is_rejected(self):
        reviews = copy.deepcopy(self.reviews)
        row = next(r for r in reviews[0]["units"] if r["verdict"] == "supported")
        row["evidence_locators"] = []
        self.assertTrue(
            any(
                "Missing source check" in e
                for e in audit.check(self.inventory, reviews, audit.ROOT)
            )
        )
