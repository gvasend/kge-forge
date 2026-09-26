"""Report exact qualified prospective identities; never apply or issue."""
import json,hashlib,os
from pathlib import Path
O=Path(__file__).parent
load=lambda n:json.loads((O/n).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
pub=load('QUALIFIED_PUBLICATION.json');p=load('PROPOSED_R12_BINDING.json');q=load('SEMANTIC_QUALIFICATION.json');pre=load('PREFLIGHT.json');recovery=load('INDEPENDENT_RECONSTRUCTION.json');negative=load('NEGATIVE_CONTEXT.json');capture=load('R11_AUTHENTICATED_CAPTURE.json');status=load('FRESH_PREDECESSOR_STATUS.json')
assert recovery['result']=='PASS_QUALIFIED_PREPARED' and not recovery['hard_exceeded'] and not recovery['handoff_eligible']
assert not os.path.lexists(Path(pub['audit']).parents[2])
base=load('PRESERVATION_BASELINE.json');assert all(sha(Path(path).read_bytes())==h for path,h in base.items())
phases={r['operation']:r['seconds'] for r in pre['diagnostics'] if 'preissuance_production' in r['operation'] or r['operation'] in ('cold_private_bootstrap','operational_context_reconstruction','model_projection_validation')}
assert all(v<30 for k,v in phases.items() if k.startswith('warm_')) and not any(r['hard_exceeded'] for r in pre['diagnostics'])
old=json.loads(Path(capture['publication']['path']).read_bytes())
result={'verdict':'RUN2_R12_READY_FOR_ARCHITECT_ISSUANCE','scope':'QUALIFIED_PREPARED; material adoption and exact Architect issuance authorization still required',
 'r11':'CANCELLED / INTERRUPTED_NO_EFFECTS','r11_safe_predecessor':'ACTIVE_CANCELLED_PRE_MODEL_NO_EFFECTS','r11_audit_sha256':capture['terminal']['audit_sha256'],
 'classification':'MATERIAL_SAFE_PREDECESSOR_POLICY_EVOLUTION','registry_id':q['registry_id'],
 'registry_file_sha256':sha((O/'EVIDENCE_SEMANTICS_REGISTRY.json').read_bytes()),
 'focused_semantic_checks':len(q['checks']),'production_negative_probes':len(negative['probes']),
 'applied_release_authority_unchanged':old['release_authority'],'applied_operational_identities_unchanged':old['operational_identities'],
 'proposed_amendment':pub['amendment_id'],'proposed_amendment_sha256':pub['amendment']['sha256'],
 'proposed_release_authority':pub['release_authority'],'proposed_operational_identities':pub['operational_identities'],'proposed_context_identities':pub['context_identities'],
 'preserved_continuation':pub['continuation_id'],'preserved_continuation_sha256':pub['continuation']['sha256'],'new_nonmaterial_continuation':None,
 'implementation_identity':pub['controller_runtime_identity'],'r12_authorization_id':pub['authorization_id'],'r12_binding_sha256':pub['proposal']['sha256'],
 'InvocationAttemptId':p['InvocationAttemptId'],'predecessors':p['predecessors'],'audit':pub['audit'],'audit_namespace':'ABSENT_UNUSED',
 'supervisor':recovery['host'],'production_seconds':phases,'independent_reconstruction_seconds':recovery['seconds'],
 'budget_policy':'UNCHANGED','status_projection':{'freshness':status['freshness'],'lifecycle':status['lifecycle_state'],'ownership':status['ownership'],'quiescence':status['architectural_state'],'seconds':status['projection_seconds']},
 'amendment_applied':False,'issuance':False,'activation':False,'ownership':'NONE','ExecutionScope':'NONE','real_r12_model_requests':0,'r12_ActionRequests':0,'r12_effects':0,
 'qualification_publication_sha256':sha((O/'QUALIFIED_PUBLICATION.json').read_bytes())}
(O/'FINAL_RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
lines=['# r12 semantic evidence qualification','', '**RUN2_R12_READY_FOR_ARCHITECT_ISSUANCE** — prospective qualification only. The material amendment is prepared, not applied. A separate exact Architect adoption/issuance authorization remains necessary.','',
 'r11 remains immutable CANCELLED / INTERRUPTED_NO_EFFECTS. Its original runtime independently reconstructed terminal cancellation, admission closure, released ownership, no ExecutionScope, QUIESCENT, zero model/provider handoff, zero actions/effects and no unresolved uncertainty. The original audit SHA-256 is `'+result['r11_audit_sha256']+'`.','',
 '| Observed r11 record | Qualified class | Interpretation |','|---|---|---|',
 '| budget_exhausted | NON_EFFECTING_OBSERVATION | Reports resource-policy exhaustion; may restrict admission and trigger governed cancellation, never grants authority or establishes a known effect outcome. |',
 '| span: attempt_history_ancestry | NON_EFFECTING_OBSERVATION | Timing around authenticated ancestry verification. |',
 '| span: attempt_history_decision | NON_EFFECTING_OBSERVATION | Timing around private decision verification. |',
 '| span: attempt_history_historical_capture | NON_EFFECTING_OBSERVATION | Timing around verification of pinned historical bytes and witnesses. |',
 '| activity: attempt_history_ancestry | NON_EFFECTING_OBSERVATION | Controller verification activity. |',
 '| activity: model_projection | NON_EFFECTING_OBSERVATION | Local projection processing; no model/provider handoff. |',
 '| context_projection_verified (additional observed class) | NON_EFFECTING_OBSERVATION | Exact local verification receipt; every projection identity must match the issued operational binding. |','',
 'The trusted versioned registry maps historical producer/schema semantics to categories. Classification is not read from caller labels. Exact field shapes, invocation/session/cycle, policy and projection identities are checked. Immutable audit bytes and original producer implementations remain authenticated. The policy removes only qualified observations from an in-memory eligibility view; authoritative lifecycle, ownership, scope, admission, terminal and uncertainty checks still decide eligibility. No historical row is rewritten.','',
 'Unknown records/operations, malformed envelopes, injected labels, model/provider handoff, action/effect records and unresolved uncertainty fail closed. Admission closure remains restrictive, never authorizing. The old r9 provisional uncertainty remains historical and is resolved only by its already-qualified authoritative recovery; older attempt decisions retain their authenticated policy version. No telemetry declaration resolves uncertainty.','',
 'Applicability is MATERIAL: the frozen policy used name-based sufficiency rules, and the accepted evidence set now changes. Only attempt_chain.py and the new evidence_semantics.py differ from the applied runtime. Their exact runtime inventory and the registry/qualification are bound directly by the material amendment. The already-applied non-material continuation is referenced unchanged; no new non-material continuation disguises this semantic change. Future known observational producers require independently qualified, authenticated registry/implementation updates; a harmless label alone never suffices.','',
 f"Qualification: {len(q['checks'])} focused semantic/history checks and {len(negative['probes'])} actual-context negatives PASS. Negatives cover unknown span/activity/event, model start/sent/provider acceptance, execution/repository/knowledge effects, uncertainty, hidden fields, caller classification, wrong cycle/identity/policy, altered historical bytes/order, projection substitution, missing registry/qualification, registry substitution, ancestry reorder/omission, absent specific issuance, and task/profile/payload/transmission/supervisor substitution.",'',
 '| Production phase | Seconds |','|---|---:|']
lines += [f'| {k} | {v:.3f} |' for k,v in phases.items()]
lines += [f"| Independent sealed reconstruction including fresh S3 | {recovery['seconds']:.3f} |",'',
 'Budgets are unchanged (phase soft 30s/hard 120s); all normal warm validation samples are below 30s and no measured required phase exceeds its hard threshold. Qualification timing is pre-issuance operational diagnostics, never r12 lifecycle telemetry. No broad lifecycle/model qualification was rerun solely because the attempt number changed. Existing accepted mechanisms are reused; no real Programmer request was made.','',
 'S3 remains the exact current qualified, exclusive READY process under its existing succession, observed freshly by the production readiness mechanism. r11 status is FRESH/CANCELLED/RELEASED/QUIESCENT despite stale activity telemetry. r12 has no live invocation to project and no audit namespace.','',
 'Exact identities (all proposed values are non-adopted):','']
for key in ('applied_release_authority_unchanged','proposed_amendment','proposed_amendment_sha256','proposed_release_authority','preserved_continuation','preserved_continuation_sha256','registry_id','implementation_identity','r12_authorization_id','r12_binding_sha256','InvocationAttemptId'):
 lines.append(f'- {key}: `{result[key]}`')
for prefix,values in [('Current',old['operational_identities']),('Proposed',pub['operational_identities']),('Proposed projection',pub['context_identities'])]:
 for k,v in values.items():lines.append(f'- {prefix} {k}: `{v}`')
lines += ['', 'The proposal preserves original dispatch, task, profile, payload, transmission/retention, budgets and S3 bindings, with r8→r9→r10→r11 as authenticated predecessors. No lifecycle, ownership, audit namespace, counters, telemetry, execution or effects are inherited. The replacement reason is PRE_MODEL_NO_PROGRESS_BUDGET_CANCELLATION_NO_EFFECTS.','',
 'Artifacts: [exact proposed binding](PROPOSED_R12_BINDING.json), [material amendment](MATERIAL_AMENDMENT.json), [qualified publication](QUALIFIED_PUBLICATION.json), [semantic probes](SEMANTIC_QUALIFICATION.json), [production negatives](NEGATIVE_CONTEXT.json), [production timing](PREFLIGHT.json), [independent reconstruction](INDEPENDENT_RECONSTRUCTION.json), [preservation baseline](PRESERVATION_BASELINE.json).','',
 'Unchanged historical r11 limitation: real issued/ACTIVE startup previously exhausted no-progress before model handoff and required cancellation-only recovery after the closed-admission instrumentation conflict. This narrow semantic eligibility qualification does not fix that previously observed orchestration behavior or guarantee future run completion. These facts remain in Run-11 evidence.','',
 'Zero real r12 model requests, ActionRequests, ExecutionScopes, ownership reservations, repository/knowledge/implementation effects. No release amendment applied, authorization issued, activation performed or task dispatched.']
(O/'REPORT.md').write_text('\n'.join(lines)+'\n')
manifest={str(p.relative_to(O)):sha(p.read_bytes()) for p in O.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='EVIDENCE_HASHES.json'}
(O/'EVIDENCE_HASHES.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
print(json.dumps({'verdict':result['verdict'],'r12':result['r12_authorization_id'],'binding':result['r12_binding_sha256'],'warm':[v for k,v in phases.items() if k.startswith('warm_')]}))
