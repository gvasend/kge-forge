"""Experiment policy, durable content-free telemetry and governed deadline admission.

This module never grants authority. A caller must bind its policy through the
released transmission/operational profile. No provider content is recorded.
"""
from contextlib import contextmanager
from pathlib import Path
import fcntl
import hashlib
import json
import os
import signal
import threading
import time

SCHEMA = 'E1-RUN-CONTROL-1'
E1_POLICY = {'schema': SCHEMA, 'seconds': {'cycle': [120, 300],
    'no_progress': [180, 300], 'invocation': [1200, 1800], 'phase': [30, 120]},
    'requests': [8, 12], 'tokens': [100000, 150000],
    'automatic_retry': False, 'usage_unknown': 'TIME_AND_REQUEST_LIMITS_ONLY'}

class BudgetExceeded(RuntimeError): pass

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def events(path):
    data=Path(path).read_bytes() if Path(path).exists() else b''
    return decode_events(data)

def decode_events(data):
    if data and not data.endswith(b'\n'): raise ValueError('truncated run evidence')
    lines=data.splitlines(keepends=True);rows=[json.loads(x) for x in lines]
    prior=None;seq=0
    prefix=hashlib.sha256()
    for row,line in zip(rows,lines):
        before=prefix.hexdigest();prefix.update(line)
        if row.get('schema')!=SCHEMA: continue
        body=dict(row);fingerprint=body.pop('record_sha256')
        seq+=1
        if row['sequence']!=seq or row['previous']!=prior or digest(body)!=fingerprint or row['audit_prefix_sha256']!=before:
            raise ValueError('run evidence order/hash mismatch')
        prior=fingerprint
    return rows

