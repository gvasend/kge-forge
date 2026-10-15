"""Irreversible claim-before-launch gate; construction is not runtime qualification.

The entry binding is a gate-local normalized evidence contract, not a native
Planner record or a newly issued grant. An independently qualified controller
must supply its exact authority/profile pins. Unknown entry evidence denies use.
Synthetic mode accepts only synthetic authority and an inert callback; the CLI
cannot enter synthetic mode. Recovery never returns launch permission.
"""
import argparse
import fcntl
import hashlib
import json
import os
import pathlib
import re
import selectors
import signal
import socket
import stat
import subprocess
import time

SUBJECT_SHA = '762b88071476cea67c08c8e57d5b893f61c2d8843cc7f0f04a07f05b52fe3a80'
SUBJECT_RAW = '8c6a1e64c932b03a8c24fee823d0b84ae7178fca708db2986308e4610a35bf8f'
CHARTER_SHA = 'd26962c58f17281173e965433dae63a941e078115f3dcc30e2a3512fa21812b8'
ISSUER = 'KGE-FORGE-PROJECT-OWNER-QUALIFICATION-GOVERNING-AUTHORITY'
SCHEMA = 'H77-02-ENTRY-BINDING-1'
KEY_SCHEMA = 'H77-02-CONSUMPTION-KEY-1'
MAX_RECORD = 262144
# No actual H77-02 authority-reader/profile has been qualified or issued.
# A future reviewed binding is required; construction cannot self-seal it.
QUALIFIED_REAL_AUTHORITY_BINDING = None
EXACT_COMMAND_SHA = '8c6ebe1406c74e740e1ed9150e62e49a1aeb0466b2aaaa01b9b977a9dfb49a6b'
REAL_LIMITS = {'MAX_ACTUAL_PROCESS_SLOTS': 4, 'MAX_PAYLOAD_LAUNCHES': 1,
               'CHILD_WALL': 60, 'CHILD_CPU': 30, 'CHILD_AS': 1073741824,
               'CHILD_FSIZE': 16777216, 'CHILD_FDS': 64,
               'TOTAL_WRITES': 1048576, 'TOTAL_WALL': 600, 'RETRIES': 0}
ENTRY_CHECKS = ('authority_reader_qualified', 'epoch_serialization_qualified',
                'authority_freshness_verified', 'filesystem_persistence_verified',
                'single_store_verified', 'permissions_verified',
                'resource_controls_verified', 'confinement_verified',
                'executable_dependencies_verified', 'no_prior_consumption_verified')
ENTRY_KEYS = {'schema', 'mode', 'grant_pin', 'effective_pin', 'subject_pin',
              'profile_pin', 'store_path', 'epoch_name', 'epoch_identity',
              'command', 'resource_limits', 'execution_context', 'entry_checks',
              'authorized_attempt_number'}


class GateError(Exception):
    pass


class LaunchFailed(GateError):
    """The OS rejected process creation; no created child is inferred."""
    pass


def require(condition, reason):
    if not condition:
        raise GateError(reason)


def canonical(value):
    # No float/timestamp coercion or identity-bearing unordered/default fields.
    def valid(x):
        if isinstance(x, dict):
            require(all(isinstance(k, str) for k in x), 'NON_STRING_KEY')
            for v in x.values():
                valid(v)
        elif isinstance(x, list):
            for v in x:
                valid(v)
        else:
            require(x is None or type(x) in (str, int, bool), 'UNSUPPORTED_JSON_VALUE')
    valid(value)
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False, allow_nan=False).encode('utf-8')


def identity(value, namespace):
    return {'kind': 'CONTENT_IDENTITY', 'namespace': namespace,
            'sha256': hashlib.sha256(canonical(value)).hexdigest()}


