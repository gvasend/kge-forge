"""Synthetic gate qualification cases; not executed during Package81.

Every active suite entry requires an independently sealed campaign/environment
manifest. The assertions test gate semantics; fixture entry-check booleans are
synthetic protocol data, never proof of actual host permissions or durability.
"""
import copy
import hashlib
import json
import multiprocessing
import signal
import subprocess
import selectors
import resource
import os
import pathlib
import fcntl
import stat
import sys
import time
import unittest
from unittest import mock

from adapter.qualification_h77_02_gate import gate

ROOT = pathlib.Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / 'docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1'
GRANT80_SHA = 'e6728a8ecea41ce083e722326270885469d229e335a61c5ddc30d54b37cbd738'
SUBJECT79_SHA = '9c6ccc426dc2acb4126d85006ea6fb6f830b8c21bbfbfcdf8003058e146c9354'
SOURCE_PATHS = ['adapter/qualification_h77_02_gate/__init__.py',
                'adapter/qualification_h77_02_gate/gate.py',
                'adapter/tests/test_h77_02_launch_gate.py']

# Independent observer operations deliberately retain original OS functions.
# Injecting gate.os.fsync must not disable the observer's own durable witness.
_HOST_OPEN, _HOST_WRITE, _HOST_FSYNC = os.open, os.write, os.fsync
_HOST_FLOCK = fcntl.flock
_RUNTIME = None


class HarnessError(RuntimeError):
    pass


def _canon(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False, allow_nan=False).encode('utf-8')


def _id(value, namespace):
    return {'kind': 'CONTENT_IDENTITY', 'namespace': namespace,
            'sha256': hashlib.sha256(_canon(value)).hexdigest()}


def _under(root, path):
    root, path = pathlib.Path(root), pathlib.Path(path)
    if not root.is_absolute() or not path.is_absolute() or root not in path.parents:
        raise HarnessError('OUTSIDE_CAMPAIGN_ROOT')
    if path.resolve() != path:
        raise HarnessError('SYMLINK_OR_PATH_ESCAPE')
    return path


def _error(exc):
    return {'type': type(exc).__name__, 'message': str(exc),
            'errno': getattr(exc, 'errno', None)}


