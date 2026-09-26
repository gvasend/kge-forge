"""Fresh-process, read-only real authority reconstruction. No ownership lease."""
import json,sys
from pathlib import Path
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.authorization_lifecycle import dispatch_binding,reconstruct
from adapter.governance_continuation import verify_authorization
from adapter.context_projection import canonical,derive,sha
from adapter.supervisor_amendment import readiness
OUT=Path('/home/gvasend/app/kge-forge/docs/experiments/E1/pre_dispatch/pd06_supervisor_amendment_publication_2026-09-17_final')
selected=json.loads((OUT/'PREPARED_STORE.json').read_bytes())
if len(sys.argv)>2:
 from adapter.controller_authority_store import _directory,_read
 import os
 pin=Path(sys.argv[2]);fd=_directory(pin.parent)
 try:data=_read(fd,pin.name)
 finally:os.close(fd)
 assert sha(data)==sys.argv[3], 'external publication pin hash mismatch'
 publication=json.loads(data)
 assert publication['event']=='material_supervisor_authority_amendment_published'
 assert publication['selected_store']==selected
 selected=publication['selected_store']
store=ControllerAuthorityStore(**selected)
try:
 for identity in store.catalog['objects']:store.resolve(identity)
 print('Private catalog and all objects verified',flush=True)
 with store.session():
  auth=reconstruct_authorization(store,store.applicability['authorization_id'])
  print('Authorization and operational ancestry reconstructed',flush=True)
  op=verify_authorization(auth)
  audit=store.state_path(auth.authorization_id+':audit')
  original=json.loads(store.resolve('sha256:'+op['governance']['material_release']['dispatch_amendment']['sha256']))['original_dispatch']
  ref={**original,'authority_id':'E1-ARCHITECT-DISPATCH-sha256:'+original['sha256']}
  binding=dispatch_binding(auth,audit,ref)
  print('Original dispatch and explicit amendment authenticated',flush=True)
  lifecycle=reconstruct(audit.read_bytes(),auth,audit)
  print('Lifecycle reconstructed',flush=True)
  p=derive(json.loads(auth.context_projection),auth.context_binding)
  assert auth.state=='INACTIVE' and not Path(auth.ownership_ledger).read_bytes()
  try:readiness(auth,store,{},True,lambda *a,**kw:(_ for _ in ()).throw(AssertionError('legacy fallback')))
  except ValueError as e:blocked=str(e)
  else:raise AssertionError('unidentified successor became ready')
  assert 'unknown logical authority' in blocked
  saved=json.loads((OUT/'PRESERVED_STATE.json').read_bytes())
  for path,h in saved.items():assert sha(Path(path).read_bytes())==h
  report={'result':'PASS','identities':op['governance']['identities'],'context_identities':op['context_identities'],
   'ancestry':auth.context_binding.governance.ancestry,'dispatch_binding':binding,'lifecycle':lifecycle,
   'private_store':selected,'objects':len(store.catalog['objects']),'distinct_objects':len({r['sha256'] for r in store.catalog['objects'].values()}),
   'profile_bytes_sha256':op['governance']['released_profile']['sha256'],
   'ModelPayloadDigest':p['ModelPayloadDigest'],'state':'INACTIVE','ownership':'NONE','handoff_eligible':False,
   'current_supervisor_readiness':{'result':'BLOCKED','reason':blocked},'candidate_launch_reported_by_host':True,'candidate_promotion_applied':False,
   'E1_activation_events_created':0,'E1_model_requests':0,'E1_implementation_effects':0}
  target=OUT/(sys.argv[1] if len(sys.argv)>1 else 'INDEPENDENT_RECONSTRUCTION.json')
  with target.open('x') as f:f.write(canonical(report))
  print(canonical({'result':'PASS','report':str(target),'OperationalContextId':op['governance']['identities']['OperationalContextId']}),flush=True)
finally:store.close()
