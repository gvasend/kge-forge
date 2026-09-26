"""Independent read-only reconstruction of an explicitly supplied prepared pin.

The descriptor is a review input, not an adopted production bootstrap selector.
This command cannot activate, reserve ownership, restart a host, or call a model.
"""
from pathlib import Path
import json
import sys
from adapter.controller_authority_store import ControllerAuthorityStore, read_authority_ref
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.authorization_lifecycle import dispatch_binding, reconstruct
from adapter.context_projection import canonical, sha, digest

out = Path(sys.argv[1]).resolve()
desc = json.loads((out/'PREPARED_STORE.json').read_bytes())
result = json.loads((out/'RESULT.json').read_bytes())
store = ControllerAuthorityStore(desc['root'],desc['catalog_sha256'],desc['applicability'])
try:
    with store.session():
        auth = reconstruct_authorization(store,desc['applicability']['authorization_id'])
        op = json.loads(auth.operational_binding)
        aid = next(identity for identity in store.catalog['objects']
                   if identity.startswith('E1-ARCHITECT-DISPATCH-sha256:'))
        ref = {'authority_id':aid,'sha256':aid.split(':')[-1]}
        audit = store.state_path(auth.authorization_id+':audit')
        ledger = store.state_path(auth.authorization_id+':ownership')
        before = {str(p):sha(p.read_bytes()) for p in (audit,ledger)}
        inherited = dispatch_binding(auth,audit,ref)
        state = reconstruct(audit.read_bytes(),auth,audit)
        assert state['state']=='INACTIVE' and not state['uncertain'] and ledger.read_bytes()==b''
        profile = read_authority_ref(op['governance']['released_profile'])
        assert sha(profile)==result['released_store']['profile_sha256']
        assert before=={str(p):sha(p.read_bytes()) for p in (audit,ledger)}
        facts = {'result':'PASS','private_bootstrap':'PASS','dispatch_ancestry':'PASS',
            'prepared_OperationalContextId':op['governance']['identities']['OperationalContextId'],
            'released_profile_content_sha256':sha(profile),'released_canonical_profile_fingerprint':digest(json.loads(profile)),
            'state':state['state'],'uncertain':state['uncertain'],'ownership_bytes':ledger.stat().st_size,
            'adopted':False,'activation_validation_run':False,'model_handoff_eligible':False,
            'E1_model_requests':0,'E1_implementation_effects':0,'preserved_mutable_fingerprints':before}
finally:store.close()
(out/'INDEPENDENT_RECONSTRUCTION.json').write_text(canonical(facts)+'\n')
print(canonical(facts))
