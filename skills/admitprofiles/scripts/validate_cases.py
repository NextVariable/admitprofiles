#!/usr/bin/env python3
"""检查证据记录一致性，不验证真值或来源语义支持。

Check evidence record consistency, not truth or semantic source support.
"""

import argparse
import json
import math
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

STATUSES = {
    "documented",
    "self_reported",
    "secondary",
    "calculated",
    "inferred",
    "unknown",
    "conflicting",
}
ACCESS = {"full_text", "partial_text", "snippet_only", "blocked", "failed"}
TIMING = {
    "before_application",
    "before_enrollment_only",
    "during_program",
    "after_program",
    "unknown",
}
TYPES = {
    "full_time",
    "part_time",
    "self_employed",
    "internship",
    "research",
    "project",
    "employment_unspecified",
}
FIELDS = {
    "enrollment_status",
    "track",
    "undergraduate_school",
    "undergraduate_major",
    "undergraduate_start",
    "undergraduate_end",
    "masters_start",
    "masters_graduation",
    "work_duration_before_application",
    "application_narrative",
}
ADMITTED = {"offer_self_reported", "offer_documented", "enrolled", "graduated"}


def _has_content(value):
    """Keep zero and false as values, but reject empty evidence placeholders."""
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (dict, list)):
        return bool(value)
    return True


def _valid_source_url(value):
    """Check URL syntax only; this does not request or verify the destination."""
    if not isinstance(value, str) or any(
        character.isspace() or ord(character) < 32 or character == "\\"
        for character in value
    ):
        return False
    try:
        parsed = urlparse(value)
        return (
            parsed.scheme in {"http", "https"}
            and bool(parsed.hostname)
            and (parsed.port is None or 0 <= parsed.port <= 65535)
        )
    except ValueError:
        return False


