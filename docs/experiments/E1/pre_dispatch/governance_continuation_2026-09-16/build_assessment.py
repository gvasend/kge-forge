"""Non-activating continuation construction and current pre-dispatch assessment."""
from pathlib import Path
from dataclasses import replace
import datetime, fcntl, hashlib, json, os, stat, subprocess, sys, uuid
ROOT = Path('/home/gvasend/app/kge-forge'); sys.path.insert(0, str(ROOT))
from adapter.tests.test_governance_continuation import construct, write
from adapter.context_projection import sha, digest, canonical, derive
from adapter.context_binding import CommittedContext
from adapter.governance_continuation import reference, verify_authorization
from adapter.governed_host import WorkAuthorization, GovernedHost
from adapter.orchestrator import ReasoningOrchestrator
from adapter.responses_orchestrator import ResponsesReasoning
from adapter.runnable_profile import validate, ARGV, INPUTS, build_acceptance
from adapter.model_transport import validate as validate_transport
from adapter.directory_provisioning import open_directory
from adapter.launch_profile import provisioning
from adapter.directory_provisioning import SOURCE
from adapter.invocation_ownership import InvocationOwnership
from adapter.recovery_ledger import _observe, CGROUP_BASE, SUPERVISOR_AUDIT
import tempfile

PRE = ROOT / 'docs/experiments/E1/pre_dispatch'
OUT = PRE / 'governance_continuation_2026-09-16'
R6 = PRE / 'pd06_context_separation'
RUN = OUT / 'production_final'
def load(p): return json.loads(Path(p).read_bytes())

released = load(R6 / 'CAPTURE_REFERENCE.json')
basis_path = Path(released['manifest']); basis = load(basis_path)
assert sha(basis_path.read_bytes()) == released['sha256']
profile = load(R6 / 'PRODUCTION_PROFILE.json'); launch = load(R6 / 'PRODUCTION_LAUNCH_RECORD.json')
assert digest(profile) == released['production_profile_sha256'] == launch['profile_sha256']
assert load(OUT / 'synthetic/REPORT.json')['result'] == 'PASS'
assert load(OUT / 'live_host/LIVE_REPORT.json')['result'] == 'PASS'
assert (OUT / 'FOCUSED_TESTS_FINAL.txt').read_text().rstrip().endswith('OK')

# Pin all current controller modules, including the newly introduced mechanism.
# These are an explicit implementation supplement, not governance continuations.
implementation = {}
for path in sorted((ROOT / 'adapter').glob('*.py')):
    implementation[str(path)] = {'previous_sha256': basis['current_inputs'].get(str(path), {}).get('sha256'),
                                'sha256': sha(path.read_bytes())}
RUN.mkdir(exist_ok=False)
# Preserve the already-created decision and continuation chain exactly. A final
# code-review change gets a new implementation supplement, not a rewritten chain.
gov = load(OUT / 'production/GOVERNANCE_SPECIFICATION.json')
gov['implementation_supplement'] = write(RUN / 'IMPLEMENTATION_SUPPLEMENT.json', {
    'authority_source': reference(OUT / 'AUTHORITY.md'), 'inputs': implementation,
    'reason': 'Final qualified continuation implementation, including explicit denial of activation without a separately bound Architect dispatch decision'})
gov['implementation_paths'] = sorted(implementation)
write(RUN / 'GOVERNANCE_SPECIFICATION.json', gov)
b = CommittedContext(PRE / 'CONTEXT_MANIFEST.json', profile['capture_commit'], gov)
assert b.verify()
result = derive(profile['context_projection'], b)
historical_projection = load(R6 / 'MODEL_CONTEXT_PROJECTION.json')
assert result['projection']['payload'] == historical_projection['payload']
assert result['ModelProjectionDigest'] != released['context_identities']['ModelProjectionDigest']
identity = {'authorization_id': 'auth-e1-wp-001-r7-' + uuid.uuid4().hex, 'revision': 7,
            'session_id': 'session-e1-' + uuid.uuid4().hex, 'turn_id': 'turn-e1-' + uuid.uuid4().hex}
