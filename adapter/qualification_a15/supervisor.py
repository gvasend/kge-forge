"""Bounded fake-protocol supervisor, namespace launcher and independent exit observer.

No native Planner dispatch. All real grant/enforcement checks precede fake calls.
"""
import json
import fcntl
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time
from . import contracts as c

SOURCE_FILES = ('adapter/qualification_a15/__init__.py',
                'adapter/qualification_a15/contracts.py',
                'adapter/qualification_a15/supervisor.py',
                'adapter/qualification_a15/worker.py',
                'adapter/qualification_a15/reader.py',
                'adapter/tests/test_qualification_a15_harness.py')

class Campaign:
    def __init__(self, scratch, audit):
        self.scratch = Path(scratch)
        self.audit = audit
        self.started = time.monotonic()
        self.launches = 0
        self.live = 0
        self.written = 0
        self.stopped = False
        self.environment_verified = False
        self.budget_path = Path(__file__).resolve().parents[2] / 'docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1/campaign-budget.jsonl'

    def account(self, kind, amount=0):
        # One append-only, locked campaign ledger shared by all seed/process runs.
        self.budget_path.parent.mkdir(parents=True, exist_ok=True)
        c.require(not self.budget_path.is_symlink(), 'BUDGET_SYMLINK')
        fd = os.open(str(self.budget_path), os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, 'r+', encoding='utf-8') as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            rows = [json.loads(line) for line in stream.read().splitlines()]
            now = time.monotonic()
            if not rows:
                rows = [{'kind': 'campaign_start', 'grant_sha': c.GRANT_SHA, 'at': now}]
                stream.write(json.dumps(rows[0], sort_keys=True) + '\n')
            c.require(rows[0]['grant_sha'] == c.GRANT_SHA and now - rows[0]['at'] < c.LIMITS['campaign_wall'], 'GLOBAL_CAMPAIGN_WALL_LIMIT')
            launches = sum(r.get('amount', 0) for r in rows if r['kind'] == 'reserve')
            live = sum(r.get('amount', 0) for r in rows if r['kind'] == 'reserve') - sum(r.get('amount', 0) for r in rows if r['kind'] == 'release')
            written = sum(r.get('amount', 0) for r in rows if r['kind'] == 'bytes')
            c.require(not any(r['kind'] == 'stop' for r in rows), 'GLOBAL_CAMPAIGN_STOPPED')
            c.require(launches + (amount if kind == 'reserve' else 0) <= c.LIMITS['launches'], 'GLOBAL_LAUNCH_LIMIT')
            c.require(live + (amount if kind == 'reserve' else 0) <= c.LIMITS['live'], 'GLOBAL_LIVE_LIMIT')
            c.require(written + (amount if kind == 'bytes' else 0) <= c.LIMITS['campaign_bytes'], 'GLOBAL_BYTE_LIMIT')
            stream.write(json.dumps({'kind': kind, 'amount': amount, 'pid': os.getpid(), 'at': now}, sort_keys=True) + '\n')
            stream.flush(); os.fsync(stream.fileno())
            fcntl.flock(stream, fcntl.LOCK_UN)

    def check(self):
        c.require(not self.stopped, 'CAMPAIGN_STOPPED_NO_RETRY')
        c.require(time.monotonic() - self.started < c.LIMITS['campaign_wall'],
                  'CAMPAIGN_WALL_LIMIT')
        c.require(self.written <= c.LIMITS['campaign_bytes'], 'CAMPAIGN_BYTE_LIMIT')

    def charge(self, byte_count):
        c.require(type(byte_count) is int and byte_count >= 0, 'INVALID_BYTE_ACCOUNT')
        self.account('bytes', byte_count)
        self.written += byte_count
        self.check()

    def reserve(self):
        self.check()
        # Reserved physical slots: bwrap monitor plus one fixed-role payload.
        # Independently sealed worker/reader/probe code cannot spawn children.
        c.require(self.live + 2 <= c.LIMITS['live'], 'LIVE_CHILD_LIMIT')
        c.require(self.launches + 2 <= c.LIMITS['launches'], 'CHILD_LAUNCH_LIMIT')
        self.account('reserve', 2)
        self.launches += 2
        self.live += 2

    def release(self):
        self.account('release', 2)
        self.live -= 2
        c.require(self.live >= 0, 'INVALID_CHILD_ACCOUNT')

    def fail_closed(self, failure, detail):
        self.account('stop')
        self.stopped = True
        self.audit({'kind': 'first_counterexample', 'failure': failure, 'detail': detail,
                    'launches': self.launches, 'written': self.written, 'retry': False})
        raise c.ProtocolError(failure)

