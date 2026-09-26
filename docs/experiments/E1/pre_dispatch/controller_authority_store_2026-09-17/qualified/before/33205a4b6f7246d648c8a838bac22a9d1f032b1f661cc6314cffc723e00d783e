"""Non-effecting E1 launch proposal and fail-closed provisioning assessment."""
from pathlib import Path
from .runnable_profile import specification
from .model_transport import configuration

LEDGER='/tmp/kge-forge-e1-invocations.jsonl'
AUDIT='/tmp/kge-forge-e1-evidence/{authorization_id}/{session_id}/{turn_id}/controller.jsonl'

def provisioning(binding,receipt=None,approved_authority_refs=()):
    from .directory_provisioning import plan, open_directory
    import hashlib, json, os
    record=plan(binding.repos['forge'],binding.digest)
    observed={}
    for row in record['directories']:
        try:
            fd=open_directory(row['path']); os.close(fd)
            observed[row['path']]={'directory':True,'symlink':False}
        except (OSError,ValueError):
            observed[row['path']]={'directory':False,'symlink':Path(row['path']).is_symlink()}
    blockers=[]
    if any(not row['directory'] for row in observed.values()):
        blockers.append('required pre-existing E1 directory absent or invalid')
    expected_digest=hashlib.sha256(json.dumps(record,sort_keys=True).encode()).hexdigest()
    expected_created=[r['path'] for r in record['directories'] if r['controller_provisioning_required']]
    if (not receipt or receipt.get('architect_authority_reference') not in approved_authority_refs
            or receipt.get('plan_sha256')!=expected_digest
            or receipt.get('created')!=expected_created or receipt.get('result')!='PASS'
            or receipt.get('state')!='INACTIVE' or receipt.get('profile_activated') is not False):
        blockers.append('exact E1 directory provisioning authorization/receipt absent')
    return {'ready':not blockers,'observed':observed,'blockers':blockers,
            'creation_performed':bool(receipt and receipt.get('result')=='PASS')}

def proposal(binding):
    if binding.manifest['work_id']!='E1-WP-001': raise ValueError('E1 context required')
    binding.verify()
    from .directory_provisioning import plan
    from .model_transmission import production_policy
    return {'schema':'E1-PROPOSED-LAUNCH-4','state':'INACTIVE','work_id':'E1-WP-001',
        'revision':4,'capture_commit':binding.capture_commit,'context_sha256':binding.digest,
        'runtime':specification(binding,binding),'model_transport':configuration(),
        'ownership':{'ledger':LEDGER,'override_permitted':False,
            'rule':'All E1 sessions/turns/controllers/revisions share the same canonical ledger; no truncate/reset; active or uncertain reservation blocks.'},
        'audit':{'path_rule':AUDIT,'directory_mode':'0700','file_mode':'0600',
                 'restart':'same identity and exact existing append-only audit; no reset'},
        'identity':{'authorization':'auth-e1-wp-001-r4-<controller UUID4>',
            'session':'session-e1-<controller UUID4>','turn':'turn-e1-<controller UUID4>',
            'scope':'scope-<controller UUID4>, per admitted execution',
            'binding':'immutable profile digest + context capture/digest + work + revision; same identities on restart',
            'production_ids_allocated':False},
        'snapshot':{'host_workspace':'/tmp/a2-exec-<controller random>, 0700',
            'payload_workspace':'/scope','scratch':'/scope/.scratch',
            'controller_policy':'/scope/.gei-runtime.json, readonly',
            'acceptance':'/scope/.gei-context, readonly; repository projections readonly at their exact original absolute roots',
            'manifest':'<audit parent>/snapshots/<scope_id>.json, 0600',
            'promotion':'none; separate governed write/patch required'},
        'external_policy':{'model_endpoint_only':configuration()['endpoint'],
            'model_redirects':False,'task_network':False,'MCP':False,'plugins':False,
            'connectors':False,'additional_agents':False,'generic_Git_tool':False,'shell':False},
        'provisioning':provisioning(binding),
        'provisioning_plan':plan(binding.repos['forge'],binding.digest),
        'model_transmission':production_policy(binding),
        'release_authorized':False,'eligible':False,'dispatch_issued':False}
