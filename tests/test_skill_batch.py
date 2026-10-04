"""Batch robustness, independent interval oracles, and evidence regressions."""
import copy
import json
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from test_skill_helpers import fixture, records, months, SCRIPTS

class EvidenceRegressions(unittest.TestCase):
    def test_group_can_cite_verified_member_experience(self):
        d=fixture(); s=copy.deepcopy(d['sources'][0]); s['id']='S2'; s['url']='https://example.org/resume'; d['sources'].append(s)
        d['cases'][0]['identity_link']['source_ids'].append('S2')
        d['cases'][0]['identity_link']['evidence'].append({'source_id':'S2','locator':'same-person resume direct link'})
        d['cases'][0]['experiences']=[{'type':'full_time','relative_timing':'before_application','status':'self_reported','source_ids':['S2'],'evidence':[{'source_id':'S2','locator':'employment section'}]}]
        d['archetypes'][0].update(source_ids=['S2'],evidence=[{'source_id':'S2','locator':'employment section'}])
        self.assertEqual(records.validate(d),[])

    def test_unknown_experience_is_not_member_group_support(self):
        d=fixture(); s=copy.deepcopy(d['sources'][0]); s['id']='S2'; d['sources'].append(s)
        d['cases'][0]['experiences']=[{'type':'employment_unspecified','relative_timing':'unknown','status':'unknown','source_ids':['S2'],'evidence':[{'source_id':'S2','locator':'no employment detail'}]}]
        d['archetypes'][0].update(source_ids=['S2'],evidence=[{'source_id':'S2','locator':'no employment detail'}])
        self.assertTrue(records.validate(d))

    def test_duplicate_conflict_fields(self):
        d=fixture(); f=d['cases'][0]['fields']['undergraduate_school']
        f.update(value=None,status='conflicting',source_ids=['S1'],evidence=[{'source_id':'S1','locator':'school'}])
        c={'field':'undergraduate_school','values':[{'value':v,'source_ids':['S1'],'evidence':[{'source_id':'S1','locator':'school'}]} for v in ('a','b')]}
        d['cases'][0]['conflicts']=[c,copy.deepcopy(c)]
        self.assertTrue(records.validate(d))

    def test_source_access_after_research(self):
        d=fixture(); d['sources'][0]['accessed_on']='2026-10-06'
        self.assertTrue(records.validate(d))

    def test_invalid_calculated_cutoff(self):
        d=fixture(); d['cases'][0]['fields']['work_duration_before_application'].update(value=12,status='calculated',source_ids=['S1'],evidence=[{'source_id':'S1','locator':'dates'}],cutoff='yesterday',calculation='union')
        self.assertTrue(records.validate(d))

    def test_duplicate_field_locator(self):
        d=fixture(); e=d['cases'][0]['fields']['enrollment_status']['evidence']; e.append(copy.deepcopy(e[0]))
        self.assertTrue(records.validate(d))

    def test_blank_known_value(self):
        d=fixture(); d['cases'][0]['fields']['undergraduate_school'].update(value='  ',status='documented',source_ids=['S1'],evidence=[{'source_id':'S1','locator':'school'}])
        self.assertTrue(records.validate(d))

    def test_negative_or_boolean_numeric_duration(self):
        for value in (-1, True):
            d=fixture(); d['cases'][0]['fields']['work_duration_before_application'].update(value=value,status='self_reported',source_ids=['S1'],evidence=[{'source_id':'S1','locator':'duration'}])
            with self.subTest(value=value): self.assertTrue(records.validate(d))

    def test_conflicting_admission_preserved_outside_group(self):
        d=fixture(); d['archetypes']=[]; d['cases'][0]['fields']['enrollment_status'].update(value=None,status='conflicting')
        d['cases'][0]['conflicts']=[{'field':'enrollment_status','values':[{'value':v,'source_ids':['S1'],'evidence':[{'source_id':'S1','locator':'status'}]} for v in ('enrolled','rejected')]}]
        # Conflict is deliberately allowed and preserved; it may never join an admitted group.
        self.assertEqual(records.validate(d),[])

    def test_all_nested_mutations_never_crash_or_mutate(self):
        base=fixture(); paths=[]
        def walk(x,p=()):
            if isinstance(x,dict):
                for k,v in x.items(): paths.append(p+(k,)); walk(v,p+(k,))
            elif isinstance(x,list):
                for i,v in enumerate(x): paths.append(p+(i,)); walk(v,p+(i,))
        walk(base)
        for p in paths:
            for value in (None,True,0,[],{},'', ['x'], {'x':1}):
                d=copy.deepcopy(base); parent=d
                for k in p[:-1]: parent=parent[k]
                parent[p[-1]]=value; before=copy.deepcopy(d)
                with self.subTest(path=p,value=value):
                    result=records.validate(d)
                    self.assertIsInstance(result,list); self.assertEqual(d,before)

class IntervalBatch(unittest.TestCase):
    def test_5000_random_intervals_against_month_sets(self):
        rng=random.Random(20261005)
        for _ in range(5000):
            cutoff=rng.randrange(12,120); intervals=[]; low=set(); high=set()
            def date(n): return f'{2000+n//12:04d}-{n%12+1:02d}'
            for _ in range(rng.randrange(0,16)):
                start=rng.randrange(0,150); end=rng.choice([None,rng.randrange(start,160)]); inclusive=rng.choice([True,False,None])
                intervals.append({'start':date(start),'end':None if end is None else date(end),'end_inclusive':inclusive})
                low.update(range(start,min(cutoff,cutoff if end is None else end+int(inclusive is True))))
                high.update(range(start,min(cutoff,cutoff if end is None else end+int(inclusive is not False))))
            data={'cutoff':date(cutoff),'intervals':intervals}; before=copy.deepcopy(data)
            result=months.calculate(data)
            self.assertEqual((result['min_months'],result['max_months']),(len(low),len(high)))
            self.assertEqual(data,before)
            rng.shuffle(intervals)
            self.assertEqual(months.calculate(data),result)
            data['intervals']=intervals+intervals
            self.assertEqual(months.calculate(data),result)

    def test_invalid_shapes_raise_value_error(self):
        for data in ([],None,{}, {'cutoff':'2021-01','intervals':[None]}, {'cutoff':'2021-01','intervals':[{}]}):
            with self.subTest(data=data),self.assertRaises(ValueError): months.calculate(data)

    def test_cli_strict_json(self):
        for content in ('{"cutoff":"2021-01","cutoff":"2022-01","intervals":[]}', '{"cutoff":"2021-01","intervals":[],"extra":NaN}', '{"cutoff":"2021-01","intervals":[null]}'):
            with tempfile.TemporaryDirectory() as folder:
                p=Path(folder)/'input.json';p.write_text(content)
                r=subprocess.run([sys.executable,str(SCRIPTS/'work_months.py'),str(p)],capture_output=True,text=True)
                self.assertEqual(r.returncode,1);self.assertNotIn('Traceback',r.stderr)

if __name__=='__main__': unittest.main()