def _limits():
    pairs = [(resource.RLIMIT_CPU, c.LIMITS['cpu']),
             (resource.RLIMIT_AS, c.LIMITS['as']),
             (resource.RLIMIT_FSIZE, c.LIMITS['file']),
             (resource.RLIMIT_NOFILE, c.LIMITS['fds'])]
    for key, limit in pairs:
        resource.setrlimit(key, (limit, limit))
        if resource.getrlimit(key) != (limit, limit):
            raise c.ProtocolError('RESOURCE_CONTROL_UNSUPPORTED')

def _environment(seed):
    c.require(type(seed) is int and seed in (0, 1, 7, 101), 'INVALID_HASH_SEED')
    return {'PATH': '/usr/bin:/bin', 'PYTHONPATH': '/code',
            'PYTHONDONTWRITEBYTECODE': '1', 'LC_ALL': 'C.UTF-8', 'PYTHONHASHSEED': str(seed)}

def _sandbox_command(repo, scratch, output, readonly_output, command):
    repo, scratch, output = Path(repo), Path(scratch), Path(output)
    c.private_path(output, scratch)
    argv = ['/usr/bin/bwrap', '--unshare-user', '--unshare-pid', '--unshare-net',
            '--unshare-ipc', '--unshare-uts', '--die-with-parent', '--new-session',
            '--cap-drop', 'ALL']
    for system in ('/usr', '/bin', '/lib', '/lib64'):
        if Path(system).exists():
            argv += ['--ro-bind', system, system]
    argv += ['--proc', '/proc', '--dev', '/dev', '--dir', '/code', '--dir', '/code/adapter',
             '--ro-bind', str(repo / 'adapter/__init__.py'), '/code/adapter/__init__.py',
             '--ro-bind', str(repo / 'adapter/qualification_a15'), '/code/adapter/qualification_a15',
             '--dir', '/code/adapter/tests', '--ro-bind', str(repo / SOURCE_FILES[-1]),
             '/code/' + SOURCE_FILES[-1], '--dir', '/tmp', '--dir', str(scratch),
             '--ro-bind', str(scratch / 'fixtures'), str(scratch / 'fixtures'),
             '--ro-bind', str(scratch / 'proof.json'), str(scratch / 'proof.json'),
             '--ro-bind' if readonly_output else '--bind', str(output), str(output),
             '--chdir', '/code']
    return argv + command

def launch_child(campaign, argv, seed, timeout=60):
    c.require(0 < timeout <= c.LIMITS['wall'], 'UNAUTHORIZED_CHILD_TIMEOUT')
    campaign.reserve()
    start = time.monotonic_ns()
    process = None
    try:
        process = subprocess.Popen(argv, env=_environment(seed), cwd='/',
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            close_fds=True, start_new_session=True, preexec_fn=_limits)
        try:
            out, err = process.communicate(timeout=min(timeout,
                c.LIMITS['campaign_wall'] - (time.monotonic() - campaign.started)))
        except subprocess.TimeoutExpired:
            # Only this own child process group; bwrap dies with its monitor.
            os.killpg(process.pid, signal.SIGKILL)
            out, err = process.communicate()
            record = {'kind': 'child_exit', 'host_child_pid': process.pid,
                'supervisor_host_pid': os.getpid(), 'started_ns': start,
                'exit_observed_ns': time.monotonic_ns(), 'exit_status': process.returncode,
                'timeout': True, 'stdout_sha256': c.raw_hash(out), 'stderr': err.decode(errors='replace')}
            campaign.audit(record)
            raise c.ProtocolError('WORKER_TIMEOUT')
        c.require(len(out) + len(err) <= c.LIMITS['file'], 'CHILD_PIPE_OUTPUT_LIMIT')
        campaign.charge(len(out) + len(err))
        record = {'kind': 'child_exit', 'host_child_pid': process.pid,
            'supervisor_host_pid': os.getpid(), 'started_ns': start,
            'exit_observed_ns': time.monotonic_ns(), 'exit_status': process.returncode,
            'timeout': False, 'stdout_sha256': c.raw_hash(out), 'stderr': err.decode(errors='replace')}
        campaign.audit(record)
        c.require(process.returncode == 0, 'CHILD_NONZERO_EXIT')
        return out, record
    except OSError as exc:
        raise c.ProtocolError('WORKER_LAUNCH_FAILED') from exc
    finally:
        if process is not None and process.poll() is None:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
        campaign.release()

