"""Verify exact R2 with both historical and synthetic extension evidence present."""
import sys,json,tempfile,subprocess
from pathlib import Path
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O))
import test_integration as t
from adapter.controller_authority_store import ControllerAuthorityStore,encoded
base=ControllerAuthorityStore(**t.t.PIN['selected_store'])
sample=json.loads((O/'SYNTHETIC_RECORDS.json').read_bytes())[0]
extension=ControllerAuthorityStore(**sample['store_pin'])
try:
 records={}
 for store in (base,extension):
  for identity in store.catalog['objects']:
   data=store.resolve(identity)
   if identity in records:assert records[identity]['bytes']==data
   records[identity]={'bytes':data,'evidence':[]}
 app=dict(base.applicability);app.update(dict(extension.applicability))
 state=dict(base.catalog['private_state']);state.update(dict(extension.catalog['private_state']))
 root=Path(tempfile.mkdtemp(prefix='R2-combined-qualification-'));root.chmod(0o700)
 combined=ControllerAuthorityStore.materialize(root/'store',records,{},
   {'authority_source':sample['candidate_ref'],'release_identities':sample['delegation']['context']},app,[],state)
 try:
  pin={'root':str(combined.root),'catalog_sha256':combined.catalog_sha256,'applicability':combined.applicability}
  selected=t.a.reconstruct(combined,base)
  expected={'runtime_head_authority':sample['delegation']['lineage'],'runtime':selected['runtime'],'head_event':selected['head']}
  code='''import sys,json
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from adapter import runtime_adoption as r
from adapter.controller_authority_store import ControllerAuthorityStore,sha
s=ControllerAuthorityStore(**json.loads(sys.argv[2]))
try:
 try:r.validate_invocation_runtime(s,json.loads(sys.argv[3]),sys.argv[1]);out={'result':'UNEXPECTED_ACCEPT'}
 except ValueError as e:out={'result':'REJECTED','reason':str(e)}
 out['consumer_sha256']=sha(Path(r.__file__).read_bytes());print(json.dumps(out))
finally:s.close()
'''
  child=subprocess.run([sys.executable,'-B','-c',code,t.t.PIN['consumer_root'],json.dumps(pin),json.dumps(expected)],capture_output=True,text=True,timeout=30)
  assert child.returncode==0,child.stderr
  result=json.loads(child.stdout);assert result['result']=='REJECTED'
  result.update(qualification_only=True,combined_store_pin=pin,all_legacy_and_extension_objects_present=True,
    external_reconstruction=selected['runtime'],expected_binding=expected,real_authority_changes=False)
  with (O/'EXACT_R2_COMBINED_CATALOG.json').open('xb') as stream:stream.write(encoded(result))
  print(json.dumps(result,indent=2))
 finally:combined.close()
finally:base.close();extension.close()
