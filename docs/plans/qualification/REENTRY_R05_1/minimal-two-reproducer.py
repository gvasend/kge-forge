from pathlib import Path
from dataclasses import replace
from unittest.mock import patch
import json,hashlib,types
from adapter.planner import codec as c,model as m,validation_transaction as vt
R=Path.cwd();O=R/'docs/plans/qualification/REENTRY_R05_1';oldtext=(O/'pre-repair-validation-implementation.py').read_text();baseline=json.loads((O/'baseline.json').read_text());assert hashlib.sha256(oldtext.encode()).hexdigest()==baseline['adapter/planner/validation_transaction.py']
old=types.ModuleType('adapter.planner._r05_verified_before');old.__package__='adapter.planner';exec(compile(oldtext,'verified-pre-repair-validation_transaction.py','exec'),old.__dict__)
inv=json.loads((R/'docs/plans/qualification/REENTRY_R04_1/checkpoint-inventory.json').read_text());z=inv[-1];b=c.restore(R/z['path'],c._unwire(z['identity']),R);source=b.current.validation_results[0]
inputs=vt.canonical_inputs(source.input_identities[:2]);r=vt.identified(replace(source,input_identities=inputs),'planner-validation-result-record-v1');support=vt.identified(replace(b.current.validation_support_records[0],validation_result_id=r.id,input_identities=inputs),'planner-validation-support-record-v1')
state=replace(b.current,validation_results=(r,),validation_support_records=(support,),validation_instances=tuple(replace(z,inputs=inputs) if z.predicate==vt.predicate_id(r) else z for z in b.current.validation_instances))
rev=replace(state,validation_results=(replace(r,input_identities=tuple(reversed(inputs))),))
assert c.canonical_bytes(c._wire(state))==c.canonical_bytes(c._wire(rev))
assert vt.identified(rev.validation_results[0],'planner-validation-result-record-v1').id==r.id
with patch.object(vt,'validate_records',old.validate_records):
 m.validate_model(state)
 try:m.validate_model(rev)
 except m.PlannerError as e:reason=str(e)
 else:raise AssertionError('expected pre-repair model inconsistency')
assert reason=='VALIDATION_PROJECTION_REQUIRED'
m.validate_model(state);m.validate_model(rev)
(O/'minimal-two-input-counterexample.json').write_text(json.dumps({'role':'ISOLATED_MODEL_COMPONENT_FIXTURE_NOT_EVENT_ADMITTED_STATE','inputs':c._wire(inputs),'canonical_bytes_equal':True,'canonical_identity_equal':True,'pre_repair_V1':'PASS','pre_repair_V2':reason,'post_repair_V1':'PASS','post_repair_V2':'PASS','before_implementation_sha256':hashlib.sha256(oldtext.encode()).hexdigest(),'call_path':['model.validate_model','hash-verified pre-repair validation_transaction.validate_records','inst.inputs == r.input_identities'],'canonical_P04_modified':False},sort_keys=True,indent=2)+'\n')
print('two-input minimal native model counterexample and repair PASS')
