"""Authenticated rebinding of a historical dispatch to a current runtime.

The historical dispatch is an immutable input.  This module derives a new
current dispatch authority only from the exact historical identity, qualified
temporal transition, and current mutable authority facts.
"""
import hashlib
import json


class DispatchAmendmentError(ValueError):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def authenticate(original, amendment, transition, current):
    if amendment.get("schema") != "E1-DISPATCH-TEMPORAL-AMENDMENT-1":
        raise DispatchAmendmentError("unknown dispatch amendment schema")
    if amendment.get("original_dispatch") != original.get("id"):
        raise DispatchAmendmentError("original dispatch missing or substituted")
    if amendment.get("original_dispatch_sha256") != digest(original):
        raise DispatchAmendmentError("original dispatch bytes changed")
    if amendment.get("temporal_authority_amendment") != transition.get("id"):
        raise DispatchAmendmentError("temporal ancestry missing or substituted")
    if transition.get("status") != "ADOPTED":
        raise DispatchAmendmentError("temporal transition is not adopted")
    for key in ("runtime", "runtime_head_authority", "release_authority",
                "OperationalContextId", "profile", "ModelPayloadDigest",
                "transmission", "budget", "supervisor", "work_package_id"):
        if amendment.get("current", {}).get(key) != current.get(key):
            raise DispatchAmendmentError("current dispatch binding mismatch: " + key)
    preserved = ("work_package_id", "profile", "ModelPayloadDigest", "transmission", "budget")
    for key in preserved:
        if original.get(key) != amendment.get("current", {}).get(key):
            raise DispatchAmendmentError("unrelated authority change: " + key)
    if amendment.get("authority") != "Architect":
        raise DispatchAmendmentError("unattributed amendment authority")
    return True


def current_dispatch(original, amendment):
    """Derive a new immutable authority record; never mutate ``original``."""
    out = dict(original)
    out.update(amendment["current"])
    out["id"] = amendment["current_dispatch"]
    out["amendment"] = amendment["id"]
    out["historical_dispatch"] = original["id"]
    out["decision"] = "DISPATCH_AUTHORIZED"
    return out
