"""Report scoped mapping qualification and the unchanged complete-oracle blocker."""
import hashlib
import json
import subprocess
from qualify import ROOT, OUT, SEALED, DOCS, PREFIX, OPTION, BASE_ID, SUBJECT_ID, read, ref, save


def main():
    mapping = read(OUT / 'qualified-composite-mapping.json')
    oracle = read(OUT / 'END-oracle-results.json')
    ready = read(OUT / 'P05-readiness-result.json')
    baseline = read(OUT / 'baseline.json')['files']
    changed = [p for p,h in baseline.items() if not (ROOT/p).is_file() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
    assert not changed,changed
    check = subprocess.run(['git','diff','--check'],cwd=str(ROOT),capture_output=True,text=True)
    assert check.returncode==0,check.stdout+check.stderr
    preserve = {'RESULT':'PASS','preexisting_files_unchanged':len(baseline),'changed_prior_files':[],
        'all_13_stage_bindings_unchanged':True,'all_native_bundle_event_Snapshot_authority_and_source_bytes_unchanged':True,
        'NATIVE_HISTORY_CHANGED':'NO','NATIVE_PERMISSIONS_CHANGED':'NO','RUNTIME_MODIFIED':'NO',
        'E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO','P05_EXECUTED':'NO','P06_EXECUTED':'NO',
        'CONTINUOUS_ORIGINAL_A01_A13_LINEAGE_PROVEN':'NO','N_REAL_SATISFIED':'NO',
        'git_diff_check':'PASS','runtime_files_unchanged':sum(p.startswith('adapter/planner/') for p in baseline),
        'frozen_E1_files_unchanged':sum(p.startswith('docs/experiments/E1/') for p in baseline)}
    save(OUT/'preservation.json',preserve)
    evidence={name:ref(OUT/file) for name,file in {
        'authentication':'scope-authentication.json','entry':'entry-gate.json',
        'qualified_mapping':'qualified-composite-mapping.json','components':'component-results.json',
        'bridges':'bridge-results.json','edges':'edge-results.json','aggregate_N12_N13':'aggregate-N12-N13-results.json',
        'negative_plan':'negative-plan.json','negatives':'negative-results.json','determinism':'determinism.json',
        'complete_END_oracle':'END-oracle-results.json','readiness':'P05-readiness-result.json','preservation':'preservation.json'}.items()}
    result={'WORK_PACKAGE':'E2-P05-COMPOSITE-END-QUALIFICATION','RESULT':'PARTIAL',
        'SELECTED_OPTION':OPTION,'SCOPE_AUTHENTICATION':'PASS','SCOPE_SUBJECT_ID':SUBJECT_ID,
        'STAGE_BINDINGS':'13/13','P05_BOUND_STAGE_INPUTS':13,'P05_REQUIRED_STAGE_INPUTS':13,'SEMANTIC_BRIDGE_COUNT':4,
        'A03_BRIDGE':'PASS; actual prospective CHECK/COLLECT occurrence, END/N12/N13 preserved',
        'A04_BRIDGE':'PASS; native extension of A03, durable PREPARE/post-Snapshot/six-member validation binding preserved',
        'A05_BRIDGE':'PASS; exact retained P03 decision, choice/context and pre-existing-grant/original-prefix limits preserved',
        'A06_BRIDGE':'PASS; exact prospective request-ready then waiting events and local END/N12/N13 preserved',
        'case_mapping_terms_are_not_four_new_semantic_edges':True,
        'exact_semantic_bridge_pairs':[(b['SOURCE'],b['TARGET']) for b in mapping['bridge_checks']],
        'NATIVE_GRAPH_PORTIONS':'PASS; exact retained typed payloads, parent/pre/post/sequence and source/policy pins',
        'P04_CANONICAL_TAIL':'PASS; full 20-event retained lineage, nine governed configuration events and A09-A13 at sequences 10-20 unchanged',
        'COMPOSITE_GRAPH_IDENTITY':BASE_ID,'QUALIFIED_MAPPING_IDENTITY':mapping['qualification_identity'],
        'graph_identity_recipe':'Immutable presealed graph identity; separate content identity for the authenticated acceptance overlay',
        'EDGE_CLASSIFICATIONS':read(OUT/'edge-results.json')['accepted_counts'],
        'edge_identity_validation_does_not_imply_all_required_interface_assurance':True,
        'AGGREGATE_N12_MAPPING':'PASS','AGGREGATE_N13_MAPPING':'PASS',
        'PASS_CLAIM':mapping['overlay']['pass_claim'],'PASS_CLAIM_STATUS':'AUTHORIZED; complete END assurance remains unestablished while six interface/process inputs are unbound',
        'EXCLUDED_CLAIMS':mapping['overlay']['excluded_claims'],
        'NATIVE_HISTORY_CHANGED':'NO','NATIVE_PERMISSIONS_CHANGED':'NO',
        'NEGATIVE_SUITE':'PASS; 16/16 user-required isolated aggregate controls against sealed definitions/exclusions',
        'DETERMINISM':'PASS; 12 fresh readers, three per hash seed 0,1,7,101',
        'SCOPED_COMPOSITE_MAPPING_QUALIFICATION':'PASS',
        'COMPOSITE_P05_END_QUALIFICATION':'FAIL','COMPLETE_END_ORACLE':'FAIL; six pre-existing unbound current interface/process obligations',
        'P05_EXECUTION_READY':'NO','FIRST_REMAINING_BLOCKER':oracle['FIRST_REMAINING_BLOCKER'],
        'P05_COMPLETE_READINESS_RERUN_PERFORMED':False,
        'readiness_rerun_guard':'Complete composite END qualification did not pass; conditional full P05 rerun not entered',
        'NEXT_PACKAGE':ready['NEXT_PACKAGE'],'CONTINUOUS_ORIGINAL_A01_A13_LINEAGE_PROVEN':'NO',
        'CONTINUOUS_NEW_NATIVE_MAINLINE_PROVEN':'NO','P05_EXECUTED':'NO','P06_EXECUTED':'NO',
        'ORIGINAL_A03_HISTORICAL_OCCURRENCE':'UNPROVEN','ORIGINAL_A04_HISTORICAL_ANCESTRY':'UNPROVEN',
        'ORIGINAL_A05_HISTORICAL_ANCESTRY':'UNPROVEN','ORIGINAL_A06_HISTORICAL_REQUEST_WAIT_TRACE':'UNPROVEN',
        'P03_HISTORICAL_CORRESPONDENCE':'UNPROVEN','N_REAL_SATISFIED':'NO',
        'RUNTIME_MODIFIED':'NO','E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO','GIT_DIFF_CHECK':'PASS',
        'evidence':evidence,'verification':{'path':str((OUT/'verification.json').relative_to(ROOT))}}
    save(DOCS/(PREFIX+'E2_P05_COMPOSITE_END_QUALIFICATION_1.json'),result)
    text=f'''# E2-P05 composite END qualification mapping 1

**RESULT = PARTIAL.** Scope authentication, all four exact semantic bridges, retained native ancestry, aggregate N12/N13, sixteen aggregate negatives and twelve fresh reconstructions pass. **SCOPED_COMPOSITE_MAPPING_QUALIFICATION = PASS.** The unchanged **complete** END oracle still fails its six current interface/process-binding obligations. Consequently **COMPOSITE_P05_END_QUALIFICATION = FAIL; P05_EXECUTION_READY = NO.** No P05/P06 or native lifecycle execution occurred.

The [machine companion](DETERMINISTIC_PLANNER_V0_1_E2_P05_COMPOSITE_END_QUALIFICATION_1.json) links full authentication, immutable stage/component/bridge/edge evidence, aggregate assurance terms, negatives, readers, the complete-oracle result, readiness guard and preservation.

## Exact scope authentication

The explicit user selection **{OPTION}** matches the unchanged [decision dossier](qualification/E2_P05_END_ANCESTRY_RECONCILIATION_1/aggregate-END-decision-dossier.json). Subject **{SUBJECT_ID}**, dossier hash **955408c7d0977f7b49fe16206fb6a6373671a172139b0536e67dce0f8cbb64fa**, graph content/identity, oracle, assurance contract, sources, four bridge IDs, pass claim and exclusions match their pre-decision seals.

[Authentication capture](qualification/E2_P05_COMPOSITE_END_QUALIFICATION_1/scope-authentication.json) records the authenticated human user's explicit choice through trusted conversation transport. It issues no native Action, event, INSTALL, END, DECIDE/USE or P05 execution authority; it creates no native RecordedDecision, choice or grant. The old unselected dossier and all individual scope records remain immutable.

The graph definition retains **{BASE_ID}**. The newly authenticated, independently checked acceptance overlay has its separate comparison identity **{mapping['qualification_identity']}**. Neither identity is a native ledger/root/head. The pending fields in the immutable pre-decision definition are preserved as historical contract data; current acceptance is recorded only in the new overlay.

## Thirteen fixed bindings and exactly four bridges

[Component checks](qualification/E2_P05_COMPOSITE_END_QUALIFICATION_1/component-results.json) load every existing stage row unchanged, with its actual source artifact/native identity/lineage/classification/historical label and bounded END/N12/N13 mapping. All thirteen bindings are identical to the pre-decision graph.

[Four bridge results](qualification/E2_P05_COMPOSITE_END_QUALIFICATION_1/bridge-results.json) retain the exact original definitions and edge IDs. The approved acceptance relation is SEMANTIC_ACCEPTANCE_EDGE; native cross-component state/producer/parent equality remains unproven.

| Exact bridge | Independent assurance checked | Native continuity excluded |
|---|---|---|
| A02 → A03 | Read-only original selected Action versus actual prospective CHECK/COLLECT results, declared accepted outputs and local occurrence/N12/N13 | Original selected Snapshot is not the new execution pre-state |
| A04 → A05 | Actual PREPARE result, immutable post-Snapshot/six typed validation members, versus exact retained ready dossier/choice/RecordedDecision evidence | The A04 result is not asserted to have produced the P03 decision's dossier |
| A05 → A06 | Retained P03 decision/context and separate sealed known-rule, missing-Evidence, held-REENTER request-ready start | The old grant or decision is not retagged into the A06 lineage |
| A06 → A07 | Actual ordered request-ready/waiting events and the separately qualified no-receipt waiting checkpoint/fidelity evidence | The P03 Snapshot is not asserted to be the actual successor of the A06 trace |

A04 remains a genuine native extension of the A03 ledger; it is **not** a fifth semantic bridge. Its durable result/event/post-Snapshot binding and six typed validation members remain exact and lossless. The A05 event remains the actual retained **P03** event with its original choice/context, pre-existing grant and original-prefix limits. It is not original A05; no new A05 occurrence, human choice or native grant is created. A06 retains its exact two events, parent/order/positions and absence of later Evidence/proof/reentry/Action effects.

## Native portions and aggregate assurance

[Edge checks](qualification/E2_P05_COMPOSITE_END_QUALIFICATION_1/edge-results.json) validate all seventy immutable edge definitions independently. Only the four authorized cross-component edges acquire semantic acceptance. All other sealed classifications remain intact; no formerly UNPROVEN link is labeled proven native ancestry. Edge identity/classification PASS does not assert that an unresolved interface's separate consumer/process assurance is satisfied.

The complete canonical P04 tail is retained as actual native history: twenty events overall, nine governed configuration occurrences at 3,4,5,6,7,8,9,16,18, with A09–A13 at 10–20. Its actual Evidence/receipt, validation/support, both reentry events, REENTER result, two deferred installs, root/slot proof admissions and FINISH result remain unchanged. A03/A04 and P03/P04 shared prefixes are checked from native fields, not joined by names or report order. A06 remains its own native history.

[Aggregate N12/N13 results](qualification/E2_P05_COMPOSITE_END_QUALIFICATION_1/aggregate-N12-N13-results.json) independently evaluate all six sealed terms for each predicate. N12 checks read-only selection versus actual effect events, no graph-to-native-event fabrication, no authored premise promoted to historical occurrence, exact within-segment order and explicit aggregate scope. N13 separately checks declaration/result roles, scoped output provenance, no foreign-lineage native substitution, independent proof/authority evidence, historical label preservation and no local mapping verdict replacing the global P05 cases.

Both mappings pass at the authorized qualification scope. They do not prove a continuous original or new native mainline, issue permission, or execute the global P05 N12/N13 negative cases.

The authorized bounded claim is preserved exactly:

> {mapping['overlay']['pass_claim']}

That claim is **not fully established for complete END acceptance** while the sealed interface/process obligations below remain unbound. All original historical limitations, the stronger continuous-mainline exclusions, A05 grant-issuance exclusion, production/E1/N-REAL exclusions and future P05/P06 obligations remain explicit.

## Negatives and fresh reconstruction

All **16/16** [aggregate negatives](qualification/E2_P05_COMPOSITE_END_QUALIFICATION_1/negative-results.json) reject before acceptance: missing/extra/changed bridges, retained but wrong native replacements, historical upgrading, A05 relabeling, removed grant limitation, native ancestry across a bridge, stronger mainline claims, N12/N13 inferred from local flags, and permission inferred from mapping. Candidates are isolated documentary copies; successful evidence and all native sources remain unchanged.

The dossier contains binding/exclusion/assurance rules rather than a separately enumerated negative-case file. The [negative plan](qualification/E2_P05_COMPOSITE_END_QUALIFICATION_1/negative-plan.json) was fixed before qualification from the sixteen cases explicitly required in this instruction and those unchanged rules. It introduces no new acceptance criterion.

Twelve fresh processes reconstructed the same membership, edge classifications, native source IDs, four bridge IDs, graph identity and acceptance identity under seeds **0,1,7,101**, three readers each. [Determinism](qualification/E2_P05_COMPOSITE_END_QUALIFICATION_1/determinism.json) uses retained actual inputs, with no writer memory, result application, event append or runtime replay. This qualifies documentary mapping determinism, not P05's still-future full D01/REG suites.

## Complete END oracle and first remaining blocker

[Complete-oracle evaluation](qualification/E2_P05_COMPOSITE_END_QUALIFICATION_1/END-oracle-results.json) checks the entire **unchanged** [sealed END oracle](qualification/E2_P05_END_ANCESTRY_RECONCILIATION_1/END-qualification-oracle.json). All thirteen stage bindings, retained native portions, four bridges, aggregate N12/N13, historical exclusions, permission separation, identities, mapping negatives and determinism pass.

Its separate `/six_interfaces_and_process_inputs` term was sealed as **CONCRETE_FULL_END_EXECUTION_MANIFEST_BINDING_STILL_REQUIRED**. It requires each current definition/capability/oracle/process interface to be bound under the selected method and explicitly says historical READY contracts alone are insufficient. Each of its six graph edges currently selects only the named string in `E2_PC04_END.json#/dependencies`; no exact current consumer/process projection is sealed on that edge.

**FIRST_REMAINING_BLOCKER = E2-PC01 canonical six-Action model → E2-END current interface/consumer/process binding.** The five later declarations are PC02, PC03, T01, D01 and post-reentry continuation. Their definitions and local qualified artifacts exist; what remains absent is the exact current interface/process binding required by this already-sealed complete oracle. This is a preparation gap, not a runtime counterexample, missing aggregate authority or newly added readiness criterion.

The selection authorizes four specific semantic bridges. It does not waive the oracle's retained interface/persistence/process requirements. Therefore complete composite END qualification cannot be marked PASS. No additional binding, source, bridge, fixture repair or permission is introduced here.

## P05 readiness and preservation

[Readiness record](qualification/E2_P05_COMPOSITE_END_QUALIFICATION_1/P05-readiness-result.json) preserves **P05_EXECUTION_READY = NO** at the existing GLOBAL_END_BINDINGS gate, now narrowed to the concrete interface/process input above. The aggregate scope and four-bridge gaps have closed. Because complete composite END qualification did not pass, the conditional full P05 readiness rerun was not entered or claimed performed. Existing sixteen P05 negative expectations, N08/N12 preparation, persistence/replay/process/authority and other non-stage obligations remain unchanged and unrepaired.

Next package: **E2-P05 CURRENT COMPOSITE END INTERFACE / PROCESS BINDING CLOSURE**. P05/P06 remain unexecuted. All 13/13 stage bindings remain closed at their exact qualified scopes.

```text
WORK_PACKAGE = E2-P05-COMPOSITE-END-QUALIFICATION
RESULT = PARTIAL
SELECTED_OPTION = {OPTION}
SCOPE_AUTHENTICATION = PASS
STAGE_BINDINGS = 13/13
SEMANTIC_BRIDGE_COUNT = 4
A03_BRIDGE = PASS
A04_BRIDGE = PASS (NATIVE COMPONENT; NOT A FIFTH BRIDGE)
A05_BRIDGE = PASS
A06_BRIDGE = PASS
NATIVE_GRAPH_PORTIONS = PASS
P04_CANONICAL_TAIL = PASS
COMPOSITE_GRAPH_IDENTITY = {BASE_ID}
AGGREGATE_N12_MAPPING = PASS
AGGREGATE_N13_MAPPING = PASS
NATIVE_HISTORY_CHANGED = NO
NATIVE_PERMISSIONS_CHANGED = NO
NEGATIVE_SUITE = PASS (16/16)
DETERMINISM = PASS (12 FRESH READERS)
SCOPED_COMPOSITE_MAPPING_QUALIFICATION = PASS
COMPOSITE_P05_END_QUALIFICATION = FAIL (SEALED INTERFACE/PROCESS INPUTS UNBOUND)
P05_EXECUTION_READY = NO
FIRST_REMAINING_BLOCKER = E2-PC01 -> E2-END CURRENT INTERFACE/CONSUMER/PROCESS BINDING
CONTINUOUS_ORIGINAL_A01_A13_LINEAGE_PROVEN = NO
CONTINUOUS_NEW_NATIVE_MAINLINE_PROVEN = NO
P05_EXECUTED = NO
P06_EXECUTED = NO
ORIGINAL_A03_HISTORICAL_OCCURRENCE = UNPROVEN
ORIGINAL_A04_HISTORICAL_ANCESTRY = UNPROVEN
ORIGINAL_A05_HISTORICAL_ANCESTRY = UNPROVEN
ORIGINAL_A06_HISTORICAL_REQUEST_WAIT_TRACE = UNPROVEN
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO
RUNTIME_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```

[Preservation](qualification/E2_P05_COMPOSITE_END_QUALIFICATION_1/preservation.json) verifies every preexisting file against entry hashes, including all old dossiers, scopes, bindings, native bundles/events/Snapshots, source/policy bytes, runtime and frozen E1. [Final verification](qualification/E2_P05_COMPOSITE_END_QUALIFICATION_1/verification.json) separately checks the authentication/graph/overlay/bridge/claim identities and source pins. New files contain only this bounded qualification evidence and its read-only harness.
'''
    path=DOCS/(PREFIX+'E2_P05_COMPOSITE_END_QUALIFICATION_1.md')
    if path.exists():assert path.read_text()==text
    else:path.write_text(text)
    print(json.dumps({'RESULT':'PARTIAL','mapping':'PASS','complete_END':'FAIL_UNBOUND_INTERFACES',
        'P05_EXECUTION_READY':'NO','stage_bindings':'13/13','preserved_files':len(baseline)}))


if __name__=='__main__':main()
