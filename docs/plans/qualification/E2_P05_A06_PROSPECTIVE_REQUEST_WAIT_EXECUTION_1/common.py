"""Qualification harness only. Native implementation and sealed oracles are read-only."""
from dataclasses import fields, is_dataclass, replace
from enum import Enum
import hashlib
import json
from pathlib import Path

from adapter.planner import codec as c, core, gates, model as m

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
SEALED = ROOT / 'docs/plans/qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1'
CONTRACT = ROOT / 'docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1.json'
LABELS = {
    'QUALIFICATION_TYPE': 'PROSPECTIVE_REPLACEMENT',
    'ORIGINAL_A06_HISTORICAL_REQUEST_WAIT_TRACE': 'UNPROVEN',
    'HISTORICAL_RECONSTRUCTION': 'NO',
    'PROSPECTIVE_A06_TRACE_IS_ORIGINAL_TRACE': 'NO',
}


class Divergence(Exception):
    def __init__(self, term, expected, actual, state=None, event=None):
        def display(value):
            if isinstance(value, bytes):
                return {'raw_sha256': hashlib.sha256(value).hexdigest(), 'length': len(value)}
            try:
                return json.loads(json.dumps(value))
            except TypeError:
                return c._wire(value)
        self.record = {'FIRST_COUNTEREXAMPLE': term, 'EXPECTED': display(expected),
                       'ACTUAL': display(actual), 'STATE_ID': state, 'EVENT_ID': event,
                       'CLASSIFICATION': 'SEALED_ORACLE_DIVERGENCE'}
        super().__init__(json.dumps(self.record, sort_keys=True))


def equal(term, actual, expected, state=None, event=None):
    if actual != expected:
        raise Divergence(term, expected, actual, state, event)


def read(path):
    return json.loads(Path(path).read_bytes())


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def aid(identity):
    return None if identity is None else identity.namespace + ':' + identity.sha256


def report_view(value):
    """Metadata view of derived computations, never a native persisted operand."""
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {field.name: report_view(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, (tuple, list)):
        return [report_view(child) for child in value]
    if value is None or type(value) in (str, int, bool):
        return value
    raise TypeError('Unsupported report metadata')


def identity(value):
    namespace, sha256 = value.rsplit(':', 1)
    return m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, namespace, sha256)


def save(path, value):
    path = Path(path)
    raw = (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode()
    if path.exists():
        equal('immutable execution evidence', path.read_bytes(), raw)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)


def ref(path, pointer=''):
    path = Path(path)
    return {'path': str(path.relative_to(ROOT)), 'raw_sha256': digest(path), 'pointer': pointer}


def refs(value):
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and isinstance(value.get('raw_sha256'), str):
            yield value
        for child in value.values():
            yield from refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from refs(child)


def pointer(value, expression):
    for part in expression.split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def verify_refs(document, cache=None):
    cache = {} if cache is None else cache
    checked = []
    for item in refs(document):
        path = ROOT / item['path']
        if item['path'] not in cache:
            cache[item['path']] = digest(path)
        equal('sealed file ' + item['path'], cache[item['path']], item['raw_sha256'])
        if item.get('pointer') and path.suffix == '.json':
            pointer(read(path), item['pointer'])
        checked.append(item['path'])
    return checked


def fixture(variant):
    fixtures = read(SEALED / 'sealed-fixtures.json')
    return next(f for f in [fixtures['primary']] + fixtures['independent_reproductions']
                if f['variant'] == variant)


