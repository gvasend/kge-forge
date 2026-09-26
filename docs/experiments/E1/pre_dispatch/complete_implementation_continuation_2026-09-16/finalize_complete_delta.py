from pathlib import Path
import json,shutil
from adapter.context_projection import canonical,digest,sha,read_exact
from adapter.governance_continuation import reference
R=Path('/home/gvasend/app/kge-forge');O=R/'docs/experiments/E1/pre_dispatch/complete_implementation_continuation_2026-09-16'
def load(n):return json.loads((O/n).read_bytes())
e=load('IMPLEMENTATION_ENDPOINTS.json');i=load('PROPOSED_IDENTITIES.json');v=load('INDEPENDENT_VERIFICATION.json');live=load('synthetic_live/LIVE_REPORT.json');q=load('synthetic_live/ancestry/REPORT.json');wp=load('write_patch/REPORT.json')
assert v['result']==live['result']==q['result']==wp['result']=='PASS'
for script in ['build_complete_delta','construct_complete_continuation','verify_complete_candidate','finalize_complete_delta']:shutil.copy('/tmp/'+script+'.py',O/(script+'.py'))
reg={'result':'PASS','production_source_changed_for_assessment':False,'canonical_verification_and_ancestry':q['result'],'negative_ancestry_cases':q['denials'],'dispatch_inheritance':'Original and intermediate authenticated ancestors accepted by production dispatch binding; real synthetic activation used descendant context','payload_stable':q['payload_byte_identical'],'binding_digest_changed':q['identities_before']['ModelProjectionBindingDigest']!=q['identities_after']['ModelProjectionBindingDigest'],'production_event_order':live['event_order'],'synthetic_activation_event':live['activation_event']['event_id'],'synthetic_reservation':live['ownership_reservation']['reservation_id'],'independent_ACTIVE_recovery':live['independent_process_ACTIVE_recovery'],'competition':live['competition'],'sequential_denial':live['sequential_denial'],'result_before_QUIESCENT':live['while_scope_closed'],'execution_result':live['execution_result'],'kernel_after':live['kernel_after'],'terminal_recovery':live['terminal_recovery'],'model_request_filtering':reference(O/'REQUEST_IDENTITY_VERIFICATION.json'),'write_patch_fixture_variants':len(wp['cases']),'write_patch_observations':sum(len(x['observations']) for x in wp['cases']),'write_patch_report':reference(O/'write_patch/REPORT.json'),'API_calls':0,'E1_effects':0,'evidence_reuse':'Accepted lifecycle component tests and integrated failure boundaries reused by exact captured identities; current versioned ancestry + owned activation + execution regression freshly rerun. No unrelated PD-05/A2 reopening.'}
(O/'INTEGRATED_REGRESSION_RESULT.json').write_text(canonical(reg))
text=['# Complete implementation continuation assessment — 2026-09-16','',
'**Classification: NON_MATERIAL_IMPLEMENTATION_CONTINUATION. Integrated regression: PASS. Continuation: NOT APPLIED.**','',
'Production-verifier result: **PASS for the prospective candidate**, using an explicitly unissued proposed approval. This is not a finding that Architect adoption has already been authorized. The actual adopted operational head and dispatch authority remain unchanged. No production source was edited for this assessment.','',
'## Implementation endpoints','',
f"- Predecessor implementation: `{e['predecessor_implementation_identity']}` (26 modules).",
f"- Candidate implementation: `{e['candidate_implementation_identity']}` (29 modules).",
f"- Forge commit locator: `{e['Forge_HEAD']}`. The working tree contains prior changes; exact captured artifact identities, not HEAD alone, define these endpoints.",
f"- Last adopted OperationalContextId: `{e['predecessor_OperationalContextId']}`.",
f"- Last adopted chain digest: `{e['predecessor_chain_digest']}`.",
'- [Endpoint inventory](IMPLEMENTATION_ENDPOINTS.json), [repository/test inventory](REPOSITORY_INVENTORY.json), and [exact direct patch](COMPLETE_PRODUCTION_DELTA.patch).',
'- All 29 candidate production files exactly match accepted versioned-binding capture `3a2f03c53b158521948b60f7a336cec0c164ee2b13f65534ea8f59d3a5d0ac48`. [Bootstrap verification](BOOTSTRAP_TRUST.json) establishes the verifier implementation identity without modifying it.',
'', 'The ten-file direct delta includes the original lifecycle five, both integration dependencies, and all six binding changes (three overlap the preceding seven). None of the unadopted intermediate implementations is represented as an authoritative context.','',
'| Production file | Actually adopted SHA-256 | Complete candidate SHA-256 |','|---|---|---|']
for d in e['complete_delta']:text.append(f"| `{Path(d['path']).name}` | `{d['old_sha256'] or 'ABSENT'}` | `{d['new_sha256']}` |")
text+=['','## Six-file binding assessment','', 'Old hashes below refer to the actually adopted state. The JSON also records hashes from the unadopted integrated qualification solely as evidence lineage.','']
for a in load('SIX_FILE_BINDING_ASSESSMENT.json'):
 text += [f"### {Path(a['path']).name}",'']
 for label,key in [('Old hash','old_sha256'),('New hash','new_sha256'),('Responsibility','semantic_responsibility'),('Required by canonical protocol','reason_required'),('Affected invariants','affected_invariants'),('Before','externally_observable_before'),('After','externally_observable_after'),('Programmer-visible behavior','Programmer_visible_before_after'),('Authority effect','authority_effect'),('Effects','new_effecting_path'),('Changed enforcement path','enforcement_path_changed')]:text.append(f"- **{label}:** {a[key] if a[key] is not None else 'ABSENT'}")
 text+=['- **Qualification:** accepted integrated/versioned captures plus fresh `synthetic_live/LIVE_REPORT.json`, `synthetic_live/ancestry/REPORT.json`, request identity checks and write/patch boundary report.','']
