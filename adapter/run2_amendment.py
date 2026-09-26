"""Bounded Run-2 decision preflight; never issues release or dispatch authority.

This additional gate does not replace context, lifecycle, ownership or supervisor
validation. The externally pinned private catalog selects every decision. A
documentary candidate, including one with correct hashes, is not a decision.
"""
import json
from .controller_authority_store import current, encoded, sha, AuthorityDenied
from .context_projection import digest
from .run_control import E1_POLICY

RUN1_AUTH = 'auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39'
PRIOR_RELEASE = 'E1-RELEASE-AUTHORITY-sha256:c0d6aed0894c9d07945b017423b3bb2fedb7207780b5e3d4e6c928aacb82bae3'
PRIOR_AMENDMENT = 'PD06-SUPERVISOR-AUTHORITY-AMENDMENT-sha256:979201e9e2d4269a483ce904ae4e7f9329ab0378836e7ada59070b3e4636d3b6'
PAYLOAD = 'd675d581c80f43e691a31da73ccf17fd4bcc6b00d3a5331f26b9294e294e1538'
SCOPES = ('governed_budgets', 'tool_contract_payload', 'safe_denial_transmission',
          'private_request_retention', 'incomplete_disposition', 'supervisor_host_lifetime')


def require(value, message):
    if not value:
        raise AuthorityDenied(message)


def sealed(kind, body):
    return dict(body, id=kind + '-sha256:' + digest(body))


def unseal(value, kind):
    body = {k: v for k, v in value.items() if k != 'id'}
    require(value == sealed(kind, body), 'Run-2 decision identity mismatch')
    return body


def read_bytes(ref):
    require(isinstance(ref, dict) and set(ref) == {'authority_id', 'sha256'},
            'Run-2 private logical reference required')
    require(isinstance(ref['authority_id'], str) and '/' not in ref['authority_id'],
            'repository path is not Run-2 authority')
    store = current()
    require(store is not None, 'Run-2 private authority session required')
    data = store.resolve(ref['authority_id'])
    require(sha(data) == ref['sha256'], 'Run-2 private object hash mismatch')
    return data


def read(ref):
    return json.loads(read_bytes(ref))


