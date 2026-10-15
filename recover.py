#!/usr/bin/env python3
"""Single descriptor-held profile recovery; import is inert.

--preflight is read-only. --execute permanently consumes the real attempt.
Never rerun execute after any failure, interruption or unknown outcome.
"""
import argparse
import ast
import contextlib
import fcntl
import hashlib
import json
import os
import pathlib
import stat
import subprocess
import sys
import tempfile

ROOT = pathlib.Path('/home/gvasend/app/kge-forge')
DOMAIN = ROOT / 'docs/plans/governance/development-model-adoption-standing-grant-issuance'
SOURCE = str(DOMAIN / 'restricted-permission-profile.toml.txt')
DEST = '/home/gvasend/.codex/kge-forge-class-a.config.toml'
SOURCE_SHA = 'b694333f4c108c8fea455f7e117cda1d003f3c915bb36d78ae7ec466022b47f8'
EMPTY_SHA = hashlib.sha256(b'').hexdigest()
SUBJECT_SHA = '053746137f0a34133cf2a3fb1859bfb318f386c373a3c4c497518a9f0c32cc23'
GRANT_SHA = '47e5b27349c076eea1a232f7e0ea5380bcf496f12fd1f4cc49bf6b389adb22a8'
ATTEMPT_KEY = '48f7ff401d5bfec3a300f79f2bab28eece53e0243865994d54fc2ae58c8c1e1f'
CONSUMPTION = DOMAIN / ('profile-recovery-attempt-' + ATTEMPT_KEY + '.json')
PYTHON = '/usr/bin/python3.8'
PYTHON_SHA = '298a9e830ed52f36c299427565485d717d1ce0179c0597cc16560513eb780b06'
PUBLISHER = ROOT / 'docs/plans/qualification/E2_P05_D01_A15_NORMATIVE_ADOPTION_ISSUANCE_68/issue.py'
PUBLISHER_SHA = 'ba6c00589e88ffb7d380538758c15ff648d431e55325e933d6f911d04a9af0bc'
SIZE = 1091
EXPECTED_UID = EXPECTED_GID = 1000
EXPECTED_MODE = 0o600
EXPECTED_RECEIPT = (64768, 2262825)  # Owner-supplied receipt, rechecked at execution.
# Parsing guards, not new authority/resource allocations.
MAX_JSON_BYTES = 16 * 1024 * 1024
RECORD_NAMESPACE = 'kge-forge-profile-recovery-consumption-record-v1'
PINS = {
    'profile-installation-recovery-subject.json': 'f08756ba6ee7d0532ffa727fa6c3e1f45eb165152e80f4512e720952c2976a82',
    'issued-profile-installation-recovery-grant.json': '54cc7c154c27d6c577c0cbab3ef1afb9784691882343f6a9fcd12aed54e72f14',
    'profile-recovery-effectiveness-reference.json': 'a1243a71f9a92d2fea04eff64893e842f2103986a0e1427ec3651285a05aa409',
    'profile-recovery-custody-supplement-subject.json': 'bdc27757859c1cb2d70a38356780b4d271e9ed40ea6ac26808bfc7cadfc13ca8',
    'profile-recovery-custody-adoption-record.json': 'fbe4a8b81d0ad94174888d1dce36b1b27936796060bc67c23d88ebaf42997b54',
    'profile-recovery-custody-effectiveness-reference.json': '9d74292c442d8d79ac148d0be61336df00ffb14b050399f5964118d63c2a4a31',
    'profile-recovery-custodian-declaration-reconciliation.json': '2a6942bb2ea7f7e4a946201196cd02bcf98d84005d9e285aa49d7aa1db3b0406',
    'profile-recovery-custodian-initial-declaration.txt': '5408ed9b89fb992fc955ad6690a762deaa8b2495cb9079f999cce587f8f6bd89',
    'profile-recovery-operator-handoff.json': '7b3c76d2360d3abef6f47e4521dab24eb1aa9fdf8a44d1c7b3287ae31098d68f',
    'profile-recovery-effectiveness-four-seed.json': 'e918a4831fd4b64d1fb48bcaf84dcac99ecdc3312278852efd36f672a5a0b00f',
    'profile-recovery-custody-effectiveness-four-seed.json': 'ab021b437f8a7659533aa961e89c93661d5dc45c0ae7245f831e89eb1317a8bc',
}

