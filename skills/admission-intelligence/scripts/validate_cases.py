#!/usr/bin/env python3
"""Check evidence record consistency, not truth or semantic source support."""
import argparse
import json
import math
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

STATUSES = {'documented', 'self_reported', 'secondary', 'calculated', 'inferred', 'unknown', 'conflicting'}
ACCESS = {'full_text', 'partial_text', 'snippet_only', 'blocked', 'failed'}
TIMING = {'before_application', 'before_enrollment_only', 'during_program', 'after_program', 'unknown'}
TYPES = {'full_time', 'part_time', 'self_employed', 'internship', 'research', 'project', 'employment_unspecified'}
FIELDS = {'enrollment_status', 'track', 'undergraduate_school', 'undergraduate_major', 'undergraduate_start', 'undergraduate_end', 'masters_start', 'masters_graduation', 'work_duration_before_application', 'application_narrative'}
ADMITTED = {'offer_self_reported', 'offer_documented', 'enrolled', 'graduated'}


def _validate_record(data):
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
        if located != set(ids):
            error(path, 'each source needs a field-specific locator')
    for cid, case in cases.items():
        refs(case['identity_link'], cid + '.identity_link')
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
        if state is not None and state not in ADMITTED | {'waitlisted', 'rejected'}:
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
            admission = case.get('fields', {}).get('enrollment_status', {})
            if admission.get('status') not in {'documented', 'self_reported', 'secondary'}:
                error(path, f'{cid} admission status must be directly reported, not inferred')
            member_sources = {sid for f in case.get('fields', {}).values() for sid in f.get('source_ids', [])}
            member_sources.update(
                sid for experience in case.get('experiences', [])
                if experience.get('status') in {'documented', 'self_reported', 'secondary'}
                for sid in experience.get('source_ids', [])
            )
            if not member_sources.intersection(group.get('source_ids', [])):
                error(path, f'{cid} needs a source from this member case field or directly reported experience')
            if state not in ADMITTED:
                error(path, f'{cid} has no usable admission/enrollment status')
            if case.get('excluded_from_on_campus_distribution'):
                error(path, f'{cid} explicitly excluded from this scope')
        refs(group, path)
    for i, conflict in enumerate(data.get('program_conflicts', [])):
        refs(conflict, f'program_conflicts[{i}]')
    return errors


