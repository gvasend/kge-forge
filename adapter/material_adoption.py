"""Qualification-only material runtime adoption consumer.

This module does not select or mutate production runtime authority. It validates
one exact Architect-granted material transition against an authenticated head.
"""
import hashlib, json

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
def digest(value): return hashlib.sha256(canonical(value)).hexdigest()
def identity(prefix, value): return f"{prefix}-sha256:{digest(value)}"

class MaterialAdoptionDenied(ValueError): pass

def make_grant(*, predecessor, successor, continuation, classification, qualification,
               enrollment, runtime_head_authority, release_context, adoption_decision,
               scope="EXACT_SINGLE_MATERIAL_TRANSITION"):
    body={"schema":"MATERIAL-RUNTIME-ADOPTION-GRANT-1","predecessor_runtime":predecessor,
          "successor_runtime":successor,"continuation":continuation,
          "classification":classification,"qualification":qualification,
          "enrollment":enrollment,"runtime_head_authority":runtime_head_authority,
          "release_context":release_context,"adoption_decision":adoption_decision,
          "scope":scope,"replay":"REJECT_SECOND_TRANSITION",
          "authority":"Architect"}
    if classification != "MATERIAL_LIFECYCLE_AUTHORITY_IMPLEMENTATION_CHANGE":
        raise MaterialAdoptionDenied("material classification required")
    body["id"]=identity("MATERIAL-RUNTIME-ADOPTION-GRANT",body)
    return body

def validate_grant(grant, *, current_runtime, enrolled, qualified, head_authority,
                   release_context, continuation, predecessor, successor,
                   adoption_decision):
    required={"schema","predecessor_runtime","successor_runtime","continuation",
      "classification","qualification","enrollment","runtime_head_authority",
      "release_context","adoption_decision","scope","replay","authority","id"}
    if set(grant)!=required: raise MaterialAdoptionDenied("grant schema")
    body=dict(grant); gid=body.pop("id")
    if gid != identity("MATERIAL-RUNTIME-ADOPTION-GRANT",body): raise MaterialAdoptionDenied("grant identity")
    if current_runtime != predecessor or grant["predecessor_runtime"] != predecessor: raise MaterialAdoptionDenied("stale predecessor")
    if not enrolled or not qualified: raise MaterialAdoptionDenied("enrollment/qualification")
    if grant["runtime_head_authority"] != head_authority: raise MaterialAdoptionDenied("runtime head")
    if grant["release_context"] != release_context: raise MaterialAdoptionDenied("release context")
    if grant["continuation"] != continuation or grant["successor_runtime"] != successor: raise MaterialAdoptionDenied("successor binding")
    if grant["adoption_decision"] != adoption_decision: raise MaterialAdoptionDenied("Architect decision")
    if grant["scope"] != "EXACT_SINGLE_MATERIAL_TRANSITION" or grant["replay"] != "REJECT_SECOND_TRANSITION": raise MaterialAdoptionDenied("scope")
    if grant["classification"] != "MATERIAL_LIFECYCLE_AUTHORITY_IMPLEMENTATION_CHANGE": raise MaterialAdoptionDenied("classification")
    return True

def transition(state, grant, **kwargs):
    if not isinstance(grant, dict) or "predecessor_runtime" not in grant or "successor_runtime" not in grant:
        raise MaterialAdoptionDenied("malformed grant")
    if state.get("pending") is not None or state.get("current_runtime") != grant["predecessor_runtime"]: raise MaterialAdoptionDenied("stale/competing head")
    validate_grant(current_runtime=state["current_runtime"], grant=grant, **kwargs)
    if grant["successor_runtime"] in state.get("used",[]): raise MaterialAdoptionDenied("replay")
    return {"current_runtime":grant["successor_runtime"],"pending":None,"used":state.get("used",[])+[grant["successor_runtime"]],"event":"MATERIAL_HEAD_COMMITTED"}