class RunControl:
    def __init__(self,path,identity,policy,clock=time.monotonic,wall=time.time):
        if policy!=E1_POLICY: raise ValueError('unqualified experiment budget policy')
        self.path=Path(path);self.identity=dict(identity);self.policy=policy
        self.clock=clock;self.wall=wall;self.lock=threading.RLock();self.cycle=0
        self.boot=Path('/proc/sys/kernel/random/boot_id').read_text().strip()
        self.closed=False;self.phase=None;self.cycle_start=None;self.phase_start=None
        self.requests=0;self.responses=0;self.tokens=0;self.usage_known=True;self.warnings=set();self.progress_keys=set()
        rows=[r for r in events(path) if r.get('schema')==SCHEMA]
        if rows:
            first=rows[0]
            if any(r['identity']!=self.identity or r['policy_sha256']!=digest(policy) for r in rows):
                raise ValueError('run identity/policy substitution')
            self.start=first['monotonic'];self.progress=self.start
            if clock()<rows[-1]['monotonic']:raise ValueError('monotonic evidence moved backwards')
            pending_spans=[]
            for r in rows:
                self.cycle=r['cycle']
                name=r['event'];d=r['details']
                if name=='cycle_start':self.cycle_start=r['monotonic'];self.warnings.discard('cycle')
                if name=='cycle_end':self.cycle_start=None
                if name=='span_start':pending_spans.append(r);self.warnings.discard('phase')
                if name=='span_end' and pending_spans:pending_spans.pop()
                if name=='model_request_start':self.requests+=1
                if name=='response_received':
                    self.responses+=1
                    usage=d.get('usage');self.usage_known &= usage is not None
                    if usage:self.tokens+=usage['total_tokens']
                if name=='substantive_progress':self.progress=r['monotonic'];self.progress_keys.add(d['key'])
                if name=='budget_warning':self.warnings.add(d['budget'])
                if name in ('budget_exhausted','admission_closed','final_disposition'):self.closed=True
            if pending_spans:
                self.phase=pending_spans[-1]['details']['name'];self.phase_start=pending_spans[0]['monotonic']
            # A different boot makes monotonic deadlines unprovable. Never reset.
            if first['boot_id']!=self.boot:self.closed=True
            if self.closed:raise BudgetExceeded('closed or uncertain recovered invocation')
            # No automatic replay/continuation of a request interrupted across restart.
            sent=sum(r['event']=='model_request_start' for r in rows)
            received=sum(r['event']=='response_received' for r in rows)
            if sent!=received:
                self.close('UNRESOLVED_MODEL_REQUEST');raise BudgetExceeded('request outcome uncertain')
            self.check()
        else:
            self.start=self.progress=clock()
            self.emit('invocation_start',{})

    def emit(self,name,details):
        created_clock=self.clock();created_wall=self.wall();created_perf=time.monotonic()
        with self.lock:
            mask=signal.pthread_sigmask(signal.SIG_BLOCK,{signal.SIGALRM})
            fd=None;owned=False
            try:
                from .audit_composition import descriptor
                fd=descriptor(self.path)
                lock_start=time.monotonic()
                if fd is None:
                    fd=os.open(self.path,os.O_RDWR|os.O_CREAT|os.O_APPEND|os.O_NOFOLLOW,0o600)
                    owned=True
                    fcntl.flock(fd,fcntl.LOCK_EX)
                lock_wait=time.monotonic()-lock_start
                from .authorization_lifecycle import _append
                def append(event,body):
                    rows=[r for r in events(self.path) if r.get('schema')==SCHEMA]
                    row={'schema':SCHEMA,'event':event,'identity':self.identity,'cycle':self.cycle,
                         'monotonic':self.clock(),'wall_time':self.wall(),'boot_id':self.boot,
                         'sequence':len(rows)+1,'previous':rows[-1]['record_sha256'] if rows else None,
                         'audit_prefix_sha256':hashlib.sha256(self.path.read_bytes()).hexdigest(),
                         'policy_sha256':digest(self.policy),'details':body}
                    row['record_sha256']=digest(row)
                    _append(fd,row)
                    return row
                append_start=time.monotonic()
                if name=='budget_warning':
                    details=dict(details,warning_created_monotonic=created_clock,
                                 warning_created_wall=created_wall,lock_wait_seconds=lock_wait)
                row=append(name,details)
                if name=='budget_warning':
                    persisted_clock=self.clock();persisted_wall=self.wall()
                    append_seconds=time.monotonic()-append_start
                    # Explicit event composition on the same descriptor; no recursion.
                    append('warning_persisted',{'warning_record_sha256':row['record_sha256'],
                        'warning_sequence':row['sequence'],'created_monotonic':created_clock,
                        'created_wall':created_wall,'durable_monotonic':persisted_clock,
                        'durable_wall':persisted_wall,'lock_wait_seconds':lock_wait,
                        'append_and_fsync_seconds':append_seconds,
                        'creation_to_persistence_seconds':time.monotonic()-created_perf})
                return row
            finally:
                if owned and fd is not None:os.close(fd)
                signal.pthread_sigmask(signal.SIG_SETMASK,mask)

    def close(self,reason):
        self.closed=True;self.emit('admission_closed',{'reason':reason})

    def values(self):
        now=self.clock()
        values={'invocation':now-self.start,'no_progress':now-self.progress}
        if self.cycle_start is not None:values['cycle']=now-self.cycle_start
        if self.phase_start is not None and self.phase in ('validation','authorization','response_validation',
                'continuation_construction','private_bootstrap','activation_recovery','host_construction','reasoning_construction','context_reconstruction','decision_consumption','authority_store_resolution','model_projection','non_host_validation'):
            values['phase']=now-self.phase_start
        values['requests']=self.requests
        if self.usage_known:values['tokens']=self.tokens
        return values

    def limits(self,name):return self.policy['seconds'].get(name,self.policy.get(name))

    def check(self,admit_model=False):
        if self.closed:raise BudgetExceeded('admission closed')
        for name,value in self.values().items():
            soft,hard=self.limits(name)
            if value>=soft and name not in self.warnings:
                self.warnings.add(name);self.emit('budget_warning',{'budget':name,'value':value,
                    'operation':self.phase,'last_progress':self.progress})
            # The twelfth request can finish; admission of a thirteenth is denied.
            reached=value>=hard if name!='requests' else value>hard or (admit_model and value>=hard)
            if reached:
                self.closed=True;self.emit('budget_exhausted',{'budget':name,'value':value,
                    'operation':self.phase,'last_progress':self.progress})
                raise BudgetExceeded(name)

    def next_cycle(self):
        self.check();self.cycle+=1;self.cycle_start=self.clock();self.warnings.discard('cycle')
        self.emit('cycle_start',{})

    def progress_event(self,key,kind):
        if key not in self.progress_keys:
            self.progress_keys.add(key);self.progress=self.clock()
            self.emit('substantive_progress',{'key':key,'kind':kind})

    def response(self,response):
        self.responses+=1
        raw=response.get('usage');usage=None
        if isinstance(raw,dict):
            keys=('input_tokens','output_tokens','total_tokens')
            if all(type(raw.get(k)) is int and raw[k]>=0 for k in keys) and raw['total_tokens']==raw['input_tokens']+raw['output_tokens']:
                usage={k:raw[k] for k in keys}
                for group,field in (('input_tokens_details','cached_tokens'),('output_tokens_details','reasoning_tokens')):
                    n=raw.get(group,{}).get(field) if isinstance(raw.get(group,{}),dict) else None
                    if type(n) is int and n>=0:usage[group]={field:n}
        self.usage_known &= usage is not None
        if usage:self.tokens+=usage['total_tokens']
        # Response IDs are provider metadata, not response text/reasoning.
        rid=response.get('id');rid=rid if isinstance(rid,str) and len(rid)<=200 else None
        self.emit('response_received',{'response_id':rid,'usage':usage,
            'usage_state':'REPORTED_ONLY_NO_RESERVATION' if self.usage_known else 'USAGE_UNKNOWN',
            'token_budget_state':'USAGE_UNKNOWN',
            'token_ceiling_enforced':False})

    @contextmanager
    def span(self,name):
        """Interrupt blocking preparation/transport, not only a cooperative loop.
        Existing signal owners are rejected rather than replaced. Nested spans
        retain the outer deadline. A budget exception must reach governed recovery.
        """
        self.check();old=(self.phase,self.phase_start);self.phase=name
        self.phase_start=min(old[1],self.clock()) if old[1] is not None else self.clock()
        if old[1] is None:self.warnings.discard('phase')
        self.emit('span_start',{'name':name})
        outer=getattr(self,'_timer_active',False)
        if not outer and threading.current_thread() is not threading.main_thread():
            raise ValueError('qualified deadline runner requires main thread')
        def alarm(_signum,_frame):
            self.check();self.emit('activity',{'operation':self.phase});arm()
        def arm():
            delays=[15.0]
            for key,value in self.values().items():
                if key not in self.policy['seconds']:continue
                soft,hard=self.limits(key)
                delays.append((hard if key in self.warnings or value>=soft else soft)-value)
            signal.setitimer(signal.ITIMER_REAL,max(.001,min(delays)))
        previous=None
        try:
            if not outer:
                previous=signal.getsignal(signal.SIGALRM)
                if signal.getitimer(signal.ITIMER_REAL)!=(0.0,0.0) or previous not in (signal.SIG_DFL,signal.SIG_IGN):
                    raise ValueError('deadline signal already owned')
                signal.signal(signal.SIGALRM,alarm);self._timer_active=True;self._arm=arm;arm()
            else:self._arm()
            yield
            self.check()
        finally:
            if not outer and getattr(self,'_timer_active',False):
                signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,previous);self._timer_active=False
            self.emit('span_end',{'name':name,'admission_closed':self.closed})
            self.phase,self.phase_start=old
            if outer:self._arm()

