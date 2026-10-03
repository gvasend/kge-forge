"""Independent PC01 whole-model fixture/oracle; no Action or event execution."""
import hashlib
import json
import sys
import tempfile
from dataclasses import fields, is_dataclass, replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from adapter.planner import codec as c, core, model as m, selector
from adapter.tests.test_planner_external_unknown import ExternalUnknownTests

SCOPE = "E2-QUALIFICATION-ONLY"
LINEAGE = "E2-CANONICAL-BASELINE-1"
GENERATION = "E2-GENERATION-1"


def _rename(value, old, new):
    if isinstance(value, m.Identifier):
        return type(value)(value.value.replace(old, new))
    if isinstance(value, tuple):
        return tuple(_rename(x, old, new) for x in value)
    if is_dataclass(value):
        vals = {}
        for f in fields(value):
            x = getattr(value, f.name)
            if f.name in ("scope", "lineage", "generation"):
                if f.name == "scope": x = SCOPE
                elif f.name == "lineage": x = LINEAGE
                else: x = GENERATION
            vals[f.name] = _rename(x, old, new)
        return replace(value, **vals)
    return value


def _source(root, name, body):
    raw = c.canonical_bytes(body)
    path = root / name
    path.write_bytes(raw)
    ident = m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, "raw-file-sha256", hashlib.sha256(raw).hexdigest())
    return m.Provenance(name, ident, "/", raw.decode(), "E2-PC01-WHOLE-MODEL-1", SCOPE)


