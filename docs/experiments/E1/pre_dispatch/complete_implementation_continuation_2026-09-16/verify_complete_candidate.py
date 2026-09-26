from pathlib import Path
import json
from adapter.context_projection import sha,digest,derive,read_exact,canonical
from adapter.continuation_envelope import archive
from adapter.governance_continuation import GovernanceContinuation
from adapter.context_binding import CommittedContext
R=Path('/home/gvasend/app/kge-forge');B=R/'docs/experiments/E1/pre_dispatch';O=B/'complete_implementation_continuation_2026-09-16'
def load(p):return json.loads(Path(p).read_bytes())
ends=load(O/'IMPLEMENTATION_ENDPOINTS.json');archive(ends['accepted_versioned_capture']);archive(load(O/'QUALIFICATION_CAPTURE.json'))
for p,h in ends['candidate_files'].items():read_exact(p,h)
spec=load(O/'PROPOSED_SPECIFICATION.json');gov=GovernanceContinuation(spec);op=load(O/'PROPOSED_OPERATIONAL_BINDING.json');launch=load(op['released_launch']['path'])
ctx=CommittedContext(B/'CONTEXT_MANIFEST.json',launch['authorization']['context_binding']['capture_commit'],spec)
result=derive(json.loads(launch['authorization']['context_projection']),ctx)
assert all(result[k]==v for k,v in op['context_identities'].items())
old=load(spec['anchor']['operational_binding']['path']);projection=load(spec['anchor']['projection']['path'])
assert result['projection']['payload']==projection['payload']
dispatch_path=B/'dispatch_authorization_2026-09-16/DISPATCH_RECORD.json';read_exact(str(dispatch_path),'08f721ab75f001d5b2a4a91c259cf52174b78d4060e0d0ecacdcc2b7ae1abaf7')
dispatch=load(dispatch_path);audit=Path(dispatch['all_authorized_bindings']['audit']);ledger=Path(dispatch['all_authorized_bindings']['ownership_ledger'])
read_exact(str(audit),'e4d8a91d0692bb48ad323005b45603cbbd2834a6babdb08b8f846b742ae1e883')
assert ledger.read_bytes()==b'' and not Path(str(ledger)+'.controller-lock').exists()
assert digest(old)=='8cfa01bc69f36465d766809bd5731ce97f18b019023b6192f8d4817457e9d792'
assert len(spec['records'])==1 and spec['identities']['OperationalContextId']!=old['governance']['identities']['OperationalContextId']
for r in [old['governance']['release_basis'],old['governance']['release_decision'],old['governance']['released_profile'],old['released_launch'],old['governance']['clearance'],*old['governance']['chain']]:read_exact(r['path'],r['sha256'])
print(canonical({'result':'PASS','independent_process':True,'prospective_verifier':'PASS with unissued proposed approval, NOT adoption','reconstructed':op['context_identities'],'ancestry_nodes':gov.ancestry,'production_files_verified':len(ends['candidate_files']),'historical_INACTIVE_audit_sha256':sha(audit.read_bytes()),'ownership_ledger_bytes':0,'E1_controller_lock_created':False,'current_authoritative_binding_unchanged':digest(old),'dispatch_record_sha256':sha(dispatch_path.read_bytes()),'PD06':'RELEASED','E1_B01':'PASS','E1':'INACTIVE','E1_WP_001':'INELIGIBLE / UNDISPATCHED','continuation_applied':False,'real_E1_activation_events_created':0,'real_E1_ownership_acquired':False,'real_E1_model_requests':0,'real_E1_implementation_effects':0}))
