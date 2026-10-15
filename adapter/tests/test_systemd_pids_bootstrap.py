"""Fourteen inert cases. No default discovery/run path activates this campaign.

Only an independently sealed entry manifest can authorize future execution.
Expected records must precede execution; this module never derives an oracle
from a coordinator result. Crash/concurrency require the fixed helper controller
specified in Package89; absent its qualification this suite refuses activation.
"""
import hashlib
import json
import os
import pathlib
import unittest
import resource
import stat
import subprocess
import sys
import time
from unittest import mock
from adapter.qualification_bootstrap import systemd_pids_once as core

TEST_IDS = (
    'B89-COMMAND_REJECTION', 'B89-GRANT_REJECTION', 'B89-FIRST_CONSUMPTION',
    'B89-DUPLICATE_CONSUMPTION', 'B89-CONCURRENT_CLAIMS', 'B89-PARTIAL_RECORD',
    'B89-CRASH_BEFORE_LAUNCH', 'B89-CRASH_AFTER_CONSUMPTION', 'B89-LAUNCH_FAILURE',
    'B89-UNKNOWN_COMPLETION', 'B89-AUDIT_FAILURE', 'B89-REVOCATION',
    'B89-RESOURCE_MISMATCH', 'B89-ZERO_RETRIES')
CRASH_POINTS = ('BEFORE_CLAIM', 'DURING_CLAIM', 'AFTER_CLAIM_BEFORE_LAUNCH',
                'DURING_LAUNCH', 'AFTER_LAUNCH_BEFORE_OBSERVATION',
                'AFTER_COMPLETION_BEFORE_AUDIT')
EXPECTED_RULES = {
    'B89-COMMAND_REJECTION': 'no claim; no callback; exact rejection',
    'B89-GRANT_REJECTION': 'no claim; no callback; exact rejection',
    'B89-FIRST_CONSUMPTION': 'one full claim; barriers/independent confirmation; one inert callback',
    'B89-DUPLICATE_CONSUMPTION': 'reject even identical record; callback total1',
    'B89-CONCURRENT_CLAIMS': '<=1 successful claim and <=1 inert callback; losing identity not predetermined',
    'B89-PARTIAL_RECORD': 'ambiguous retained; callback0; recover denies',
    'B89-CRASH_BEFORE_LAUNCH': 'consumed remains; recovery denies callback',
    'B89-CRASH_AFTER_CONSUMPTION': 'partial/consumed/unknown never reopens; independent parent exit witness',
    'B89-LAUNCH_FAILURE': 'claim retained; first exception retained; no retry',
    'B89-UNKNOWN_COMPLETION': 'claim remains consumed/unknown; no resubmission',
    'B89-AUDIT_FAILURE': 'original error/available outcome preserved; permission remains consumed',
    'B89-REVOCATION': 'deny before callback; never assume fresh authority',
    'B89-RESOURCE_MISMATCH': 'no callback; rejection exact',
    'B89-ZERO_RETRIES': 'zero additional callbacks; no reset cleanup'}


def canonical(value):
    # Independent encoding; do not call coordinator identity/serialization APIs.
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False, allow_nan=False).encode('utf-8')


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


class InertFailure(RuntimeError):
    pass


class Witness:
    def __init__(self, callback_failure=False):
        self.events = []; self.callback_failure = callback_failure
        self.calls = 0; self.barriers = []; self.confirmations = []

    def observe(self, event, value):
        self.events.append({'event': event, 'value': json.loads(canonical(value))})

    def callback(self):
        self.calls += 1
        self.observe('independent.callback.entry', {'arguments': [], 'order': self.calls})
        if self.callback_failure:
            self.observe('independent.callback.exception', {'type': 'InertFailure', 'message': 'INERT_CALLBACK_FAILURE'})
            raise InertFailure('INERT_CALLBACK_FAILURE')
        self.observe('independent.callback.return', {'value': {'inert': True}})
        return {'inert': True}


def store_snapshot(fixture):
    """Independent descriptor-based bytes; never accepts the gate's result alone."""
    directory = core.owned_directory(pathlib.Path(fixture['entry']['store']))
    result = {}
    try:
        for name in sorted(os.listdir(directory)):
            if name == 'epoch.json': continue
            raw, unused = core.read_at(directory, name)
            result[name] = raw.hex()
        return result
    finally:
        os.close(directory)


