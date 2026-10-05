#!/usr/bin/env python3
"""Validate archived JSON consistency; no network or semantic source audit."""

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "validate_cases", ROOT / "skills/admission-intelligence/scripts/validate_cases.py"
)
records = importlib.util.module_from_spec(spec)
spec.loader.exec_module(records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT / "research")
    args = parser.parse_args()
    failed = False
    checked = legacy = 0
    for path in sorted(args.root.resolve().rglob("cases.json")):
        name = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
        try:
            data = json.loads(
                path.read_text(encoding="utf-8"),
                object_pairs_hook=records.reject_duplicate_keys,
                parse_constant=records.reject_constant,
                parse_float=records.finite_float,
            )
            if isinstance(data, dict) and data.get("schema_version") == "1.0":
                print(f"{name}: historical 1.0, not validated against 1.1")
                legacy += 1
                continue
            errors = records.validate(data)
        except (OSError, ValueError, TypeError, AttributeError, RecursionError) as exc:
            errors = [str(exc)]
        checked += 1
        if errors:
            failed = True
            print(f"{name}: FAIL\n" + "\n".join(errors), file=sys.stderr)
        else:
            print(f"{name}: consistency passed (source support not verified)")
    if not checked:
        failed = True
        print("No current-schema research records found.", file=sys.stderr)
    print(f"Checked {checked}; legacy preserved {legacy}.")
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