op = {'schema': 1, 'governance': gov, 'released_launch': reference(R6 / 'PRODUCTION_LAUNCH_RECORD.json'),
      'invocation_identity': identity,
      'context_identities': {k: result[k] for k in ('AuthoritativeContextId', 'FullContextDigest', 'ModelProjectionDigest')}}
write(RUN / 'OPERATIONAL_BINDING.json', op)
write(RUN / 'AUTHORITATIVE_OPERATIONAL_CONTEXT.json', result['controller_context'])
write(RUN / 'MODEL_CONTEXT_PROJECTION.json', result['projection'])
raw = dict(launch['authorization']); raw.update(identity)
raw['context_binding'] = b; raw['operational_binding'] = canonical(op)
for key in ('read_roots', 'write_roots', 'deny_roots', 'exec_bins', 'read_deny_roots', 'write_deny_roots', 'write_directory_roots'):
    raw[key] = tuple(raw[key])
raw['exec_argv_allowlist'] = tuple(tuple(row) for row in raw['exec_argv_allowlist'])
auth = WorkAuthorization(**raw); assert auth.state == 'INACTIVE'
verify_authorization(auth)
audit = Path(profile['audit']['path_rule'].format(**auth.__dict__))
parent = audit.parent
missing = []
while not parent.exists(): missing.append(parent); parent = parent.parent
for parent in reversed(missing): parent.mkdir(mode=0o700)
host = GovernedHost(auth, audit); runner = ResponsesReasoning(ReasoningOrchestrator(host))
assert runner._verify_context() == historical_projection['payload']
# Reconstruction uses the issued operational supplement, not a rewritten release.
fresh = CommittedContext(b.path, b.capture_commit, gov)
restored = GovernedHost(replace(auth, context_binding=fresh), audit)
resumed = ResponsesReasoning(ReasoningOrchestrator(restored))
assert resumed.projection.verify()['ModelProjectionDigest'] == result['ModelProjectionDigest']
try: runner.run(result['projection']['payload']['task'], result['projection']['payload']['context'], 1)
except ValueError as exc: assert str(exc) == 'Programmer authorization not released'
else: raise AssertionError('inactive invocation became effective')
assert not host.invocations and host.scope is None

validate(profile['runtime'], ARGV, str(ROOT), list(INPUTS))
validate_transport(profile['model_transport'], profile['model_transport']['endpoint'], profile['model_transport']['model'])
receipt = load(PRE / 'pd06_release_evidence/provisioning/RECEIPT.json')
assert provisioning(b, receipt, (SOURCE,))['ready']
directories = {}
for row in profile['provisioning_plan']['directories']:
    fd = open_directory(row['path']); st = os.fstat(fd); os.close(fd)
    directories[row['path']] = {'device': st.st_dev, 'inode': st.st_ino, 'entries': sorted(p.name for p in Path(row['path']).iterdir())}
for rel in ('src/kge_forge/context', 'tests/context', 'docs/implementation'):
    assert directories[str(ROOT / rel)]['entries'] == []
assert not (ROOT / 'src/kge_forge/__init__.py').exists()
# The acceptance snapshot intentionally retains the exact released committed
# inputs. The LOCAL_ONLY continuation governs the controller, not new test inputs.
with tempfile.TemporaryDirectory(prefix='e1-continuation-acceptance-check-') as tmp:
    acceptance = build_acceptance(profile['runtime'], Path(tmp), gov)
    for source in acceptance['sources']:
        assert sha((Path(tmp) / source['snapshot_path']).read_bytes()) == source['sha256']
write(RUN / 'ACCEPTANCE_VERIFICATION.json', acceptance)

ledger = Path(profile['ownership']['ledger'])
assert str(ledger) == '/tmp/kge-forge-e1-invocations.jsonl' == launch['ownership']['ledger']
owners = {}
for path in (ledger, OUT / 'live/ownership.jsonl', OUT / 'live_host/ownership.jsonl'):
    fd = os.open(str(path), os.O_RDONLY | os.O_NOFOLLOW)
    try:
        fcntl.flock(fd, fcntl.LOCK_SH)
        owners[str(path)] = InvocationOwnership.__new__(InvocationOwnership)._history(fd)
        assert owners[str(path)] is None
    finally: os.close(fd)
