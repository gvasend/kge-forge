"""Emit an honest partial report and verify preservation of all pre-existing files."""
import hashlib,json,subprocess
from collections import Counter
from pathlib import Path
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;D=R/'docs/plans';P='DETERMINISTIC_PLANNER_V0_1_'
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
s=read(O/'summary.json');inventory=read(O/'initial-111-operand-inventory.json')['ROWS']
remaining=[r for r in inventory if r['STATUS']!='RESOLVED'];assert len(remaining)==72
counts=Counter(r['CURRENT_GAP'] for r in remaining)
verification={'hash_seeds':[0,1,7,101],'fresh_processes':4,'resolved_reference_count':39,'remaining_reference_count':72,'resolved_subset_identity':'qualification-D01-resolution-subset-v1:57ed0bde1998d67b2c132e13e15c1d74c65a9f4df8ea511d35a6373849cab63c','independent_resolved_subset_source_and_derivation_checks':'PASS','FULL_INVOCATION_DETERMINISM':'NOT_QUALIFIED','qualification_cases_executed':0}
save(O/'fresh-process-subset-verification.json',verification)
s['REMAINING_GAP_CLASSES']=dict(counts);s['FRESH_PROCESS_SUBSET_VERIFICATION']=verification
s['INITIAL_INVENTORY_SOURCE']='docs/plans/qualification/E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2/revised-operand-audit.json'
s['QUALIFICATION_IDENTITIES_ARE_NATIVE_IDENTITIES']=False
s['COMPLETE_INVOCATION_MANIFEST_CREATED']=False
s['COMPLETE_ORACLE_HANDOFF_CREATED']=False
s['BLOCKERS']=[
 {'id':'A03_PRESTATE','evidence':[r for r in remaining if r['CURRENT_GAP']=='RETAINED_OPERAND_PRESTATE_MISMATCH'],'meaning':'Retained COLLECT acquisition result expects the state after CHECK; capsule is before CHECK. Binding CHECK instead changes the acquisition-case semantics. Requires an explicit versioned capsule/dispatch alignment.'},
 {'id':'A14_BUNDLE_DATAFLOW','evidence':[r for r in remaining if r['CASE_ID']=='E2-A14'],'meaning':'Snapshot-only GovUnknown capsule has no bundle. V2 SAVE_BUNDLE requires PersistenceBundle, and following RESTORE names absent fixture fields instead of consuming SAVE_BUNDLE path/identity. Requires a sealed pure bundle construction and versioned result dataflow.'},
 {'id':'MUTATION_AND_SOURCE_BINDINGS','meaning':'Unchanged retained requests/bundles/grants cannot realize wrong-request, wrong-lineage, wrong-authority, or tampering variants. Exact deferred operators, targets and preserved preconditions are not yet bound. No mutation was applied.'},
 {'id':'ROLE_BOUNDARIES','evidence':'fixture-boundary-evidence.json','meaning':'Root/slot invalidation capsules contain zero typed proofs and zero proof contracts; receipt invalidation capsule contains zero receipt admissions and zero Evidence entities. Exact dependency-bearing input boundaries must be corrected before descriptor binding.'}]
