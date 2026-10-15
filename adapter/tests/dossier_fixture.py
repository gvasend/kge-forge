"""Independent D01 fixture. No E2/A04 inputs, oracles, IDs or transactions."""
import json
from dataclasses import replace
from pathlib import Path

from adapter.planner import codec as c, core, model as m, selector, dossier_transaction as dt

REPO = Path(__file__).resolve().parents[2]
SCOPE = 'D01-ISOLATED-QUALIFICATION'
LINEAGE = 'D01-GENERIC-QUALIFICATION-1'
BUILD = m.ActionId('GENERIC-DOSSIER-BUILD')
REVIEW = m.ActionId('GENERIC-REVIEW')
ACQUIRE = m.ActionId('GENERIC-ACQUIRE')


def packet():
    return {'schema': 'ISOLATED-DOSSIER-SOURCE-1', 'scope': SCOPE,
            'question': 'Choose one bounded qualification option', 'alternatives': ['KEEP', 'DECLINE'],
            'authority_granted_if_approved': 'Only this bounded qualification option',
            'authority_excluded': 'Production, unrelated decisions and release qualification',
            'required_fact': 'GENERIC-ACQUIRED-FACT'}


def provenance(path, raw, scope=SCOPE, section='/'):
    return m.Provenance(path, c._identity(raw, 'raw-file-sha256'), section,
                        raw.decode(), 'AUTHORED_ISOLATED_QUALIFICATION', scope)


def create(root):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    raw = c.canonical_bytes({'schema': 'GENERIC-D01-ACTIONS-1', 'qualification_only': True})
    (root / 'actions.json').write_bytes(raw)
    p = provenance('actions.json', raw)
    ka = m.KnowledgeRecord(m.KnowledgeId('GENERIC-ACQUIRED'), m.KnowledgeState.KNOWN_COMPLETE,
            'Bounded prerequisite acquired', p, producer=ACQUIRE, outcome=m.ActionResult.PASS)
    kb = m.KnowledgeRecord(m.KnowledgeId('GENERIC-DOSSIER-OUTPUT'), m.KnowledgeState.KNOWN_COMPLETE,
            'Actual bounded dossier output', p, producer=BUILD, outcome=m.ActionResult.PASS)
    acquire = m.Action(ACQUIRE, m.OperationClass.SOURCE_ACQUISITION, m.EffectClass.NON_EFFECTING, (), p, (ka,))
    build = m.Action(BUILD, m.OperationClass.DECISION_INPUT_ACQUISITION, m.EffectClass.NON_EFFECTING,
            (m.Gate(m.GateKind.ACTION_COMPLETED, ACQUIRE),), p, (kb,))
    review = m.Action(REVIEW, m.OperationClass.ARCHITECT_CONTRACT_DECISION, m.EffectClass.NON_EFFECTING, (), p, ())
    decision = m.Decision(REVIEW, None, BUILD, 'bounded generic dossier', m.DecisionStage.DECISION_INPUTS_REQUIRED, p)
    state = m.Snapshot((acquire, build, review),
            (m.ActionStatus(ACQUIRE, m.ActionState.ACTIONABLE), m.ActionStatus(BUILD, m.ActionState.ACTIONABLE),
             m.ActionStatus(REVIEW, m.ActionState.WAITING)), (), (), (),
            predicates=(m.Predicate(m.PredicateId('GENERIC-ACQUIRED-FACT'), m.PredicateKind.KNOWLEDGE_ACCEPTED,
                                    knowledge=ka.id),),
            context=m.EvaluationContext(SCOPE, LINEAGE, 'D01-GENERIC-GENERATION-1', 0), decisions=(decision,))
    policy = selector.POLICY_PIN
    target = root / policy.path
    target.parent.mkdir(parents=True)
    target.write_bytes((REPO / policy.path).read_bytes())
    initial = m.PersistenceBundle(state, (), state, (m.ArtifactPin(p.path, p.identity),), policy, 'E1-SELECTION-1-P06')
    start = c.record_result(initial, m.SuppliedResult(ACQUIRE, m.ActionResult.PASS, (replace(ka),), c.snapshot_id(state)))
    data = c.canonical_bytes(packet())
    pin = m.ArtifactPin('dossier-input.json', c._identity(data, 'raw-file-sha256'))
    # New input is intentionally offline, to qualify atomic source enrollment.
    return start, ((pin, data),)


