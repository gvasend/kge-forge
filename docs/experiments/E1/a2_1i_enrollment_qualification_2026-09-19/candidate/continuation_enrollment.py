"""Prospective enrollment only. This module cannot adopt or select a runtime.

The host supplies a pinned private decision store, not caller-supplied decisions.
Qualification and Architect enrollment decisions are distinct trusted catalog
entries. Production provisioning of those entries is an external authority act.
The delegated journal grants eligibility only; consumers must separately validate
the adoption decision and serialize their head transition against freshness.
"""
import fcntl
import json
import os
import stat
from contextlib import contextmanager
from pathlib import Path
from adapter.runtime_adoption import read, seal, unseal, require, descriptor
from adapter.controller_authority_store import encoded, sha

DELEGATION = 'controller:future-enrollment-delegation'


def delegation(store):
    d = json.loads(store.resolve(DELEGATION))
    unseal('CONTINUATION-ENROLLMENT-DELEGATION', d)
    require(d['schema'] == 'CONTINUATION-ENROLLMENT-DELEGATION-1', 'delegation schema')
    require(d['binding_kind'] in ('QUALIFICATION_BINDING', 'PRODUCTION_ENROLLMENT'), 'delegation kind')
    require(store.applicability.get('enrollment_delegation') == d['id'], 'unselected delegation')
    require(d['capability'] == 'ENROLL_EXACT_QUALIFIED_CONTINUATION_ONLY', 'delegation scope')
    require(d['mechanism_sha256'] == sha(Path(__file__).read_bytes()), 'enrollment implementation changed')
    source = read(store, d['authority_source'])
    require(source == {'authority': 'Architect', 'decision': 'DELEGATE_FUTURE_ENROLLMENT',
                      'lineage': d['lineage'], 'binding_kind': d['binding_kind'],
                      'capability': d['capability']}, 'delegation authority mismatch')
    return d


def trusted(store, role, ref):
    obj = read(store, ref)
    # The alias must be provisioned by the separate authority intake. A candidate
    # object existing in the catalog is not a qualification/enrollment decision.
    require(store.resolve(role + ':' + ref['sha256']) == encoded(obj), 'unselected decision')
    return obj


def validate(store, d, candidate_ref, qualification_ref, decision_ref):
    c = read(store, candidate_ref); unseal('FUTURE-CONTINUATION-CANDIDATE', c)
    require(c['schema'] == 'FUTURE-CONTINUATION-CANDIDATE-1', 'candidate schema')
    require(c['lineage'] == d['lineage'] and c['context'] == d['context'], 'candidate ancestry')
    before = descriptor(store, c['predecessor']); after = descriptor(store, c['successor'], live=True)
    delta = [{'path':n, 'old_sha256':before['files'].get(n), 'new_sha256':after['files'].get(n)}
             for n in sorted(set(before['files']) | set(after['files'])) if before['files'].get(n) != after['files'].get(n)]
    require(delta and delta == c['delta'], 'candidate delta')
    q = trusted(store, 'qualification-attestation', qualification_ref)
    unseal('CONTINUATION-QUALIFICATION-ATTESTATION', q)
    require(q['schema'] == 'CONTINUATION-QUALIFICATION-ATTESTATION-1' and
            q['candidate'] == candidate_ref and q['result'] == 'PASS' and
            q['qualification_policy'] == d['qualification_policy'] and
            q['binding_kind'] == d['binding_kind'], 'qualification mismatch')
    require(q['evidence'], 'missing qualification evidence')
    for ref in q['evidence']: read(store, ref)
    grant = trusted(store, 'enrollment-decision', decision_ref)
    unseal('CONTINUATION-ENROLLMENT-DECISION', grant)
    require(grant['schema'] == 'CONTINUATION-ENROLLMENT-DECISION-1' and
            grant['authority'] == 'Architect' and grant['decision'] == 'ENROLL_ONLY' and
            grant['delegation'] == d['id'] and grant['candidate'] == candidate_ref and
            grant['qualification'] == qualification_ref and grant['binding_kind'] == d['binding_kind'],
            'unauthorized enrollment decision')
    return c, before, after, grant


