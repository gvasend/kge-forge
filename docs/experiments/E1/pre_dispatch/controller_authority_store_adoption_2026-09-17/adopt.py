"""Adopt an exactly qualified, sealed continuation by exclusive private pin.

No resealing, authority-record rewrite, production implementation edit, activation,
ownership operation, supervisor operation or model call. The qualified bootstrap
accepts an external store pin; this records the Architect-authorized selection.
"""
from pathlib import Path
import json
import os
from adapter.context_projection import canonical, sha
from adapter.controller_authority_store import ControllerAuthorityStore, outside, _directory, _put
from verify_adoption import Q, OUT, exact, load

proof=load(OUT/'ADOPTION_VALIDATION.json')
assert proof['result']=='PASS' and proof['adopted'] is False
exact(proof['qualified_closure'])
row=load(Q/'PREPARED_CONTINUATION.json')
assert row['continuation_id']==proof['continuation_id']
assert sha((Q/'PREPARED_CONTINUATION.json').read_bytes())==proof['continuation_sha256']
for p,h in proof['preserved_mutable_fingerprints'].items(): exact({'path':p,'sha256':h})
for item in load(Q/'REFERENCE_CLASSIFICATION.json')['references']: exact(item['evidence'])
for p,h in load(Q/'RESULT.json')['preserved_fingerprints'].items(): exact({'path':p,'sha256':h})
expected=load(Q/'IMPLEMENTATION_BEFORE.json')
expected.update({a['path']:a['new_sha256'] for a in row['artifacts']})
root=Q.parents[5]
assert {str(p):sha(p.read_bytes()) for p in (root/'adapter').glob('*.py')}==expected
desc=load(Q/'PREPARED_STORE.json')
selection={k:desc[k] for k in ('root','catalog_sha256','applicability')}
assert selection['catalog_sha256']==proof['stores']['PREPARED_STORE']['catalog_sha256']
store=ControllerAuthorityStore(**{'root':selection['root'],'catalog_sha256':selection['catalog_sha256'],
                                 'applicability':selection['applicability']})
private=store.root.parent/'adoption-2026-09-17'
try:
    outside(private,store.catalog['programmer_roots'])
    for identity in store.catalog['objects']: store.resolve(identity)
    authority={'authority':'Architect','source':'User ARCHITECT ADOPTION AUTHORIZATION, current conversation, 2026-09-17',
        'decision':'ADOPT_EXACT_QUALIFIED_CONTINUATION',
        'authorization_quote':'The Architect accepts the Controller Authority Store qualification as PASS and the prepared implementation continuation as NON_MATERIAL_IMPLEMENTATION_CONTINUATION. Authorize adoption of the exact qualified continuation prepared by docs/experiments/E1/pre_dispatch/controller_authority_store_2026-09-17/ subject to exact verification against its qualified closure evidence and fingerprints.',
        'continuation_id':row['continuation_id'],'continuation_sha256':proof['continuation_sha256'],
        'qualified_closure_sha256':proof['qualified_closure']['sha256'],
        'preserve':'Existing release, dispatch, authorization, profile, task, payload, and all historical evidence fingerprints.',
        'stop':'INACTIVE and NO OWNERSHIP; analyze supervisor binding; stop before host intervention.',
        'prohibited':['E1 activation','E1 ownership acquisition','E1 model request','E1 dispatch','supervisor restart or substitution']}
    record={'event':'operational_continuation_adopted','canonical_mechanism':'OPERATIONAL-CONTINUATION-1',
        'classification':row['classification'],'continuation_id':row['continuation_id'],
        'continuation_sha256':proof['continuation_sha256'],
        'qualified_closure_sha256':proof['qualified_closure']['sha256'],
        'architect_adoption':authority,'predecessor':proof['predecessor'],
        'identities':proof['identities'],'selected_store':selection,
        'qualification_verification':proof,
        'selection_semantics':'This durable private record adopts the exact sealed prepared continuation and selects its qualified bootstrap pin. Prepared record status/reason remain historical preparation evidence; the separate Architect adoption is effective selection authority. No envelope, approval, context or catalog bytes are rewritten.',
        'activation_performed':False,'ownership_created':False,'supervisor_intervention':False,
        'E1_model_requests':0,'E1_implementation_effects':0}
    data=canonical(record).encode()
    private.mkdir(mode=0o700)
    fd=_directory(private)
    try:
        # Exclusive durable creation is the adoption commit point. No mutable
        # repository selector and no generic mutation of lifecycle records.
        _put(fd,'ADOPTION_RECORD.json',data)
        os.fsync(fd)
    finally: os.close(fd)
    fd=_directory(private.parent)
    try: os.fsync(fd)
    finally: os.close(fd)
finally: store.close()
with (OUT/'ADOPTION_RECORD.json').open('xb') as f:
    f.write(data);f.flush();os.fsync(f.fileno())
pin={'path':str(private/'ADOPTION_RECORD.json'),'sha256':sha(data),
     'role':'Documentary copy of externally selected controller bootstrap pin; repository file is not operational authority.'}
with (OUT/'PRIVATE_BOOTSTRAP_PIN.json').open('x') as f: f.write(canonical(pin)+'\n')
print(canonical(pin),flush=True)
