exec(compile(Path('/tmp/build_complete_delta.py').read_text(),'/tmp/build_complete_delta.py','exec')) if False else None
from pathlib import Path
import json,shutil,subprocess
from adapter.context_projection import canonical,digest,sha,read_exact,derive,projection_binding
from adapter.continuation_envelope import archive,invariants,seal,historical_operation,SCHEMA
from adapter.governance_continuation import reference,GovernanceContinuation
from adapter.context_binding import CommittedContext
R=Path('/home/gvasend/app/kge-forge');B=R/'docs/experiments/E1/pre_dispatch';O=B/'complete_implementation_continuation_2026-09-16';P=B/'governance_continuation_2026-09-16/production_final'
def load(p):return json.loads(Path(p).read_bytes())
def write(n,v):
 p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(canonical(v));return reference(p)
ends=load(O/'IMPLEMENTATION_ENDPOINTS.json');op=load(P/'OPERATIONAL_BINDING.json');g=op['governance'];full=load(P/'AUTHORITATIVE_OPERATIONAL_CONTEXT.json');proj=load(P/'MODEL_CONTEXT_PROJECTION.json');protected=invariants(op,proj)
authority=O/'ARCHITECT_AUTHORITY_AND_PROPOSAL_STATUS.md'
authority.write_text('''# Architect authority and proposal status

The Architect accepts Versioned Operational Binding qualification as PASS and OPERATIONAL-CONTINUATION-1 as canonical. The current instruction requires accounting for the complete production delta from the last actually adopted implementation, combined applicability assessment, and, only if NON_MATERIAL_IMPLEMENTATION_CONTINUATION, construction of one canonical proposed continuation and production-verifier validation.

The earlier integrated activation qualification and its NON_MATERIAL classification were accepted against capture 627fc40163edea51492f1711d645b11ac72ceb6d5fa2c2ed9fc5438356a67f6f. That acceptance did not adopt the subsequently expanded implementation delta. The current instruction explicitly says the reconstructed E1 continuation is NOT YET authorized for adoption and requires: Do not apply the continuation; do not create the E1 activation event; do not acquire E1 ownership; do not activate E1; do not make an E1 model request; do not dispatch E1-WP-001.

The complete-delta classification in this package is the requested applicability assessment, submitted to the Architect. PROPOSED_APPROVAL.json is an unissued draft approval encoding used solely for prospective validation by the unchanged production verifier. Its decision field is proposed text, not an Architect decision already made. Neither the specification nor the draft approval is installed in the authoritative operational context. Actual adoption remains unauthorized. If the Architect adopts different exact approval bytes, dependent proposal identities must be recomputed and explicitly reviewed; historical authorities cannot be replaced.
''')
# Build a content-addressed qualification capture, including both sides of every delta.
paths=[p for p in O.rglob('*') if p.is_file() and 'captures' not in p.parts]
paths += [Path(p) for p in ends['candidate_files']]
paths += list((R/'adapter/tests').glob('*.py'))
for d in ends['complete_delta']:
 if d['old_sha256']:paths.append(Path(ends['adopted_capture']['path']).parent/'blobs'/d['old_sha256'])
