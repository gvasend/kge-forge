"""Bridge canonical WORK-AUTHORIZATION-1 artifacts into the existing lifecycle.

This bridge is deliberately non-authorizing: it validates an authenticated
artifact, constructs the typed WorkAuthorization, and delegates the single
INACTIVE boundary to the existing invocation_issuance implementation.
"""
import json
from pathlib import Path

from .context_projection import sha
from .invocation_constructor import identity, construct_work_authorization, ConstructionDenied
from .invocation_issuance import issue_inactive


class WorkAuthorizationLifecycleDenied(ValueError):
    pass


def consume_and_issue(artifact_bytes, artifact_sha256, inputs, template,
                      audit, dispatch_ref):
    if sha(artifact_bytes) != artifact_sha256:
        raise WorkAuthorizationLifecycleDenied("WorkAuthorization bytes changed")
    try:
        artifact = json.loads(artifact_bytes)
        identity(artifact)
        built, auth = construct_work_authorization(inputs, template)
        if built != artifact:
            raise WorkAuthorizationLifecycleDenied("constructed WorkAuthorization differs")
        if auth.state != "INACTIVE" or auth.ownership_ledger is None:
            raise WorkAuthorizationLifecycleDenied("invalid initial lifecycle state")
        return issue_inactive(auth, audit, dispatch_ref)
    except (KeyError, TypeError, ValueError, ConstructionDenied) as exc:
        raise WorkAuthorizationLifecycleDenied(str(exc)) from exc
