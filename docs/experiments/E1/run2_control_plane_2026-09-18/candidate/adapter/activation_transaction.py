"""Controller-only activation transaction. No Programmer tool or model endpoint.

A per-ledger live controller lock fences ownership across controller restarts;
reservation facts live in the existing shared append-only ownership ledger.
Neither ACTIVE evidence nor knowledge of its IDs conveys the live lock.
"""
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from .validation_spans import measured
import fcntl, json, os, stat, signal
from .context_projection import canonical, digest, sha, read_exact, derive
from .authorization_lifecycle import (LifecycleDenied, serialized, original,
    dispatch_binding, reconstruct, event, _read, _append, historical_original)
from .invocation_ownership import InvocationOwnership, OwnershipDenied
from .controller_authority_store import read_authority_ref, require_store


def _lease(path):
    fd=os.open(str(path)+'.controller-lock',os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode): raise LifecycleDenied('controller fence not regular')
        fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BaseException: os.close(fd); raise LifecycleDenied('controller ownership already held')
    return fd


def invocation(fd):
    checker=InvocationOwnership.__new__(InvocationOwnership)
    checker._history(fd)  # strict scope/invocation ordering, including truncated tails
    current=None
    for line in _read(fd).splitlines():
        row=json.loads(line)
        if row['event']=='invocation_reserved':
            body=dict(row); rid=body.pop('reservation_id',None)
            if rid!='INVOCATION-RESERVATION-sha256:'+digest(body):
                raise LifecycleDenied('reservation fingerprint mismatch')
            current=row
        elif row['event']=='invocation_released': current=None
    return current


def execution_guard(ownership):
    """Legacy controllers also respect the invocation fence; owned scopes nest."""
    if ownership.activation_owner is not None:
        ownership.activation_owner.verify_handoff()
        return None
    try: gate=_lease(ownership.path)
    except LifecycleDenied as exc: raise OwnershipDenied(str(exc)) from exc
    try:
        fd=ownership._locked()
        try:
            if invocation(fd) is not None: raise OwnershipDenied('invocation requires recovery')
        finally: os.close(fd)
        return gate
    except BaseException: os.close(gate); raise


def _host(expected, check_scopes=True):
    from .recovery_ledger import CGROUP_BASE, SUPERVISOR_AUDIT, _observe, _events
    pid=expected['pid']; proc=Path('/proc')/str(pid)
    observed={'pid':pid,'ppid':int((proc/'stat').read_text().split(') ',1)[1].split()[1]),
        'exe':str((proc/'exe').resolve()),'exe_sha256':sha((proc/'exe').read_bytes()),
        'cwd':str((proc/'cwd').resolve()),'argv':(proc/'cmdline').read_bytes().rstrip(b'\0').replace(b'\0',b' ').decode(),
        'uid':proc.stat().st_uid,'cgroup':(proc/'cgroup').read_text().strip()}
    if observed!=expected: raise LifecycleDenied('supervisor identity changed')
    socket=Path('/tmp/a21m.sock'); st=socket.lstat()
    if not stat.S_ISSOCK(st.st_mode) or st.st_uid!=expected['uid'] or stat.S_IMODE(st.st_mode)!=0o600:
        raise LifecycleDenied('supervisor socket authority invalid')
    # No active or unclosed scope can be interpreted as a free host.
    events=_events(SUPERVISOR_AUDIT)
    if not CGROUP_BASE.is_dir(): raise LifecycleDenied('supervisor cgroup authority unavailable')
    for path in (CGROUP_BASE.glob('scope-*') if check_scopes else []):
        observed_scope=_observe(path)
        rows=[r for r in events if r.get('scope_id')==path.name]
        if observed_scope['members'] or observed_scope['populated']!=0:
            raise LifecycleDenied('active or uncertain supervisor scope: '+path.name)
    return {'supervisor':observed,'socket_device':st.st_dev,'socket_inode':st.st_ino,
            'cgroup_base':str(CGROUP_BASE)}


