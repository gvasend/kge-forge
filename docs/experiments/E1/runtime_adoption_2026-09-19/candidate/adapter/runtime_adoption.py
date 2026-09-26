"""Typed ordinary-runtime adoption. Immutable private decisions plus serialized journal.

The bootstrap-pinned private catalog selects the MATERIAL policy and its exact
Architect decisions. Record labels or an unpinned candidate confer no authority.
The journal is the sole current-head authority: HEAD_COMMITTED is its linearization
point. Qualification catalogs cannot be used for production adoption.
"""
import fcntl
import json
import os
import stat
from contextlib import contextmanager
from pathlib import Path
from .controller_authority_store import encoded, sha, outside

POLICY = 'controller:runtime-head-policy'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def identity(kind, value):
    return kind + '-sha256:' + sha(encoded(value))


def seal(kind, value):
    return dict(value, id=identity(kind, value))


def unseal(kind, value):
    body = {k: v for k, v in value.items() if k != 'id'}
    require(value.get('id') == identity(kind, body), 'changed ' + kind)
    return body


def read(store, ref):
    require(set(ref) == {'authority_id', 'sha256'}, 'malformed private reference')
    b = store.resolve(ref['authority_id'])
    require(sha(b) == ref['sha256'], 'private reference substitution')
    return json.loads(b)


def descriptor(store, ref, live=False):
    d = read(store, ref)
    require(set(d) == {'schema', 'identity', 'root', 'files'}, 'runtime descriptor shape')
    require(d['schema'] == 'RUNTIME-INVENTORY-1' and d['files'], 'runtime schema')
    require(d['identity'] == 'sha256:' + sha(encoded(d['files'])), 'runtime identity')
    outside(d['root'], store.catalog['programmer_roots'])
    for name, h in d['files'].items():
        require(Path(name).name == name and name.endswith('.py'), 'runtime inventory path')
        require(sha(store.resolve('sha256:' + h)) == h, 'missing immutable runtime byte')
    if live:
        root = Path(d['root']) / 'adapter'
        require(root.resolve() == root and not root.is_symlink(), 'runtime root alias')
        files = list(root.glob('*.py'))
        require(all(not f.is_symlink() for f in files), 'runtime byte alias')
        require({f.name: sha(f.read_bytes()) for f in files} == d['files'], 'unaccounted runtime')
    return d


def policy(store):
    p = json.loads(store.resolve(POLICY))
    unseal('RUNTIME-HEAD-AUTHORITY', p)
    require(p['schema'] == 'RUNTIME-HEAD-AUTHORITY-1', 'runtime policy schema')
    require(p['binding_kind'] in ('PRODUCTION_ADOPTION', 'QUALIFICATION_BINDING'), 'runtime policy kind')
    a = read(store, p['material_amendment'])
    unseal('RUNTIME-CONSUMPTION-AMENDMENT', a)
    require(a['schema'] == 'RUNTIME-CONSUMPTION-AMENDMENT-1' and a['classification'] == 'MATERIAL', 'material runtime mechanism required')
    require(a['release_context'] == p['release_context'] and a['mechanism'] == p['mechanism'], 'runtime policy ancestry')
    require(a['rules'] == RULES, 'runtime policy changed')
    grant = read(store, p['material_decision'])
    source = read(store, grant['authority_source'])
    expected = {'authority': 'Architect', 'decision': 'ADOPT_RUNTIME_CONSUMPTION_AMENDMENT',
                'amendment': p['material_amendment'], 'binding_kind': p['binding_kind']}
    require({k:v for k,v in grant.items() if k != 'authority_source'} == expected and source == dict(expected, channel='user'), 'material decision not authenticated')
    require(store.applicability.get('runtime_head_authority') == p['id'], 'runtime policy not selected by bootstrap')
    # Exact execution of the qualified consumer is itself an authority dependency.
    require(sha(Path(__file__).read_bytes()) == p['mechanism']['sha256'], 'runtime consumer implementation changed')
    require(sha(store.resolve(p['mechanism']['authority_id'])) == p['mechanism']['sha256'], 'runtime consumer private identity')
    descriptor(store, p['genesis'])
    return p


RULES = ['exact_predecessor', 'qualified_exact_delta', 'explicit_architect_adoption',
         'single_writer', 'durable_intent_then_head_commit', 'no_implicit_retry',
         'fresh_actual_bytes', 'immutable_historical_bindings', 'unknown_fails_closed']


