"""Recover/seal P05 specifications and inventory inputs without executing P05."""
import ast
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOCS = ROOT / 'docs/plans'
OUT = Path(__file__).resolve().parent
PREFIX = 'DETERMINISTIC_PLANNER_V0_1_'


def read(path):
    return json.loads(path.read_text())


def rel(path):
    return path.relative_to(ROOT).as_posix()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, value):
    path = OUT / name
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    return {'path': rel(path), 'raw_sha256': sha(path)}


def doc(name, suffix='json'):
    return DOCS / (PREFIX + name + '.' + suffix)


def main():
    plan_path = doc('CANONICAL_QUALIFICATION_EXPERIMENT_1', 'md')
    matrix_path = doc('CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1', 'md')
    plan_json = doc('CANONICAL_QUALIFICATION_EXPERIMENT_1')
    plan = read(plan_json)
    p05 = next(p for p in plan['packages'] if p['id'] == 'E2-P05')
    p06 = next(p for p in plan['packages'] if p['id'] == 'E2-P06')
    cases = {c['CASE_ID']: c for c in plan['cases']}
    parsed = {}
    case = None
    labels = {'Initial State': 'INITIAL_STATE', 'Operation': 'OPERATION',
              'Expected State': 'EXPECTED_STATE', 'Negative Invariants': 'NEGATIVE_INVARIANTS',
              'Persistence Requirement': 'PERSISTENCE_REQUIREMENT',
              'Determinism Requirement': 'DETERMINISM_REQUIREMENT'}
    for number, line in enumerate(matrix_path.read_text().splitlines(), 1):
        match = re.match(r'^## (E2-[A-Z]+[0-9]*) — (.*)$', line)
        if match:
            case = match.group(1)
            parsed[case] = {'CASE_ID': case, 'PURPOSE': match.group(2),
                            'source': {'path': rel(matrix_path), 'line': number, 'raw_sha256': sha(matrix_path)}}
        match = re.match(r'^\*\*(.*?):\*\* (.*)$', line)
        if match and case and match.group(1) in labels:
            parsed[case][labels[match.group(1)]] = match.group(2)
    assert set(parsed) == set(cases) and len(cases) == 36
    for name, recovered in parsed.items():
        for key in ('PURPOSE',) + tuple(labels.values()):
            assert recovered[key] == cases[name][key], (name, key)
        recovered['contract_status'] = 'AUTHORITATIVE_EXPECTATION_SEALED_NOT_EXECUTED'
        recovered['owner'] = 'E2-P06' if name == 'E2-REVIEW' else (
            'E2-P05' if name in p05['cases'] else 'PRIOR_PACKAGE_OUTPUT_CONSUMED_BY_P05')
    case_file = write('canonical-case-contracts.json', {'schema': 'E2-P05-CANONICAL-CASE-RECOVERY-1',
                     'matrix_json_equality': 'PASS', 'P05_assignment': p05, 'P06_assignment': p06,
                     'cases': [parsed[n] for n in cases], 'P05_EXECUTED': 'NO'})
    inspection = read(OUT / 'target-inspection.json')
    assert inspection['RESULT'] == 'PASS'
    target = inspection['checks']
    native = inspection['current_snapshot']
    expected = read(OUT / 'initial-oracle.json')
    manifests_path = DOCS / 'qualification/E2_P04_CANONICAL_EXECUTION_RETRY_1/checkpoint-manifests.json'
    manifests = read(manifests_path)
    historical = []
    for name, entry in manifests.items():
        path = Path(entry['path'])
        historical.append({'boundary': name, 'bundle_path': rel(path), 'raw_sha256': sha(path),
                           'bundle_id': entry['bundle_id'], 'snapshot_id': entry['state_id'],
                           'head': entry['head'], 'event_count': entry['event_count'],
                           'use': 'P04_HISTORICAL_INPUT_ONLY; no canonical lifecycle resubmission'})
    history_file = write('P04-input-checkpoints.json', historical)
    old_pc03 = read(doc('E2_PC03_FIXTURES'))
    old_p02 = read(doc('E2_P02_RETRY_4_RESULT'))
    early = {'P02_initial_snapshot': old_p02['initial_snapshot'],
             'P02_post_decision_snapshot': old_p02['post_decision_snapshot'],
             'PC03_lineage': old_pc03['lineage'], 'P04_lineage': native['context']['lineage'],
             'P04_initial_completed_actions': inspection['initial_completed_actions'],
             'P04_history_prefix': inspection['historical_prefix_inventory'],
             'old_PC03_post_reentry_oracle': next(p for p in old_pc03['phase_oracle'] if p['phase'] == 'POST_REENTRY'),
             'P04_sealed_post_A12_control': manifests['post-a12']['semantic_oracle']['computation']['control']['value'],
             'classification': 'STATEFUL_BASELINE_INPUTS_NOT_INTERCHANGEABLE',
             'scope': 'P03 prospective acceptance replaced A07/A08 checkpoint fidelity, not E2-END A01-A13 coverage.',
             'first_preparation_blocker': 'E2-END_CURRENT_NATIVE_INPUT_GRAPH_NOT_BOUND',
             'resolution': 'Bind a complete independently authored A01-A13 qualification input graph with its own source/authority/parent contracts. Do not splice earlier P02 history into the prospective P04 ledger or assert original P03 correspondence.'}
    early_file = write('E2-END-input-closure-trace.json', early)
    prior_pin_checks = []
    for name, wanted in read(doc('E2_P01_RETRY_1_RESULT'))['pinned_qualification_set'].items():
        actual = sha(ROOT / name)
        prior_pin_checks.append({'path': name, 'expected': wanted, 'actual': actual, 'pass': actual == wanted})
    assert all(p['pass'] for p in prior_pin_checks)
    old_file = write('P01-preflight-pin-checks.json', {'checks': prior_pin_checks,
                     'historical_preflight_preserved': True,
                     'limit': 'Pin equality does not rebind an earlier baseline to the later prospective lineage.'})

    checkpoint = {
        'P04_TARGET': rel(doc('E2_P04_CANONICAL_TARGET_BUNDLE_1')),
        'POST_A09': next(x['bundle_path'] for x in historical if x['boundary'] == 'post-a09'),
        'POST_A10': next(x['bundle_path'] for x in historical if x['boundary'] == 'post-a10'),
        'POST_A11': next(x['bundle_path'] for x in historical if x['boundary'] == 'post-a11'),
        'POST_A12': next(x['bundle_path'] for x in historical if x['boundary'] == 'post-a12'),
        'PRE_A09': rel(doc('E2_P04_FINAL_PREEXECUTION_CONFIGURATION_BUNDLE_1')),
        'A14': 'docs/plans/qualification/P03_PROSPECTIVE_CHECKPOINT_1/runs/revision-3-a/unknown/checkpoint/bundle-15d6e65c9a65732f7fdd98771582c487267689bc93e6e91dd69ad9d8974c7ea0.json'}
    assert all((ROOT / p).is_file() for p in checkpoint.values())
    seed_map = {'E2-N01': ['A14'], 'E2-N02': ['A14'], 'E2-N03': ['A14','PRE_A09','POST_A09'],
                'E2-N04': ['POST_A09','POST_A10'], 'E2-N05': ['PRE_A09','P04_TARGET'],
                'E2-N06': ['POST_A11'], 'E2-N07': ['POST_A12'],
                'E2-N08': [], 'E2-N09': ['POST_A11'], 'E2-N10': ['P04_TARGET'],
                'E2-N11': ['PRE_A09','POST_A09','POST_A10','P04_TARGET'],
                'E2-N12': [], 'E2-N13': ['POST_A11'], 'E2-N14': ['PRE_A09','POST_A09'],
                'E2-N15': ['POST_A11'], 'E2-N16': ['A14']}
    negatives = []
    for name in p05['cases']:
        if name.startswith('E2-N'):
            item = dict(parsed[name])
            item['seed_inputs'] = [{'role': s, 'path': checkpoint[s], 'raw_sha256': sha(ROOT / checkpoint[s])}
                                   for s in seed_map[name]]
            item['input_classification'] = 'DERIVABLE' if item['seed_inputs'] else 'MUST_MATERIALIZE'
            item['input_limit'] = ('One-dimension isolated candidate mutation from pinned historical inputs; use current native admission, not direct edits to the successful target.'
                                  if item['seed_inputs'] else 'Initial/selected-without-result input is part of the E2-END initial-state binding gap.')
            item['EXPECTED_CASE_RESULT'] = 'PASS_ONLY_IF_REQUIRED_NATIVE_REJECTION_OR_FAIL_CLOSED_STATE_MATCHES_SEALED_CONTRACT'
            item['forbidden'] = ['successful_canonical_target_mutation','new_authority','new_contract_interpretation',
                                 'attacker_rehash_as_trust_anchor','runtime_repair_inside_qualification']
            item['actual_execution'] = 'NOT_EXECUTED'
            negatives.append(item)
    negative_file = write('sealed-negative-oracles.json', {'schema': 'E2-P05-NEGATIVE-ORACLES-1',
                           'expected_cases': 16, 'cases': negatives, 'P05_EXECUTED': 'NO',
                           'full_mutant_bytes': 'NOT_MATERIALIZED; expected contracts sealed before execution',
                           'mutation_domains': old_pc03['case_mutation_rules']})

    inputs = [
        {'id':'CANONICAL_PLAN_AND_MATRIX','classification':'PRESENT_CURRENT','cases':'ALL','evidence':case_file},
        {'id':'P04_CANONICAL_TARGET','classification':'PRESENT_CURRENT','cases':'P05_INITIAL / D01 / END comparison','evidence':rel(OUT/'target-inspection.json')},
        {'id':'P04_BOUNDARY_BUNDLES_AND_ORACLES','classification':'PRESENT_CURRENT','cases':'A09-A13 coverage / N03-N07,N09-N15 / D01','evidence':history_file},
        {'id':'P03_GOVERNED_UNKNOWN_AND_INVALIDATION_FIXTURES','classification':'PRESENT_CURRENT','cases':'A14-A16 / N01-N03,N16','evidence':rel(doc('P03_PROSPECTIVE_CHECKPOINT_QUALIFICATION_1'))},
        {'id':'CURRENT_NATIVE_E2_END_A01_A13_INPUT_GRAPH','classification':'MUST_MATERIALIZE','cases':'END / D01 / N08,N12','evidence':early_file,
         'why':'The current target starts from prospective authored completed-prefix premises; old PC01-PC04 bind a different baseline. No complete native current full-lifecycle binding is established.'},
        {'id':'END_SOURCE_POLICY_AUTHORITY_AND_PARENT_BINDINGS','classification':'DERIVABLE','cases':'END','dependency':'CURRENT_NATIVE_E2_END_A01_A13_INPUT_GRAPH',
         'limit':'Resolve within exact existing semantic scope; changed authority subjects require separate bounded closure, not reuse of historical grants.'},
        {'id':'NATIVE_NEGATIVE_OPERANDS','classification':'DERIVABLE','cases':'N01-N07,N09-N11,N13-N16','evidence':negative_file},
        {'id':'INITIAL_AND_SELECTED_UNEXECUTED_NEGATIVE_OPERANDS','classification':'MUST_MATERIALIZE','cases':'N08,N12','dependency':'CURRENT_NATIVE_E2_END_A01_A13_INPUT_GRAPH'},
        {'id':'D01_DIMENSIONS_AND_READER_ALLOWLIST','classification':'PRESENT_CURRENT','cases':'D01','evidence':rel(doc('E2_PC04_D01'))},
        {'id':'D01_CASE_CHECKPOINT_PROCESS_BINDINGS','classification':'DERIVABLE','cases':'D01','dependency':'CURRENT_NATIVE_E2_END_A01_A13_INPUT_GRAPH'},
        {'id':'BASELINE_CURRENT_NATIVE_CLI_IMPORTER_CONSTRUCTOR_TESTS','classification':'PRESENT_CURRENT','cases':'REG','evidence':rel(OUT/'static-test-inventory.json')},
        {'id':'BASELINE_READ_ONLY_E1_CORPUS_AND_POLICY','classification':'PRESENT_CURRENT','cases':'REG','evidence':'docs/experiments/E1; baseline preservation pins'},
        {'id':'NEGATIVE_EXPECTATIONS','classification':'PRESENT_CURRENT','cases':'N01-N16','evidence':negative_file},
        {'id':'P06_REVIEW_SUBJECT_TEMPLATE','classification':'PRESENT_CURRENT','cases':'P06 gate','evidence':rel(doc('E2_PC04_REVIEW'))},
        {'id':'FUTURE_P05_PASS_LOGS','classification':'OTHER','cases':'P05 exit / P06 gate',
         'why':'Outputs of P05 execution, not circular execution-readiness inputs.'}]
    input_file = write('input-inventory.json', inputs)
    capability_specs = [
        ('CANONICAL_TYPES_O01_RECOMPUTE_SELECTION_CODEC', 'E2_P01_RETRY_1_RESULT', 'Native definitions/complete-model validation; recompute/selector/codec; current tests remain required.'),
        ('NATIVE_EVENT_BEARING_START', 'E2_EVENT_GENESIS_RESULT', 'Qualified G01-G04 capability, where required by the bound END native input graph; never substitute a different historical start.'),
        ('INITIAL_BOUNDED_RESULTS_DOSSIER_DECISION', 'E2_P02_RETRY_4_RESULT', 'Generic supported prefix semantics; exact old stateful fixtures not current END inputs.'),
        ('COLD_RESTORE_SOURCE_INVALIDATION_UNKNOWN', 'P03_PROSPECTIVE_CHECKPOINT_QUALIFICATION_1', 'Qualified source/policy-pinned prospective and unknown checkpoints.'),
        ('ATOMIC_EVIDENCE_AND_RECEIPT', 'EVIDENCE_E07_INGRESS_INTEGRATION_RESULT', 'Typed transient E02 attestation; atomic evidence/receipt path.'),
        ('PERSISTED_VALIDATION_SUPPORT', 'VALIDATION_V02_RESULT', 'Accepted/rejected typed result/support and historical replay.'),
        ('COMPUTED_PROOF_EVENT_C03', 'REENTRY_R05_UNORDERED_PROJECTION_RESULT', 'Unordered input-set semantics; computed Proof/ResumeEligibility; accepted dependent-action event.'),
        ('GOVERNED_DEFINITION_INSTALLATION_ACTION_ADAPTER', 'INSTALLATION_I05_RESULT', 'Qualified bounded INSTALL/REPLACE; no new installation required merely by P05.'),
        ('TYPED_ROOT_SLOT_REEVALUATION_FINISH', 'FINISH_F03_RESULT', 'Qualified typed proof contracts, independent root source and bounded dependency reevaluation.'),
        ('CANONICAL_A09_A13_INTEGRATED_PATH', 'E2_P04_CANONICAL_EXECUTION_RETRY_1_RESULT', 'Actual qualified event-bearing P04 history; preserves two exact deferred installs.')]
    caps = []
    for name, evidence, use in capability_specs:
        path = doc(evidence, 'md')
        assert path.is_file()
        caps.append({'id':name,'classification':'QUALIFIED_AVAILABLE','qualified_evidence':rel(path),
                     'raw_sha256':sha(path),'application_limit':use})
    caps.append({'id':'REG_CURRENT_RUN','classification':'P05_EXECUTION_OUTPUT_NOT_PREPARATION',
                 'existing_programs':rel(OUT/'static-test-inventory.json'), 'current_PASS':'NOT_ASSERTED'})
    cap_file = write('capability-inventory.json', {'new_capability_required':'NONE_ESTABLISHED','capabilities':caps})
    authorities = {
        'P05_EVALUATION':{'class':'NO_NEW_NATIVE_AUTHORITY','status':'AUTHORITY_APPLIES','basis':'Canonical P05 allocation and current user instruction permit recovery; later qualification operates only synthetic isolated inputs.'},
        'P04_HISTORICAL_INSTALL_GRANTS':{'status':'PRESENT_CURRENT_FOR_HISTORICAL_BINDINGS','restriction':'Only exact historical subjects/pre-state/parents; no P05-wide grant and no authorization to install unrelated definitions.'},
        'P04_ROOT_SLOT_SEMANTIC_AUTHORITY':{'status':'PRESENT_CURRENT','restriction':'Exact P04 qualification-only source/propositions/lineage; typed proof usability checked on target.'},
        'P04_ATTEST_AND_ACTION_AUTHORITIES':{'status':'PRESENT_IN_TRUSTED_CANONICAL_STATE','restriction':'Applicability evaluated at required historic/current consumer boundaries; terminal state is not an invitation to execute completed Actions.'},
        'END_REPRODUCTION_AUTHORITY_BINDING':{'status':'OTHER','classification':'NOT_YET_BOUND_TO_CURRENT_END_INPUT_GRAPH',
                 'restriction':'Use only applicable existing bounded subjects. No new human decision or native grant is defined or issued by this recovery.'},
        'BASELINE_REGRESSION_IMPORTER':{'status':'NO_NEW_AUTHORITY_REQUIRED','restriction':'Read-only legacy regression tests are explicitly owned by REG; import_e1 is excluded from canonical E2 END.'}}
    auth_file = write('authority-inventory.json', authorities)

    comparisons = ['complete typed snapshot inventories','full Computation including branches/witnesses/reasons',
                   'selected Action identity / decision readiness','Proof and recomputed ResumeEligibility',
                   'source/policy content pins and currentness','authority/provenance/context','canonical snapshot/bundle/event identities',
                   'ordered event parent/state ancestry','native typed rejection boundary']
    allowlist = ['persisted native bundle','independently trusted expected bundle identity','pinned source files','pinned supported policy','reviewed contracts']
    persistence = {
        'status':'CONTRACT_COMPLETE; current full END checkpoint binding depends on input closure',
        'canonical_target':'READ_ONLY; no new canonical P05 append event',
        'required_dimensions':{'hash_seeds':[0,1,7,101],'cold_readers_per_checkpoint_per_seed':3,
                               'writer_termination':True,'independent_processes':True,
                               'unordered_collection_orders':['original','reversed','rotated'],'object_key_orders':True},
        'allowlist':allowlist,'comparison_only_inputs':['sealed expected-state/oracle files'],
        'checkpoints':[
            {'when':'P05 entry / successful terminal P04 target','input':checkpoint['P04_TARGET'],'expected':'Exact sealed P04 target; TERMINAL_SUCCESS; completed six Actions; slot RESOLVED/root SATISFIED; no active resume'},
            {'when':'END each positive A01-A13 transition and external wait','input':'CURRENT_NATIVE_E2_END_A01_A13_INPUT_GRAPH after binding','expected':'Matrix stage contract; writer terminates at external checkpoint; identity/head continuity across fresh reader'},
            {'when':'Historical P04 actual A09-A13 boundaries and deferred installs','input':history_file,'expected':'Existing F03/P04 sealed native oracles; do not split atomic Evidence/receipt pair'},
            {'when':'A14 governed-unknown checkpoint and A16 acquisition invalidation','input':checkpoint['A14'],'expected':'Unknown proof; EXTERNAL_WAIT/resume false; invalidated sole valid route -> PLAN_DEFECT'},
            {'when':'A15 all disjoint accepted support/knowledge/authority/source invalidations','input':rel(doc('P03_PROSPECTIVE_CHECKPOINT_QUALIFICATION_1')),'expected':'Obligations retained; current support withdrawn; exact before/after native identities'},
            {'when':'N01-N16 isolated mutation/rejection boundaries','input':negative_file,'expected':'Native rejection or exact fail-closed state per case; rejected inputs produce no accepted post-state'}],
        'records':['writer PID and exit status','reader PID and exit status','input allowlists','source/code/contract SHA-256 pins',
                   'trusted identities before/after','native operands and event trace','full typed comparisons','rejection versus semantic oracle mismatch'],
        'compare':comparisons,'ordered_collections':['causal events','policy clauses'],
        'preservation':'Expected-answer files never Planner inputs; no frozen E1 writes; negative fixtures never alter successful target.'}
    persistence_file = write('persistence-plan.json', persistence)
    replay = {'status':'CONTRACT_COMPLETE; full END source/parent input binding still required',
              'native_operations':['codec.restore','codec._replay (via native restore)','core.recompute','core.resume_eligibility'],
              'target_history':'Replay trusted P04 recorded events, preserving 20 events and actual witnesses; no new decision, authority or result issuance.',
              'END':'Reproduce bound A01-A13 independently under D01; do not splice historical P02 and prospective P04.',
              'atomic_boundary':'EvidenceSourceAdmission + receipt remain one transaction; ingress-only prefix is private.',
              'derived_values':'Recompute Proof/C03/ResumeEligibility; do not serialize eligibility as permission.',
              'configuration':'The historical two deferred INSTALLs are checked as already accepted history, not new P05 authorization.',
              'compare':comparisons,'new_events_in_successful_P04_lineage':0}
    replay_file = write('replay-plan.json', replay)
    exit_terms = [
        {'id':'PACKAGE_PREREQUISITE','predicate':'E2_P04_RESULT == PASS'},
        {'id':'FULL_MATRIX_COVERAGE','predicate':'All 16 positive cases accounted at their governing scope; no missing or skipped requirement; all 19 P05-assigned cases pass'},
        {'id':'END','predicate':'Independently authored canonical A01-A13 full lifecycle passes real writer termination/fresh restore and D01 repetition; no E1 migration'},
        {'id':'D01','predicate':'All supported positive/negative states equal under seeds 0,1,7,101, declared unordered/key permutations and fresh processes, >=3 cold readers/checkpoint/seed'},
        {'id':'REG','predicate':'All affected current baseline A-N/X01-X11/C01-C06/refined C06/external unknown/C06A budget/native CLI/importer/constructor tests pass; prior closed findings remain closed'},
        {'id':'NEGATIVES','predicate':'E2-N01..E2-N16 pass their native fail-closed oracles with recorded before/after identities/trace'},
        {'id':'PERSISTENCE_REPLAY','predicate':'All required full state, source, policy, authority, ancestry and identity comparisons pass'},
        {'id':'PRESERVATION','predicate':'No E1 mutation, production effects, unqualified configuration, authority leakage, fabricated proof or bypass; no deferred-scope violations'},
        {'id':'REVIEW_READY','predicate':'Final implementation/contracts/evidence pinned; complete END/D01/REG and case evidence is ready for new independent P06 review'}]
    gate = {'schema':'E2-P05-READINESS-GATES-1','P05_INITIAL_ORACLE':'PASS','contract_recovery':'PASS',
            'P05_native_target':'Qualification evidence and review subject; canonical P04 terminal state unchanged',
            'P05_exit_terms':exit_terms,'P05_exit_predicate':' AND '.join(t['id'] for t in exit_terms),
            'P06_readiness_predicate':'E2_P05_RESULT == PASS AND complete pinned E2-END/E2-D01/E2-REG/full-matrix evidence AND new independent review subject ready',
            'P06_owned_case':p06['cases'],'P06_ready_now':'NO','P05_EXECUTION_READY':'NO','E2_P05_READY':'YES',
            'E2_P05_READY_domain':'Canonical package prerequisite only, as explicitly defined by prior P04 report; stricter prepared-execution gate is P05_EXECUTION_READY.',
            'execution_readiness_terms':{
                'initial_oracle':'PASS',
                'required_inputs_present_current':'NO; current native END graph / initial negative seeds not bound',
                'required_capabilities_qualified':'YES; no new native capability established',
                'required_definitions_current':'P04 active definitions PASS; END definition/input projection not yet bound',
                'required_authorities_applicable':'P04 historical/current consumer checks preserved; END reproduction subjects not yet bound',
                'negative_expectations_sealed':'YES; sixteen authoritative case contracts',
                'persistence_replay_contract':'COMPLETE; concrete full END process/checkpoint bindings remain DERIVABLE after input closure',
                'authoritative_P05_semantic_contract_recovered':'YES',
                'unresolved_preparation_bindings':'CURRENT_END_INPUT_GRAPH'},
            'first_dependency_ordered_blocker':'E2-END_CURRENT_NATIVE_INPUT_GRAPH_NOT_BOUND',
            'preparation_order':['Bind complete current independently authored A01-A13 input/source/policy/authority/parent graph and independent boundary oracles',
                                 'Bind initial/selected-unexecuted N08/N12 fixtures and remaining current negative/D01 checkpoint operands without changing expectations',
                                 'Seal concrete process/reader input manifests and evaluate prepared execution gate',
                                 'Execute P05 qualification only in its subsequent authorized execution package'],
            'not_readiness_blockers':['Future P05 PASS logs are outputs, not prerequisite inputs',
                                      'P03 original historical correspondence is not reopened by this package',
                                      'N_REAL is an independent aggregate release condition, not a new P05/P06 prerequisite',
                                      'Known historical baseline failures are not presumed new capability gaps; REG must rerun and retain them separately'],
            'no_runtime_defect_established':True,'no_new_configuration_required_established':True}
    gate_file = write('readiness-gates.json', gate)
    source_paths = [plan_path,matrix_path,plan_json,doc('E2_P04_CANONICAL_EXECUTION_RETRY_1_RESULT','md'),
                    doc('E2_P04_CANONICAL_EXECUTION_RETRY_1_RESULT'),doc('E2_P04_CANONICAL_TARGET_BUNDLE_1'),
                    doc('E2_PC01_FIXTURES'),doc('E2_PC01_COMPLETION_1_WHOLE_MODEL'),doc('E2_PC02_FIXTURES'),
                    doc('E2_PC03_FIXTURES'),doc('E2_PC03_ORACLE','py'),doc('E2_PC04_D01'),doc('E2_PC04_END'),
                    doc('E2_PC04_REVIEW'),doc('E2_PC04_PREFLIGHT'),doc('E2_P01_RETRY_1_RESULT'),
                    doc('E2_P02_RETRY_4_RESULT'),doc('P03_CHECKPOINT_SCOPE_DECISION_DOSSIER_1','md'),
                    doc('P03_PROSPECTIVE_CHECKPOINT_QUALIFICATION_1','md'),manifests_path,
                    ROOT/expected['semantic_oracle_path']]
    source_paths += [ROOT/c['qualified_evidence'] for c in caps if 'qualified_evidence' in c]
    source_paths += sorted((ROOT/'adapter/planner').glob('*.py'))
    source_paths += sorted((ROOT/'adapter/tests').glob('test_planner*.py'))
    source_paths = sorted(set(source_paths))
    sources_file = write('source-pins.json', {'identity_domain':'raw-file-sha256; not Planner object identity',
                         'files':[{'path':rel(p),'raw_sha256':sha(p)} for p in source_paths]})
    report = {'schema':'E2-P05-AUTHORITATIVE-CONTRACT-RECOVERY-READINESS-1','WORK_PACKAGE':'E2-P05-READINESS',
              'RESULT':'PARTIAL','CONTRACT_RECOVERY':'PASS','ENTRY_BUNDLE_TRUST':'PASS','COLD_RESTORE':'PASS',
              'P05_PURPOSE':p05['purpose'],'P05_INITIAL_ORACLE':'PASS','P05_INITIAL_CHECKS':len(target),
              'P05_ENTRY_BUNDLE_ID':expected['bundle_id'],'P05_ENTRY_STATE_ID':expected['state_id'],
              'P05_ENTRY_LEDGER_ROOT':expected['ledger_anchor'],'P05_ENTRY_APPEND_HEAD':expected['append_head'],
              'P05_INITIAL_CONTROL':'TERMINAL_SUCCESS',
              'P05_INITIAL_STATE':{'contract':'Trusted exact P04 terminal target; no P05/P06 case executed',
                      'expected':rel(OUT/'initial-oracle.json'),'comparison':rel(OUT/'target-inspection.json'),
                      'knowledge':'Current accepted E2-K-REENTER and E2-K-FINISH; actual admitted lifecycle witnesses',
                      'actions':'All six completed; no selected/actionable Action; final ResumeEligibility false',
                      'root_slot':'E2-SLOT RESOLVED / E2-ROOT SATISFIED; two usable typed proof instances',
                      'ancestry':'Twenty exact native events; exactly two authorized deferred installs inside P04'},
              'P04_OUTPUTS_CONSUMED':['Trusted terminal target and actual 20-event ordered ancestry','Native Evidence/admitted attestation/receipt',
                                      'Accepted ValidationResult/support','Two required A11 reentry events plus computed historical Proof/C03',
                                      'Actual permitted REENTER and FINISH result witnesses/current knowledge',
                                      'SLOT_PROOF and ROOT_PROOF, resolved slot/satisfied root, independent source',
                                      'Exact two deferred installs, retained authorities/source/policy/context',
                                      'Sealed P04 boundary oracles, cold/replay/determinism/negative evidence'],
              'P05_OWNED_TRANSITIONS':['Integration/full-matrix evidence evaluation','Isolated E2-N01..N16 native rejection/state probes',
                                      'E2-D01 determinism and independent cold process comparisons',
                                      'E2-END independent full A01-A13 lifecycle qualification reproduction',
                                      'E2-REG current affected baseline native/CLI/importer/constructor regressions',
                                      'Pin complete final evidence as P06 review subject'],
              'P05_OWNED_ACTIONS':[], 'P05_OWNED_EVENTS':'No new canonical P05 lifecycle event. Native transitions/invalidation/reproductions belong to isolated assigned qualification cases.',
              'P05_ALLOWED_CONFIGURATION_CHANGES':'NONE_TO_SUCCESSFUL_CANONICAL_TARGET; no P05-specific INSTALL/authority issuance is established.',
              'P05_REQUIRED_INPUTS':input_file,'P05_REQUIRED_AUTHORITIES':auth_file,'P05_REQUIRED_CAPABILITIES':cap_file,
              'P05_REQUIRED_ORACLES':{'entry':rel(OUT/'initial-oracle.json'),'full_matrix':case_file,
                      'negative_cases':negative_file,'D01':'Full typed semantics and canonical identities equal for native-declared equivalent inputs; policy/event order preserved',
                      'END':'Independent A01-A13 stage oracles; comparison-only expected inputs; complete current native binding still required',
                      'REG':'All current affected baseline requirements pass; no skips/historical-count substitute',
                      'preservation':'All preexisting files unchanged; E1/runtime/production effects zero',
                      'exit':gate_file},
              'P05_CONFIGURATION_REQUIREMENTS':{'canonical_target':'NONE','new_definition_or_adapter':'NONE_ESTABLISHED',
                    'isolated_END':'Full input graph must establish exact applicable historical/current contracts; no silent reuse of another lineage or new grant.'},
              'P05_NEGATIVE_ORACLES':negative_file,'P05_PERSISTENCE_PLAN':persistence_file,'P05_REPLAY_PLAN':replay_file,
              'P05_TARGET':gate['P05_native_target'],'P05_EXIT_PREDICATE':exit_terms,
              'P06_READINESS_PREDICATE':gate['P06_readiness_predicate'],'E2_P06_READY':'NO',
              'P05_EXECUTION_READY':'NO','E2_P05_READY':'YES','E2_P05_READY_DOMAIN':gate['E2_P05_READY_domain'],
              'FIRST_PREPARATION_BLOCKER':gate['first_dependency_ordered_blocker'],
              'NEXT_PACKAGE':'E2-P05 CURRENT END / MATRIX INPUT-BINDING CLOSURE',
              'CURRENT_REGRESSION_EXECUTION':'NOT_RUN; 18 modules / 246 declared test methods statically inventoried; no current PASS inferred',
              'P05_EXECUTED':'NO','P06_EXECUTED':'NO','E2_P04_RESULT':'PASS','P03_HISTORICAL_CORRESPONDENCE':'UNPROVEN',
              'N_REAL_SATISFIED':'NO','RUNTIME_MODIFIED':'NO','E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO',
              'NEW_AUTHORITY_ISSUED':'NO','NEW_DEFINITIONS_INSTALLED':0,
              'evidence':{'case_contracts':case_file,'old_pin_checks':old_file,'P04_checkpoints':history_file,
                          'END_input_trace':early_file,'initial_oracle':rel(OUT/'initial-oracle.json'),
                          'target_inspection':rel(OUT/'target-inspection.json'),'readiness_gates':gate_file,'source_pins':sources_file},
              'inspection_correction':{'first_result':rel(OUT/'target-inspection-first-inspection.json'),
                     'classification':'READINESS_HARNESS_OVERSTRICT_RETAINED_ROUTE_CURRENTNESS_ASSERTION',
                     'reason':'Native governed_external_unknown excludes DEPENDENT_ACTION_REENTRY; route bytes/support and immutable install witness remain exact. Required active definitions are current.',
                     'runtime_change':False,'P04_change':False,'sealed_semantic_oracle_change':False},
              'preservation':'Verification pending final file audit; this report does not execute any P05 case.'}
    if (OUT / 'preservation.json').is_file():
        audit = read(OUT / 'preservation.json')
        assert audit['RESULT'] == 'PASS'
        report['preservation'] = {'path':rel(OUT/'preservation.json'), 'raw_sha256':sha(OUT/'preservation.json'),
                                  'RESULT':'PASS', 'preexisting_files_checked':audit['preexisting_files_checked'],
                                  'runtime_files_checked':audit['runtime_files_checked'],
                                  'frozen_E1_files_checked':audit['frozen_E1_files_checked']}
        report['GIT_DIFF_CHECK'] = audit['GIT_DIFF_CHECK']
    path = doc('E2_P05_READINESS')
    path.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'RESULT':report['RESULT'],'P05_INITIAL_ORACLE':'PASS','assigned_cases':len(p05['cases']),
                      'negative_cases':len(negatives),'P05_EXECUTION_READY':'NO','E2_P05_READY':'YES',
                      'P05_EXECUTED':'NO','report':rel(path)}))


if __name__ == '__main__':
    main()
