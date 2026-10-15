"""Seal a contract, never execute or qualify a PREPARE transaction.

New persistence types below are specifications, not additions to the runtime
registry. All constructed event/bundle values are comparison-only oracles.
"""
import ast
import hashlib
import json
from dataclasses import fields, replace
from pathlib import Path

from adapter.planner import codec as c, core, gates, model as m

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
PLANS = ROOT / 'docs/plans'
PREFIX = 'DETERMINISTIC_PLANNER_V0_1_'
NAME = PREFIX + 'E2_P05_A04_DURABLE_ADMISSION_CONTRACT_1'
OLD = PREFIX + 'E2_P05_A04_PROSPECTIVE_ANCESTRY_CONTRACT_1'
RECON = PREFIX + 'E2_P05_A04_EVENT_VALIDATION_RECONCILIATION_1'
BASE = PLANS / 'qualification/E2_P05_A04_PROSPECTIVE_ANCESTRY_CONTRACT_1'
REC = PLANS / 'qualification/E2_P05_A04_EVENT_VALIDATION_RECONCILIATION_1'
BARRED = []
LABELS = {
    'QUALIFICATION_TYPE': 'PROSPECTIVE_REPLACEMENT',
    'ORIGINAL_A04_HISTORICAL_ANCESTRY': 'UNPROVEN',
    'ORIGINAL_A03_HISTORICAL_OCCURRENCE': 'UNPROVEN',
    'HISTORICAL_RECONSTRUCTION': 'NO',
    'PROSPECTIVE_A04_EVENT_IS_ORIGINAL_EVENT': 'NO',
}


def guard():
    def forbidden(name):
        def reject(*args, **kwargs):
            BARRED.append(name)
            raise AssertionError('contract-only inspection: ' + name)
        return reject
    for module, names in (
        (core, ('recompute', 'apply_event', 'apply_result', '_inventory', '_decision_result',
                'admit_dossier_materialization', 'apply_recorded_decision', 'apply_decision_reentry')),
        (c, ('_replay', 'apply_event', 'record_result', 'append_event', 'commit_event', 'commit_result',
             'save_bundle', 'restore', 'bundle_bytes', 'bundle_id', '_publish_head', '_prefix_bundle')),
        (gates, ('decision_readiness', 'evaluate_predicate', '_evaluate_predicate')),
    ):
        for name in names:
            if hasattr(module, name):
                setattr(module, name, forbidden(module.__name__ + '.' + name))


def read(path):
    return json.loads(Path(path).read_bytes())