def compare_record_state(case, fixture, records=None):
    records = store_snapshot(fixture) if records is None else records
    case.assertEqual(records, fixture['expected_records'])
    key = fixture['key_sha256']; name = key + '.claim.json'
    if name not in records: state = 'UNCLAIMED'
    elif records[name] == '': state = 'OUTCOME_UNKNOWN'
    else:
        record = json.loads(bytes.fromhex(records[name]))
        case.assertEqual(digest(record['content']), record['identity']['sha256'])
        case.assertEqual(record['identity']['namespace'], 'bootstrap-inert-consumption-record-v1')
        case.assertEqual(record['content']['state'], 'CONSUMED')
        case.assertEqual(digest(record['content']['key']), key)
        state = 'CONSUMED'
    case.assertEqual(state, fixture['expected_consumption_state'])
    observed_recovery = core.recover_inert(fixture['entry']['store'], key)
    case.assertEqual(observed_recovery, fixture['expected_recovery'])
    case.assertFalse(observed_recovery['launch_permitted'])
    case.assertFalse(observed_recovery['retry_allowed'])
    # Full record-set equality above includes every expected audit phase and the
    # absence of unauthorized phases; validate audit ancestry as a separate witness.
    for name, encoded in records.items():
        if name.endswith('.claim.json') or name == 'crash-witness.json': continue
        audit = json.loads(bytes.fromhex(encoded))
        case.assertEqual(audit['schema'], 'BOOTSTRAP-AUDIT-1')
        case.assertEqual(audit['key']['sha256'], key)
        case.assertIn(audit['phase'], ('consumed', 'attempt', 'completed', 'unknown'))
    return records


def compare_concurrent_snapshots(case, fixture, observations):
    case.assertEqual(len(observations), 2)
    successes = sum(item['result'] is not None for item in observations)
    callbacks = sum(item['callback_count'] for item in observations)
    case.assertLessEqual(successes, 1)
    case.assertLessEqual(callbacks, 1)
    case.assertEqual(successes, 1)
    case.assertEqual(callbacks, 1)
    expected = fixture['expected_final_records']
    for item in observations:
        case.assertEqual(item['retry_count'], 0)
        vector = {k:v for k,v in item.items() if k != 'records'}
        case.assertIn(vector, fixture['accepted_helper_vectors'])
        if item['result'] is not None:
            case.assertEqual(item['records'], expected)
        else:
            case.assertIn(item['failure'], fixture['accepted_loser_failures'])
            case.assertTrue(set(item['records']) <= set(expected))
            for name, encoded in item['records'].items():
                actual = bytes.fromhex(encoded); final = bytes.fromhex(expected[name])
                case.assertTrue(final.startswith(actual), 'NONPREFIX_CONCURRENT_SNAPSHOT')
                # Empty is an observed incomplete publication, never a fresh claim.
                if not actual: case.assertIn(name, expected)
    compare_record_state(case, fixture)


class BoundedParentStream:
    """A precharged parent capture; no uncapped TextTestRunner stderr fallback."""
    def __init__(self, permit, fd, allowance):
        self.permit = permit; self.fd = fd; self.allowance = allowance; self.written = 0

    def write(self, text):
        raw = text.encode('utf-8')
        if self.written + len(raw) > self.allowance:
            raise InertFailure('PARENT_OUTPUT_CEILING')
        # allowance was precharged in full; check the common deadline before writes.
        self.permit.charge(0)
        core._write_all(self.fd, raw); self.written += len(raw)
        return len(text)

    def flush(self):
        os.fsync(self.fd)

