import json,sys,time,os,tempfile
from pathlib import Path
O=Path(__file__).resolve().parent;Q=O.parent/'runtime_r3_self_hosting_qualified_2026-09-19';pin=json.loads((O/'AUTHORIZED_SELECTION.json').read_bytes());prior=json.loads((O/'ADOPTION_RESULT.json').read_bytes());sys.path.insert(0,pin['runtime_root'])
from adapter import ordinary_runtime as a,runtime_adoption as r
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha
s=ControllerAuthorityStore(**pin['selected_store']);start=time.monotonic();state=a.reconstruct(s);binding=a.binding(s);verified=a.validate_executing_runtime(s,binding)
assert state['runtime']==pin['successor'] and state['pending'] is None and state['head']==prior['state']['head']
assert len(state['events'])==3 and [x['event'] for x in state['events']]==['INTENT','COMMITTED','RECORDED']
assert 'sha256:a37de248a046263db9269e88d4714bfd1d9468719dbff3365d77bde2c501bc3c' not in json.dumps(state)
assert a.validate_production_binding(s,binding,pin['predecessor'])==verified
p,d,anchor=a.policy(s);assert p['binding_kind']=='PRODUCTION_ENROLLMENT'
release,ids=a.production_identities(s,p['legacy_release_context']['release_authority'],{k:v for k,v in p['legacy_release_context'].items() if k!='release_authority'},binding)
legacy=next(v for k,v in sys.modules.items() if k.startswith('_forge_frozen_runtime_') and k.endswith('.runtime_adoption'));boot=sys.modules[legacy.__package__+'.runtime_bootstrap'];Store=sys.modules[legacy.__package__+'.controller_authority_store'].ControllerAuthorityStore
base=Store(**pin['base_store']);_,record,_=boot.verify_records(base);boot.fresh_supervisor(base,record)
for path,h in pin['baseline'].items():assert sha(Path(path).read_bytes())==h
assert s.state_path(d['journal']).stat().st_mode&0o777==0o600
out={'result':'PASS','independent_process':True,'state':state,'binding':binding,'self_hosting':verified,'release_authority':release,'context':ids,'S3':'READY','enrollment_mode':'0600','enrollment_sha256':sha(s.state_path(d['journal']).read_bytes()),'adoption_journal_sha256':sha(s.state_path(p['journal']).read_bytes()),'seconds':time.monotonic()-start,'real_model_requests':0,'E1_effects':0}
with (O/'INDEPENDENT_RECONSTRUCTION.json').open('xb') as f:f.write(encoded(out))
s.close();base.close();print(json.dumps({k:v for k,v in out.items() if k!='state'},indent=2))