PROBE = """import json,os,pathlib,resource
limits={k:list(resource.getrlimit(getattr(resource,k))) for k in ('RLIMIT_CPU','RLIMIT_AS','RLIMIT_FSIZE','RLIMIT_NOFILE')}
interfaces=sorted(p.name for p in pathlib.Path('/sys/class/net').glob('*')) if pathlib.Path('/sys/class/net').exists() else []
routes=pathlib.Path('/proc/net/route').read_text().splitlines()[1:]
print(json.dumps({'limits':limits,'pid_namespace':os.readlink('/proc/self/ns/pid'),'net_namespace':os.readlink('/proc/self/ns/net'),'pid':os.getpid(),'proc_pids':sorted(p.name for p in pathlib.Path('/proc').iterdir() if p.name.isdigit()),'routes':routes,'interfaces':interfaces,'workspace_visible':pathlib.Path('/home/gvasend/app/kge-forge/docs/plans').exists(),'code_readonly':bool(os.statvfs('/code/adapter/qualification_a15').f_flag & os.ST_RDONLY),'fixtures_readonly':bool(os.statvfs(os.environ['A15_PROBE_FIXTURES']).f_flag & os.ST_RDONLY)},sort_keys=True))
"""

def verify_environment(campaign, repo, probe_output, code_hashes):
    c.require(set(code_hashes) == set(SOURCE_FILES), 'CODE_SEAL_FIELD_SET')
    for file, digest in code_hashes.items():
        c.require(c.raw_hash((Path(repo) / file).read_bytes()) == digest, 'CODE_SEAL_MISMATCH')
    # Fixed source roles contain no nested launch/native dispatch. Closed code,
    # not an untrusted request, selects the two physical process slots.
    for file in ('worker.py', 'reader.py'):
        text = (Path(repo) / 'adapter/qualification_a15' / file).read_text()
        c.require('subprocess' not in text and 'os.fork' not in text and 'adapter.planner' not in text,
                  'UNSEALED_PAYLOAD_PROCESS_CAPABILITY')
    # Add only one temporary environment binding for the metadata-only probe.
    command = _sandbox_command(repo, campaign.scratch, probe_output, False,
        ['/usr/bin/python3', '-c', PROBE.replace("os.environ['A15_PROBE_FIXTURES']", repr(str(campaign.scratch / 'fixtures')))])
    out, exit_record = launch_child(campaign, command, 0)
    result = c.parse(out)
    expected = {'RLIMIT_CPU': [30, 30], 'RLIMIT_AS': [1073741824, 1073741824],
                'RLIMIT_FSIZE': [16777216, 16777216], 'RLIMIT_NOFILE': [64, 64]}
    c.require(result['limits'] == expected, 'RESOURCE_LIMIT_OBSERVATION_MISMATCH')
    c.require(result['pid_namespace'] != os.readlink('/proc/self/ns/pid') and
              result['net_namespace'] != os.readlink('/proc/self/ns/net'), 'UNISOLATED_NAMESPACE')
    c.require(len(result['proc_pids']) <= 2, 'UNBOUNDED_SANDBOX_PROCESS_COUNT')
    c.require(not result['routes'] and all(i == 'lo' for i in result['interfaces']), 'EXTERNAL_NETWORK_AVAILABLE')
    c.require(result['code_readonly'] and result['fixtures_readonly'] and
              not result['workspace_visible'], 'FILESYSTEM_CONFINEMENT_FAILED')
    campaign.environment_verified = True
    campaign.audit({'kind': 'metadata_preflight', 'observation': result,
                    'supervisor_exit_observation': exit_record})
    return result

def observe_child_exit(record):
    c.require(record['kind'] == 'child_exit' and record['exit_status'] == 0 and
              not record['timeout'] and record['exit_observed_ns'] >= record['started_ns'],
              'WRITER_EXIT_NOT_OBSERVED')

