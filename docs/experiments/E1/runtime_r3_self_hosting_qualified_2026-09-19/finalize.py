import json,hashlib
from pathlib import Path
O=Path(__file__).resolve().parent
read=lambda n:json.loads((O/n).read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
encoded=lambda d:json.dumps(d,sort_keys=True,separators=(',',':')).encode()
d=read('RUNTIME_QUALIFICATION_FINAL.json');perf=read('PRODUCTION_MEASUREMENTS.json')['samples'];host=read('REAL_R1_S3_RECHECK.json');history=read('HISTORICAL_PRESERVATION.json');components=read('RUNTIME_TIMING.json')
assert len(perf)==3 and all(s['performance_pass'] and s['forbidden_real_request_effect_records']==0 and not s['warnings'] and not s['exhaustion'] for s in perf)
assert all(s['terminal_status']['lifecycle_state']=='CANCELLED' and s['terminal_status']['ownership']=='RELEASED' for s in perf)
assert host['result']=='PASS' and host['S3']=='PASS' and host['runtime']['identity']==d['R1']['identity'] and history['result']=='PASS'
assert host['journal_sha256']=='dc54d729887651e929a7f1eb5258942331524d68ef1aaa7269c7b579ecb9c9b3'
assert host['bootstrap_journal_sha256']=='b4b1abc4343529544437ec07972938995e28f37f3c555bb952501f80f7bca28a'
refs={n:sha(O/n) for n in ['RUNTIME_QUALIFICATION_FINAL.json','RUNTIME_TIMING.json','PRODUCTION_MEASUREMENTS.json','REAL_R1_S3_RECHECK.json','HISTORICAL_PRESERVATION.json','EXACT_BYTE_VERIFICATION.json','NEGATIVE_TEST_LOG.txt','NEGATIVE_QUALIFICATION_APPLICABILITY.json','FINAL_ARCHIVE_TEST_LOG.txt','BOUNDARY_PREDECESSOR.json']}
closure={'schema':'EXACT-SELF-HOSTING-RUNTIME-QUALIFICATION-1','result':'PASS','candidate':d['continuation']['id'],'R1':d['R1']['identity'],'R3':d['R3']['identity'],'evidence':refs,'scope':'ISOLATED_SYNTHETIC_ADOPTION_ONLY','real_enrollment':False,'real_adoption':False,'real_model_requests':0,'real_E1_effects':0}
closure['id']='SELF-HOSTING-QUALIFICATION-sha256:'+hashlib.sha256(encoded(closure)).hexdigest()
(O/'QUALIFICATION_CLOSURE.json').write_bytes(encoded(closure))
pub={'verdict':'SELF_HOSTING_RUNTIME_READY_FOR_ARCHITECT_ENROLLMENT_DECISION','selected_lineage':'R1 -> new exact continuation -> R3','R1':d['R1']['identity'],'R2':'sha256:a37de248a046263db9269e88d4714bfd1d9468719dbff3365d77bde2c501bc3c','R2_disposition':'BLOCKED_EXACT_R2_SELF_HOSTING; qualification artifact only; never production adopted','continuation':d['continuation']['id'],'continuation_file_sha256':sha(O/'PROPOSED_R1_R3_CONTINUATION.json'),'R3':d['R3']['identity'],'qualification':closure['id'],'runtime_head_authority':d['delegation']['lineage'],'prospective_integration_classification':'MATERIAL_RUNTIME_CONSUMPTION_INTEGRATION','real_release_authority':host['release_authority'],'real_context':host['runtime_authority_context'],'real_current_runtime':d['R1']['identity'],'production_journals_unchanged':True,'real_R3_enrolled':False,'real_R3_adopted':False,'S3':'READY','r13_created':False,'real_model_requests':0,'E1_effects':0}
(O/'PUBLICATION.json').write_bytes(encoded(pub))
table='\n'.join(f"| {s['case']} | {s['cumulative_model_request_ready_seconds']:.3f}s | {s['maximum_individual_phase_seconds']:.3f}s | {sum(s['freshness_counts'].values())} FRESH |" for s in perf)
phase=[]
for s in perf:
 phase.append(s['case']+': '+', '.join(f"{p['phase']} {p['seconds']:.3f}s" for p in s['phases'])+'; dispatcher '+', '.join(f"{p['name']} {p['seconds']:.3f}s" for p in s['dispatcher_spans'])+f"; cycle preparation {s['model_cycle_preparation_seconds']:.3f}s.")
report=f'''SELF_HOSTING_RUNTIME_READY_FOR_ARCHITECT_ENROLLMENT_DECISION

Qualification only. Real R1 remains uniquely current. R3 is not enrolled, adopted, or current in production. No r13, provider request, model request, or E1 effect occurred.

Selected production lineage: **R1 → new exact continuation → R3**. R2 was never enrolled/adopted in production and contributes no necessary production state or authority. Its exact consumer fails self-hosting with `invocation runtime is not current adopted head`; that finding and its content remain unchanged. Path A is unnecessary and is not qualified as a safe intermediate production transition. Development/qualification history is not production ancestry.

Exact identities:

- R1: `{d['R1']['identity']}`.
- R2 qualification artifact: `{pub['R2']}`; C2 `C2-CONTENT-CANDIDATE-sha256:0084c85d313ee3fc6e55f4ab012e7fd693337a384d1804e8967dafbb0253b2a2`.
- R1→R3 continuation candidate: `{d['continuation']['id']}`.
- Continuation file SHA-256: `{pub['continuation_file_sha256']}`.
- Exact R3: `{d['R3']['identity']}`.
- Completed qualification: `{closure['id']}`.
- Existing runtime-head authority: `{d['delegation']['lineage']}`.

Self-hosting PASS. Exact R3 loads from its private descriptor root and derives the executing root from the consumer module, not a caller-supplied runtime label. Full content inventory, private authority selection, authenticated R1 prefix and append-only ordinary ancestry establish its synthetic current head. Independent child processes running exact R3 reproduce the result. Genuine production functions in the isolated bound context reached MODEL_REQUEST_READY without provider transport or a mocked validator. Schema-8 qualification machinery is explicitly distinguished from production adoption.

Synthetic R4 PASS. R3 created/qualified/enrolled a later exact candidate under separate synthetic authority; it remained unadopted and R3 remained selected. Separate fixtures applied an explicit synthetic R4 adoption decision, reconstructed R4, and rejected the former R3 as current. No bootstrap transition was invoked. Read-only authentication of the immutable consumed-bootstrap prefix is historical verification, not reuse of bootstrap selection authority.

Negative/recovery qualification: 16 bounded tests PASS for exact R3 bytes, including missing adoption/enrollment, wrong actor/head/predecessor, unadopted executing runtime, substituted bytes, stale enrollment, replay, concurrent adoption, malformed journal, and interruptions after intent/commit. Exact final private-archive focused tests also PASS. Synthetic journals alone were mutated. The main R4 fixture remains unadopted. Tests and source hashes are retained in the closure.

Applicability is separated:

- Correct executing-content identification and dependency-bound verification reuse implement the intended runtime-head model; no budget, task, payload, tool, transmission, ownership, or supervisor semantic change.
- The complete R1→R3 integration is conservatively **MATERIAL_RUNTIME_CONSUMPTION_INTEGRATION**: it selects an externally authorized enrollment-aware ordinary consumer and append-only extension of the established R1 head. It requires an exact material integration decision; the existing prospective enrollment delegation alone does not select this consumer.
- Accepted enrollment component bytes remain identical (`7adf73eb300d7dd2fc1fae8fc36595de2c8b0b35cc534f8c795448414422c549`). No expansion of enrollment capability is proposed. Exact enrollment remains separate from an exact adoption decision.
- Bootstrap, original runtime-head authority, C1, R1 and all historical invocation bindings remain immutable. No qualification decision becomes real authority.

The six-file delta is fully listed in PROPOSED_R1_R3_CONTINUATION.json: two modified integration files and four added consumer/enrollment support files. R3 identity covers all runtime files. Its frozen historical verifier is a byte-identical controller-private archive outside Programmer roots, not a repository runtime authority path. The immutable prefix cache rehashes exact dependencies each time; extension head, selected runtime bytes, lifecycle, ownership, admission, scopes, uncertainty and supervisor are freshly checked.

Timing (unchanged phase soft/hard 30/120s and no-progress hard 300s):

| Sample | Preparation → MODEL_REQUEST_READY | Maximum individual phase | Status |
|---|---:|---:|---|
{table}

No normal soft warnings or hard exhaustion. Each fixture cancelled/released and independently recovered QUIESCENT after reaching the no-provider boundary. Detailed durable spans, controller glue intervals, terminal convergence and per-phase timings are in PRODUCTION_MEASUREMENTS.json.

'''+'\n\n'.join(phase)+f'''

Component samples: runtime-head verification {min(x['seconds']['runtime_head_verification'] for x in components):.3f}–{max(x['seconds']['runtime_head_verification'] for x in components):.3f}s; self-hosting {min(x['seconds']['self_hosting_validation'] for x in components):.3f}–{max(x['seconds']['self_hosting_validation'] for x in components):.3f}s; enrollment validation {min(x['seconds']['enrollment_validation'] for x in components):.3f}–{max(x['seconds']['enrollment_validation'] for x in components):.3f}s; adoption validation {min(x['seconds']['adoption_validation'] for x in components):.3f}–{max(x['seconds']['adoption_validation'] for x in components):.3f}s; independent process {min(x['seconds']['independent_self_hosting_process'] for x in components):.3f}–{max(x['seconds']['independent_self_hosting_process'] for x in components):.3f}s. Enrollment/adoption append and R4 timings are retained separately.

Preservation: {history['checks']} historical hash checks PASS plus 223 exact runtime/archive file checks. Real bootstrap/runtime journal fingerprints match their pre-work values. Independent real reconstruction still selects R1. r12 remains ACTIVE_CANCELLED_PRE_MODEL_NO_EFFECTS with no ownership/scope/uncertainty. Current S3 exact identity and readiness freshly pass; supervisor authority is unchanged.

Real release remains `{host['release_authority']}`. Real OperationalContextId remains `{host['runtime_authority_context']['OperationalContextId']}`. ModelPayloadDigest remains `d675d581c80f43e691a31da73ccf17fd4bcc6b00d3a5331f26b9294e294e1538`.

Preserved intermediate findings: initial candidate R4-enrollment lock composition failure; context-hook name collision; unoptimized cold path 281.167s with soft-phase failures. These were isolated qualification attempts, never production authority. Corrected content received new identities; no failed identity was reused for corrected bytes. Final timing uses only the exact R3 above.

Next authority boundary: Architect review of exact candidate/material integration and enrollment, followed by a separate exact adoption decision. This report grants neither. Production journals remain unchanged; no real ownership was acquired.
'''
(O/'REPORT.md').write_text(report)
print(json.dumps(pub,indent=2))