refs=load(O/'COMPLETE_DELTA_ASSESSMENT.json')['qualification_evidence']
paths += [Path(r['path']) for r in refs]+[Path(ends['adopted_capture']['path'])]
# Include all synthetic durable files at original paths as well as review copies.
paths += [p for p in Path('/tmp/kge-complete-delta-live-20260916').rglob('*') if p.is_file() and not p.is_symlink()]
paths += [Path('/tmp/build_complete_delta.py'),Path('/tmp/construct_complete_continuation.py')]
inputs={str(p.resolve()):{'sha256':sha(p.read_bytes())} for p in sorted(set(paths))}
manifest={'schema':'COMPLETE-IMPLEMENTATION-QUALIFICATION-1','result':'PASS','classification':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION','predecessor_implementation_identity':ends['predecessor_implementation_identity'],'candidate_implementation_identity':ends['candidate_implementation_identity'],'inputs':inputs,'accepted_prior_qualification':refs}
h=digest(manifest);cd=O/'captures'/h;cd.mkdir(parents=True);(cd/'blobs').mkdir()
for p,r in inputs.items():
 data=read_exact(p,r['sha256']);blob=cd/'blobs'/r['sha256']
 if not blob.exists():blob.write_bytes(data)
(cd/'MANIFEST.json').write_text(canonical(manifest));cap=reference(cd/'MANIFEST.json');assert cap['sha256']==h;archive(cap);write('QUALIFICATION_CAPTURE.json',cap)
artifacts=[]
for d in ends['complete_delta']:
 artifacts.append({**d,'old_blob':str(cd/'blobs'/d['old_sha256']) if d['old_sha256'] else None,'new_blob':str(cd/'blobs'/d['new_sha256'])})
evidence=write('QUALIFIED_FACTS.json',{'result':'PASS','classification':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION','artifacts_sha256':digest(artifacts),'authority_invariants':protected,'capture':cap,'prior_qualification':refs,'scope':'All ten production changes directly from last adopted implementation; no intermediate adopted context','assessment':reference(O/'COMPLETE_DELTA_ASSESSMENT.json'),'adoption_authorized':False})
body={'schema':SCHEMA,'type':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION','sequence':1,'predecessor_OperationalContextId':g['identities']['OperationalContextId'],'predecessor_chain_digest':g['identities']['continuation_chain_digest'],'artifacts':artifacts,'authority':reference(authority),'classification':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION','evidence':evidence,'authority_invariants':protected,'reason':'Proposed direct complete implementation continuation from the last adopted operational state; lifecycle, integration and versioned-binding composition qualified. NOT APPLIED; draft approval is not issued Architect authority.'}
approval=write('PROPOSED_APPROVAL.json',{'authority':'Architect','decision':'AUTHORIZE_NON_MATERIAL_CONTINUATION','body_sha256':digest(body),'evidence':evidence,'authority_source':body['authority'],'status':'PROPOSED_NOT_ISSUED','adoption_authorized':False})
row=seal(body,approval);ref=write('CANONICAL_COMPLETE_CONTINUATION.json',row)
spec={'schema':2,'anchor':{'operational_binding':reference(P/'OPERATIONAL_BINDING.json'),'full_context':reference(P/'AUTHORITATIVE_OPERATIONAL_CONTEXT.json'),'projection':reference(P/'MODEL_CONTEXT_PROJECTION.json'),'evidence_capture':ends['adopted_capture']},**{k:g[k] for k in ['release_basis','release_decision','released_profile','clearance']},'authority_invariants':protected,'records':[ref],'approvals':[approval],'identities':{**g['identities'],**{k:row[k] for k in ['OperationalContextId','continuation_chain_digest']}}}
write('PROPOSED_SPECIFICATION.json',spec)
verified=GovernanceContinuation(spec)
proposed=historical_operation(op,full,proj,spec,verified.supplement)
launch=load(op['released_launch']['path']);ctx=CommittedContext(B/'CONTEXT_MANIFEST.json',launch['authorization']['context_binding']['capture_commit'],spec)
projection=derive(json.loads(launch['authorization']['context_projection']),ctx)
assert projection['projection']['payload']==proj['payload']
assert all(projection[k]==v for k,v in proposed['context_identities'].items())
write('PROPOSED_OPERATIONAL_BINDING.json',proposed)
write('PROPOSED_IDENTITIES.json',{'continuation':ref,'continuation_id':row['continuation_id'],'predecessor':g['identities'],'proposed':{**spec['identities'],**proposed['context_identities']},'released_profile_fingerprint':protected['released_profile_sha256'],'E1_WP_001_sha256':protected['task_sha256'],'ModelPayloadDigest_unchanged':protected['ModelPayloadDigest'],'previous_ModelProjectionBindingDigest':projection_binding(protected['ModelPayloadDigest'],protected['clearance'],g['identities'],protected['released_profile_sha256'],{'path':protected['task_path'],'sha256':protected['task_sha256']},op['context_identities']['FullContextDigest']),'approval_status':'PROPOSED_NOT_ISSUED','continuation_applied':False})
write('PRODUCTION_VERIFIER_RESULT.json',{'result':'PASS_PROSPECTIVE_CANDIDATE','verifier':'adapter.continuation_envelope.verify via GovernanceContinuation','bootstrap':reference(O/'BOOTSTRAP_TRUST.json'),'accepted_artifacts':len(artifacts),'accepted_current_implementation_modules':len(verified.supplement['inputs']),'actual_context_and_cleared_payload_reconstructed':True,'payload_identical':True,'approval_selected_only_in_unadopted_candidate':True,'adoption_authorized':False,'limitation':'This verifies the complete candidate with the explicitly unissued proposed approval encoding. It does not establish actual Architect approval or select an operational head.'})
print(canonical(load(O/'PROPOSED_IDENTITIES.json')))
