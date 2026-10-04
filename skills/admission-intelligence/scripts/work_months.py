#!/usr/bin/env python3
"""Union month-level employment intervals without guessing date precision."""
import argparse
import json
import re
from pathlib import Path


def month(value):
    if not isinstance(value, str) or not re.fullmatch(r'[0-9]{4}-(0[1-9]|1[0-2])', value):
        raise ValueError('dates must be YYYY-MM; year-only dates cannot be calculated')
    year, number = map(int, value.split('-'))
    if year < 1:
        raise ValueError('year must be positive')
    return year * 12 + number - 1


def union_length(intervals):
    merged = []
    for start, end in sorted(intervals):
        if end <= start:
            continue
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(end, merged[-1][1])
        else:
            merged.append([start, end])
    return sum(end - start for start, end in merged)


def calculate(data):
    cutoff = month(data['cutoff'])
    lower, upper = [], []
    if not isinstance(data['intervals'], list):
        raise ValueError('intervals must be a list')
    for item in data['intervals']:
        start = month(item['start'])
        end = cutoff if item['end'] is None else month(item['end'])
        inclusive = item.get('end_inclusive')
        if inclusive is not None and type(inclusive) is not bool:
            raise ValueError('end_inclusive must be true, false or null')
        if item['end'] is not None and end < start:
            raise ValueError('end precedes start')
        if start >= cutoff:
            continue
        low_end = end + (inclusive is True and item['end'] is not None)
        high_end = end + (inclusive is not False and item['end'] is not None)
        lower.append((start, min(low_end, cutoff)))
        upper.append((start, min(high_end, cutoff)))
    return {
        'min_months': union_length(lower),
        'max_months': union_length(upper),
        'cutoff': data['cutoff'],
        'method': 'union of supplied intervals; cutoff excludes cutoff month',
        'limitation': 'does not verify source dates, full-time status or application timing',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    try:
        result = calculate(json.loads(args.input.read_text(encoding='utf-8')))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f'Invalid employment intervals: {exc}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
