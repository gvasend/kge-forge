"""Controller-private supervisor succession. A catalog pin is the trust root.

No authority is inferred from a label, a matching process, or repository evidence.
The append operation does not issue an approval or select the appended head.
"""
from pathlib import Path
import fcntl
import json
import os
import stat
from .context_projection import canonical, digest, sha
from .controller_authority_store import outside


class SuccessionDenied(ValueError): pass


def require(condition, message):
    if not condition: raise SuccessionDenied(message)


def sealed(kind, body):
    require('id' not in body, 'body already sealed')
    return {**body, 'id':kind+'-sha256:'+digest(body)}


def check_id(value, kind):
    body=dict(value); identity=body.pop('id',None)
    require(identity==kind+'-sha256:'+digest(body), 'identity/hash mismatch')
    return identity


def get(store, identity, schema):
    require(isinstance(identity,str) and '/' not in identity, 'logical identity required')
    value=json.loads(store.resolve(identity))
    require(value.get('schema')==schema, 'authority schema mismatch')
    return value


def instance(value):
    check_id(value,'SupervisorInstance')
    require(value.get('schema')=='SUPERVISOR-INSTANCE-1','full instance required')
    required={'schema','process','executable','implementation','workspace','cgroup','socket',
              'protocol_configuration','host_launch','runtime_binding','id'}
    require(set(value)==required,'instance fields incomplete/unknown')
    p=value['process']
    require(set(p)=={'pid','ppid','boot_id','start_ticks','pid_namespace_inode','parent_start_ticks','uid','gid','groups'},'process identity incomplete')
    require(all(type(p[k]) is int and p[k]>0 for k in ('pid','ppid','start_ticks','pid_namespace_inode','parent_start_ticks')),'invalid process birth')
    require(isinstance(p['boot_id'],str) and len(p['boot_id'])==36,'boot identity missing')
    require(all(type(p[k]) is int and p[k]>=0 for k in ('uid','gid')) and isinstance(p['groups'],list),'runtime credentials missing')
    for k in ('implementation','protocol_configuration','runtime_binding'):
        require(isinstance(value[k],dict) and bool(value[k]),k+' missing')
    require(set(value['executable'])=={'path','sha256','argv'},'interpreter identity missing')
    require(set(value['workspace'])=={'path','device','inode'},'workspace identity missing')
    require(set(value['cgroup'])=={'path','unified','memberships','device','inode'},'cgroup identity missing')
    require(set(value['socket'])=={'path','device','inode','uid','gid','mode','listener_pid','listener_start_ticks','listener_inode'},'socket identity missing')
    s=value['socket']
    require(s['mode']==0o600 and s['uid']==p['uid'] and s['gid']==p['gid'],'socket credentials invalid')
    require(s['listener_pid']==p['pid'] and s['listener_start_ticks']==p['start_ticks'],'listener not instance')
    require(isinstance(value['host_launch'],str) and value['host_launch'],'host launch provenance missing')
    require(all(isinstance(h,str) and len(h)==64 for h in value['implementation'].values()),'implementation hash invalid')
    return value


def runtime_binding(auth, store, profile):
    op=json.loads(auth.operational_binding)
    return {'authorization_id':auth.authorization_id,**op['governance']['identities'],
            'released_profile_content_sha256':sha(canonical(profile).encode()),
            'execution_profile_sha256':sha(auth.execution_profile.encode()),
            'authority_store_epoch_sha256':digest({'authorization_id':auth.authorization_id,**op['governance']['identities']})}


def equivalent(value):
    """Configuration equality never implies instance equality."""
    p=value['process'];s=value['socket']
    return {'uid':p['uid'],'gid':p['gid'],'groups':p['groups'],
        'executable':value['executable'],'implementation':value['implementation'],
        'workspace':value['workspace'],'cgroup':value['cgroup'],
        'socket':{k:s[k] for k in ('path','uid','gid','mode')},
        'protocol_configuration':value['protocol_configuration']}


def validate_instance(store, identity, policy):
    value=instance(get(store,identity,'SUPERVISOR-INSTANCE-1'))
    require(value['id']==identity, 'instance alias substitution')
    require(equivalent(value)==policy['requirements'],'successor configuration/implementation mismatch')
    require(value['runtime_binding']==policy['runtime_binding'],'instance ancestry mismatch')
    host=get(store,value['host_launch'],'SUPERVISOR-HOST-LAUNCH-1')
    require(host['authority']=='HOST_OPERATOR' and host['authorized_launch'] is True,'host launch not authorized')
    require(host['runtime_binding']==value['runtime_binding'],'host launch ancestry mismatch')
    require(host['process']==value['process'] and host['configuration']==equivalent(value),'host launch identity mismatch')
    require(host['parent_start_identity']=={'pid':value['process']['ppid'],'boot_id':value['process']['boot_id'],'start_ticks':value['process']['parent_start_ticks']} and host['command_sha256'] and host['operator_authorization_id'],'host launch provenance incomplete')
    require(host['delegated_before_credentials_dropped'] is True and host['runtime_uid']==value['process']['uid'] and host['runtime_gid']==value['process']['gid'],'host authority boundary violated')
    return value