def run_supervisor(request, bindings, campaign, repo, scope_verifier):
    c.validate(request, 'SUPERVISOR_REQUEST')
    c.require(callable(scope_verifier) and scope_verifier(request) is True, 'EXTERNAL_SCOPE_NOT_AUTHORIZED')
    c.require(campaign.environment_verified, 'UNQUALIFIED_FAKE_ENVIRONMENT')
    c.require(len(bindings) == 2 and len(request['payload']['variant_requests']) == 2,
              'EXACT_TWO_VARIANTS_REQUIRED')
    results = []
    seen_sources, seen_outputs = set(), set()
    initial = None
    try:
        for binding, expected_request in zip(bindings, request['payload']['variant_requests']):
            worker_request = c.read_exact(binding['request_path'])
            c.validate(worker_request, 'WORKER_REQUEST')
            c.require(worker_request['identity'] == expected_request, 'UNBOUND_VARIANT_REQUEST')
            c.validate_binding(binding, 'WORKER', worker_request, campaign.scratch)
            source = c.canonical(worker_request['payload']['source_identity'])
            output = binding['output_directory']
            c.require(source not in seen_sources and output not in seen_outputs, 'CROSS_VARIANT_CONTAMINATION')
            seen_sources.add(source); seen_outputs.add(output)
            state = worker_request['payload']['initial_snapshot_identity']
            if initial is None:
                initial = state
            c.require(state == initial, 'VARIANTS_DIFFERENT_INITIAL_STATE')
            argv = _sandbox_command(repo, campaign.scratch, output, False,
                ['/usr/bin/python3', '-m', 'adapter.qualification_a15.worker',
                 binding['request_path'] + '.binding',
                 str(campaign.scratch), c.raw_hash(c.canonical(binding))])
            out, writer_exit = launch_child(campaign, argv, 0)
            observe_child_exit(writer_exit)
            worker_result = c.parse(out);c.validate(worker_result, 'WORKER_RESULT')
            publication = c.read_exact(Path(output) / 'published-output.json')
            handoff = c.read_exact(Path(output) / 'handoff.json')
            c.compare_complete_output(publication, c.read_exact(binding['expected_path']))
            c.validate_handoff(handoff, worker_request, publication,
                               (Path(output) / 'published-output.json').read_bytes())
            c.require(worker_result['payload'] == {'request_identity': worker_request['identity'],
                'published_output_identity': publication['identity'], 'handoff_identity': handoff['identity']},
                'WORKER_RESULT_BINDING_MISMATCH')
            c.require({p.name for p in Path(output).iterdir()} == {'published-output.json', 'handoff.json'},
                      'UNEXPECTED_FILESYSTEM_MUTATION')
            campaign.charge(sum(p.stat().st_size for p in Path(output).iterdir()))
            readers = []
            for seed in (0, 1, 7, 101):
                reader_request = c.record('READER_REQUEST', {'case_id': worker_request['payload']['case_id'],
                    'variant_id': worker_request['payload']['variant_id'],
                    'published_output_identity': publication['identity'],
                    'expected_output_identity': c.read_exact(binding['expected_path'])['identity'], 'seed': seed})
                reader_path = Path(binding['request_path']).with_name('reader-' + str(seed) + '.json')
                reader_path.write_bytes(c.canonical(reader_request))
                rb = dict(binding, role='READER', request_path=str(reader_path),
                    request_identity=reader_request['identity'], fault='NONE',
                    exit_evidence={'writer_exit_observed': True, 'writer_exit_code': 0,
                                   'publication_verified': True, 'handoff_verified': True})
                c.validate_binding(rb, 'READER', reader_request, campaign.scratch)
                binding_path = str(reader_path) + '.binding';Path(binding_path).write_bytes(c.canonical(rb))
                campaign.charge(len(c.canonical(reader_request)) + len(c.canonical(rb)))
                argv = _sandbox_command(repo, campaign.scratch, output, True,
                    ['/usr/bin/python3', '-m', 'adapter.qualification_a15.reader', binding_path,
                     str(campaign.scratch), c.raw_hash(c.canonical(rb))])
                readout, reader_exit = launch_child(campaign, argv, seed)
                c.require(reader_exit['started_ns'] > writer_exit['exit_observed_ns'], 'READER_BEFORE_WRITER_EXIT')
                reader_result = c.parse(readout);c.validate(reader_result, 'READER_RESULT')
                c.require(reader_result['payload']['request_identity'] == reader_request['identity'], 'UNBOUND_READER_RESULT')
                readers.append(reader_result)
            results.append({'worker': worker_result, 'readers': readers})
        return c.record('SUPERVISOR_RESULT', {'request_identity': request['identity'], 'variant_results': results})
    except (c.ProtocolError, OSError, ValueError) as exc:
        campaign.fail_closed(type(exc).__name__, str(exc))

def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    c.require(len(argv) == 2, 'EXACT_SUPERVISOR_ARGUMENTS_REQUIRED')
    manifest = c.read_exact(argv[0]);c.require(c.raw_hash(c.canonical(manifest)) == argv[1], 'MANIFEST_BYTES_MISMATCH')
    c.keys(manifest, {'schema', 'scratch', 'repo', 'request', 'bindings', 'proof_path', 'code_hashes', 'probe_output'})
    c.require(manifest['schema'] == 'A15-FAKE-SUPERVISOR-INVOCATION-1', 'WRONG_SUPERVISOR_INVOCATION')
    proof = c.read_exact(manifest['proof_path']);c.authorize_proof(proof)
    observations = []
    campaign = Campaign(manifest['scratch'], observations.append)
    verify_environment(campaign, manifest['repo'], manifest['probe_output'], manifest['code_hashes'])
    result = run_supervisor(manifest['request'], manifest['bindings'], campaign,
                            manifest['repo'], lambda request: c.authorize_proof(proof))
    print(c.canonical({'semantic_result': result, 'observations': observations,
                      'launches': campaign.launches, 'written': campaign.written}).decode())
    return 0

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (c.ProtocolError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)