class BootstrapInertTests(unittest.TestCase):
    """Fixtures and complete expected witness vectors are sealed future inputs."""
    permit = None
    # No reusable arbitrary callback/launcher parameter; this source fixes callbacks.
    qualified_helper_controller = None

    @classmethod
    def setUpClass(cls):
        if cls.permit is None:
            raise RuntimeError('NO_INDEPENDENTLY_VERIFIED_CAMPAIGN_ENTRY')
        cls.permit.check()
        if cls.qualified_helper_controller is None:
            raise RuntimeError('FIXED_HELPER_CONTROLLER_NOT_QUALIFIED')

    def fixture(self, test_id, variant='primary'):
        self.assertIn(test_id, TEST_IDS)
        candidates = [v for v in self.permit.manifest['fixtures'].values()
                      if v['entry']['test_id'] == test_id and v['variant'] == variant]
        self.assertEqual(len(candidates), 1)
        fixture = candidates[0]
        self.assertEqual(fixture['expected_rule'], EXPECTED_RULES[test_id])
        self.assertEqual(digest(fixture['expected']), fixture['expected_sha256'])
        self.assertEqual(digest(fixture['entry']), fixture['entry_sha256'])
        # Physical paths are observation bindings, excluded from semantic key.
        self.assertTrue(pathlib.Path(fixture['entry']['store']).is_relative_to(self.permit.root)
                        if hasattr(pathlib.Path, 'is_relative_to') else
                        self.permit.root in pathlib.Path(fixture['entry']['store']).parents)
        return fixture

    def exercise(self, fixture, point=None, callback_failure=False, audit_failure=False):
        entry = fixture['entry']; witness = Witness(callback_failure)
        original_fsync = core.os.fsync; original_confirm = core.confirm_consumption
        original_publish = core._publish
        def barrier(fd):
            info = os.fstat(fd)
            witness.barriers.append({'directory': stat.S_ISDIR(info.st_mode)})
            return original_fsync(fd)
        def confirmation(directory, name, expected, inode):
            value = original_confirm(directory, name, expected, inode)
            # Independent readonly bytes/identity check, not merely returned success.
            fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory)
            try: raw = os.read(fd, 65537)
            finally: os.close(fd)
            self.assertEqual(raw, canonical(expected))
            self.assertEqual(digest(expected['content']), expected['identity']['sha256'])
            witness.confirmations.append(expected['identity'])
            return value
        def fault(observed):
            if observed == point:
                witness.observe('independent.fault', {'point': point})
                raise InertFailure('INERT_FAULT:' + point)
        def publication(directory, name, value, permit, **kwargs):
            if audit_failure and '.claim.json' not in name:
                witness.observe('independent.audit.failure', {'name': name})
                raise InertFailure('INERT_AUDIT_FAILURE')
            return original_publish(directory, name, value, permit, **kwargs)
        result = None; failure = None; original_fault = None
        with mock.patch.object(core.os, 'fsync', barrier), \
             mock.patch.object(core, 'confirm_consumption', confirmation), \
             mock.patch.object(core, '_publish', publication):
            try:
                result = core.consume_inert(entry, self.permit, witness.callback,
                                            witness.observe, fault if point else None)
            except Exception as error:
                original_fault = error
                failure = {'type': type(error).__name__, 'message': str(error),
                           'first': getattr(error, 'bootstrap_first', None),
                           'secondary': list(getattr(error, 'bootstrap_secondary', ()))}
        try: records = store_snapshot(fixture)
        except BaseException as later:
            if original_fault is None: raise
            original_fault.bootstrap_secondary = tuple(getattr(original_fault, 'bootstrap_secondary', ())) + ({'phase':'snapshot_observer','type':type(later).__name__,'message':str(later)},)
            raise original_fault from later
        observation = {'result': result, 'failure': failure, 'events': witness.events,
                       'callback_count': witness.calls, 'barriers': witness.barriers,
                       'confirmations': witness.confirmations, 'records': records,
                       'retry_count': 0}
        # Compare every field with independently sealed per-operation vectors.
        return observation

    def compare(self, fixture, observation):
        self.assertEqual(set(observation), set(fixture['expected']))
        self.assertEqual(observation, fixture['expected'])
        self.assertEqual(observation['retry_count'], 0)
        self.assertLessEqual(observation['callback_count'], 1)
        compare_record_state(self, fixture, observation['records'])

    def case(self, test_id, **fault):
        fixture = self.fixture(test_id)
        self.compare(fixture, self.exercise(fixture, **fault))

    def test_COMMAND_REJECTION(self):
        self.case('B89-COMMAND_REJECTION')

    def test_GRANT_REJECTION(self):
        self.case('B89-GRANT_REJECTION')

    def test_FIRST_CONSUMPTION(self):
        self.case('B89-FIRST_CONSUMPTION')

    def test_DUPLICATE_CONSUMPTION(self):
        first = self.fixture('B89-DUPLICATE_CONSUMPTION', 'first')
        self.compare(first, self.exercise(first))
        duplicate = self.fixture('B89-DUPLICATE_CONSUMPTION')
        self.compare(duplicate, self.exercise(duplicate))
        observed = self.qualified_helper_controller.run(duplicate, ('restart',))
        self.assertEqual(observed, duplicate['expected_helpers'])

    def test_CONCURRENT_CLAIMS(self):
        # The controller must be fixed-source, separately sealed and qualified.
        # No arbitrary subprocess API is exposed by this test or the coordinator.
        fixture = self.fixture('B89-CONCURRENT_CLAIMS')
        observation = self.qualified_helper_controller.run(fixture, ('claim', 'claim'))
        compare_concurrent_snapshots(self, fixture, observation)

    def test_PARTIAL_RECORD(self):
        self.case('B89-PARTIAL_RECORD', point='DURING_CLAIM')

    def test_CRASH_BEFORE_LAUNCH(self):
        self.case('B89-CRASH_BEFORE_LAUNCH', point='AFTER_CLAIM_BEFORE_LAUNCH')

    def test_CRASH_AFTER_CONSUMPTION(self):
        # Raising an exception is not evidence of actual process-crash recovery.
        for point in CRASH_POINTS:
            fixture = self.fixture('B89-CRASH_AFTER_CONSUMPTION', point)
            observed = self.qualified_helper_controller.run(fixture, (point,))
            self.assertEqual(observed, fixture['expected_helpers'])
            recovery = core.recover_inert(fixture['entry']['store'], fixture['key_sha256'])
            self.assertEqual(recovery, fixture['expected_recovery'])
            self.assertFalse(recovery['launch_permitted'])
            self.assertFalse(recovery['retry_allowed'])
            compare_record_state(self, fixture)

    def test_LAUNCH_FAILURE(self):
        self.case('B89-LAUNCH_FAILURE', callback_failure=True)

    def test_UNKNOWN_COMPLETION(self):
        self.case('B89-UNKNOWN_COMPLETION', point='AFTER_LAUNCH_BEFORE_OBSERVATION')

    def test_AUDIT_FAILURE(self):
        self.case('B89-AUDIT_FAILURE', audit_failure=True)

    def test_REVOCATION(self):
        self.case('B89-REVOCATION')

    def test_RESOURCE_MISMATCH(self):
        self.case('B89-RESOURCE_MISMATCH')

    def test_ZERO_RETRIES(self):
        failed = self.fixture('B89-ZERO_RETRIES', 'first')
        self.compare(failed, self.exercise(failed, callback_failure=True))
        duplicate = self.fixture('B89-ZERO_RETRIES')
        self.compare(duplicate, self.exercise(duplicate))


