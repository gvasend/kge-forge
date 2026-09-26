"""Read-only exact-continuation application gate; no invocation creation."""
import json,sys,time,hashlib,signal
from pathlib import Path
O=Path(__file__).resolve().parent;Q=O.parent/'run2_control_plane_binding_2026-09-18'
pub=json.loads((Q/'QUALIFIED_PUBLICATION.json').read_bytes());c=json.loads((Q/'PROPOSED_PRODUCTION_CONTINUATION.json').read_bytes())
root=str(Path(c['artifacts'][0]['new_blob']).parent.parent);sys.path.insert(0,root)
from adapter.context_projection import sha,digest,canonical
from adapter.continuation_envelope import seal,BODY_KEYS
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('120s hard phase limit')));signal.alarm(120)
t=time.monotonic();assert sha((Q/'PROPOSED_PRODUCTION_CONTINUATION.json').read_bytes())==pub['proposed_production_continuation_file_sha256']
assert c==seal({k:c[k] for k in BODY_KEYS},None) and c['continuation_id']==pub['proposed_production_continuation']
assert 'sha256:'+digest({f.name:sha(f.read_bytes()) for f in Path(root,'adapter').glob('*.py')})==pub['implementation']
for row in c['artifacts']:
 assert sha(Path(row['new_blob']).read_bytes())==row['new_sha256']
 if row['old_blob']:assert sha(Path(row['old_blob']).read_bytes())==row['old_sha256']
store=ControllerAuthorityStore(**pub['candidate_store'])
with store.session():
 assert json.loads(store.resolve(pub['proposed_continuation_ref']['authority_id']))==c
 for row in c['artifacts']:assert sha(store.resolve(row['new_content']['authority_id']))==row['new_sha256']
store.close()
pin=json.loads((O.parent/'run2_r12_dispatch_2026-09-18/CURRENT_PIN.json').read_bytes());raw=Path(pin['path']).read_bytes();assert sha(raw)==pin['sha256'];oldpub=json.loads(raw)
s=ControllerAuthorityStore(**oldpub['selected_store'])
with s.session():
 aid=s.applicability['authorization_id'];selection=json.loads(s.resolve(aid+':attempt-chain'));a=json.loads(s.resolve(aid));op=json.loads(a['operational_binding'])
 assert c['predecessor_OperationalContextId']==s.applicability['OperationalContextId'] and c['predecessor_chain_digest']==s.applicability['continuation_chain_digest']
 amendment=json.loads(s.resolve(selection['amendment']['authority_id']));runtime=json.loads(s.resolve(amendment['controller_runtime']['authority_id']))
 try: reconstruct_authorization(s,aid)
 except ValueError as e: failure=str(e)
 else:raise AssertionError('expected exact old runtime rejection absent')
 assert failure=='unaccounted runtime',failure
 audit=Path(oldpub['audit']);auditsha=sha(audit.read_bytes());ledger=Path(a['ownership_ledger']);ledgersha=sha(ledger.read_bytes())
s.close()
result={'verdict':'BLOCKED_PRODUCTION_CONTINUATION_CONSUMPTION','exact_candidate_integrity':'PASS','predecessor_identity':'PASS','ordinary_context_schema':op['governance']['schema'],'production_reconstruction_error':failure,'continuation':c['continuation_id'],'continuation_sha256':pub['proposed_production_continuation_file_sha256'],'qualified_runtime':pub['implementation'],'ordinary_context_required_runtime':runtime['identity'],'ordinary_context_required_continuation':selection['continuation'],'proposed_context_not_applied':c['OperationalContextId'],'current_context':pub['real_historical_context'],'current_release':pub['real_release_authority'],'seconds':time.monotonic()-t,'historical_audit':{'path':str(audit),'sha256':auditsha},'real_ledger':{'path':str(ledger),'sha256':ledgersha},'applied':False,'r13_created':False,'real_model_requests':0,'effects':0}
(O/'APPLICATION_GATE.json').write_text(canonical(result));print(canonical(result))