def _validate_relationships(data):
    """Check source and case links after the structure validator has passed."""
    errors = []

    def error(path, message):
        errors.append(f"{path}: {message}")

    if data.get("schema_version") != "1.1":
        error("schema_version", "expected 1.1; legacy records need explicit migration")

    def index(key):
        records = data.get(key, [])
        result = {}
        for row in records:
            if row["id"] in result:
                error(key, f"duplicate id {row['id']}")
            result[row["id"]] = row
        return result

    sources, cases = index("sources"), index("cases")
    for sid, source in sources.items():
        if source.get("access_state") not in ACCESS:
            error(sid, "invalid access_state")

    def refs(row, path, required=True):
        ids = row.get("source_ids", [])
        if required and not ids:
            error(path, "evidence source required")
        if len(ids) != len(set(ids)):
            error(path, "duplicate source reference")
        for sid in ids:
            if sid not in sources:
                error(path, f"unknown source {sid}")
            elif sources[sid].get("access_state") in {"blocked", "failed"}:
                error(path, f"inaccessible source {sid} cannot support a claim")
            elif (
                sources[sid].get("access_state") == "snippet_only"
                and row.get("status") == "documented"
            ):
                error(path, "snippet-only source cannot support documented status")
        evidence = row.get("evidence", [])
        located = set()
        for entry in evidence:
            if (
                not isinstance(entry, dict)
                or entry.get("source_id") not in ids
                or not entry.get("locator")
            ):
                error(path, "evidence locator must reference a cited source")
            else:
                located.add(entry["source_id"])
        if located != set(ids):
            error(path, "each source needs a field-specific locator")

    for cid, case in cases.items():
        refs(case["identity_link"], cid + ".identity_link")
        fields = case.get("fields", {})
        for missing in FIELDS - fields.keys():
            error(cid, f"missing field {missing}")
        for name, field in fields.items():
            path = f"{cid}.{name}"
            if field.get("status") not in STATUSES:
                error(path, "invalid field status")
                continue
            if field["status"] == "unknown":
                if field.get("value") is not None:
                    error(path, "unknown value must be null, not zero or a guess")
                refs(field, path, required=False)
            else:
                if field.get("value") is None and field["status"] != "conflicting":
                    error(path, "known field needs a value")
                refs(field, path)
            if field["status"] == "conflicting":
                conflicts = [
                    x for x in case.get("conflicts", []) if x.get("field") == name
                ]
                if (
                    not conflicts
                    or len(
                        {
                            json.dumps(x.get("value"), sort_keys=True)
                            for x in conflicts[0].get("values", [])
                        }
                    )
                    < 2
                ):
                    error(path, "conflicting field needs two preserved alternatives")
                else:
                    for alternative in conflicts[0]["values"]:
                        refs(alternative, path + ".alternative")
        duration = fields.get("work_duration_before_application", {})
        if duration.get("status") == "calculated" and (
            not duration.get("cutoff") or not duration.get("calculation")
        ):
            error(cid, "calculated work duration needs cutoff and calculation")
        state = fields.get("enrollment_status", {}).get("value")
        if state is not None and state not in ADMITTED | {"waitlisted", "rejected"}:
            error(cid, "use a canonical enrollment_status; detail belongs in note")
        for i, experience in enumerate(case.get("experiences", [])):
            path = f"{cid}.experiences[{i}]"
            if (
                experience.get("type") not in TYPES
                or experience.get("relative_timing") not in TIMING
            ):
                error(path, "invalid experience type or timing")
            if experience.get("status") not in STATUSES:
                error(path, "invalid experience status")
            refs(experience, path, required=experience.get("status") != "unknown")
    for i, group in enumerate(data.get("archetypes", [])):
        path = f"archetypes[{i}]"
        ids = group.get("case_ids", [])
        if not ids or len(set(ids)) != len(ids):
            error(path, "non-empty unique case_ids required")
            continue
        for cid in ids:
            if cid not in cases:
                error(path, f"unknown case {cid}")
                continue
            case = cases[cid]
            state = case.get("fields", {}).get("enrollment_status", {}).get("value")
            admission = case.get("fields", {}).get("enrollment_status", {})
            if admission.get("status") not in {
                "documented",
                "self_reported",
                "secondary",
            }:
                error(
                    path,
                    f"{cid} admission status must be directly reported, not inferred",
                )
            member_sources = {
                sid
                for f in case.get("fields", {}).values()
                if f.get("status") in {"documented", "self_reported", "secondary"}
                for sid in f.get("source_ids", [])
            }
            member_sources.update(
                sid
                for experience in case.get("experiences", [])
                if experience.get("status")
                in {"documented", "self_reported", "secondary"}
                for sid in experience.get("source_ids", [])
            )
            if not member_sources.intersection(group.get("source_ids", [])):
                error(
                    path,
                    f"{cid} needs a source from this member case field or directly reported experience",
                )
            if state not in ADMITTED:
                error(path, f"{cid} has no usable admission/enrollment status")
            if case.get("excluded_from_on_campus_distribution"):
                error(path, f"{cid} explicitly excluded from this scope")
        refs(group, path)
    for i, conflict in enumerate(data.get("program_conflicts", [])):
        refs(conflict, f"program_conflicts[{i}]")
    return errors