def check_identity(value):
    require(isinstance(value, dict) and set(value) == {'kind', 'namespace', 'sha256'},
            'IDENTITY_FIELDS')
    require(value['kind'] == 'CONTENT_IDENTITY' and isinstance(value['namespace'], str)
            and re.fullmatch('[a-zA-Z0-9_-]+', value['namespace'])
            and isinstance(value['sha256'], str)
            and re.fullmatch('[0-9a-f]{64}', value['sha256']), 'IDENTITY_DOMAIN')


def decode(raw):
    def pairs(items):
        out = {}
        for k, v in items:
            require(k not in out, 'DUPLICATE_JSON_KEY')
            out[k] = v
        return out
    value = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs)
    canonical(value)
    return value


def open_directory(path):
    """Walk absolute components by descriptors; never follow a path symlink."""
    path = pathlib.Path(path)
    require(path.is_absolute() and '..' not in path.parts and str(path) != '/',
            'STORE_PATH')
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parts[1:]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                            dir_fd=fd)
            os.close(fd)
            fd = child
        info = os.fstat(fd)
        require(info.st_uid == os.geteuid() and stat.S_IMODE(info.st_mode) == 0o700,
                'STORE_OWNER_OR_MODE')
        return fd
    except BaseException:
        os.close(fd)
        raise


def read_at(directory, name):
    require('/' not in name and name not in ('', '.', '..'), 'RECORD_NAME')
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory)
    try:
        info = os.fstat(fd)
        require(stat.S_ISREG(info.st_mode) and info.st_uid == os.geteuid()
                and not info.st_mode & 0o022 and info.st_nlink == 1
                and info.st_size <= MAX_RECORD, 'UNTRUSTED_RECORD')
        with os.fdopen(os.dup(fd), 'rb') as stream:
            raw = stream.read(MAX_RECORD + 1)
        require(len(raw) <= MAX_RECORD, 'RECORD_TOO_LARGE')
        return raw, info
    finally:
        os.close(fd)


def read_pin(pin):
    require(isinstance(pin, dict) and set(pin) == {'path', 'sha256'}, 'PIN_FIELDS')
    path = pathlib.Path(pin['path'])
    directory = open_directory(path.parent)
    try:
        raw, unused = read_at(directory, path.name)
    finally:
        os.close(directory)
    require(hashlib.sha256(raw).hexdigest() == pin['sha256'], 'PIN_MISMATCH')
    return decode(raw)