def validate(data):
    errors = []
    def require(condition, path, message):
        if not condition: errors.append(f'{path}: {message}')
    def text(value):
        return isinstance(value, str) and bool(value.strip())
    def iso_date(value):
        try:
            return isinstance(value, str) and date.fromisoformat(value).isoformat() == value
        except ValueError:
            return False
    def objects(value, path):
        require(isinstance(value, list), path, 'must be a list')
        if not isinstance(value, list): return []
        require(all(isinstance(x, dict) for x in value), path, 'entries must be objects')
        return [x for x in value if isinstance(x, dict)]
    def references(row, path):
        ids = row.get('source_ids', [])
        require(isinstance(ids, list) and all(text(x) for x in ids), path, 'source_ids must be non-empty strings')
        seen = set()
        for e in objects(row.get('evidence', []), path + '.evidence'):
            require(text(e.get('source_id')) and text(e.get('locator')), path, 'evidence locator and source_id must be non-empty text')
            if text(e.get('source_id')) and text(e.get('locator')):
                pair = (e['source_id'], e['locator'])
                require(pair not in seen, path, 'duplicate evidence locator')
                seen.add(pair)
    if not isinstance(data, dict): return ['record must be an object']
    require(isinstance(data.get('scope'), dict) and text(data.get('scope', {}).get('institution')) and text(data.get('scope', {}).get('program')), 'scope', 'institution and program required')
    require(iso_date(data.get('researched_on')), 'researched_on', 'valid YYYY-MM-DD date required')
    for source in objects(data.get('sources'), 'sources'):
        for key in ('id','url','title','source_type','access_state','locator'):
            require(text(source.get(key)), 'sources.' + key, 'non-empty text required')
        require(iso_date(source.get('accessed_on')), 'sources.accessed_on', 'valid YYYY-MM-DD date required')
        if iso_date(source.get('accessed_on')) and iso_date(data.get('researched_on')):
            require(source['accessed_on'] <= data['researched_on'], 'sources.accessed_on', 'access cannot be later than research date')
        if source.get('published_on') is not None:
            require(iso_date(source['published_on']), 'sources.published_on', 'valid YYYY-MM-DD date required')
        try: urlparse(str(source.get('url', '')))
        except ValueError: errors.append('sources.url: invalid URL')
    for case in objects(data.get('cases'), 'cases'):
        require(text(case.get('id')), 'cases.id', 'non-empty text required')
        if 'excluded_from_on_campus_distribution' in case:
            require(type(case['excluded_from_on_campus_distribution']) is bool, 'excluded_from_on_campus_distribution', 'must be a boolean')
        identity = case.get('identity_link')
        require(isinstance(identity, dict) and text(identity.get('basis')), 'identity_link', 'explicit identity connection required')
        if isinstance(identity, dict): references(identity, 'identity_link')
        fields = case.get('fields')
        require(isinstance(fields, dict), 'fields', 'must be an object')
        if isinstance(fields, dict):
            for name, f in fields.items():
                require(isinstance(f, dict), name, 'field must be an object')
                if isinstance(f, dict):
                    require(isinstance(f.get('status'), str), name, 'status must be text')
                    references(f, name)
                    if f.get('status') != 'unknown' and isinstance(f.get('value'), str):
                        require(text(f['value']), name, 'known value cannot be blank')
                    if name == 'work_duration_before_application' and isinstance(f.get('value'), (int, float)):
                        value = f['value']
                        require(type(value) is not bool and value >= 0 and (not isinstance(value, float) or math.isfinite(value)), name, 'numeric duration must be finite and non-negative, not boolean')
                    if name == 'work_duration_before_application' and f.get('status') == 'calculated' and f.get('cutoff'):
                        cutoff = f.get('cutoff')
                        require(isinstance(cutoff, str) and bool(re.fullmatch(r'[0-9]{4}(?:-(?:0[1-9]|1[0-2]))?', cutoff) or iso_date(cutoff)) and cutoff[:4] != '0000', name, 'calculated cutoff must preserve valid date precision')
            enrollment = fields.get('enrollment_status', {})
            if isinstance(enrollment, dict):
                require(enrollment.get('value') is None or isinstance(enrollment.get('value'), str), 'enrollment_status', 'canonical text or null required')
        for e in objects(case.get('experiences', []), 'experiences'):
            for key in ('type','relative_timing','status'):
                require(isinstance(e.get(key), str), 'experiences.' + key, 'text required')
            references(e, 'experiences')
        conflict_fields = set()
        for conflict in objects(case.get('conflicts', []), 'conflicts'):
            require(text(conflict.get('field')), 'conflicts.field', 'field required')
            if text(conflict.get('field')):
                require(conflict['field'] not in conflict_fields, 'conflicts.field', 'duplicate conflict field; preserve all alternatives in one record')
                conflict_fields.add(conflict['field'])
            if isinstance(fields, dict) and isinstance(conflict.get('field'), str):
                f = fields.get(conflict['field'])
                require(isinstance(f, dict) and f.get('status') == 'conflicting', 'conflicts.field', 'must match a field with conflicting status')
            for alternative in objects(conflict.get('values'), 'conflicts.values'):
                require(alternative.get('value') is not None, 'conflicts.values', 'non-null alternative required')
                references(alternative, 'conflicts.values')
    for group in objects(data.get('archetypes'), 'archetypes'):
        require(text(group.get('label')), 'archetypes.label', 'non-empty text required')
        require(group.get('status') == 'inferred', 'archetypes.status', 'classification must be inferred')
        ids = group.get('case_ids')
        require(isinstance(ids, list) and all(text(x) for x in ids), 'archetypes.case_ids', 'string list required')
        references(group, 'archetypes')
    for conflict in objects(data.get('program_conflicts', []), 'program_conflicts'):
        require(text(conflict.get('field')), 'program_conflicts.field', 'non-empty field required')
        alternatives = conflict.get('alternatives')
        valid = isinstance(alternatives, list) and all(text(x) for x in alternatives)
        require(valid and len(set(alternatives)) >= 2, 'program_conflicts.alternatives', 'two distinct non-empty text alternatives required')
        require(text(conflict.get('resolution')), 'program_conflicts.resolution', 'explicit unresolved or resolved decision required')
        references(conflict, 'program_conflicts')
    return errors if errors else _validate_record(data)


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result: raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f'non-finite JSON value: {value}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    try:
        errors = validate(json.loads(args.input.read_text(encoding='utf-8'), object_pairs_hook=reject_duplicate_keys, parse_constant=reject_constant))
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        parser.exit(1, f'Invalid case record: {exc}\n')
    if errors:
        parser.exit(1, '\n'.join(errors) + '\n')
    print('Record consistency passed. Source truth and claim support still require review.')


if __name__ == '__main__':
    main()
