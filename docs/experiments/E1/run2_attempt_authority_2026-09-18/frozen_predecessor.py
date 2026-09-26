"""Read-only peer executed by the original, unchanged released controller.

No invocation issuance, activation, ownership write, or model transport entry.
"""
import json,sys,time
from pathlib import Path
from adapter.context_projection import canonical,sha,derive
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.authorization_lifecycle import dispatch_binding
from adapter.supervisor_amendment import readiness,authenticated_policy
from adapter.activation_transaction import _host

pin=json.loads(sys.argv[1]);data=Path(pin['path']).read_bytes()
assert sha(data)==pin['sha256']
pub=json.loads(data);store=ControllerAuthorityStore(**pub['selected_store'])
with store.session():
    auth=reconstruct_authorization(store,store.applicability['authorization_id'])
    g=auth.context_binding.governance
    with store.witness() as witness:
        g.verify()
        ref={'authority_id':pub['dispatch_ref'],'sha256':pub['dispatch_ref'].split(':')[-1]}
        binding=dispatch_binding(auth,pub['audit'],ref)
        if sys.argv[2]=='context':
            derived=derive(json.loads(auth.context_projection),auth.context_binding)
            mutable={p:r['new_sha256'] for p,r in g.changes.items()}
            mutable.update({p:r['sha256'] for p,r in g.supplement['inputs'].items()})
            for source in auth.context_binding.sources.values():
                p=str(auth.context_binding.repos[source['repository']]/source['path'])
                mutable[p]=g.current_hash(p,source['sha256'])
            result={'governance':g.__dict__,'mutable':mutable,'context':derived,
                    'dispatch':json.loads(store.resolve(pub['dispatch_ref'])),
                    'authorization':json.loads(store.resolve(auth.authorization_id))}
        elif sys.argv[2]=='readiness':
            policy=authenticated_policy(auth,store)
            result=readiness(auth,store,policy['released_supervisor'],True,_host)
        else:raise ValueError('unknown readonly operation')
        result['immutable_witness']=dict(witness)
print(canonical(result))
store.close()
