"""Prepare, verify and materialize only. No adoption, activation or ownership calls."""
from pathlib import Path
from dataclasses import replace
import collections
import json
import os
import sys

from adapter.context_projection import canonical, digest, sha, read_exact, derive
from adapter.governance_continuation import reference, GovernanceContinuation
from adapter.continuation_envelope import seal, SCHEMA, TYPES
from adapter.context_binding import CommittedContext
from adapter.governed_host import WorkAuthorization
from adapter.authorization_lifecycle import dispatch_binding, historical_original, reconstruct
from adapter.controller_authority_store import ControllerAuthorityStore, roots_for
from adapter.authority_bootstrap import capture_inputs, selection, reconstruct_authorization

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
BASE = ROOT/'docs/experiments/E1/pre_dispatch'
OLD = BASE/'complete_continuation_adoption_2026-09-16'


def load(p): return json.loads(Path(p).read_bytes())


def write(name, value):
    path = OUT/name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(canonical(value)); stream.flush(); os.fsync(stream.fileno())
    return reference(path)


def raw_authorization(raw, context, op):
    raw = dict(raw, context_binding=context, operational_binding=canonical(op))
    for key in ('read_roots','write_roots','deny_roots','exec_bins','read_deny_roots','write_deny_roots','write_directory_roots'):
        raw[key] = tuple(raw[key])
    raw['exec_argv_allowlist'] = tuple(tuple(x) for x in raw['exec_argv_allowlist'])
    return WorkAuthorization(**raw)