text+=['## Combined invariant assessment','', '| Released invariant | Combined finding | Enforcement implementation changed |','|---|---|---|']
for a in load('COMBINED_INVARIANT_MATRIX.json'):text.append(f"| {a['invariant']} | {a['finding']} | {a['enforcement_implementation_changed']} |")
text+=['',load('COMPLETE_DELTA_ASSESSMENT.json')['composition_argument'],'',
'## Integrated regression','',
'Fresh synthetic committed-fixture qualification passed canonical governance/implementation ancestry, exact and inherited dispatch, stable payload/changing projection binding, production atomic validation, durable intent, exclusive reservation, ACTIVE reconstruction in another process, model-handoff gating, real supervised governed execution, result-before-QUIESCENT denial, sequential denial, competitor denial, terminal release and restart reconstruction. All four captured reasoning requests passed transmission filtering; zero API calls occurred.',
f"Fresh write/patch qualification passed {reg['write_patch_observations']} observations across {reg['write_patch_fixture_variants']} synthetic committed fixture variants, preserving complete before/after effects, protected-neighbor denial, leaf replacement and missing/wrong-type-parent behavior. These checks use the same current production code; unchanged method-body comparison ties them to the historical grant semantics.",
'[Integrated regression details](INTEGRATED_REGRESSION_RESULT.json), [request filtering proof](REQUEST_IDENTITY_VERIFICATION.json), [write/patch report](write_patch/REPORT.json), [unchanged effect-method/tool-registry AST](ENFORCEMENT_AST_COMPARISON.json).',
'', '## One proposed canonical continuation','',
'[Canonical complete continuation](CANONICAL_COMPLETE_CONTINUATION.json) contains all ten old/new artifact pairs, bound evidence and unchanged released authorities. [Qualified facts](QUALIFIED_FACTS.json) binds lifecycle, integrated activation, accepted versioned-binding and complete-delta regression evidence. [Proposed specification](PROPOSED_SPECIFICATION.json) contains one new link directly from the adopted anchor.','',
f"- Continuation identity: `{i['continuation_id']}`.",f"- Canonical file SHA-256: `{i['continuation']['sha256']}`."]
for k in ['OperationalContextId','continuation_chain_digest','FullContextDigest','ModelProjectionBindingDigest','ModelPayloadDigest']:text.append(f"- Proposed {k}: `{i['proposed'][k]}`.")
text += [f"- Unchanged released profile fingerprint: `{i['released_profile_fingerprint']}`.",f"- Unchanged E1-WP-001 content SHA-256: `{i['E1_WP_001_sha256']}`.",f"- Historical ModelProjectionDigest retained: `{i['proposed']['ModelProjectionDigest']}`.",'',
'The production verifier accepts the complete proposed artifact accounting and current bytes. Independent fresh-process reconstruction reproduces all proposed context identities and the exact released model payload. [Verifier result](PRODUCTION_VERIFIER_RESULT.json); [independent verification](INDEPENDENT_VERIFICATION.json).',
'', '**Approval boundary:** `PROPOSED_APPROVAL.json` is draft text, not an issued Architect decision. It is supplied only in the unadopted candidate specification for prospective verifier assessment. No authoritative selector references it. Proposed identifiers bind its exact bytes; different final approval bytes would require explicit recalculation and review. No actual approval was inferred from the verifier accepting supplied draft inputs.',
'', '## Preserved state','',
'PD-06 RELEASED; E1-B01 PASS; E1 INACTIVE; E1-WP-001 INELIGIBLE and UNDISPATCHED. The historical authorization audit and immutable dispatch hash match; the real ownership ledger remains empty and no E1 controller fence exists. No continuation was applied, no E1 activation event created, no real E1 ownership acquired, no E1 model request sent, and no E1 implementation effect occurred.']
(O/'FINAL_REPORT.md').write_text('\n'.join(text)+'\n')
# Final immutable review package captures candidate/verification in addition to the prior qualification archive.
paths=[p for p in O.rglob('*') if p.is_file() and 'captures' not in p.relative_to(O).parts and p.name!='FINAL_CAPTURE.json']
inputs={str(p):{'sha256':sha(p.read_bytes())} for p in paths};manifest={'schema':'COMPLETE-CONTINUATION-REVIEW-1','classification':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION','result':'PASS','qualification_capture':load('QUALIFICATION_CAPTURE.json'),'continuation_applied':False,'inputs':inputs}
h=digest(manifest);c=O/'captures'/h;c.mkdir();(c/'blobs').mkdir()
for p,r in inputs.items():
 dest=c/'blobs'/r['sha256']
 if not dest.exists():dest.write_bytes(read_exact(p,r['sha256']))
(c/'MANIFEST.json').write_text(canonical(manifest));(O/'FINAL_CAPTURE.json').write_text(canonical(reference(c/'MANIFEST.json')))
print(canonical({'report':str(O/'FINAL_REPORT.md'),'final_capture_sha256':h,'classification':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION','continuation_applied':False}))