def validate_authority(entry, epoch, synthetic=False):
    """Require exact pinned issued/effective records and independently sealed profile.

    Private normalized records here are schema-strict. No assertion in this
    function issues authority; real schemas/reader and actual host evidence must
    be independently qualified before entry_checks can legitimately be true.
    """
    require(isinstance(entry, dict) and set(entry) == ENTRY_KEYS, 'ENTRY_FIELDS')
    require(synthetic or QUALIFIED_REAL_AUTHORITY_BINDING is not None,
            'REAL_AUTHORITY_READER_AND_PROFILE_NOT_QUALIFIED')
    require(entry['schema'] == SCHEMA and entry['mode'] ==
            ('SYNTHETIC' if synthetic else 'REAL'), 'ENTRY_MODE')
    require(type(entry['authorized_attempt_number']) is int and
            entry['authorized_attempt_number'] == 1, 'ATTEMPT_NUMBER')
    require(set(entry['entry_checks']) == set(ENTRY_CHECKS) and
            all(entry['entry_checks'][k] is True for k in ENTRY_CHECKS), 'ENTRY_UNVERIFIED')
    grant = read_pin(entry['grant_pin'])
    require(set(grant) == {'identity', 'content'}, 'ISSUED_GRANT_FIELDS')
    check_identity(grant['identity'])
    require(identity(grant['content'], grant['identity']['namespace']) == grant['identity'],
            'GRANT_IDENTITY')
    g = grant['content']
    require(set(g) == {'schema', 'status', 'subject_identity', 'probe_identity',
                      'command_identity', 'context_identity', 'issuer_role',
                      'charter_identity', 'resource_limits', 'single_probe_limit',
                      'automatic_retries', 'store_path', 'epoch_name'}, 'GRANT_FIELDS')
    require(g['schema'] == 'H77-02-NORMALIZED-ISSUED-AUTHORITY-1' and
            g['status'] == 'ISSUED' and g['issuer_role'] == ISSUER, 'ISSUER_OR_STATUS')
    require(g['single_probe_limit'] == 1 and type(g['single_probe_limit']) is int
            and g['automatic_retries'] == 0 and type(g['automatic_retries']) is int,
            'ONE_USE_SCOPE')
    require(isinstance(entry['resource_limits'], dict) and
            all(type(v) is int for v in entry['resource_limits'].values()),
            'RESOURCE_VALUE_TYPES')
    subject = read_pin(entry['subject_pin'])
    require(set(subject) == {'IDENTITY', 'CONTENT', 'APPROVAL', 'ISSUED'}, 'SUBJECT_FIELDS')
    require(identity(subject['CONTENT'], subject['IDENTITY']['namespace']) ==
            subject['IDENTITY'] == g['subject_identity'], 'SUBJECT_IDENTITY')
    command_id = identity(entry['command'], 'qualification-h77-02-command-contract-v1')
    context_id = entry['execution_context']['profile_identity']
    check_identity(context_id)
    require(set(entry['execution_context']) == {'profile_identity', 'host', 'mode'},
            'CONTEXT_FIELDS')
    require(command_id == g['command_identity'] and context_id == g['context_identity'],
            'COMMAND_OR_CONTEXT')
    require(g['store_path'] == entry['store_path'] and g['epoch_name'] == entry['epoch_name'],
            'STORE_SUBSTITUTION')
    effective = read_pin(entry['effective_pin'])
    require(set(effective) == {'schema', 'grant_identity', 'subject_identity', 'effective'}
            and effective['schema'] == 'H77-02-NORMALIZED-EFFECTIVE-AUTHORITY-1'
            and effective['effective'] is True and effective['grant_identity'] == grant['identity']
            and effective['subject_identity'] == subject['IDENTITY'], 'GRANT_NOT_EFFECTIVE')
    require(set(epoch) == {'schema', 'grant_identity', 'epoch', 'status',
                          'expiration_checked', 'freshness_verified'}
            and epoch['schema'] == 'H77-02-AUTHORITY-EPOCH-1'
            and epoch['grant_identity'] == grant['identity'] and epoch['status'] == 'EFFECTIVE'
            and type(epoch['epoch']) is int and epoch['epoch'] > 0
            and epoch['expiration_checked'] is True and epoch['freshness_verified'] is True
            and identity(epoch, 'qualification-h77-02-authority-epoch-v1') ==
            entry['epoch_identity'], 'REVOKED_EXPIRED_OR_UNKNOWN_EPOCH')
    profile = read_pin(entry['profile_pin'])
    require(identity(profile, context_id['namespace']) == context_id, 'PROFILE_IDENTITY')
    require(set(profile) == {'schema', 'mode', 'host', 'store_path', 'store_device',
                            'store_inode', 'resource_limits', 'entry_checks',
                            'launch_working_directory'} and
            profile['schema'] == 'H77-02-QUALIFIED-ENTRY-PROFILE-1'
            and profile['mode'] == entry['mode'] and profile['host'] ==
            entry['execution_context']['host'] and profile['store_path'] == entry['store_path'],
            'PROFILE_SCOPE')
    require(profile['entry_checks'] == entry['entry_checks'] and
            profile['resource_limits'] == entry['resource_limits'] == g['resource_limits'],
            'RESOURCE_OR_PROFILE_MISMATCH')
    if synthetic:
        require(grant['identity']['namespace'].startswith('qualification-h77-02-gate-synthetic-')
                and subject['IDENTITY']['namespace'].startswith('qualification-h77-02-gate-synthetic-')
                and context_id['namespace'].startswith('qualification-h77-02-gate-synthetic-')
                and entry['execution_context']['mode'] == 'SYNTHETIC'
                and entry['command'] == {'operation': 'INERT_CALLBACK', 'argv': []},
                'REAL_INPUT_IN_SYNTHETIC_MODE')
        require(entry['resource_limits'] == REAL_LIMITS, 'SYNTHETIC_RESOURCE_MISMATCH')
    else:
        require(QUALIFIED_REAL_AUTHORITY_BINDING is not None,
                'REAL_AUTHORITY_READER_AND_PROFILE_NOT_QUALIFIED')
        # A construction/test grant cannot pass this probe-authority boundary.
        require(grant['identity']['namespace'].startswith('qualification-h77-02-probe-')
                and subject['IDENTITY']['sha256'] == SUBJECT_SHA
                and subject['IDENTITY']['namespace'] ==
                'qualification-a15-host-capability-test-subject-v1'
                and entry['subject_pin']['sha256'] == SUBJECT_RAW, 'NOT_H77_PROBE_GRANT')
        b = subject['CONTENT']
        require(g['charter_identity']['sha256'] == CHARTER_SHA and
                g['charter_identity'] == b['GOVERNING_CHARTER_IDENTITY'], 'CHARTER')
        require(entry['command'] == b['PROCEDURE']['COMMAND_OR_TEST'] and
                g['probe_identity'] == b['PROCEDURE']['PROGRAM']['CONTENT_IDENTITY'] and
                entry['resource_limits'] == REAL_LIMITS and
                entry['execution_context']['mode'] == 'DIRECT_HOST_NOT_CODEX'
                and socket.gethostname() == 'ubuntu01' and os.geteuid() == 1000
                and os.uname().release == '5.4.0-216-generic', 'DIRECT_HOST_ENTRY')
        status = pathlib.Path('/proc/self/status').read_text()
        require(re.search(r'^Seccomp:\s+0$', status, re.M) and
                re.search(r'^NoNewPrivs:\s+0$', status, re.M) and
                re.search(r'^CapEff:\s+0+$', status, re.M), 'OUTER_RESTRICTIONS')
        for pin in b['PROCEDURE']['TOOL_BINARY_PINS']:
            require(hashlib.sha256(pathlib.Path(pin['PATH']).read_bytes()).hexdigest()
                    == pin['RAW_SHA256'], 'EXECUTABLE_PIN')
        require(pathlib.Path('/usr/bin/python3').resolve() == pathlib.Path('/usr/bin/python3.8'),
                'INTERPRETER_SUBSTITUTION')
        require(isinstance(profile['launch_working_directory'], str) and
                re.fullmatch('/tmp/kge-a15-harness-test-[0-9a-f]{32}',
                             profile['launch_working_directory']), 'PRIVATE_LAUNCH_CWD')
    return grant['identity'], subject['IDENTITY'], g['probe_identity'], command_id, profile