def _durable_exclusive(path, value):
    raw = _canon(value)
    if len(raw) > 262144:
        raise HarnessError('WITNESS_FILE_LIMIT')
    fd = _HOST_OPEN(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        offset = 0
        while offset < len(raw):
            n = _HOST_WRITE(fd, raw[offset:])
            if n <= 0: raise HarnessError('SHORT_WITNESS_WRITE')
            offset += n
        _HOST_FSYNC(fd)
    finally:
        os.close(fd)
    directory = _HOST_OPEN(str(path.parent), os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try: _HOST_FSYNC(directory)
    finally: os.close(directory)
    if path.read_bytes() != raw: raise HarnessError('WITNESS_REREAD_MISMATCH')
    return {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest()}


def _expected_fixture(root, descriptor):
    """Independent rule calculation; never uses producer/gate results or hashes."""
    root = pathlib.Path(root); store, auth = root / 'store', root / 'authority'
    checks = {k: True for k in (
        'authority_reader_qualified', 'epoch_serialization_qualified',
        'authority_freshness_verified', 'filesystem_persistence_verified',
        'single_store_verified', 'permissions_verified', 'resource_controls_verified',
        'confinement_verified', 'executable_dependencies_verified', 'no_prior_consumption_verified')}
    # True flags are disposable synthetic protocol data, not host capabilities.
    per_claim_limits = {'MAX_ACTUAL_PROCESS_SLOTS': 4, 'MAX_PAYLOAD_LAUNCHES': 1,
        'CHILD_WALL': 60, 'CHILD_CPU': 30, 'CHILD_AS': 1073741824,
        'CHILD_FSIZE': 16777216, 'CHILD_FDS': 64, 'TOTAL_WRITES': 1048576,
        'TOTAL_WALL': 600, 'RETRIES': 0}
    content = {'purpose': 'DISPOSABLE_INERT_GATE_SYNTHETIC_ONLY', 'fixture_descriptor': descriptor}
    subject = {'CONTENT': content, 'IDENTITY': _id(content,
               'qualification-h77-02-gate-synthetic-subject-v1'), 'APPROVAL': None, 'ISSUED': False}
    info = store.stat()
    profile = {'schema': 'H77-02-QUALIFIED-ENTRY-PROFILE-1', 'mode': 'SYNTHETIC',
        'host': 'SYNTHETIC_DISPOSABLE_HOST', 'store_path': str(store),
        'store_device': info.st_dev, 'store_inode': info.st_ino,
        'launch_working_directory': str(root), 'resource_limits': per_claim_limits,
        'entry_checks': checks}
    profile_id = _id(profile, 'qualification-h77-02-gate-synthetic-profile-v1')
    command = {'operation': 'INERT_CALLBACK', 'argv': []}
    command_id = _id(command, 'qualification-h77-02-command-contract-v1')
    body = {'schema': 'H77-02-NORMALIZED-ISSUED-AUTHORITY-1', 'status': 'ISSUED',
        'subject_identity': subject['IDENTITY'], 'probe_identity': _id(
            {'operation': 'INERT', 'fixture_descriptor': descriptor},
            'qualification-h77-02-gate-synthetic-probe-v1'),
        'command_identity': command_id, 'context_identity': profile_id,
        'issuer_role': 'KGE-FORGE-PROJECT-OWNER-QUALIFICATION-GOVERNING-AUTHORITY',
        'charter_identity': _id({'synthetic': True}, 'qualification-h77-02-gate-synthetic-charter-v1'),
        'resource_limits': per_claim_limits, 'single_probe_limit': 1,
        'automatic_retries': 0, 'store_path': str(store), 'epoch_name': 'epoch.json'}
    grant = {'content': body, 'identity': _id(body, 'qualification-h77-02-gate-synthetic-grant-v1')}
    effective = {'schema': 'H77-02-NORMALIZED-EFFECTIVE-AUTHORITY-1',
        'grant_identity': grant['identity'], 'subject_identity': subject['IDENTITY'], 'effective': True}
    epoch = {'schema': 'H77-02-AUTHORITY-EPOCH-1', 'grant_identity': grant['identity'],
        'epoch': 1, 'status': 'EFFECTIVE', 'expiration_checked': True, 'freshness_verified': True}
    docs = {'subject.json': subject, 'profile.json': profile, 'grant.json': grant,
            'effective.json': effective, 'epoch.json': epoch}
    def dp(name):
        directory = store if name == 'epoch.json' else auth
        return {'path': str(directory / name), 'sha256': hashlib.sha256(_canon(docs[name])).hexdigest()}
    context = {'profile_identity': profile_id, 'host': 'SYNTHETIC_DISPOSABLE_HOST', 'mode': 'SYNTHETIC'}
    entry = {'schema': 'H77-02-ENTRY-BINDING-1', 'mode': 'SYNTHETIC',
        'grant_pin': dp('grant.json'), 'effective_pin': dp('effective.json'),
        'subject_pin': dp('subject.json'), 'profile_pin': dp('profile.json'),
        'store_path': str(store), 'epoch_name': 'epoch.json',
        'epoch_identity': _id(epoch, 'qualification-h77-02-authority-epoch-v1'),
        'command': command, 'resource_limits': per_claim_limits, 'execution_context': context,
        'entry_checks': checks, 'authorized_attempt_number': 1}
    key = {'schema': 'H77-02-CONSUMPTION-KEY-1', 'issued_grant_identity': grant['identity'],
        'approved_subject_identity': subject['IDENTITY'], 'probe_identity': body['probe_identity'],
        'command_identity': command_id, 'execution_context': context, 'authorized_attempt_number': 1}
    claim = {'schema': 'H77-02-CONSUMPTION-RECORD-1', 'key': key, 'state': 'CONSUMED'}
    record = {'content': claim, 'identity': _id(claim, 'qualification-h77-02-consumption-record-v1')}
    return {'descriptor': descriptor, 'entry': entry, 'documents': docs, 'key': key,
        'key_identity': _id(key, 'qualification-h77-02-consumption-key-v1'),
        'claim_record': record, 'fixture_identity': _id({'descriptor': descriptor,
        'documents': docs, 'entry': entry}, 'qualification-h77-02-gate-synthetic-fixture-v1'),
        'test_directory_identity': _id(descriptor, 'qualification-h77-02-gate-synthetic-directory-v1')}


class HarnessRuntime:
    """In-file binding/witness/accounting controller, not OS qualification proof."""
    def __init__(self, entry):
        if entry['binding_phase'] != 'RUN': raise HarnessError('INSTANCE_NOT_SEALED')
        self.entry = entry
        self.root = pathlib.Path(entry['campaign_root']['path'])
        root = entry['campaign_root']; info = self.root.stat()
        if (self.root.resolve() != self.root or stat.S_IMODE(info.st_mode) != 0o700
                or info.st_uid != root['owner'] or root['owner'] != os.geteuid()
                or root['identity'] != _id(root['content'], 'qualification-h77-02-synthetic-campaign-root-v1')
                or str(self.root) != '/tmp/kge-h77-02-gate-synthetic-' + root['identity']['sha256'][:32]):
            raise HarnessError('WRONG_CAMPAIGN_ROOT')
        self.catalog = gate.read_pin(entry['fixture_manifest_pin'])
        self.oracles = gate.read_pin(entry['independent_oracle_pin'])
        if (self.catalog.get('schema') != 'H77-02-SEALED-FIXTURE-CATALOG-83-1'
                or self.catalog.get('root_identity') != root['identity']
                or self.catalog.get('campaign_identity') != entry['campaign_identity']
                or self.oracles.get('schema') != 'H77-02-INDEPENDENT-ORACLES-84-1'):
            raise HarnessError('MANIFEST_IDENTITY_OR_SCOPE')
        oracle_body = dict(self.oracles); oracle_identity = oracle_body.pop('identity')
        if oracle_identity != _id(oracle_body, 'qualification-h77-02-executable-oracles-v1') or self.oracles['status'] != 'COMPLETE_STATIC_PARAMETERIZED':
            raise HarnessError('UNSEALED_EXECUTABLE_ORACLE')
        self.rows = {}
        for rowpin in self.catalog['rows']:
            row = gate.read_pin(rowpin)
            path = _under(self.root, row['root'])
            expected = _expected_fixture(path, row['fixture']['descriptor'])
            if expected != row['fixture']: raise HarnessError('FIXTURE_IDENTITY_MISMATCH')
            if expected['fixture_identity']['sha256'] in self.rows:
                raise HarnessError('CROSS_TEST_FIXTURE_COLLISION')
            self.rows[expected['fixture_identity']['sha256']] = row
        descriptors = {(r['fixture']['descriptor']['seed'], r['fixture']['descriptor']['method'], r['fixture']['descriptor']['variant']) for r in self.rows.values()}
        required = {(seed, method, variant) for seed in (0, 1, 7, 101) for method in self.oracles['tests'] for variant in self.oracles['tests'][method]['variants']}
        if descriptors != required or len(self.rows) != len(required):
            raise HarnessError('INCOMPLETE_OR_DUPLICATE_FIXTURE_CATALOG')
        self.ledger = self.root / 'controller-budget.jsonl'
        self.seed = int(os.environ.get('PYTHONHASHSEED', '-1'))
        if self.seed not in (0, 1, 7, 101): raise HarnessError('UNSEALED_SEED')
        self.current_method = os.environ.get('KGE_H77_CURRENT_CASE')
        self._observer_failures = []
        self._tracker_pid = None
        self._tracker_observation = None
        self._operations = {}
        self._children = {}
        self._first_failure = None
        self._secondary_errors = []

    def row(self, root):
        root = _under(self.root, root)
        matches = [r for r in self.rows.values() if r['root'] == str(root)]
        if len(matches) != 1: raise HarnessError('UNASSIGNED_TEST_DIRECTORY')
        descriptor = matches[0]['fixture']['descriptor']
        if descriptor['seed'] != self.seed or (self.current_method is not None and
                descriptor['method'] != self.current_method):
            raise HarnessError('SIBLING_TEST_ACCESS')
        return matches[0]

    def case_root(self, method):
        if method not in self.oracles['tests']: raise HarnessError('UNAPPROVED_TEST_SELECTION')
        return _under(self.root, self.root / 'cases' / ('seed%d' % self.seed) / method)

    def begin_case(self, method):
        self.current_method = method
        self._operations = {}
        os.environ['KGE_H77_CURRENT_CASE'] = method
        self.account('case', 0, method)
        self.case_root(method)  # May only use a controller-prepared child.

    def account(self, kind, amount=0, role='parent'):
        fd = _HOST_OPEN(str(self.ledger), os.O_RDWR | os.O_NOFOLLOW)
        try:
            _HOST_FLOCK(fd, fcntl.LOCK_EX)
            with os.fdopen(os.dup(fd), 'r+b') as stream:
                rows = [json.loads(line) for line in stream.read().splitlines()]
                if not rows or rows[0]['campaign_identity'] != self.entry['campaign_identity']:
                    raise HarnessError('CAMPAIGN_LEDGER_BINDING')
                limits = self.entry['resource_limits']
                header = rows[0]
                if (header['failure_evidence_reserve'] != 2097152 or header['charged_bytes'] != 2097152 + len(_canon(header) + b'\n') or header['deadline_ns'] - header['started_ns'] != limits['TOTAL_WALL'] * 1000000000):
                    raise HarnessError('UNSEALED_CAMPAIGN_ACCOUNTING_HEADER')
                if kind not in ('stop', 'release', 'failure') and (any(r['kind'] == 'stop' for r in rows) or time.monotonic_ns() > rows[0]['deadline_ns']):
                    raise HarnessError('CAMPAIGN_STOPPED_OR_TIMEOUT')
                if kind not in ('reserve', 'release', 'bytes', 'case', 'stop', 'failure') or type(amount) is not int or amount < 0:
                    raise HarnessError('INVALID_ACCOUNTING_EVENT')
                launches = sum(r.get('amount', 0) for r in rows if r['kind'] == 'reserve')
                live = launches - sum(r.get('amount', 0) for r in rows if r['kind'] == 'release')
                written = sum(r.get('charged_bytes', 0) for r in rows)
                if (kind == 'reserve' and (launches + amount > limits['MAX_PAYLOAD_LAUNCHES']
                    or live + amount > limits['MAX_ACTUAL_PROCESS_SLOTS'])):
                    raise HarnessError('CAMPAIGN_PROCESS_LIMIT')
                if kind == 'release' and (amount != 1 or sum(r.get('amount', 0) for r in rows if r['kind'] == 'reserve' and r['role'] == role) <= sum(r.get('amount', 0) for r in rows if r['kind'] == 'release' and r['role'] == role)):
                    raise HarnessError('UNRESERVED_PROCESS_RELEASE')
                if kind == 'bytes' and written + amount > limits['TOTAL_WRITES']:
                    raise HarnessError('CAMPAIGN_OUTPUT_LIMIT')
                event = {'kind': kind, 'amount': amount, 'role': role, 'charged_bytes': 0}
                raw = _canon(event) + b'\n'
                # Include ledger bytes, not only final file sizes. No recursive
                # accounting call; exact fixed-point charge is sealed per append.
                for unused in range(8):
                    event['charged_bytes'] = (amount if kind == 'bytes' else 0) + len(raw)
                    updated = _canon(event) + b'\n'
                    if updated == raw: break
                    raw = updated
                else: raise HarnessError('ACCOUNTING_FIXED_POINT_FAILURE')
                if written + event['charged_bytes'] > limits['TOTAL_WRITES']:
                    raise HarnessError('CAMPAIGN_OUTPUT_LIMIT')
                stream.seek(0, os.SEEK_END); stream.write(raw); stream.flush(); _HOST_FSYNC(stream.fileno())
        finally: os.close(fd)

    def reserve_child(self, role, root):
        self.row_for_case(root)
        # multiprocessing's tracker is another actual child, not free capacity.
        # A qualified external process profile must account for tracker/launcher
        # roles too. The source controller refuses to assume that capability.
        if self.entry['entry_predicates']['resource_limits_enforceable'] is not True:
            raise HarnessError('PROCESS_PROFILE_UNQUALIFIED')
        from multiprocessing import resource_tracker
        tracker = resource_tracker._resource_tracker
        if self._tracker_pid is None:
            if tracker._pid is not None:
                raise HarnessError('UNACCOUNTED_EXISTING_TRACKER')
            self.account('reserve', 1, 'multiprocessing-resource-tracker')
            tracker.ensure_running()
            if tracker._pid is None: raise HarnessError('TRACKER_LAUNCH_UNOBSERVED')
            self._tracker_pid = tracker._pid
            self.event(self.case_root(self.current_method), 'supervisor', 'tracker.created',
                       {'pid': self._tracker_pid})
        elif tracker._pid != self._tracker_pid:
            raise HarnessError('TRACKER_IDENTITY_CHANGED')
        self.account('reserve', 1, role)

    def row_for_case(self, root):
        path = _under(self.root, root)
        if self.current_method and self.case_root(self.current_method) != path:
            raise HarnessError('SIBLING_TEST_ACCESS')
        return path

    def process_created(self, role, pid):
        self.event(self.case_root(self.current_method), 'supervisor', 'process.created',
                   {'role': role, 'pid': pid})

    def process_exited(self, role, pid, code):
        self.event(self.case_root(self.current_method), 'supervisor', 'process.observed_exit',
                   {'role': role, 'pid': pid, 'exit_code': code})
        self.account('release', 1, role)

    def stop_after_unexpected_failure(self, original):
        # Latch before any fallible publication, accounting or cleanup.
        detail = _error(original)
        if self._first_failure is None:
            self._first_failure = detail
        elif detail != self._first_failure:
            self._secondary_errors.append(detail)
        try:
            self.failure_evidence(self.root / 'first-counterexample.json', {
                'schema': 'H77-02-FIRST-COUNTEREXAMPLE-84-1',
                'campaign_identity': self.entry['campaign_identity'],
                'first': self._first_failure, 'retry_allowed': False})
        except FileExistsError:
            try:
                prior = json.loads((self.root / 'first-counterexample.json').read_text())
                if prior['campaign_identity'] != self.entry['campaign_identity']:
                    raise HarnessError('FIRST_FAILURE_BINDING_CONFLICT')
                if prior['first'] != self._first_failure:
                    self._secondary_errors.append(self._first_failure)
                    self._first_failure = prior['first']
            except BaseException as secondary:
                # A partial/conflicting record is retained, never repaired or
                # substituted. It cannot replace the original causal failure.
                self._secondary_errors.append(_error(secondary))
        except BaseException as secondary:
            self._secondary_errors.append(_error(secondary))

        try: self.account('stop', 0, 'controller')
        except BaseException as secondary: self._secondary_errors.append(_error(secondary))

    def failure_evidence(self, path, value):
        _under(self.root, path)
        # Fixed closed set of emergency files, conservatively prepaid from the
        # campaign ceiling. No unbounded append or post-stop test work.
        permitted = {'first-counterexample.json', 'campaign-controller.result.json'} | {'controller-seed%d.result.json' % seed for seed in (0, 1, 7, 101)}
        if pathlib.Path(path).parent != self.root or pathlib.Path(path).name not in permitted:
            raise HarnessError('UNAUTHORIZED_FAILURE_EVIDENCE')
        return _durable_exclusive(path, value)

    def start_child(self, process, role, root):
        self.reserve_child(role, root)
        try:
            process.start()
            self._children[role] = process
            self.process_created(role, process.pid)
        except BaseException as original:
            self.stop_after_unexpected_failure(original)
            # Ambiguous creation retains its reserved slot. No compensating retry.
            raise

    def wait_child(self, process, role, expected_codes=(0,)):
        first = None
        try:
            process.join(timeout=min(10, self.entry['resource_limits']['CHILD_WALL']))
            if process.is_alive():
                first = HarnessError('OWNED_CHILD_TIMEOUT:' + role)
                self.stop_after_unexpected_failure(first)
                process.terminate(); process.join(timeout=2)
                if process.is_alive(): process.kill(); process.join(timeout=2)
            if process.is_alive(): raise HarnessError('CHILD_TERMINATION_UNOBSERVED:' + role)
            self.process_exited(role, process.pid, process.exitcode)
            self._children.pop(role, None)
            if first is not None: raise first
            if process.exitcode not in expected_codes:
                raise HarnessError('UNEXPECTED_CHILD_EXIT:' + role + ':' + str(process.exitcode))
            return process.exitcode
        except BaseException as original:
            self.stop_after_unexpected_failure(original)
            raise

    def close_children(self):
        for role, process in list(self._children.items()):
            try:
                if process.is_alive(): process.terminate()
                self.wait_child(process, role, expected_codes=())
            except BaseException as secondary:
                self.stop_after_unexpected_failure(secondary)

    def close_tracker(self):
        if self._tracker_pid is None: return
        from multiprocessing import resource_tracker
        tracker = resource_tracker._resource_tracker
        if tracker._pid != self._tracker_pid: raise HarnessError('TRACKER_EXIT_IDENTITY')
        # Close the owned channel, then independently wait with a bounded deadline.
        # Private CPython fields are version-pinned entry requirements, never
        # assumed portable or qualified merely because this code is present.
        os.close(tracker._fd); tracker._fd = None
        deadline = time.monotonic() + 2
        pid = self._tracker_pid
        while True:
            observed, status = os.waitpid(pid, os.WNOHANG)
            if observed == pid: break
            if time.monotonic() >= deadline:
                self.stop_after_unexpected_failure(HarnessError('TRACKER_TIMEOUT'))
                os.kill(pid, signal.SIGKILL)
                deadline = time.monotonic() + 2
                while True:
                    observed, status = os.waitpid(pid, os.WNOHANG)
                    if observed == pid: break
                    if time.monotonic() >= deadline: raise HarnessError('TRACKER_TERMINATION_UNOBSERVED')
                    time.sleep(0.01)
                break
            time.sleep(0.01)
        self._tracker_observation = {'pid': pid, 'wait_status': status, 'observed_by_parent': True}
        tracker._pid = None
        self.account('release', 1, 'multiprocessing-resource-tracker')
        self._tracker_pid = None
        if status != 0: raise HarnessError('TRACKER_NONZERO_EXIT:' + str(status))

    def begin_operation(self, root, actor):
        row = self.row(root); witness = pathlib.Path(root) / 'witness.jsonl'
        prior = [json.loads(line)['content'] for line in witness.read_text().splitlines()] if witness.exists() else []
        ordinal = 1 + sum(e['actor'] == actor and e['kind'] == 'claim.request' for e in prior)
        value = {'fixture_identity': row['fixture']['fixture_identity'], 'actor': actor, 'ordinal': ordinal}
        operation = _id(value, 'qualification-h77-02-synthetic-operation-v1')
        self._operations[actor] = operation
        return operation

    def event(self, root, actor, kind, value):
        row = self.row(root); path = _under(self.root, pathlib.Path(root) / 'witness.jsonl')
        fd = _HOST_OPEN(str(path), os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
        try:
            _HOST_FLOCK(fd, fcntl.LOCK_EX)
            with os.fdopen(os.dup(fd), 'r+b') as stream:
                prior = [json.loads(line) for line in stream.read().splitlines()]
                record = {'schema': 'H77-02-INDEPENDENT-WITNESS-84-1',
                    'fixture_identity': row['fixture']['fixture_identity'], 'actor': actor,
                    'sequence': len(prior), 'kind': kind, 'value': value,
                    'operation_identity': self._operations.get(actor),
                    'previous': prior[-1]['identity'] if prior else None}
                envelope = {'content': record, 'identity': _id(record,
                    'qualification-h77-02-gate-synthetic-witness-v1')}
                raw = _canon(envelope) + b'\n'
                self.account('bytes', len(raw), actor)
                stream.seek(0, os.SEEK_END); stream.write(raw); stream.flush(); _HOST_FSYNC(stream.fileno())
            directory = _HOST_OPEN(str(path.parent), os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            try: _HOST_FSYNC(directory)
            finally: os.close(directory)
        except BaseException as original:
            self.stop_after_unexpected_failure(original)
            raise
        finally: os.close(fd)

    def finish_case(self, method):
        # Independent executable model is loaded from its own immutable oracle
        # pin. Missing observations are a failure, never assumed success.
        specification = self.oracles['tests'][method]
        rows = [r for r in self.rows.values() if r['fixture']['descriptor']['method'] == method
                and r['fixture']['descriptor']['seed'] == self.seed]
        try:
            for row in rows:
                _compare_observations(self, row, specification)
            if self._observer_failures: raise HarnessError('WITNESS_PUBLICATION_UNCONFIRMED')
        except BaseException as original:
            self.stop_after_unexpected_failure(original)
            raise


def _runtime():
    global _RUNTIME
    if _RUNTIME is None: _RUNTIME = HarnessRuntime(require_test_entry())
    return _RUNTIME


def make_fixture(root):
    runtime = _runtime(); row = runtime.row(root); expected = row['fixture']
    # Every generated artifact is independently compared against sealed expected
    # bytes before any gate input is returned. No unverified runtime identity.
    for name, value in expected['documents'].items():
        path = pathlib.Path(root) / ('store' if name == 'epoch.json' else 'authority') / name
        if path.read_bytes() != _canon(value): raise HarnessError('FIXTURE_CONTENT_MISMATCH')
    return copy.deepcopy(expected['entry'])


def mutate_epoch_for_negative_case(path, value):
    runtime = _runtime(); root = pathlib.Path(path).parent.parent
    row = runtime.row(root)
    expected = copy.deepcopy(row['fixture']['documents']['epoch.json'])
    expected['status'] = 'REVOKED'
    if value != expected: raise HarnessError('UNSEALED_EPOCH_MUTATION')
    raw = _canon(value); runtime.account('bytes', len(raw), 'parent')
    fd = _HOST_OPEN(str(path), os.O_WRONLY | os.O_TRUNC | os.O_NOFOLLOW)
    try: _HOST_WRITE(fd, raw); _HOST_FSYNC(fd)
    finally: os.close(fd)


def fault_witness(entry, actor, point, cause):
    root = pathlib.Path(entry['grant_pin']['path']).parent.parent
    _runtime().event(root, actor, 'fault.injected', {'point': point, 'cause': cause})


def observed_claim(entry, *, synthetic_callback, stage_hook=None, actor='parent'):
    runtime = _runtime(); root = pathlib.Path(entry['grant_pin']['path']).parent.parent
    row = runtime.row(root)
    if entry.get('mode') != 'SYNTHETIC': raise HarnessError('REAL_INPUT_DENIED')
    if getattr(synthetic_callback, '__code__', None) is None or pathlib.Path(
            synthetic_callback.__code__.co_filename).resolve() != pathlib.Path(__file__).resolve():
        raise HarnessError('UNAPPROVED_CALLBACK_CODE')
    operation_id = runtime.begin_operation(root, actor)
    runtime.event(root, actor, 'claim.request', {'entry': entry})
    callback_id = _id({'fixture': row['fixture']['fixture_identity'], 'actor': actor,
                       'operation': operation_id}, 'qualification-h77-02-gate-synthetic-callback-v1')
    def callback():
        runtime.event(root, actor, 'callback.invoked', {'callback_identity': callback_id, 'arguments': []})
        try:
            value = synthetic_callback()
        except BaseException as exc:
            try:
                runtime.event(root, actor, 'callback.exception', {'callback_identity': callback_id, 'first': _error(exc)})
            except BaseException as secondary:
                runtime._observer_failures.append({'first': _error(exc), 'secondary': _error(secondary)})
            raise
        runtime.event(root, actor, 'callback.returned', {'callback_identity': callback_id, 'value': value})
        return value
    original_fsync = gate.os.fsync
    original_verify = gate.verify_consumption_record
    original_write = gate._write_all
    first = []
    def observe_failure(origin, exc):
        detail = {'origin': origin, 'exception': _error(exc)}
        if not first: first.append(detail)
        try:
            runtime.event(root, actor, 'fault.observed', {'first': first[0],
                          'observed': detail, 'secondary': detail != first[0]})
        except BaseException as secondary:
            runtime._observer_failures.append({'first': first[0], 'secondary': _error(secondary)})
            # Preserve the original exception, not an invented failed result.
    def fsync(fd):
        info = os.fstat(fd)
        target = 'directory' if stat.S_ISDIR(info.st_mode) else pathlib.Path(
            os.readlink('/proc/self/fd/%d' % fd)).name
        runtime.event(root, actor, 'barrier.request', {'target': target})
        try: value = original_fsync(fd)
        except BaseException as exc:
            observe_failure('fsync:' + target, exc); raise
        runtime.event(root, actor, 'barrier.confirmed', {'target': target})
        return value
    def verify_record(*args):
        runtime.event(root, actor, 'readonly-confirmation.request', {})
        try: value = original_verify(*args)
        except BaseException as exc:
            observe_failure('readonly-confirmation', exc); raise
        runtime.event(root, actor, 'readonly-confirmation.confirmed', {'identity': value})
        return value
    def write_all(fd, raw):
        try:
            runtime.account('bytes', len(raw), actor)
        except BaseException as original:
            runtime.stop_after_unexpected_failure(original)
            raise
        try: return original_write(fd, raw)
        except BaseException as exc:
            observe_failure('gate-write', exc); raise
    def hook(point):
        runtime.event(root, actor, 'stage', {'point': point})
        if stage_hook:
            try: stage_hook(point)
            except BaseException as exc:
                observe_failure('stage:' + point, exc); raise
    try:
        with mock.patch.object(gate.os, 'fsync', side_effect=fsync), mock.patch.object(
                gate, 'verify_consumption_record', side_effect=verify_record), mock.patch.object(
                gate, '_write_all', side_effect=write_all):
            result = gate.claim_and_launch(entry, synthetic_callback=callback, stage_hook=hook)
    except BaseException as exc:
        observe_failure('gate-exception', exc)
        try: runtime.event(root, actor, 'claim.failed', {'exception': _error(exc)})
        except BaseException as secondary:
            runtime._observer_failures.append({'first': _error(exc), 'secondary': _error(secondary)})
        raise
    runtime.event(root, actor, 'claim.returned', {'result': result})
    return result


def observed_recover(store, key_sha):
    runtime = _runtime(); root = pathlib.Path(store).parent; row = runtime.row(root)
    if key_sha != row['fixture']['key_identity']['sha256']: raise HarnessError('RECOVERY_KEY_MISMATCH')
    result = gate.recover(store, key_sha)
    runtime._operations.pop('parent', None)
    runtime.event(root, 'parent', 'recovery.observed', {'result': result, 'key_sha': key_sha})
    return result


def _bind_oracle(value, fixture, actor, ordinal):
    """Resolve only independently sealed input parameters, never observed output."""
    if isinstance(value, list): return [_bind_oracle(v, fixture, actor, ordinal) for v in value]
    if isinstance(value, dict): return {k: _bind_oracle(v, fixture, actor, ordinal) for k, v in value.items()}
    if not isinstance(value, str): return value
    operation = _id({'fixture_identity': fixture['fixture_identity'], 'actor': actor,
                     'ordinal': ordinal}, 'qualification-h77-02-synthetic-operation-v1')
    if value.startswith('$ENTRY:'):
        entry = copy.deepcopy(fixture['entry']); selector = value[7:]
        if selector == 'BAD_GRANT_PIN': entry['grant_pin']['sha256'] = '0' * 64
        elif selector == 'WRONG_COMMAND': entry['command']['argv'] = ['/bin/false']
        elif selector == 'CPU_MISMATCH': entry['resource_limits']['CHILD_CPU'] = 31
        elif selector == 'PERMISSION_UNKNOWN': entry['entry_checks']['permissions_verified'] = False
        elif selector == 'BAD_SUBJECT_PIN': entry['subject_pin']['sha256'] = '0' * 64
        elif selector == 'SYMLINK_STORE': entry['store_path'] = str(pathlib.Path(entry['store_path']).parent / 'store-link')
        elif selector != 'BASE': raise HarnessError('UNKNOWN_ORACLE_INPUT_SELECTOR')
        return entry
    if value == '$CALLBACK_ID': return _id({'fixture': fixture['fixture_identity'], 'actor': actor,
        'operation': operation}, 'qualification-h77-02-gate-synthetic-callback-v1')
    if value == '$CLAIM_ID': return fixture['claim_record']['identity']
    if value == '$CLAIM_RESULT': return {'key_identity': fixture['key_identity'],
        'consumption_identity': fixture['claim_record']['identity'], 'consumed': True,
        'synthetic': True, 'result': {'inert_callback_only': True}, 'retry_allowed': False}
    filename = fixture['key_identity']['sha256'] + '.claim.json'
    if value == '$ERROR:duplicate': return {'type': 'FileExistsError', 'errno': 17,
        'message': "[Errno 17] File exists: '" + filename + "'"}
    if value == '$ERROR:locked': return {'type': 'BlockingIOError', 'errno': 11,
        'message': '[Errno 11] Resource temporarily unavailable'}
    if value == '$ERROR:symlink':
        path = str(pathlib.Path(fixture['entry']['store_path']).parent / 'store-link')
        return {'$one_of': [{'type': 'NotADirectoryError', 'errno': 20,
            'message': "[Errno 20] Not a directory: '" + path + "'"},
            {'type': 'OSError', 'errno': 40,
            'message': "[Errno 40] Too many levels of symbolic links: '" + path + "'"}]}
    for phase in ('claim', 'consumed', 'attempt', 'observed', 'unknown'):
        value = value.replace('$FILE:' + phase, fixture['key_identity']['sha256'] + '.' + phase + '.json')
    if '$' in value: raise HarnessError('UNBOUND_ORACLE_PARAMETER')
    return value


def _matches_exact(expected, observed):
    if isinstance(expected, dict) and set(expected) == {'$one_of'}:
        return any(_matches_exact(candidate, observed) for candidate in expected['$one_of'])
    if type(expected) is not type(observed): return False
    if isinstance(expected, dict):
        return set(expected) == set(observed) and all(_matches_exact(expected[k], observed[k]) for k in expected)
    if isinstance(expected, list):
        return len(expected) == len(observed) and all(_matches_exact(a, b) for a, b in zip(expected, observed))
    return expected == observed


def _compare_operation_traces(row, content, specification):
    variant = row['fixture']['descriptor']['variant']
    model = specification['operation_comparisons'][variant]
    if model['schema'] != 'H77-02-OPERATION-COMPARISON-84-1' or model['retry_count'] != 0:
        raise HarnessError('INCOMPLETE_OPERATION_ORACLE')
    allowed = set(); winners = 0; matched_operations = {}
    for slot in model['slots']:
        actor, ordinal = slot['actor'], slot['ordinal']
        identity = _id({'fixture_identity': row['fixture']['fixture_identity'], 'actor': actor,
            'ordinal': ordinal}, 'qualification-h77-02-synthetic-operation-v1')
        allowed.add(identity['sha256'])
        events = [e for e in content if e['operation_identity'] == identity]
        if any(e['actor'] != actor for e in events): raise HarnessError('OPERATION_ACTOR_MISMATCH')
        observed = [{'kind': e['kind'], 'value': e['value']} for e in events]
        matched = [option for option in slot['alternatives'] if _matches_exact(
            _bind_oracle(option['events'], row['fixture'], actor, ordinal), observed)]
        if len(matched) != 1: raise HarnessError('EXACT_OPERATION_TRACE_MISMATCH:' + actor + ':' + str(ordinal))
        matched_operations[(actor, ordinal)] = _bind_oracle(matched[0]['events'], row['fixture'], actor, ordinal)
        winners += matched[0]['classification'] == 'success'
    if winners != model['successful_claims'] or winners > 1:
        raise HarnessError('CONCURRENT_WINNER_OR_CALLBACK_MISMATCH')
    if any(e['operation_identity'] is not None and e['operation_identity']['sha256'] not in allowed
           and e['kind'] != 'recovery.observed' for e in content):
        raise HarnessError('UNSEALED_OPERATION')
    permitted_outside = {'recovery.observed', 'process.created', 'process.observed_exit',
                         'tracker.created', 'key.observed'}
    if any(e['operation_identity'] is None and e['kind'] not in permitted_outside for e in content):
        raise HarnessError('UNBOUND_OBSERVATION')
    for event in content:
        if event['kind'] in ('process.created', 'process.observed_exit', 'tracker.created') and (event['actor'] != 'supervisor' or event['operation_identity'] is not None):
            raise HarnessError('PARENT_PROCESS_WITNESS_ROLE')
        if event['kind'] in ('key.observed', 'recovery.observed') and (event['actor'] != 'parent' or event['operation_identity'] is not None):
            raise HarnessError('INDEPENDENT_COMPARISON_WITNESS_ROLE')
    recoveries = [e['value'] for e in content if e['kind'] == 'recovery.observed']
    expected_recoveries = [{'result': result, 'key_sha': row['fixture']['key_identity']['sha256']}
                          for result in specification['variants'][variant]['recovery_constraints']]
    if recoveries != expected_recoveries: raise HarnessError('COMPLETE_RECOVERY_OBSERVATION_MISMATCH')
    tracker_events = [e['value'] for e in content if e['kind'] == 'tracker.created']
    if (len(tracker_events) != (1 if row['fixture']['descriptor']['method'] == 'test_concurrent_claimants_at_most_one' and variant == 'main' else 0) or any(set(v) != {'pid'} or type(v['pid']) is not int or v['pid'] <= 0 for v in tracker_events)):
        raise HarnessError('TRACKER_CREATION_COMPARISON_MISMATCH')
    created = [e['value'] for e in content if e['kind'] == 'process.created']
    exited = [e['value'] for e in content if e['kind'] == 'process.observed_exit']
    method = row['fixture']['descriptor']['method']
    roles = {'test_concurrent_claimants_at_most_one': ['result0', 'result1'],
             'test_process_restart_preserves_claim': ['first.json', 'restart.json'],
             'test_controlled_crash_points_remain_blocked': ['crash-result%d.json' % i for i in range(7)]}.get(method, []) if variant == 'main' else []
    if [v['role'] for v in created] != roles or [v['role'] for v in exited] != roles:
        raise HarnessError('INCOMPLETE_PARENT_PROCESS_LIFECYCLE')
    for a, b in zip(created, exited):
        if (set(a) != {'role', 'pid'} or set(b) != {'role', 'pid', 'exit_code'} or
                type(a['pid']) is not int or a['pid'] <= 0 or a['pid'] != b['pid'] or
                b['exit_code'] != (77 if method == 'test_controlled_crash_points_remain_blocked' else 0)):
            raise HarnessError('INDEPENDENT_EXIT_OBSERVATION_MISMATCH')
    result_names = {'test_concurrent_claimants_at_most_one': ['result0.json', 'result1.json'],
                    'test_process_restart_preserves_claim': ['first.json', 'restart.json']}.get(method, [])
    for filename in result_names:
        actor = pathlib.Path(filename).stem
        trace = matched_operations[(actor, 1)]
        final = trace[-1]
        if final['kind'] == 'claim.returned':
            expected_result = {'accepted': True, 'result': final['value']['result']}
        else:
            detail = final['value']['exception']
            expected_result = {'accepted': False, 'error_type': detail['type'],
                'error_message': detail['message'], 'errno': detail['errno']}
        if (pathlib.Path(row['root']) / filename).read_bytes() != _canon(expected_result):
            raise HarnessError('COMPLETE_CHILD_RESULT_MISMATCH')
    expected_store = {'epoch.json'} | {row['fixture']['key_identity']['sha256'] + '.' + phase + '.json'
        for phase, tag in specification['variants'][variant]['audit_constraints'].items() if tag is not None}
    if specification['variants'][variant]['claim_shape'] != 'ABSENT':
        expected_store.add(row['fixture']['key_identity']['sha256'] + '.claim.json')
    if {p.name for p in (pathlib.Path(row['root']) / 'store').iterdir()} != expected_store:
        raise HarnessError('UNEXPECTED_STORE_OUTPUT')
    if {p.name for p in (pathlib.Path(row['root']) / 'authority').iterdir()} != {'grant.json', 'subject.json', 'effective.json', 'profile.json'}:
        raise HarnessError('UNEXPECTED_AUTHORITY_OUTPUT')
    # Identity-bearing fields remain exact. PIDs are retained and linked to the
    # same parent's exit witness; concurrent winner identity is not predetermined.
    key_events = [e['value'] for e in content if e['kind'] == 'key.observed']
    expected_keys = [{'fields': row['fixture']['key'], 'identity': row['fixture']['key_identity'],
                     'reordered_identity': row['fixture']['key_identity']}] if method == 'test_key_is_independently_reconstructed_and_stable' else []
    if key_events != expected_keys: raise HarnessError('INDEPENDENT_KEY_COMPARISON')


def _compare_observations(runtime, row, specification):
    """Independent readonly comparator, never computes expectations from gate output."""
    root = pathlib.Path(row['root']); witness = root / 'witness.jsonl'
    events = [json.loads(line) for line in witness.read_text().splitlines()] if witness.exists() else []
    previous = None
    for sequence, envelope in enumerate(events):
        body = envelope['content']
        if set(envelope) != {'content', 'identity'} or set(body) != {'schema', 'fixture_identity', 'actor', 'sequence', 'kind', 'value', 'operation_identity', 'previous'} or body['schema'] != 'H77-02-INDEPENDENT-WITNESS-84-1':
            raise HarnessError('WITNESS_SCHEMA_OR_UNKNOWN_FIELD')
        if (body['sequence'] != sequence or body['previous'] != previous or
            envelope['identity'] != _id(body, 'qualification-h77-02-gate-synthetic-witness-v1') or
            body['fixture_identity'] != row['fixture']['fixture_identity']):
            raise HarnessError('WITNESS_BINDING_OR_ORDER')
        previous = envelope['identity']
    content = [e['content'] for e in events]
    _compare_operation_traces(row, content, specification)
    variant = row['fixture']['descriptor']['variant']
    model = copy.deepcopy(specification['variants'][variant])
    if model['schema'] != 'H77-02-EXECUTABLE-ORACLE-MODEL-83-1':
        raise HarnessError('ORACLE_SCHEMA')
    fixture = row['fixture']
    key = fixture['key_identity']
    audit_values = {
        'CONSUMED': {'schema': 'H77-02-GATE-AUDIT-1', 'key_identity': key, 'phase': 'consumed',
                     'outcome': {'state': 'CONSUMED', 'identity': fixture['claim_record']['identity']}},
        'ATTEMPT': {'schema': 'H77-02-GATE-AUDIT-1', 'key_identity': key, 'phase': 'attempt',
                    'outcome': {'state': 'LAUNCH_ATTEMPT', 'synthetic': True}},
        'OBSERVED': {'schema': 'H77-02-GATE-AUDIT-1', 'key_identity': key, 'phase': 'observed',
                     'outcome': {'state': 'COMPLETED', 'synthetic': True,
                                 'result': {'inert_callback_only': True}}},
        'UNKNOWN': {'schema': 'H77-02-GATE-AUDIT-1', 'key_identity': key, 'phase': 'unknown',
                    'outcome': {'state': 'OUTCOME_UNKNOWN', 'error_type': model['error_type'],
                                'retry_allowed': False}}}
    model['audit_constraints'] = {phase: (audit_values[tag] if tag else None)
                                  for phase, tag in model['audit_constraints'].items()}
    allowed_entries = []
    for selector in model['request_constraints']['variants']:
        candidate = copy.deepcopy(fixture['entry'])
        if selector == 'BAD_GRANT_PIN': candidate['grant_pin']['sha256'] = '0' * 64
        elif selector == 'WRONG_COMMAND': candidate['command']['argv'] = ['/bin/false']
        elif selector == 'CPU_MISMATCH': candidate['resource_limits']['CHILD_CPU'] = 31
        elif selector == 'PERMISSION_UNKNOWN': candidate['entry_checks']['permissions_verified'] = False
        elif selector == 'BAD_SUBJECT_PIN': candidate['subject_pin']['sha256'] = '0' * 64
        elif selector == 'SYMLINK_STORE': candidate['store_path'] = str(root / 'store-link')
        elif selector != 'BASE': raise HarnessError('UNSEALED_MUTATION_SELECTOR')
        allowed_entries.append(candidate)
    model['request_constraints']['allowed_entries'] = allowed_entries
    callbacks = [e for e in content if e['kind'] == 'callback.invoked']
    if len(callbacks) != model['callback_count']: raise HarnessError('CALLBACK_COUNT_MISMATCH')
    if any(e['value']['arguments'] != [] for e in callbacks): raise HarnessError('CALLBACK_ARGUMENTS')
    callback_returns = [e for e in content if e['kind'] == 'callback.returned']
    callback_errors = [e for e in content if e['kind'] == 'callback.exception']
    if len(callback_returns) != model['callback_returns'] or len(callback_errors) != len(model['callback_errors']):
        raise HarnessError('CALLBACK_OUTCOME_COUNT')
    if any(e['value']['value'] != {'inert_callback_only': True} for e in callback_returns):
        raise HarnessError('CALLBACK_RETURN_VALUE')
    if [e['value']['first'] for e in callback_errors] != model['callback_errors']:
        raise HarnessError('CALLBACK_EXCEPTION_CONTENT')
    claim_path = root / 'store' / (row['fixture']['key_identity']['sha256'] + '.claim.json')
    shape = model['claim_shape']
    if shape == 'ABSENT':
        if claim_path.exists(): raise HarnessError('UNEXPECTED_CONSUMPTION')
    elif shape == 'EMPTY':
        if claim_path.read_bytes() != b'': raise HarnessError('PARTIAL_CLAIM_SHAPE')
    elif claim_path.read_bytes() != _canon(row['fixture']['claim_record']):
        raise HarnessError('DURABLE_RECORD_IDENTITY')
    if any(e['kind'] == 'recovery.observed' and (e['value']['result']['launch_permitted'] is not False
            or e['value']['result']['retry_allowed'] is not False) for e in content):
        raise HarnessError('RECOVERY_REOPENS_AUTHORITY')
    returned = [e for e in content if e['kind'] == 'claim.returned']
    if len(returned) != model['successful_claims']: raise HarnessError('CLAIM_COUNT_MISMATCH')
    for e in returned:
        value = e['value']['result']
        expected = {'key_identity': row['fixture']['key_identity'],
                    'consumption_identity': row['fixture']['claim_record']['identity'],
                    'consumed': True, 'synthetic': True, 'result': {'inert_callback_only': True},
                    'retry_allowed': False}
        if value != expected: raise HarnessError('COMPLETE_CLAIM_OUTPUT_MISMATCH')
    for name, expected_document in fixture['documents'].items():
        expected_document = copy.deepcopy(expected_document)
        if name == 'epoch.json' and model['epoch_status'] is not None:
            expected_document['status'] = model['epoch_status']
        path = root / ('store' if name == 'epoch.json' else 'authority') / name
        if path.read_bytes() != _canon(expected_document): raise HarnessError('FIXTURE_MUTATION:' + name)
    # Missing audit/fault/barrier predicates are not waved away. The model must
    # supply explicit exact obligations; comparison readiness fails if absent.
    for name in ('fault_constraints', 'barrier_constraints', 'audit_constraints', 'request_constraints'):
        if name not in model: raise HarnessError('INCOMPLETE_EXECUTABLE_ORACLE:' + name)
    # Fault occurrence counts/content/order are exact in per-operation traces.
    for phase, expected_body in model['audit_constraints'].items():
        path = root / 'store' / (row['fixture']['key_identity']['sha256'] + '.' + phase + '.json')
        if expected_body is None:
            if path.exists(): raise HarnessError('UNEXPECTED_AUDIT:' + phase)
        else:
            # Parameterized exact bodies are resolved by the independent binder,
            # not substituted with an observed file as an oracle.
            if path.read_bytes() != _canon(expected_body): raise HarnessError('AUDIT_CONTENT:' + phase)
    barriers = [e for e in content if e['kind'] == 'barrier.confirmed']
    confirmed_files = sum(e['value']['target'] != 'directory' for e in barriers)
    confirmed_directories = len(barriers) - confirmed_files
    limits = model['barrier_constraints']
    if (confirmed_files != limits['file_confirmations'] or
            confirmed_directories != limits['directory_confirmations']):
        raise HarnessError('BARRIER_OBSERVATION_MISMATCH')
    requests = [e for e in content if e['kind'] == 'claim.request']
    if len(requests) != model['request_constraints']['count']:
        raise HarnessError('REQUEST_COUNT_MISMATCH')
    allowed = model['request_constraints']['allowed_entries']
    if any(e['value']['entry'] not in allowed for e in requests):
        raise HarnessError('UNSEALED_RUNTIME_INPUT')
    for actor in {e['actor'] for e in content}:
        kinds = [e['kind'] for e in content if e['actor'] == actor]
        if 'callback.returned' in kinds and kinds.index('callback.returned') < kinds.index('callback.invoked'):
            raise HarnessError('CALLBACK_ORDER_MISMATCH')
    if len(callbacks) > 1: raise HarnessError('DUPLICATE_CALLBACK')
    confirmations = [e for e in content if e['kind'] == 'readonly-confirmation.confirmed']
    if len(confirmations) != model['barrier_constraints']['readonly_confirmations']:
        raise HarnessError('READONLY_CONFIRMATION_COUNT')
    expected_key = row['fixture']['key_identity']['sha256']
    expected_file_events = model['barrier_constraints']['confirmed_file_phases']
    observed_file_events = [e['value']['target'] for e in barriers if e['value']['target'] != 'directory']
    if observed_file_events != [expected_key + '.' + phase + '.json' for phase in expected_file_events]:
        raise HarnessError('EXACT_FILE_BARRIER_ORDER')
    recoveries = [e['value']['result'] for e in content if e['kind'] == 'recovery.observed']
    if recoveries != model['recovery_constraints']: raise HarnessError('RECOVERY_OUTPUT_MISMATCH')
    # Each original counterexample is latched before secondary accounting/audit
    # errors; all observed failure events must retain that exact first evidence.
    if any(e['kind'] == 'fault.observed' and not isinstance(e['value'].get('first'), dict)
           for e in content): raise HarnessError('MISSING_FIRST_CAUSAL_FAILURE')
    expected_crash = model['controlled_crash_point']
    injected = [e for e in content if e['kind'] == 'fault.injected']
    if expected_crash is not None:
        if len(injected) != 1 or injected[0]['value'] != {'point': expected_crash, 'cause': 'CONTROLLED_EXIT_77'}:
            raise HarnessError('CRASH_FAULT_WITNESS')
        parent = root.parent
        parent_events = [json.loads(line)['content'] for line in (parent / 'witness.jsonl').read_text().splitlines()]
        role = 'crash-result' + variant.removeprefix('crash') if hasattr(str, 'removeprefix') else 'crash-result' + variant[5:]
        role += '.json'
        exits = [e for e in parent_events if e['kind'] == 'process.observed_exit' and e['value']['role'] == role]
        if len(exits) != 1 or exits[0]['value']['exit_code'] != 77:
            raise HarnessError('CRASH_EXIT_NOT_INDEPENDENTLY_OBSERVED')
    elif injected:
        raise HarnessError('UNDECLARED_CRASH_INJECTION')


def prepare_campaign_instance():
    """Future qualified preparation only, never called by Package83 tooling.

    Allocate one root and bind all physical parameters before gate tests. The
    independent blueprint path is evaluated without using produced gate results.
    No campaign grant or OS capability is created by this routine.
    """
    global _RUNTIME
    entry = require_test_entry()
    if entry['binding_phase'] != 'PREPARE': raise HarnessError('PREPARATION_PHASE')
    contract = entry['campaign_root']; root = pathlib.Path(contract['path'])
    if (contract['identity'] != _id(contract['content'], 'qualification-h77-02-synthetic-campaign-root-v1')
            or str(root) != '/tmp/kge-h77-02-gate-synthetic-' + contract['identity']['sha256'][:32]
            or contract['owner'] != os.geteuid()):
        raise HarnessError('ROOT_CREATION_BINDING')
    # Exclusive mkdir consumes this preparation attempt; never reuse an existing
    # partial root after ambiguity or clean it up to obtain another attempt.
    root.mkdir(mode=0o700, exist_ok=False)
    ledger = root / 'controller-budget.jsonl'
    started_ns = time.monotonic_ns()
    header = {'kind': 'start', 'started_ns': started_ns, 'campaign_identity': entry['campaign_identity'],
              'deadline_ns': started_ns + entry['resource_limits']['TOTAL_WALL'] * 1000000000,
              'charged_bytes': 2097152, 'failure_evidence_reserve': 2097152}
    for unused in range(8):
        raw = _canon(header) + b'\n'
        if header['charged_bytes'] == 2097152 + len(raw): break
        header['charged_bytes'] = 2097152 + len(raw)
    fd = _HOST_OPEN(str(ledger), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        raw = _canon(header) + b'\n'; _HOST_WRITE(fd, raw); _HOST_FSYNC(fd)
    finally: os.close(fd)
    bootstrap = HarnessRuntime.__new__(HarnessRuntime)
    bootstrap.entry, bootstrap.root, bootstrap.ledger = entry, root, ledger
    _RUNTIME = bootstrap  # Only accounting methods used until binding completes.
    master = gate.read_pin(entry['fixture_manifest_pin'])
    if master.get('schema') != 'H77-02-FIXTURE-BINDING-SPEC-83-1':
        raise HarnessError('UNSEALED_FIXTURE_BLUEPRINT')
    master_body = dict(master); master_identity = master_body.pop('identity')
    if master_identity != _id(master_body, 'qualification-h77-02-gate-synthetic-binding-spec-v1'):
        raise HarnessError('BINDING_SPEC_IDENTITY')
    approved_names = {n for n in GateSyntheticTests.__dict__ if n.startswith('test_')}
    if set(master['test_names']) != approved_names or len(master['test_names']) != 18:
        raise HarnessError('EXACT_TEST_SELECTION')
    rows = []
    seen = set()
    for seed in (0, 1, 7, 101):
        for method in master['test_names']:
            if not method.startswith('test_') or '/' in method: raise HarnessError('TEST_DIRECTORY_RULE')
            case = root / 'cases' / ('seed%d' % seed) / method
            case.mkdir(mode=0o700, parents=True, exist_ok=False)
            variants = ['main'] + (['crash%d' % i for i in range(7)] if method ==
                         'test_controlled_crash_points_remain_blocked' else [])
            for variant in variants:
                path = case if variant == 'main' else case / variant
                if variant != 'main': path.mkdir(mode=0o700, exist_ok=False)
                descriptor = {'method': method, 'seed': seed, 'variant': variant,
                              'binding_spec_identity': master['identity']}
                produced = _produce_fixture(path, descriptor)
                expected = _expected_fixture(path, descriptor)
                if produced != expected['entry']: raise HarnessError('INDEPENDENT_FIXTURE_DERIVATION')
                for name, body in expected['documents'].items():
                    actual = path / ('store' if name == 'epoch.json' else 'authority') / name
                    if actual.read_bytes() != _canon(body): raise HarnessError('PRODUCER_BYTES_MISMATCH')
                if expected['fixture_identity']['sha256'] in seen: raise HarnessError('FIXTURE_ID_COLLISION')
                seen.add(expected['fixture_identity']['sha256'])
                row = {'schema': 'H77-02-BOUND-FIXTURE-83-1', 'root': str(path),
                       'fixture': expected, 'provenance': {'master': master['identity'],
                       'gate_executed': False, 'binding_inputs': 'owned path/device/inode only'}}
                rows.append(write_fixture(path / 'fixture-binding.json', row))
    catalog = {'schema': 'H77-02-SEALED-FIXTURE-CATALOG-83-1',
               'campaign_identity': entry['campaign_identity'], 'root_identity': contract['identity'],
               'rows': rows}
    pin = write_fixture(root / 'fixture-catalog.json', catalog)
    _RUNTIME = None
    return pin  # Qualified owner must seal RUN entry; not automatic activation.


def require_test_entry():
    name = os.environ.get('KGE_H77_GATE_SYNTHETIC_TEST_ENTRY')
    gate.require(name is not None, 'NO_AUTHORIZED_SYNTHETIC_TEST_ENTRY')
    path = pathlib.Path(name)
    boundary = EVIDENCE / 'single-use-gate-implementation-qualification-1'
    gate.require(path.is_absolute() and boundary in path.parents and
                 path.resolve() == path and path.is_file(), 'TEST_ENTRY_PATH')
    fd = gate.open_directory(path.parent)
    try:
        raw, unused = gate.read_at(fd, path.name)
    finally:
        os.close(fd)
    manifest = gate.decode(raw)
    fields = {'schema', 'effective_grant_sha', 'approved_subject_sha', 'source_hashes',
              'campaign_identity', 'fixture_manifest_pin', 'independent_oracle_pin',
              'controller_qualification_pin', 'environment_qualification_pin',
              'permissions_qualification_pin', 'entry_predicates', 'resource_limits',
              'no_real_invocation', 'no_automatic_retries', 'campaign_root', 'binding_phase'}
    gate.require(set(manifest) == fields and manifest['schema'] ==
                 'H77-02-GATE-ACTIVE-SYNTHETIC-ENTRY-2', 'TEST_ENTRY_SCHEMA')
    gate.require(manifest['effective_grant_sha'] == GRANT80_SHA and
                 manifest['approved_subject_sha'] == SUBJECT79_SHA, 'TEST_ENTRY_AUTHORITY')
    refpath = EVIDENCE / 'gate-construction-grant-80/effective-gate-construction-grant-reference.json'
    ref = json.loads(refpath.read_text())
    gate.require(ref['GRANT_EFFECTIVE'] is True and ref['GRANT_IDENTITY']['sha256'] ==
                 GRANT80_SHA, 'CONSTRUCTION_GRANT_NOT_EFFECTIVE')
    grantpin = ref['GRANT_RECORD_PIN']
    rawgrant = (ROOT / grantpin['PATH']).read_bytes()
    gate.require(hashlib.sha256(rawgrant).hexdigest() == grantpin['RAW_SHA256'], 'GRANT_PIN')
    grantdoc = gate.decode(rawgrant)
    gate.require(gate.identity(grantdoc['RECORD'], grantdoc['GRANT_IDENTITY']['namespace']) ==
                 grantdoc['GRANT_IDENTITY'], 'ISSUED_GRANT_IDENTITY')
    gate.require(set(manifest['source_hashes']) == set(SOURCE_PATHS) and
                 all(hashlib.sha256((ROOT / f).read_bytes()).hexdigest() == h
                     for f, h in manifest['source_hashes'].items()), 'TEST_SOURCE_IDENTITY')
    predicates = {'grant_effective', 'grant_current_and_unrevoked', 'test_phase_authorized',
                  'fixtures_synthetic', 'executable_verified', 'environment_verified',
                  'resource_limits_enforceable', 'paths_authorized', 'campaign_authority_valid',
                  'independent_observer_verified'}
    gate.require(set(manifest['entry_predicates']) == predicates and
                 all(v is True for v in manifest['entry_predicates'].values()), 'TEST_PREDICATE_UNKNOWN')
    for label in ['controller_qualification_pin', 'environment_qualification_pin',
                  'permissions_qualification_pin']:
        document = gate.read_pin(manifest[label])
        gate.require(document.get('result') == 'PASS' and document.get('campaign_identity') ==
                     manifest['campaign_identity'], 'UNQUALIFIED_TEST_RECEIPT')
    gate.check_identity(manifest['campaign_identity'])
    gate.require(manifest['no_real_invocation'] is True and
                 manifest['no_automatic_retries'] is True and
                 manifest['resource_limits'] == grantdoc['RECORD']['RESOURCE_LIMITS'],
                 'TEST_SCOPE_OR_LIMITS')
    # Such receipts require separate independent qualification and revocation,
    # environment/confinement freshness checks; this suite never generates them.
    return manifest


def write_fixture(path, value):
    if _RUNTIME is not None:
        _under(_RUNTIME.root, path)
        _RUNTIME.account('bytes', len(_canon(value)), 'fixture-writer')
    return _durable_exclusive(path, value)


def _produce_fixture(root, descriptor):
    store, auth = root / 'store', root / 'authority'
    store.mkdir(mode=0o700); auth.mkdir(mode=0o700)
    checks = {k: True for k in gate.ENTRY_CHECKS}
    subjectbody = {'purpose': 'DISPOSABLE_INERT_GATE_SYNTHETIC_ONLY', 'fixture_descriptor': descriptor}
    subject = {'CONTENT': subjectbody, 'IDENTITY': gate.identity(subjectbody,
               'qualification-h77-02-gate-synthetic-subject-v1'), 'APPROVAL': None, 'ISSUED': False}
    subjectpin = write_fixture(auth / 'subject.json', subject)
    info = store.stat()
    profile = {'schema': 'H77-02-QUALIFIED-ENTRY-PROFILE-1', 'mode': 'SYNTHETIC',
               'host': 'SYNTHETIC_DISPOSABLE_HOST', 'store_path': str(store),
               'store_device': info.st_dev, 'store_inode': info.st_ino,
               'launch_working_directory': str(root),
               'resource_limits': dict(gate.REAL_LIMITS), 'entry_checks': checks}
    profileid = gate.identity(profile, 'qualification-h77-02-gate-synthetic-profile-v1')
    command = {'operation': 'INERT_CALLBACK', 'argv': []}
    body = {'schema': 'H77-02-NORMALIZED-ISSUED-AUTHORITY-1', 'status': 'ISSUED',
            'subject_identity': subject['IDENTITY'], 'probe_identity': gate.identity(
                {'operation': 'INERT', 'fixture_descriptor': descriptor}, 'qualification-h77-02-gate-synthetic-probe-v1'),
            'command_identity': gate.identity(command, 'qualification-h77-02-command-contract-v1'),
            'context_identity': profileid, 'issuer_role': gate.ISSUER,
            'charter_identity': gate.identity({'synthetic': True},
                'qualification-h77-02-gate-synthetic-charter-v1'),
            'resource_limits': dict(gate.REAL_LIMITS), 'single_probe_limit': 1,
            'automatic_retries': 0, 'store_path': str(store), 'epoch_name': 'epoch.json'}
    grant = {'content': body, 'identity': gate.identity(body,
             'qualification-h77-02-gate-synthetic-grant-v1')}
    effective = {'schema': 'H77-02-NORMALIZED-EFFECTIVE-AUTHORITY-1',
                 'grant_identity': grant['identity'], 'subject_identity': subject['IDENTITY'],
                 'effective': True}
    epoch = {'schema': 'H77-02-AUTHORITY-EPOCH-1', 'grant_identity': grant['identity'],
             'epoch': 1, 'status': 'EFFECTIVE', 'expiration_checked': True,
             'freshness_verified': True}
    write_fixture(store / 'epoch.json', epoch)
    return {'schema': gate.SCHEMA, 'mode': 'SYNTHETIC',
            'grant_pin': write_fixture(auth / 'grant.json', grant),
            'effective_pin': write_fixture(auth / 'effective.json', effective),
            'subject_pin': subjectpin, 'profile_pin': write_fixture(auth / 'profile.json', profile),
            'store_path': str(store), 'epoch_name': 'epoch.json',
            'epoch_identity': gate.identity(epoch, 'qualification-h77-02-authority-epoch-v1'),
            'command': command, 'resource_limits': dict(gate.REAL_LIMITS),
            'execution_context': {'profile_identity': profileid,
                                  'host': 'SYNTHETIC_DISPOSABLE_HOST', 'mode': 'SYNTHETIC'},
            'entry_checks': checks, 'authorized_attempt_number': 1}


def inert():
    return {'inert_callback_only': True}


def claimant(entry, result_path, crash_stage=None):
    def hook(stage):
        if stage == crash_stage:
            fault_witness(entry, pathlib.Path(result_path).stem, stage, 'CONTROLLED_EXIT_77')
            os._exit(77)  # Only the owned disposable claimant process.
    try:
        result = observed_claim(entry, synthetic_callback=inert, stage_hook=hook, actor=pathlib.Path(result_path).stem)
        value = {'accepted': True, 'result': result}
    except BaseException as exc:
        value = {'accepted': False, 'error_type': type(exc).__name__, 'error_message': str(exc), 'errno': getattr(exc, 'errno', None)}
    write_fixture(pathlib.Path(result_path), value)


class GateSyntheticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entry_authorization = require_test_entry()
        cls.runtime = _runtime()

    def setUp(self):
        self.runtime.begin_case(self._testMethodName)
        self.root = self.runtime.case_root(self._testMethodName)
        self.entry = make_fixture(self.root)
        self.context = multiprocessing.get_context('spawn')

    def tearDown(self):
        self.runtime.finish_case(self._testMethodName)

    def claim(self, entry, **kwargs):
        return observed_claim(entry, actor='parent', **kwargs)

    # Preserve claim stores as qualification evidence, not cleanup/reset of a
    # real consumption namespace. Any later synthetic cleanup is controller-owned.
    def run_child(self, entry, name, crash_stage=None):
        child = self.context.Process(target=claimant,
                   args=(entry, str(self.root / name), crash_stage))
        self.runtime.start_child(child, name, self.root)
        return self.runtime.wait_child(child, name, expected_codes=(77,) if crash_stage else (0,))

    def test_first_and_duplicate_claim(self):
        result = self.claim(self.entry, synthetic_callback=inert)
        self.assertTrue(result['consumed']); self.assertFalse(result['retry_allowed'])
        with self.assertRaises(FileExistsError):
            self.claim(self.entry, synthetic_callback=inert)

    def test_key_is_independently_reconstructed_and_stable(self):
        doc = json.loads(pathlib.Path(self.entry['grant_pin']['path']).read_text())
        g = doc['content']
        fields, key = gate.consumption_key(doc['identity'], g['subject_identity'],
                       g['probe_identity'], g['command_identity'], self.entry['execution_context'])
        expected = {'schema': 'H77-02-CONSUMPTION-KEY-1',
                    'issued_grant_identity': doc['identity'], 'approved_subject_identity': g['subject_identity'],
                    'probe_identity': g['probe_identity'], 'command_identity': g['command_identity'],
                    'execution_context': self.entry['execution_context'], 'authorized_attempt_number': 1}
        encoded = json.dumps(expected, sort_keys=True, separators=(',', ':'),
                             ensure_ascii=False, allow_nan=False).encode('utf-8')
        self.assertEqual(fields, expected)
        self.assertEqual(key['sha256'], hashlib.sha256(encoded).hexdigest())
        reordered = dict(reversed(list(self.entry['execution_context'].items())))
        reordered_identity = gate.consumption_key(doc['identity'], g['subject_identity'],
                         g['probe_identity'], g['command_identity'], reordered)[1]
        self.runtime.event(self.root, 'parent', 'key.observed', {'fields': fields,
            'identity': key, 'reordered_identity': reordered_identity})
        self.assertEqual(key, reordered_identity)

    def test_concurrent_claimants_at_most_one(self):
        children = [self.context.Process(target=claimant,
                    args=(self.entry, str(self.root / ('result%d.json' % i)))) for i in range(2)]
        try:
            for i, child in enumerate(children):
                self.runtime.start_child(child, 'result%d' % i, self.root)
            for i, child in enumerate(children):
                self.runtime.wait_child(child, 'result%d' % i)
        except BaseException:
            self.runtime.close_children()
            raise
        results = [json.loads((self.root / ('result%d.json' % i)).read_text()) for i in range(2)]
        self.assertEqual(sum(r['accepted'] for r in results), 1)

    def test_process_restart_preserves_claim(self):
        self.assertEqual(self.run_child(self.entry, 'first.json'), 0)
        self.assertEqual(self.run_child(self.entry, 'restart.json'), 0)
        self.assertFalse(json.loads((self.root / 'restart.json').read_text())['accepted'])

    def test_controlled_crash_points_remain_blocked(self):
        for i, point in enumerate(['DURING_CLAIM', 'AFTER_FILE_FSYNC', 'AFTER_DIRECTORY_FSYNC',
                'AFTER_CLAIM_BEFORE_LAUNCH', 'DURING_LAUNCH',
                'AFTER_LAUNCH_BEFORE_OBSERVATION', 'AFTER_COMPLETION_BEFORE_AUDIT']):
            row = self.root / ('crash%d' % i)
            entry = make_fixture(row)
            self.assertEqual(self.run_child(entry, 'crash-result%d.json' % i, point), 77)
            with self.assertRaises(FileExistsError):
                self.claim(entry, synthetic_callback=inert)

    def test_before_claim_failure_does_not_launch(self):
        seen = []
        def hook(stage):
            if stage == 'BEFORE_CLAIM': raise RuntimeError('synthetic before-claim fault')
        with self.assertRaises(RuntimeError):
            self.claim(self.entry, synthetic_callback=lambda: seen.append(1), stage_hook=hook)
        self.assertEqual(seen, [])

    def test_invalid_grant_pin(self):
        self.entry['grant_pin']['sha256'] = '0' * 64
        with self.assertRaises(gate.GateError): self.claim(self.entry, synthetic_callback=inert)

    def test_wrong_command(self):
        self.entry['command']['argv'] = ['/bin/false']
        with self.assertRaises(gate.GateError): self.claim(self.entry, synthetic_callback=inert)

    def test_revoked_epoch(self):
        path = pathlib.Path(self.entry['store_path']) / self.entry['epoch_name']
        value = json.loads(path.read_text()); value['status'] = 'REVOKED'
        mutate_epoch_for_negative_case(path, value)
        with self.assertRaises(gate.GateError): self.claim(self.entry, synthetic_callback=inert)

    def test_resource_mismatch(self):
        self.entry['resource_limits'] = dict(gate.REAL_LIMITS, CHILD_CPU=31)
        with self.assertRaises(gate.GateError): self.claim(self.entry, synthetic_callback=inert)

    def test_partial_and_conflicting_records(self):
        def fault(stage):
            if stage == 'DURING_CLAIM': raise RuntimeError('synthetic partial write')
        with self.assertRaises(RuntimeError):
            self.claim(self.entry, synthetic_callback=inert, stage_hook=fault)
        claims = list(pathlib.Path(self.entry['store_path']).glob('*.claim.json'))
        self.assertEqual(len(claims), 1); self.assertEqual(claims[0].read_bytes(), b'')
        with self.assertRaises(FileExistsError): self.claim(self.entry, synthetic_callback=inert)
        recovery = observed_recover(self.entry['store_path'], claims[0].name.split('.')[0])
        self.assertEqual(recovery['state'], 'OUTCOME_UNKNOWN'); self.assertFalse(recovery['launch_permitted'])

    def test_file_fsync_failure_blocks_launch(self):
        seen = []
        with mock.patch.object(gate.os, 'fsync', side_effect=OSError('synthetic fsync failure')):
            with self.assertRaises(OSError):
                self.claim(self.entry, synthetic_callback=lambda: seen.append(1))
        self.assertEqual(seen, [])
        with self.assertRaises(FileExistsError): self.claim(self.entry, synthetic_callback=inert)

    def test_directory_fsync_failure_blocks_launch(self):
        original = gate.os.fsync
        def failure(fd):
            if os.fstat(fd).st_ino == pathlib.Path(self.entry['store_path']).stat().st_ino:
                raise OSError('synthetic directory fsync failure')
            return original(fd)
        with mock.patch.object(gate.os, 'fsync', side_effect=failure):
            with self.assertRaises(OSError): self.claim(self.entry, synthetic_callback=inert)
        with self.assertRaises(FileExistsError): self.claim(self.entry, synthetic_callback=inert)

    def test_independent_reread_failure_blocks_launch(self):
        seen = []
        with mock.patch.object(gate, 'verify_consumption_record', side_effect=gate.GateError('synthetic reread failure')):
            with self.assertRaises(gate.GateError):
                self.claim(self.entry, synthetic_callback=lambda: seen.append(1))
        self.assertEqual(seen, [])
        with self.assertRaises(FileExistsError): self.claim(self.entry, synthetic_callback=inert)

    def test_post_consumption_failure_unknown_and_no_retry(self):
        def failure(): raise RuntimeError('synthetic callback failure')
        with self.assertRaises(RuntimeError): self.claim(self.entry, synthetic_callback=failure)
        with self.assertRaises(FileExistsError): self.claim(self.entry, synthetic_callback=inert)
        claim = next(pathlib.Path(self.entry['store_path']).glob('*.claim.json'))
        self.assertFalse(observed_recover(self.entry['store_path'], claim.name.split('.')[0])['retry_allowed'])

    def test_missing_permissions_and_wrong_subject(self):
        bad = copy.deepcopy(self.entry); bad['entry_checks']['permissions_verified'] = False
        with self.assertRaises(gate.GateError): self.claim(bad, synthetic_callback=inert)
        bad = copy.deepcopy(self.entry); bad['subject_pin']['sha256'] = '0' * 64
        with self.assertRaises(gate.GateError): self.claim(bad, synthetic_callback=inert)

    def test_symlink_store_rejected(self):
        link = self.root / 'store-link'; link.symlink_to(self.entry['store_path'], target_is_directory=True)
        bad = copy.deepcopy(self.entry); bad['store_path'] = str(link)
        with self.assertRaises(OSError): self.claim(bad, synthetic_callback=inert)

    def test_no_real_launcher_reachable_in_synthetic_mode(self):
        with mock.patch.object(gate.subprocess, 'Popen', side_effect=AssertionError('real launcher forbidden')):
            self.claim(self.entry, synthetic_callback=inert)


class BoundResult(unittest.TextTestResult):
    def _preserve_failure(self, err):
        _runtime().stop_after_unexpected_failure(err[1])
    def addError(self, test, err):
        self._preserve_failure(err); super().addError(test, err)
    def addFailure(self, test, err):
        self._preserve_failure(err); super().addFailure(test, err)


def run_bound_controller():
    runtime = _runtime()
    outer = json.loads((runtime.root / 'campaign-controller.claim.json').read_text())
    if (set(outer) != {'campaign_identity', 'seeds', 'automatic_retries', 'owner_pid', 'source_sha256'} or outer['campaign_identity'] != runtime.entry['campaign_identity'] or outer['owner_pid'] != os.getppid() or outer['seeds'] != [0, 1, 7, 101] or outer['automatic_retries'] != 0 or outer['source_sha256'] != hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()):
        raise HarnessError('UNACCOUNTED_OR_UNOBSERVED_SEED_CONTROLLER')
    names = list(runtime.oracles['tests'])
    approved = {n for n in GateSyntheticTests.__dict__ if n.startswith('test_')}
    if set(names) != approved or len(names) != 18:
        raise HarnessError('EXACT_CONTROLLER_TEST_SET')
    # A per-seed exclusive lease prevents duplicate or concurrent controller runs.
    lease = runtime.root / ('controller-seed%d.claim.json' % runtime.seed)
    write_fixture(lease, {'campaign_identity': runtime.entry['campaign_identity'],
                         'seed': runtime.seed, 'test_names': names, 'retry_allowed': False})
    result = None
    try:
        suite = unittest.TestSuite(GateSyntheticTests(name) for name in names)
        result = unittest.TextTestRunner(verbosity=2, failfast=True,
                    resultclass=BoundResult).run(suite)
        if not result.wasSuccessful() or result.testsRun != 18:
            raise HarnessError('SYNTHETIC_COMPARISON_FAILURE')
    except BaseException as original:
        runtime.stop_after_unexpected_failure(original)
    finally:
        runtime.close_children()
        try: runtime.close_tracker()
        except BaseException as secondary: runtime.stop_after_unexpected_failure(secondary)
    report = {'schema': 'H77-02-CONTROLLER-OBSERVATION-84-1',
        'campaign_identity': runtime.entry['campaign_identity'], 'seed': runtime.seed,
        'tests_run': result.testsRun if result is not None else 0,
        'tracker_exit_observation': runtime._tracker_observation,
        'first_counterexample': runtime._first_failure,
        'secondary_errors': runtime._secondary_errors + runtime._observer_failures,
        'retry_count': 0, 'cleanup_policy': 'retain all consumption and witness files'}
    try: runtime.failure_evidence(runtime.root / ('controller-seed%d.result.json' % runtime.seed), report)
    except BaseException as secondary:
        runtime.stop_after_unexpected_failure(secondary)
    if runtime._first_failure is not None:
        raise HarnessError('CAMPAIGN_FAILED:' + json.dumps(runtime._first_failure, sort_keys=True))
    return report


def run_campaign_controller():
    """Future authorized outer controller; no static verifier invokes this."""
    runtime = _runtime()
    write_fixture(runtime.root / 'campaign-controller.claim.json', {
        'campaign_identity': runtime.entry['campaign_identity'], 'seeds': [0, 1, 7, 101],
        'automatic_retries': 0, 'owner_pid': os.getpid(),
        'source_sha256': hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()})
    observations = []
    limits = runtime.entry['resource_limits']
    def child_limits():
        for name, value in [('RLIMIT_CPU', limits['CHILD_CPU']),
                ('RLIMIT_AS', limits['CHILD_AS']), ('RLIMIT_FSIZE', limits['CHILD_FSIZE']),
                ('RLIMIT_NOFILE', limits['CHILD_FDS'])]:
            resource.setrlimit(getattr(resource, name), (value, value))
    for seed in (0, 1, 7, 101):
        process = None; selector = selectors.DefaultSelector(); buffers = {'stdout': bytearray(), 'stderr': bytearray()}
        role = 'seed-controller-%d' % seed
        released = False
        try:
            runtime.account('reserve', 1, role)
            environment = dict(os.environ, PYTHONHASHSEED=str(seed))
            environment.pop('KGE_H77_CURRENT_CASE', None)
            started = time.monotonic()
            process = subprocess.Popen([sys.executable, str(pathlib.Path(__file__).resolve()), '--harness-controller'],
                cwd=str(ROOT), env=environment, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, close_fds=True, start_new_session=True, preexec_fn=child_limits)
            for name, stream in [('stdout', process.stdout), ('stderr', process.stderr)]:
                os.set_blocking(stream.fileno(), False); selector.register(stream, selectors.EVENT_READ, name)
            while selector.get_map():
                runtime.account('case', 0, role)  # shared campaign deadline/stop check
                if time.monotonic() - started >= limits['CHILD_WALL']:
                    raise HarnessError('SEED_CONTROLLER_TIMEOUT:' + str(seed))
                for event, unused in selector.select(timeout=0.1):
                    chunk = os.read(event.fileobj.fileno(), 4096)
                    if not chunk: selector.unregister(event.fileobj)
                    else:
                        buffers[event.data].extend(chunk)
                        if sum(map(len, buffers.values())) > 32768:
                            raise HarnessError('SEED_CONTROLLER_OUTPUT_BUDGET')
            code = process.wait(timeout=max(0.01, limits['CHILD_WALL'] - (time.monotonic() - started)))
            observation = {'seed': seed, 'pid': process.pid, 'exit_code': code,
                'stdout': bytes(buffers['stdout']).decode('utf-8'),
                'stderr': bytes(buffers['stderr']).decode('utf-8')}
            observations.append(observation)
            runtime.account('release', 1, role)
            released = True
            if code != 0: raise HarnessError('SEED_CONTROLLER_NONZERO:' + str(seed))
            report = json.loads((runtime.root / ('controller-seed%d.result.json' % seed)).read_text())
            if (set(report) != {'schema', 'campaign_identity', 'seed', 'tests_run', 'tracker_exit_observation', 'first_counterexample', 'secondary_errors', 'retry_count', 'cleanup_policy'} or report['schema'] != 'H77-02-CONTROLLER-OBSERVATION-84-1' or report['campaign_identity'] != runtime.entry['campaign_identity'] or report['seed'] != seed or
                    report['tests_run'] != 18 or report['first_counterexample'] is not None or
                    report['secondary_errors'] or report['retry_count'] != 0):
                raise HarnessError('SEED_CONTROLLER_REPORT_MISMATCH')
            tracker_witness_path = runtime.root / 'cases' / ('seed%d' % seed) / 'test_concurrent_claimants_at_most_one' / 'witness.jsonl'
            tracker_witnesses = [json.loads(line)['content']['value'] for line in tracker_witness_path.read_text().splitlines() if json.loads(line)['content']['kind'] == 'tracker.created']
            if (len(tracker_witnesses) != 1 or report['tracker_exit_observation'] != {'pid': tracker_witnesses[0]['pid'], 'wait_status': 0, 'observed_by_parent': True}):
                raise HarnessError('TRACKER_LIFECYCLE_COMPARISON_MISMATCH')
        except BaseException as original:
            runtime.stop_after_unexpected_failure(original)
            if process is not None:
                try:
                    if process.poll() is None: os.killpg(process.pid, signal.SIGKILL)
                    process.wait(timeout=2)
                    observations.append({'seed': seed, 'pid': process.pid, 'exit_code': process.returncode,
                                         'termination_after_failure': True})
                    if not released:
                        runtime.account('release', 1, role)
                        released = True
                except BaseException as secondary: runtime.stop_after_unexpected_failure(secondary)
            break  # Never launch a later seed or retry after first failure.
        finally:
            selector.close()
            if process is not None:
                process.stdout.close(); process.stderr.close()
    report = {'schema': 'H77-02-OUTER-CONTROLLER-84-1',
        'campaign_identity': runtime.entry['campaign_identity'], 'seed_observations': observations,
        'first_counterexample': runtime._first_failure, 'secondary_errors': runtime._secondary_errors,
        'retry_count': 0, 'consumption_cleanup_permitted': False}
    try: runtime.failure_evidence(runtime.root / 'campaign-controller.result.json', report)
    except BaseException as secondary: runtime.stop_after_unexpected_failure(secondary)
    if runtime._first_failure is not None: raise HarnessError('OUTER_CAMPAIGN_FAILED')
    ledger = [json.loads(line) for line in runtime.ledger.read_text().splitlines()]
    if sum(r.get('amount', 0) for r in ledger if r['kind'] == 'reserve') != sum(
            r.get('amount', 0) for r in ledger if r['kind'] == 'release'):
        raise HarnessError('UNOBSERVED_CAMPAIGN_PROCESS')
    return report


if __name__ == '__main__':
    if sys.argv[1:] == ['--harness-prepare']:
        print(_canon(prepare_campaign_instance()).decode('utf-8'))
    elif sys.argv[1:] == ['--harness-campaign']:
        print(_canon(run_campaign_controller()).decode('utf-8'))
    elif sys.argv[1:] == ['--harness-controller']:
        print(_canon(run_bound_controller()).decode('utf-8'))
    else:
        raise HarnessError('UNCONTROLLED_TEST_DISCOVERY_DENIED')
