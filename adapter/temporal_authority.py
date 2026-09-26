"""Temporal predecessor validation across authenticated runtime transitions.

Historical invocation evidence is checked against the authority/runtime that
created it. Current succession eligibility is checked separately against the
current runtime head and an authenticated transition chain. No function in
this module rewrites or upgrades historical bindings.
"""

from dataclasses import dataclass
import hashlib
import json


class TemporalAuthorityError(ValueError):
    """A historical/current authority relationship cannot be authenticated."""


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _digest(value):
    return hashlib.sha256(_canonical(value).encode()).hexdigest()


@dataclass(frozen=True)
class HistoricalValidity:
    authorization_id: str
    runtime_identity: str
    operational_binding_digest: str
    disposition: str


def validate_historical_validity(record, *, runtime_identity, operational_binding):
    """Validate a predecessor only under its original authority epoch."""
    if record.get("runtime_identity") != runtime_identity:
        raise TemporalAuthorityError("historical runtime identity mismatch")
    if record.get("operational_binding") != operational_binding:
        raise TemporalAuthorityError("historical operational binding changed")
    if record.get("disposition") != "CANCELLED / INTERRUPTED_NO_EFFECTS":
        raise TemporalAuthorityError("predecessor is not an accepted terminal disposition")
    if any(record.get(key) for key in ("model_requests", "provider_requests",
                                       "action_requests", "executions",
                                       "repository_effects", "knowledge_effects",
                                       "unresolved_uncertainty")):
        raise TemporalAuthorityError("historical predecessor has effects or uncertainty")
    if record.get("ownership") != "RELEASED" or not record.get("quiescent"):
        raise TemporalAuthorityError("historical predecessor is not released/quiescent")
    return HistoricalValidity(record["authorization_id"], runtime_identity,
                              _digest(operational_binding), record["disposition"])


def validate_transition_ancestry(transition, *, historical_runtime, current_runtime,
                                 bootstrap_id, adoption_id):
    """Verify the authenticated bridge from the old runtime to the current head."""
    if transition.get("bootstrap") != bootstrap_id:
        raise TemporalAuthorityError("bootstrap ancestry missing or substituted")
    if transition.get("predecessor_runtime") != historical_runtime:
        raise TemporalAuthorityError("historical transition predecessor mismatch")
    if transition.get("successor_runtime") != current_runtime:
        raise TemporalAuthorityError("current runtime transition mismatch")
    if transition.get("adoption") != adoption_id:
        raise TemporalAuthorityError("runtime adoption ancestry missing or substituted")
    if transition.get("status") != "ADOPTED":
        raise TemporalAuthorityError("runtime transition is not adopted")
    return True


def validate_current_eligibility(validity, transition, *, current_runtime,
                                 current_operational_binding, predecessor_id):
    """Authorize only a new current attempt; never mutate ``validity``."""
    if validity.authorization_id != predecessor_id:
        raise TemporalAuthorityError("wrong predecessor identity")
    if transition.get("successor_runtime") != current_runtime:
        raise TemporalAuthorityError("current runtime head is stale")
    if not current_operational_binding:
        raise TemporalAuthorityError("current operational binding missing")
    return {
        "historical_predecessor": validity.authorization_id,
        "historical_runtime": validity.runtime_identity,
        "current_runtime": current_runtime,
        "current_operational_binding": current_operational_binding,
        "historical_binding_preserved": True,
        "eligible": True,
    }