def consumption_key(grant_id, subject_id, probe_id, command_id, context):
    for item in (grant_id, subject_id, probe_id, command_id):
        check_identity(item)
    require(set(context) == {'profile_identity', 'host', 'mode'}, 'CONTEXT_KEY_FIELDS')
    check_identity(context['profile_identity'])
    fields = {'schema': KEY_SCHEMA, 'issued_grant_identity': grant_id,
              'approved_subject_identity': subject_id, 'probe_identity': probe_id,
              'command_identity': command_id, 'execution_context': context,
              'authorized_attempt_number': 1}
    return fields, identity(fields, 'qualification-h77-02-consumption-key-v1')


def verify_consumption_record(directory, name, fields, expected_inode):
    """Separate readonly reconstruction; no claim, launch capability or repair."""
    raw, info = read_at(directory, name)
    body = {'schema': 'H77-02-CONSUMPTION-RECORD-1', 'key': fields, 'state': 'CONSUMED'}
    expected = {'content': body, 'identity': identity(body, 'qualification-h77-02-consumption-record-v1')}
    require(info.st_ino == expected_inode and raw == canonical(expected)
            and decode(raw) == expected, 'CONSUMPTION_VERIFICATION_FAILED')
    return expected['identity']


def _write_all(fd, raw):
    offset = 0
    while offset < len(raw):
        written = os.write(fd, raw[offset:])
        require(written > 0, 'SHORT_WRITE')
        offset += written