class Stop(Exception):
    pass

def require(ok, message):
    if not ok:
        raise Stop(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode('ascii')

def identity(namespace, value):
    return {'kind': 'CONTENT_IDENTITY', 'namespace': namespace, 'sha256': sha(canonical(value))}

def checked_directory(st):
    require(stat.S_ISDIR(st.st_mode) and st.st_uid in (0, EXPECTED_UID), 'unsafe parent owner/type')
    require(not st.st_mode & stat.S_IWOTH or
            (st.st_uid == 0 and st.st_mode & stat.S_ISVTX), 'unsafe writable parent')
    require(not st.st_mode & stat.S_IWGRP or st.st_gid in (0, EXPECTED_GID), 'unsafe parent group')

@contextlib.contextmanager
def directory_fd(path):
    p = pathlib.PurePosixPath(str(path))
    require(p.is_absolute() and '..' not in p.parts, 'invalid absolute path')
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    fd = os.open('/', flags)
    try:
        checked_directory(os.fstat(fd))
        for part in p.parts[1:]:
            nxt = os.open(part, flags, dir_fd=fd)
            try:
                checked_directory(os.fstat(nxt))
            except BaseException:
                os.close(nxt)
                raise
            os.close(fd)
            fd = nxt
        yield fd
    finally:
        os.close(fd)

def read_fd(fd, limit):
    data = bytearray()
    while len(data) <= limit:
        part = os.read(fd, min(65536, limit + 1 - len(data)))
        if not part:
            break
        data.extend(part)
    require(len(data) <= limit, 'input exceeds implementation read bound')
    return bytes(data)

def read_path(path, limit=MAX_JSON_BYTES):
    p = pathlib.Path(path)
    with directory_fd(p.parent) as parent:
        fd = os.open(p.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK, dir_fd=parent)
        try:
            before = os.fstat(fd)
            require(stat.S_ISREG(before.st_mode), 'input is not regular')
            data = read_fd(fd, limit)
            after = os.fstat(fd)
            require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) ==
                    (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns),
                    'input changed while reading')
            named = os.stat(p.name, dir_fd=parent, follow_symlinks=False)
            require((named.st_dev, named.st_ino) == (after.st_dev, after.st_ino), 'input path changed')
            return data
        finally:
            os.close(fd)

def decode_json(data):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    def invalid(_):
        raise Stop('non-finite JSON value')
    return json.loads(data.decode('utf-8'), object_pairs_hook=pairs, parse_constant=invalid)

def verify_identity(value, payload='RECORD', field='IDENTITY'):
    ident = value[field]
    require(ident == identity(ident['namespace'], value[payload]), 'canonical identity mismatch')

def read_source():
    data = read_path(SOURCE, SIZE)
    require(len(data) == SIZE and sha(data) == SOURCE_SHA, 'source identity mismatch')
    return data

def validate_destination(st, expected, size):
    require(stat.S_ISREG(st.st_mode), 'destination is not regular')
    require(st.st_uid == EXPECTED_UID and st.st_gid == EXPECTED_GID, 'destination owner mismatch')
    require(stat.S_IMODE(st.st_mode) == EXPECTED_MODE, 'destination mode mismatch')
    require(st.st_nlink == 1 and st.st_size == size, 'destination link/size mismatch')
    if expected is not None:
        require((st.st_dev, st.st_ino) == expected, 'destination receipt identity mismatch')