class _StructureValidator:
    """Validate shape before relation checks can safely inspect nested values."""

    def __init__(self):
        self.errors = []

    def require(self, condition, path, message):
        if not condition:
            self.errors.append(f"{path}: {message}")

    def text(self, value):
        return isinstance(value, str) and bool(value.strip())

    def iso_date(self, value):
        try:
            return (
                isinstance(value, str)
                and date.fromisoformat(value).isoformat() == value
            )
        except ValueError:
            return False

    def objects(self, value, path):
        self.require(isinstance(value, list), path, "must be a list")
        if not isinstance(value, list):
            return []
        self.require(
            all((isinstance(x, dict) for x in value)), path, "entries must be objects"
        )
        return [x for x in value if isinstance(x, dict)]

    def references(self, row, path):
        ids = row.get("source_ids", [])
        self.require(
            isinstance(ids, list) and all((self.text(x) for x in ids)),
            path,
            "source_ids must be non-empty strings",
        )
        seen = set()
        for e in self.objects(row.get("evidence", []), path + ".evidence"):
            self.require(
                self.text(e.get("source_id")) and self.text(e.get("locator")),
                path,
                "evidence locator and source_id must be non-empty text",
            )
            if self.text(e.get("source_id")) and self.text(e.get("locator")):
                pair = (e["source_id"], e["locator"])
                self.require(pair not in seen, path, "duplicate evidence locator")
                seen.add(pair)

    def _check_sources(self, data):
        for source in self.objects(data.get("sources"), "sources"):
            for key in ("id", "url", "title", "source_type", "access_state", "locator"):
                self.require(
                    self.text(source.get(key)),
                    "sources." + key,
                    "non-empty text required",
                )
            self.require(
                self.iso_date(source.get("accessed_on")),
                "sources.accessed_on",
                "valid YYYY-MM-DD date required",
            )
            if self.iso_date(source.get("accessed_on")) and self.iso_date(
                data.get("researched_on")
            ):
                self.require(
                    source["accessed_on"] <= data["researched_on"],
                    "sources.accessed_on",
                    "access cannot be later than research date",
                )
            if source.get("published_on") is not None:
                self.require(
                    self.iso_date(source["published_on"]),
                    "sources.published_on",
                    "valid YYYY-MM-DD date required",
                )
            self.require(
                _valid_source_url(source.get("url")),
                "sources.url",
                "valid http(s) URL with hostname and port required; encode spaces",
            )

    def _check_cases(self, data):
        for case in self.objects(data.get("cases"), "cases"):
            self._check_case(case)

    def _check_archetypes(self, data):
        for group in self.objects(data.get("archetypes"), "archetypes"):
            self.require(
                self.text(group.get("label")),
                "archetypes.label",
                "non-empty text required",
            )
            self.require(
                group.get("status") == "inferred",
                "archetypes.status",
                "classification must be inferred",
            )
            ids = group.get("case_ids")
            self.require(
                isinstance(ids, list) and all((self.text(x) for x in ids)),
                "archetypes.case_ids",
                "string list required",
            )
            self.references(group, "archetypes")

    def _check_program_conflicts(self, data):
        for conflict in self.objects(
            data.get("program_conflicts", []), "program_conflicts"
        ):
            self.require(
                self.text(conflict.get("field")),
                "program_conflicts.field",
                "non-empty field required",
            )
            alternatives = conflict.get("alternatives")
            valid = isinstance(alternatives, list) and all(
                (self.text(x) for x in alternatives)
            )
            self.require(
                valid and len(set(alternatives)) >= 2,
                "program_conflicts.alternatives",
                "two distinct non-empty text alternatives required",
            )
            self.require(
                self.text(conflict.get("resolution")),
                "program_conflicts.resolution",
                "explicit unresolved or resolved decision required",
            )
            self.references(conflict, "program_conflicts")

    def _check_case(self, case):
        self.require(self.text(case.get("id")), "cases.id", "non-empty text required")
        if "excluded_from_on_campus_distribution" in case:
            self.require(
                type(case["excluded_from_on_campus_distribution"]) is bool,
                "excluded_from_on_campus_distribution",
                "must be a boolean",
            )
        identity = case.get("identity_link")
        self.require(
            isinstance(identity, dict) and self.text(identity.get("basis")),
            "identity_link",
            "explicit identity connection required",
        )
        if isinstance(identity, dict):
            self.references(identity, "identity_link")
        fields = case.get("fields")
        self.require(isinstance(fields, dict), "fields", "must be an object")
        if isinstance(fields, dict):
            for name, f in fields.items():
                self.require(isinstance(f, dict), name, "field must be an object")
                if isinstance(f, dict):
                    self.require(
                        isinstance(f.get("status"), str), name, "status must be text"
                    )
                    self.references(f, name)
                    if (
                        name == "work_duration_before_application"
                        and f.get("status") == "calculated"
                    ):
                        self.require(
                            self.text(f.get("calculation")),
                            name,
                            "calculated work duration needs cutoff and calculation; calculation must be non-empty method text",
                        )
                    if f.get("status") not in ("unknown", "conflicting"):
                        self.require(
                            _has_content(f.get("value")),
                            name,
                            "known value cannot be blank or empty",
                        )
                    if name == "work_duration_before_application" and isinstance(
                        f.get("value"), (int, float)
                    ):
                        value = f["value"]
                        self.require(
                            type(value) is not bool
                            and value >= 0
                            and (not isinstance(value, float) or math.isfinite(value)),
                            name,
                            "numeric duration must be finite and non-negative, not boolean",
                        )
                    if (
                        name == "work_duration_before_application"
                        and f.get("status") == "calculated"
                        and f.get("cutoff")
                    ):
                        cutoff = f.get("cutoff")
                        self.require(
                            isinstance(cutoff, str)
                            and bool(
                                re.fullmatch("[0-9]{4}(?:-(?:0[1-9]|1[0-2]))?", cutoff)
                                or self.iso_date(cutoff)
                            )
                            and (cutoff[:4] != "0000"),
                            name,
                            "calculated cutoff must preserve valid date precision",
                        )
            enrollment = fields.get("enrollment_status", {})
            if isinstance(enrollment, dict):
                self.require(
                    enrollment.get("value") is None
                    or isinstance(enrollment.get("value"), str),
                    "enrollment_status",
                    "canonical text or null required",
                )
        for e in self.objects(case.get("experiences", []), "experiences"):
            for key in ("type", "relative_timing", "status"):
                self.require(
                    isinstance(e.get(key), str), "experiences." + key, "text required"
                )
            self.references(e, "experiences")
        self._check_conflicts(case, fields)

    def _check_conflicts(self, case, fields):
        conflict_fields = set()
        for conflict in self.objects(case.get("conflicts", []), "conflicts"):
            self.require(
                self.text(conflict.get("field")), "conflicts.field", "field required"
            )
            if self.text(conflict.get("field")):
                self.require(
                    conflict["field"] not in conflict_fields,
                    "conflicts.field",
                    "duplicate conflict field; preserve all alternatives in one record",
                )
                conflict_fields.add(conflict["field"])
            if isinstance(fields, dict) and isinstance(conflict.get("field"), str):
                f = fields.get(conflict["field"])
                self.require(
                    isinstance(f, dict) and f.get("status") == "conflicting",
                    "conflicts.field",
                    "must match a field with conflicting status",
                )
            for alternative in self.objects(conflict.get("values"), "conflicts.values"):
                self.require(
                    _has_content(alternative.get("value")),
                    "conflicts.values",
                    "non-empty alternative required",
                )
                self.references(alternative, "conflicts.values")

    def validate(self, data):
        if not isinstance(data, dict):
            return ["record must be an object"]
        self.require(
            isinstance(data.get("scope"), dict)
            and self.text(data.get("scope", {}).get("institution"))
            and self.text(data.get("scope", {}).get("program")),
            "scope",
            "institution and program required",
        )
        self.require(
            self.iso_date(data.get("researched_on")),
            "researched_on",
            "valid YYYY-MM-DD date required",
        )
        self._check_sources(data)
        self._check_cases(data)
        self._check_archetypes(data)
        self._check_program_conflicts(data)
        return self.errors