def _exclusive_record(directory, name, value, fault_hook=None, reservation_observer=None):
    raw = canonical(value)
    require(len(raw) <= MAX_RECORD, 'RECORD_BUDGET')
    # This reservation is never removed, even on write/fsync/verification failure.
    fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                 0o600, dir_fd=directory)
    try:
        inode = os.fstat(fd).st_ino
        if reservation_observer:
            reservation_observer()
        if fault_hook:
            fault_hook('DURING_CLAIM')
        _write_all(fd, raw)
        os.fsync(fd)
        if fault_hook:
            fault_hook('AFTER_FILE_FSYNC')
    finally:
        os.close(fd)
    os.fsync(directory)
    if fault_hook:
        fault_hook('AFTER_DIRECTORY_FSYNC')
    return inode


def _audit(directory, key_id, phase, outcome):
    value = {'schema': 'H77-02-GATE-AUDIT-1', 'key_identity': key_id,
             'phase': phase, 'outcome': outcome}
    return _exclusive_record(directory, key_id['sha256'] + '.' + phase + '.json', value)


def _fixed_real_launch(command, observe_launch, qualified_working_directory):
    """Only called after exact subject validation and durable irreversible claim."""
    require(set(command) == {'ARGV', 'CWD', 'ENVIRONMENT'}, 'COMMAND_FIELDS')
    require(QUALIFIED_REAL_AUTHORITY_BINDING is not None and
            hashlib.sha256(canonical(command)).hexdigest() == EXACT_COMMAND_SHA,
            'UNQUALIFIED_OR_SUBSTITUTED_REAL_LAUNCH')
    # Subject's descriptive private-/tmp parent CWD is bound by the independently
    # qualified context, not substituted with an arbitrary runtime directory.
    require(re.fullmatch('/tmp/kge-a15-harness-test-[0-9a-f]{32}',
                         qualified_working_directory), 'PRIVATE_LAUNCH_CWD')
    cwdfd = open_directory(qualified_working_directory)
    try:
        require(cwdfd < REAL_LIMITS['CHILD_FDS'], 'CWD_DESCRIPTOR_LIMIT')
        checked = open_directory(qualified_working_directory)
        try:
            require((os.fstat(checked).st_dev, os.fstat(checked).st_ino) ==
                    (os.fstat(cwdfd).st_dev, os.fstat(cwdfd).st_ino), 'LAUNCH_CWD_REPLACED')
        finally:
            os.close(checked)
        # No host-directory descriptor is inherited into the confined payload.
        # Actual profile qualification must also establish trusted serialized
        # ownership of the parent CWD through process creation.
        process = subprocess.Popen(command['ARGV'], cwd=qualified_working_directory,
                                   close_fds=True, env=command['ENVIRONMENT'],
                                   stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, start_new_session=True)
    except OSError as exc:
        raise LaunchFailed('OS_PROCESS_CREATION_FAILED') from exc
    finally:
        os.close(cwdfd)
    selector = selectors.DefaultSelector()
    buffers = {'stdout': bytearray(), 'stderr': bytearray()}
    started = time.monotonic()
    try:
        observe_launch({'state': 'LAUNCHED', 'process_created': True, 'pid': process.pid})
        for name, stream in [('stdout', process.stdout), ('stderr', process.stderr)]:
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ, name)
        while selector.get_map():
            require(time.monotonic() - started < REAL_LIMITS['CHILD_WALL'], 'CHILD_TIMEOUT')
            for event, unused in selector.select(timeout=0.1):
                chunk = os.read(event.fileobj.fileno(), 4096)
                if not chunk:
                    selector.unregister(event.fileobj)
                else:
                    buffers[event.data].extend(chunk)
                    require(sum(len(x) for x in buffers.values()) <= 131072, 'OUTPUT_BUDGET')
        code = process.wait(timeout=max(0.01, 60 - (time.monotonic() - started)))
        return {'process_created': True, 'exit_code': code,
                'stdout': bytes(buffers['stdout']).decode('utf-8'),
                'stderr': bytes(buffers['stderr']).decode('utf-8')}
    finally:
        selector.close()
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=5)
        process.stdout.close()
        process.stderr.close()


