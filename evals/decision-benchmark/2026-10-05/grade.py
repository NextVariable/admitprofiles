#!/usr/bin/env python3
"""Compare frozen synthetic decisions; no live research or routing score."""

import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent


def main():
    oracle = json.loads((BASE / "oracle.json").read_text())
    digest = hashlib.sha256((BASE / "packet.json").read_bytes()).hexdigest()
    if digest != oracle["packet_sha256"]:
        raise ValueError("Benchmark input changed after oracle freeze")
    scores = []
    for path in sorted(BASE.glob("*-run*.json")):
        rows = json.loads(path.read_text())["rows"]
        seen = [r["id"] for r in rows]
        if len(seen) != len(set(seen)) or set(seen) != set(oracle["expected"]):
            raise ValueError(f"Missing, duplicate, or extra decisions: {path.name}")
        if any(not r.get("rationale", "").strip() for r in rows):
            raise ValueError(f"Missing reasoning: {path.name}")
        failures = [
            r["id"] for r in rows if r["decision"] != oracle["expected"][r["id"]]
        ]
        scores.append(
            {
                "run": path.name,
                "total": len(rows),
                "matched": len(rows) - len(failures),
                "failures": failures,
            }
        )
    print(json.dumps({"packet_sha256": digest, "scores": scores}, indent=2))


if __name__ == "__main__":
    main()
