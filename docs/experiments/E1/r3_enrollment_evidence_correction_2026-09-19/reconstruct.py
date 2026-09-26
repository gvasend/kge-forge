import json,sys,importlib.util,time
from pathlib import Path
from structured_evidence import validate
O=Path(__file__).resolve().parent;pin=json.loads((O/'AUTHORIZED_ENROLLMENT_SELECTION.json').read_bytes());sys.path.insert(0,pin['consumer_root'])
from adapter import runtime_adoption as r,runtime_bootstrap as b
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha
sp=importlib.util.spec_from_file_location('enrollment_verifier',pin['enrollment_module']);en=importlib.util.module_from_spec(sp);sp.loader.exec_module(en)
s=ControllerAuthorityStore(**pin['selected_store']);base=ControllerAuthorityStore(**pin['base_store']);d=en.delegation(s);row=json.loads((O/'ENROLLMENT_RESULT.json').read_bytes());start=time.monotonic();neg=[]
assert sha(Path(pin['enrollment_module']).read_bytes())==pin['enrollment_module_sha256']
for label in ('qualification_report','architect_instruction'):
 data=(O/(label+'.json')).read_bytes();validate(label,data);assert s.resolve('sha256:'+sha(data))==data
assert en.require_eligible(s,base,pin['candidate'],row['id'],binding_kind='PRODUCTION_ENROLLMENT')==row
with en.lock(s,d,False) as fd:assert en.history(s,d,fd)==[row]
journal=s.state_path(d['journal']);journal_before=journal.read_bytes()
def reject(name,fn):
 try:fn()
 except Exception as exc:neg.append({'test':name,'result':'REJECTED','reason':str(exc)})
 else:raise AssertionError(name+' unexpectedly accepted')
reject('enrollment_replay',lambda:en.enroll(s,base,pin['candidate'],pin['qualification'],pin['decision'],binding_kind='PRODUCTION_ENROLLMENT'))
assert journal.read_bytes()==journal_before
for name,ref in [('qualification_cannot_adopt',pin['qualification']),('enrollment_decision_cannot_adopt',pin['decision']),('candidate_cannot_self_adopt',pin['candidate'])]:
 reject(name,lambda ref=ref:en.trusted(s,'runtime-adoption-decision',ref))
assert not any(k.startswith('runtime-adoption-decision:') for k in s.catalog['objects'])
reject('filesystem_presence_cannot_select_R3',lambda:r.validate_invocation_runtime(base,pin['base_binding'],pin['runtime']['root']))
reject('caller_asserted_R3_head',lambda:r.validate_invocation_runtime(base,dict(pin['base_binding'],runtime=pin['runtime']['identity']),pin['runtime']['root']))
reject('R2_cannot_substitute',lambda:r.validate_invocation_runtime(base,dict(pin['base_binding'],runtime='sha256:a37de248a046263db9269e88d4714bfd1d9468719dbff3365d77bde2c501bc3c'),pin['runtime']['root']))
reject('different_candidate_cannot_use_enrollment',lambda:en.require_eligible(s,base,{'authority_id':'sha256:'+'0'*64,'sha256':'0'*64},row['id'],binding_kind='PRODUCTION_ENROLLMENT'))
reject('raw_Markdown_remains_rejected',lambda:r.read(s,pin['intake']['source']))
state=r.reconstruct(base);assert state['current_runtime']==pin['R1'] and state['head_event']==pin['base_binding']['head_event'] and state['pending'] is None
assert b.reconstruct(base)['state']=='SUCCESSOR_CURRENT'
for name,h in pin['baseline'].items():assert sha(Path(name).read_bytes())==h
_,record,_=b.verify_records(base);b.fresh_supervisor(base,record)
result={'result':'PASS','independent_process':True,'enrollment':row['id'],'enrollment_file_sha256':sha(encoded(row)),'eligibility':'ENROLLED_ELIGIBLE_FOR_ADOPTION','R1_current':state['current_runtime'],'runtime_head':state['head_event'],'runtime_head_authority':r.policy(base)['id'],'R3':pin['runtime']['identity'],'R3_adopted':False,'R3_current':False,'S3':'READY','negatives':neg,'original_runtime_bootstrap_journals_unchanged':True,'enrollment_event_count':1,'enrollment_journal_sha256':sha(journal_before),'seconds':time.monotonic()-start,'r13_created':False,'model_requests':0,'E1_effects':0}
with (O/'INDEPENDENT_RECONSTRUCTION.json').open('xb') as f:f.write(encoded(result))
s.close();base.close();print(json.dumps(result,indent=2))