scopes = {p.name: _observe(p) for p in CGROUP_BASE.iterdir() if p.is_dir() and p.name.startswith('scope-')}
assert all(not r['members'] and r['populated'] == 0 for r in scopes.values())
events = [json.loads(line) for line in SUPERVISOR_AUDIT.read_text().splitlines()]
created = {r['scope_id'] for r in events if r.get('event') == 'scope_created'}
closed = {r['scope_id'] for r in events if r.get('event') == 'scope_closed'}
assert created <= closed
assert not any(any(str(v).startswith('auth-e1-') for v in r.get('owner', [])) for r in events if r.get('event') == 'scope_created')
for audit_path in (Path(launch['audit_destination']), audit):
    ae = [json.loads(line) for line in audit_path.read_text().splitlines()]
    assert not any(r.get('event') == 'action_request' for r in ae)
    assert audit_path.stat().st_mode & 0o777 == 0o600
    for grant in auth.read_roots + auth.write_roots:
        assert Path(grant) != audit_path and Path(grant) not in audit_path.parents
    parent = audit_path.parent
    while parent != Path('/tmp'):
        assert not parent.is_symlink() and parent.stat().st_mode & 0o777 == 0o700
        parent = parent.parent

# Fresh read-only host identity and authority observation (no payload/process creation).
proc = Path('/proc/57950')
supervisor = {'pid': 57950, 'cmdline': (proc / 'cmdline').read_bytes().replace(b'\0', b' ').decode().strip(),
    'exe': os.readlink(str(proc / 'exe')), 'exe_sha256': sha((proc / 'exe').read_bytes()),
    'cwd': os.readlink(str(proc / 'cwd')), 'cgroup': (proc / 'cgroup').read_text(),
    'status': [line for line in (proc / 'status').read_text().splitlines() if line.startswith(('Uid:', 'Gid:', 'CapEff:', 'NoNewPrivs:'))],
    'delegation_writable': os.access(str(CGROUP_BASE), os.W_OK),
    'socket_mode': oct(Path('/tmp/a21m.sock').stat().st_mode & 0o777),
    'socket_is_socket': stat.S_ISSOCK(Path('/tmp/a21m.sock').stat().st_mode)}
historical_host = load(PRE / 'pd05_final_evidence/HOST_RECEIPT.json')['supervisor'][0]
assert supervisor['cmdline'] == historical_host['argv'] and supervisor['exe_sha256'] == historical_host['exe_sha256']
assert supervisor['cwd'] == str(ROOT) and supervisor['delegation_writable'] and supervisor['socket_is_socket']
assert supervisor['socket_mode'] == '0o600' and '0::/kge-forge/executor' in supervisor['cgroup']