def main():
    old_op = load(OLD/'OPERATIONAL_BINDING.json')
    old_spec = old_op['governance']
    dispatch = reference(BASE/'dispatch_authorization_2026-09-16/DISPATCH_RECORD.json')
    decision = load(dispatch['path']); audit = Path(decision['all_authorized_bindings']['audit'])
    ledger = Path(decision['all_authorized_bindings']['ownership_ledger'])
    preserved = [audit, ledger, Path(dispatch['path']), OLD/'ADOPTION_RECORD.json',
                 OLD/'OPERATIONAL_BINDING.json', Path(old_spec['released_profile']['path'])]
    before = {str(p): sha(p.read_bytes()) for p in preserved}
    issued = next(json.loads(line)['authorization'] for line in audit.read_text().splitlines()
                  if json.loads(line).get('event') == 'authorization_issued')
    previous = load(OUT/'IMPLEMENTATION_BEFORE.json')
    candidate = {str(p): sha(p.read_bytes()) for p in (ROOT/'adapter').glob('*.py')}
    assert set(previous) <= set(candidate)
    artifacts = []
    blobs = OUT/'qualification/blobs'; blobs.mkdir(parents=True,exist_ok=True)
    inputs = {}
    for path, h in sorted(candidate.items()):
        old = previous.get(path)
        if old == h: continue
        old_blob = None
        if old is not None:
            old_data = read_exact(str(OUT/'before'/old), old)
            (blobs/old).write_bytes(old_data)
            old_blob = str(blobs/old)
            inputs[old_blob] = {'sha256': old}
        (blobs/h).write_bytes(read_exact(path,h))
        inputs[path] = {'sha256': h}
        artifacts.append({'path':path,'old_sha256':old,'new_sha256':h,
                          'old_blob':old_blob,'new_blob':str(blobs/h)})
    # Test evidence is captured, never used as an executable or a new release.
    for name in ('STORE_QUALIFICATION.log','REGRESSION.log','GOVERNANCE_RETEST.log','STRICT_REGRESSION.log'):
        data=(OUT/name).read_bytes();h=sha(data);(blobs/h).write_bytes(data)
        inputs[str(OUT/name)]={'sha256':h}
    assert (OUT/'STORE_QUALIFICATION.log').read_text().endswith('\nOK\n')
    assert (OUT/'GOVERNANCE_RETEST.log').read_text().endswith('\nOK\n')
    assert (OUT/'STRICT_REGRESSION.log').read_text().endswith('\nOK\n')
    classification = TYPES['NON_MATERIAL_IMPLEMENTATION_CONTINUATION']
    cap = write('qualification/MANIFEST.json', {'inputs':inputs,'result':'PASS',
        'classification':classification,
        'limits':'Non-live qualification. Synthetic host observations only; actual Bubblewrap namespace probe passed. No E1 activation.'})
    authority = write('ARCHITECT_PREPARATION_AUTHORITY.json', {
        'authority':'Architect', 'source':'Current user instruction: Controller Authority Store, sections 1–10',
        'authorized':'Implement and qualify private logical authority resolution; materialize existing authority; prepare OPERATIONAL-CONTINUATION-1.',
        'prohibited':['supervisor restart','E1 activation','real E1 ownership','E1 model request','E1 dispatch'],
        'adoption':'NOT APPLIED; preparation only'})
    evidence = write('QUALIFIED_FACTS.json', {'result':'PASS','classification':classification,
        'artifacts_sha256':digest(artifacts),'authority_invariants':old_spec['authority_invariants'],
        'capture':cap,'scope':'non-live implementation and authority-store qualification',
        'regression_disposition':'44 of 45 broad regression cases passed initially; corrected test exception scoping and all three governance tests passed on retest. Final private-store/lifecycle/ancestry suite and private-store suite passed independently.'})
    body = {'schema':SCHEMA,'type':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION',
        'sequence':len(old_spec['records'])+1,
        'predecessor_OperationalContextId':old_spec['identities']['OperationalContextId'],
        'predecessor_chain_digest':old_spec['identities']['continuation_chain_digest'],
        'artifacts':artifacts,'authority':authority,'classification':classification,
        'evidence':evidence,'authority_invariants':old_spec['authority_invariants'],
        'reason':'Private logical controller-authority resolution; existing released bytes, ancestry, grants, task, transmission and payload unchanged. Preparation only.'}
    approval = write('PREPARED_APPROVAL.json', {'authority':'Architect',
        'decision':'AUTHORIZE_NON_MATERIAL_CONTINUATION','body_sha256':digest(body),
        'evidence':evidence,'authority_source':authority,'status':'PREPARED_NOT_ADOPTED'})
    row = seal(body,approval)
    row_ref = write('PREPARED_CONTINUATION.json',row)
    spec = json.loads(canonical(old_spec)); spec['records'].append(row_ref);spec['approvals'].append(approval)
    spec['identities'].update({k:row[k] for k in ('OperationalContextId','continuation_chain_digest')})
    write('PREPARED_SPECIFICATION.json',spec)
    g = GovernanceContinuation(spec)
    context = CommittedContext(BASE/'CONTEXT_MANIFEST.json',issued['context_binding']['capture_commit'],spec)
    projected = derive(json.loads(issued['context_projection']),context)
    assert projected['ModelPayloadDigest'] == old_op['context_identities']['ModelPayloadDigest']
    assert projected['projection']['payload'] == g.anchor_projection['payload']
    op = dict(old_op,governance=spec,context_identities={k:projected[k] for k in old_op['context_identities']})
    write('PREPARED_OPERATIONAL_BINDING.json',op)
    auth = raw_authorization(issued,context,op)
    assert historical_original(auth) == issued
    inheritance = dispatch_binding(auth,audit,dispatch)
    records = capture_inputs(auth,audit,dispatch)
    aliases,applicability,provenance,private = selection(auth,audit,dispatch)
    private_base = Path('/tmp/kge-forge-controller-authority')
    for path in (private_base,private_base/auth.authorization_id):
        if not path.exists(): path.mkdir(mode=0o700)
        assert path.resolve()==path and path.stat().st_uid==os.getuid() and path.stat().st_mode&0o077==0
    private_base = private_base/auth.authorization_id
    suffix = '-'+OUT.name if len(sys.argv)>1 else ''
    store = ControllerAuthorityStore.materialize(private_base/('prepared'+suffix), records, aliases,
        provenance,applicability,roots_for(auth),private)
    try:
        with store.session():
            restored = reconstruct_authorization(store,auth.authorization_id)
            private_dispatch = dispatch_binding(restored,audit,dispatch)
            assert private_dispatch == inheritance
            state = reconstruct(audit.read_bytes(),restored,audit)
            assert state['state']=='INACTIVE' and not state['uncertain'] and ledger.read_bytes()==b''
            profile = store.resolve('sha256:'+old_spec['released_profile']['sha256'])
            assert profile==Path(old_spec['released_profile']['path']).read_bytes()
        descriptor = {'root':str(store.root),'catalog_sha256':store.catalog_sha256,
                      'applicability':store.applicability,'status':'PREPARED_NOT_SELECTED'}
        write('PREPARED_STORE.json',descriptor)
    finally:store.close()

    # Classify historical *references*, then select by logical content identity.
    # Some documentary copies share a digest with an already selected witness;
    # this does not turn that path into a production selector.
    inventory = load(BASE/'controller_placement_recheck_2026-09-17/RECHECK.json')['inventory']
    evidence_uses = {(e['path'],e['sha256']) for item in records.values() for e in item['evidence']}
    rows=[]
    for old in inventory:
        ref=old['historical_reference'];p=Path(ref['path']);key=(ref['path'],ref['sha256'])
        representation = None
        if p.parent == OLD and p.name in ('OPERATIONAL_BINDING.json','ADOPTED_SPECIFICATION.json'):
            category='MIXED'
            representation=old_spec['identities']['OperationalContextId']
            reason='The private operational-context representation preserves this binding/governance value; standalone repository file is not a runtime selector.'
        elif p.name in ('E1-WP-001.md','CONTEXT_PROTOCOL.md','DECISIONS.md'):
            category='MIXED'
            reason='Governing/task evidence has private exact-byte witnesses and live source-integrity observations. No authority is selected from live source bytes.'
        elif key not in evidence_uses and p.name in ('ADOPTION_VALIDATION.json','PROPOSED_PRODUCTION_PROFILE.json'):
            category='QUALIFICATION_EVIDENCE'
            reason='Historical validation/proposal evidence retained for reproducibility; no independent runtime authority selection.'
        elif key not in evidence_uses:
            category='DOCUMENTARY_ONLY'
            reason='Not read by the private controller dependency inventory; preserved for engineering traceability.'
        elif 'blobs' in p.parts:
            category='MIXED'
            reason='Historical qualification/release witness is consumed by unchanged exact-byte ancestry checks; only content identity is operational.'
        elif p.name in ('QUALIFIED_FACTS.json','MANIFEST.json','RECEIPT.json','MODEL_CONTEXT_PROJECTION.json'):
            category='MIXED'
            reason='Engineering evidence also supplies exact runtime verification facts; private content resolution required.'
        else:
            category='OPERATIONAL_AUTHORITY'
            reason='Exact release, dispatch, clearance, launch or continuation authority selected by the verifier.'
        rows.append({'evidence':ref,'classification':category,'reason':reason,
                     'runtime_identity':representation or (('sha256:'+ref['sha256']) if category in ('MIXED','OPERATIONAL_AUTHORITY') else None)})
    counts={k:sum(r['classification']==k for r in rows) for k in
            ('DOCUMENTARY_ONLY','QUALIFICATION_EVIDENCE','OPERATIONAL_AUTHORITY','MIXED')}
    write('REFERENCE_CLASSIFICATION.json',{'counts':counts,'total':len(rows),'references':rows,
        'qualification_evidence_note':'Qualification witnesses still consumed by exact ancestry checks are MIXED. Standalone historical validation/proposal records not selected by runtime are qualification-only. Mixed context/specification files are represented once by the existing OperationalContextId.'})

    # Materialize the exact currently adopted authority separately from the
    # prepared descendant. Do not select the descendant or replace adopted IDs.
    wanted={r['runtime_identity'] for r in rows if r['runtime_identity']}
    existing={k:v for k,v in records.items() if k in wanted or k.startswith(('git-sha1:','git-commit:'))}
    # Current manifest and controller-only source authority were outside the old
    # 716-reference inventory; retain these traced dependencies too.
    for k,v in records.items():
        if any(e['path']==str(context.path) or e['path'].endswith('/pd06_context_separation/ARCHITECT_AUTHORITY.md')
               for e in v['evidence']):existing[k]=v
    saved = dict(issued, operational_binding=canonical(old_op),
                 context_binding={'path':str(context.path),'capture_commit':context.capture_commit})
    existing[auth.authorization_id]={'bytes':canonical(saved).encode(),'evidence':[]}
    existing[old_spec['identities']['OperationalContextId']]={'bytes':canonical(old_op).encode(),
        'evidence':[reference(OLD/'OPERATIONAL_BINDING.json')]}
    old_app={'authorization_id':auth.authorization_id,**old_spec['identities']}
    old_provenance={**provenance,'release_identities':old_spec['identities']}
    released=ControllerAuthorityStore.materialize(private_base/('released'+suffix),existing,aliases,
        old_provenance,old_app,roots_for(auth),private)
    try:
        profile_location=released.location('sha256:'+old_spec['released_profile']['sha256'])
        released_descriptor={'root':str(released.root),'catalog_sha256':released.catalog_sha256,
            'applicability':old_app,'profile_location':str(profile_location),
            'profile_sha256':sha(profile_location.read_bytes()),'status':'MATERIALIZED_NOT_ACTIVATED',
            'logical_objects':len(released.catalog['objects']),
            'unique_content_objects':len({r['sha256'] for r in released.catalog['objects'].values()})}
        write('RELEASED_STORE.json',released_descriptor)
    finally:released.close()
    assert before=={str(p):sha(p.read_bytes()) for p in preserved}
    write('RESULT.json',{'result':'NON_LIVE_QUALIFIED_AND_PREPARED','classification_counts':counts,
        'prepared_continuation_id':row['continuation_id'],'classification':classification,
        'implementation_delta_count':len(artifacts),'adopted_identities_unchanged':old_spec['identities'],
        'prepared_identities':spec['identities'],'dispatch_inheritance':'PASS',
        'private_reconstruction':'INACTIVE, certain, existing ancestry authenticated',
        'profile_exact_bytes_verified':True,'ModelPayloadDigest':projected['ModelPayloadDigest'],
        'released_store':released_descriptor,'prepared_store':descriptor,
        'preserved_fingerprints':before,'E1':'INACTIVE','E1_WP_001':'INELIGIBLE_AND_UNDISPATCHED',
        'activation_event':None,'ownership_reservation':None,'E1_model_requests':0,'E1_implementation_effects':0,
        'supervisor_restarted':False,'production_activation_validation_run':False,
        'remaining':'Prepared continuation and bootstrap catalog selection require adoption before production use. Released supervisor PID 57950 remains a separate host prerequisite; no restart performed.'})
    print(canonical({'counts':counts,'prepared_continuation':row['continuation_id'],
                     'released_store':released_descriptor,'prepared_store':descriptor}))


if __name__=='__main__':main()