def verify_held_path(parent, name, fd, expected, size):
    held = os.fstat(fd)
    named = os.stat(name, dir_fd=parent, follow_symlinks=False)
    validate_destination(held, expected, size)
    validate_destination(named, expected, size)
    require((held.st_dev, held.st_ino) == (named.st_dev, named.st_ino), 'destination pathname replaced')

def inspect_destination():
    p = pathlib.Path(DEST)
    with directory_fd(p.parent) as parent:
        fd = os.open(p.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK, dir_fd=parent)
        try:
            st = os.fstat(fd)
            validate_destination(st, None, 0)
            require(sha(read_fd(fd, 0)) == EMPTY_SHA, 'destination not empty')
            expected = (st.st_dev, st.st_ino)
            verify_held_path(parent, p.name, fd, expected, 0)
            return expected
        finally:
            os.close(fd)

def authority_bundle():
    loaded = {}
    for name, expected in PINS.items():
        data = read_path(DOMAIN / name)
        require(sha(data) == expected, 'authority raw pin mismatch: ' + name)
        if name.endswith('.json'):
            loaded[name] = decode_json(data)
    subject = loaded['profile-installation-recovery-subject.json']
    grant = loaded['issued-profile-installation-recovery-grant.json']
    effect = loaded['profile-recovery-effectiveness-reference.json']
    supplement = loaded['profile-recovery-custody-supplement-subject.json']
    adoption = loaded['profile-recovery-custody-adoption-record.json']
    custody = loaded['profile-recovery-custody-effectiveness-reference.json']
    initial = loaded['profile-recovery-custodian-declaration-reconciliation.json']
    for v in (subject, supplement):
        verify_identity(v, 'CONTENT')
    verify_identity(grant, field='GRANT_IDENTITY')
    for v in (effect, adoption, custody, initial):
        verify_identity(v)
    require(subject['IDENTITY']['sha256'] == SUBJECT_SHA, 'wrong subject')
    require(grant['GRANT_IDENTITY']['sha256'] == GRANT_SHA and
            grant['RECORD']['APPROVED_CONTENT'] == subject['CONTENT'], 'wrong grant/scope')
    require(effect['RECORD']['GRANT_IDENTITY'] == grant['GRANT_IDENTITY'] and
            effect['RECORD']['STATUS'] == 'EFFECTIVE_RECOVERY_ONLY_SUBJECT_TO_FRESH_ENTRY', 'grant ineffective')
    require(custody['RECORD']['STATUS'] == 'EFFECTIVE_RECOVERY_CUSTODY_BINDING_ONLY' and
            custody['RECORD']['ADOPTION_IDENTITY'] == adoption['IDENTITY'], 'custody ineffective')
    bindings = custody['RECORD']['OPERATIVE_BINDINGS']
    require(bindings == supplement['CONTENT']['OPERATIVE_BINDINGS'], 'custody bindings changed')
    require(bindings['ATTEMPT_STATE_CUSTODIAN'] == 'KGE-FORGE-PROJECT-OWNER' and
            bindings['AUTHORITATIVE_RECORD_DOMAIN'] == str(DOMAIN) and
            bindings['PERMANENT_CONSUMPTION_RECORD'] == str(CONSUMPTION), 'wrong state store')
    attempt = grant['RECORD']['SINGLE_ATTEMPT_IDENTITY']
    require(attempt['sha256'] == ATTEMPT_KEY and initial['RECORD']['ATTEMPT_IDENTITY'] == attempt,
            'wrong attempt')
    require(initial['RECORD']['INITIAL_ATTEMPT_STATE'] == 'UNUSED' and
            initial['RECORD']['GRANT_IDENTITY'] == grant['GRANT_IDENTITY'] and
            initial['RECORD']['CUSTODY_SUPPLEMENT_EFFECTIVENESS_IDENTITY'] == custody['IDENTITY'],
            'initial state not reconciled unused')
    allocation = subject['CONTENT']['FINITE_SCOPE']
    require(allocation['RECOVERY_ATTEMPTS'] == 1 and allocation['AUTOMATIC_RETRIES'] == 0 and
            allocation['MAX_SUCCESSFUL_CONTENT_BYTES'] == SIZE, 'wrong recovery limits')
    require(loaded['profile-recovery-operator-handoff.json']['EXACT_PROCEDURE_VERBATIM'] ==
            subject['CONTENT']['PROCEDURE'], 'handoff changed')
    for name in ('profile-recovery-effectiveness-four-seed.json', 'profile-recovery-custody-effectiveness-four-seed.json'):
        check = loaded[name]
        require(check['RESULT'] == 'PASS' and len(check['RESULTS']) == 4 and
                len({x['semantic_sha256'] for x in check['RESULTS']}) == 1, 'effectiveness verification missing')
    return loaded