def produce(snapshot, artifacts, presentation='original'):
    pin, raw = artifacts[0]
    data = c.parse_json(raw)
    dt.require(set(data) == set(packet()) and data['schema'] == 'ISOLATED-DOSSIER-SOURCE-1', 'GENERIC_INPUT_SCHEMA')
    p = provenance(pin.path, raw)
    checks = tuple(m.DecisionCheck(kind, m.PredicateId('GENERIC-CHECK-' + kind.value), p)
                   for kind in sorted(m.SUPPORTED_DOSSIER_CHECKS, key=lambda x: x.value))
    dossier = m.DecisionDossier(REVIEW, p, data['question'], data['scope'], tuple(data['alternatives']), checks,
                (m.PredicateId(data['required_fact']),), ('downstream fact intentionally deferred',),
                data['authority_granted_if_approved'], data['authority_excluded'])
    # Each rule is evaluated independently from pinned actual inputs, not from an
    # expected state, result, validation tuple or report.
    from adapter.planner.gates import evaluate_predicate
    evaluations = {
        m.DossierCheck.QUESTION_SCOPE: bool(dossier.question) and dossier.scope == snapshot.context.scope,
        m.DossierCheck.SOURCE_PROVENANCE: c._identity(raw, 'raw-file-sha256') == pin.identity,
        m.DossierCheck.CONCRETE_ALTERNATIVES: len(set(dossier.alternatives)) == len(dossier.alternatives) >= 2,
        m.DossierCheck.AUTHORITY_BOUNDARY: bool(dossier.authority_granted_if_approved and dossier.authority_excluded),
        m.DossierCheck.DECISION_FACTS_COMPLETE: all(evaluate_predicate(snapshot, ref).state is m.ProofState.PROVED
                                                    for ref in dossier.required_facts),
        m.DossierCheck.INDEPENDENT_VALIDATION: all(check.provenance.identity == pin.identity for check in checks)
                                             and dossier.validation is m.ValidationState.ACCEPTED,
    }
    did = c._identity(c.canonical_bytes(c._wire(dossier)), 'planner-dossier-sha256')
    validations = tuple(m.ValidationInstance(ch.predicate, ch.kind.value, did,
            (c.snapshot_id(snapshot), pin.identity), m.ValidationOutcome.PASS if evaluations[ch.kind] else m.ValidationOutcome.FAIL,
            snapshot.context.scope, snapshot.context.lineage,
            m.ValidationState.ACCEPTED if evaluations[ch.kind] else m.ValidationState.REJECTED, p) for ch in checks)
    action = next(a for a in snapshot.actions if a.id == BUILD)
    supplied = m.SuppliedResult(action.id, m.ActionResult.PASS, tuple(replace(k) for k in action.accepted_inventory),
                               c.snapshot_id(snapshot), dossier)
    if presentation != 'original':
        permute = (lambda v: v[::-1]) if presentation == 'reverse' else (lambda v: v[1:] + v[:1])
        supplied = replace(supplied, dossier=replace(dossier, checks=permute(dossier.checks),
                         alternatives=permute(dossier.alternatives)), knowledge=permute(supplied.knowledge))
        validations = permute(validations)
    return supplied, validations


