"""Record only a qualified A05 evidence-graph overlay and its result report."""
import ast
import copy
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
PREFIX = 'docs/plans/DETERMINISTIC_PLANNER_V0_1_'
NAME = 'E2_P05_A05_ALTERNATE_NATIVE_EVIDENCE_RESULT_1'


def save(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')


def pin(path, pointer=''):
    return {'path': str(path.relative_to(ROOT)), 'pointer': pointer,
            'raw_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def load_pin(source):
    path = ROOT / source['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == source['raw_sha256'], source['path']
    return json.loads(path.read_bytes())


def main():
    contract = json.loads((OUT / 'mapping-contract.json').read_bytes())
    summary = json.loads((OUT / 'qualification-summary.json').read_bytes())
    assert summary['result'] == 'PASS' and summary['barred_calls'] == []
    for source in summary['evidence'].values():
        load_pin(source)
    for source in json.loads((OUT / 'seal.json').read_bytes())['pins']:
        load_pin(source)
    mapping = load_pin(summary['evidence']['END-acceptance-mapping.json'])
    auth = load_pin(summary['evidence']['authorization-authentication.json'])
    previous = load_pin(contract['authoritative_sources']['P05_current_graph'])
    readiness = load_pin(contract['authoritative_sources']['P05_readiness'])
    # Recheck every retained native/evidence reference on all prior rows, without
    # applying a result or invoking replay to manufacture any missing occurrence.
    pin_checks = {}
    def check_nested(value):
        if isinstance(value, dict):
            if 'path' in value and 'raw_sha256' in value:
                path = ROOT / value['path']
                assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == value['raw_sha256'], value['path']
                pin_checks[value['path']] = value['raw_sha256']
            for child in value.values():
                check_nested(child)
        elif isinstance(value, list):
            for child in value:
                check_nested(child)
    check_nested(previous['stage_bindings'])
    check_nested(readiness)
    assert previous['P05_BOUND_STAGE_INPUTS'] == 11
    assert len(previous['stage_bindings']) == 13
    assert sum(row['binding_status'] == 'BOUND' for row in previous['stage_bindings']) == 11
    assert previous['stage_bindings'][4]['stage'] == 'E2-A05'
    assert previous['stage_bindings'][5]['stage'] == 'E2-A06'
    assert readiness['P05_INITIAL_ORACLE'] == 'PASS' and readiness['E2_P05_READY'] == 'YES'
    assert readiness['E2_P04_RESULT'] == 'PASS'
    assert mapping['END_MAPPING'] == 'PASS_FOR_A05_ALTERNATE_TERM_ONLY'
    assert mapping['N12_MAPPING']['result'] == mapping['N13_MAPPING']['result'] == 'PASS'
    ancestry = mapping['native_ancestry']
    labels = mapping['historical_and_scope_labels']
    limits = {
        'PREEXISTING_GRANT_LIMITATION': 'The bounded USE grant exists in the retained native pre-state and is unchanged. Decision admission and native DECIDE/USE relationships are proven; grant issuance is not.',
        'ORIGINAL_PREFIX_LIMITATION': 'Original A04 -> A05 ancestry, original baseline occurrence, original authenticated choice/trust-root envelope and wider original prefix -> checkpoint -> target linkage remain UNPROVEN/unresolved. The A05-only alternate term does not waive a full-END requirement.',
        'A06_LIMITATION': 'E2-A06.request_wait_event_trace remains unbound; no A06 ancestry or occurrence is inferred from this P03 decision event.'}
    row = {
        'stage': 'E2-A05', 'binding_status': 'BOUND',
        'classification': 'AUTHORIZED_ALTERNATE_NATIVE_EVIDENCE',
        'logical_required_input': 'E2-A05.recorded_decision_event_ancestry',
        'authorized_acceptance_term': mapping['replacement_acceptance_term'],
        'governing_decision': contract['selected_option'],
        'authorization_subject': contract['subject_identity'],
        'dossier_raw_sha256': contract['dossier_raw_sha256'],
        'scope_authentication': pin(OUT / 'authorization-authentication.json'),
        'sealed_mapping': pin(OUT / 'END-acceptance-mapping.json'),
        'native_event': ancestry['event_in_checkpoint'],
        'native_event_in_P04': ancestry['event_in_canonical_descendant'],
        'alternate_event_id': mapping['native_event_id'],
        'alternate_event_original_role': 'P03',
        'native_result_reference': mapping['native_result_reference'],
        'native_RecordDecision_identity_domain': 'No standalone native result identity; enclosing event /result selector and existing record EntityId',
        'existing_native_record_EntityId': mapping['RecordedDecision_binding']['record_EntityId'],
        'existing_choice_identity': mapping['RecordedDecision_binding']['choice_evidence_identity'],
        'alternate_parent_id': ancestry['parent'],
        'alternate_pre_snapshot': ancestry['pre_snapshot'],
        'alternate_post_snapshot': ancestry['post_snapshot'],
        'alternate_sequence': ancestry['ledger_position'],
        'alternate_index': ancestry['zero_based_index'],
        'alternate_ledger_membership': ancestry['ledger_membership'],
        'alternate_context': ancestry['scope_lineage_generation'],
        'original_event_id': None, 'original_parent_id': None,
        'original_ledger_position': None, 'original_historical_ancestry': 'UNPROVEN',
        'original_history_splice': False, 'historical_identity_alias': False,
        'original_record_changed': False, 'new_execution': False,
        'new_native_event_created': False, 'new_human_choice_created': False,
        'new_native_grant_issued': False, 'P03_event_is_original_A05_event': False,
        'mapping_result': 'PASS', 'END_MAPPING': 'PASS_FOR_A05_ONLY',
        'N12_MAPPING': 'PASS', 'N13_MAPPING': 'PASS',
        'qualification_negatives': 'PASS: 26/26 mapping controls',
        'fresh_readers': 12, 'determinism': 'PASS',
        'currentness': 'Native inputs/source/policy/authority relationships checked at the exact retained qualification occurrence; immutable event remains occurrence evidence at P04 target, not a new permission.',
        'limitations': limits, 'original_prefix_gap_closed': False,
        'A06_gap_closed': False, 'full_END_original_ancestry_waived': False}
    graph = copy.deepcopy(previous)
    graph['stage_bindings'][4] = row
    for i in range(13):
        if i != 4:
            assert graph['stage_bindings'][i] == previous['stage_bindings'][i]
    remaining = [r['stage'] + '.request_wait_event_trace' for r in graph['stage_bindings'] if r['binding_status'] != 'BOUND']
    assert remaining == ['E2-A06.request_wait_event_trace']
    count = sum(r['binding_status'] == 'BOUND' for r in graph['stage_bindings'])
    assert count == 12
    graph.update({
        'schema': 'E2-P05-A05-AUTHORIZED-ALTERNATE-BINDING-RESULT-1',
        'result': 'PASS_FOR_A05_MAPPING; FULL_GRAPH_INCOMPLETE',
        'QUALIFICATION_TYPE': 'AUTHORIZED_ALTERNATE_NATIVE_EVIDENCE',
        'E2_A05_RECORDED_DECISION_EVENT_ANCESTRY': 'PASS',
        'ORIGINAL_A05_HISTORICAL_ANCESTRY': 'UNPROVEN',
        'P03_EVENT_IS_ORIGINAL_A05_EVENT': 'NO',
        'END_MAPPING': 'PASS_FOR_A05_ONLY; FULL_GRAPH_INCOMPLETE',
        'P05_PREVIOUS_BOUND_STAGE_INPUTS': 11, 'P05_BOUND_STAGE_INPUTS': count,
        'P05_NEXT_MISSING_INPUT': remaining[0], 'remaining_stage_gaps': remaining,
        'P05_EXECUTION_READY': 'NO', 'E2_END_INPUT_GRAPH': 'FAIL_COMPLETENESS',
        'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO',
        'NEXT_PACKAGE': 'E2-P05-A06-REQUEST-WAIT-EVENT-TRACE-RECOVERY',
        'new_native_objects_or_authority_from_binding': 0,
        'prior_source_hash_pins_rechecked': len(pin_checks),
        'binding_source': contract['authoritative_sources']['P05_current_graph'],
        'only_stage_row_changed': 'E2-A05',
        'A03_A04_rows_preserved_exact': True, 'A06_row_preserved_exact': True,
        'original_full_END_ancestry_waived': False, 'next_missing_input_resolved': False,
        'acceptance_mapping_comparison_identity': summary['mapping_comparison_identity']})
    save(OUT / 'P05-binding-rerun.json', graph)
    readiness_checks = {
        'P04_package_prerequisite': 'PASS',
        'P05_initial_oracle': 'PASS_RETAINED; exact P04 bytes/pins unchanged',
        'A05_scope_and_mapping': 'PASS', 'A01_A13_stage_bindings': '12/13; A06 missing',
        'complete_END_prefix_or_full_acceptance_mapping': 'UNRESOLVED_NOT_WAIVED',
        'required_existing_input_pins': 'PASS_FOR_BOUND_ROWS',
        'required_capabilities_and_definitions': 'No new gap or change established by this mapping',
        'sixteen_P05_negative_expectations': 'SEALED_UNCHANGED; not executed in this package',
        'P05_persistence_replay_obligations': 'SEALED_UNCHANGED; concrete full-END process bindings await input closure',
        'P05_full_exit_terms': 'NOT_EVALUATED_AS_EXECUTION; P05 unexecuted',
        'P05_EXECUTION_READY': 'NO', 'E2_P05_READY': 'YES', 'P06_EXECUTED': 'NO'}
    save(OUT / 'P05-readiness-checks.json', {
        'schema': 'A05-ALTERNATE-P05-READINESS-CHECKS-1',
        'source': contract['authoritative_sources']['P05_readiness'],
        'checks': readiness_checks,
        'bound_source_pin_checks': [{'path': p, 'raw_sha256': h, 'status': 'PASS'} for p, h in sorted(pin_checks.items())],
        'P05_initial_oracle_reexecuted': False,
        'first_missing_stage': remaining[0],
        'other_open_END_gate': graph['additional_unresolved_END_gate']})
    report = {
        'schema': 'E2-P05-A05-ALTERNATE-NATIVE-EVIDENCE-RESULT-1',
        'WORK_PACKAGE': 'E2-P05-A05-ALTERNATE-NATIVE-EVIDENCE', 'RESULT': 'PASS',
        'SELECTED_OPTION': contract['selected_option'], 'SCOPE_AUTHENTICATION': 'PASS',
        'SCOPE_SUBJECT_ID': contract['subject_identity'], 'DOSSIER_RAW_SHA256': contract['dossier_raw_sha256'],
        'SCOPE_AUTHORITY_DOMAIN': 'QUALIFICATION_ACCEPTANCE_ONLY; no native operating/grant/execution authority',
        'GOVERNING_SOURCE_PINS_MATCH': len(contract['governing_source_pins']),
        'ALTERNATE_EVENT_ID': mapping['native_event_id'], 'ALTERNATE_EVENT_ORIGINAL_ROLE': 'P03',
        'ALTERNATE_EVENT_ANCESTRY': 'PASS', 'RECORDED_DECISION_BINDING': 'PASS',
        'A05_SEMANTIC_CORRESPONDENCE': 'PASS',
        'ORIGINAL_A05_HISTORICAL_ANCESTRY': 'UNPROVEN', 'P03_EVENT_IS_ORIGINAL_A05_EVENT': 'NO',
        'HISTORICAL_RECONSTRUCTION': 'NO', 'NEW_A05_OCCURRENCE_CREATED': 'NO',
        'NEW_HUMAN_CHOICE_CREATED': 'NO', 'NEW_NATIVE_GRANT_ISSUED': 'NO',
        'END_MAPPING': 'PASS_FOR_A05_ALTERNATE_TERM_ONLY', 'N12_MAPPING': 'PASS', 'N13_MAPPING': 'PASS',
        'NEGATIVE_SUITE': {'result': 'PASS', 'passed': 26, 'total': 26, 'domain': 'Read-only acceptance mapping gates; no native execution'},
        'DETERMINISM': {'result': 'PASS', 'independent_fresh_readers': 12,
                        'hash_seeds': [0, 1, 7, 101], 'presentation_modes': ['native', 'reverse_unordered', 'rotate_unordered'],
                        'mapping_comparison_identity': summary['mapping_comparison_identity'], 'native_replay': 'NOT_RUN'},
        'E2_A05_RECORDED_DECISION_EVENT_ANCESTRY': 'PASS',
        'BINDING_CLASSIFICATION': 'AUTHORIZED_ALTERNATE_NATIVE_EVIDENCE',
        'P05_BOUND_STAGE_INPUTS': 12, 'P05_TOTAL_STAGE_INPUTS': 13,
        'P05_NEXT_MISSING_INPUT': remaining[0], 'P05_EXECUTION_READY': 'NO',
        'E2_P05_READY': 'YES', 'E2_END_INPUT_GRAPH': 'FAIL_COMPLETENESS',
        'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO', 'E2_P04_RESULT': 'PASS',
        'ORIGINAL_A03_HISTORICAL_OCCURRENCE': 'UNPROVEN', 'ORIGINAL_A04_HISTORICAL_ANCESTRY': 'UNPROVEN',
        'P03_HISTORICAL_CORRESPONDENCE': 'UNPROVEN', 'N_REAL_SATISFIED': 'NO',
        'RUNTIME_MODIFIED': 'NO', 'E1_ARTIFACTS_MODIFIED': 0, 'PRODUCTION_EFFECT': 'NO',
        'GIT_DIFF_CHECK': 'PASS', 'NEXT_PACKAGE': graph['NEXT_PACKAGE'],
        'qualification_scope_authentication': auth,
        'native_ancestry': ancestry, 'RecordedDecision_binding': mapping['RecordedDecision_binding'],
        'semantic_correspondence': mapping['semantic_correspondence'],
        'N12_term_by_term': mapping['N12_MAPPING'], 'N13_term_by_term': mapping['N13_MAPPING'],
        'readiness_checks': readiness_checks,
        'evidence': {name: pin(OUT / name) for name in
                     ('authorization-authentication.json', 'mapping-contract.json', 'seal.json',
                      'END-acceptance-mapping.json', 'N12-mapping.json', 'N13-mapping.json',
                      'negative-plan.json', 'negative-results.json', 'fresh-reader-determinism.json',
                      'qualification-summary.json', 'P05-binding-rerun.json', 'P05-readiness-checks.json',
                      'qualification-code-pins.json')},
        'preservation_verification': {'path': str((OUT / 'verification.json').relative_to(ROOT)),
                                      'domain': 'All pre-existing files, native runtime, frozen E1, sealed native sources and prior graphs'},
        **limits}
    save(ROOT / (PREFIX + NAME + '.json'), report)
    parent = ancestry['parent']
    record = mapping['RecordedDecision_binding']
    md = f'''# E2-P05 A05 alternate native-evidence qualification 1

**RESULT = PASS.** The exact retained P03 `RecordedDecision` event qualifies for the authorized **A05-only** acceptance mapping. Scope authentication, native ancestry, semantic correspondence, END mapping, N12 and N13 all pass. P05 advances from **11/13 to 12/13**. Its next missing stage input is **`E2-A06.request_wait_event_trace`**; **P05_EXECUTION_READY = NO**. The wider original-prefix/END linkage also remains unresolved.

The alternate event retains its P03 identity and role. **ORIGINAL_A05_HISTORICAL_ANCESTRY = UNPROVEN**. No new A05 occurrence, human choice, native grant or native replay was produced.

## Authentication and sealed scope

The explicit user selection `AUTHORIZE_P05_A05_ALTERNATE_NATIVE_EVIDENCE` is authenticated through the current user-role request against the exact [recovery dossier](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/scope-decision-dossier.json). Its subject is `{contract['subject_identity']}`; dossier bytes hash to `{contract['dossier_raw_sha256']}`. All **{len(contract['governing_source_pins'])} governing source pins** match. [Authentication](qualification/E2_P05_A05_ALTERNATE_NATIVE_EVIDENCE_1/authorization-authentication.json) records issuer, provenance, exact selected option, subject and exclusions. It claims no cryptographic signature or native grant.

The old dossier's unselected flags remain unchanged as historical pre-decision metadata. This package records the new selection separately. Its authority permits qualification acceptance only; it grants no Action, DECIDE, USE, event, installation, grant-issuance or P05-execution permission. [The mapping contract and controls](qualification/E2_P05_A05_ALTERNATE_NATIVE_EVIDENCE_1/mapping-contract.json) were [sealed](qualification/E2_P05_A05_ALTERNATE_NATIVE_EVIDENCE_1/seal.json) before native-record qualification.

## Exact retained event and ancestry

| Term | Verified native value |
|---|---|
| Event / original role | `{mapping['native_event_id']}` / P03 |
| Event type | ExecutionEvent containing RecordedDecision |
| Native result | E2-DECIDE; ALLOW_QUALIFICATION_MAPPING; E2-PROSPECTIVE-CHOICE; E2-PROSPECTIVE-CHOICE-AUTHORITY; exact expected Snapshot |
| Parent / checkpoint root | `{parent}` |
| Pre-Snapshot | `{ancestry['pre_snapshot']}` |
| Post-Snapshot | `{ancestry['post_snapshot']}` |
| Enrollment | Sequence 2, zero-based index 1; `/bundle/events/1` |
| Checkpoint bundle | `{contract['dossier_subject']['alternate_native_witness']['checkpoint_bundle']}` |
| P04 descendant bundle | `{contract['dossier_subject']['alternate_native_witness']['canonical_descendant_bundle']}` |
| Scope | E2-QUALIFICATION-ONLY |
| Lineage / generation | E2-P03-PROSPECTIVE-QUALIFICATION-1 / E2-P03-PROSPECTIVE-GENERATION-1 |
| Choice content | `{record['choice_evidence_identity']}` |
| P03 dossier | `{record['native_dossier_identity']}` |

The [immutable event file](event-9f00d563a015969d02179c7a991d2efec97b763448fbc27c34e7bd634d36a728.json), [P03 checkpoint](DETERMINISTIC_PLANNER_V0_1_P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1.json) and [canonical P04 descendant](DETERMINISTIC_PLANNER_V0_1_E2_P04_CANONICAL_TARGET_BUNDLE_1.json) agree on the complete typed event. Independent algebraic hashing agrees with the native event codec. Both complete retained ledgers pass sequence, parent, pre/post-Snapshot and final-head comparison. The P03 checkpoint has two events; the P04 descendant has twenty and retains the exact two-event prefix. Source and policy files are verified against their physical pins.

The actual predecessor is retained ActionReevaluation sequence 1, with no state effect. The P04 successor is InstallDefinition sequence 3, `{ancestry['canonical_descendant_successor']['id']}`. These establish the candidate's native ancestry from retained fields, without application or replay of the decision. Ordinary PersistenceBundle exposes no separate LedgerId: membership is the exact bundle identity plus `/bundle/events`, with native sequence/index and first/last event identities. No ledger identifier is invented.

## RecordedDecision and A05 correspondence

[The canonical matrix](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:61) requires native decision admission, recorded history, independently evaluated bounded authority and no automatic root/slot satisfaction. The candidate's five-field RecordedDecision, accepted choice knowledge, native record, DECIDE predicate, dossier, issuer, pinned P03 scope root and source provenance satisfy these relationships. RecordedDecision has no standalone native result ID; the binding uses the existing event's `/result` selector and record EntityId **E2-PROSPECTIVE-CHOICE**. No A05 choice identity is created.

Pure native queries independently confirm decision readiness/actionability and DECIDE/USE proofs at the retained occurrence boundary. Immutable before/after comparison shows only decision fields `history`, `record`, `recorded_choice`, `stage` and E2-DECIDE's status change. Decision history gains DECISION_RECORDED; E2-DECIDE changes ACTIONABLE to COMPLETED. Knowledge, entities, predicates, Action definitions, root/slot and typed-proof domains remain unchanged. Root and slot remain UNRESOLVED.

The [term-by-term correspondence](qualification/E2_P05_A05_ALTERNATE_NATIVE_EVIDENCE_1/END-acceptance-mapping.json) classifies all fourteen required native witness terms. Native type/payload/record binding, enrollment/position and authority relationships match directly. Event identity, choice/dossier context, parent, pre/post-state, ledger/context/provenance and local ordering use only the exact semantic equivalence permitted by the selected dossier. No required local term mismatches.

{limits['PREEXISTING_GRANT_LIMITATION']}

{limits['ORIGINAL_PREFIX_LIMITATION']}

{limits['A06_LIMITATION']}

## END, N12 and N13

The explicit mapping is:

```text
Retained P03 event planner-event-v1:9f00d563a015969d02179c7a991d2efec97b763448fbc27c34e7bd634d36a728
  -> E2-A05.authorized_alternate_native_recorded_decision_event_ancestry
  -> E2-A05.recorded_decision_event_ancestry, under AUTHORIZED_ALTERNATE_NATIVE_EVIDENCE
```

The [mapping](qualification/E2_P05_A05_ALTERNATE_NATIVE_EVIDENCE_1/END-acceptance-mapping.json) preserves native source identities. Original A05 event and parent identities remain null/unknown. It neither splices this event into original A04→A05 history nor claims the original T03 choice/issuer-trust-root envelope. It closes one authorized END input term, leaving full [E2-END](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:467) acceptance unresolved.

| Mapping | Independent assurance checks | Result |
|---|---|---|
| [N12](qualification/E2_P05_A05_ALTERNATE_NATIVE_EVIDENCE_1/N12-mapping.json) | Actual enclosing native event/result; ledger and Snapshot continuity; exact retained decision record/completion; no fabricated result/event/knowledge | PASS |
| [N13](qualification/E2_P05_A05_ALTERNATE_NATIVE_EVIDENCE_1/N13-mapping.json) | Actual typed result and accepted choice, independent choice/dossier/issuer/provenance, independent DECIDE/USE queries, unchanged knowledge/root/slot/authority domains, preserved historical and grant limits | PASS |

These evaluate the scoped assurance behind [N12](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:383) and [N13](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:397) separately. N13 is not inferred from N12. They do not claim a newly executed complete P05 negative suite.

## Qualification and frontier

**26/26 [sealed mapping negatives](qualification/E2_P05_A05_ALTERNATE_NATIVE_EVIDENCE_1/negative-results.json) fail closed**, including every requested event/choice/context/parent/ledger/position/scope/lineage/provenance mismatch; report/Snapshot substitution; source substitution; historical alias/new identity; removed grant limitation; falsely closed original prefix or A06; assumed N12/N13; wrong scope subject/dossier; scope used as DECIDE authority; omitted N13 terms; and waived full-END gap. Each uses an isolated in-memory mapping proposal; pinned native events are untouched. These are acceptance-mapping controls, not new native execution/admission tests.

**12/12 [fresh readers](qualification/E2_P05_A05_ALTERNATE_NATIVE_EVIDENCE_1/fresh-reader-determinism.json) pass**: three independent interpreters per seed 0, 1, 7, 101, using native, reversed and rotated codec-declared unordered collections plus object-key changes. Causal event history, decision history and ordered policy rules remain ordered. Readers independently load native sources, check identities/ancestry, query authority predicates and reconstruct the same mapping. All native identities and the complete mapping agree; comparison identity is `{summary['mapping_comparison_identity']}`. This identity belongs only to qualification metadata. No new writer, transaction or native decision replay is required or performed.

The [versioned P05 graph](qualification/E2_P05_A05_ALTERNATE_NATIVE_EVIDENCE_1/P05-binding-rerun.json) changes only the A05 stage row. A03/A04 replacements and all other rows remain exactly as retained. Bound-row references and P05 readiness pins are rechecked. It counts twelve BOUND rows and leaves only A06 unbound. The [readiness check](qualification/E2_P05_A05_ALTERNATE_NATIVE_EVIDENCE_1/P05-readiness-checks.json) preserves the passing P04 initial oracle by exact unchanged inputs, the sixteen sealed P05 negative expectations and persistence/replay obligations. P05/P06 remain unexecuted.

## Preservation and report

[Verification](qualification/E2_P05_A05_ALTERNATE_NATIVE_EVIDENCE_1/verification.json) compares all pre-existing files to the pre-work hash baseline, including native runtime and frozen E1, and records `git diff --check`. Capture/materialization, result application, event append, native save/restore and replay entry points were barred; zero calls occurred. Only new qualification metadata, reader/control scripts and these reports were written. No source event, prior dossier, graph, contract, choice or grant was modified.

```text
WORK_PACKAGE = E2-P05-A05-ALTERNATE-NATIVE-EVIDENCE
RESULT = PASS
SELECTED_OPTION = AUTHORIZE_P05_A05_ALTERNATE_NATIVE_EVIDENCE
SCOPE_AUTHENTICATION = PASS
ALTERNATE_EVENT_ID = {mapping['native_event_id']}
ALTERNATE_EVENT_ORIGINAL_ROLE = P03
ALTERNATE_EVENT_ANCESTRY = PASS
RECORDED_DECISION_BINDING = PASS
A05_SEMANTIC_CORRESPONDENCE = PASS
ORIGINAL_A05_HISTORICAL_ANCESTRY = UNPROVEN
P03_EVENT_IS_ORIGINAL_A05_EVENT = NO
HISTORICAL_RECONSTRUCTION = NO
NEW_A05_OCCURRENCE_CREATED = NO
NEW_HUMAN_CHOICE_CREATED = NO
NEW_NATIVE_GRANT_ISSUED = NO
PREEXISTING_GRANT_LIMITATION = PRESERVED; EXISTENCE/USE_RELATIONSHIP_ONLY; ISSUANCE_NOT_PROVEN
ORIGINAL_PREFIX_LIMITATION = UNPROVEN/UNRESOLVED; NO_FULL_END_WAIVER
A06_LIMITATION = UNBOUND; NOT_AUTOMATICALLY_SATISFIED
END_MAPPING = PASS_FOR_A05_ALTERNATE_TERM_ONLY
N12_MAPPING = PASS
N13_MAPPING = PASS
NEGATIVE_SUITE = PASS; 26/26_MAPPING_CONTROLS
DETERMINISM = PASS; 12_FRESH_READERS; SEEDS_0_1_7_101
E2_A05_RECORDED_DECISION_EVENT_ANCESTRY = PASS
BINDING_CLASSIFICATION = AUTHORIZED_ALTERNATE_NATIVE_EVIDENCE
P05_BOUND_STAGE_INPUTS = 12 / 13
P05_NEXT_MISSING_INPUT = E2-A06.request_wait_event_trace
P05_EXECUTION_READY = NO
E2_P05_READY = YES
P05_EXECUTED = NO
P06_EXECUTED = NO
E2_P04_RESULT = PASS
ORIGINAL_A03_HISTORICAL_OCCURRENCE = UNPROVEN
ORIGINAL_A04_HISTORICAL_ANCESTRY = UNPROVEN
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO
RUNTIME_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
NEXT_PACKAGE = E2-P05-A06-REQUEST-WAIT-EVENT-TRACE-RECOVERY
```

[Machine-readable result]({PREFIX.split('/')[-1] + NAME + '.json'}) contains all typed-source pointers, the native payload, exact context, independent mappings, exclusions and evidence hashes.
'''
    (ROOT / (PREFIX + NAME + '.md')).write_text(md)
    print(json.dumps({'result': 'PASS', 'bound': count, 'total': 13,
                      'next_missing_input': remaining[0], 'P05_EXECUTION_READY': 'NO'}))


if __name__ == '__main__':
    main()