def check_dispositions(allow_consumed=False):
    with directory_fd(DOMAIN) as domain:
        try:
            os.stat(CONSUMPTION.name, dir_fd=domain, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            require(allow_consumed, 'attempt occupied/consumed: never retry')
        for name in os.listdir(domain):
            if not name.endswith('.json') or (allow_consumed and name == CONSUMPTION.name):
                continue
            value = decode_json(read_path(DOMAIN / name))
            body = value.get('RECORD', value.get('CONTENT', value)) if isinstance(value, dict) else {}
            if not isinstance(body, dict):
                continue
            text = canonical(body).decode('ascii')
            if not any(key in text for key in (ATTEMPT_KEY, GRANT_SHA, SUBJECT_SHA)):
                continue
            classifications = [body.get(k, '') for k in
                               ('STATE', 'EVENT_TYPE', 'STATUS', 'DISPOSITION',
                                'RECORD_TYPE', 'ISSUANCE_RECORD_TYPE')]
            require(not any(isinstance(v, str) and
                            ('REVOC' in v.upper() or 'REVOK' in v.upper() or
                             'SUPERSE' in v.upper() or v in
                             ('CONSUMED_BEFORE_WRITE', 'CONSUMED', 'UNKNOWN', 'FAILED',
                              'RECOVERY_ATTEMPT_UNKNOWN_OUTCOME', 'RECOVERY_ATTEMPT_FAILED'))
                            for v in classifications),
                    'conflicting authority/use event: ' + name)
            if isinstance(value, dict) and 'GRANT_IDENTITY' in value and 'RECORD' in value:
                require(value['GRANT_IDENTITY']['sha256'] == GRANT_SHA,
                        'conflicting grant for this recovery: ' + name)
            if body.get('RECORD_TYPE') == 'RECOVERY_INITIAL_STATE_DECLARATION_RECONCILIATION':
                require(body.get('INITIAL_ATTEMPT_STATE') == 'UNUSED',
                        'contradictory current initial-state receipt: ' + name)
            require(not any(v is True for k, v in body.items() if
                            k.startswith('RECOVERY_ATTEMPT_CONSUMED') or k == 'HOST_RECOVERY_EXECUTED'),
                    'reported prior use: ' + name)

# Separate fresh Python process; no import of this writer, no writable open.
INDEPENDENT_READER = r'''
import hashlib,json,os,stat,sys
path,expected_raw,expected_canonical=sys.argv[1:]
parts=path.split('/')
fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC)
try:
 for part in parts[1:-1]:
  nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=fd)
  os.close(fd);fd=nxt
 f=os.open(parts[-1],os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=fd)
 try:
  st=os.fstat(f)
  assert stat.S_ISREG(st.st_mode) and st.st_nlink==1
  assert st.st_uid==1000 and st.st_gid==1000 and stat.S_IMODE(st.st_mode)==0o600
  with os.fdopen(f,'rb',closefd=False) as stream:data=stream.read(8193)
  assert len(data)<=8192 and hashlib.sha256(data).hexdigest()==expected_raw
  named=os.stat(parts[-1],dir_fd=fd,follow_symlinks=False)
  assert (named.st_dev,named.st_ino)==(st.st_dev,st.st_ino)
 finally:os.close(f)
finally:os.close(fd)
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')
def unique(items):
 d={}
 for k,v in items:
  assert k not in d;d[k]=v
 return d
v=json.loads(data.decode('ascii'),object_pairs_hook=unique);r=v['RECORD']
cid=hashlib.sha256(canon(r)).hexdigest()
assert cid==expected_canonical==v['IDENTITY']['sha256']
assert v['IDENTITY']['kind']=='CONTENT_IDENTITY'
assert v['IDENTITY']['namespace']=='kge-forge-profile-recovery-consumption-record-v1'
assert r['RECORD_TYPE']=='RECOVERY_ATTEMPT_CONSUMPTION' and r['STATE']=='CONSUMED_BEFORE_WRITE'
assert r['ATTEMPT_IDENTITY']['sha256']=='48f7ff401d5bfec3a300f79f2bab28eece53e0243865994d54fc2ae58c8c1e1f'
assert r['GRANT_IDENTITY']['sha256']=='47e5b27349c076eea1a232f7e0ea5380bcf496f12fd1f4cc49bf6b389adb22a8'
assert r['SOURCE_SHA256']=='b694333f4c108c8fea455f7e117cda1d003f3c915bb36d78ae7ec466022b47f8'
assert r['SOURCE_BYTES']==r['MAX_SUCCESSFUL_CONTENT_BYTES']==1091
assert r['RECOVERY_ATTEMPTS']==1 and r['AUTOMATIC_RETRIES']==0
assert r['OPERATION_IDENTITY']['sha256']==hashlib.sha256(canon(r['OPERATION'])).hexdigest()
print(cid)
'''

def independent_consumption_reader(envelope, serialized):
    require(sha(read_path(PYTHON)) == PYTHON_SHA, 'reader executable changed')
    require(len(serialized) <= 8192, 'record exceeds reader bound')
    result = subprocess.run([PYTHON, '-I', '-B', '-c', INDEPENDENT_READER, str(CONSUMPTION),
                             sha(serialized), envelope['IDENTITY']['sha256']],
                            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            close_fds=True, env={'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'LANG': 'C'}, timeout=10)
    require(result.returncode == 0 and result.stdout.strip() == envelope['IDENTITY']['sha256'].encode('ascii'),
            'independent consumption verification failed: UNKNOWN, no write')

def durable_consume_and_independently_verify(attempt_key, device, inode, *, held_fd):
    require(attempt_key == ATTEMPT_KEY, 'wrong attempt key')
    require((device, inode) == EXPECTED_RECEIPT, 'wrong approved receipt binding')
    require(os.geteuid() == EXPECTED_UID and os.getegid() == EXPECTED_GID,
            'consumption operator identity mismatch')
    mode = fcntl.fcntl(held_fd, fcntl.F_GETFL)
    require(mode & os.O_ACCMODE == os.O_RDWR and not mode & os.O_APPEND,
            'destination descriptor must be the held non-append read/write descriptor')
    fcntl.flock(held_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    with directory_fd(pathlib.Path(DEST).parent) as parent:
        verify_held_path(parent, pathlib.Path(DEST).name, held_fd, (device, inode), 0)
    require(os.pread(held_fd, 1, 0) == b'', 'held destination not empty')
    read_source()
    bundle = authority_bundle()
    check_dispositions()
    grant = bundle['issued-profile-installation-recovery-grant.json']
    custody = bundle['profile-recovery-custody-effectiveness-reference.json']
    initial = bundle['profile-recovery-custodian-declaration-reconciliation.json']
    utility = str(pathlib.Path(__file__).absolute())
    operation = {'UTILITY_PATH': utility, 'UTILITY_SHA256': sha(read_path(utility)),
                 'ARGV': list(sys.argv), 'PYTHON_ISOLATED': sys.flags.isolated,
                 'EXECUTABLE': PYTHON, 'EXECUTABLE_SHA256': PYTHON_SHA, 'SOURCE_PATH': SOURCE,
                 'SOURCE_SHA256': SOURCE_SHA, 'SOURCE_BYTES': SIZE, 'DESTINATION_PATH': DEST,
                 'DESTINATION_DEVICE': device, 'DESTINATION_INODE': inode, 'ATTEMPT_KEY': ATTEMPT_KEY,
                 'MECHANISM': 'HELD_NOFOLLOW_DESCRIPTOR_INPLACE_WRITE_NO_CREATE_NO_TRUNCATE'}
    record = {'RECORD_TYPE': 'RECOVERY_ATTEMPT_CONSUMPTION', 'STATE': 'CONSUMED_BEFORE_WRITE',
              'CUSTODIAN_ROLE': 'KGE-FORGE-PROJECT-OWNER', 'ATTEMPT_IDENTITY': grant['RECORD']['SINGLE_ATTEMPT_IDENTITY'],
              'GRANT_IDENTITY': grant['GRANT_IDENTITY'], 'CUSTODY_EFFECTIVENESS_IDENTITY': custody['IDENTITY'],
              'INITIAL_STATE_IDENTITY': initial['IDENTITY'], 'SOURCE_SHA256': SOURCE_SHA, 'SOURCE_BYTES': SIZE,
              'DESTINATION_PATH': DEST, 'DESTINATION_DEVICE': device, 'DESTINATION_INODE': inode,
              'OPERATION': operation, 'OPERATION_IDENTITY': identity('kge-forge-profile-recovery-operation-v1', operation),
              'RECOVERY_ATTEMPTS': 1, 'AUTOMATIC_RETRIES': 0, 'MAX_SUCCESSFUL_CONTENT_BYTES': SIZE,
              'FAILURE_RULE': 'PERMANENTLY_CONSUMED_ON_FAILURE_CRASH_OR_UNKNOWN; NO_RETRY'}
    envelope = {'RECORD': record, 'IDENTITY': identity(RECORD_NAMESPACE, record)}
    serialized = (json.dumps(envelope, indent=2, sort_keys=True, ensure_ascii=True) + '\n').encode()
    require(len(serialized) <= 8192, 'record exceeds reader bound')
    source = read_path(PUBLISHER)
    require(sha(source) == PUBLISHER_SHA, 'qualified publisher changed')
    node = next(n for n in ast.parse(source.decode()).body if isinstance(n, ast.FunctionDef) and n.name == 'publish')
    namespace = {'D': DOMAIN, 'os': os, 'json': json, 'tempfile': tempfile}
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(PUBLISHER), 'exec'), namespace)
    with directory_fd(DOMAIN) as parent:
        held = os.fstat(parent)
        def unchanged():
            named = os.stat(DOMAIN, follow_symlinks=False)
            require((held.st_dev, held.st_ino) == (named.st_dev, named.st_ino), 'record domain changed')
        unchanged()
        # Reuse exactly the qualified publication function, not its old issuer.
        namespace['publish'](CONSUMPTION.name, envelope)
        unchanged()
        independent_consumption_reader(envelope, serialized)
    check_dispositions(allow_consumed=True)
    require(read_path(CONSUMPTION, 8192) == serialized,
            'consumption record changed after independent verification: UNKNOWN, no write')
    return envelope['IDENTITY']

def write_authenticated(fd, data, write=os.write):
    require(len(data) == SIZE and sha(data) == SOURCE_SHA, 'unauthenticated buffer')
    offset = 0
    while offset < SIZE:
        sent = write(fd, data[offset:])
        require(isinstance(sent, int) and 0 < sent <= SIZE - offset, 'zero/invalid write result: stop')
        offset += sent  # Only the unwritten suffix; no restart/replay.

def recover_transaction(data, path, expected, consume):
    """Core transaction. Synthetic tests supply disposable path/mock adapter.
    Real CLI exposes no source/destination/store override.
    """
    require(len(data) == SIZE and sha(data) == SOURCE_SHA, 'source not authenticated')
    p = pathlib.Path(path)
    with directory_fd(p.parent) as parent:
        fd = os.open(p.name, os.O_RDWR | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK, dir_fd=parent)
        try:
            validate_destination(os.fstat(fd), expected, 0)
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            verify_held_path(parent, p.name, fd, expected, 0)
            require(sha(read_fd(fd, 0)) == EMPTY_SHA, 'destination not empty')
            consumed = consume(ATTEMPT_KEY, expected[0], expected[1], held_fd=fd)
            require(consumed is not None, 'no verified consumption result')
            verify_held_path(parent, p.name, fd, expected, 0)
            os.lseek(fd, 0, os.SEEK_SET)
            write_authenticated(fd, data)
            os.fsync(fd)
            verify_held_path(parent, p.name, fd, expected, SIZE)
            reader = os.open(p.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK, dir_fd=parent)
            try:
                validate_destination(os.fstat(reader), expected, SIZE)
                installed = read_fd(reader, SIZE)
                require(len(installed) == SIZE and sha(installed) == SOURCE_SHA, 'post-write mismatch: no retry')
                verify_held_path(parent, p.name, reader, expected, SIZE)
            finally:
                os.close(reader)
            return consumed
        finally:
            os.close(fd)  # Never delete/restore attempt or partial artifact.

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--preflight', action='store_true', help='read-only snapshot')
    mode.add_argument('--execute', action='store_true', help='irreversible real recovery')
    parser.add_argument('--expected-device', type=int)
    parser.add_argument('--expected-inode', type=int)
    parser.add_argument('--confirm-exclusive-operator', action='store_true')
    args = parser.parse_args()
    require(os.getuid() == os.geteuid() == EXPECTED_UID and os.getgid() == os.getegid() == EXPECTED_GID,
            'operator identity mismatch')
    require(not any(name in os.environ for name in ('LD_PRELOAD', 'LD_LIBRARY_PATH', 'BASH_ENV')),
            'unsafe startup context')
    require(sha(read_path(PYTHON)) == PYTHON_SHA and pathlib.Path(sys.executable).resolve() == pathlib.Path(PYTHON),
            'use exact pinned Python3.8')
    require(sys.flags.isolated and sys.dont_write_bytecode, 'invoke with Python -I -B')
    authority_bundle()
    check_dispositions()
    data = read_source()
    if args.preflight:
        dev, ino = inspect_destination()
        print('PREFLIGHT_SNAPSHOT_PASS device={} inode={} (not launch authorization)'.format(dev, ino))
        return
    require(args.expected_device is not None and args.expected_inode is not None and
            args.expected_device >= 0 and args.expected_inode > 0, 'execute needs receipt device/inode')
    require((args.expected_device, args.expected_inode) == EXPECTED_RECEIPT,
            'receipt differs from nominated failed artifact; stop for adjudication')
    require(args.confirm_exclusive_operator, 'operator must exclude concurrent writers')
    consumed = recover_transaction(data, DEST, (args.expected_device, args.expected_inode),
                                   durable_consume_and_independently_verify)
    print('RECOVERY_INSTALLED_VERIFIED attempt={} consumption={} (no activation)'.format(
        ATTEMPT_KEY, consumed['sha256']))

if __name__ == '__main__':
    try:
        main()
    except (Stop, OSError, ValueError, KeyError, subprocess.SubprocessError, AssertionError,
            KeyboardInterrupt) as exc:
        print('STOP_OR_UNKNOWN: {}; never retry --execute; reconcile permanent attempt record'.format(exc), file=sys.stderr)
        sys.exit(2)