def assert_admission(path,policy,identity):
    """Fresh read-only budget check for production validation under its locks."""
    if policy!=E1_POLICY:raise BudgetExceeded('unqualified budget policy')
    rows=[r for r in events(path) if r.get('schema')==SCHEMA]
    if not rows:return # pre-invocation activation only; effect gates require control
    boot=Path('/proc/sys/kernel/random/boot_id').read_text().strip();now=time.monotonic()
    if any(r['identity']!=identity or r['policy_sha256']!=digest(policy) or r['boot_id']!=boot for r in rows):
        raise BudgetExceeded('budget authority/birth mismatch')
    if any(r['event'] in ('admission_closed','budget_exhausted','final_disposition') for r in rows):
        raise BudgetExceeded('durable admission closure')
    first=rows[0]['monotonic'];progress=first;cycle=None;spans=[];requests=0;tokens=0;known=True
    for r in rows:
        name=r['event']
        if name=='substantive_progress':progress=r['monotonic']
        if name=='cycle_start':cycle=r['monotonic']
        if name=='cycle_end':cycle=None
        if name=='span_start':spans.append(r)
        if name=='span_end' and spans:spans.pop()
        if name=='model_request_start':requests+=1
        if name=='response_received':
            usage=r['details'].get('usage');known &= usage is not None
            if usage:tokens+=usage['total_tokens']
    checks={'invocation':now-first,'no_progress':now-progress}
    if cycle is not None:checks['cycle']=now-cycle
    preparation=[r for r in spans if r['details']['name'] in ('validation','authorization','response_validation',
        'continuation_construction','private_bootstrap','activation_recovery','host_construction','reasoning_construction','context_reconstruction','decision_consumption','authority_store_resolution','model_projection','non_host_validation')]
    if preparation:checks['phase']=now-preparation[0]['monotonic']
    if now<rows[-1]['monotonic'] or any(v>=policy['seconds'][k][1] for k,v in checks.items()) or requests>policy['requests'][1] or (known and tokens>=policy['tokens'][1]):
        raise BudgetExceeded('durable budget exhausted')