def verify(authorization_id):
    """Authenticate the exact selected material/dispatch chain, without effects."""
    store = current()
    require(store is not None, 'Run-2 private authority session required')
    require(store.applicability['authorization_id'] == authorization_id and
            authorization_id != RUN1_AUTH, 'Run-2 needs a distinct invocation')
    selected = json.loads(store.resolve(authorization_id + ':run2-material'))
    require(set(selected) == {'candidate', 'release_decision', 'dispatch_decision',
                             'continuations', 'operational_context'}, 'unknown Run-2 selection')
    candidate = read(selected['candidate'])
    c = unseal(candidate, 'E1-RUN2-RELEASE-AMENDMENT')
    require(c['schema'] == 'E1-RUN2-RELEASE-AMENDMENT-1' and
            c['prior_release_authority'] == PRIOR_RELEASE and
            c['prior_supervisor_amendment'] == PRIOR_AMENDMENT and
            c['material_scopes'] == list(SCOPES), 'Run-2 amendment outside approved scope')
    require(c['ModelPayloadDigest'] == PAYLOAD and c['budget_policy'] == E1_POLICY,
            'Run-2 payload or budget substitution')
    require(c['work_package'] == 'E1-WP-001' and c['new_invocation_required'] is True and
            c['successor_instance'] is None and c['host_launch_authorization'] is None,
            'Run-2 amendment cannot authorize an instance, host launch or retry')
    # The original decision and prior amendment are immutable private objects,
    # not regenerated using the currently installed model-visible tool schema.
    old = read(c['original_release_decision'])
    basis = read(c['original_release_basis'])
    require(c['original_release_basis']['sha256'] == 'bc176574817f6b7fe06fdcf87a71c57b2a8bfe74e55ed20f2aa55ad5d4fa5181' and
            c['original_release_decision']['sha256'] == '43ab22254604a29f3cf2164152803ee5f689f7540e2006c43d27ded87d83d8c0',
            'Run-2 original release substitution')
    require(old['ReleaseBasisId'] == 'E1-RELEASE-BASIS-sha256:' + c['original_release_basis']['sha256'] and
            old['decision'] == {'PD06': 'RELEASED', 'E1_B01': 'PASS'} and
            old['released_profile_sha256'] == basis['production_profile_sha256'],
            'Run-2 original release mismatch')
    # Historical records keep their evidence spelling. Resolution still uses
    # the private content object; no repository fallback is available here.
    source_ref = old['authority_source']
    require(bool(read_bytes({'authority_id': 'sha256:' + source_ref['sha256'], 'sha256': source_ref['sha256']})),
            'original release attribution absent')
    prior = read(c['prior_supervisor_decision'])
    p = unseal(prior, 'PD06-SUPERVISOR-AMENDMENT-DECISION')
    require(p['amendment_identity'] == PRIOR_AMENDMENT and
            p['resulting_release_authority'] == PRIOR_RELEASE and
            p['authority'] == 'Architect' and
            p['decision'] == 'AUTHORIZE_MATERIAL_SUPERVISOR_AMENDMENT',
            'Run-2 predecessor amendment mismatch')
    require(p['original_release'] == {'ReleaseBasisId': 'E1-RELEASE-BASIS-sha256:' + c['original_release_basis']['sha256'],
            'ReleaseDecisionId': 'E1-RELEASE-DECISION-sha256:' + c['original_release_decision']['sha256']},
            'Run-2 predecessor release reordering')
    prior_candidate = read(p['candidate'])
    require(prior_candidate['amendment_candidate_identity'] == PRIOR_AMENDMENT and
            'PD06-SUPERVISOR-AUTHORITY-AMENDMENT-sha256:' + digest(prior_candidate['body']) == PRIOR_AMENDMENT,
            'Run-2 predecessor candidate mismatch')
    source = read(p['authority_source'])
    require(source['authority'] == 'Architect' and source['channel'] == 'user' and
            source['accepted']['amendment_identity'] == PRIOR_AMENDMENT and
            source['accepted']['candidate_file_sha256'] == p['candidate']['sha256'] and
            source['accepted']['resulting_release_authority'] == PRIOR_RELEASE,
            'Run-2 predecessor attribution mismatch')
    profile = read(c['profile']); payload = read(c['payload']); policy = read(c['policy'])
    require(payload['ModelPayloadDigest'] == PAYLOAD and
            profile['proposed_run2_bindings']['ModelPayloadDigest'] == PAYLOAD and
            policy['run_control'] == E1_POLICY, 'Run-2 content binding mismatch')
    from .context_projection import model_input
    require(digest({'input': model_input(payload['payload']), 'tools': payload['tools']}) == PAYLOAD,
            'Run-2 payload bytes changed')
    inventory = read(c['implementation'])
    require(inventory['identity'] == 'sha256:' + digest(inventory['inventory']),
            'Run-2 implementation inventory changed')
    from pathlib import Path
    actual = {str(p.resolve()): sha(p.read_bytes())
              for p in Path(__file__).resolve().parent.glob('*.py')}
    require(actual == inventory['inventory'], 'Run-2 live implementation differs from qualification')
    qualification = read(c['qualification'])
    require(qualification['result'] == 'PASS' and
            qualification['implementation_identity'] == inventory['identity'],
            'Run-2 implementation not qualified')
    result = 'E1-RELEASE-AUTHORITY-sha256:' + digest({
        'predecessor': PRIOR_RELEASE, 'Run2AmendmentId': candidate['id']})
    decision = read(selected['release_decision'])
    r = unseal(decision, 'E1-RUN2-RELEASE-DECISION')
    require(r['decision'] == 'AUTHORIZE_E1_RUN2_RELEASE' and r['authority'] == 'Architect' and
            r['candidate'] == selected['candidate'] and r['resulting_release_authority'] == result,
            'Run-2 release not authorized')
    attribution = read(r['authority_source'])
    require(attribution == {'authority': 'Architect', 'channel': 'user',
        'decision': 'AUTHORIZE_E1_RUN2_RELEASE', 'candidate': selected['candidate'],
        'resulting_release_authority': result}, 'Run-2 release attribution mismatch')
    head = c['predecessor_operational_context']
    require(head == {'OperationalContextId': 'E1-OPERATIONAL-CONTEXT-sha256:3672ba1076042f90563116c57a0e002beb19f03f164c4dfabc71fe721ac72453',
                     'continuation_chain_digest': '2193231e010af1189bd90e5519bfc1232f84e0de8dfc9fd6ed5d377616f83515'},
            'Run-2 historical operational predecessor changed')
    require(selected['continuations'] == c['applicable_continuations'], 'Run-2 continuation selection changed')
    head = {'OperationalContextId': 'E1-OPERATIONAL-CONTEXT-sha256:' + digest({
                'predecessor': head['OperationalContextId'], 'Run2AmendmentId': candidate['id']}),
            'continuation_chain_digest': digest({'predecessor': head['continuation_chain_digest'],
                'Run2AmendmentId': candidate['id']})}
    seen = set()
    for ref in selected['continuations']:
        row = read(ref)
        from .continuation_envelope import BODY_KEYS, seal
        body = {k: row[k] for k in BODY_KEYS}
        approval = read(row['approval'])
        require(row == seal(body, row['approval']) and row['continuation_id'] not in seen and
                row['predecessor_OperationalContextId'] == head['OperationalContextId'] and
                row['predecessor_chain_digest'] == head['continuation_chain_digest'] and
                row['classification'] == 'NON_MATERIAL_IMPLEMENTATION_CONTINUATION' and
                approval['authority'] == 'Architect' and
                approval['decision'] == 'AUTHORIZE_NON_MATERIAL_CONTINUATION' and
                approval['body_sha256'] == digest(body), 'Run-2 continuation mismatch/replay')
        read(approval['authority_source'])
        evidence = read(row['evidence'])
        require(evidence['result'] == 'PASS' and evidence['artifacts_sha256'] == digest(row['artifacts']),
                'Run-2 continuation qualification missing')
        seen.add(row['continuation_id'])
        head = {k: row[k] for k in ('OperationalContextId', 'continuation_chain_digest')}
    require(head == selected['operational_context'], 'Run-2 operational head mismatch')
    require(all(store.applicability.get(k) == v for k, v in head.items()), 'Run-2 stale catalog applicability')
    dispatch = read(selected['dispatch_decision'])
    d = unseal(dispatch, 'E1-RUN2-DISPATCH-DECISION')
    expected = {'authority': 'Architect', 'decision': 'AUTHORIZE_E1_RUN2_DISPATCH',
        'authorization_id': authorization_id, 'release_authority': result,
        'release_decision': decision['id'], 'ModelPayloadDigest': PAYLOAD,
        'profile': c['profile'], 'operational_context': head}
    require({k: d.get(k) for k in expected} == expected, 'Run-2 specific dispatch missing/stale')
    dispatch_source = read(d['authority_source'])
    require(dispatch_source == dict(expected, channel='user'), 'Run-2 dispatch attribution mismatch')
    return {'release_authority': result, 'amendment': candidate['id'],
            'dispatch': dispatch['id'], 'operational_context': head}