def validate_production(auth,audit,dispatch_ref,ledger_fd, *, allow_owned=None, idle_host=True):
    if any(json.loads(line).get('qualification_only') for line in Path(audit).read_bytes().splitlines()):
        raise LifecycleDenied('qualification audit cannot authorize production activation')
    if json.loads(auth.operational_binding)['governance'].get('schema')==7:
        from .attempt_chain import require_issued
        require_issued(auth)
    if json.loads(auth.operational_binding)['governance'].get('schema')==6:
        from .attempt_transition import require_issued
        require_issued(auth)
    if json.loads(auth.operational_binding)['governance'].get('schema')==5:
        from .attempt_context import require_issued
        require_issued(auth)
    if json.loads(auth.operational_binding)['governance'].get('schema')==4:
        from .run2_context import selection
        selection(auth.authorization_id,issued=True)
    return _validate_production(auth,audit,dispatch_ref,ledger_fd,allow_owned=allow_owned,idle_host=idle_host)


@measured('non_host_validation')
def validate_non_host(auth,audit,dispatch_ref,ledger_fd):
    """Non-effecting candidate inspection; never returns an activation proof.

    All non-host production predicates execute. The only excluded observation is
    the live supervisor, after those predicates and recovery have succeeded.
    """
    if json.loads(auth.operational_binding)['governance'].get('schema')!=4:
        raise LifecycleDenied('versioned Run-2 context required for non-host qualification')
    return _validate_production(auth,audit,dispatch_ref,ledger_fd,_qualification=True)


from .history_catalogs import reuse_history_catalogs