def entry():
    contract = read(CONTRACT)
    required = {
        'SELECTED_OPTION': 'AUTHORIZE_PROSPECTIVE_P05_A06_REQUEST_WAIT_QUALIFICATION',
        'RESULT': 'PASS', 'PROSPECTIVE_A06_EXECUTION_READY': 'YES',
        'ADDITIONAL_AUTHORITY_REQUIRED': 'NO', 'N12_MAPPING_PRESERVED': 'YES',
        'N13_MAPPING_PRESERVED': 'YES', 'PROSPECTIVE_A06_EXECUTED': 'NO',
        'P05_BOUND_STAGE_INPUTS': 12,
    }
    for key, expected in dict(LABELS, **required).items():
        equal('entry ' + key, contract[key], expected)
    cache, paths = {}, set()
    for path in sorted(SEALED.rglob('*.json')) + [CONTRACT]:
        if path.name == 'baseline.json':
            continue
        paths.update(verify_refs(read(path), cache))
    verification = read(SEALED / 'verification.json')
    for item in verification['report_pins'] + verification['script_pins']:
        equal('sealed report/code ' + item['path'], digest(ROOT / item['path']), item['raw_sha256'])
    auth = read(SEALED / 'authorization-capture.json')
    dossier = read(ROOT / auth['scope_dossier']['path'])
    subject = 'qualification-scope-subject-v1:' + hashlib.sha256(c.canonical_bytes(dossier['subject'])).hexdigest()
    equal('scope subject', subject, auth['scope_subject_identity'])
    equal('selected scope', auth['SELECTED_OPTION'], required['SELECTED_OPTION'])
    equal('additional authority', auth['ADDITIONAL_AUTHORITY_REQUIRED'], 'NO')
    equal('native grants', auth['native_grants_issued_or_reused'], 0)
    graph = read(ROOT / read(SEALED / 'post-A06-complete-P05-readiness-oracle.json')['current_graph']['path'])
    equal('prior stage coverage', graph['P05_BOUND_STAGE_INPUTS'], 12)
    equal('A06 missing', graph['stage_bindings'][5]['binding_status'], 'MISSING_CANONICAL_OUTPUT')
    # No execution output or native committed occurrence can preexist this package.
    equal('primary execution not yet run', (OUT / 'runs/primary-seed-0/commit-1.json').exists(), False)
    return dict(LABELS, RESULT='PASS', checks=required, sealed_files=len(paths),
                verified_paths=sorted(paths), scope_subject=subject,
                original_recovery_dossier_unchanged=True, authority_issued=False)


def state_check(bundle, spec, boundary):
    """Actual native Computation, compared to the already sealed state oracle."""
    expected = read(ROOT / spec['EXPECTED_STATE_ORACLES'][boundary]['path'])
    state = bundle.current
    sid = aid(c.snapshot_id(state))
    raw = c.snapshot_bytes(state)
    wanted = (ROOT / spec['EXPECTED_STATE_ORACLES'][boundary + '_snapshot']['path']).read_bytes()
    equal('full canonical Snapshot ' + boundary, hashlib.sha256(raw).hexdigest(),
          hashlib.sha256(wanted).hexdigest(), sid)
    computation = core.recompute(state)
    proof = gates.obligation_proof(state, state.evidence_requirements[0].id)
    resume = core.resume_eligibility(bundle, ROOT)
    actual = {
        'snapshot_identity': sid, 'bundle_comparison_identity': aid(c.bundle_id(bundle)),
        'CONTROL': computation.control.value, 'gate_stage': state.external_gates[0].stage.value,
        'gate_history': [stage.value for stage in state.external_gates[0].history],
        'event_count': len(bundle.events), 'append_head': aid(bundle.events[-1].identity) if bundle.events else None,
        'persisted_Action_status': {s.id.value: s.state.value for s in state.statuses},
        'computed_Action_status': {s.id.value: s.state.value for s in computation.statuses},
        'computed_blockers': list(dict(computation.blocked)[state.actions[0].id]),
        'actionable': [a.value for a in computation.actionable],
        'human_ready': list(computation.human_batches),
        'selected': computation.selection.selected.value if computation.selection else None,
        'obligation_Proof': {'state': proof.state.value, 'reasons': list(proof.reasons)},
        'root': {r.id.value: r.state.value for r in state.roots},
        'slots': [s.id.value for s in state.slots],
        'completed_Actions': [s.id.value for s in state.statuses if s.state is m.ActionState.COMPLETED],
        'Knowledge': [k.id.value for k in state.knowledge],
        'ActionResults': [aid(e.identity) for e in bundle.events if type(e.result) is m.SuppliedResult],
        'evidence': [e.id.value for e in state.entities], 'receipt': list(state.receipt_admissions),
        'validation_results': list(state.validation_results) + list(state.validation_instances),
        'support': list(state.validation_support_records), 'typed_proofs': list(state.typed_proofs),
        'native_authorities': list(state.entities), 'human_decisions': list(state.decisions),
        'scope': state.context.scope, 'lineage': state.context.lineage, 'generation': state.context.generation,
    }
    for key, actual_value in actual.items():
        equal(boundary + ':' + key, actual_value, expected[key], sid)
    equal('ResumeEligibility.allowed', resume.allowed, expected['ResumeEligibility']['allowed'], sid)
    equal('ResumeEligibility.actions', list(resume.actions), expected['ResumeEligibility']['actions'], sid)
    for required in expected['ResumeEligibility']['required_missing_predicates']:
        equal('ResumeEligibility premise ' + required, any(required in r for r in resume.reasons), True, sid)
    equal('no PLAN_DEFECT', computation.defects, (), sid)
    c._verify_sources(bundle, ROOT)
    c._check_snapshot_pins(state, bundle.sources)
    equal('query is read-only', c.snapshot_bytes(bundle.current), raw, sid)
    return {'RESULT': 'PASS', 'boundary': boundary, 'actual': actual,
            'native_Computation_metadata': report_view(computation), 'native_ResumeEligibility': c._wire(resume),
            'source_policy_pins': 'PASS', 'comparison': ref(ROOT / spec['EXPECTED_STATE_ORACLES'][boundary]['path'])}