def pin(path, pointer=''):
    path = Path(path).resolve()
    return {'path': str(path.relative_to(ROOT)), 'pointer': pointer,
            'raw_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def save(name, value):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()
    if path.exists() and path.read_bytes() != raw:
        raise AssertionError('sealed output conflict: ' + name)
    path.write_bytes(raw)
    return pin(path)


def text_id(value):
    return value.namespace + ':' + value.sha256


def location(path, symbol):
    tree = ast.parse((ROOT / path).read_text())
    node = next(n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == symbol)
    return dict(pin(ROOT / path), symbol=symbol, line=node.lineno, end_line=node.end_lineno)


def main():
    guard()
    old = read(PLANS / (OLD + '.json'))
    rec = read(PLANS / (RECON + '.json'))
    assert old['RESULT'] == 'PARTIAL' and rec['RESULT'] == 'PASS'
    assert old['SELECTED_OPTION'] == 'AUTHORIZE_PROSPECTIVE_P05_A04_ANCESTRY_QUALIFICATION'
    assert old['P05_BOUND_STAGE_INPUTS'] == 10
    assert old['PROSPECTIVE_A04_EXECUTED'] == old['PROSPECTIVE_A04_EXECUTION_READY'] == 'NO'
    assert rec['RUNTIME_MODIFIED'] == rec['A04_EXECUTED'] == 'NO'
    for item in old['EVIDENCE'].values():
        assert pin(ROOT / item['path'])['raw_sha256'] == item['raw_sha256']
    for item in rec['evidence'].values():
        assert pin(ROOT / item['path'])['raw_sha256'] == item['raw_sha256']

    expected = old['EXPECTED_RESULT_ORACLE']
    supplied = c._unwire(expected['expected_result'])
    after = c._unwire(expected['expected_post_state'])
    validations = c._unwire(expected['expected_validation_instances'])
    start_path = ROOT / old['PROSPECTIVE_START']['START_PATH']['path']
    start = c._unwire(c.parse_json(start_path.read_bytes())['bundle'])
    before_id = c._identity(start_path.read_bytes(), 'planner-bundle-v1')
    assert c._bundle_bytes_admitted(start) == start_path.read_bytes()
    assert text_id(before_id) == old['PROSPECTIVE_START']['START_BUNDLE_ID']
    assert len(start.events) == 2 and not start.current.validation_instances
    assert supplied.expected_snapshot == c.snapshot_id(start.current)
    assert c.snapshot_id(after).sha256 == expected['expected_post_state_id'].split(':')[1]
    assert tuple(after.validation_instances) == validations
    new_pin = c._unwire(old['EXPECTED_EVENT_ORACLE']['EVENT_PAYLOAD']['source_additions'][0])
    assert new_pin not in start.sources
    assert hashlib.sha256((ROOT / new_pin.path).read_bytes()).hexdigest() == new_pin.identity.sha256
    rep = read(REC / 'oracles/composite-representation.json')
    event = c._unwire(rep['native_event'])
    assert event.result == supplied and event.after_snapshot == c.snapshot_id(after)
    assert event.identity == c._event_identity(3, event.parent_snapshot, event.parent_event, supplied, event.after_snapshot)
    assert event.parent_snapshot == c.snapshot_id(start.current)
    assert event.parent_event == start.events[-1].identity and event.sequence == 3

    pins = [pin(PLANS / (name + suffix)) for name in (OLD, RECON) for suffix in ('.md', '.json')]
    pins += [pin(BASE / p) for p in ('prospective-start.json', 'prospective-inputs.json',
        'authenticated-scope-decision.json', 'authority.json', 'A04-definition.json',
        'inputs/dossier-source.json', 'inputs/bounded-producer-contract.json',
        'oracles/expected-result-and-state.json', 'oracles/ancestry-oracle.json',
        'oracles/ordering-oracle.json', 'END-replacement-mapping.json',
        'N12-N13-assurance-mapping.json', 'negative-contract.json',
        'persistence-replay-contract.json', 'later-execution-contract.json')]
    pins += [pin(REC / p) for p in ('native-schemas.json', 'dossier-validation-inventory.json',
        'native-correlation.json', 'P05-N12-N13-assurance.json', 'transaction-and-replay-gap.json',
        'minimum-generic-capability.json', 'contract-revision-overlay.json',
        'oracles/composite-representation.json')]
    pins += [pin(start_path)]
    pins += [pin(PLANS / (PREFIX + p)) for p in ('CANONICAL_QUALIFICATION_EXPERIMENT_1.json',
        'CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md', 'E2_T02_RESULT.json',
        'E2_T02_RESULT.md', 'E2_PC01_SOURCES.json', 'E2_P05_END_INPUT_BINDING_1.json',
        'E2_P05_READINESS.json')]
    pins += [pin(PLANS / 'qualification/E2_P05_END_INPUT_BINDING_1/input-oracle.json'),
             pin(PLANS / 'qualification/E2_P05_A03_PROSPECTIVE_OCCURRENCE_EXECUTION_1/P05-binding-rerun.json')]
    pins += [pin(ROOT / p) for p in read(OUT / 'baseline.json')['files'] if p.startswith('adapter/planner/')]
    assert read(PLANS / 'qualification/E2_P05_A03_PROSPECTIVE_OCCURRENCE_EXECUTION_1/P05-binding-rerun.json')['P05_BOUND_STAGE_INPUTS'] == 10
    save('source-pins.json', {'pins': pins})

    path = {
        'existing_sequence': [
            {'step': 'typed inputs', 'exists': True, 'contract': 'SuppliedResult plus separate Tuple[ValidationInstance,...]; expected_snapshot binds native pre-state'},
            {'step': 'bounded producer and independent checks', 'exists': 'SEALED_SOURCE_RULES; NO_DURABLE_EXECUTOR_INTEGRATION', 'contract': 'Future fresh bounded producer reads authored source and Action contract, evaluates six rules; no expected oracle input'},
            {'step': 'state admission/result application', 'exists': True, 'call': 'core.admit_dossier_materialization(snapshot, supplied, validation_instances)'},
            {'step': 'private immutable post-state', 'exists': True, 'contract': 'One TransitionReport after model and readiness checks; no persisted event'},
            {'step': 'Snapshot construction/hash/encoding', 'exists': True, 'call': 'Snapshot is the returned immutable state; codec.snapshot_bytes / snapshot_id'},
            {'step': 'ordinary event construction/append', 'exists': 'GENERIC_PRIMITIVE_ONLY', 'call': 'record_result -> apply_event -> apply_result, not T02'},
            {'step': 'bundle/immutable files/HEAD publication', 'exists': 'GENERIC_PRIMITIVE_ONLY', 'call': 'commit_event -> record_result -> _publish_head -> save_bundle -> bundle_bytes -> _replay'},
            {'step': 'T02 durable replay integration', 'exists': False, 'contract': 'No historical Snapshot resolver or dossier-event branch'},
        ],
        'state_effects': ['PREPARE completed', 'actual bounded E2-K-PREPARE admitted', 'Action.prepared_dossier set',
            'Decision.dossier and native stage/history advanced to DECISION_READY', 'six ValidationInstances admitted',
            'native decision Action readiness recomputed; no human choice/authority issued'],
        'ordinary_failure_before_append': 'validate_result rejects fresh dossier when Action.prepared_dossier is None; SuppliedResult carries no validation tuple',
        'T02_atomicity_limit': 'Immutable state admission only; no event/ledger/source enrollment/HEAD publication',
        'T02_replay_claim_limit': 'Prior T02 encode/decode is Snapshot retention, not event-bearing dossier transaction replay',
        'existing_snapshot_is_state': 'No separate mutable post-state entity is needed. The returned Snapshot is encoded and hashed as PLANNER-SNAPSHOT-1.',
        'gaps': [
            {'category': 'RESULT_APPLICATION', 'gap': 'Integrate existing T02 admission into durable PREPARE path; do not use ordinary apply_result for fresh dossier'},
            {'category': 'POST_SNAPSHOT_CREATION', 'gap': 'Existing hash/codec sufficient; retain canonical historical Snapshot body as immutable archive object'},
            {'category': 'EVENT_APPEND', 'gap': 'Compose unchanged ExecutionEvent from T02 post-state rather than ordinary dispatcher'},
            {'category': 'EVENT_TO_POST_SNAPSHOT_BINDING', 'gap': 'after_snapshot already supplies identity; implement resolver and historical outcome checks'},
            {'category': 'PERSISTENCE_BUNDLE_COMMIT', 'gap': 'Atomic source-pin boundary, minimal bundle binding, archive files and existing HEAD protocol'},
            {'category': 'REPLAY', 'gap': 'Resolve historical Snapshot, extract original typed outcomes, verify pure T02 projection and prefix sources'},
            {'category': 'OTHER', 'gap': 'Durable semantic retry/conflict detection before producer invocation; state no-op is insufficient'},
        ],
        'locations': [location('adapter/planner/core.py', s) for s in ('apply_result', 'admit_dossier_materialization', 'apply_event')]
            + [location('adapter/planner/codec.py', s) for s in ('snapshot_bytes', 'snapshot_id', '_event_identity',
                '_replay', 'record_result', 'save_bundle', 'restore', '_publish_head', '_read_head', '_prefix_bundle', 'commit_event')]
            + [location('adapter/planner/validation_transaction.py', s) for s in ('apply', 'commit')],
    }
    save('existing-path.json', path)

    transaction = {
        'status': 'COMPLETE_PROPOSED_CONTRACT_NOT_IMPLEMENTED_OR_EXECUTED',
        'operation': 'GENERIC_PERSISTED_DOSSIER_MATERIALIZATION',
        'applicability': 'Selected native DECISION_INPUT_ACQUISITION Action with a supported dossier and independent typed checks; qualification executor is NON_EFFECTING here',
        'public_operands': [
            {'name': 'pre_bundle', 'type': 'PersistenceBundle', 'binding': 'Trusted exact native bundle identity, current Snapshot, append head, source/policy inventory and context'},
            {'name': 'expected_bundle', 'type': 'ArtifactIdentity[planner-bundle-v1]', 'binding': 'External trusted pre-bundle/HEAD anchor, not a newly computed trust claim'},
            {'name': 'action', 'type': 'ActionId', 'binding': 'Exactly selected unexecuted decision-input producer in pre-state'},
            {'name': 'producer', 'type': 'Qualified bounded executor callable', 'binding': 'Registered trusted producer bound to current Action/source rules; receives pinned inputs only; no caller-supplied executed/validated Boolean'},
            {'name': 'source_artifacts', 'type': 'Tuple[(ArtifactPin, bytes), ...]', 'binding': 'Exact raw bytes for new source pins; immutable path/profile/content and rule/provenance references'},
            {'name': 'repo_root / output_dir', 'type': 'Filesystem roots', 'binding': 'Existing no-symlink, local-lock, frozen-E1 and immutable-content constraints'},
        ],
        'producer_outputs': {
            'supplied': 'Actual native SuppliedResult: ActionId, bounded ActionResult, actual KnowledgeRecord tuple, mandatory expected_snapshot, DecisionDossier',
            'validation_instances': 'Actual Tuple[ValidationInstance,...] from independent producer-rule evaluations, never copied from expected oracles',
            'trust_boundary': 'The live operation owns invocation of the qualified producer. A raw result/candidate/expected Snapshot supplied without that invocation is not a live execution API. Native historical replay has a separate verifier path.',
        },
        'private_precommit_candidate': {
            'type': 'Frozen internal execution context, never serialized as an event/result field',
            'members': ['trusted pre-bundle ID/state/head', 'actual supplied result', 'actual validation tuple', 'source pins and bytes',
                'T02 post-Snapshot', 'native occurrence event', 'minimal bundle binding', 'updated PersistenceBundle'],
            'equivalence': 'Preflight and publication consume the same canonical native values; recheck full values/source bytes/pre-head under the lock. No independently reconstructed replacement result.',
            'live_admission_operand': 'core.admit_dossier_materialization(pre_bundle.current, actual_supplied, actual_validation_tuple)',
        },
        'outputs': ['committed PersistenceBundle and native planner-bundle-v1 ID', 'native ExecutionEvent and planner-event-v1 ID',
            'canonical post-Snapshot and planner-snapshot-v1 ID', 'full actual SuppliedResult in event.result',
            'actual KnowledgeRecords and DecisionDossier in post-state', 'native ValidationInstances in post-state',
            'bundle-level DossierMaterializationBinding', 'content-addressed archive closure', 'HEAD and commit/retry disposition'],
        'excluded_outputs': ['new standalone ActionResult ID', 'new ValidationInstance ID', 'Proof entity', 'permission/eligibility Boolean',
            'recorded human choice', 'new authority', 'INSTALL event', 'P05 execution'],
        'order': [
            'Validate exact sealed contract and expected external trust anchor; load pinned pre-bundle and source bytes',
            'Acquire existing local transaction lock; restore and audit HEAD and native prefix; resolve retry before producer',
            'For new intent require exact expected bundle/state/head/context/policy and selected unexecuted PREPARE',
            'Invoke bounded producer on admitted inputs and pinned authored source; capture actual result and independent typed validations',
            'Validate native result/tuple, provenance, supported check membership, ordered input identities and authority applicability',
            'Apply unchanged T02 state admission privately; require exact independent result/postcondition oracle',
            'Encode immutable post-Snapshot as PLANNER-SNAPSHOT-1; compute native SnapshotId',
            'Construct unchanged native SuppliedResult occurrence event from sequence, pre-Snapshot, parent event, actual result, post-Snapshot ID',
            'Construct DossierMaterializationBinding for event, trusted pre-bundle and exact new source pins; build updated bundle',
            'Run full detached-archive replay verifier and occurrence/ancestry/post-state oracles without invoking producer or live validators',
            'Stage immutable source/archive/event/bundle files, fsync; revalidate all pins and HEAD/pre-state',
            'Atomically publish existing PLANNER-HEAD-1 with new bundle, previous pre-bundle, command=None; fsync directory; return success',
        ],
        'failure_policy': 'Any mismatch before HEAD replacement aborts; no later step, live repair, new fixture or new authority. Post-publication uncertainty is resolved by reading HEAD under lock and comparing the identical intent.',
        'producer_retry_limit': 'Exactly once durable semantic occurrence; a crash before commit may rerun this NON_EFFECTING producer. No claim of exactly once callback invocation across crashes or distributed writers.',
        'postconditions': 'Complete sealed T02 result/knowledge/dossier/validations and decision readiness; no decision choice, no authority issuance, no other Action execution',
        'source_admission': 'One sealed raw dossier source is enrolled atomically with this event; this is provenance enrollment, not governed definition INSTALL or a new semantic grant',
    }
    save('transaction-contract.json', transaction)

    storage = {
        'chosen_representation': 'DETACHED_NATIVE_POST_SNAPSHOT_WITH_MINIMAL_BUNDLE_BINDING',
        'new_runtime_types_status': 'CONTRACT_ONLY_NOT_IN_CURRENT_TYPE_REGISTRY',
        'event_and_snapshot_schema_changes': 'NONE',
        'new_binding_type': {
            'name': 'DossierMaterializationBinding', 'frozen': True,
            'fields': [
                {'name': 'event_identity', 'type': 'ArtifactIdentity', 'namespace': 'planner-event-v1'},
                {'name': 'expected_bundle', 'type': 'ArtifactIdentity', 'namespace': 'planner-bundle-v1'},
                {'name': 'source_additions', 'type': 'Tuple[ArtifactPin,...]', 'collection_semantics': 'UNORDERED_UNIQUE_PIN_SET'},
            ],
            'standalone_identity': False,
            'why_required': 'Pin the exact pre-bundle/source-enrollment boundary in the hash-bound replay context; event already binds result and post-Snapshot, so neither validation bodies nor a second Snapshot reference is needed here',
        },
        'bundle_extension': {
            'field': 'dossier_materializations', 'type': 'Tuple[DossierMaterializationBinding,...]', 'default': [],
            'collection_semantics': 'UNORDERED_UNIQUE_BY_EVENT_IDENTITY',
            'wire': 'Additive field of PLANNER-BUNDLE-1 PersistenceBundle, native $type registry encoding, canonical tuple as JSON list',
            'default_omission': 'Explicit codec default-omission registration, following P03_FIELDS convention; existing bundles without the field retain exact bytes/IDs',
            'known_fields_only': True,
            'constraints': ['Exactly one binding per dossier-materialization event; no orphan/duplicate binding',
                'Binding is covered by trusted final bundle hash, not trusted as a report or an unbound sidecar',
                'The bound event must be SuppliedResult with a dossier for a decision-input Action; no authority/decision/result variant substitution',
                'All source additions unique by path/pointer/profile across this and existing introduction mechanisms; existing pins are reused, not reintroduced',
                'All additions physically verified and referenced by dossier/check/ValidationInstance provenance; reject unrelated pin additions',
                'Prefix reconstruction filters bindings to included events and excludes later source additions; expected_bundle must equal native reconstructed prefix ID'],
        },
        'archive': {
            'key': 'ExecutionEvent.after_snapshot: existing planner-snapshot-v1 ArtifactIdentity',
            'file': 'snapshot-<after_snapshot.sha256>.json in the transaction directory',
            'bytes': 'Exactly codec.snapshot_bytes(Snapshot): canonical PLANNER-SNAPSHOT-1 envelope',
            'resolver': 'resolve_snapshot(ArtifactIdentity) -> Snapshot; reject wrong domain/missing/symlink/noncanonical/type/model/hash mismatch',
            'closure': 'Retain one immutable object for every event referenced by dossier_materializations, even after later invalidation/removal of current validation members',
            'authority': 'No archive object alone establishes occurrence. Only an accepted event in a trusted complete bundle/HEAD with verified replay correlation does.',
            'same_snapshot_deduplication': 'One file per exact SnapshotId; immutable-create conflict rules; archive is physical retention, not a new entity or installation',
            'private_preflight_resolver': 'Frozen in-memory map of verified historical archive plus candidate post-Snapshot; real restore uses only persisted files',
        },
        'native_relationships': [
            'event.result is the actual full SuppliedResult; no invented result-entity or command identity',
            'event.parent_snapshot == supplied.expected_snapshot == snapshot_id(actual pre-state)',
            'after == T02(pre-state, actual supplied, actual validations).snapshot',
            'event.after_snapshot == snapshot_id(after); archive returns exactly that Snapshot',
            'after.validation_instances contains exact uniquely selected PredicateId/dossier members with full typed values',
            'Dossier content ID == SHA256(canonical _wire(supplied.dossier)); event and Snapshot retain that same dossier',
            'event.identity == existing _event_identity(sequence, pre-Snapshot ID, parent event, full supplied, post-Snapshot ID, None)',
            'bundle contains the exact event and binding, post-state and source pins; HEAD names that native bundle identity',
        ],
        'typed_member_selector': '(event.after_snapshot, native PredicateId, native dossier ArtifactIdentity); no report pointer as native identity',
        'tamper_rule': 'Any changed validation-covered native post-state member changes canonical SnapshotId and therefore event identity, or fails typed/model admission. A forged replacement hash cannot match the trusted event/bundle/HEAD anchor.',
        'unordered_semantics': 'Snapshot.validation_instances and native declared sets canonicalized per codec; ValidationInstance.inputs remains ordered. Duplicate PredicateIds rejected; no set conversion of ordered input tuple.',
        'additional_provenance_check': 'Validate every ValidationInstance.provenance and input-source binding against the historical prefix plus exact additions; do not rely solely on current decision_provenances/external_provenances coverage',
        'A04_expected_source_additions': c._wire((new_pin,)),
        'A04_expected_validation_count': 6,
        'A04_member_bindings': [dict(predicate=c._wire(v.predicate), dossier=c._wire(v.dossier),
            snapshot=c._wire(event.after_snapshot), ordered_inputs=c._wire(v.inputs)) for v in validations],
        'post_bundle_required_contents': ['unchanged initial Snapshot and CHECK/COLLECT ledger prefix', 'A04 full native SuppliedResult occurrence event at sequence3',
            'current full post-Snapshot', 'one DossierMaterializationBinding', 'old source pins plus exactly sealed dossier source',
            'unchanged policy/version/scope', 'standalone immutable event/Snapshot/bundle files required for restore'],
        'authority_references': 'Preserve exact start context and PC01 native Action.authority=None; qualification scope decision remains external sealed authorization, not a new native grant. Any required authority already in pre-state is hashed there.',
    }
    save('snapshot-event-binding.json', storage)

    commit = {
        'visibility_boundary': 'Atomic replacement of HEAD after complete immutable artifact closure and all semantic checks; artifact existence alone is not acceptance',
        'atomic_semantic_unit': ['actual supplied PREPARE result and bounded knowledge', 'complete dossier/typed validations/post-Snapshot',
            'one native event/ledger append', 'exact source additions and replay binding', 'post PersistenceBundle and HEAD'],
        'precommit_unchanged': 'Authoritative pre-bundle/state/ledger/HEAD remain byte-identical through all checks and staging failures',
        'durable_invariants': ['No accepted applied result/knowledge/dossier without its occurrence event',
            'No accepted event without complete archived post-Snapshot and validations',
            'No Snapshot or validation tuple labeled qualified occurrence without native admitted event',
            'No accepted bundle with missing source pins/archive/binding',
            'No canonical append-head advance without complete transaction'],
        'file_order': ['source objects/new raw pinned artifacts', 'historical/candidate Snapshot archive objects',
            'immutable event files', 'immutable canonical bundle file', 'directory fsync',
            'HEAD temporary file/fsync, final source verification and parent check', 'atomic HEAD replacement and directory fsync'],
        'orphan_files': 'Crash-created files before HEAD may remain as unaccepted staging objects; they do not authorize acceptance, graph binding or resume. Never load an orphan as trusted merely by computing its hash.',
        'trusted_readers': 'Only restore externally trusted bundle identity or validated HEAD; require complete archive/event/source closure and full replay before exposure. Hashes are integrity bindings, not issuer signatures.',
        'retry_intent': '(trusted expected pre-bundle ID, original parent Snapshot ID, original parent event ID, native ActionId); all are native identities, no new command namespace',
        'retry_effect': 'Full canonical SuppliedResult, canonical native validation member values, source pin/content inventory and resulting Snapshot/event/bundle identities',
        'intent_recovery': 'Resolve original native prefix using exact expected_bundle and source/binding history. Inspect exactly the next event; derive ActionId and original parent fields from its native envelope/result.',
        'identical_retry': 'If a verified committed matching intent and exact effect already exist, return historical committed transaction identity and current verified head without producer invocation, ledger append, state reset or new bundle. If descendants exist, preserve them.',
        'retry_evidence': 'If an already-prepared candidate is resubmitted, require exact canonical result/tuple/source effect equality to archived committed operands. A new source/content/result under same intent is conflict, not a fresh command.',
        'conflicting_retry': 'Fail if any result/dossier/outcome/output/validation/source/context differs, if original prefix cannot be proven, if another command consumed that parent, or if retry asserts a new current parent for an already completed Action',
        'retry_after_precommit_failure': 'No admitted event exists; reload same verified parent and run the NON_EFFECTING producer again. Orphan immutable files must match exact bytes or fail; do not silently mutate them.',
        'retry_after_uncertain_publication': 'Read trusted HEAD under lock; exact transaction present => historical no-op success; pre-state still current => new attempt; divergent head/effect => fail',
        'HEAD_contract': 'Existing PLANNER-HEAD-1 fields unchanged: bundle=new ID, previous=expected pre-bundle ID, command=None for SuppliedResult. _read_head/_prefix_bundle must understand detached dossier bindings.',
        'filesystem_semantics': 'Existing local flock/immutable-create/fsync/atomic replace protocol; no distributed concurrency guarantee. Post-replace I/O uncertainty is not reported as a rolled-back pre-state.',
        'failure_injection_points': ['after producer', 'after typed validation checks', 'after T02/private state', 'after Snapshot hashing',
            'after event/binding construction', 'after source stage', 'after archive stage', 'after event stage',
            'after bundle stage', 'after pre-HEAD fsync/pin verification', 'during HEAD replacement', 'after HEAD replacement/before acknowledgement'],
    }
    save('durable-commit-contract.json', commit)

    replay = {
        'status': 'SEALED_CONTRACT_NOT_IMPLEMENTED_OR_QUALIFIED',
        'cold_restore_inputs': ['externally trusted planner-bundle-v1 identity or audited HEAD', 'canonical bundle file',
            'immutable event files', 'immutable Snapshot archive files addressed by event.after_snapshot', 'raw source and policy pins'],
        'cold_restore_order': ['verify expected bundle hash/known schema/type/canonical wire', 'verify policy and source files',
            'verify unique binding/event correspondence and archive hash/model', 'replay complete history with historical archive resolver',
            'compare final state/Snapshot/source inventory; audit HEAD previous/command when restoring HEAD',
            'reconstruct exact A04 occurrence, parent, sequence/index, actual result/outputs and typed member bindings'],
        'algorithm': [
            'Validate the complete bundle and native event identities; collect all exact source introductions from existing admissions and new dossier bindings',
            'Initial replay sources = bundle.sources minus explicitly recorded introductions; validate initial Snapshot/provenance and unchanged policy/scope',
            'Walk native events in sequence, checking parent_snapshot/current state and parent_event/previous event',
            'For each ordinary event without a dossier binding preserve existing native dispatch behavior',
            'For bound dossier event require exact SuppliedResult type/dossier, selected native decision-input Action, original expected_snapshot and binding.expected_bundle == native current prefix bundle ID',
            'Resolve archive exclusively by event.after_snapshot; verify canonical PLANNER-SNAPSHOT-1 bytes and native identity/model',
            'Select original ValidationInstances by dossier checks/unique native PredicateIds; verify full subject/proposition/ordered inputs/scope/lineage/provenance/currentness and historical source boundary',
            'Make exactly the binding source additions available at this event; verify raw source contents and reject duplicate/unrelated introduction',
            'Invoke unchanged T02 admission as a pure historical state projection using event.result and the resolved original typed records; never call the live producer or independent validator',
            'Compare entire canonical recomputed Snapshot with archive, not just validations or decision-ready flag; require after_snapshot equality',
            'Advance event head exactly once; preserve native computed readiness separately from history and persisted outcomes',
            'For prefixes keep only included binding entries and source introductions; for final bundle require exact current Snapshot hash and exact sources',
        ],
        'historical_outcomes': 'ValidationOutcome/currentness is read from the original event-bound archived Snapshot. Readiness/model/binding checks may recompute; independent validation is not rerun as a new epistemic decision.',
        'not_allowed': ['latest mutable bundle.current as historical operand for an earlier event', 'writer caches or report paths as operand identity',
            'rerunning PREPARE/source acquisition/independent validation', 'adding event/knowledge/result/authority on replay',
            'inventing missing historical Snapshot/typed outcomes from final state', 'serializing computed permission/eligibility'],
        'result_output_correlation': 'Full native event.result values must match the admitted post-state KnowledgeRecords/dossier and exact T02 effect; no separate invented ActionResult identity',
        'validation_correlation': 'Immutable after_snapshot selects exact original typed tuple; binding pin introductions authenticate historical provenance; whole-state projection closes correlation',
        'validation_tamper_rejection': ['wrong archive hash/canonical bytes', 'missing or duplicate PredicateId', 'wrong dossier/ordered inputs/provenance',
            'changed generation/context/post-state', 'missing new source pin or changed raw source', 'wrong prefix/binding expected_bundle', 'event.result mismatch'],
        'later_invalidation': 'Retain original archive/event for historical audit. Replay later source/check invalidation separately; current readiness may become false without deleting or rewriting the original occurrence.',
        'exactly_once': 'Historical verification folds each committed event once; replay returns the historical bundle/state, never commits a second occurrence or increments HEAD',
        'fresh_reader_contract': 'No writer process/imported expected-state object may supply the archive. Missing disk archive fails even if latest current Snapshot or a report contains an equivalent value.',
        'prefix_equivalence': 'Reconstructed original prefix must preserve exact sources, bindings, policy, initial/current state and event order; expected_bundle is checked before the new binding is added, avoiding a hash cycle',
        'qualification_requirements': ['positive durable A04 event/complete state/source boundary', 'older 24 negatives plus durable negatives',
            'injected failures at every precommit boundary', 'retry/no-op/conflict with descendants',
            'cold restore and full replay in fresh processes after writer exit', 'replay after later validation/source invalidation retains original archive',
            'missing archive/forged mapping must fail', 'zero live-producer/validator calls during replay',
            'hash seeds0,1,7,101 and native unordered presentations'],
    }
    save('replay-contract.json', replay)

    identity = {
        'IDENTITY_CYCLE': 'NO',
        'nodes_in_topological_order': ['sealed pre-bundle/pins/context', 'actual SuppliedResult/dossier/typed validation values',
            'T02 post-Snapshot canonical bytes/ID', 'native occurrence event bytes/ID',
            'DossierMaterializationBinding value', 'post PersistenceBundle bytes/ID', 'HEAD pointer'],
        'edges': [
            ['sealed pre-bundle/pins/context', 'actual SuppliedResult/dossier/typed validation values'],
            ['actual SuppliedResult/dossier/typed validation values', 'T02 post-Snapshot canonical bytes/ID'],
            ['sealed pre-bundle/pins/context', 'T02 post-Snapshot canonical bytes/ID'],
            ['T02 post-Snapshot canonical bytes/ID', 'native occurrence event bytes/ID'],
            ['actual SuppliedResult/dossier/typed validation values', 'native occurrence event bytes/ID'],
            ['sealed pre-bundle/pins/context', 'native occurrence event bytes/ID'],
            ['native occurrence event bytes/ID', 'DossierMaterializationBinding value'],
            ['sealed pre-bundle/pins/context', 'DossierMaterializationBinding value'],
            ['DossierMaterializationBinding value', 'post PersistenceBundle bytes/ID'],
            ['T02 post-Snapshot canonical bytes/ID', 'post PersistenceBundle bytes/ID'],
            ['native occurrence event bytes/ID', 'post PersistenceBundle bytes/ID'],
            ['post PersistenceBundle bytes/ID', 'HEAD pointer'],
        ],
        'no_back_edges': ['Snapshot/context/dossier/validation values never refer to the new event ID, new ledger head or new bundle ID',
            'event.after_snapshot refers to state before ledger append, whose native Snapshot has no embedded ledger/head field',
            'binding.expected_bundle refers to the already-existing pre-bundle, never the post-bundle',
            'ledger pointer is a post-bundle events locator used by readers, not a hashed field of the event'],
        'event_type': 'ExecutionEvent.result branch SuppliedResult; no new PREPARE event tag',
        'native_hashes': {'dossier': 'planner-dossier-sha256', 'Snapshot': 'planner-snapshot-v1', 'event': 'planner-event-v1', 'bundle': 'planner-bundle-v1'},
        'no_new_identity_domains': True,
        'stage_rule': 'Compute state first, then event, then temporal binding and bundle; write immutably, publish HEAD last',
        'event_payload_unchanged': True,
        'result_schema_unchanged': True,
        'snapshot_schema_unchanged': True,
        'new_bundle_field_not_yet_native': True,
    }
    save('identity-order.json', identity)

    # Contract wire illustration only. This future optional field is NOT
    # registered in codec/model and this is NOT a new occurred PersistenceBundle.
    binding_wire = {'$type': 'DossierMaterializationBinding', 'event_identity': c._wire(event.identity),
                    'expected_bundle': c._wire(before_id), 'source_additions': c._wire((new_pin,))}
    future_bundle = c._wire(replace(start, events=start.events + (event,), current=after,
                                  sources=start.sources + (new_pin,)))
    future_bundle['dossier_materializations'] = [binding_wire]
    future_bytes = c.canonical_bytes({'schema': 'PLANNER-BUNDLE-1', 'bundle': future_bundle})
    comparison_id = c._identity(future_bytes, 'planner-bundle-v1')
    oracle = {
        **LABELS, 'role': 'STATIC_FUTURE_WIRE_COMPARISON_NOT_EXECUTED_NOT_COMMITTED_NOT_REPLAYED',
        'native_event_oracle': pin(REC / 'oracles/composite-representation.json', '/native_event'),
        'EXPECTED_EVENT_ID': text_id(event.identity), 'EXPECTED_POST_SNAPSHOT_ID': text_id(event.after_snapshot),
        'EXPECTED_DOSSIER_ID': expected['expected_dossier_id'], 'EXPECTED_PRE_BUNDLE_ID': text_id(before_id),
        'EXPECTED_PARENT_EVENT': text_id(event.parent_event), 'EXPECTED_PRE_STATE': text_id(event.parent_snapshot),
        'sequence': 3, 'array_index': 2, 'LEDGER_ROOT': old['PROSPECTIVE_START']['LEDGER_ROOT'],
        'existing_event_schema': [f.name for f in fields(m.ExecutionEvent)],
        'post_snapshot_oracle': pin(BASE / 'oracles/expected-result-and-state.json', '/expected_post_state'),
        'archive_expected_file_name': 'snapshot-' + event.after_snapshot.sha256 + '.json',
        'archive_expected_raw_sha256': hashlib.sha256(c.snapshot_bytes(after)).hexdigest(),
        'binding_future_wire': binding_wire,
        'EXPECTED_FUTURE_BUNDLE_ID_COMPARISON_ONLY': text_id(comparison_id),
        'future_bundle_wire': {'schema': 'PLANNER-BUNDLE-1', 'bundle': future_bundle},
        'future_bundle_schema_currently_supported': False,
        'additional_configuration_events': 0,
        'actual_execution_occurrence': False,
        'P05_binding_applied': False,
    }
    save('oracles/prospective-native-binding.json', oracle)

    cases = [
        ('wrong PrepareResult', 'Outcome/Action/dossier/result contract differs', 'Reject before T02/HEAD'),
        ('result not actually executed', 'Raw supplied/oracle result presented to live commit without qualified producer context', 'Reject live API bypass; replay verifier is read-only'),
        ('wrong pre-state', 'expected_snapshot or native pre-state differs', 'Reject stale/misbound context'),
        ('wrong parent', 'Original head/parent event differs', 'Reject before append'),
        ('wrong post-Snapshot', 'Archive ID/body differs from event.after_snapshot', 'Reject hash/model/whole-state comparison'),
        ('tampered post-state', 'Unrelated Action/control/knowledge/validation/context changes', 'Reject complete T02 projection equality'),
        ('wrong event', 'Envelope/result/sequence/identity branch differs', 'Reject native event identity and binding check'),
        ('wrong ledger', 'Event not in externally trusted bundle/prefix', 'Reject occurrence mapping'),
        ('wrong append head', 'HEAD advanced to foreign/conflicting command', 'Reject exact prefix intent'),
        ('validation bound to different Snapshot', 'Member selector resolves a foreign after-state/dossier', 'Reject immutable binding'),
        ('missing validation binding', 'Check/member/dossier/source/binding/archive missing', 'Reject complete tuple/reference closure'),
        ('event without result', 'Missing actual typed result/output', 'Reject schema or replay effect'),
        ('result without event', 'State-only T02/snapshot/report offered as durable occurrence', 'Reject P05 occurrence assurance'),
        ('duplicate retry', 'Exact already committed operation resubmitted', 'No duplicate durable effect; reject second append and return historical no-op'),
        ('conflicting retry', 'Same intent different result/check tuple/source/context', 'Reject effect conflict'),
        ('replay creating second occurrence', 'Replay attempts append/publish or producer invocation', 'Reject; verify-only replay'),
        ('source substitution', 'Raw source bytes/provenance/content differ from sealed pin', 'Reject source validation'),
        ('source boundary drift', 'Future source visible in an earlier prefix or omitted at A04', 'Reject expected pre-bundle/source equality'),
        ('archive missing after descendant invalidation', 'Latest state substituted for original archived state', 'Reject restore/replay; history cannot be inferred'),
        ('orphan archive accepted as occurrence', 'Pre-HEAD files presented without trusted accepted event/bundle', 'Reject graph binding'),
        ('binding tampering', 'Bundle binding event/pre-bundle/source delta mutated', 'Reject trusted bundle hash or semantic binding'),
        ('duplicate binding/member', 'Duplicate native event binding or PredicateId', 'Reject uniqueness'),
        ('ordered input reversal', 'ValidationInstance.inputs reversed', 'Reject sealed ordered input contract; R05 does not declare this tuple unordered'),
        ('historical relabeling', 'New event mapped as original A04/A03 ancestry', 'Reject authorized replacement labeling'),
    ]
    negatives = {'status': 'SEALED_NOT_RUN', 'inherited_24_negative_expectations': pin(BASE / 'negative-contract.json'),
        'inherited_count': 24,
        'durable_cases': [{'id': 'DA%02d' % i, 'case': name, 'mutation': mutation,
            'expected': expected_case, 'status': 'SEALED_NOT_RUN'} for i, (name, mutation, expected_case) in enumerate(cases, 1)],
        'failure_injection': commit['failure_injection_points'],
        'positive_retry_is_not_rejected': 'An identical semantic retry is a success/no-op; the negative is an attempted second result/event/ledger append',
        'qualification_boundary': 'Run only in isolated fixtures in the later implementation/qualification package; no mutations or execution here'}
    assert len(old['NEGATIVE_SUITE']) == 24 and all(x['status'] == 'SEALED_NOT_RUN' for x in old['NEGATIVE_SUITE'])
    save('negative-contract.json', negatives)

    preserved_files = [pin(BASE / p) for p in ('prospective-start.json', 'prospective-inputs.json',
        'inputs/dossier-source.json', 'inputs/bounded-producer-contract.json', 'oracles/expected-result-and-state.json',
        'oracles/ancestry-oracle.json', 'oracles/ordering-oracle.json', 'authenticated-scope-decision.json',
        'authority.json', 'END-replacement-mapping.json', 'N12-N13-assurance-mapping.json', 'negative-contract.json')]
    overlay = {
        'schema': 'A04-DURABLE-ADMISSION-OVERLAY-1', **LABELS,
        'base_contract': pin(PLANS / (OLD + '.json')),
        'previous_representation_overlay': pin(REC / 'contract-revision-overlay.json'),
        'authorization_subject': old['AUTHORITATIVE_QUALIFICATION_SCOPE_SUBJECT'],
        'scope_decision': old['SELECTED_OPTION'],
        'preserved_files': preserved_files,
        'prior_sealed_artifacts_rewritten': False,
        'preserved_semantics': ['Exact retained start and two-event CHECK/COLLECT prefix', 'A04 native Action, operation and output inventory',
            'Authored source bytes and six independently evaluated validation rules', 'Result/dossier/post-Snapshot oracles',
            'No extra grant or pre-A04 setup/INSTALL event', 'Exact parent and sequence3/index2 occurrence/ancestry',
            '24 sealed negatives, END A04-only replacement mapping, N12/N13 mapping',
            'Original A03/A04 historical UNPROVEN labels; no new historical alias', 'P05 stays10/13 and unexecuted'],
        'explicitly_superseded': ['Inline validation/source-addition event-payload requirement already superseded by representation overlay',
            'Unresolved detached historical operand/source enrollment/retry/replay representation now defined by this contract',
            'Old missing-event-identity blocker now replaced by unchanged native representational event ID and future bundle binding oracle'],
        'future_bundle_identity_change': 'Additive bundle-level replay binding introduces a new comparison post-bundle ID only; sealed start, post-Snapshot, SuppliedResult and native event identity remain exact',
        'not_superseded': ['Old RESULT=PARTIAL is historical immutable report', 'Execution readiness remains NO',
            'State-level T02 is not relabeled as durable event qualification', 'Prospective replacement is not original history',
            'No user scope or event schema change'],
        'later_implementation_package': 'Implement/independently qualify generic dossier materialization commit, detached Snapshot resolver, bundle binding/prefix source handling and historical replay. Do not execute the primary prospective A04 yet.',
        'later_execution_package': 'Only after generic qualification and all sealed entry checks pass: execute prospective A04 once from exact start, verify actual result/event/archive, restore/replay/negatives and A04-only END mapping; stop on divergence',
        'P05_effect': 'This contract applies no binding. Successful later authorized execution may close A04 only (10->11/13); A05/A06 and full original END ancestry remain separate unresolved requirements',
        'N12_mapping': 'Preserved: readiness/selection/history != execution; only complete actual native transaction proves PREPARE occurrence',
        'N13_mapping': 'Preserved: declared accepted output != supplied result; exact actual native result and complete event/Snapshot/typed checks required',
    }
    save('versioned-overlay.json', overlay)

    gates_ready = {name: 'COMPLETE_CONTRACT_NOT_RUNTIME_QUALIFICATION' for name in (
        'transaction_operands', 'transaction_outputs', 'Snapshot_binding', 'event_binding', 'atomicity', 'idempotence',
        'PersistenceBundle', 'cold_restore', 'replay', 'identity_order_and_cycles', 'negative_suite')}
    evidence = {name[:-5].replace('/', '_'): pin(OUT / name) for name in (
        'source-pins.json', 'existing-path.json', 'transaction-contract.json', 'snapshot-event-binding.json',
        'durable-commit-contract.json', 'replay-contract.json', 'identity-order.json',
        'oracles/prospective-native-binding.json', 'negative-contract.json', 'versioned-overlay.json')}
    report = {
        'WORK_PACKAGE': 'E2-P05-A04-DURABLE-ADMISSION-CONTRACT', 'RESULT': 'PASS',
        'RESULT_SCOPE': 'Complete contract and versioned overlay; no native implementation, durable transaction or execution qualification',
        **LABELS,
        'SELECTED_OPTION': old['SELECTED_OPTION'], 'AUTHORIZATION_SUBJECT': old['AUTHORITATIVE_QUALIFICATION_SCOPE_SUBJECT'],
        'EXISTING_PREPARE_PATH': path,
        'DURABILITY_GAPS': path['gaps'],
        'TRANSACTION_OPERANDS': transaction['public_operands'], 'TRANSACTION_OUTPUTS': transaction['outputs'],
        'TRANSACTION_ORDER': transaction['order'],
        'POST_SNAPSHOT_BINDING': storage,
        'EVENT_BINDING': storage['native_relationships'],
        'ATOMICITY': commit,
        'IDEMPOTENCE': {k: v for k, v in commit.items() if 'retry' in k},
        'PERSISTENCE_BUNDLE_CONTRACT': storage['post_bundle_required_contents'],
        'COLD_RESTORE_CONTRACT': {'inputs': replay['cold_restore_inputs'], 'order': replay['cold_restore_order'], 'writer_memory_required': False},
        'REPLAY_CONTRACT': replay,
        'IDENTITY_DEPENDENCY_ORDER': identity, 'IDENTITY_CYCLE': 'NO',
        'REUSED_NATIVE_CAPABILITIES': ['qualified T02 admit_dossier_materialization state semantics',
            'native Snapshot/model/PLANNER-SNAPSHOT-1 codec and hash', 'unchanged ExecutionEvent/SuppliedResult/event identity',
            'PersistenceBundle canonical model/PLANNER-BUNDLE-1 with default-omitting extension convention',
            'source/policy pin verification', 'immutable file creation and local lock', 'PLANNER-HEAD-1 publication/audit'],
        'NEW_CAPABILITY': 'Generic persisted dossier/PREPARE integration: detached Snapshot resolver, minimal bundle replay/source-boundary binding, T02 event dispatch, durable retry and historical replay. Not a new A04-only store or a defect in all ordinary result transactions.',
        'NEW_CAPABILITY_SCOPE': 'GENERIC_DOSSIER_PREPARE_INTEGRATION',
        'NEGATIVE_CONTRACT': negatives,
        'IMPLEMENTATION_READINESS_GATES': gates_ready,
        'A04_DURABLE_TRANSACTION_IMPLEMENTATION_READY': 'YES',
        'EXISTING_PATH_SATISFIES_CONTRACT_UNCHANGED': 'NO',
        'PROSPECTIVE_A04_EXECUTION_READY': 'NO',
        'A04_EXECUTED': 'NO', 'PROSPECTIVE_A04_EXECUTED': 'NO', 'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO',
        'P05_BOUND_STAGE_INPUTS': 10, 'P05_EXECUTION_READY': 'NO',
        'P03_HISTORICAL_CORRESPONDENCE': 'UNPROVEN', 'N_REAL_SATISFIED': 'NO',
        'RUNTIME_MODIFIED': 'NO', 'E1_ARTIFACTS_MODIFIED': 0, 'PRODUCTION_EFFECT': 'NO',
        'ACTUAL_DURABLE_TRANSACTION': 'NOT_RUN', 'ACTUAL_COLD_RESTORE': 'NOT_RUN', 'ACTUAL_REPLAY': 'NOT_RUN',
        'ACTUAL_NEGATIVE_QUALIFICATION': 'NOT_RUN',
        'COMPARISON_EVENT_ID': oracle['EXPECTED_EVENT_ID'],
        'COMPARISON_POST_SNAPSHOT_ID': oracle['EXPECTED_POST_SNAPSHOT_ID'],
        'COMPARISON_FUTURE_BUNDLE_ID': oracle['EXPECTED_FUTURE_BUNDLE_ID_COMPARISON_ONLY'],
        'NEXT_PACKAGE': 'Generic native dossier durable admission/replay implementation and independent qualification',
        'evidence': evidence,
        'verification_artifact': str((OUT / 'verification.json').relative_to(ROOT)),
    }
    report_path = PLANS / (NAME + '.json')
    raw = (json.dumps(report, sort_keys=True, indent=2) + '\n').encode()
    if report_path.exists() and report_path.read_bytes() != raw:
        raise AssertionError('report conflict')
    report_path.write_bytes(raw)
    assert not BARRED
    print(json.dumps({'RESULT': 'PASS', 'scope': 'CONTRACT_ONLY', 'implementation_ready': 'YES',
        'execution_ready': 'NO', 'event_ORACLE_ONLY': oracle['EXPECTED_EVENT_ID'],
        'post_snapshot_ORACLE_ONLY': oracle['EXPECTED_POST_SNAPSHOT_ID'],
        'future_bundle_ORACLE_ONLY': oracle['EXPECTED_FUTURE_BUNDLE_ID_COMPARISON_ONLY'], 'barred_calls': BARRED}, sort_keys=True))


if __name__ == '__main__':
    main()
