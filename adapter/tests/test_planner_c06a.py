"""Independent budget oracle and real importer regression. No E1 mutations."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from adapter.planner import codec as c, core, model as m, replay

ROOT = Path(__file__).resolve().parents[2]
ORACLE = ROOT / 'docs/plans/DETERMINISTIC_PLANNER_V0_1_BUDGET_PROOF_MATRIX_ORACLE_1.json'
PARAMETER_PIN = '1b0533a7c24306c2452a68df1b5777d1b6d699420aa1947b1b3ac5ef5d5079f7'

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()).hexdigest()


def independent_positive(document):
    """Contract equations; no planner helper/result is used as an oracle."""
    p, s = document['qualification_parameters'], document['positive_submission']
    assert digest({k:v for k,v in p.items() if k!='parameters_sha256'}) == PARAMETER_PIN
    e = p['expected_envelope']; assert s['envelope']==e and not s['invalidated_ids']
    records = {r['id']:r['body'] for r in s['records']}
    assert len(records)==17 and len(s['rows'])==8
    grants = {g['record_id']:g for g in p['trusted_record_grants']}
    for identity, body in records.items():
        assert digest(body)==identity
        assert body['envelope']==e and body['generation']==p['anchor']['generation']
        assert body['anchor']==p['anchor']['id']
        assert grants[identity]['producer']==body['producer']
    a=records[s['source_authentication_id']]
    assert a['authority_identity']==e['authority'] and a['identity_verified'] and a['owning_policy_preserved']
    for row in s['rows']:
        f=records[row['fact_id']]['facts']; r=records[row['rule_id']]['policy']; name=row['id']
        assert records[row['rule_id']]['rule_profile']=='EXACT_CHECKPOINT_1'
        if name.endswith('AVAILABILITY_PUBLICATION'):
            assert f['available'] and f['authority_body']==e['authority'] and f['store']==e['controller_store'] and (r['publication']=='NOT_REQUIRED' or (r['publication']=='REQUIRED' and f['published']))
        elif name.endswith('SCOPE'):
            assert all(f[k]==r[k]==e[k] for k in ('source_scope','target_scope','operation')) and r['permitted']
        elif name.endswith('LINEAGE'):
            assert f['source_lineage']==f['target_lineage']==r['selected_lineage']==e['lineage'] and f['selected_release']==r['selected_release']==e['release'] and not f['superseded']
        elif name.endswith('RUNTIME'):
            assert f['source_runtime']==f['target_runtime']==r['selected_runtime']==e['runtime'] and f['content_verified'] and f['selection_current']
        elif name.endswith('CONTROLLER_STORE_G4'):
            assert f['source_store']==f['target_store']==r['selected_store']==e['controller_store'] and f['authority']==e['authority'] and f['membership']
        elif name.endswith('PROGRAMMER_PROFILE'):
            assert f['profile']==r['profile']==e['profile'] and (r['profile_check']=='NOT_APPLICABLE' or (r['profile_check']=='REQUIRED' and f['identity_verified'] and f['target_binding'] and not f['superseded']))
        elif name.endswith('TEMPORAL_CURRENTNESS'):
            assert f['authority']==e['authority'] and f['invocation']==e['invocation'] and all(r.values()) and not f['revoked'] and not f['superseded'] and f['single_use_available']
        elif name.endswith('EXECUTION_REQUEST_PHASE'):
            assert f['source_phase']==r['source_phase']=='FIRST_PROGRAMMER_EXECUTION' and f['target_phase']==r['target_phase']=='FIRST_PROGRAMMER_REQUEST' and f['operation']==r['operation']==e['operation'] and r['permitted'] and r['effects_allowed']==[]
        else: raise AssertionError(name)
    return True


def write_input(directory, document=None):
    doc = document or json.loads(ORACLE.read_text())
    data={'schema':'PLANNER-BUDGET-QUALIFICATION-1', 'parameters':doc['qualification_parameters'],
          'submission':doc['positive_submission']}
    sources=Path(directory)/'budget.sources'; sources.mkdir(exist_ok=True)
    normalized=dict(data['submission'],records=sorted(data['submission']['records'],key=lambda r:r['id']), rows=sorted(data['submission']['rows'],key=lambda r:r['id']), invalidated_ids=sorted(data['submission']['invalidated_ids'],key=lambda v:json.dumps(v,sort_keys=True)))
    for value in [data['parameters'],normalized]+[r['body'] for r in data['submission']['records']]:
        (sources/(digest(value)+'.json')).write_bytes(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode())
    path=Path(directory)/'budget.json'; path.write_text(json.dumps(data,sort_keys=True))
    return path


class BudgetRestorationTests(unittest.TestCase):
    def test_positive_full_restoration(self):
        doc=json.loads(ORACLE.read_text())
        self.assertTrue(independent_positive(doc))
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            path=write_input(directory,doc)
            # Real public import boundary, no mocked validator or patched loaded state.
            bundle,events,expected=replay.import_fixture(path,ROOT)
            restored=c.decode_snapshot(c.snapshot_bytes(bundle.current))
            self.assertEqual(len(restored.budget_matrices),1)
            matrix=restored.budget_matrices[0]
            self.assertEqual(json.loads(matrix.parameters),doc['qualification_parameters'])
            actual=json.loads(matrix.submission); wanted=doc['positive_submission']
            self.assertEqual({r['id']:r for r in actual['records']},{r['id']:r for r in wanted['records']})
            self.assertEqual({r['id']:r for r in actual['rows']},{r['id']:r for r in wanted['rows']})
            for key in ('envelope','source_authentication_id','invalidated_ids','schema','mode'):
                self.assertEqual(actual[key],wanted[key])
            for key,value in wanted['envelope'].items():
                field=getattr(matrix.envelope,key)
                if type(value) is dict:
                    self.assertEqual((field.kind.value,field.namespace,field.sha256),(value['kind'],value['namespace'],value['sha256']))
                else:self.assertEqual(field,value)
            proof=json.loads(next(k.statement for k in restored.knowledge if k.id==matrix.knowledge))
            self.assertEqual(proof['type'],'BUDGET_APPLICABILITY_PROOF_MATRIX_V1')
            self.assertEqual(proof['source_authentication_id'],wanted['source_authentication_id'])
            self.assertEqual(proof['parameter_identity']['sha256'],PARAMETER_PIN)
            self.assertEqual(proof['envelope'],wanted['envelope'])
            self.assertEqual(proof['anchor'],doc['qualification_parameters']['anchor'])
            self.assertEqual(proof['invalidated_ids'],[])
            self.assertEqual(matrix.identity.sha256,digest(proof))
            for row in proof['rows']:
                self.assertEqual(row['proof_state'],'PROVED')
                self.assertEqual(row['envelope'],wanted['envelope'])
                self.assertEqual(row['generation'],7)
                self.assertEqual(row['anchor'],'TEST-CHECKPOINT-7')
            self.assertEqual(len(matrix.evidence),19)
            by_id={r['id']:r for r in wanted['rows']}
            for row in matrix.rows:
                self.assertEqual(row.fact.sha256,by_id[row.obligation.value]['fact_id'])
                self.assertEqual(row.rule.sha256,by_id[row.obligation.value]['rule_id'])
            self.assertEqual({r.obligation.value for r in matrix.rows},{r['id'] for r in doc['positive_submission']['rows']})
            result=core.apply_result(restored, m.SuppliedResult(m.ActionId('FACT-BUDGET-APPLICABILITY'),m.ActionResult.PASS,
                next(a.accepted_inventory for a in restored.actions if a.id.value=='FACT-BUDGET-APPLICABILITY'),c.snapshot_id(restored)))
            self.assertEqual(restored.roots,result.snapshot.roots)
            self.assertEqual(restored.slots,result.snapshot.slots)
            self.assertEqual(result.snapshot.roots[0].state,m.ConditionState.UNRESOLVED)
            self.assertEqual(result.snapshot.slots[0].state,m.SlotState.UNRESOLVED)
            self.assertNotIn(m.ActionId('FACT-BUDGET-APPLICABILITY'),result.computation.actionable)
            self.assertIn(m.ActionId('QUALIFICATION-REEVAL-BUDGET'),result.computation.actionable)

    def test_negative_oracle_semantics_and_import(self):
        from adapter.planner import budget
        original=json.loads(ORACLE.read_text())
        mutations=[('AVAILABILITY_PUBLICATION','facts','available',False),
            ('SCOPE','facts','target_scope','TEST/WRONG'),
            ('LINEAGE','facts','source_lineage',{'kind':'CANONICAL_OBJECT_IDENTITY','namespace':'WRONG','sha256':'1'*64}),
            ('RUNTIME','facts','source_runtime',{'kind':'CONTENT_IDENTITY','namespace':'WRONG','sha256':'1'*64}),
            ('CONTROLLER_STORE_G4','facts','target_store',{'kind':'CANONICAL_OBJECT_IDENTITY','namespace':'WRONG','sha256':'1'*64}),
            ('PROGRAMMER_PROFILE','facts','profile',{'kind':'AUTHORITY_IDENTITY','namespace':'ReleasedProfileAuthority','sha256':'1'*64}),
            ('EXECUTION_REQUEST_PHASE','policy','permitted',False),
            ('EXECUTION_REQUEST_PHASE','policy','effects_allowed',['EXECUTE']),
            ('TEMPORAL_CURRENTNESS','facts','revoked',True),
            ('TEMPORAL_CURRENTNESS','facts','single_use_available',False),
            ('AVAILABILITY_PUBLICATION','facts','available','true'),
            ('AVAILABILITY_PUBLICATION','policy','publication','UNKNOWN')]
        for suffix,section,key,value in mutations:
            with self.subTest(suffix=suffix,key=key):
                doc=copy.deepcopy(original);p=doc['qualification_parameters'];s=doc['positive_submission']
                row=next(r for r in s['rows'] if r['id'].endswith(suffix))
                refkey='rule_id' if section=='policy' else 'fact_id'; old=row[refkey]
                record=next(r for r in s['records'] if r['id']==old)
                record['body'][section][key]=value
                record['id']=digest(record['body']);row[refkey]=record['id']
                next(g for g in p['trusted_record_grants'] if g['record_id']==old)['record_id']=record['id']
                p['parameters_sha256']=digest({k:v for k,v in p.items() if k!='parameters_sha256'})
                # Explicit independently admitted negative variant: do not merely
                # fail its checksum. The governing row expression must reject it.
                with self.assertRaises(m.PlannerError):budget.validate_input(p,s,p['parameters_sha256'])
                with tempfile.TemporaryDirectory(dir=ROOT) as directory:
                    with self.assertRaises(m.PlannerError):replay.import_fixture(write_input(directory,doc),ROOT)
        for mutation in ('missing_row','missing_rule','stale','envelope','identity','unknown_rule','missing_grant','source_auth','duplicate','unknown_field','invalidation'):
            with self.subTest(mutation=mutation):
                doc=copy.deepcopy(original);p=doc['qualification_parameters'];s=doc['positive_submission']
                if mutation=='missing_row':s['rows'].pop()
                elif mutation=='missing_rule':s['rows'][0]['rule_id']='0'*64
                elif mutation=='missing_grant':p['trusted_record_grants'].pop()
                elif mutation=='source_auth':s['source_authentication_id']='0'*64
                elif mutation=='duplicate':s['rows'].append(copy.deepcopy(s['rows'][0]))
                elif mutation=='unknown_field':s['other']=True
                elif mutation=='invalidation':s['invalidated_ids']=[s['rows'][0]['fact_id']]
                else:
                    row=s['rows'][0]; ref='rule_id' if mutation=='unknown_rule' else 'fact_id'
                    old=row[ref];rec=next(r for r in s['records'] if r['id']==old)
                    if mutation=='stale':rec['body']['generation']=6
                    elif mutation=='envelope':rec['body']['envelope']['invocation']['sha256']='1'*64
                    elif mutation=='identity':rec['body']['facts']['authority_body']['kind']='CONTENT_IDENTITY'
                    else:rec['body']['rule_profile']='UNKNOWN'
                    rec['id']=digest(rec['body']);row[ref]=rec['id']
                    next(g for g in p['trusted_record_grants'] if g['record_id']==old)['record_id']=rec['id']
                p['parameters_sha256']=digest({k:v for k,v in p.items() if k!='parameters_sha256'})
                with self.assertRaises(m.PlannerError):budget.validate_input(p,s,p['parameters_sha256'])
                with tempfile.TemporaryDirectory(dir=ROOT) as directory:
                    with self.assertRaises(m.PlannerError):replay.import_fixture(write_input(directory,doc),ROOT)

    def test_each_source_invalidation_after_reload(self):
        from adapter.planner import gates
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            b,_,_=replay.import_fixture(write_input(directory),ROOT)
            original=c.decode_snapshot(c.snapshot_bytes(b.current));aid=m.ActionId('FACT-BUDGET-APPLICABILITY')
            self.assertIn(aid,core.recompute(original).actionable)
            self.assertEqual(core.recompute(original).control,m.ControlState.RUNNABLE)
            self.assertEqual(next(s.state for s in original.statuses if s.id.value=='REEVAL-BUDGET'),m.ActionState.BLOCKED)
            for assertion in original.assertions:
                if assertion.id.value=='budget-action-contract': continue
                with self.subTest(source=assertion.id):
                    stale=c.invalidate_sources(original,(assertion.provenance.identity,))
                    restored=c.decode_snapshot(c.snapshot_bytes(stale))
                    self.assertNotIn(aid,core.recompute(restored).actionable)
                    self.assertNotEqual(core.recompute(restored).control,m.ControlState.RUNNABLE)
                    self.assertNotEqual(gates.evaluate_predicate(restored,m.PredicateId('budget-matrix')).state,m.ProofState.PROVED)
                    self.assertEqual(core.recompute(stale),core.recompute(restored))
            # Refined C06 source remains an additional independent prerequisite.
            history=next(k for k in original.knowledge if k.producer==m.ActionId('REEVAL-BUDGET'))
            stale=c.invalidate_sources(original,(history.provenance.identity,))
            self.assertNotIn(aid,core.recompute(c.decode_snapshot(c.snapshot_bytes(stale))).actionable)
            self.assertEqual(original.roots,stale.roots); self.assertEqual(original.slots,stale.slots)

    def test_restored_contract_cannot_lose_members(self):
        from dataclasses import replace
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            b,_,_=replay.import_fixture(write_input(directory),ROOT);s=b.current;matrix=s.budget_matrices[0]
            with self.assertRaises(m.PlannerError):c.bundle_bytes(replace(b,scope='FULL_FROZEN_E1_REPLAY',policy_version='E1-SELECTION-1-P06'))
            corruptions=[replace(s,budget_matrices=(replace(matrix,parameters=json.dumps(json.loads(matrix.parameters),indent=2)),)),
                replace(s,budget_matrices=()),
                replace(s,budget_matrices=(replace(matrix,rows=matrix.rows[:-1]),)),
                replace(s,budget_matrices=(replace(matrix,evidence=matrix.evidence[:-1]),)),
                replace(s,budget_matrices=(replace(matrix,envelope=replace(matrix.envelope,runtime=matrix.envelope.authority)),)),
                replace(s,actions=tuple(replace(a,requirements=()) if a.id==matrix.consumer else a for a in s.actions)),
                replace(s,actions=tuple(replace(a,accepted_inventory=()) if a.id==matrix.consumer else a for a in s.actions))]
            for corrupt in corruptions:
                with self.assertRaises(m.PlannerError):c.decode_snapshot(c.snapshot_bytes(corrupt))

    def test_persisted_events_cold_process_and_permutations(self):
        import os,subprocess,sys
        from dataclasses import replace
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            path=write_input(directory); b,_,_=replay.import_fixture(path,ROOT)
            action=next(a for a in b.current.actions if a.id.value=='FACT-BUDGET-APPLICABILITY')
            supplied=m.SuppliedResult(action.id,m.ActionResult.PASS,action.accepted_inventory,c.snapshot_id(b.current))
            done=c.record_result(b,supplied)
            saved,ident=c.save_bundle(done,Path(directory)/'saved',ROOT)
            self.assertEqual(c.bundle_bytes(c.restore(saved,ident,ROOT)),c.bundle_bytes(done))
            outputs=[]
            script='''import json,sys
from pathlib import Path
from adapter.planner import codec as c,replay,core
b=c.restore(Path(sys.argv[1]),c._unwire(json.loads(sys.argv[2])),Path(sys.argv[3]))
s=core.recompute(b.current)
print(json.dumps({'state':c.snapshot_id(b.current).sha256,'actionable':[a.value for a in s.actionable],'selected':s.selection.selected.value if s.selection else None,'control':s.control.value if s.control else None},sort_keys=True))'''
            for seed in ('0','31','777'):
                outputs.append(subprocess.check_output([sys.executable,'-c',script,str(saved),json.dumps(c._wire(ident)),str(ROOT)],env=dict(os.environ,PYTHONHASHSEED=seed),text=True))
            self.assertEqual(len(set(outputs)),1)
            doc=json.loads(ORACLE.read_text());doc['positive_submission']['records'].reverse();doc['positive_submission']['rows'].reverse()
            changed,_,_=replay.import_fixture(write_input(directory,doc),ROOT)
            self.assertEqual(c.snapshot_bytes(b.current),c.snapshot_bytes(changed.current))
            for _ in range(3):self.assertEqual(core.recompute(b.current),core.recompute(c.decode_snapshot(c.snapshot_bytes(changed.current))))
            raw=json.loads(path.read_text());path.write_text(json.dumps(dict(reversed(list(raw.items())))))
            again,_,_=replay.import_fixture(path,ROOT);self.assertEqual(c.snapshot_bytes(b.current),c.snapshot_bytes(again.current))
            # Persist invalidation itself in the existing append-only replay ledger.
            stale=c.record_result(done,m.SourceInvalidation((b.current.assertions[0].provenance.identity,),c.snapshot_id(done.current)))
            sp,si=c.save_bundle(stale,Path(directory)/'stale',ROOT)
            self.assertEqual(c.bundle_bytes(c.restore(sp,si,ROOT)),c.bundle_bytes(stale))

    def test_cli_profile_and_source_bytes_cannot_be_repaired(self):
        import subprocess,sys
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            path=write_input(directory)
            outputs=[subprocess.check_output([sys.executable,'-m','adapter.planner','validate',str(path)],cwd=ROOT) for _ in range(2)]
            self.assertEqual(outputs[0],outputs[1])
            self.assertFalse(json.loads(outputs[0])['resume_allowed'])
            b,_,_=replay.import_fixture(path,ROOT)
            record=next(p for p in b.sources if 'budget.sources' in p.path)
            (ROOT/record.path).write_bytes((ROOT/record.path).read_bytes()+b' ')
            with self.assertRaises(m.PlannerError):replay.import_fixture(path,ROOT)