def transition(store, p, continuation_ref, grant_ref):
    # A finite pin is a decision selected by controller bootstrap, not caller PASS.
    require({'continuation': continuation_ref, 'grant': grant_ref} in p['adoptions'], 'unselected adoption authority')
    c = read(store, continuation_ref); unseal('IMPLEMENTATION-RUNTIME-CONTINUATION', c)
    require(c['schema'] == 'IMPLEMENTATION-RUNTIME-CONTINUATION-1' and c['classification'] == 'NON_MATERIAL_IMPLEMENTATION_CONTINUATION', 'continuation applicability')
    require(c['release_context'] == p['release_context'], 'stale continuation ancestry')
    before = descriptor(store, c['predecessor']); after = descriptor(store, c['successor'], live=True)
    expected = [{'path': n, 'old_sha256': before['files'].get(n), 'new_sha256': after['files'].get(n)}
                for n in sorted(set(before['files']) | set(after['files'])) if before['files'].get(n) != after['files'].get(n)]
    require(expected and c['delta'] == expected, 'inexact implementation delta')
    q = read(store, c['qualification']); unseal('RUNTIME-QUALIFICATION', q)
    require(q['schema'] == 'RUNTIME-QUALIFICATION-1' and q['result'] == 'PASS' and q['delta'] == expected and
            q['predecessor'] == before['identity'] and q['successor'] == after['identity'] and
            q['classification'] == c['classification'], 'qualification substitution')
    require(c['qualification'] in p['qualified_evidence'], 'caller qualification assertion')
    for ref in q['evidence']:
        read(store, ref)
    if c['original_continuation'] is not None:
        original = read(store, c['original_continuation'])
        from .continuation_envelope import seal as original_seal, BODY_KEYS
        require(original == original_seal({k:original[k] for k in BODY_KEYS}, original['approval']), 'original continuation altered')
        require(original['classification'] == c['classification'] and
                sorted((Path(r['path']).name, r['old_sha256'], r['new_sha256']) for r in original['artifacts']) ==
                sorted((r['path'],r['old_sha256'],r['new_sha256']) for r in expected), 'original continuation delta differs')
        require(original['predecessor_OperationalContextId'] == p['release_context']['OperationalContextId'] and
                original['predecessor_chain_digest'] == p['release_context']['continuation_chain_digest'], 'original continuation ancestry differs')
    grant = read(store, grant_ref)
    body = {'authority': 'Architect', 'decision': 'ADOPT_EXACT_RUNTIME_CONTINUATION',
            'continuation': continuation_ref, 'predecessor': before['identity'], 'successor': after['identity'],
            'runtime_head_authority': p['id'], 'release_context': p['release_context'],
            'binding_kind': p['binding_kind']}
    # Avoid a self-referential policy/grant hash: grant binds immutable amendment,
    # genesis and mechanism; the bootstrap-selected policy pins the grant itself.
    body.pop('runtime_head_authority');body['material_amendment'] = p['material_amendment']
    require({k:v for k,v in grant.items() if k!='authority_source'} == body and
            read(store, grant['authority_source']) == dict(body, channel='user'), 'stale or unapproved adoption')
    return c, before, after


@contextmanager
def locked(store, p, write=False):
    path = store.state_path(p['journal'])
    fd = os.open(path, (os.O_RDWR if write else os.O_RDONLY) | os.O_NOFOLLOW)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX if write else fcntl.LOCK_SH)
        st = os.fstat(fd); now = path.lstat()
        require((st.st_dev,st.st_ino)==(now.st_dev,now.st_ino) and stat.S_ISREG(st.st_mode) and st.st_nlink==1, 'runtime journal replaced')
        yield fd
    finally:
        os.close(fd)


def data(fd):
    os.lseek(fd, 0, os.SEEK_SET)
    chunks=[]
    while True:
        b=os.read(fd,65536)
        if not b: return b''.join(chunks)
        chunks.append(b)
        require(sum(map(len,chunks)) <= 32*1024*1024, 'runtime journal bound exceeded')


def reconstruct_locked(store,p,fd):
    raw=data(fd); require(not raw or raw.endswith(b'\n'), 'INDETERMINATE: torn runtime journal')
    head=descriptor(store,p['genesis'])['identity'];head_ref=p['genesis'];chain=[];pending=None;last=None;used=set();history=[]
    for number,line in enumerate(raw.splitlines()):
        row=json.loads(line);body=unseal('RUNTIME-ADOPTION-EVENT',row)
        require(set(body)=={'schema','sequence','previous','event','continuation','grant','predecessor','successor'} and
                body['schema']=='RUNTIME-ADOPTION-EVENT-1' and body['sequence']==number and body['previous']==last,'INDETERMINATE: journal order')
        c,b,a=transition(store,p,body['continuation'],body['grant'])
        require(body['predecessor']==b['identity'] and body['successor']==a['identity'],'INDETERMINATE: journal binding')
        pair=(body['continuation'],body['grant']);event=body['event']
        if event=='ADOPTION_INTENT':
            require(pending is None and head==b['identity'] and c['id'] not in used,'INDETERMINATE: competing or replayed intent')
            pending=pair;used.add(c['id'])
        elif event=='HEAD_COMMITTED':
            require(pending==pair and head==b['identity'],'INDETERMINATE: skipped predecessor')
            head=a['identity'];head_ref=c['successor'];chain.append(c['id'])
        elif event=='ADOPTION_RECORDED':
            require(pending==pair and head==a['identity'],'INDETERMINATE: adoption not committed');pending=None
        elif event=='INTENT_ABORTED':
            require(pending==pair and head==b['identity'],'INDETERMINATE: committed adoption cannot abort');pending=None
        else:raise ValueError('INDETERMINATE: unknown runtime event')
        history.append(row);last=row['id']
    descriptor(store,head_ref,live=True)
    return {'current_runtime':head,'current_descriptor':head_ref,'continuations':chain,'pending':pending,'used':sorted(used),'events':history,'head_event':last,'binding_kind':p['binding_kind']}