@reuse_history_catalogs
def _validate_production(auth,audit,dispatch_ref,ledger_fd, *, allow_owned=None, idle_host=True, _qualification=False, _preissuance=False):
    """One fact-derived operation, called while the controller/ledger/audit are locked.

    Requirements are immutable dispatch-record inputs, not caller-provided PASS
    assertions. Every verification reads current bytes or kernel state. Missing
    selections fail closed; this operation does not repair or choose them.
    """
    from .governance_continuation import verify_authorization
    from .directory_provisioning import open_directory
    from .model_transport import validate as validate_transport
    if _preissuance:
        store=require_store(auth)
        from .controller_authority_store import outside
        if json.loads(auth.operational_binding)['governance'].get('schema')==7:
            from .attempt_chain import selected
        elif json.loads(auth.operational_binding)['governance'].get('schema')==6:
            from .attempt_transition import selected
        else:
            from .attempt_context import selected
        if selected()['mode']!='PREPARED' or auth.state!='INACTIVE':raise LifecycleDenied('unissued preflight only')
        planned=store.catalog['private_state'][auth.authorization_id+':audit']['path']
        outside(planned,store.catalog['programmer_roots'])
        if Path(planned)!=Path(audit) or os.path.lexists(planned):raise LifecycleDenied('attempt audit namespace is not unused')
    else:store=require_store(auth,audit)
    control_policy=json.loads(auth.model_transmission or '{}').get('run_control')
    if control_policy:
        from .run_control import assert_admission
        assert_admission(audit,control_policy,{'authorization_id':auth.authorization_id,
            'session_id':auth.session_id,'invocation_id':auth.turn_id,'work_package_id':auth.work_package_id})
    if (not isinstance(dispatch_ref,dict) or set(dispatch_ref)!={'authority_id','sha256'} or
            dispatch_ref['authority_id']!='E1-ARCHITECT-DISPATCH-sha256:'+dispatch_ref['sha256']):
        raise LifecycleDenied('private logical dispatch reference required for production validation')
    expected_ledger=Path(auth.ownership_ledger).stat();held_ledger=os.fstat(ledger_fd)
    if (expected_ledger.st_dev,expected_ledger.st_ino)!=(held_ledger.st_dev,held_ledger.st_ino):
        raise LifecycleDenied('production ownership ledger descriptor mismatch')
    binding=dispatch_binding(auth,audit,dispatch_ref)
    op=verify_authorization(auth)
    decision=json.loads(read_authority_ref(dispatch_ref))
    requirements_ref=op['governance']['released_profile']
    profile=json.loads(read_authority_ref(requirements_ref))
    if (profile['ownership']['ledger']!=auth.ownership_ledger or profile['ownership']['override_permitted'] is not False
            or profile['runtime']!=json.loads(auth.execution_profile)
            or profile['model_transport']!=json.loads(auth.model_transport)):
        raise LifecycleDenied('released runtime/ownership/transport mismatch')
    if len(profile['supervisor_binding'])!=1:raise LifecycleDenied('ambiguous supervisor selection')
    basisref=op['governance']['release_basis']
    basis=json.loads(read_authority_ref(basisref))
    inputs=basis.get('current_inputs',basis.get('inputs'))
    receipts=[{'path':p,'sha256':r['sha256']} for p,r in inputs.items()
        if r['sha256']==profile['provisioning_receipt_sha256']]
    if len(receipts)!=1:raise LifecycleDenied('provisioning evidence missing or ambiguous')
    provisioning=profile['provisioning_plan']
    req={'execution_profile_sha256':digest(profile['runtime']),
        'provisioned_directories':[row['path'] for row in provisioning['directories']],
        'provisioning_receipt':receipts[0],'supervisor':profile['supervisor_binding'][0],
        'evidence_destinations':[str(Path(audit).parent),str(Path(auth.ownership_ledger).parent)]}
    release=json.loads(read_authority_ref(op['governance']['release_decision']))
    if release['decision']!={'PD06':'RELEASED','E1_B01':'PASS'}: raise LifecycleDenied('release not accepted')
    spec=json.loads(auth.context_projection)
    projection=derive(spec,auth.context_binding)
    identity_keys=('AuthoritativeContextId','FullContextDigest','ModelProjectionDigest')
    if op['governance'].get('schema') in (2,3,4,5,6,7):identity_keys+=('ModelPayloadDigest','ModelProjectionBindingDigest')
    if any(projection[k]!=op['context_identities'][k] for k in identity_keys):
        raise LifecycleDenied('projection binding stale')
    # Use the actual transmission/read validator without emitting audit during
    # atomic observation; its host writes are buffered as controller-local facts.
    from .governed_host import GovernedHost
    from .context_projection import ContextProjection
    proxy=GovernedHost.__new__(GovernedHost);proxy.auth=auth;proxy.audit=Path(audit); buffered=[];proxy._write=buffered.append
    ContextProjection(proxy).verify()
    transport=json.loads(auth.model_transport);validate_transport(transport,transport['endpoint'],transport['model'])
    if auth.shell or auth.network: raise LifecycleDenied('payload shell/network forbidden')
    if req['execution_profile_sha256']!=digest(json.loads(auth.execution_profile)):
        raise LifecycleDenied('execution profile mismatch')
    from .runnable_profile import validate as validate_execution
    runtime=json.loads(auth.execution_profile)
    validate_execution(runtime,runtime['argv'],runtime['cwd'],runtime['inputs'])
    required_dirs=set(auth.write_directory_roots)|{str(Path(p).parent) for p in auth.write_roots}
    if not required_dirs<=set(req['provisioned_directories']): raise LifecycleDenied('required provisioning omitted')
    directories=[]
    for path in req['provisioned_directories']:
        if not any(Path(root)==Path(path) or Path(root) in Path(path).parents for root in auth.read_roots):
            raise LifecycleDenied('provisioning outside authorized root')
        fd=open_directory(path)
        try: st=os.fstat(fd);directories.append({'path':path,'dev':st.st_dev,'ino':st.st_ino})
        finally: os.close(fd)
    receipt=json.loads(read_authority_ref(req['provisioning_receipt']))
    if (receipt['result']!='PASS' or receipt['plan_sha256']!=sha(json.dumps(provisioning,sort_keys=True).encode())
            or receipt['created']!=[row['path'] for row in provisioning['directories'] if row['controller_provisioning_required']]
            or receipt['state']!='INACTIVE' or receipt['profile_activated'] is not False):
        raise LifecycleDenied('provisioning receipt mismatch')
    isolated=[str(Path(audit)),auth.ownership_ledger,auth.ownership_ledger+'.controller-lock',str(store.location('sha256:'+requirements_ref['sha256']))]
    isolated+=req['evidence_destinations']
    for path in isolated:
        if any(Path(path)==Path(root) or Path(root) in Path(path).parents for root in (*auth.read_roots,*auth.write_roots)):
            raise LifecycleDenied('controller evidence within Programmer grant')
    owner=invocation(ledger_fd)
    if owner!=allow_owned: raise LifecycleDenied('conflicting invocation ownership')
    scope=InvocationOwnership.__new__(InvocationOwnership)._history(ledger_fd)
    if scope is not None and (allow_owned is None or any(scope[k]!=allow_owned[k] for k in ('authorization_id','session_id','controller_audit'))):
        raise LifecycleDenied('conflicting execution ownership')
    from .supervisor_amendment import readiness
    if idle_host:
        from .recovery_ledger import reconstruct as recover
        restored=recover(Path(audit),auth)
        if restored and (restored['incomplete'] or restored['category'] in ('ACTIVE','UNCERTAIN','INTERRUPTED')):
            raise LifecycleDenied('unreconciled execution/action audit')
    if _qualification:
        return {'schema':'NON-EFFECTING-RUN2-PREFLIGHT-1','result':'PASS_EXCEPT_CURRENT_SUPERVISOR',
            'non_host_validation':'PASS','current_supervisor':'NOT_OBSERVED',
            'activation_eligible':False,'handoff_eligible':False,'binding':binding,
            'context_identities':op['context_identities'],'authority_store_catalog_sha256':store.catalog_sha256}
    host=readiness(auth,store,req['supervisor'],idle_host,_host)
    if _preissuance:
        return {'schema':'NON-EFFECTING-UNISSUED-ATTEMPT-PREFLIGHT-1','result':'PASS_PENDING_SPECIFIC_ARCHITECT_ISSUANCE',
            'binding':binding,'context_identities':op['context_identities'],'host':host,
            'activation_eligible':False,'handoff_eligible':False,'audit_unused':True}
    body={'schema':'PRODUCTION-DISPATCH-VALIDATION-1','binding':binding,
        'requirements':requirements_ref,'context_identities':op['context_identities'],
        'authority_store':{'catalog_sha256':store.catalog_sha256,
                           'applicability':store.applicability},
        'ReleasedProfileContentId':'sha256:'+requirements_ref['sha256'],
        'OperationalProfileLocation':str(store.location('sha256:'+requirements_ref['sha256'])),
        'clearance_sha256':spec['clearance_sha256'],'launch':op['released_launch'],
        'provisioning':directories,'host':host,'ledger_prefix_sha256':sha(_read(ledger_fd)),
        'audit_prefix_sha256':sha(Path(audit).read_bytes()),
        'ledger_identity':{'device':os.fstat(ledger_fd).st_dev,'inode':os.fstat(ledger_fd).st_ino}}
    return {**body,'validation_id':'DISPATCH-VALIDATION-sha256:'+digest(body)}


