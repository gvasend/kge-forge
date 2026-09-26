"""Read-only exact qualification and private ancestry verification; no live calls."""
from pathlib import Path
import json
import sys
from adapter.context_projection import canonical, digest, sha
from adapter.continuation_envelope import BODY_KEYS, seal
from adapter.controller_authority_store import ControllerAuthorityStore, read_authority_ref, _directory, _read, outside
import os
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.authorization_lifecycle import dispatch_binding, reconstruct

BASE = Path(__file__).resolve().parent.parent
Q = BASE/'controller_authority_store_2026-09-17/qualified'
OUT = Path(__file__).resolve().parent
ROOT = BASE.parents[3]

def load(p): return json.loads(Path(p).read_bytes())
def ref(p): return {'path':str(p), 'sha256':sha(Path(p).read_bytes())}
def exact(r):
    b = Path(r['path']).read_bytes()
    assert sha(b) == r['sha256'], r['path']
    return b

def verify(pin=None, pin_sha256=None):
    closure = load(Q/'CLOSURE.json')
    for r in closure['evidence']: exact(r)
    result = load(Q/'RESULT.json')
    for p,h in result['preserved_fingerprints'].items(): exact({'path':p,'sha256':h})
    inventory = load(Q/'REFERENCE_CLASSIFICATION.json')
    assert inventory['total']==len(inventory['references'])==716
    for r in inventory['references']: exact(r['evidence'])
    row = load(Q/'PREPARED_CONTINUATION.json')
    body = {k:row[k] for k in BODY_KEYS}
    assert row==seal(body,row['approval'])
    assert row['continuation_id']==closure['prepared_continuation_id']==result['prepared_continuation_id']
    for r in (row['approval'],row['authority'],row['evidence']): exact(r)
    facts = json.loads(exact(row['evidence']))
    assert facts['result']=='PASS' and facts['artifacts_sha256']==digest(row['artifacts'])
    capture = json.loads(exact(facts['capture']))
    for p,r in capture['inputs'].items():
        exact({'path':p,**r})
        exact({'path':str(Path(facts['capture']['path']).parent/'blobs'/r['sha256']),**r})
    before = load(Q/'IMPLEMENTATION_BEFORE.json')
    expected = dict(before)
    for a in row['artifacts']:
        assert before.get(a['path'])==a['old_sha256']
        expected[a['path']]=a['new_sha256']
        for h,p in ((a['old_sha256'],a['old_blob']),(a['new_sha256'],a['new_blob'])):
            if h is not None: exact({'path':p,'sha256':h})
    actual = {str(p):sha(p.read_bytes()) for p in (ROOT/'adapter').glob('*.py')}
    assert actual==expected, 'unaccounted production implementation change'
    old = load(BASE/'complete_continuation_adoption_2026-09-16/OPERATIONAL_BINDING.json')
    assert row['predecessor_OperationalContextId']==old['governance']['identities']['OperationalContextId']
    assert row['predecessor_chain_digest']==old['governance']['identities']['continuation_chain_digest']
    prepared_op = load(Q/'PREPARED_OPERATIONAL_BINDING.json')
    assert prepared_op['governance']==load(Q/'PREPARED_SPECIFICATION.json')
    assert prepared_op['governance']['records'][:-1]==old['governance']['records']
    assert prepared_op['governance']['approvals'][:-1]==old['governance']['approvals']
    assert prepared_op['governance']['authority_invariants']==old['governance']['authority_invariants']
    summaries = {}
    for name in ('RELEASED_STORE','PREPARED_STORE'):
        desc = load(Q/(name+'.json'))
        store = ControllerAuthorityStore(desc['root'],desc['catalog_sha256'],desc['applicability'])
        try:
            for identity in store.catalog['objects']: store.resolve(identity)
            summaries[name] = {'root':desc['root'],'catalog_sha256':desc['catalog_sha256'],
                'logical_entries':len(store.catalog['objects']),
                'distinct_content_objects':len({r['sha256'] for r in store.catalog['objects'].values()}),
                'all_private_hashes':'PASS','provenance_and_placement':'PASS'}
        finally: store.close()
        print(name+' all logical entries and object hashes PASS',flush=True)
    assert summaries['RELEASED_STORE']['logical_entries']==477
    assert summaries['RELEASED_STORE']['distinct_content_objects']==473
    desc = load(Q/'PREPARED_STORE.json')
    if pin is not None:
        fd=_directory(pin.parent)
        try: pin_bytes=_read(fd,pin.name)
        finally: os.close(fd)
        assert sha(pin_bytes)==pin_sha256, 'adoption bootstrap pin mismatch'
        adopted = json.loads(pin_bytes)
        assert adopted['event']=='operational_continuation_adopted'
        assert adopted['canonical_mechanism']=='OPERATIONAL-CONTINUATION-1'
        assert adopted['continuation_id']==row['continuation_id']
        assert adopted['continuation_sha256']==sha((Q/'PREPARED_CONTINUATION.json').read_bytes())
        assert adopted['qualified_closure_sha256']==sha((Q/'CLOSURE.json').read_bytes())
        assert adopted['selected_store']=={k:desc[k] for k in ('root','catalog_sha256','applicability')}
        assert adopted['architect_adoption']['decision']=='ADOPT_EXACT_QUALIFIED_CONTINUATION'
        assert adopted['architect_adoption']['continuation_id']==row['continuation_id']
        assert adopted['architect_adoption']['continuation_sha256']==adopted['continuation_sha256']
        desc=adopted['selected_store']
    store = ControllerAuthorityStore(desc['root'],desc['catalog_sha256'],desc['applicability'])
    try:
        if pin is not None: outside(pin,store.catalog['programmer_roots'])
        with store.session():
            auth = reconstruct_authorization(store,desc['applicability']['authorization_id'])
            op = json.loads(auth.operational_binding)
            assert op==prepared_op
            g = auth.context_binding.governance
            assert g.ancestor_ops[-2]==old
            assert g.ancestry[-1]=={k:row[k] for k in ('OperationalContextId','continuation_chain_digest')}
            print('Private bootstrap and complete operational ancestry PASS',flush=True)
            dispatch_ids=[i for i in store.catalog['objects'] if i.startswith('E1-ARCHITECT-DISPATCH-sha256:')]
            assert len(dispatch_ids)==1
            dispatch_id=dispatch_ids[0]
            audit = store.state_path(auth.authorization_id+':audit')
            ledger = store.state_path(auth.authorization_id+':ownership')
            initial = {str(p):sha(p.read_bytes()) for p in (audit,ledger)}
            binding=dispatch_binding(auth,audit,{'authority_id':dispatch_id,'sha256':dispatch_id.split(':')[-1]})
            state = reconstruct(audit.read_bytes(),auth,audit)
            assert state['state']=='INACTIVE' and not state['uncertain'] and ledger.read_bytes()==b''
            assert auth.work_package_id=='E1-WP-001' and auth.state=='INACTIVE'
            profile_bytes=read_authority_ref(op['governance']['released_profile'])
            assert sha(profile_bytes)==result['released_store']['profile_sha256']
            assert digest(json.loads(profile_bytes))==row['authority_invariants']['released_profile_sha256']
            assert op['context_identities']['ModelPayloadDigest']==result['ModelPayloadDigest']
            release=json.loads(read_authority_ref(op['governance']['release_decision']))
            assert release['decision']=={'PD06':'RELEASED','E1_B01':'PASS'}
            assert initial=={str(p):sha(p.read_bytes()) for p in (audit,ledger)}
            output={'result':'PASS','adopted':pin is not None,'canonical_mechanism':'OPERATIONAL-CONTINUATION-1',
                'continuation_id':row['continuation_id'],'continuation_sha256':sha((Q/'PREPARED_CONTINUATION.json').read_bytes()),
                'qualified_closure':ref(Q/'CLOSURE.json'),'predecessor':old['governance']['identities'],
                'identities':{**op['governance']['identities'],**op['context_identities']},
                'stores':summaries,'implementation_files_verified':len(actual),'qualified_delta_files':len(row['artifacts']),
                'historical_reference_fingerprints_unchanged':716,'dispatch_inheritance':'PASS',
                'dispatch_id':dispatch_id,'authorization_id':auth.authorization_id,
                'released_profile_bytes_sha256':sha(profile_bytes),'released_profile_canonical_fingerprint':digest(json.loads(profile_bytes)),
                'profile_location':str(store.location('sha256:'+sha(profile_bytes))),
                'operational_ancestry':g.ancestry,'state':state['state'],'uncertain':state['uncertain'],
                'ownership':'NO OWNERSHIP','model_handoff_eligible':False,'activation_event':None,'ownership_reservation':None,
                'E1_model_requests':0,'E1_implementation_effects':0,'supervisor_intervention':False,
                'preserved_mutable_fingerprints':initial,'dispatch_binding':binding}
    finally: store.close()
    for p,h in result['preserved_fingerprints'].items(): exact({'path':p,'sha256':h})
    for r in inventory['references']: exact(r['evidence'])
    return output

if __name__=='__main__':
    pin=Path(sys.argv[1]) if len(sys.argv)>1 else None
    value=verify(pin,sys.argv[2] if pin else None)
    path=OUT/('INDEPENDENT_RECONSTRUCTION.json' if pin else 'ADOPTION_VALIDATION.json')
    with path.open('x') as f: f.write(canonical(value)+'\n')
    print(canonical(value),flush=True)
