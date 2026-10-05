#!/usr/bin/env python3
"""Check recorded benchmark completeness and decisions, not live model quality."""

import argparse
import hashlib
import json
import sys
from pathlib import Path


def grade(directory):
    oracle = json.loads((directory / "oracle.json").read_text())
    digest = hashlib.sha256((directory / "packet.json").read_bytes()).hexdigest()
    if digest != oracle["packet_sha256"]:
        raise ValueError("Benchmark input changed after oracle freeze")
    manifest = json.loads((directory / "execution.json").read_text())
    required = [r["output"] for r in manifest["independent_sessions"]]
    required += manifest["same_context_repeats"]
    if not required or len(required) != len(set(required)):
        raise ValueError("Expected run list must be non-empty and unique")
    actual = {p.name for p in directory.glob("*-run*.json")}
    if actual != set(required):
        raise ValueError(
            f"Run set differs: missing={sorted(set(required) - actual)}, extra={sorted(actual - set(required))}"
        )
    expected = oracle["expected"]
    if not expected:
        raise ValueError("Expected decisions cannot be empty")
    scores = []
    for name in sorted(required):
        rows = json.loads((directory / name).read_text())["rows"]
        seen = [r["id"] for r in rows]
        if len(seen) != len(set(seen)) or set(seen) != set(expected):
            raise ValueError(f"Missing, duplicate, or extra decisions: {name}")
        if any(
            not isinstance(r.get("rationale"), str) or not r["rationale"].strip()
            for r in rows
        ):
            raise ValueError(f"Missing reasoning: {name}")
        failures = [r["id"] for r in rows if r["decision"] != expected[r["id"]]]
        scores.append(
            {
                "run": name,
                "total": len(rows),
                "matched": len(rows) - len(failures),
                "failures": failures,
            }
        )
    return {"packet_sha256": digest, "scores": scores}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    try:
        result = grade(args.directory)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Invalid benchmark: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return int(any(row["failures"] for row in result["scores"]))


if __name__ == "__main__":
    sys.exit(main())