class ActivationTransaction:
    def __init__(self,auth,audit,ref):
        store=require_store(auth,audit)
        if not isinstance(ref,str) or not ref.startswith('E1-ARCHITECT-DISPATCH-sha256:'):
            raise LifecycleDenied('logical dispatch identity required; repository references are evidence only')
        dispatch_bytes=store.resolve(ref)
        if ref!='E1-ARCHITECT-DISPATCH-sha256:'+sha(dispatch_bytes):
            raise LifecycleDenied('logical dispatch content mismatch')
        ref={'authority_id':ref,'sha256':sha(dispatch_bytes)}
        self.inactive=replace(auth,state='INACTIVE',operational_binding=canonical(json.loads(original(serialized(auth))['operational_binding'])))
        self.audit=Path(audit).resolve();self.ref=ref;self.fd=None;self.reservation=None
        from .directory_provisioning import open_directory
        raw=Path(auth.ownership_ledger)
        if not raw.is_absolute() or raw.resolve()!=raw:raise LifecycleDenied('noncanonical ownership ledger')
        parent=open_directory(raw.parent);os.close(parent)
        self.ownership=InvocationOwnership(auth.ownership_ledger)
        self.fd=_lease(self.ownership.path)
        self.lease_stat=os.fstat(self.fd)
        self.auth=auth
        self.controller_pid=os.getpid()

    def close(self):
        if self.fd is not None: os.close(self.fd);self.fd=None

    def _locks(self):
        from .audit_composition import enter,leave
        ledger=os.open(self.ownership.path,os.O_RDWR|os.O_NOFOLLOW)
        audit=None;token=None
        try:
            fcntl.flock(ledger,fcntl.LOCK_EX|fcntl.LOCK_NB)
            audit=os.open(self.audit,os.O_RDWR|os.O_APPEND|os.O_NOFOLLOW)
            # No signal-driven emitter may run between acquisition and capability
            # installation. Contention fails closed rather than masking a wait.
            mask=signal.pthread_sigmask(signal.SIG_BLOCK,{signal.SIGALRM})
            try:
                fcntl.flock(audit,fcntl.LOCK_EX|fcntl.LOCK_NB)
                token=enter(self.audit,audit)
                self._audit_token=token
            finally:signal.pthread_sigmask(signal.SIG_SETMASK,mask)
            return ledger,audit
        except BaseException:
            if token is not None:leave(token)
            if audit is not None:os.close(audit)
            os.close(ledger);raise

    def _unlock(self,ledger,audit):
        from .audit_composition import leave
        try:
            if audit is not None:
                leave(self._audit_token)
        finally:
            if audit is not None:os.close(audit)
            if ledger is not None:os.close(ledger)

    def _event(self,fd,previous,name,result,**extra):
        binding=dispatch_binding(self.inactive,self.audit,self.ref)
        auth_hash=digest(historical_original(self.inactive))
        mask=signal.pthread_sigmask(signal.SIG_BLOCK,{signal.SIGALRM})
        try:
            row=event({'event':'authorization_lifecycle_'+name,'version':1,
                'binding':binding,'authorization_sha256':auth_hash,
                'audit_prefix_sha256':sha(_read(fd)),'predecessor_event':previous['last_event_id'],
                'predecessor_state':previous['state'],'resulting_state':result,**extra})
            _append(fd,row);return row
        finally:signal.pthread_sigmask(signal.SIG_SETMASK,mask)

    @classmethod
    def activate(cls,inactive,audit,ref):
        if inactive.state!='INACTIVE': raise LifecycleDenied('INACTIVE predecessor required')
        self=cls(inactive,audit,ref);ledger=fd=None
        ref=self.ref
        try:
            ledger,fd=self._locks()
            previous=reconstruct(_read(fd),inactive,self.audit)
            if previous['state']!='INACTIVE' or previous['uncertain']: raise LifecycleDenied('activation cannot retry or replay')
            receipt=validate_production(inactive,self.audit,ref,ledger)
            _append(fd,{'event':'production_dispatch_validated','receipt':receipt})
            if previous['phase']=='INACTIVE':
                self._event(fd,previous,'dispatch_authorized','INACTIVE')
                previous=reconstruct(_read(fd),inactive,self.audit)
            intent=self._event(fd,previous,'activation_intent','INACTIVE',validation=receipt)
            reservation={'event':'invocation_reserved','authorization_id':inactive.authorization_id,
                'session_id':inactive.session_id,'controller_audit':str(self.audit),
                'validation_id':receipt['validation_id'],'intent_event_id':intent['event_id'],
                'dispatch_record':ref,'ledger_prefix_sha256':sha(_read(ledger))}
            reservation['reservation_id']='INVOCATION-RESERVATION-sha256:'+digest(reservation)
            _append(ledger,reservation);self.reservation=reservation
            previous=reconstruct(_read(fd),inactive,self.audit)
            op=json.loads(inactive.operational_binding);op['dispatch_authorization']=ref
            self.auth=replace(inactive,state='ACTIVE',operational_binding=canonical(op))
            self._event(fd,previous,'activated','ACTIVE',validation=receipt,
                intent_event_id=intent['event_id'],ownership_reservation=reservation,
                effective_authorization_sha256=digest(serialized(self.auth)))
            reconstructed=reconstruct(_read(fd),self.auth,self.audit)
            if reconstructed['activation_event']['ownership_reservation']!=invocation(ledger):
                raise LifecycleDenied('ACTIVE ownership mismatch')
            return self
        except BaseException: self.close();raise
        finally:
            self._unlock(ledger,fd)

    @classmethod
    def recover(cls,inactive,audit,ref):
        self=cls(inactive,audit,ref);ledger=fd=None
        ref=self.ref
        try:
            ledger,fd=self._locks();state=reconstruct(_read(fd),inactive,self.audit)
            owner=invocation(ledger);self.reservation=owner
            eligible=state['state']=='ACTIVE' and not state['uncertain']
            if eligible:
                commit=state['activation_event']
                if owner is None or commit.get('ownership_reservation')!=owner:
                    raise LifecycleDenied('ACTIVE lacks exact authoritative ownership')
                op=json.loads(inactive.operational_binding);op['dispatch_authorization']=ref
                self.auth=replace(inactive,state='ACTIVE',operational_binding=canonical(op))
                current=validate_production(self.auth,self.audit,ref,ledger,allow_owned=owner)
                if any(current[k]!=commit['validation'][k] for k in ('provisioning','ledger_identity','authority_store')):
                    raise LifecycleDenied('activation resource identity changed across restart')
            elif state['state'] in ('COMPLETED','REVOKED','CANCELLED'):
                if owner is not None: raise LifecycleDenied('terminal ownership release incomplete; reconciliation required')
            phase=state['phase']
            if state['uncertain']: phase='OWNERSHIP_HELD_ACTIVATION_INCOMPLETE' if owner else 'ACTIVATION_PENDING'
            elif state['state']=='INACTIVE' and any(json.loads(line).get('event')=='production_dispatch_validated' for line in _read(fd).splitlines()): phase='VALIDATED_NOT_ACTIVATED'
            self.recovery={'lifecycle_state':state['state'],'phase':phase,
                'ownership':owner,'handoff_eligible':eligible,
                'reconciliation_required':state['uncertain'] or (owner is not None and not eligible)}
            return self
        except BaseException:self.close();raise
        finally:
            self._unlock(ledger,fd)

    def verify_handoff(self):
        if self.fd is None or os.getpid()!=self.controller_pid: raise LifecycleDenied('live controller ownership absent')
        actual=os.stat(str(self.ownership.path)+'.controller-lock',follow_symlinks=False)
        if (actual.st_dev,actual.st_ino)!=(self.lease_stat.st_dev,self.lease_stat.st_ino): raise LifecycleDenied('controller fence replaced')
        ledger,fd=self._locks()
        try:
            value=reconstruct(_read(fd),self.auth,self.audit)
            owner=invocation(ledger)
            if value['state']!='ACTIVE' or value['uncertain'] or owner is None or owner!=self.reservation or value['activation_event'].get('ownership_reservation')!=owner:
                raise LifecycleDenied('ACTIVE+OWNED not established')
            current=validate_production(self.auth,self.audit,self.ref,ledger,allow_owned=owner,idle_host=False)
            if (current['provisioning']!=value['activation_event']['validation']['provisioning']
                    or current['ledger_identity']!=value['activation_event']['validation']['ledger_identity']
                    or current['authority_store']!=value['activation_event']['validation']['authority_store']):
                raise LifecycleDenied('provisioned directory identity changed after activation')
            return True
        finally:self._unlock(ledger,fd)

    def attach(self,host):
        if host.auth!=self.auth or host.audit!=self.audit:raise LifecycleDenied('host binding mismatch')
        self.verify_handoff();host.activation_transaction=self
        host.ownership.activation_owner=self

    def complete(self,host,rid):
        self.verify_handoff()
        ledger,fd=self._locks()
        try:
            rows=[json.loads(x) for x in _read(fd).splitlines()]
            terminal=next((x for x in reversed(rows) if x.get('event')=='action_result' and x.get('action_request_id')==rid),None)
            if terminal is None or terminal.get('type')!='finish' or terminal.get('result')!='SUCCEEDED':
                raise LifecycleDenied('terminal ActionResult required')
            if self.ownership._history(ledger) is not None or host._actions_inflight or (host.scope and host.scope.state!='QUIESCENT'):
                raise LifecycleDenied('terminal before authoritative QUIESCENT')
            previous=reconstruct(_read(fd),self.auth,self.audit)
            row=self._event(fd,previous,'terminal','COMPLETED',terminal_action_result_sha256=digest(terminal))
            _append(ledger,{'event':'invocation_released','reservation_id':self.reservation['reservation_id'],
                'terminal_event_id':row['event_id'],'terminal_action_result_sha256':digest(terminal)})
        finally:self._unlock(ledger,fd)
        self.close()

    from .validation_spans import reconciliation_only

    @reconciliation_only
    def cancel(self,host,reason):
        """Typed cancellation after interruption; uncertain actions retain ownership."""
        if self.fd is None:raise LifecycleDenied('cancellation requires controller fence')
        if host.audit!=self.audit or host.auth.authorization_id!=self.auth.authorization_id:
            raise LifecycleDenied('cancellation host identity mismatch')
        if not host._interruption_requested:raise LifecycleDenied('governed interruption required')
        ledger,fd=self._locks()
        try:
            previous=reconstruct(_read(fd),self.inactive,self.audit)
            owner=invocation(ledger)
            if previous['state']=='CANCELLED' and owner is None:
                return {'disposition':'CANCELLED','ownership':'RELEASED','uncertainty':None}
            if previous['state']!='ACTIVE' or owner!=previous['activation_event']['ownership_reservation']:
                raise LifecycleDenied('cancellation predecessor/ownership mismatch')
            rows=[json.loads(x) for x in _read(fd).splitlines()]
            requests={r['action_request_id'] for r in rows if r.get('event')=='action_request'}
            results={r['action_request_id']:r for r in rows if r.get('event')=='action_result'}
            uncertain=(requests-set(results) or any(r.get('result')=='INDETERMINATE' for r in results.values())
                or host._actions_inflight or self.ownership._history(ledger) is not None
                or (host.scope and host.scope.state!='QUIESCENT'))
            if uncertain:
                return {'disposition':'INDETERMINATE','ownership':'HELD_FOR_RECONCILIATION',
                        'uncertainty':'ACTION_OR_EXECUTION_OUTCOME_UNRESOLVED'}
            row=self._event(fd,previous,'terminal','CANCELLED',reason=reason,interruption_requested=True)
            _append(ledger,{'event':'invocation_released','reservation_id':owner['reservation_id'],
                'terminal_event_id':row['event_id'],'reason':reason})
            return {'disposition':'CANCELLED','ownership':'RELEASED','uncertainty':None,
                    'terminal_event_id':row['event_id']}
        finally:self._unlock(ledger,fd)