baseline=read(O/'preservation-baseline.json');changed=[p for p,h in baseline.items() if not (R/p).is_file() or sha(R/p)!=h]
assert not changed,changed
check=subprocess.run(['git','diff','--check'],cwd=str(R),capture_output=True,text=True);assert check.returncode==0,check.stdout+check.stderr
preservation={'PRE_EXISTING_FILES_CHANGED':changed,'TRACKED_BASELINE_FILE_COUNT':len(baseline),'NATIVE_STATE_CHANGED':'NO','E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO','QUALIFICATION_CASES_EXECUTED':0,'P05_EXECUTED':'NO','P06_EXECUTED':'NO','INSTALL_EVENTS':0,'NEW_AUTHORITIES':0,'N_REAL_SATISFIED':'NO','END_INTERFACES_BOUND':'4/6','P05_STAGE_BINDINGS':'13/13','PC01_END':'PASS','PC02_END':'PASS','PC03_END':'PASS','T01_END':'PASS','E2_D01_END':'BLOCKED','CONTINUATION_INTERFACE':'UNRESOLVED_UNCHANGED','HISTORICAL_UNPROVEN_LABELS':'PRESERVED','GIT_DIFF_CHECK':'PASS'}
save(O/'preservation.json',preservation);s['PRESERVATION']=preservation
s['ARTIFACTS'].update({n:{'path':str((O/n).relative_to(R)),'raw_sha256':sha(O/n)} for n in ['construct.py','verify.py','finalize.py','fixture-boundary-evidence.json','fresh-process-subset-verification.json','preservation.json']})
save(D/(P+'E2_P05_D01_OPERAND_CLOSURE_3.json'),s)
lines=['# E2-P05 D01 invocation-operand closure 3','',
'`WORK_PACKAGE = E2-P05-D01-OPERAND-CLOSURE-3`  ',
'`RESULT = PARTIAL`','',
'39 of the exact 111 initial missing operand reference occurrences are resolved. **72 remain unresolved.** The package contains draft invocation records for every one of the 128 obligations, but no record is promoted to complete. It does not satisfy operand-closure acceptance.','',
'| Report field | Result |','| --- | --- |',
'| INITIAL_MISSING_OPERANDS | 111 |','| FINAL_MISSING_OPERANDS | 72 |',
'| INVOCATION_RECORDS | 0/128 complete; 128 draft obligation records |',
'| SOURCE_RESOLUTION | 39 pinned reference occurrences; partial |',
'| DERIVED_OPERANDS | Five structurally parsed SourceInvalidation descriptors; no invalidation applied |',
'| CROSS_OPERAND_CONSISTENCY | NOT_PASS |',
'| INVOCATION_STATIC_PREFLIGHT | NOT_PASS: unresolved operands and applicability |',
'| INDEPENDENT_OPERAND_RECONSTRUCTION | Coverage PASS; resolved subset independently verified; complete semantic reconstruction NOT_PASS |',
'| OPERAND_NEGATIVE_SUITE | Seven static guards PASS; complete requested suite NOT_COMPLETE |',
'| D01_INVOCATION_OPERANDS_COMPLETE | NO |',
'| ORACLE_HANDOFF_MANIFEST | NOT_READY; preparation inventory only |',
'| FULL_OUTPUT_ORACLES | 0/128 |',
'| PROSPECTIVE_D01_MATRIX_CONSTRUCTION_READY | NO |',
'| PROSPECTIVE_D01_SCOPE_DECISION_READY | NO |',
'| PROSPECTIVE_D01_EXECUTION_READY | NO |',
'| END_INTERFACES_BOUND | 4/6 |','| P05_EXECUTION_READY | NO |',
'| E1_ARTIFACTS_MODIFIED | 0 |','| PRODUCTION_EFFECT | NO |','',
'## Source and operand recovery','',
'The initial inventory is taken directly from Closure 2’s revised operand audit, with an assertion of exactly 111 occurrences. Each inventory record identifies obligation, case, variant, dispatch step, capsule, operand, required native type/domain, semantic role, entrypoint, source candidate, and the remaining gap or resolution. Positional signatures, keyword-only operands, defaults, docstrings and current source hashes are recovered from native function ASTs. No native case function is called.','',
'Resolved inputs include A04’s retained supplied dossier result and typed validation records; A05’s recorded decision; A06’s ordered READY/WAIT event commands; A09’s retained admission request and exact raw payload-byte descriptor; A10’s validation admission; A11/A12/A13’s retained ordered event/result commands; and retained cold-reader bundle paths with pinned raw identities and matching sibling event files. The archive/source closure and current applicability of the reader process are not claimed fully validated.','',
'The five additional invalidation references use each N04 capsule’s unique receipt: Evidence selects receipt.artifact; attestor selects receipt.authentication, its Predicate.entity, and that entity’s source identity. The external-route obligation selects its unique native resolution-contract provenance identity. Each descriptor binds the canonical sealed pre-Snapshot identity. Descriptor construction changes no Snapshot, source, ledger, receipt, or persisted Planner bundle.','',
'Existing results are supplied only to entrypoints that consume them. Pre-Snapshots come from sealed capsules; post-Snapshots are not supplied as pre-state. Future native returns remain explicit V2 dataflow references, never precomputed inputs. Qualification content digests identify documentary operand bindings; they are not substituted for native ArtifactIdentity, ActionId, KnowledgeId or PredicateId domains.','',
'## Unresolved construction conflicts','',
'**A03:** both acquisition rows have a pre-state mismatch. The retained COLLECT result expects the state after CHECK; the capsule is before CHECK. Substituting CHECK would change the acquisition case. Exact hashes and source pointers are recorded in the 111-reference inventory.','',
'**A14:** both rows contain only a governed-unknown Snapshot. The dispatch calls SAVE_BUNDLE with an absent PersistenceBundle and then RESTORE with absent fixture path/identity fields. RECOMPUTE returns a Computation, not that bundle. An explicit pure bundle-construction rule and corrected save-to-restore dataflow remain necessary.','',
'**Role boundaries:** the root/slot invalidation capsules have no typed proof or proof contract. The receipt-invalidation capsule has no receipt or Evidence entity. Their structural validity does not establish the required dependency-bearing boundary. `fixture-boundary-evidence.json` records the pinned capsules and native collection counts.','',
'**Negative and mutation inputs:** unchanged positive admission commands, grants and bundles cannot replace intended negative variants. Exact deferred operators and targets, request-key rebinding, trusted pre-tamper identities, and compatible fixture boundaries remain unsealed. This package does not choose arbitrary alternate sources or apply mutations.','',
'| Remaining gap class | Occurrences |','| --- | --- |']
for k,v in sorted(counts.items()):lines.append('| '+k.replace('|','/')+' | '+str(v)+' |')
lines+=['','## Validation and handoff','',
'Native structural decoding loads existing operands, and the audit checks dispatch targets, prior-result dependency order, Snapshot identities, source file availability, and pinned byte identities. These are partial checks: no complete cross-operand applicability, currentness, reader isolation, permutation or mutation preflight is asserted.','',
'An independent script reconstructs frozen obligation/capsule coverage, rereads retained inputs, verifies raw pins/content identities, and independently derives the five descriptor targets and pre-Snapshot hashes. Fresh processes under seeds 0, 1, 7 and 101 produce the same resolved-subset identity:','',
'`'+verification['resolved_subset_identity']+'`','',
'The seven fail-closed static guards reject missing/duplicate rows, wrong dispatch, wrong variant, wrong capsule, altered source pin, and promotion of incomplete records. The requested semantic operand-negative suite remains incomplete.','',
'`oracle-handoff.preparation.json` exposes every draft invocation reference, the full-output schema fields requiring expected values, and proposed independent oracle-source classifications. It contains no expected output values and is not a complete handoff manifest. Complete invocation records and an accepted handoff are withheld until all references and applicability checks pass.','',
'## Artifacts','',
'All supporting files are under `qualification/E2_P05_D01_OPERAND_CLOSURE_3/`:','',
'- `initial-111-operand-inventory.json`: all initial occurrences and final dispositions.',
'- `entrypoint-contracts.json`: exact native signature/default/source inventory.',
'- `operand-source-and-derivation-inventory.json`: resolved source pins and rules.',
'- `invocation-records.partial.json`: 128 draft obligation records with explicit variant steps and pinned operand references.',
'- `cross-operand-validation.json`: partial per-variant checks and remaining applicability gaps.',
'- `independent-reconstruction.json`, `fresh-process-subset-verification.json`, `operand-negatives.json`: bounded verification evidence.',
'- `oracle-handoff.preparation.json`: output schema and oracle-source preparation; no expected values.',
'- `construct.py`, `verify.py`, `finalize.py`: reproducible metadata-only tooling.',
'- `preservation-baseline.json`, `preservation.json`: pre-existing file integrity and preservation evidence.','',
'## Preservation','',
'All pre-existing adapter/docs file hashes in the baseline are unchanged. P05 stage bindings remain 13/13; PC01/PC02/PC03/T01 remain PASS; END remains 4/6; E2-D01 stays BLOCKED and the continuation interface stays unresolved. Original D01 complete inputs remain UNRECOVERED. Historical UNPROVEN labels and N_REAL_SATISFIED=NO are preserved.','',
'`QUALIFICATION_CASES_EXECUTED = 0`; `P05_EXECUTED = NO`; `P06_EXECUTED = NO`; `NATIVE_STATE_CHANGED = NO`; `INSTALL_EVENTS = 0`; `NEW_AUTHORITIES = 0`; `E1_ARTIFACTS_MODIFIED = 0`; `PRODUCTION_EFFECT = NO`; `git diff --check = PASS`.','']
(D/(P+'E2_P05_D01_OPERAND_CLOSURE_3.md')).write_text('\n'.join(line.rstrip() for line in lines))
print('REPORT_CREATED: PARTIAL; 111 -> 72; native state and all pre-existing documents unchanged')