def _finite_number_errors(data):
    """Reject overflow/NaN anywhere, including optional values and nested notes."""
    errors = []
    pending = [("record", data)]
    visited = set()
    while pending:
        path, value = pending.pop()
        if isinstance(value, float) and not math.isfinite(value):
            errors.append(f"{path}: non-finite JSON value")
        elif isinstance(value, (dict, list)):
            if id(value) in visited:
                continue
            visited.add(id(value))
            if isinstance(value, dict):
                pending.extend((f"{path}.{key}", item) for key, item in value.items())
            else:
                pending.extend(
                    (f"{path}[{index}]", item) for index, item in enumerate(value)
                )
    return errors


def validate(data):
    """Check shape first, then cross-record evidence relationships; never mutate input."""
    errors = _finite_number_errors(data)
    if errors:
        return errors
    errors = _StructureValidator().validate(data)
    return errors if errors else _validate_relationships(data)


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def finite_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"non-finite JSON value: {value}")
    return number


def reject_constant(value):
    raise ValueError(f"non-finite JSON value: {value}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        errors = validate(
            json.loads(
                args.input.read_text(encoding="utf-8"),
                object_pairs_hook=reject_duplicate_keys,
                parse_constant=reject_constant,
                parse_float=finite_float,
            )
        )
    except (OSError, ValueError, TypeError, AttributeError, RecursionError) as exc:
        parser.exit(1, f"Invalid case record: {exc}\n")
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    print(
        "Record consistency passed. Source truth and claim support still require review."
    )


if __name__ == "__main__":
    main()