def build():
    helper = ExternalUnknownTests(); helper.setUp()
    root = Path(helper.temp.name)
    state = _rename(helper.state, "TEST-", "E2-")
    # Preserve the authoritative typed prerequisite graph from the PC01
    # source fixture.  The previous constructor rebuilt Actions from a small
    # shape-only loop and silently replaced every prerequisite tuple with ().
    # This mapping is generic: each source Action supplies its own typed
    # prerequisite relations; no ActionId-specific policy is introduced.
    source_fixture = ROOT / "docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_PC01_FIXTURES.json"
    source_value = json.loads(source_fixture.read_text())
    source_actions = {a.id: a for a in
                      (c._unwire(raw) for raw in source_value["native_actions"])}
    source_prerequisites = {action_id: action.prerequisites
                            for action_id, action in source_actions.items()}
    # Preserve the canonical decision-input route declared by the source
    # model.  A DECISION_INPUT_ACQUISITION action is not self-authorizing;
    # native Planner requires a typed Decision whose input_action names that
    # action.  The route is derived from the source dossier's decision owner,
    # and its downstream set is derived from prerequisite edges, so no
    # ActionId-specific route is introduced here.
    decision_routes = []
    for input_action, source_action in sorted(source_actions.items(), key=lambda kv: kv[0].value):
        dossier = source_action.prepared_dossier
        if dossier is None:
            continue
        semantic_action = dossier.decision
        downstream = tuple(sorted((a.id for a in source_actions.values()
                                   if any(g.target == semantic_action for g in a.prerequisites)),
                                  key=lambda x: x.value))
        decision_routes.append(m.Decision(
            action=semantic_action,
            semantic_action=semantic_action,
            input_action=input_action,
            external_input="",
            stage=m.DecisionStage.DECISION_INPUTS_REQUIRED,
            provenance=source_action.source,
            dossier=None,
            downstream=downstream,
        ))
    actions = list(state.actions)
    # Replace the existing held action with the accepted E2-REENTER definition.
    reenter = replace(actions[0], id=m.ActionId("E2-REENTER"), operation=m.OperationClass.DETERMINISTIC_MAPPING,
                      prerequisites=source_prerequisites[m.ActionId("E2-REENTER")],
                      requirements=(m.PredicateId("E2-PROOF"),), source=actions[0].source)
    extras = []
    for name, op in (("E2-COLLECT", m.OperationClass.SOURCE_ACQUISITION),
                     ("E2-CHECK", m.OperationClass.DETERMINISTIC_VALIDATION),
                     ("E2-PREPARE", m.OperationClass.DECISION_INPUT_ACQUISITION),
                     ("E2-DECIDE", m.OperationClass.ARCHITECT_CONTRACT_DECISION),
                     ("E2-FINISH", m.OperationClass.DETERMINISTIC_VALIDATION)):
        prov = _source(root, name + ".json", {"action": name, "scope": SCOPE, "lineage": LINEAGE})
        inv = ()
        if name in ("E2-COLLECT", "E2-CHECK", "E2-PREPARE", "E2-FINISH"):
            inv = (m.KnowledgeRecord(m.KnowledgeId(name.replace("E2-", "E2-K-")), m.KnowledgeState.KNOWN_COMPLETE,
                  "prospective output contract for " + name, prov, (), m.ValidationState.ACCEPTED,
                  m.ActionId(name), m.ActionResult.PASS),)
        extras.append(m.Action(m.ActionId(name), op, m.EffectClass.NON_EFFECTING,
            source_prerequisites[m.ActionId(name)], prov, inv,
            (), (), None, m.ActionStage.DEFAULT, None, "", True, m.ActionResult.PASS, None, m.ValidationState.ACCEPTED))
    actions = tuple(extras + [reenter])
    statuses = tuple(m.ActionStatus(a.id, m.ActionState.ACTION_ELIGIBLE) for a in actions)
    gate = state.external_gates[0]
    gate = replace(gate, id=m.GateId("E2-GATE"), reentry=(m.ActionId("E2-REENTER"),),
                   held_actions=(m.ActionId("E2-REENTER"),))
    req = state.evidence_requirements[0]
    req = replace(req, id=m.EvidenceId("E2-EXTERNAL-REQUIREMENT"), rule_known=True)
    proof = replace(state.predicates[0], id=m.PredicateId("E2-PROOF"), obligation=req.id)
    fact_check = m.Predicate(m.PredicateId("E2-KP-CHECK"), m.PredicateKind.KNOWLEDGE_ACCEPTED,
                             knowledge=m.KnowledgeId("E2-K-CHECK"), action=m.ActionId("E2-CHECK"),
                             expected=next(a for a in actions if a.id == m.ActionId("E2-CHECK")).accepted_inventory[0].provenance.identity,
                             required_outcome=m.ActionResult.PASS)
    fact_collect = m.Predicate(m.PredicateId("E2-KP-COLLECT"), m.PredicateKind.KNOWLEDGE_ACCEPTED,
                                knowledge=m.KnowledgeId("E2-K-COLLECT"), action=m.ActionId("E2-COLLECT"),
                             expected=next(a for a in actions if a.id == m.ActionId("E2-COLLECT")).accepted_inventory[0].provenance.identity,
                                required_outcome=m.ActionResult.PASS)
    boundary = replace(state.boundaries[0], id=gate.id, actions=(m.ActionId("E2-REENTER"),))
    goal = replace(state.goals[0], entry_actions=(m.ActionId("E2-REENTER"),))
    gate = replace(gate, requirements=(req.id,), resolution_contracts=tuple(
        replace(x, gate=gate.id, requirement=req.id, reentry=(m.ActionId("E2-REENTER"),),
                held_actions=(m.ActionId("E2-REENTER"),), scope=SCOPE, lineage=LINEAGE, generation=GENERATION)
        for x in gate.resolution_contracts))
    current = replace(state, actions=actions, statuses=statuses, decisions=tuple(decision_routes), evidence_requirements=(req,),
                      predicates=(proof, fact_check, fact_collect),
                      external_gates=(gate,), boundaries=(boundary,), goals=(goal,))
    m.validate_model(current)
    return current, root, helper


def qualify():
    state, root, helper = build()
    try:
        m.validate_model(state)
        computation = core.recompute(state)
        assert all(a.id in {x.id for x in state.actions} for a in state.actions)
        snap = c.decode_snapshot(c.snapshot_bytes(state))
        m.validate_model(snap)
        assert c.snapshot_id(snap) == c.snapshot_id(state)
        positives = ["whole-model", "snapshot-round-trip", "external-absence", "policy-binding"]
        negatives = []
        for label, bad in (("wrong-scope", replace(state, context=replace(state.context, scope="WRONG"))),
                           ("duplicate-action", replace(state, actions=state.actions + (state.actions[0],))),
                           ("missing-gate", replace(state, external_gates=()))):
            try:
                m.validate_model(bad)
            except m.PlannerError:
                negatives.append(label)
        assert set(negatives) == {"duplicate-action", "missing-gate"}
        return {"whole_model_admission": "ACCEPT", "actions": 6, "positive_cases": positives,
                "negative_cases": negatives, "control": computation.control.value,
                "snapshot_identity": c.snapshot_id(state).sha256, "experiment_actions_executed": 0}
    finally:
        helper.doCleanups()


if __name__ == "__main__":
    print(json.dumps(qualify(), sort_keys=True))