# Account for every changed release-capture input. No automatic baseline rewrite.
differences = []
for path, expected in basis['current_inputs'].items():
    data = Path(path).read_bytes(); old = (basis_path.parent / 'blobs' / expected['sha256']).read_bytes()
    assert sha(old) == expected['sha256']
    if sha(data) == expected['sha256']: continue
    if path == str(PRE / 'DECISIONS.md'):
        category = 'AUTHORIZED_LOCAL_ONLY_GOVERNANCE_CONTINUATION'; assert data.startswith(old)
    elif path in implementation:
        category = 'AUTHORIZED_QUALIFIED_CONTROLLER_IMPLEMENTATION_SUPPLEMENT'
    elif path == str(SUPERVISOR_AUDIT):
        category = 'SYNTHETIC_QUALIFICATION_AUDIT_APPEND'; assert data.startswith(old)
        allowed = set(load(OUT / 'live_host/LIVE_REPORT.json')['scope_ids']) | {load(OUT / 'live/RECONCILIATION.json')['reservation']['scope_id']}
        assert all(json.loads(line).get('scope_id') in allowed for line in data[len(old):].decode().splitlines())
    else: raise AssertionError('unexplained post-basis change: ' + path)
    differences.append({'path': path, 'previous_sha256': expected['sha256'], 'current_sha256': sha(data), 'classification': category})
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=str(ROOT), text=True).strip()
assert head == basis['current_Forge_HEAD']
working = subprocess.check_output(['git', 'status', '--porcelain=v1'], cwd=str(ROOT), text=True)
source_identity = {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in sorted((ROOT / 'adapter').rglob('*.py'))}
write(OUT / 'SOURCE_SHA256_FINAL.json', source_identity)
clearance = load(Path(profile['context_projection']['clearance_path']))
assert clearance['counts'] == {'TRANSMIT': 6, 'LOCAL_ONLY': 120, 'NEVER_TRANSMIT': 60}
assessment = {'result': 'PASS / READY_FOR_ARCHITECT_DISPATCH_DECISION',
    'observed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    **gov['identities'], **op['context_identities'], 'released_profile_sha256': digest(profile),
    'released_capture_sha256': released['sha256'], 'release_decision_classification': 'NON_MATERIAL_TO_RELEASE_AUTHORITY',
    'classification_reason': 'Only the exact existing release entry was appended. Task, grants, cleared bytes, requirements/architecture, acceptance inputs, destinations and trust selections are unchanged.',
    'released_model_payload_byte_identical': True, 'clearance_counts_unchanged': clearance['counts'],
    'post_basis_changes': differences, 'new_implementation_inputs': [p for p, r in implementation.items() if r['previous_sha256'] is None],
    'Forge_HEAD': head, 'working_tree_clean': not working, 'working_tree_porcelain': working,
    'working_tree_disposition': 'Released implementation was explicitly HEAD plus source fingerprints. Same HEAD; qualified current module/test fingerprints and authorized evidence supplement recorded, not falsely reported as committed or clean.',
    'directories': directories, 'acceptance_sources': acceptance['sources'],
    'host': supervisor, 'ownership': {'reservations': owners, 'unclosed_scopes': sorted(created-closed), 'scopes': scopes,
        'pending_E1_action_results': [], 'common_ledger': str(ledger), 'rule': profile['ownership']['rule'],
        'note': 'Read-only observation; no E1 reservation acquired. The unchanged flock/reserve path arbitrates later concurrent controllers.'},
    'checks': {k: 'PASS' for k in ('release_basis_integrity', 'decision_attribution', 'append_chain_reconstruction',
        'current_governing_sources', 'cleared_projection_reconstruction', 'released_profile_unchanged', 'released_launch_unchanged',
        'runtime_executables_environment_network', 'model_transport_configuration', 'provisioning', 'committed_acceptance_snapshot',
        'supervisor_host_authority', 'ownership_and_quiescence', 'no_pending_E1_ActionResult', 'audit_isolation',
        'inactive_reconstruction', 'no_E1_execution', 'post_basis_change_attribution')},
    'states': {'PD06': 'RELEASED', 'E1_B01': 'PASS', 'ACTIVATION_READY': True, 'E1': 'INACTIVE',
        'eligibility_assessment': 'READY_FOR_ARCHITECT_DISPATCH_DECISION', 'ELIGIBLE': False,
        'DISPATCH_AUTHORIZED': False, 'DISPATCHED': False},
    'proposed_dispatch_bindings': {**identity, 'work_id': 'E1-WP-001', 'baseline': 'E1-ARCH-1',
        **gov['identities'], **op['context_identities'], 'released_profile_sha256': digest(profile),
        'operational_binding_sha256': digest(op), 'production_task_sha256': profile['production_task_sha256'],
        'audit': str(audit), 'ownership_ledger': str(ledger), 'status': 'PROPOSED_ONLY_NO_ARCHITECT_DISPATCH_RECORD'},
    'anomalies': ['Initial sandbox-blocked synthetic bridge attempt retained INDETERMINATE outcome; exact empty scope subsequently registered/closed and reservation released. See live/RECONCILIATION.json. No E1 scope involved.'],
    'limits': ['Existing release limitations retained.', 'No real model API call or credential read.',
        'Inactivity preserved; activation and eligibility still require separate Architect dispatch authorization.',
        'Controller-trusted issued specification pins the approved chain; read-only artifacts are not privileged WORM.',
        'Acceptance payload remains the exact released committed baseline; operational governance and projection provenance stay controller-local.']}
write(OUT / 'PRE_DISPATCH_ASSESSMENT_FINAL.json', assessment)
print(json.dumps({k: assessment[k] for k in ('result', 'ReleaseBasisId', 'ReleaseDecisionId', 'OperationalContextId',
    'continuation_chain_digest', 'FullContextDigest', 'ModelProjectionDigest', 'released_profile_sha256')}, indent=2))
