"""Record the qualified documentary interface without altering earlier bindings."""
from copy import deepcopy
import json
import subprocess
from contract import (ROOT, OUT, DOCS, PREFIX, CLOSURE, PRIOR, COMPOSITE, INPUT,
    HISTORICAL, FIELDS, ROLE_FIELDS, read, sha, ref, at, save, equal, qid, source_specs)


def main():
    p = read(OUT / 'END-projection.json')
    mf = read(OUT / 'invocation-input-manifest.json')
    preflight = read(OUT / 'preflight.json')
    negatives = read(OUT / 'negative-results.json')
    determinism = read(OUT / 'determinism.json')
    equal('qualified PC02 consumer interface', preflight['PC02_END_INTERFACE'], 'PASS')
    equal('negative qualification', negatives['RESULT'], 'PASS')
    equal('fresh reader reconstruction', determinism['RESULT'], 'PASS')
    body = p['projection']
    recovered = body['recovered_contract']
    contract_report = {'PC02_ID': 'E2-PC02', 'PC02_PURPOSE': recovered['PURPOSE'],
        'PC02_SOURCE_TYPE': [x['source_type'] for x in body['primary_sources']],
        'PC02_REQUIRED_SOURCE': body['primary_sources'],
        'END_CONSUMER': recovered['CONSUMER'], 'END_INPUT': recovered['INTERFACE_ID'],
        'PROCESS': recovered['PROCESS'], 'SATISFACTION_RULE': recovered['REQUIRED_OUTPUT'],
        'REQUIRED_INPUT': recovered['REQUIRED_INPUT'], 'CURRENTNESS_RULE': recovered['CURRENTNESS'],
        'SCOPE': recovered['SCOPE'], 'LINEAGE': recovered['LINEAGE'], 'PROVENANCE': recovered['PROVENANCE'],
        'exact_recovered_contract': recovered, 'no_contract_reinterpretation': True}
    save('recovered-consumer-contract.json', contract_report)
    save('qualified-process-binding.json', {'RESULT': 'PASS', 'consumer': INPUT,
        'process_identity': body['process']['identity'], 'projection_identity': p['identity'],
        'manifest_identity': mf['identity'], 'process_edges': mf['manifest']['process_edges'],
        'materialized_binding': ref(OUT / 'process-binding.json'),
        'preflight': ref(OUT / 'preflight.json'), 'PROCESS': preflight['terms']['PROCESS'],
        'INPUT_MANIFEST': preflight['terms']['INPUT_MANIFEST'], 'native_mutations': False})
    views = {v['view']['field']: v for v in body['native_views']}
    s = read(ROOT / source_specs()[2]['source']['path'])['bundle']['current']
    dossier = s['decisions'][0]['dossier']
    roles = []
    for role in sorted(ROLE_FIELDS):
        record = {'role': role, 'original_declaration': next(x for x in body['original_fixture']['source_roles'] if x['role'] == role),
            'END_consumer': INPUT, 'process': body['process']['identity'],
            'source_view_identities': [views[field]['identity'] for field in ROLE_FIELDS[role]],
            'comparison': 'Exact pinned current native semantics against the independently sealed source views',
            'historical_PC02_source_reused_as_P04_permission': False}
        if role == 'DOSSIER':
            record['native_subject'] = s['decisions'][0]['action']
            record['current_dossier_provenance'] = dossier['provenance']
            record['original_checks'] = body['original_fixture']['dossier']['checks']
            record['retained_current_checks'] = [x['kind']['value'] for x in dossier['checks']]
            record['typed_dossier_outcomes'] = [x for x in s['validation_instances'] if x['predicate']['value'].startswith('E2-CHECK-')]
            record['descriptive_checks'] = ['ASSUMPTIONS_CONSEQUENCES', 'DOWNSTREAM_QUALIFICATION', 'NO_INVENTED_FACTS']
            record['native_boundary'] = 'gates.decision_readiness; existing supported check contract unchanged'
        elif role == 'GRANT':
            record['native_entity'] = next(x for x in s['entities'] if x['id']['value'] == 'E2-GRANT')
            record['native_predicate'] = next(x for x in s['predicates'] if x['id']['value'] == 'E2-USE-AUTHORITY')
            record['consumer_target_distinction'] = 'Original fixture target names E2-REENTER consumer; native grant targets the exact mapping subject checked by its native predicate'
            record['native_authority_in_current_REENTER_definition'] = next(x for x in s['actions'] if x['id']['value'] == 'E2-REENTER').get('authority')
            record['limitations'] = 'Retained pre-existing grant and bounded applicability; no reissuance, stronger authority assurance or new Action authority inferred'
        elif role in ('ROOT_PROOF', 'SLOT_PROOF'):
            contract = next(x for x in s['proof_contracts'] if x['proof_type']['value'] == role)
            record['native_contract'] = contract
            record['native_source'] = next(x for x in s['entities'] if x['identity'] == contract['provenance']['identity'] and x['kind']['value'] == 'SOURCE')
            record['native_semantic_authority'] = next(x for x in s['entities'] if x['id'] == contract['authority'])
            record['currentness'] = 'Exact active contract, separate supported source and semantic authority, native support fingerprint and current usable retained proof'
            record['historical_baseline_fixture_authority_applied_to_P04'] = False
        elif role == 'EXTERNAL_ROUTE':
            record['native_gate'] = s['external_gates'][0]['id']
            record['native_requirement'] = s['evidence_requirements'][0]
            record['retained_route'] = s['external_gates'][0]['resolution_contracts']
            record['retained_stage'] = s['external_gates'][0]['stage']
            record['fixture_variants'] = body['original_fixture']['external_routes']
            record['current_native_route_count'] = len(s['external_gates'][0]['resolution_contracts'])
            record['current_route_acquisition_applicability'] = False
            record['route_support_current'] = True
            record['no_new_gate_or_occurrence_from_fixture_variant'] = True
        else:
            record['native_ingress'] = s['ingress_contracts']
            record['native_ATTEST_entities'] = [x for x in s['entities'] if any(y['value'] == 'ATTEST' for y in x.get('permissions', []))]
            record['native_receipt'] = s['receipt_admissions']
            record['receipt_validation_proof_resume_separation'] = body['original_fixture']['invariants'][2:6]
        roles.append(record)
    root = next(x for x in s['proof_contracts'] if x['proof_type']['value'] == 'ROOT_PROOF')
    slot = next(x for x in s['proof_contracts'] if x['proof_type']['value'] == 'SLOT_PROOF')
    root_body, slot_body = (json.loads(x['provenance']['excerpt']) for x in (root, slot))
    save('contract-correspondence.json', {'RESULT': 'PASS', 'role_inventory': roles,
        'all_consumed_native_fields': FIELDS, 'qualification_declaration_vs_native_instance_kept_separate': True,
        'root_slot_independence': {'source_content_identities_differ': root['provenance']['identity'] != slot['provenance']['identity'],
            'propositions_differ': root['proposition'] != slot['proposition'],
            'origin_identities_differ': root_body['provenance_origin'] != slot_body['provenance_origin'],
            'native_semantic_authority_identities_differ': root['authority_identity'] != slot['authority_identity'],
            'root_origin': root_body['provenance_origin'], 'slot_origin': slot_body['provenance_origin'],
            'native_configuration_and_currentness_validation': 'PASS; preflight installation/typed-proof primitives'},
        'no_new_semantics': True, 'derived_from_fixed_oracle_matched_inventory': True})
    previous = read(PRIOR / 'six-interface-frontier.json')
    old_records = previous['interfaces']
    equal('unchanged entry frontier', previous['END_INTERFACES_BOUND'], 1)
    equal('closed PC01 source binding', previous['PC01_END_INTERFACE'], 'PASS')
    records = deepcopy(old_records)
    current = records[1]
    for dimension in ('CONSUMER_BINDING', 'PROCESS_BINDING', 'CURRENTNESS'):
        current['STATUS'][dimension] = 'PASS'
    current['STATUS_EXPLANATIONS'].update({
        'CONSUMER_BINDING': 'Exact independent-oracle-qualified PC02 native/fixture projection attached to END dependency 1',
        'PROCESS_BINDING': 'Exact concrete read-only process identity/input/invocation manifest independently qualified',
        'CURRENTNESS': 'Pinned historical qualification roles and supported current native definition versions at the stated consumer boundary'})
    current['first_failure_dimensions'] = []
    current['current_interface_oracle'] = 'PASS'
    current['current_consumer_projection'] = ref(OUT / 'END-projection.json')
    current['current_invocation_manifest'] = ref(OUT / 'invocation-input-manifest.json')
    current['current_process_binding'] = ref(OUT / 'qualified-process-binding.json')
    current['current_preflight'] = ref(OUT / 'preflight.json')
    current['projection_identity'] = p['identity']
    current['manifest_identity'] = mf['identity']
    current['current_binding_note'] = 'Qualified documentary projection only; native versions/history/permissions unchanged'
    equal('PC01 earlier binding record unchanged', records[0], old_records[0])
    equal('remaining four interface records unchanged', records[2:], old_records[2:])
    bound = sum(all(value in ('PASS', 'NOT_REQUIRED') for value in row['STATUS'].values()) for row in records)
    equal('PC02-only frontier closure', bound, 2)
    next_source = records[2]['SOURCE'] + ' -> E2-END'
    frontier = {'RESULT': 'PASS_FRONTIER_REEVALUATION_ONLY', 'previous_frontier': ref(PRIOR / 'six-interface-frontier.json'),
        'interfaces': records, 'PC01_END_INTERFACE': 'PASS', 'PC02_END_INTERFACE': 'PASS',
        'END_INTERFACES_BOUND': 2, 'END_INTERFACE_COUNT': 6, 'NEXT_UNRESOLVED_INTERFACE': next_source,
        'P05_STAGE_BINDINGS': '13/13', 'FOUR_SEMANTIC_BRIDGES': 'PASS', 'AGGREGATE_N12': 'PASS', 'AGGREGATE_N13': 'PASS',
        'COMPOSITE_P05_END_QUALIFICATION': 'FAIL', 'P05_EXECUTION_READY': 'NO',
        'remaining_four_records_unchanged': True, 'PC01_record_unchanged': True,
        'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO'}
    save('six-interface-frontier.json', frontier)
    baseline = read(OUT / 'baseline.json')['file_sha256']
    changed = [name for name, digest in baseline.items() if not (ROOT / name).is_file() or sha(ROOT / name) != digest]
    equal('all prior artifacts byte preserved', changed, [])
    check = subprocess.run(['git', 'diff', '--check'], cwd=str(ROOT), capture_output=True, text=True)
    equal('git diff check', check.returncode, 0)
    save('preservation.json', {'RESULT': 'PASS', 'prior_file_count': len(baseline), 'prior_files_modified': [],
        'runtime_files_unchanged': sum(name.startswith('adapter/planner/') for name in baseline),
        'E1_files_unchanged': sum(name.startswith('docs/experiments/E1/') for name in baseline),
        'NATIVE_STATE_CHANGED': 'NO', 'INSTALL_EVENTS': 0, 'NEW_AUTHORITIES': 0, 'RUNTIME_MODIFIED': 'NO',
        'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO', 'N_REAL_SATISFIED': 'NO',
        'E1_ARTIFACTS_MODIFIED': 0, 'PRODUCTION_EFFECT': 'NO', 'git_diff_check': 'PASS',
        'closed_stage_bridge_aggregate_and_PC01_artifacts_unchanged': True,
        'historical_labels': HISTORICAL, 'CONTINUOUS_ORIGINAL_A01_A13_LINEAGE_PROVEN': 'NO'})
    evidence = {name: ref(OUT / file) for name, file in {
        'source_pins': 'source-pins.json', 'source_semantics': 'source-semantics-inventory.json',
        'contract_correspondence': 'contract-correspondence.json', 'projection': 'END-projection.json',
        'invocation_manifest': 'invocation-input-manifest.json', 'process_binding': 'qualified-process-binding.json',
        'recovered_contract': 'recovered-consumer-contract.json',
        'independent_oracle': 'expected-oracle.json', 'manifest_oracle': 'expected-manifest-oracle.json',
        'oracle_seal': 'oracle-seal.json', 'preflight': 'preflight.json', 'negative_plan': 'negative-plan.json',
        'negatives': 'negative-results.json', 'determinism': 'determinism.json',
        'frontier': 'six-interface-frontier.json', 'preservation': 'preservation.json'}.items()}
    result = {'WORK_PACKAGE': 'E2-P05-PC02-END-BINDING', 'RESULT': 'PASS',
        'PC02_CONTRACT': contract_report, 'PC02_SOURCE': body['primary_sources'],
        'PC02_SOURCE_QUALIFICATION': 'PASS; retained PC02 preparation scope, not future execution PASS',
        'PC01_BINDING_PATTERN_REUSABLE': 'YES', 'END_CONSUMER': body['consumer'],
        'END_PROCESS': body['process'], 'END_PROJECTION': evidence['projection'],
        'PROJECTION_IDENTITY': p['identity'], 'INVOCATION_INPUT_MANIFEST': evidence['invocation_manifest'],
        'MANIFEST_IDENTITY': mf['identity'], 'MANIFEST_INPUT_COUNT': len(mf['manifest']['inputs']),
        'CURRENTNESS': 'PASS; exact current native definitions/source/policy support, bounded historical fixture role and completed-route applicability distinguished',
        'SCOPE': 'PASS; E2-QUALIFICATION-ONLY documentary acceptance',
        'LINEAGE': 'PASS; original baseline and current P04 contexts retained separately',
        'PROVENANCE': 'PASS; exact native selectors/source bytes, content identities and existing governed history',
        'NATIVE_VALIDATION': 'PASS; unchanged model, typed records, identities, policy/source pins, authorities and supported definition versions',
        'END_INTERFACE_PREFLIGHT': preflight['terms'],
        'NEGATIVE_SUITE': 'PASS; 22/22 PC02-specific isolated controls',
        'DETERMINISM': 'PASS; 36 fresh readers, seeds 0,1,7,101 and original/reversed/rotated native set presentations',
        'PC02_END_INTERFACE': 'PASS', 'PC01_END_INTERFACE': 'PASS',
        'END_INTERFACES_BOUND': 2, 'END_INTERFACE_COUNT': 6, 'NEXT_UNRESOLVED_INTERFACE': next_source,
        'P05_STAGE_BINDINGS': '13/13', 'FOUR_SEMANTIC_BRIDGES': 'PASS', 'AGGREGATE_N12': 'PASS', 'AGGREGATE_N13': 'PASS',
        'COMPOSITE_P05_END_QUALIFICATION': 'FAIL', 'P05_EXECUTION_READY': 'NO',
        'NEXT_PACKAGE': 'E2-P05 PC03 -> END QUALIFICATION INTERFACE / PROCESS BINDING CLOSURE',
        'NATIVE_STATE_CHANGED': 'NO', 'INSTALL_EVENTS': 0, 'NEW_AUTHORITIES': 0, 'RUNTIME_MODIFIED': 'NO',
        'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO', 'N_REAL_SATISFIED': 'NO',
        'CONTINUOUS_ORIGINAL_A01_A13_LINEAGE_PROVEN': 'NO', 'E1_ARTIFACTS_MODIFIED': 0,
        'PRODUCTION_EFFECT': 'NO', 'GIT_DIFF_CHECK': 'PASS', 'evidence': evidence,
        'verification': {'path': str((OUT / 'verification.json').relative_to(ROOT))}}
    result.update(HISTORICAL)
    result_path = DOCS / (PREFIX + 'E2_P05_PC02_END_BINDING_1.json')
    equal('report not already authored', result_path.exists(), False)
    result_path.write_text(json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + '\n')
    checks = preflight['native_validation']
    versions = checks['definition_currentness']
    field_table = '\n'.join('| ' + view['view']['field'] + ' | ' + str(len(view['view']['members'])) +
        ' | ' + ', '.join(sorted(set(x['native_type'] for x in view['view']['members']))) + ' |' for view in body['native_views'])
    version_table = '\n'.join('| ' + x['type'] + ' | ' + str(x['sequence']) + ' | ' +
        ('Current supported definition' if x['consumer_applicable_now'] else 'Supported history; acquisition inapplicable after completion') + ' |' for x in sorted(versions, key=lambda x: x['sequence']))
    text = f'''# E2-P05 PC02 → END qualification binding materialization 1

**RESULT = PASS. PC02_END_INTERFACE = PASS.** The recovered PC02 contract is bound to END dependency 1 through a qualification projection, explicit read-only process and concrete input/invocation manifest. The independently sealed projection and manifest oracles, all nine interface terms, native structural/currentness checks, **22/22 negatives** and **36 fresh-reader reconstructions** pass. **END_INTERFACES_BOUND = 2/6**. The next unresolved interface is **E2-PC03 → E2-END**; P05 remains not ready and unexecuted.

The [machine companion](DETERMINISTIC_PLANNER_V0_1_E2_P05_PC02_END_BINDING_1.json) links exact [source pins](qualification/E2_P05_PC02_END_BINDING_1/source-pins.json), the complete [native source inventory](qualification/E2_P05_PC02_END_BINDING_1/source-semantics-inventory.json), [contract correspondence](qualification/E2_P05_PC02_END_BINDING_1/contract-correspondence.json), [projection](qualification/E2_P05_PC02_END_BINDING_1/END-projection.json), [manifest](qualification/E2_P05_PC02_END_BINDING_1/invocation-input-manifest.json), [process binding](qualification/E2_P05_PC02_END_BINDING_1/process-binding.json) and qualification evidence.

## Recovered contract and reuse boundary

The authoritative contract is [END_INTERFACE_CLOSURE_1](qualification/E2_P05_END_INTERFACE_CLOSURE_1/six-interface-inventory.json), `/interfaces/1`, consumed unchanged. PC02 supplies independently source-bound proof, authority, decision and external-lifecycle contracts. The source types are historical fixture/oracle declarations and later P04 governed typed contracts. END input is **{INPUT}**, consumer is the **E2-END experiment acceptance-case comparison/runner harness**, and the declared process is a **read-only consumer projection of qualified typed source/authority/proof/lifecycle contracts**. Native consumers keep their own bounds. Required output is an exact current END projection and process/input binding with independently reviewed comparison obligations; readiness is not future execution PASS.

The existing PC01 pattern is reusable **only for the documentary binding mechanism**: retained sources → consumer projection → invocation/input manifest → explicit process edge → END. PC02 consumes its own six source roles, dossier, proof, authority, gate, receipt and support semantics. No PC01 six-Action-only acceptance criterion is imposed on this interface. No new native adapter, INSTALL, binding object or grant is needed.

The consumer pins original PC04 dependency 1 and sealed edge `qualification-END-edge-v1:e45ec4bf691372c7726d213cd9de9fa07e5c82688effb94880150e0826df3d10`, under the unchanged composite graph and qualified acceptance overlay. Qualification scope remains E2-QUALIFICATION-ONLY; no native END Action/slot or permission is created.

## Exact sources and semantic inventory

Exactly the three sources already named by interface recovery are selected:

| Source / identity | Retained use |
|---|---|
| PC02_FIXTURES, raw-file-sha256:1610f526a7f055f759355ce1cde4abee5b6780ec73eb3358c57b7a9738bda248 | Original E2-CANONICAL-BASELINE-1 qualification declarations: six roles, nine dossier checks, authority/applicability separation, distinct proofs, both absence-route variants and 23 clause-level case contracts |
| PC02_VALIDATION, raw-file-sha256:7b0639898a404816b836c74b3f5bbea855e43adac66f39b4ab726b8245ae4395 | Already-established preparation-scope PASS, 13 positive/10 negative cases; no producer rerun and no lifecycle occurrence inferred |
| P04 canonical target, planner-bundle-v1:3e36b39884db3ea4ecaea0b2371d2af910c34b984fc69c5d3e2b42bc26ce13c2 | Retained native source/definition/authority contracts and actual canonical support/history |

The P04 native Snapshot is `planner-snapshot-v1:046fdc270a0060503729151368a68672f76af122830b86e65d372e6bc5d7dea4`, context **E2-QUALIFICATION-ONLY / E2-P03-PROSPECTIVE-QUALIFICATION-1 / E2-P03-PROSPECTIVE-GENERATION-1**, tick 0. The historical PC02 baseline is neither retagged nor promoted to P04 authority. Original preparation fixtures are documentary contracts; where native evidence is required, the retained P04 typed representation supplies it.

Every consumed native member is recorded with immutable source selector, native type/key, complete native value, exact Snapshot/context and a separate qualification view comparison identity. The inventory includes:

| Native field | Members | Types |
|---|---|---|
{field_table}

The six role correlations remain explicit:

- **DOSSIER:** E2-DECIDE, exact DecisionDossier, required facts and nine named checks. Six supported dossier predicates have separate typed PASS values; the seventh ValidationInstance belongs to external validation. The three descriptive checks remain rehomed metadata under the already-qualified native contract. No inline check outcomes are fabricated.
- **GRANT:** retained E2-GRANT, native AUTHORITY_IDENTITY and independently evaluated E2-USE-AUTHORITY predicate. The original fixture names E2-REENTER as its consumer; the native grant targets its exact mapping subject. Current Action fields and the pre-existing-grant limitation remain unchanged; no missing Action authority field is filled in.
- **SLOT_PROOF:** exact `planner-TypedProofContract-v1:02b2c4c3f0faf45a9d111a27d8cdec7252a8f3e2156a8fd29b2e1cf6d2510315`, E2-SLOT-PROPOSITION, actual E2-K-REENTER support, E2-SLOT target and separately supported slot source/semantic authority.
- **ROOT_PROOF:** exact `planner-TypedProofContract-v1:10f96412ca6b0096f8fdf83878b123728946d18049e7ce2d432d8b65512a62ec`, E2-ROOT-PROPOSITION, E2-SLOT support, E2-ROOT target and independent root source/semantic authority. Source content, proposition and provenance origin differ from the slot source. SLOT_PROOF cannot substitute for ROOT_PROOF.
- **EXTERNAL_ROUTE:** exact E2-GATE, E2-EXTERNAL-REQUIREMENT, native governed route, unresolved-rule acquisition contract and later receipt/validation/support/reentry bindings. Both historical known-rule and governed-unknown fixture variants remain separately qualified contracts; no second native P04 gate or past occurrence is invented.
- **ATTESTOR:** exact installed authentication entities/predicates, ingress contract, producer/target correspondence and actual receipt references. Requirement, receipt, validation, obligation Proof and resume remain separate terms.

The projection also preserves every original separation invariant and clause-level negative expectation. Retained proof instances, results, Knowledge and completed states are observed from the original native bundle; this mapping neither creates them nor replaces their historical identities.

## Currentness and native validation

[Independent preflight](qualification/E2_P05_PC02_END_BINDING_1/preflight.json) uses unchanged native type/model validation, Snapshot/event identities, source/policy pin checks, installation descriptors/authority applicability, supported definition currentness, dossier readiness and typed proof usability. The full retained model passes, and all inspected bundle/state bytes stay exact. Twenty retained events are checked by native event comparison identity, parent/pre-state continuity and ledger position; no historical operation is replayed or reexecuted.

| Governed definition | Native installation position | Consumer role at P04 target |
|---|---|---|
{version_table}

Eight active definition versions pass native currentness. The route’s native support remains current while its acquisition consumer is inapplicable after gate completion; that expected distinction passes. No route is reactivated and historical completion supplies no new execution permission. All nine installation authorities remain exact bounded references; their events and pre-install/post-install identities are read from retained history, never applied again. Concrete SLOT/ROOT contract installations at positions 16/18 retain the actual governed versions expected by END.

SOURCE, CONSUMER, PROJECTION, PROCESS, INPUT_MANIFEST, CURRENTNESS, SCOPE, LINEAGE and PROVENANCE each pass independently. This establishes current documentary END consumption of supported source contracts and history at the specified checkpoint, while preserving separate historical/current source roles.

## Independent oracles, projection and invocation

The [oracle seal](qualification/E2_P05_PC02_END_BINDING_1/oracle-seal.json), [expected projection](qualification/E2_P05_PC02_END_BINDING_1/expected-oracle.json), [expected manifest](qualification/E2_P05_PC02_END_BINDING_1/expected-manifest-oracle.json) and [negative plan](qualification/E2_P05_PC02_END_BINDING_1/negative-plan.json) precede materialization/preflight. The oracle reads pinned raw source JSON and recovered consumer declarations independently; it never calls the typed decoder, projection builder or native transition. Its expectations are not chosen from materializer output.

```text
PROJECTION_IDENTITY = {p['identity']}
MANIFEST_IDENTITY = {mf['identity']}
PROCESS_IDENTITY = {body['process']['identity']}
```

These qualification identities bind exact source/qualification/native view identities, consumer, process code/contracts, semantics, scope, lineage and provenance. They are not native ledger, Snapshot, event, grant or ActionResult identities. Native SET_FIELDS collections normalize under unchanged codec semantics; ordered ancestry and positional support bindings remain ordered.

The manifest has **36 concrete input terms**: three retained primary sources; twenty-four exact native semantic views; and nine comparison/process/context inputs. Every term has an expected type, source artifact/selector and identity, exact semantic view/key relationship, projection, consumer, process, scope, lineage, provenance and currentness role. The independent oracle is **COMPARISON_ONLY**, excluded from Planner execution operands. The process pins its interpreter/code/native primitives and concrete seal/materialization/preflight/readers; no field or argument is TBD.

Process edges are explicit: **PC02 retained contracts/native sources → END-specific qualification projection → invocation/input manifest → END dependency 1**. Only these documentary artifacts are persisted. Fresh readers reconstruct them from existing pinned native sources; no new PersistenceBundle or state transition is created.

## Negative qualification, determinism and frontier

All **22/22** [isolated negatives](qualification/E2_P05_PC02_END_BINDING_1/negative-results.json) reject: wrong native source/qualification, missing/extra primary source, wrong source identity/proposition, consumer/process mismatch, missing/extra manifest input, wrong projection or current proof-contract version, wrong scope/lineage/provenance, stale support, report-for-native substitution, order-sensitive identity, slot-for-root substitution, old baseline authority/context reused in P04, receipt-for-validation substitution and readiness upgraded to execution permission. Mutated candidates may be rehashed; the fixed independent oracle still rejects them. Sources and the successful mapping stay unchanged.

[Determinism](qualification/E2_P05_PC02_END_BINDING_1/determinism.json) passes **36 fresh processes**: seeds 0,1,7,101 × three readers × original/reversed/rotated declared-set presentations. Readers lack writer memory and reconstruct identical full projection/manifest identities and all interface terms. Native event order is never permuted. Mutation barriers show zero execution, replay, result application, commit or installation calls.

The [six-interface frontier](qualification/E2_P05_PC02_END_BINDING_1/six-interface-frontier.json) overlays only PC02’s missing consumer/process/currentness dimensions. **PC01 stays PASS; PC02 is PASS; 2/6 interfaces are bound.** PC01’s previous record and the four remaining interface records are byte-equivalent values to the prior frontier. Next failure is **{next_source}**; it is inventoried but not resolved here. Thirteen stage bindings, four bridges and aggregate N12/N13 remain closed without reevaluation or remapping. Composite END remains FAIL and P05_EXECUTION_READY remains NO.

## Preservation

[Preservation](qualification/E2_P05_PC02_END_BINDING_1/preservation.json) and [final verification](qualification/E2_P05_PC02_END_BINDING_1/verification.json) check all **{len(baseline)}** pre-existing workspace files, all pinned selectors/code/data identities, unchanged native artifacts/history/authorities and frozen E1. P03 historical correspondence and original A03/A04/A05/A06 historical witness labels remain UNPROVEN. No continuous original A01–A13 lineage is claimed. P05/P06 remain unexecuted; N_REAL remains unsatisfied.

```text
WORK_PACKAGE = E2-P05-PC02-END-BINDING
RESULT = PASS
PC02_SOURCE_QUALIFICATION = PASS (PREPARATION SCOPE)
PC01_BINDING_PATTERN_REUSABLE = YES
NATIVE_VALIDATION = PASS
NEGATIVE_SUITE = PASS (22/22)
DETERMINISM = PASS (36 FRESH READERS)
PC02_END_INTERFACE = PASS
END_INTERFACES_BOUND = 2
END_INTERFACE_COUNT = 6
NEXT_UNRESOLVED_INTERFACE = E2-PC03 -> E2-END
P05_STAGE_BINDINGS = 13/13
FOUR_SEMANTIC_BRIDGES = PASS
AGGREGATE_N12 = PASS
AGGREGATE_N13 = PASS
COMPOSITE_P05_END_QUALIFICATION = FAIL
P05_EXECUTION_READY = NO
NATIVE_STATE_CHANGED = NO
INSTALL_EVENTS = 0
NEW_AUTHORITIES = 0
RUNTIME_MODIFIED = NO
P05_EXECUTED = NO
P06_EXECUTED = NO
N_REAL_SATISFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```
'''
    result_path.with_suffix('.md').write_text(text)
    print(json.dumps({'RESULT': 'PASS', 'PC02_END_INTERFACE': 'PASS', 'interfaces_bound': '2/6',
        'next_interface': next_source, 'preserved_prior_files': len(baseline), 'P05_EXECUTION_READY': 'NO'}))


if __name__ == '__main__':
    main()