def trace_check(bundle, spec, count=2):
    equal('native trace type', type(bundle).__name__, 'PersistenceBundle')
    equal('exact event count', len(bundle.events), count)
    previous = None
    records = []
    for index, actual in enumerate(bundle.events):
        expected = spec['EXPECTED_EVENT_ORACLE'][index]
        expected_raw = (ROOT / expected['expected_event_file']['path']).read_bytes()
        equal('native event bytes', c.canonical_bytes(c._wire(actual)), expected_raw,
              aid(actual.after_snapshot), aid(actual.identity))
        equal('sequence', actual.sequence, index + 1)
        equal('parent continuity', actual.parent_event, previous)
        equal('event/result pre-state', actual.parent_snapshot, actual.result.expected_snapshot)
        equal('actual phase result type', type(actual.result).__name__, 'ExternalEvent')
        equal('actual event ID', aid(actual.identity), expected['EVENT_ID'])
        records.append({'event': c._wire(actual), 'event_id': aid(actual.identity),
                        'ledger_position': index, 'oracle': ref(ROOT / expected['expected_event_file']['path'])})
        previous = actual.identity
    state_check(bundle, spec, 'post-trace' if count == 2 else 'request-ready')
    return {'RESULT': 'PASS', 'events': records, 'ordering': 'PASS', 'ledger_membership': 'PASS',
            'ledger_id': aid(c.bundle_id(bundle)) + '#/bundle/events',
            'root': aid(bundle.events[0].identity), 'head': aid(bundle.events[-1].identity)}


def bundle_path(store, value):
    return Path(store) / ('bundle-' + identity(value).sha256 + '.json')


def permutation(bundle, form):
    def perm(seq):
        if form == 'reversed':
            return tuple(reversed(seq))
        if form == 'rotated':
            return seq[1:] + seq[:1]
        return seq
    if form not in ('original', 'reversed', 'rotated'):
        raise ValueError('Unsealed permutation')
    return replace(bundle, initial=replace(bundle.initial, predicates=perm(bundle.initial.predicates)),
                   current=replace(bundle.current, predicates=perm(bundle.current.predicates)),
                   sources=perm(bundle.sources))


def semantic_projection(bundle):
    gate = bundle.current.external_gates[0]
    request = gate.resolution_contracts[0]
    result = core.recompute(bundle.current)
    return {'stages': [e.result.stage.value for e in bundle.events],
            'request': request.request, 'gate': gate.id.value, 'proposition': request.proposition,
            'target': c._wire(request.target), 'producers': c._wire(request.producers),
            'held_actions': c._wire(request.held_actions), 'reentry': c._wire(request.reentry),
            'positions': [e.sequence for e in bundle.events],
            'null_first_parent': bundle.events[0].parent_event is None,
            'second_parent_is_first': bundle.events[1].parent_event == bundle.events[0].identity,
            'gate_stage': gate.stage.value, 'gate_history': [s.value for s in gate.history],
            'rule_known': bundle.current.evidence_requirements[0].rule_known,
            'CONTROL': result.control.value, 'actionable': c._wire(result.actionable),
            'effects': {'Knowledge': len(bundle.current.knowledge), 'entities': len(bundle.current.entities),
                       'receipts': len(bundle.current.receipt_admissions),
                       'proofs': len(bundle.current.typed_proofs), 'decisions': len(bundle.current.decisions),
                       'installations': len(bundle.current.installed_definitions),
                       'completion': sum(s.state is m.ActionState.COMPLETED for s in bundle.current.statuses)}}
