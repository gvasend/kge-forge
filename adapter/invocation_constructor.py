"""Pure generic construction of canonical WorkAuthorization artifacts."""
from .context_projection import canonical, digest, sha
from .governed_host import WorkAuthorization

SCHEMA = "WORK-AUTHORIZATION-1"
TEMPLATE_SCHEMA = "WORK-AUTHORIZATION-TEMPLATE-1"


class ConstructionDenied(ValueError):
    pass


def _body(inputs):
    required = {"InvocationAttemptId", "binding_sha256", "canonical_binding", "DispatchAuthorizationId",
        "specific_approval_id", "predecessor", "eligibility", "release_authority",
        "OperationalContextId", "runtime", "runtime_head", "supervisor",
        "succession_head", "profile_sha256", "ModelPayloadDigest",
        "transmission_retention", "budget_policy", "implementation_identity",
        "audit", "initial_state", "ownership", "lifecycle_envelope"}
    if set(inputs) != required:
        raise ConstructionDenied("complete authority input set required")
    if inputs["initial_state"] != "INACTIVE" or inputs["ownership"] != "NONE":
        raise ConstructionDenied("initial WorkAuthorization must be INACTIVE and unowned")
    binding = inputs["canonical_binding"]
    if sha(canonical(binding).encode()) != inputs["binding_sha256"]:
        raise ConstructionDenied("canonical invocation binding digest mismatch")
    if binding.get("InvocationAttemptId") != inputs["InvocationAttemptId"] or \
       binding.get("DispatchAuthorizationId") != inputs["DispatchAuthorizationId"]:
        raise ConstructionDenied("invocation binding identity mismatch")
    if binding.get("bindings", {}).get("release_authority") != inputs["release_authority"] or \
       binding.get("bindings", {}).get("OperationalContextId") != inputs["OperationalContextId"]:
        raise ConstructionDenied("invocation binding authority mismatch")
    return dict(inputs)


def artifact(inputs):
    body = {"schema": SCHEMA, **_body(inputs)}
    body["WorkAuthorizationId"] = "WorkAuthorization-sha256:" + digest(body)
    return body


def serialize(value):
    return canonical(value).encode()


def identity(value):
    if value.get("schema") != SCHEMA:
        raise ConstructionDenied("unknown WorkAuthorization schema")
    expected = "WorkAuthorization-sha256:" + digest({k: v for k, v in value.items()
                                                       if k != "WorkAuthorizationId"})
    if value.get("WorkAuthorizationId") != expected:
        raise ConstructionDenied("WorkAuthorization identity mismatch")
    return expected


def construct_artifact(authenticated_inputs):
    result = artifact(authenticated_inputs)
    identity(result)
    return result


def _argv_allowlist_from_json(value):
    """Decode T1 JSON arrays into the host's exact tuple-of-tuples form.

    This is a representation boundary, not policy normalization: preserve
    order, duplicates and every string verbatim. Reject non-JSON containers
    and malformed commands instead of coercing arbitrary iterables/atoms.
    An explicit empty array retains the existing empty-allowlist semantics;
    this decoder does not authenticate or select a policy value.
    """
    if type(value) is not list or any(
            type(command) is not list or not command or any(
                type(part) is not str or not part or '\x00' in part
                for part in command)
            for command in value):
        raise ConstructionDenied("exec_argv_allowlist must be JSON arrays of nonempty argv strings")
    return tuple(tuple(command) for command in value)


def construct_work_authorization(authenticated_inputs, template):
    if template.get("schema") != TEMPLATE_SCHEMA:
        raise ConstructionDenied("unknown WorkAuthorization template")
    if template.get("state") != "INACTIVE" or template.get("ownership") != "NONE":
        raise ConstructionDenied("invalid template initial state")
    if template.get("binding_digest") != digest(authenticated_inputs):
        raise ConstructionDenied("template authority projection mismatch")
    result = construct_artifact(authenticated_inputs)
    fields = dict(template.get("fields_values", {}))
    if set(fields) != set(WorkAuthorization.__dataclass_fields__):
        raise ConstructionDenied("incomplete WorkAuthorization template")
    fields["exec_argv_allowlist"] = _argv_allowlist_from_json(fields["exec_argv_allowlist"])
    fields.update(authorization_id=result["InvocationAttemptId"], revision=1,
                  state="INACTIVE", ownership_ledger=result["audit"])
    return result, WorkAuthorization(**fields)


def canonical_serialization(value):
    identity(value)
    return serialize(value)
