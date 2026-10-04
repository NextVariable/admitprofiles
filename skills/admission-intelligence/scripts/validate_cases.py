#!/usr/bin/env python3
"""Check evidence record consistency, not truth or semantic source support."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

STATUSES = {'documented', 'self_reported', 'secondary', 'calculated', 'inferred', 'unknown', 'conflicting'}
ACCESS = {'full_text', 'partial_text', 'snippet_only', 'blocked', 'failed'}
TIMING = {'before_application', 'before_enrollment_only', 'during_program', 'after_program', 'unknown'}
TYPES = {'full_time', 'part_time', 'self_employed', 'internship', 'research', 'project', 'employment_unspecified'}
FIELDS = {'enrollment_status', 'track', 'undergraduate_school', 'undergraduate_major', 'undergraduate_start', 'undergraduate_end', 'masters_start', 'masters_graduation', 'work_duration_before_application', 'application_narrative'}
ADMITTED = {'offer_self_reported', 'offer_documented', 'enrolled', 'graduated'}


def validate(data):
    errors = []
    def error(path, message):
        errors.append(f'{path}: {message}')
    if not isinstance(data, dict):
        return ['record must be an object']
    if data.get('schema_version') != '1.1':
        error('schema_version', 'expected 1.1; legacy records need explicit migration')
    for key in ('scope', 'researched_on', 'sources', 'cases', 'archetypes'):
        if key not in data:
            error(key, 'required')
    def index(key):
        records = data.get(key, [])
        result = {}
        if not isinstance(records, list):
            error(key, 'must be a list')
            return result
        for i, row in enumerate(records):
            if not isinstance(row, dict) or not isinstance(row.get('id'), str) or not row['id']:
                error(f'{key}[{i}]', 'non-empty id required')
                continue
            if row['id'] in result:
                error(key, f'duplicate id {row["id"]}')
            result[row['id']] = row
        return result
    sources, cases = index('sources'), index('cases')
    for sid, source in sources.items():
        for key in ('url', 'title', 'source_type', 'accessed_on', 'access_state', 'locator'):
            if not source.get(key):
                error(sid, f'{key} required')
        parsed = urlparse(str(source.get('url', '')))
        if parsed.scheme not in ('http', 'https') or not parsed.netloc:
            error(sid, 'source URL must be http(s)')
        if source.get('access_state') not in ACCESS:
            error(sid, 'invalid access_state')
    def refs(row, path, required=True):
        ids = row.get('source_ids', [])
        if not isinstance(ids, list) or any(not isinstance(i, str) for i in ids):
            error(path, 'source_ids must be a string list')
            return
        if required and not ids:
            error(path, 'evidence source required')
        if len(ids) != len(set(ids)):
            error(path, 'duplicate source reference')
        for sid in ids:
            if sid not in sources:
                error(path, f'unknown source {sid}')
            elif sources[sid].get('access_state') in {'blocked', 'failed'}:
                error(path, f'inaccessible source {sid} cannot support a claim')
            elif sources[sid].get('access_state') == 'snippet_only' and row.get('status') == 'documented':
                error(path, 'snippet-only source cannot support documented status')
        evidence = row.get('evidence', [])
        if not isinstance(evidence, list):
            error(path, 'evidence must be a list')
            return
        located = set()
        for entry in evidence:
            if not isinstance(entry, dict) or entry.get('source_id') not in ids or not entry.get('locator'):
                error(path, 'evidence locator must reference a cited source')
            else:
                located.add(entry['source_id'])
        if required and located != set(ids):
            error(path, 'each source needs a field-specific locator')
    for cid, case in cases.items():
        fields = case.get('fields', {})
        if not isinstance(fields, dict):
            error(cid, 'fields must be an object')
            continue
        for missing in FIELDS - fields.keys():
            error(cid, f'missing field {missing}')
        for name, field in fields.items():
            path = f'{cid}.{name}'
            if not isinstance(field, dict) or field.get('status') not in STATUSES:
                error(path, 'invalid field status')
                continue
            if field['status'] == 'unknown':
                if field.get('value') is not None:
                    error(path, 'unknown value must be null, not zero or a guess')
                refs(field, path, required=False)
            else:
                if field.get('value') is None and field['status'] != 'conflicting':
                    error(path, 'known field needs a value')
                refs(field, path)
            if field['status'] == 'conflicting':
                conflicts = [x for x in case.get('conflicts', []) if x.get('field') == name]
                if not conflicts or len({json.dumps(x.get('value'), sort_keys=True) for x in conflicts[0].get('values', [])}) < 2:
                    error(path, 'conflicting field needs two preserved alternatives')
                else:
                    for alternative in conflicts[0]['values']:
                        refs(alternative, path + '.alternative')
        duration = fields.get('work_duration_before_application', {})
        if duration.get('status') == 'calculated' and (not duration.get('cutoff') or not duration.get('calculation')):
            error(cid, 'calculated work duration needs cutoff and calculation')
        state = fields.get('enrollment_status', {}).get('value')
        if state is not None and state not in ADMITTED | {'waitlisted', 'rejected', 'unknown'}:
            error(cid, 'use a canonical enrollment_status; detail belongs in note')
        for i, experience in enumerate(case.get('experiences', [])):
            path = f'{cid}.experiences[{i}]'
            if experience.get('type') not in TYPES or experience.get('relative_timing') not in TIMING:
                error(path, 'invalid experience type or timing')
            if experience.get('status') not in STATUSES:
                error(path, 'invalid experience status')
            refs(experience, path, required=experience.get('status') != 'unknown')
    for i, group in enumerate(data.get('archetypes', [])):
        path = f'archetypes[{i}]'
        ids = group.get('case_ids', [])
        if not isinstance(ids, list) or not ids or len(set(ids)) != len(ids):
            error(path, 'non-empty unique case_ids required')
            continue
        for cid in ids:
            if cid not in cases:
                error(path, f'unknown case {cid}')
                continue
            case = cases[cid]
            state = case.get('fields', {}).get('enrollment_status', {}).get('value')
            if state not in ADMITTED:
                error(path, f'{cid} has no usable admission/enrollment status')
            if case.get('excluded_from_on_campus_distribution'):
                error(path, f'{cid} explicitly excluded from this scope')
        refs(group, path)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    try:
        errors = validate(json.loads(args.input.read_text(encoding='utf-8')))
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        parser.exit(1, f'Invalid case record: {exc}\n')
    if errors:
        parser.exit(1, '\n'.join(errors) + '\n')
    print('Record consistency passed. Source truth and claim support still require review.')


if __name__ == '__main__':
    main()