def events(data):
    require(not data or data.endswith(b'\n'),'truncated succession ledger')
    try: rows=[json.loads(line) for line in data.splitlines()]
    except (ValueError,UnicodeError) as exc: raise SuccessionDenied('corrupt succession ledger') from exc
    for row in rows:
        require(row.get('schema')=='SUPERVISOR-SUCCESSION-1','unknown succession event')
        check_id(row,'SupervisorSuccession')
    return rows


def reconstruct(store, policy, data, *, require_head=True, historical_applicability=None):
    require(policy['schema'] in ('SUPERVISOR-SUCCESSION-POLICY-1','SUPERVISOR-SUCCESSION-POLICY-2'),'policy schema')
    binding=policy['runtime_binding']
    applicability=store.applicability if historical_applicability is None else historical_applicability
    require({k:binding[k] for k in applicability}==applicability,'stale policy ancestry')
    prefix=None
    if policy['schema']=='SUPERVISOR-SUCCESSION-POLICY-2':
        require(historical_applicability is None,'nested supervisor epochs forbidden')
        from .run2_context import supervisor_prefix
        prefix=supervisor_prefix(store)
        require(policy['historical_prefix']==prefix['reference'],'unselected supervisor epoch predecessor')
        restored=reconstruct(store,prefix['policy'],prefix['data'],historical_applicability=prefix['applicability'])
        anchor=restored['instance']
        require(anchor['id']==policy['anchor_id'],'supervisor epoch anchor substitution')
    else:anchor=json.loads(store.resolve(policy['anchor_id']))
    if anchor.get('schema')=='SUPERVISOR-HISTORICAL-INSTANCE-1':
        check_id(anchor,'SupervisorHistoricalInstance')
        require(anchor['id']==policy['anchor_id'],'historical alias substitution')
    elif prefix is None: anchor=validate_instance(store,policy['anchor_id'],policy)
    current=anchor;head=restored['head'] if prefix else None;sequence=restored['sequence'] if prefix else 0;seen={};used={anchor['id']}
    for row in events(data):
        if row['id'] in seen:
            require(row==seen[row['id']], 'ambiguous replay')
            continue
        require(set(row)=={'schema','sequence','predecessor_event','predecessor_instance','predecessor_status',
            'predecessor_evidence','successor_instance','reason','architect_authorization','host_launch',
            'qualification','runtime_binding','id'},'event fields incomplete/unknown')
        require(row['sequence']==sequence+1 and row['predecessor_event']==head,'missing/reordered/competing succession')
        require(row['predecessor_instance']==current['id'],'predecessor instance mismatch')
        require(row['successor_instance']!=current['id'] and row['successor_instance'] not in used,'instance reuse')
        require(row['runtime_binding']==binding,'succession ancestry mismatch')
        aid=row['architect_authorization']
        require(aid in policy['authorized_succession_ids'] and aid not in used,'succession is not independently authorized')
        approval=get(store,aid,'SUPERVISOR-SUCCESSION-AUTHORIZATION-1')
        body={k:v for k,v in row.items() if k not in ('id','architect_authorization')}
        require(approval['authority']=='Architect' and approval['decision']=='AUTHORIZE_SUPERVISOR_SUCCESSION' and approval['event_body_sha256']==digest(body),'approval binding mismatch')
        evidence=get(store,row['predecessor_evidence'],'SUPERVISOR-PREDECESSOR-EVIDENCE-1')
        require(evidence['instance_id']==current['id'] and evidence['runtime_binding']==binding and evidence['status']==row['predecessor_status'],'predecessor evidence mismatch')
        require(evidence['authority']=='HOST_OPERATOR' and evidence['observation_id'] and evidence['observed_at'],'predecessor evidence unauthenticated')
        require(row['reason'] and row['reason']==approval['reason'],'reason not authorized')
        if row['predecessor_status']=='UNAVAILABLE':
            require(evidence['process_absent'] is True and evidence['listener_absent'] is True,'predecessor not unavailable')
        elif row['predecessor_status']=='FENCED':
            require(approval.get('allow_live_predecessor') is True and evidence['execution_authority_fenced'] is True and evidence['listener_absent'] is True,'live predecessor not explicitly fenced')
        else: raise SuccessionDenied('active/uncertain predecessor cannot succeed')
        require(evidence['outstanding_scopes_accounted'] is True,'unaccounted predecessor execution')
        successor=validate_instance(store,row['successor_instance'],policy)
        require(successor['host_launch']==row['host_launch'],'launch provenance substitution')
        q=get(store,row['qualification'],'SUPERVISOR-QUALIFICATION-1')
        require(q['instance_id']==successor['id'] and q['runtime_binding']==binding and q['result']=='PASS' and q['configuration']==equivalent(successor) and q['capture_sha256'],'successor qualification missing/mismatched')
        current=successor;head=row['id'];sequence+=1;seen[head]=row;used.update((aid,current['id']))
    if require_head: require(head==policy['pinned_head'],'succession head missing/stale/deleted')
    return {'instance':current,'head':head,'sequence':sequence}