def oracle(before, after, event):
    """Independent state boundary: explicit allowed fields and expected lifecycle."""
    allowed = {'actions', 'statuses', 'knowledge', 'decisions', 'validation_instances'}
    from dataclasses import fields
    for field in fields(m.Snapshot):
        if field.name not in allowed:
            dt.require(getattr(before, field.name) == getattr(after, field.name), 'GENERIC_FRAME:' + field.name)
    dt.require(event.parent_snapshot == c.snapshot_id(before) and event.after_snapshot == c.snapshot_id(after), 'GENERIC_SNAPSHOT_BINDING')
    dt.require(event.result.action == BUILD and event.result.result is m.ActionResult.PASS, 'GENERIC_ACTUAL_RESULT')
    dt.require(next(s for s in after.statuses if s.id == BUILD).state is m.ActionState.COMPLETED, 'GENERIC_COMPLETION')
    dt.require(next(s for s in after.statuses if s.id == ACQUIRE) == next(s for s in before.statuses if s.id == ACQUIRE), 'GENERIC_UNRELATED_ACTION')
    dt.require(len(after.knowledge) == 2 and len(after.validation_instances) == 6, 'GENERIC_OUTPUTS')
    decision = after.decisions[0]
    dt.require(decision.stage is m.DecisionStage.DECISION_READY and decision.record is None and decision.recorded_choice is None,
               'GENERIC_DECISION_NOT_EXECUTED')
    dt.require(decision.history == (m.DecisionStage.DECISION_INPUT_ACQUISITION, m.DecisionStage.DECISION_DOSSIER_READY,
                                  m.DecisionStage.DECISION_READY), 'GENERIC_DECISION_HISTORY')
    dt.require(not after.entities and not after.typed_proofs and not after.installed_definitions, 'GENERIC_NO_UNAUTHORIZED_ADVANCEMENT')
    return True


def expected(start, artifacts):
    """Seal a complete comparison oracle without invoking operation/admission."""
    pin, raw = artifacts[0]
    p = provenance(pin.path, raw)
    checks = tuple(m.DecisionCheck(kind, m.PredicateId('GENERIC-CHECK-' + kind.value), p)
                   for kind in sorted(m.SUPPORTED_DOSSIER_CHECKS, key=lambda x: x.value))
    data = packet()
    dossier = m.DecisionDossier(REVIEW, p, data['question'], SCOPE, ('KEEP', 'DECLINE'), checks,
        (m.PredicateId('GENERIC-ACQUIRED-FACT'),), ('downstream fact intentionally deferred',),
        data['authority_granted_if_approved'], data['authority_excluded'])
    sid = c.snapshot_id(start.current)
    did = c._identity(c.canonical_bytes(c._wire(dossier)), 'planner-dossier-sha256')
    vs = tuple(m.ValidationInstance(ch.predicate, ch.kind.value, did, (sid, pin.identity),
            m.ValidationOutcome.PASS, SCOPE, LINEAGE, m.ValidationState.ACCEPTED, p) for ch in checks)
    build = next(a for a in start.current.actions if a.id == BUILD)
    supplied = m.SuppliedResult(BUILD, m.ActionResult.PASS, build.accepted_inventory, sid, dossier)
    decision = replace(start.current.decisions[0], dossier=dossier, stage=m.DecisionStage.DECISION_READY,
            history=(m.DecisionStage.DECISION_INPUT_ACQUISITION, m.DecisionStage.DECISION_DOSSIER_READY, m.DecisionStage.DECISION_READY))
    after = replace(start.current, actions=tuple(replace(a, prepared_dossier=dossier) if a.id == BUILD else a for a in start.current.actions),
            statuses=tuple(replace(s, state=m.ActionState.COMPLETED if s.id == BUILD else m.ActionState.ACTIONABLE)
                           if s.id in (BUILD, REVIEW) else s for s in start.current.statuses),
            knowledge=tuple(sorted(start.current.knowledge + build.accepted_inventory, key=lambda k: k.id.value)),
            decisions=(decision,), validation_instances=vs)
    aid = c.snapshot_id(after)
    ordinal = len(start.events) + 1
    parent = start.events[-1].identity
    event = m.ExecutionEvent(ordinal, sid, parent, supplied, aid, c._event_identity(ordinal, sid, parent, supplied, aid))
    binding = m.DossierMaterializationBinding(event.identity, c.bundle_id(start), (pin,))
    final = replace(start, events=start.events+(event,), current=after, sources=start.sources+(pin,), dossier_materializations=(binding,))
    return final, c._identity(c._bundle_bytes_admitted(final), 'planner-bundle-v1')
