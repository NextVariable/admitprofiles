#!/usr/bin/env python3
"""Verify audit coverage and frozen evidence; never certify source semantics."""

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "evals/source-audits/2026-10-05"
VERDICTS = {
    "supported",
    "overstated",
    "unsupported",
    "changed",
    "inaccessible",
    "unknown_preserved",
}


def check(inventory, audits, root):
    errors = []
    expected = {u["unit_id"] for u in inventory["units"]}
    if len(expected) != len(inventory["units"]):
        errors.append("Inventory has duplicate unit IDs")
    seen = set()
    for audit in audits:
        for row in audit["units"]:
            ident = row.get("unit_id")
            if ident in seen:
                errors.append(f"Duplicate audit unit: {ident}")
            seen.add(ident)
            if row.get("verdict") not in VERDICTS:
                errors.append(f"Invalid verdict: {ident}")
            if (
                not isinstance(row.get("rationale"), str)
                or not row["rationale"].strip()
            ):
                errors.append(f"Missing rationale: {ident}")
            if row.get("checked_on") != inventory["date"]:
                errors.append(f"Audit date differs: {ident}")
            if row.get("verdict") != "unknown_preserved":
                if not row.get("checked_urls") or not row.get("evidence_locators"):
                    errors.append(f"Missing source check or locator: {ident}")
    for ident in sorted(expected - seen):
        errors.append(f"Missing audit unit: {ident}")
    for ident in sorted(seen - expected):
        errors.append(f"Unexpected audit unit: {ident}")
    for entry in inventory["files"]:
        path = root / entry["path"]
        try:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError:
            digest = None
        if digest != entry["sha256"]:
            errors.append(f"Historical file changed: {entry['path']}")
    return errors


def main():
    inventory = json.loads((AUDIT / "inventory.json").read_text())
    audits = [
        json.loads((AUDIT / f"{name}.json").read_text())
        for name in ("berkeley", "brown", "cmu", "northwestern")
    ]
    errors = check(inventory, audits, ROOT)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(
        f"Audit covers {len(inventory['units'])} frozen units; source truth is not machine certified."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
