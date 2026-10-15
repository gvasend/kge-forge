"""Generic materialization of authored Action result contracts.

The PC01/source model carries output declarations separately from the native
``Action`` object.  This module is the single bounded mapping that preserves
those declarations as the typed ``accepted_inventory`` required by result
admission.  It deliberately accepts an authored declaration rather than a
caller-supplied result or entity identity.
"""

from dataclasses import replace

from . import model as m


def materialize_action(action, declaration):
    """Return ``action`` with its authored result inventory materialized.

    ``declaration`` is the source-model mapping for this exact Action.  Only
    its output contract is copied; no runtime result or completion state is
    created.  Empty output is valid for decision Actions and remains empty.
    """
    if type(action) is not m.Action or type(declaration) is not dict:
        raise m.PlannerError("typed Action and declaration required")
    if declaration.get("id") != action.id.value:
        raise m.PlannerError("Action/declaration identity mismatch")
    output = declaration.get("output")
    if output is None:
        inventory = ()
    else:
        if type(output) is not dict or set(output) != {"id", "type", "statement", "producer", "outcome"}:
            raise m.PlannerError("complete authored output contract required")
        if output["type"] != "KnowledgeRecord" or output["producer"] != action.id.value:
            raise m.PlannerError("output producer/type differs from Action")
        if output["outcome"] != action.accepted_result.value:
            raise m.PlannerError("output outcome differs from Action result contract")
        inventory = (m.KnowledgeRecord(
            m.KnowledgeId(output["id"]), m.KnowledgeState.KNOWN_COMPLETE,
            output["statement"], action.source, (),
            m.ValidationState.ACCEPTED, action.id, action.accepted_result),)
    return replace(action, accepted_inventory=inventory,
                   pass_model_complete=bool(declaration.get("pass_model_complete", action.pass_model_complete)))


def materialize_actions(actions, declarations):
    """Materialize all authored result contracts, preserving Action order."""
    by_id = {d.get("id"): d for d in declarations if type(d) is dict}
    if len(by_id) != len(actions):
        raise m.PlannerError("one declaration required per Action")
    return tuple(materialize_action(a, by_id.get(a.id.value)) for a in actions)
