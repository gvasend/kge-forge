"""Independent read-only recovery of the exact authorized r9 publication."""
import json,sys,time
from pathlib import Path
from adapter.context_projection import canonical,sha
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.activation_transaction import ActivationTransaction
pin=json.loads(Path(sys.argv[1]).read_bytes());b=Path(pin['path']).read_bytes();assert sha(b)==pin['sha256'];p=json.loads(b)
s=ControllerAuthorityStore(**p['selected_store']);begin=time.monotonic()
with s.session():
 a=reconstruct_authorization(s,s.applicability['authorization_id']);tx=ActivationTransaction.recover(a,p['audit'],p['dispatch']['authority_id'])
 try:r=dict(tx.recovery,seconds=time.monotonic()-begin,independent_process=True)
 finally:tx.close()
s.close();print(canonical(r))