def _append_under_fence(store, policy, path, row):
    """CAS append under flock; pin selection is a separate authorized operation.

    A crash before a newly approved catalog selects this head blocks readiness.
    Replay returns False without writing. There is no overwrite/truncate API.
    """
    require(Path(path)==store.state_path(policy['ledger_id']),'unregistered succession ledger')
    fd=os.open(path,os.O_RDWR|os.O_NOFOLLOW)
    try:
        fcntl.flock(fd,fcntl.LOCK_EX)
        st=os.fstat(fd)
        require(stat.S_ISREG(st.st_mode) and st.st_uid==os.getuid() and not st.st_mode&0o077 and st.st_nlink==1,'unsafe succession ledger')
        with os.fdopen(os.dup(fd),'rb') as stream:data=stream.read()
        previous=events(data)
        if any(old==row for old in previous):
            reconstruct(store,policy,data);return False
        reconstruct(store,policy,data)
        candidate=data+canonical(row).encode()+b'\n'
        reconstruct(store,{**policy,'pinned_head':row['id']},candidate)
        os.lseek(fd,0,os.SEEK_END)
        with os.fdopen(os.dup(fd),'ab') as stream:
            stream.write(canonical(row).encode()+b'\n');stream.flush();os.fsync(stream.fileno())
        return True
    finally:os.close(fd)


def append_authorized(store, policy, path, row):
    """Use the existing invocation fence; succession cannot race an E1 owner."""
    from .supervisor_amendment import authorize_append
    authorize_append(store,policy,row)
    from .activation_transaction import _lease, invocation
    from .invocation_ownership import InvocationOwnership
    ownership=store.state_path(store.applicability['authorization_id']+':ownership')
    lease=_lease(ownership)
    owner_fd=None
    try:
        owner=InvocationOwnership(ownership)
        owner_fd=owner._locked()
        require(invocation(owner_fd) is None and owner._history(owner_fd) is None,
                'supervisor succession blocked by invocation/execution ownership')
        return _append_under_fence(store,policy,path,row)
    finally:
        if owner_fd is not None: os.close(owner_fd)
        os.close(lease)


def legacy_tuple(value):
    p=value['process']
    return {'pid':p['pid'],'ppid':p['ppid'],'uid':p['uid'],
        'exe':value['executable']['path'],'exe_sha256':value['executable']['sha256'],
        'argv':value['executable']['argv'],'cwd':value['workspace']['path'],
        'cgroup':value['cgroup']['memberships']}


def readiness(auth, store, historical, check_scopes, legacy_check):
    """Select only private, context-bound authority and fresh kernel observations."""
    from .supervisor_observation import observe
    identity=auth.authorization_id+':supervisor-succession'
    require(identity in store.catalog['objects'],'no authenticated current supervisor policy')
    policy=get(store,identity,'SUPERVISOR-SUCCESSION-POLICY-1')
    op=json.loads(auth.operational_binding)
    profile=json.loads(store.resolve('sha256:'+op['governance']['released_profile']['sha256']))
    require(policy['runtime_binding']==runtime_binding(auth,store,profile),'operational context mismatch')
    require(policy['released_supervisor']==historical,'historical release binding changed')
    anchor=json.loads(store.resolve(policy['anchor_id']))
    require((anchor.get('released_supervisor') if anchor['schema']=='SUPERVISOR-HISTORICAL-INSTANCE-1' else legacy_tuple(anchor))==historical,'S1 historical tuple changed')
    if anchor['schema']=='SUPERVISOR-HISTORICAL-INSTANCE-1':
        require(anchor['released_profile_bytes_sha256']==op['governance']['released_profile']['sha256'],'historical profile anchor mismatch')
    data=store.state_path(policy['ledger_id']).read_bytes()
    selected=reconstruct(store,policy,data)
    current=selected['instance']
    require(current['schema']=='SUPERVISOR-INSTANCE-1','historical S1 lacks birth evidence; no current qualified instance')
    observed=observe(current)
    require(observed==current,'fresh supervisor instance observation mismatch')
    legacy=legacy_tuple(current)
    # Existing socket/cgroup/scope QUIESCENT checks are retained verbatim.
    host=legacy_check(legacy,check_scopes=check_scopes)
    require(observe(current)==current,'supervisor changed during readiness')
    require(store.state_path(policy['ledger_id']).read_bytes()==data,'succession changed during readiness')
    return {**host,'SupervisorInstanceId':current['id'],'SupervisorSuccessionHead':selected['head']}