def status(path,now=None,stale_after=60):
    """Read-only evidence projection. No model content, paths or diagnostics echoed."""
    rows=events(path);timing=[r for r in rows if r.get('schema')==SCHEMA]
    if not timing:return {'state':'UNKNOWN','reason':'NO_TIMING_EVIDENCE'}
    now=time.time() if now is None else now;last=timing[-1]
    stale=now-last['wall_time']>stale_after or now<last['wall_time']
    progress=[r for r in timing if r['event']=='substantive_progress']
    spans=[]
    for r in timing:
        if r['event']=='span_start':spans.append(r)
        elif r['event']=='span_end' and spans:spans.pop()
    final=next((r['details'] for r in reversed(timing) if r['event']=='final_disposition'),None)
    results=[r for r in rows if r.get('event')=='action_result']
    requests=[r for r in rows if r.get('event')=='action_request']
    lifecycle=next((r.get('resulting_state') for r in reversed(rows) if r.get('event')=='authorization_lifecycle_terminal'),None)
    observation=next((r for r in reversed(timing) if r['event']=='governance_observation'),None)
    gov=observation['details'] if observation and 0<=now-observation['wall_time']<=stale_after else {}
    usages=[r['details'].get('usage') for r in timing if r['event']=='response_received']
    reliable=bool(usages) and all(u is not None for u in usages)
    return {'schema':'E1-OPERATOR-STATUS-1','identity':last['identity'],
        'projection_generated':now,'source_sequence':last['sequence'],'freshness':'UNKNOWN' if stale else 'FRESH',
        'lifecycle_state':'UNKNOWN' if stale else lifecycle or gov.get('authorization','UNKNOWN'),
        'authorization_state':'UNKNOWN' if stale else lifecycle or gov.get('authorization','UNKNOWN'),
        'ownership':'UNKNOWN' if stale else (final or gov).get('ownership','UNKNOWN'),
        'supervisor_readiness':'UNKNOWN' if stale else gov.get('supervisor','UNKNOWN'),
        'cycle':last['cycle'],'current_subphase':'UNKNOWN' if stale else spans[-1]['details']['name'] if spans else None,
        'outstanding_operation':'UNKNOWN' if stale else spans[-1]['details']['name'] if spans else None,
        'subphase_start':spans[-1]['wall_time'] if spans else None,
        'last_event_age':max(0,now-last['wall_time']),
        'last_substantive_progress':progress[-1] if progress else None,
        'progress_age':max(0,now-(progress[-1] if progress else timing[0])['wall_time']),
        'activity_is_progress':False,'model_requests':sum(r['event']=='model_request_start' for r in timing),
        'responses':sum(r['event']=='response_received' for r in timing),
        'action_requests':{'pending':len({r['action_request_id'] for r in requests}-{r['action_request_id'] for r in results}),
            'accepted':sum(r.get('result')=='SUCCEEDED' for r in results),'denied':sum(r.get('result')=='DENIED' for r in results)},
        'action_results':len(results),'executions':sum(r.get('event')=='execution_scope_created' for r in rows),
        'authoritative_effects':sum(r.get('result')=='SUCCEEDED' and r.get('type') in ('write','patch') for r in results),
        'budget_state':next((r['details'] for r in reversed(timing) if r['event'] in ('budget_warning','budget_exhausted')),{}),
        'latest_safe_event':last['event'],'terminal_disposition':final,
        'usage_state':'REPORTED_ONLY_NO_RESERVATION' if reliable else 'USAGE_UNKNOWN',
        'reported_cumulative_tokens':sum(u['total_tokens'] for u in usages) if reliable else None,
        'token_budget_state':'USAGE_UNKNOWN',
        'uncertainty':'STALE_OBSERVATION' if stale else (final or {}).get('uncertainty') or (final or {}).get('provider_uncertainty'),
        'token_ceiling_enforced':False}
