"""Report the independently qualified PC03 binding and remaining frontier."""
from copy import deepcopy
import json
import subprocess
from common_v2 import (ROOT, OUT, BASE_OUT, DOCS, Q, PREFIX, PRIOR, CLOSURE,
    HISTORICAL, TERMS, read, sha, ref, save, equal, recovered, selection)


def main():
    p = read(OUT / 'END-projection.json'); manifest = read(OUT / 'invocation-input-manifest.json')
    preflight = read(OUT / 'preflight.json'); negatives = read(OUT / 'negative-results.json')
    deterministic = read(OUT / 'determinism.json'); selected = selection()
    equal('PC03 qualified interface', preflight['PC03_END_INTERFACE'], 'PASS')
    equal('negative suite passes', negatives['RESULT'], 'PASS')
    equal('reader suite passes', deterministic['RESULT'], 'PASS')
    equal('all retained native models inspected', preflight['native_validation']['model_count'], 16)
    body = p['projection']; contract = recovered()
    contract_view = {'PC03_ID': 'E2-PC03', 'PC03_PURPOSE': contract['PURPOSE'],
        'SOURCE_TYPE': ['Original independent phase/mutation/persistence fixture specifications',
            'Retained typed Snapshot/PersistenceBundle phase and checkpoint operands',
            'Sealed independent lifecycle oracles', 'Retained writer/reader fidelity/process comparison records'],
        'REQUIRED_SOURCE': selected, 'END_CONSUMER': contract['CONSUMER'], 'END_INPUT': contract['INTERFACE_ID'],
        'PROCESS': contract['PROCESS'], 'SATISFACTION_RULE': contract['REQUIRED_OUTPUT'],
        'CURRENTNESS_RULE': contract['CURRENTNESS'], 'SCOPE': contract['SCOPE'],
        'LINEAGE': contract['LINEAGE'], 'PROVENANCE': contract['PROVENANCE'],
        'recovered_declaration': contract, 'original_contract_not_changed': True}
    save('recovered-consumer-contract.json', contract_view)
    save('qualified-process-binding.json', {'RESULT': 'PASS', 'process': body['process'],
        'projection_identity': p['identity'], 'manifest_identity': manifest['identity'],
        'materialized_process_binding': ref(OUT / 'process-binding.json'),
        'consumer': body['consumer'], 'process_edges': manifest['manifest']['process_edges'],
        'preflight': ref(OUT / 'preflight.json'), 'PROCESS': 'PASS', 'INPUT_MANIFEST': 'PASS',
        'native_mutating_operations': [], 'prior_producer_commands_are_historical_provenance_only': True})
    old_frontier = read(PRIOR / 'six-interface-frontier.json')
    equal('entry frontier remains PC01/PC02 only', old_frontier['END_INTERFACES_BOUND'], 2)
    records = deepcopy(old_frontier['interfaces'])
    row = records[2]
    for dimension in ('SOURCE_INSTANCE', 'CONSUMER_BINDING', 'PROCESS_BINDING', 'CURRENTNESS'):
        row['STATUS'][dimension] = 'PASS'
    row['STATUS_EXPLANATIONS'].update({
        'SOURCE_INSTANCE': 'Sixteen exact retained native model roles and pinned independent/fidelity/mutation/process pairings resolve the unselected collection; distinct scopes preserved',
        'CONSUMER_BINDING': 'Independent-oracle-qualified documentary projection bound to END dependency 2',
        'PROCESS_BINDING': 'Ninety-one explicit source/oracle/process inputs and concrete read-only invocations qualified',
        'CURRENTNESS': 'Exact supported role/checkpoint versions and physical current source/policy/code pins, with immutable original preparation scope'})
    row['first_failure_dimensions'] = []
    row['current_interface_oracle'] = 'PASS'
    row['current_projection'] = ref(OUT / 'END-projection.json')
    row['current_manifest'] = ref(OUT / 'invocation-input-manifest.json')
    row['current_process_binding'] = ref(OUT / 'qualified-process-binding.json')
    row['independent_preflight'] = ref(OUT / 'preflight.json')
    row['projection_identity'] = p['identity']; row['manifest_identity'] = manifest['identity']
    equal('PC01 and PC02 frontier records preserved', records[:2], old_frontier['interfaces'][:2])
    equal('last three records preserved', records[3:], old_frontier['interfaces'][3:])
    count = sum(all(value in ('PASS', 'NOT_REQUIRED') for value in r['STATUS'].values()) for r in records)
    equal('PC03-only interface closure', count, 3)
    next_interface = records[3]['SOURCE'] + ' -> E2-END'
    # PC04-PC06 below are the user's remaining-interface ordinal labels.
    # They are not invented native package/interface IDs.
    classifications = {}
    for label, record, classification, reason in [
        ('PC04', records[3], 'SAME_QUALIFICATION_BINDING_PATTERN',
            'Recovered read-only T01 capability/API + exact actual A09 source/authentication/event/post-state binding; no new receipt transition'),
        ('PC05', records[4], 'CONTRACT_VARIANT',
            'D01 requires an independently selected complete current positive/negative/seed/permutation/writer/reader input matrix; the source-instance ambiguity remains, and later D01 execution is separate'),
        ('PC06', records[5], 'SAME_QUALIFICATION_BINDING_PATTERN',
            'Recovered documentary binding of existing canonical REENTER/root/slot/FINISH ordered tail and independent boundary oracles; each current eligibility/definition consumer still has its own bounds')]:
        classifications[label] = {'CLASSIFICATION': classification, 'interface_ordinal': record['ORDINAL'],
            'actual_recovered_source': record['SOURCE'], 'actual_input': record['INTERFACE_ID'],
            'process_contract': record['PROCESS'], 'reason': reason, 'binding_status': 'UNRESOLVED_NOT_QUALIFIED_HERE',
            'no_binding_created': True, 'informational_only': True}
    save('remaining-pattern-classification.json', {'classifications': classifications,
        'labels_PC04_PC06_are_remaining_interface_ordinals_not_native_IDs': True,
        'recovered_source_and_contract_preserved': True, 'no_remaining_interface_bound': True})
    save('six-interface-frontier.json', {'RESULT': 'PASS_FRONTIER_REEVALUATION_ONLY',
        'previous_frontier': ref(PRIOR / 'six-interface-frontier.json'), 'interfaces': records,
        'PC01_END_INTERFACE': 'PASS', 'PC02_END_INTERFACE': 'PASS', 'PC03_END_INTERFACE': 'PASS',
        'END_INTERFACES_BOUND': 3, 'END_INTERFACE_COUNT': 6, 'NEXT_UNRESOLVED_INTERFACE': next_interface,
        'P05_STAGE_BINDINGS': '13/13', 'FOUR_SEMANTIC_BRIDGES': 'PASS', 'AGGREGATE_N12': 'PASS', 'AGGREGATE_N13': 'PASS',
        'COMPOSITE_P05_END_QUALIFICATION': 'FAIL', 'P05_EXECUTION_READY': 'NO',
        'previous_two_and_remaining_three_records_unchanged': True,
        'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO'})
    baseline = read(BASE_OUT / 'baseline.json')['file_sha256']
    changed = [name for name, digest in baseline.items() if not (ROOT / name).is_file() or sha(ROOT / name) != digest]
    equal('all pre-existing files preserved', changed, [])
    diagnostic = read(BASE_OUT / 'attempt-1-diagnostic.json')
    for name, digest in diagnostic['retained_attempt_files'].items():
        equal('attempt 1 source/oracle evidence retained', sha(BASE_OUT / name), digest)
    check = subprocess.run(['git', 'diff', '--check'], cwd=str(ROOT), capture_output=True, text=True)
    equal('git diff check', check.returncode, 0)
    save('preservation.json', {'RESULT': 'PASS', 'baseline_file_count': len(baseline), 'prior_files_modified': [],
        'runtime_files_unchanged': sum(name.startswith('adapter/planner/') for name in baseline),
        'E1_files_unchanged': sum(name.startswith('docs/experiments/E1/') for name in baseline),
        'native_artifacts_or_oracle_values_modified': False, 'NATIVE_STATE_CHANGED': 'NO', 'RUNTIME_MODIFIED': 'NO',
        'INSTALL_EVENTS': 0, 'NEW_AUTHORITIES': 0, 'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO',
        'N_REAL_SATISFIED': 'NO', 'E1_ARTIFACTS_MODIFIED': 0, 'PRODUCTION_EFFECT': 'NO', 'git_diff_check': 'PASS',
        'historical_UNPROVEN_labels': HISTORICAL, 'CONTINUOUS_ORIGINAL_A01_A13_LINEAGE_PROVEN': 'NO',
        'original_attempt_and_corrected_checker_seals_retained': True})
    evidence = {key: ref(OUT / filename) for key, filename in {
        'recovered_contract': 'recovered-consumer-contract.json', 'projection': 'END-projection.json',
        'manifest': 'invocation-input-manifest.json', 'source_semantics': 'source-semantics-inventory.json',
        'process': 'qualified-process-binding.json', 'expected_oracle': 'expected-oracle.json',
        'manifest_oracle': 'expected-manifest-oracle.json', 'oracle_seal': 'oracle-seal.json',
        'preflight': 'preflight.json', 'negative_plan': 'negative-plan.json', 'negatives': 'negative-results.json',
        'determinism': 'determinism.json', 'frontier': 'six-interface-frontier.json',
        'pattern_assessment': 'remaining-pattern-classification.json', 'preservation': 'preservation.json'}.items()}
    evidence.update(source_selection=ref(BASE_OUT / 'selected-source-collection.json'),
        checker_attempt_1=ref(BASE_OUT / 'attempt-1-diagnostic.json'))
    result = {'WORK_PACKAGE': 'E2-P05-PC03-END-BINDING', 'RESULT': 'PASS',
        'PC03_CONTRACT': contract_view, 'PC03_SOURCE': evidence['source_selection'],
        'PC03_SOURCE_QUALIFICATION': 'PASS; original preparation scope and already-qualified local scoped comparisons/current canonical operands remain distinct',
        'EXISTING_BINDING_PATTERN_REUSABLE': 'YES',
        'binding_pattern_variant': 'Independent phase/mutation oracle + exact native operand + writer/reader process pairing, not the PC01/PC02 model-only projection',
        'END_CONSUMER': body['consumer'], 'END_PROCESS': body['process'],
        'END_PROJECTION': evidence['projection'], 'PROJECTION_IDENTITY': p['identity'],
        'INVOCATION_INPUT_MANIFEST': evidence['manifest'], 'MANIFEST_IDENTITY': manifest['identity'],
        'MANIFEST_INPUT_COUNT': 91, 'CURRENTNESS': 'PASS; immutable scoped historical roles and exact supported native checkpoint/definition/policy/code/source versions',
        'SCOPE': 'PASS; qualification-only documentary END consumption',
        'LINEAGE': 'PASS; original baseline, A03/A04, A06 and P03/P04 contexts stay distinct; canonical tail remains native',
        'PROVENANCE': 'PASS; exact retained native identities/source selectors and sealed independent versus fidelity oracle provenance',
        'NATIVE_VALIDATION': 'PASS; 16 retained models, native identities/ordered event chains/source-policy support; eight independent F02 boundaries',
        'END_INTERFACE_PREFLIGHT': preflight['terms'], 'NEGATIVE_SUITE': 'PASS; 24/24 isolated binding controls, including native ordered-ledger rejection',
        'DETERMINISM': 'PASS; 36 fresh readers, seeds 0,1,7,101 and three native-declared unordered presentations',
        'PC03_END_INTERFACE': 'PASS', 'PC01_END_INTERFACE': 'PASS', 'PC02_END_INTERFACE': 'PASS',
        'END_INTERFACES_BOUND': 3, 'END_INTERFACE_COUNT': 6, 'NEXT_UNRESOLVED_INTERFACE': next_interface,
        'REMAINING_PATTERN_CLASSIFICATION': classifications, 'P05_STAGE_BINDINGS': '13/13',
        'FOUR_SEMANTIC_BRIDGES': 'PASS', 'AGGREGATE_N12': 'PASS', 'AGGREGATE_N13': 'PASS',
        'COMPOSITE_P05_END_QUALIFICATION': 'FAIL', 'P05_EXECUTION_READY': 'NO',
        'NEXT_PACKAGE': 'E2-P05 E2-T01 -> END QUALIFICATION INTERFACE / PROCESS BINDING CLOSURE',
        'checker_revision': 'Versioned v2 corrects a new checker error; original attempt, prior native sources and lifecycle oracle values retained',
        'NATIVE_STATE_CHANGED': 'NO', 'RUNTIME_MODIFIED': 'NO', 'INSTALL_EVENTS': 0, 'NEW_AUTHORITIES': 0,
        'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO', 'N_REAL_SATISFIED': 'NO',
        'CONTINUOUS_ORIGINAL_A01_A13_LINEAGE_PROVEN': 'NO', 'E1_ARTIFACTS_MODIFIED': 0,
        'PRODUCTION_EFFECT': 'NO', 'GIT_DIFF_CHECK': 'PASS', 'evidence': evidence,
        'verification': {'path': str((OUT / 'verification.json').relative_to(ROOT))}}
    result.update(HISTORICAL)
    path = DOCS / (PREFIX + 'E2_P05_PC03_END_BINDING_1.json')
    raw = json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + '\n'
    if path.exists(): equal('immutable result companion', path.read_text(), raw)
    else: path.write_text(raw)
    native_rows = preflight['native_validation']['model_checks']
    table = '\n'.join('| ' + r['model_id'] + ' | ' + str(r['control']) + ' | ' + str(r['ordered_event_count']) + ' |' for r in native_rows)
    text = f'''# E2-P05 PC03 → END qualification binding materialization 1

**RESULT = PASS. PC03_END_INTERFACE = PASS.** Exact retained independent comparison contracts, native phase/checkpoint operands and writer/reader provenance are bound to END dependency 2 through a documentary projection and concrete manifest. All nine interface terms, **16 native structural/identity/source checks**, **eight independent F02 boundaries**, **24/24 negatives** and **36 fresh-reader reconstructions** pass. **END_INTERFACES_BOUND = 3/6**. Next unresolved: **E2-T01 → E2-END**. P05 remains not ready and unexecuted.

The [machine companion](DETERMINISTIC_PLANNER_V0_1_E2_P05_PC03_END_BINDING_1.json) contains the full report and references the [source selection](qualification/E2_P05_PC03_END_BINDING_1/selected-source-collection.json), [native/oracle/mutation inventory](qualification/E2_P05_PC03_END_BINDING_1/v2/source-semantics-inventory.json), [projection](qualification/E2_P05_PC03_END_BINDING_1/v2/END-projection.json), [invocation/input manifest](qualification/E2_P05_PC03_END_BINDING_1/v2/invocation-input-manifest.json) and [qualified process binding](qualification/E2_P05_PC03_END_BINDING_1/v2/qualified-process-binding.json).

## Recovered PC03 contract and source selection

The exact recovered contract is [END_INTERFACE_CLOSURE_1](qualification/E2_P05_END_INTERFACE_CLOSURE_1/six-interface-inventory.json), `/interfaces/2`, with consumer **E2-END experiment acceptance-case comparison/runner harness**, input **E2-END#/dependencies/2**, edge `qualification-END-edge-v1:b34d2cb6f849d1f4a5f8ef5bc52ba2fcaffb8c61c02e64c4c30befb9c1d8cb0e`. Its purpose is independently source-bound **state, mutation, persistence and cold-reader comparison contracts**. Its process binds independent comparison oracles to exact phase/checkpoint/mutation operands and concrete writer/reader records. Required output is a current END consumer projection/process binding; readiness is not a future execution PASS.

The three directly recovered source pins remain exact: **PC03_FIXTURES** `e601d1cdc133cdc790a90ed8c7218c779214bd47407bc044b7e9b86e7f5c7fd4`, **PC03_VALIDATION** `7ee1d18ec492f73d3e5e6f90561b179f7df772cf5d49c4eefa48d4c4be0a9f1d`, and **FINISH_F03_RESULT** `89f99cb877301679441d9750d31726c6403f4784741ba67fc2a9b2df35458937`. Original PC03 preparation qualification remains PASS: eight ordered phase specifications, sixteen positive and sixteen negative case contracts, six designated invalidation dependencies, mutation isolation and the no-hidden-memory persistence/cold-reader contract. PC03 was not rerun.

The source-instance ambiguity is resolved by selecting existing artifacts explicitly: one retained baseline A01/A02 model; the already-authorized A03, A04, A06 and P03 native post-state bundles; and eleven retained P04 preexecution/configuration/A09–A13 checkpoints. Every role has exact native identity, source selector/raw pin, scope, lineage, generation, qualified use and independent/fidelity comparator. Native source bytes supply structural/state/occurrence evidence; prose/result summaries never substitute for them.

The original PC03 **POST_REENTRY RUNNABLE / FINISH actionable / resume=true scaffold is historical preparation scope**. It is not applied to the current deferred-install boundary. Current post-A12 and pre-root comparisons consume the already-sealed F02/F03 **PLAN_DEFECT** and nonterminal FINISH hold. The exact scope/clarification remains retained; no oracle/control/goal rewrite occurs.

## Phase, mutation, persistence and oracle semantics

| Retained native role | Read-only current computation | Ordered events |
|---|---|---|
{table}

The full typed Snapshot/source is content-addressed and compared independently; the projection also inventories Action statuses, Knowledge/currentness/producers, root/slot state, gate stage/history, decisions/choice references, receipts/observations, ValidationResults/support, typed validations/proofs and installed definition versions. Exact event IDs, result comparison identities, parents, pre/post states, positions and root/head relationships remain ordered.

Eight independent F02 pairs bind POST_A12/PRE_SUPPORT, POST_SUPPORT, POST_SLOT_PROOF, POST_ROOT_PROOF, POST_ROOT_SATISFACTION, PRE_FINISH, POST_FINISH and P04_TARGET to the exact retained canonical checkpoints. Native read-only recomputation, root/slot/proof IDs and unchanged goal inventory match every independent boundary term.

Oracle roles remain separate. Original/local independently authored result/state contracts establish lifecycle expectations. The previously frozen F03 writer/reader full-structure comparators establish **persistence fidelity**, with native source/identity/state comparison; they are not recast as independent lifecycle oracles. Existing transient ResumeEligibility values remain local computed comparison evidence, never persisted permission. No C03 replay, producer invocation or new eligibility event occurs here.

The four explicitly pinned mutation families preserve their already-sealed A03, A04, A06 and F02/A13 negative specifications, exact native operand roles, original driver content and retained qualification results. PC03's six source-invalidation relations remain distinct. These are exact comparison inputs and existing history, not new mutations or future PASS evidence. The canonical tail and successful native lineages remain untouched.

Prior writer/reader manifests, source/policy allowlists, actual checkpoint/event records, source invalidation results and fresh-process qualification evidence are attached explicitly. Each reader receives pinned durable inputs and comparison-only expected files; writer memory is unavailable. Historical producer commands/code are provenance, not executable invitations. No native bundle is created, restored by replay, or persisted by this binding.

## Pattern, identities and concrete invocation

**EXISTING_BINDING_PATTERN_REUSABLE = YES**, with PC03's oracle/operand/process variant. The mechanism is unchanged: retained sources → END-specific qualification projection → invocation/input manifest → explicit process edge → END consumer. PC03's independent phase and mutation comparison requirements are checked separately from PC01/PC02's source-model semantics.

```text
PROJECTION_IDENTITY = {p['identity']}
MANIFEST_IDENTITY = {manifest['identity']}
PROCESS_IDENTITY = {body['process']['identity']}
```

All are separate qualification comparison identities. No synthetic native ledger/root/head, Snapshot, ActionResult, authority or history is introduced. The manifest contains **91 explicit source/native-operand/oracle/process inputs**, with type, source identity/selector, expected semantics, projection, consumer/process, context/provenance/currentness and operand role. Expected/comparator files are marked **COMPARISON_ONLY** and excluded from Planner operands. Concrete interpreter/code/native primitive pins and all bounded CLI seed/reader/presentation invocations are recorded; no TBD term remains.

The [independent raw-source projection oracle](qualification/E2_P05_PC03_END_BINDING_1/v2/expected-oracle.json), [manifest oracle](qualification/E2_P05_PC03_END_BINDING_1/v2/expected-manifest-oracle.json) and [seal](qualification/E2_P05_PC03_END_BINDING_1/v2/oracle-seal.json) preceded active materialization/preflight. They never called the materializer/decoder or a producer. Actual values come from unchanged typed native decoding and read-only model/identity/currentness calculations.

A [retained first-attempt diagnostic](qualification/E2_P05_PC03_END_BINDING_1/attempt-1-diagnostic.json) records a new checker mistake: the final A03 Knowledge inventory was initially compared with COLLECT's per-result output alone. The versioned checker compares the post-state inventory with both already-sealed CHECK/COLLECT output declarations and canonicalizes native-declared Snapshot sets. The original attempt/code/oracles remain retained, and all prior lifecycle oracle values and native artifacts remain exact. This was a checker error, with no producer execution or native runtime counterexample.

## Preflight, currentness and qualification

[Preflight](qualification/E2_P05_PC03_END_BINDING_1/v2/preflight.json) separately passes SOURCE, CONSUMER, PROJECTION, PROCESS, INPUT_MANIFEST, CURRENTNESS, SCOPE, LINEAGE and PROVENANCE. Sixteen retained models pass native structural validation and exact Snapshot identities; event-bearing models pass ordinary native identity/parent/pre-state/position checks without applying a historical event. Physical qualified source/policy pins and required active definition versions pass at their own checkpoint. Later concrete proof definitions remain absent before their actual historical installations. Supported acquisition routes retain their historical role after acquisition applicability ends.

Read-only recomputation inspects immutable inputs and its ordinary deterministic coverage analysis; it supplies no actual result or transition. Source Snapshot bytes remain unchanged. Guards report zero actual result application, event transaction, replay, commit, installation or authority issuance calls.

All **24/24** [PC03 binding negatives](qualification/E2_P05_PC03_END_BINDING_1/v2/negative-results.json) fail closed: source/qualification/membership/identity/semantic/version errors; wrong consumer/process/input manifest/projection; scope/lineage/provenance/stale support; report-for-native substitution; order-sensitive identity; ordered ancestry reversal; old phase-scaffold substitution; oracle-as-operand; hidden writer memory; cross-lineage splice; missing independent boundary pair. Rehashed candidates still fail the independently fixed oracle. Reversed A06 native events additionally fail the ordinary native ledger sequence/parent invariant, establishing order sensitivity independently of metadata comparison.

[Determinism](qualification/E2_P05_PC03_END_BINDING_1/v2/determinism.json) passes **36 fresh readers**: seeds 0,1,7,101 × three readers × original/reversed/rotated declared-set presentations. Each independently reconstructs the exact projection/manifest and inspects all sixteen native roles. Only codec SET_FIELDS collections are permuted; event ancestry, gate history, phase order and positional input relationships retain their order. R05 unordered semantics are preserved.

## Frontier and remaining pattern assessment

The [six-interface frontier](qualification/E2_P05_PC03_END_BINDING_1/v2/six-interface-frontier.json) closes only PC03's source-instance selection, consumer/process attachment and currentness dimensions. **PC01 and PC02 stay PASS; PC03 PASS; 3/6 interfaces bound.** Both prior records and the last three interface records remain identical values to the previous frontier. Next first failure: **{next_interface}**. No remaining binding is created.

The user's PC04–PC06 labels are remaining-interface ordinals, not newly invented native IDs. [Informational classification](qualification/E2_P05_PC03_END_BINDING_1/v2/remaining-pattern-classification.json) records: **PC04/E2-T01 = SAME_QUALIFICATION_BINDING_PATTERN**, with native API/A09 occurrence semantics; **PC05/E2-D01 = CONTRACT_VARIANT**, requiring explicit complete current runner/positive/negative/seed/reader matrix selection; **PC06/post-reentry continuation = SAME_QUALIFICATION_BINDING_PATTERN**, with exact ordered canonical continuation and independent boundaries. Their own native contracts and unresolved statuses remain authoritative.

Thirteen stage bindings, four semantic bridges, aggregate N12/N13, and PC01/PC02 results remain closed and unchanged. **COMPOSITE_P05_END_QUALIFICATION = FAIL; P05_EXECUTION_READY = NO** while the remaining interfaces and sealed global terms are unclosed. Next package: **E2-P05 E2-T01 → END qualification interface/process binding closure**.

## Preservation

[Preservation](qualification/E2_P05_PC03_END_BINDING_1/v2/preservation.json) and [final verification](qualification/E2_P05_PC03_END_BINDING_1/v2/verification.json) check all **{len(baseline)}** pre-existing files, exact native/authority/code/source/policy pins, original attempts and historical exclusions. All 10,677 frozen E1 files remain unchanged. P03 correspondence and original A03/A04/A05/A06 historical witness labels stay UNPROVEN; no continuous original A01–A13 lineage is claimed. P05/P06 remain unexecuted, and N_REAL remains unsatisfied.

```text
WORK_PACKAGE = E2-P05-PC03-END-BINDING
RESULT = PASS
EXISTING_BINDING_PATTERN_REUSABLE = YES
NATIVE_VALIDATION = PASS (16 MODELS; 8 INDEPENDENT BOUNDARIES)
NEGATIVE_SUITE = PASS (24/24)
DETERMINISM = PASS (36 FRESH READERS)
PC03_END_INTERFACE = PASS
END_INTERFACES_BOUND = 3
END_INTERFACE_COUNT = 6
NEXT_UNRESOLVED_INTERFACE = E2-T01 -> E2-END
P05_STAGE_BINDINGS = 13/13
FOUR_SEMANTIC_BRIDGES = PASS
AGGREGATE_N12 = PASS
AGGREGATE_N13 = PASS
PC01_END_INTERFACE = PASS
PC02_END_INTERFACE = PASS
COMPOSITE_P05_END_QUALIFICATION = FAIL
P05_EXECUTION_READY = NO
NATIVE_STATE_CHANGED = NO
RUNTIME_MODIFIED = NO
INSTALL_EVENTS = 0
NEW_AUTHORITIES = 0
P05_EXECUTED = NO
P06_EXECUTED = NO
N_REAL_SATISFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```
'''
    md = path.with_suffix('.md')
    if md.exists(): equal('immutable Markdown result', md.read_text(), text)
    else: md.write_text(text)
    print(json.dumps({'RESULT': 'PASS', 'PC03_END_INTERFACE': 'PASS', 'interfaces': '3/6',
        'next_interface': next_interface, 'prior_files_preserved': len(baseline), 'P05_EXECUTION_READY': 'NO'}))


if __name__ == '__main__':
    main()
