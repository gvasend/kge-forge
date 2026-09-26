"""Independent sealed-store reconstruction. Read-only; no lifecycle mutations."""
import json,sys,os,time,signal
from pathlib import Path
from adapter.context_projection import canonical,sha,derive
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.attempt_transition import selected
from adapter.activation_transaction import invocation
from adapter.invocation_ownership import InvocationOwnership
out=Path(sys.argv[1]);pin=json.loads((out/'CURRENT_PIN.json').read_bytes());b=Path(pin['path']).read_bytes();assert sha(b)==pin['sha256'];pub=json.loads(b)
def expired(*_):raise TimeoutError('independent reconstruction hard phase budget')
signal.signal(signal.SIGALRM,expired);signal.setitimer(signal.ITIMER_REAL,120)
s=ControllerAuthorityStore(**pub['selected_store']);begin=time.monotonic()
with s.session():
 a=reconstruct_authorization(s,s.applicability['authorization_id']);bootstrap=time.monotonic()-begin;g=a.context_binding.governance
 sel=selected();assert sel['mode']=='PREPARED' and sel['specific_invocation_authorization'] is None
 qbytes=s.resolve(sel['qualification']['authority_id']);assert sha(qbytes)==sel['qualification']['sha256'];q=json.loads(qbytes)
 assert q['result']=='PASS' and q['accepted_proposal']==pub['proposal'] and q['controller_runtime']==pub['controller_runtime'] and q['amendment']==pub['amendment']
 for path,h in q['evidence'].items():assert sha(Path(path).read_bytes())==h
 for path,h in q['historical_hashes'].items():assert sha(Path(path).read_bytes())==h
 derived=derive(json.loads(a.context_projection),a.context_binding)
 assert {k:derived[k] for k in pub['context_identities']}==pub['context_identities']
 assert g.identities==pub['operational_identities'] and g.run6['release_authority']==pub['release_authority']
 proof=g.run6['predecessor']['terminal'];assert proof['lifecycle']['state']=='CANCELLED' and not proof['lifecycle']['uncertain'] and proof['scope'] is None and proof['ownership'] is None
 fd=os.open(a.ownership_ledger,os.O_RDONLY|os.O_NOFOLLOW)
 try:assert invocation(fd) is None and InvocationOwnership.__new__(InvocationOwnership)._history(fd) is None
 finally:os.close(fd)
 assert not os.path.lexists(g.run6['proposal']['audit'])
 result={'result':'PASS','status':'QUALIFIED_PREPARED_NOT_ISSUED','bootstrap_seconds':bootstrap,'total_seconds':time.monotonic()-begin,
 'release_authority':pub['release_authority'],'operational_identities':g.identities,'context_identities':pub['context_identities'],
 'r8':'UNISSUED_PROPOSED_AUTHORIZATION_WITH_FAILED_CLOSED_AUDIT_NAMESPACE','r9':'CANCELLED / INTERRUPTED_NO_EFFECTS',
 'r10_audit_unused':True,'ownership':'NONE','handoff_eligible':False,'real_model_requests':0,'effects':0,'historical_hashes_unchanged':True,
 'qualification':pub['qualification'],'source_pin':pin}
s.close();signal.setitimer(signal.ITIMER_REAL,0);(out/'INDEPENDENT_RECONSTRUCTION.json').write_text(canonical(result));print(canonical(result))