def append(fd,state,event,cref,gref,before,after):
    row=seal('RUNTIME-ADOPTION-EVENT',{'schema':'RUNTIME-ADOPTION-EVENT-1','sequence':len(state['events']),
             'previous':state['head_event'],'event':event,'continuation':cref,'grant':gref,
             'predecessor':before['identity'],'successor':after['identity']})
    blob=encoded(row)+b'\n';os.lseek(fd,0,os.SEEK_END)
    # Partial append is intentionally detectable and INDETERMINATE on recovery.
    while blob:
        n=os.write(fd,blob);require(n>0,'journal write failed');blob=blob[n:]
    os.fsync(fd)


def reconstruct(store):
    p=policy(store)
    with locked(store,p) as fd:return reconstruct_locked(store,p,fd)


def adopt(store, continuation_ref, grant_ref, *, binding_kind='PRODUCTION_ADOPTION'):
    p=policy(store);require(p['binding_kind']==binding_kind,'qualification cannot adopt production')
    with locked(store,p,True) as fd:
        state=reconstruct_locked(store,p,fd)
        c,b,a=transition(store,p,continuation_ref,grant_ref)
        require(state['pending'] is None and c['id'] not in state['used'] and state['current_runtime']==b['identity'],'competing, replayed or stale adoption')
        for event in ('ADOPTION_INTENT','HEAD_COMMITTED','ADOPTION_RECORDED'):
            # Fresh immutable catalog/bytes and current head under one writer lock.
            policy(store);transition(store,p,continuation_ref,grant_ref)
            append(fd,state,event,continuation_ref,grant_ref,b,a)
            state=reconstruct_locked(store,p,fd)
        return state


def recover(store):
    """Complete only terminal audit; never turn a pending intent into adoption."""
    p=policy(store)
    with locked(store,p,True) as fd:
        s=reconstruct_locked(store,p,fd)
        if s['pending']:
            cref,gref=s['pending'];c,b,a=transition(store,p,cref,gref)
            event='ADOPTION_RECORDED' if s['current_runtime']==a['identity'] else 'INTENT_ABORTED'
            append(fd,s,event,cref,gref,b,a);s=reconstruct_locked(store,p,fd)
        return s


def validate_invocation_runtime(store, binding, actual_root):
    p=policy(store);require(p['binding_kind']=='PRODUCTION_ADOPTION','qualification not production execution')
    s=reconstruct(store);require(s['pending'] is None,'runtime transition unresolved')
    require(binding=={'runtime_head_authority':p['id'],'runtime':s['current_runtime'],'head_event':s['head_event']},'invocation runtime is not current adopted head')
    d=descriptor(store,s['current_descriptor'],live=True)
    require(Path(actual_root).resolve()==Path(d['root']).resolve(),'unaccounted runtime')
    return s


def production_identities(store, predecessor_release, predecessor_ids, binding):
    """Bind production context to adopted head; historical context is untouched."""
    p=policy(store);s=reconstruct(store)
    require(p['binding_kind']=='PRODUCTION_ADOPTION' and s['pending'] is None,'production runtime not settled')
    require(binding=={'runtime_head_authority':p['id'],'runtime':s['current_runtime'],'head_event':s['head_event']},'runtime context substitution')
    require(p['release_context']==dict(predecessor_ids,release_authority=predecessor_release),'runtime release/context ancestry mismatch')
    release=identity('E1-RELEASE-AUTHORITY',{'predecessor':predecessor_release,'runtime_consumption_amendment':p['material_amendment']})
    ids=dict(predecessor_ids)
    ids['OperationalContextId']=identity('E1-OPERATIONAL-CONTEXT',{'predecessor':predecessor_ids['OperationalContextId'],'runtime_binding':binding})
    ids['continuation_chain_digest']=sha(encoded({'predecessor':predecessor_ids['continuation_chain_digest'],'runtime_binding':binding}))
    return release,ids