def claim_and_launch(entry, *, synthetic_callback=None, stage_hook=None):
    """Consume irrevocably in this call; never return a reusable launch token.

    Hooks/callbacks are synthetic-only fault injection. No recovery can resume
    this call's launch eligibility. The effective authority epoch's protected
    stable inode is the administrative lock; owner updates must use that same
    serialized protocol and its qualification is an explicit entry predicate.
    """
    entry = decode(canonical(entry))  # Freeze caller mutation before validation.
    synthetic = entry.get('mode') == 'SYNTHETIC'
    require(synthetic or QUALIFIED_REAL_AUTHORITY_BINDING is not None,
            'REAL_AUTHORITY_READER_AND_PROFILE_NOT_QUALIFIED')
    require(synthetic or (synthetic_callback is None and stage_hook is None), 'REAL_INJECTION')
    require(not synthetic or callable(synthetic_callback), 'INERT_CALLBACK_REQUIRED')
    directory = open_directory(entry['store_path'])
    epochfd = None
    claimed = False
    key_id = None
    def hook(stage):
        if synthetic and stage_hook:
            stage_hook(stage)
    def reserved():
        nonlocal claimed
        claimed = True  # Reservation/ambiguity, NOT durable launch permission.
    try:
        epoch_name = entry['epoch_name']
        require('/' not in epoch_name and epoch_name not in ('', '.', '..'), 'EPOCH_NAME')
        epochfd = os.open(epoch_name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory)
        fcntl.flock(epochfd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        raw, info = read_at(directory, epoch_name)
        require(info.st_ino == os.fstat(epochfd).st_ino, 'EPOCH_REPLACED')
        epoch = decode(raw)
        grant_id, subject_id, probe_id, command_id, profile = validate_authority(entry, epoch, synthetic)
        storeinfo = os.fstat(directory)
        require((storeinfo.st_dev, storeinfo.st_ino) ==
                (profile['store_device'], profile['store_inode']), 'STORE_INSTANCE')
        fields, key_id = consumption_key(grant_id, subject_id, probe_id, command_id,
                                         entry['execution_context'])
        name = key_id['sha256'] + '.claim.json'
        hook('BEFORE_CLAIM')
        body = {'schema': 'H77-02-CONSUMPTION-RECORD-1', 'key': fields, 'state': 'CONSUMED'}
        value = {'content': body, 'identity': identity(body, 'qualification-h77-02-consumption-record-v1')}
        # Reservation occurs inside _exclusive_record; any failure may leave a
        # blocking incomplete token. Never catch FileExistsError as success.
        inode = _exclusive_record(directory, name, value, hook if synthetic else None,
                                  reservation_observer=reserved)
        hook('AFTER_CLAIM_BEFORE_LAUNCH')
        consumption_id = verify_consumption_record(directory, name, fields, inode)
        fresh, now_info = read_at(directory, epoch_name)
        require(now_info.st_ino == os.fstat(epochfd).st_ino and fresh == raw,
                'AUTHORITY_CHANGED')
        checkdir = open_directory(entry['store_path'])
        try:
            require(os.fstat(checkdir).st_ino == storeinfo.st_ino and
                    os.fstat(checkdir).st_dev == storeinfo.st_dev, 'STORE_REPLACED')
        finally:
            os.close(checkdir)
        # A second independent authority read closes changed pin/invocation paths.
        validate_authority(entry, epoch, synthetic)
        _audit(directory, key_id, 'consumed', {'state': 'CONSUMED', 'identity': consumption_id})
        _audit(directory, key_id, 'attempt', {'state': 'LAUNCH_ATTEMPT', 'synthetic': synthetic})
        hook('DURING_LAUNCH')
        # No exported token, loop, retry, or restart-capable permission exists.
        outcome = synthetic_callback() if synthetic else _fixed_real_launch(
            entry['command'], lambda event: _audit(directory, key_id, 'launched', event),
            profile['launch_working_directory'])
        canonical(outcome)
        hook('AFTER_LAUNCH_BEFORE_OBSERVATION')
        hook('AFTER_COMPLETION_BEFORE_AUDIT')
        _audit(directory, key_id, 'observed', {'state': 'COMPLETED' if synthetic or
               outcome['exit_code'] == 0 else 'FAILED', 'synthetic': synthetic, 'result': outcome})
        return {'key_identity': key_id, 'consumption_identity': consumption_id,
                'consumed': True, 'synthetic': synthetic, 'result': outcome, 'retry_allowed': False}
    except BaseException as exc:
        # Even if creation/write failed before claimed=True, an existing or
        # partial file blocks every later call through exclusive creation.
        if claimed and key_id is not None:
            try:
                _audit(directory, key_id, 'unknown', {'state': 'LAUNCH_FAILED' if
                       isinstance(exc, LaunchFailed) else 'OUTCOME_UNKNOWN',
                       'error_type': type(exc).__name__, 'retry_allowed': False})
            except BaseException:
                pass  # Preserve original error; no deletion or reopening.
        raise
    finally:
        if epochfd is not None:
            os.close(epochfd)
        os.close(directory)


def recover(store_path, key_sha):
    """Readonly; an incomplete/conflicting token is ambiguous, never unused."""
    require(re.fullmatch('[0-9a-f]{64}', key_sha), 'KEY_SHA')
    directory = open_directory(store_path)
    try:
        try:
            raw, info = read_at(directory, key_sha + '.claim.json')
            record = decode(raw)
            require(identity(record['content'], 'qualification-h77-02-consumption-record-v1')
                    == record['identity'] and record['content']['state'] == 'CONSUMED'
                    and identity(record['content']['key'], 'qualification-h77-02-consumption-key-v1')['sha256']
                    == key_sha, 'RECOVERY_RECORD')
            return {'state': 'CONSUMED', 'launch_permitted': False, 'retry_allowed': False}
        except (OSError, ValueError, KeyError, GateError):
            return {'state': 'OUTCOME_UNKNOWN', 'launch_permitted': False, 'retry_allowed': False}
    finally:
        os.close(directory)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', required=True, choices=['claim-and-launch', 'recover'])
    parser.add_argument('--manifest', required=True)
    args = parser.parse_args()
    # CLI pins the manifest through its protected owner-only directory. It is
    # not a synthetic test launcher or a path to bypass real authority validation.
    path = pathlib.Path(args.manifest)
    fd = open_directory(path.parent)
    try:
        raw, unused = read_at(fd, path.name)
    finally:
        os.close(fd)
    entry = decode(raw)
    require(entry.get('mode') == 'REAL', 'CLI_SYNTHETIC_DENIED')
    if args.mode == 'recover':
        require(set(entry) == {'mode', 'store_path', 'key_sha'}, 'RECOVERY_MANIFEST')
        result = recover(entry['store_path'], entry['key_sha'])
    else:
        result = claim_and_launch(entry)
    print(canonical(result).decode('utf-8'))


if __name__ == '__main__':
    main()
