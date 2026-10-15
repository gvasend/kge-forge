"""Execute only the sealed authored PREPARE source and admitted prerequisites.

This producer does not load oracle files, expected objects, reports, or historical
handoffs. Its fresh dossier and six independent rule decisions are operation
outputs. The execution harness separately compares them with immutable oracles.
"""
from dataclasses import replace

from adapter.planner import codec as c, core, dossier_transaction as dt, model as m
from adapter.planner.gates import evaluate_predicate


def execute(snapshot, artifacts, prefix, audit, presentation='original'):
    audit['producer_invocations'] += 1
    dt.require(len(artifacts) == 1, 'A04_ONE_AUTHORED_SOURCE')
    pin, raw = artifacts[0]
    data = c.parse_json(raw)
    audit['operation_inputs'] = [pin.path, 'EXACT_RETAINED_NATIVE_PRE_BUNDLE']
    audit['oracle_files_read_by_producer'] = []
    ctx = snapshot.context
    dt.require((data['scope'], data['lineage'], data['generation']) ==
               (ctx.scope, ctx.lineage, ctx.generation), 'A04_SOURCE_CONTEXT')
    dt.require(c.snapshot_id(snapshot) == c.snapshot_id(prefix.current), 'A04_PRODUCER_PRE_STATE')
    dt.require(len(prefix.events) == 2 and [e.result.action.value for e in prefix.events] ==
               ['E2-CHECK', 'E2-COLLECT'], 'A04_NATIVE_PREREQUISITE_HISTORY')
    previous, state = None, c.snapshot_id(prefix.initial)
    for number, event in enumerate(prefix.events, 1):
        dt.require(event.sequence == number and event.parent_event == previous and
                   event.parent_snapshot == state and event.identity == c._event_identity(
                   number, state, previous, event.result, event.after_snapshot, event.resume_binding),
                   'A04_INPUT_EVENT_BINDING')
        previous, state = event.identity, event.after_snapshot
    dt.require(state == c.snapshot_id(snapshot), 'A04_PREFIX_CURRENT_STATE')
    declaration = data['dossier_declaration']
    p = m.Provenance(pin.path, c._identity(raw, 'raw-file-sha256'), '/dossier_declaration',
                     c.canonical_bytes(declaration).decode(),
                     'PROSPECTIVE_A04_AUTHORED_DOSSIER_DEFINITION', ctx.scope)
    checks = tuple(m.DecisionCheck(m.DossierCheck(name), m.PredicateId('E2-CHECK-' + name), p)
                   for name in declaration['checks'])
    dossier = m.DecisionDossier(m.ActionId(declaration['decision']), p, declaration['question'],
        declaration['scope'], tuple(declaration['alternatives']), checks,
        tuple(m.PredicateId(ref) for ref in declaration['required_facts']),
        tuple(declaration['deferred_downstream_facts']),
        declaration['authority_granted_if_approved'], declaration['authority_excluded'])
    facts = {ref.value: evaluate_predicate(snapshot, ref).state is m.ProofState.PROVED
             for ref in dossier.required_facts}
    prerequisite_outputs = all(
        any(k.id == output.id and k == output for k in snapshot.knowledge) and
        core.current_completion(snapshot, event.result.action)
        for event in prefix.events for output in event.result.knowledge)
    decisions = {
        'QUESTION_SCOPE': bool(declaration['question']) and dossier.question == declaration['question']
                          and dossier.scope == ctx.scope == data['scope'],
        'SOURCE_PROVENANCE': pin.identity == p.identity == c._identity(raw, 'raw-file-sha256')
                             and p.section == '/dossier_declaration'
                             and p.excerpt == c.canonical_bytes(declaration).decode()
                             and prerequisite_outputs,
        'CONCRETE_ALTERNATIVES': len(dossier.alternatives) == 2 and
            set(dossier.alternatives) == {'ALLOW_QUALIFICATION_MAPPING', 'DECLINE'},
        'AUTHORITY_BOUNDARY': bool(dossier.authority_excluded) and
            'independent applicable synthetic grant is still required' in dossier.authority_granted_if_approved
            and 'No production' in dossier.authority_excluded
            and data['production_effect'] is False and data['no_world_facts'] is True
            and all(d.record is None and d.recorded_choice is None for d in snapshot.decisions),
        'DECISION_FACTS_COMPLETE': set(facts) == {'E2-KP-CHECK', 'E2-KP-COLLECT'} and all(facts.values()),
    }
    decisions['INDEPENDENT_VALIDATION'] = all(decisions.values()) and (
        set(data['checks_native']) == {kind.value for kind in m.SUPPORTED_DOSSIER_CHECKS}
        and all(check.provenance == p for check in checks)
        and len(data['validation_rules']) == 6)
    did = c._identity(c.canonical_bytes(c._wire(dossier)), 'planner-dossier-sha256')
    validations = tuple(m.ValidationInstance(check.predicate, check.kind.value, did,
        (c.snapshot_id(snapshot), pin.identity),
        m.ValidationOutcome.PASS if decisions[check.kind.value] else m.ValidationOutcome.FAIL,
        ctx.scope, ctx.lineage,
        m.ValidationState.ACCEPTED if decisions[check.kind.value] else m.ValidationState.REJECTED, p)
        for check in checks if check.kind in m.SUPPORTED_DOSSIER_CHECKS)
    action = next(a for a in snapshot.actions if a.operation is m.OperationClass.DECISION_INPUT_ACQUISITION)
    dt.require(len(action.accepted_inventory) == 1, 'A04_EXACT_OUTPUT_CONTRACT')
    # Fresh bounded output from the admitted native inventory; no external fact.
    outputs = tuple(replace(k) for k in action.accepted_inventory)
    supplied = m.SuppliedResult(action.id, m.ActionResult.PASS, outputs, c.snapshot_id(snapshot), dossier)
    audit['independent_rule_evaluations'] = decisions
    audit['prerequisite_predicates'] = facts
    if presentation != 'original':
        permute = (lambda v: v[::-1]) if presentation == 'reverse' else (lambda v: v[1:] + v[:1])
        supplied = replace(supplied, knowledge=permute(supplied.knowledge), dossier=replace(dossier,
            checks=permute(dossier.checks), alternatives=permute(dossier.alternatives),
            required_facts=permute(dossier.required_facts)))
        validations = permute(validations)
    return supplied, validations