class FixedHelperController:
    """Exact same-file helpers only. Future campaign entry supplies all pins.

    Source review does not establish enforceability of these resource controls.
    No automatic restart, retry, cleanup of consumption, or arbitrary command API.
    """
    def __init__(self, permit, entry_pin):
        self.permit = permit; self.entry_pin = entry_pin
        self.launches = 0; self.first_failure = None; self.secondary = []
        self.started = time.monotonic()
        self.exit_observations = []

    def run(self, fixture, operations):
        if len(operations) > 2 or self.launches + len(operations) > 16:
            raise RuntimeError('HELPER_PROCESS_CEILING')
        if any(op not in ('claim', 'restart', 'preflight') + CRASH_POINTS for op in operations):
            raise RuntimeError('UNAPPROVED_HELPER_OPERATION')
        children = []; outputs = []; observations = []; causal = None
        try:
            for index, operation in enumerate(operations):
                self.permit.check(); self.permit.charge(65536)
                if time.monotonic() - self.started >= 30:
                    raise RuntimeError('CAMPAIGN_DEADLINE')
                # No writable output outside the exact campaign-owned case root.
                output = pathlib.Path(fixture['entry']['store']).parent / ('helper-' + operation + '-' + str(index) + '.json')
                fd = os.open(str(output), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
                outputs.append((output, fd))
                argv = [sys.executable, '-m', 'adapter.tests.test_systemd_pids_bootstrap',
                        '--inert-helper', self.entry_pin['path'], self.entry_pin['raw_sha256'],
                        fixture['entry']['fixture_id'], operation]
                def child_limits():
                    for key, value in ((resource.RLIMIT_CPU, 5), (resource.RLIMIT_AS, 134217728),
                                       (resource.RLIMIT_FSIZE, 65536), (resource.RLIMIT_NOFILE, 32)):
                        resource.setrlimit(key, (value, value))
                self.launches += 1  # Counts even a launch failure; never refunded.
                launched = time.monotonic()  # Conservative before-Popen absolute deadline.
                child = subprocess.Popen(argv, cwd=str(core.ROOT), stdin=subprocess.DEVNULL,
                                         stdout=fd, stderr=fd, close_fds=True, start_new_session=True,
                                         env={'PATH': '/usr/bin:/bin', 'PYTHONNOUSERSITE': '1',
                                              'PYTHONHASHSEED': '0', 'PYTHONDONTWRITEBYTECODE': '1'},
                                         preexec_fn=child_limits)
                children.append(child)
                self.exit_observations.append({'pid': child.pid, 'fixture_id': fixture['entry']['fixture_id'],
                                               'operation': operation, 'launch_time': launched,
                                               'deadline': min(launched + 10, self.started + 30), 'status': None})
            for child, (output, fd) in zip(children, outputs):
                receipt = next(r for r in self.exit_observations if r['pid'] == child.pid)
                remaining = receipt['deadline'] - time.monotonic()
                if remaining <= 0: raise RuntimeError('CAMPAIGN_DEADLINE')
                status = child.wait(timeout=remaining)  # Parent independently observes exit.
                receipt['status'] = status
                receipt['wait_observed'] = True
                os.fsync(fd)
                parent = core.owned_directory(output.parent)
                try: raw, unused = core.read_at(parent, output.name)
                finally: os.close(parent)
                receipt['raw_sha256'] = hashlib.sha256(raw).hexdigest()
                receipt['output_path'] = str(output)
                receipt['actual_bytes'] = len(raw)
                if len(raw) > 65536: raise RuntimeError('HELPER_OUTPUT_CEILING')
                self.permit.charge(0)
                if status == 77:
                    crash_path = pathlib.Path(fixture['entry']['store']) / 'crash-witness.json'
                    crash_dir = core.owned_directory(crash_path.parent)
                    try: crash_raw, unused = core.read_at(crash_dir, crash_path.name)
                    finally: os.close(crash_dir)
                    crash_record = json.loads(crash_raw)
                    receipt['fault_witness_sha256'] = hashlib.sha256(crash_raw).hexdigest()
                    if crash_record['point'] not in CRASH_POINTS:
                        raise RuntimeError('MISSING_INDEPENDENT_CRASH_WITNESS')
                    if crash_record['point'] != receipt['operation']:
                        raise RuntimeError('WRONG_CRASH_POINT')
                    observations.append(dict(crash_record, exit_status=77, controlled_crash=True))
                elif status == 0:
                    observations.append(json.loads(raw))
                else: raise RuntimeError('UNEXPECTED_HELPER_EXIT:' + str(status))
            selected = [r for r in self.exit_observations if r['pid'] in {c.pid for c in children}]
            if len({r['pid'] for r in selected}) != len(children) or not all(r.get('wait_observed') for r in selected):
                raise RuntimeError('MISSING_INDEPENDENT_EXIT_BINDING')
            return observations
        except BaseException as error:
            causal = error
            if self.first_failure is None:
                self.first_failure = {'type': type(error).__name__, 'message': str(error)}
            else: self.secondary.append({'type': type(error).__name__, 'message': str(error)})
            raise
        finally:
            for child in children:
                if child.poll() is None:
                    try:
                        os.killpg(child.pid, 9); child.wait(timeout=2)
                    except BaseException as error:
                        self.secondary.append({'type': type(error).__name__, 'message': str(error)})
            for output, fd in outputs:
                try: os.close(fd)
                except OSError as error:
                    self.secondary.append({'type': type(error).__name__, 'message': str(error)})
            if self.secondary:
                if self.first_failure is None:
                    self.first_failure = dict(self.secondary[0])
                    raise InertFailure('SECONDARY_PROCESS_OR_ACCOUNTING_FAILURE')
                if causal is not None:
                    causal.bootstrap_first = self.first_failure
                    causal.bootstrap_secondary = tuple(self.secondary)
                # Retained secondary failures never replace the active primary error.
            # No deletion of durable consumption records or retained crash evidence.


def helper(entry_pin, fixture_id, operation):
    permit = core.authorize_campaign(entry_pin)
    fixture = permit.fixture(fixture_id)
    case = BootstrapInertTests(); case.permit = permit
    if operation == 'preflight':
        return {'limits': {str(key): list(resource.getrlimit(key)) for key in
                          (resource.RLIMIT_CPU, resource.RLIMIT_AS, resource.RLIMIT_FSIZE, resource.RLIMIT_NOFILE)},
                'callback_count': 0}
    if operation == 'restart':
        return dict(core.recover_inert(fixture['entry']['store'], fixture['key_sha256']), callback_count=0)
    if operation in CRASH_POINTS:
        witness = Witness()
        def crash(point):
            if point == operation:
                # Independent fault witness survives the deliberately abrupt exit.
                record = canonical({'point': point, 'callback_count': witness.calls, 'retry_count': 0})
                permit.charge(len(record))
                folder = pathlib.Path(fixture['entry']['store'])
                directory = core.owned_directory(folder)
                fd = os.open('crash-witness.json', os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=directory)
                try:
                    core._write_all(fd, record); os.fsync(fd); os.fsync(directory)
                finally: os.close(fd); os.close(directory)
                os._exit(77)
        core.consume_inert(fixture['entry'], permit, witness.callback, witness.observe, crash)
        raise RuntimeError('CRASH_INJECTION_NOT_REACHED')
    if operation == 'claim':
        return case.exercise(fixture)
    raise RuntimeError('UNAPPROVED_HELPER_OPERATION')


def run_campaign(pin):
    permit = None; controller = None
    try:
        permit = core.authorize_campaign(pin)
        controller = FixedHelperController(permit, pin)
        claim_fd = core.owned_directory(permit.root); claim_error = None
        try:
            campaign_claim = {'campaign': permit.manifest['campaign_identity'], 'consumed': True, 'retries': 0}
            core._publish(claim_fd, 'active-campaign-consumed.json', campaign_claim, permit)
            confirmed_bytes, unused = core.read_at(claim_fd, 'active-campaign-consumed.json')
            if confirmed_bytes != canonical(campaign_claim):
                raise RuntimeError('CAMPAIGN_CLAIM_CONFIRMATION_FAILURE')
        except BaseException as error:
            claim_error = error
            raise
        finally:
            try: os.close(claim_fd)
            except OSError as later:
                if claim_error is None: raise
                claim_error.bootstrap_secondary = tuple(getattr(claim_error, 'bootstrap_secondary', ())) + ({'phase':'campaign_claim_close','type':type(later).__name__,'message':str(later)},)
        BootstrapInertTests.permit = permit
        BootstrapInertTests.qualified_helper_controller = controller
        first = next(v for v in permit.manifest['fixtures'].values()
                     if v['entry']['test_id'] == 'B89-FIRST_CONSUMPTION')
        preflight = controller.run(first, ('preflight',))
        if preflight != first['expected_preflight']:
            raise SystemExit('RESOURCE_PREFLIGHT_MISMATCH')
        suite = unittest.TestSuite(BootstrapInertTests('test_' + name[4:]) for name in TEST_IDS)
        permit.charge(65536)
        logfd = os.open(str(permit.root / 'parent-test-stream.log'),
                        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        primary_stream_error = None
        try:
            stream = BoundedParentStream(permit, logfd, 65536)
            result = unittest.TextTestRunner(stream=stream, failfast=True).run(suite)
            stream.flush()
        except BaseException as error:
            primary_stream_error = error
            raise
        finally:
            try: os.close(logfd)
            except OSError as cleanup:
                if primary_stream_error is None: raise
                primary_stream_error.bootstrap_secondary = tuple(getattr(primary_stream_error, 'bootstrap_secondary', ())) + ({'phase':'parent_stream_close','type':type(cleanup).__name__,'message':str(cleanup)},)
        if result.wasSuccessful() and controller.launches != 10:
            raise RuntimeError('EXACT_HELPER_LAUNCH_ACCOUNTING_MISMATCH')
        summary = {'tests_run': result.testsRun, 'success': result.wasSuccessful(),
                   'failures': result.failures, 'errors': result.errors,
                   'launches': controller.launches, 'exit_observations': controller.exit_observations,
                   'first_failure': controller.first_failure, 'secondary': controller.secondary, 'retries': 0}
        # unittest errors are converted to strings, not serialized native results.
        summary['failures'] = [(str(case), detail) for case, detail in result.failures]
        summary['errors'] = [(str(case), detail) for case, detail in result.errors]
        primary = (summary['failures'] + summary['errors'])[:1]
        folder = core.owned_directory(permit.root); result_error = None
        try:
            try: core._publish(folder, 'campaign-result.json', summary, permit)
            except BaseException as audit_error:
                if primary:
                    preserved = InertFailure('FIRST_TEST_COUNTEREXAMPLE:' + primary[0][1])
                    preserved.bootstrap_first = primary[0]
                    preserved.bootstrap_secondary = ({'type': type(audit_error).__name__, 'message': str(audit_error)},)
                    raise preserved from audit_error
                raise
        except BaseException as error:
            result_error = error
            raise
        finally:
            try: os.close(folder)
            except OSError as later:
                if result_error is None and not primary: raise
                if result_error is not None:
                    result_error.bootstrap_secondary = tuple(getattr(result_error, 'bootstrap_secondary', ())) + ({'phase':'campaign_result_close','type':type(later).__name__,'message':str(later)},)
                else:
                    preserved = InertFailure('FIRST_TEST_COUNTEREXAMPLE:' + primary[0][1])
                    preserved.bootstrap_first = primary[0]
                    preserved.bootstrap_secondary = ({'phase':'campaign_result_close','type':type(later).__name__,'message':str(later)},)
                    raise preserved from later
        # No rerun; consumption evidence is retained even after a failed campaign.
        return 0 if result.wasSuccessful() else 1
    except BaseException as original:
        first = {'type': type(original).__name__, 'message': str(original)}
        secondary = list(getattr(original, 'bootstrap_secondary', ()))
        if permit is not None:
            folder = None
            try:
                folder = core.owned_directory(permit.root)
                core._publish(folder, 'campaign-first-failure.json',
                              {'first': first, 'secondary': secondary, 'retry_allowed': False,
                               'launch_attempts': controller.launches if controller else 0,
                               'exit_observations': controller.exit_observations if controller else []}, permit)
            except BaseException as later:
                secondary.append({'type': type(later).__name__, 'message': str(later)})
            finally:
                if folder is not None:
                    try: os.close(folder)
                    except OSError as later:
                        secondary.append({'type': type(later).__name__, 'message': str(later)})
        try:
            original.bootstrap_first = getattr(original, 'bootstrap_first', first)
            original.bootstrap_secondary = tuple(secondary)
        except BaseException: pass
        raise


if __name__ == '__main__':
    if len(sys.argv) == 6 and sys.argv[1] == '--inert-helper':
        answer = helper({'path': sys.argv[2], 'raw_sha256': sys.argv[3]}, sys.argv[4], sys.argv[5])
        sys.stdout.write(canonical(answer).decode('utf-8'))
    elif len(sys.argv) == 4 and sys.argv[1] == '--inert-campaign':
        raise SystemExit(run_campaign({'path': sys.argv[2], 'raw_sha256': sys.argv[3]}))
    else:
        raise SystemExit('NO_VERIFIED_CAMPAIGN_ENTRY; NO_DEFAULT_TEST_EXECUTION')