@contextmanager
def lock(store, d, write):
    path = store.state_path(d['journal'])
    fd = os.open(path, (os.O_RDWR if write else os.O_RDONLY) | os.O_NOFOLLOW)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX if write else fcntl.LOCK_SH)
        a, b = os.fstat(fd), path.lstat()
        require(stat.S_ISREG(a.st_mode) and a.st_nlink == 1 and
                (a.st_dev,a.st_ino) == (b.st_dev,b.st_ino), 'journal substitution')
        yield fd
    finally:
        os.close(fd)


def history(store, d, fd):
    os.lseek(fd, 0, os.SEEK_SET)
    raw = b''
    while True:
        chunk = os.read(fd, 65536)
        if not chunk: break
        raw += chunk
        require(len(raw) <= 32*1024*1024, 'journal bound')
    require(not raw or raw.endswith(b'\n'), 'INDETERMINATE torn enrollment')
    rows = []; last = None; candidates = set(); decisions = set()
    for line in raw.splitlines():
        row = json.loads(line); unseal('CONTINUATION-ENROLLMENT', row)
        require(set(row) == {'id','schema','sequence','previous','delegation','candidate','qualification','decision','predecessor','head_event'}, 'enrollment shape')
        require(row['schema'] == 'CONTINUATION-ENROLLMENT-1' and row['sequence'] == len(rows) and
                row['previous'] == last and row['delegation'] == d['id'], 'enrollment order')
        c,b,a,g = validate(store,d,row['candidate'],row['qualification'],row['decision'])
        require(row['predecessor'] == b['identity'] and row['head_event'] == g['head_event'], 'enrollment binding')
        require(c['id'] not in candidates and row['decision']['sha256'] not in decisions, 'enrollment replay')
        candidates.add(c['id']); decisions.add(row['decision']['sha256']); rows.append(row); last = row['id']
    return rows


@contextmanager
def current_head(base_store, d):
    # Fresh authenticated reconstruction, never a caller-supplied runtime string.
    from adapter import runtime_adoption as r
    p = r.policy(base_store)
    require(p['id'] == d['lineage'], 'wrong runtime lineage')
    from adapter.runtime_bootstrap import require_established
    require_established(base_store, p)
    # Global order: runtime-head authority, then enrollment journal. Keep the
    # predecessor stable through enrollment commit. Never acquire in reverse.
    with r.locked(base_store, p) as fd:
        s = r.reconstruct_locked(base_store, p, fd)
        require(s['pending'] is None, 'pending runtime transition')
        yield s


def enroll(store, base_store, candidate, qualification, decision, *, binding_kind):
    d = delegation(store)
    require(d['binding_kind'] == binding_kind, 'qualification/production boundary')
    with current_head(base_store,d) as head, lock(store,d,True) as fd:
        rows = history(store,d,fd)
        c,b,a,g = validate(store,d,candidate,qualification,decision)
        require(head['current_runtime'] == b['identity'] and head['head_event'] == g['head_event'], 'stale enrollment')
        require(all(row['candidate'] != candidate and row['decision'] != decision for row in rows), 'enrollment replay')
        row = seal('CONTINUATION-ENROLLMENT', {'schema':'CONTINUATION-ENROLLMENT-1',
            'sequence':len(rows),'previous':rows[-1]['id'] if rows else None,'delegation':d['id'],
            'candidate':candidate,'qualification':qualification,'decision':decision,
            'predecessor':b['identity'],'head_event':head['head_event']})
        blob = encoded(row)+b'\n'; os.lseek(fd,0,os.SEEK_END)
        while blob:
            n = os.write(fd,blob); require(n>0,'enrollment write failed'); blob=blob[n:]
        os.fsync(fd)
        return row


def require_eligible(store, base_store, candidate, enrollment_id, *, binding_kind):
    d = delegation(store)
    require(d['binding_kind'] == binding_kind, 'qualification/production boundary')
    with current_head(base_store,d) as head, lock(store,d,False) as fd:
        rows = history(store,d,fd)
        matches = [row for row in rows if row['id'] == enrollment_id and row['candidate'] == candidate]
        require(len(matches) == 1, 'absent or mismatched enrollment')
        row = matches[0]
        require((head['current_runtime'],head['head_event']) == (row['predecessor'],row['head_event']), 'stale enrollment')
        return row
