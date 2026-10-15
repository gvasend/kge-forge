"""Command-specific bootstrap consumption core. Import has no side effects.

Only INERT mode exists. Documentary construction authority is not probe authority.
The file/directory barriers establish their observed layers, not power-loss proof.
"""
import fcntl
import hashlib
import json
import os
import pathlib
import stat
import time

REAL_PROBE_BINDING = None
SYSTEMD_EXECUTION = SUDO_EXECUTION = BWRAP_EXECUTION = False
H77_02_EXECUTION = A15_EXECUTION = False
ROOT = pathlib.Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / 'docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1'
GRANT_SHA = '38120e22ad910456ccc4096d59b619fa79efcd6903d3d769c9524495c8c88165'
SUBJECT_SHA = '596a92d446ae2f4b8de57f02b977302577845586c2a45f40d01479e9827a2b3d'
SUBJECT_RAW = '1db52295406a68d938bb4d4e38b059dd774dcf08903782c411813f0a8363d69e'
CHARTER_SHA = 'd26962c58f17281173e965433dae63a941e078115f3dcc30e2a3512fa21812b8'
ISSUER = 'KGE-FORGE-PROJECT-OWNER-QUALIFICATION-GOVERNING-AUTHORITY'
SOURCE_PATHS = ['adapter/qualification_bootstrap/systemd_pids_once.py',
                'adapter/tests/test_systemd_pids_bootstrap.py']
LIMITS = {'MAX_LIVE_CHILDREN': 2, 'MAX_CHILD_LAUNCHES': 16,
          'CHILD_CPU_SECONDS': 5, 'CHILD_WALL_SECONDS': 10,
          'CHILD_ADDRESS_SPACE_BYTES': 134217728, 'CHILD_FILE_BYTES': 65536,
          'CHILD_FDS': 32, 'CAMPAIGN_WALL_SECONDS': 30,
          'CAMPAIGN_WRITTEN_BYTES': 1048576, 'AUTOMATIC_RETRIES': 0}
TEST_IDS = ['B89-' + name for name in (
    'COMMAND_REJECTION', 'GRANT_REJECTION', 'FIRST_CONSUMPTION',
    'DUPLICATE_CONSUMPTION', 'CONCURRENT_CLAIMS', 'PARTIAL_RECORD',
    'CRASH_BEFORE_LAUNCH', 'CRASH_AFTER_CONSUMPTION', 'LAUNCH_FAILURE',
    'UNKNOWN_COMPLETION', 'AUDIT_FAILURE', 'REVOCATION', 'RESOURCE_MISMATCH',
    'ZERO_RETRIES')]
ENTRY_PROOFS = ('TEST_PHASE_AUTHORIZED', 'EXACT_TEST_SET', 'SYNTHETIC_FIXTURES',
                'INDEPENDENT_EXPECTED_OUTPUTS', 'EXECUTABLE_IDENTITIES',
                'STORE_PERMISSIONS', 'DURABILITY_CONTROLS', 'RESOURCE_ENFORCEMENT',
                'OBSERVER_BOUNDARY', 'CAMPAIGN_ENTRY', 'NO_REAL_PROBE_PATH')
_SECRET = object()


class BootstrapError(RuntimeError):
    def __init__(self, code, first=None, secondary=()):
        super().__init__(code)
        self.code, self.first, self.secondary = code, first, tuple(secondary)


def require(condition, code):
    if not condition:
        raise BootstrapError(code)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False, allow_nan=False).encode('utf-8')


def identity(value, namespace):
    return {'kind': 'CONTENT_IDENTITY', 'namespace': namespace,
            'sha256': hashlib.sha256(canonical(value)).hexdigest()}


def check_identity(value, synthetic=False):
    require(isinstance(value, dict) and set(value) == {'kind', 'namespace', 'sha256'}, 'IDENTITY_FIELDS')
    require(value['kind'] == 'CONTENT_IDENTITY' and isinstance(value['namespace'], str), 'IDENTITY_DOMAIN')
    require(isinstance(value['sha256'], str) and len(value['sha256']) == 64 and
            all(c in '0123456789abcdef' for c in value['sha256']), 'IDENTITY_HASH')
    if synthetic:
        require(value['namespace'].startswith('bootstrap-inert-'), 'REAL_IDENTITY_IN_INERT_MODE')


def owned_directory(path):
    path = pathlib.Path(path)
    require(path.is_absolute() and path.resolve() == path, 'DIRECTORY_ESCAPE')
    fd = os.open(str(path), os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        info = os.fstat(fd)
        require(info.st_uid == os.geteuid() and stat.S_IMODE(info.st_mode) == 0o700, 'DIRECTORY_OWNER_MODE')
        return fd
    except BaseException:
        os.close(fd)
        raise


def read_at(directory, name):
    require(isinstance(name, str) and '/' not in name and name not in ('', '.', '..'), 'RECORD_NAME')
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory)
    try:
        info = os.fstat(fd)
        require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_uid == os.geteuid()
                and stat.S_IMODE(info.st_mode) == 0o600 and info.st_size <= ORDINARY_RECORD_MAX_BYTES, 'RECORD_OWNER_SHAPE')
        chunks = []; remaining = ORDINARY_RECORD_MAX_BYTES + 1
        while remaining:
            part = os.read(fd, min(4096, remaining))
            if not part: break
            chunks.append(part); remaining -= len(part)
        raw = b''.join(chunks)
        require(len(raw) <= ORDINARY_RECORD_MAX_BYTES, 'RECORD_SIZE')
        return raw, info
    finally:
        os.close(fd)


def read_pin(pin, private=True):
    require(set(pin) == {'path', 'raw_sha256'}, 'PIN_FIELDS')
    path = pathlib.Path(pin['path'])
    require(path.is_absolute() and path.resolve() == path, 'PIN_PATH')
    if private:
        directory = owned_directory(path.parent)
        try: raw, unused = read_at(directory, path.name)
        finally: os.close(directory)
    else:
        require(path.is_file() and not path.is_symlink(), 'DOCUMENTARY_PIN_PATH')
        raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == pin['raw_sha256'], 'PIN_MISMATCH')
    return json.loads(raw)


def verify_construction_authority():
    base = EVIDENCE / 'bootstrap-grant-issuance-90'
    ref = json.loads((base / 'effective-bootstrap-construction-grant-reference.json').read_text())
    require(ref['BOOTSTRAP_GRANT_EFFECTIVE'] is True and ref['GRANT_IDENTITY']['sha256'] == GRANT_SHA,
            'CONSTRUCTION_GRANT_NOT_EFFECTIVE')
    raw = (ROOT / ref['GRANT_RECORD_PIN']['path']).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == ref['GRANT_RECORD_PIN']['raw_sha256'], 'CONSTRUCTION_RECORD_PIN')
    envelope = json.loads(raw); record = envelope['RECORD']
    require(identity(record, envelope['GRANT_IDENTITY']['namespace']) == envelope['GRANT_IDENTITY']
            and envelope['GRANT_IDENTITY'] == ref['GRANT_IDENTITY'], 'CONSTRUCTION_GRANT_IDENTITY')
    subject = EVIDENCE / 'bootstrap-trust-authority-89/proposed-construction-test-authority-subject.json'
    require(hashlib.sha256(subject.read_bytes()).hexdigest() == SUBJECT_RAW and
            record['APPROVED_SUBJECT_IDENTITY']['sha256'] == SUBJECT_SHA, 'CONSTRUCTION_SUBJECT')
    require(record['ISSUER_ROLE'] == ISSUER and record['GOVERNING_CHARTER_IDENTITY']['sha256'] == CHARTER_SHA
            and record['PERMITTED_SOURCE_FILES'] == SOURCE_PATHS and record['PERMITTED_INERT_TESTS'] == TEST_IDS
            and record['RESOURCE_LIMITS'] == LIMITS and record['TARGET_COMMAND_EXECUTION_PERMITTED'] is False,
            'CONSTRUCTION_SCOPE')
    for pin in ref['VERIFICATION_PINS']:
        require(hashlib.sha256((ROOT / pin['path']).read_bytes()).hexdigest() == pin['raw_sha256'], 'ISSUANCE_CHECK_PIN')
    return record


class CampaignPermit:
    """Minted only from an independently owned, pinned qualified entry manifest."""
    def __init__(self, token, manifest):
        require(token is _SECRET, 'NO_VERIFIED_CAMPAIGN_PERMIT')
        self.manifest = manifest
        self.root = pathlib.Path(manifest['root'])
        self.budget = self.root / 'budget.json'

    def check(self):
        verify_repair_authority()
        verify_entry_repair_reference(self.manifest)
        require(self.manifest['grant_sha'] == GRANT_SHA, 'PERMIT_GRANT')
        for p in self.manifest['proof_pins'].values():
            receipt = read_pin(p)
            require(receipt['result'] == 'PASS' and receipt['campaign_identity'] == self.manifest['campaign_identity'],
                    'ENTRY_PROOF_CHANGED')

    def charge(self, amount, critical=False):
        require(type(amount) is int and amount >= 0, 'BUDGET_AMOUNT')
        proof = read_pin(self.manifest['proof_pins']['RESOURCE_ENFORCEMENT'])
        reserve = proof.get('critical_evidence_reserve_bytes')
        critical_bound = proof.get('critical_write_envelope_bytes')
        require(type(reserve) is int and type(critical_bound) is int and
                0 < critical_bound <= reserve < LIMITS['CAMPAIGN_WRITTEN_BYTES'], 'CRITICAL_RESERVE_UNVERIFIED')
        directory = owned_directory(self.root)
        fd = os.open('budget.json', os.O_RDWR | os.O_NOFOLLOW, dir_fd=directory)
        causal = None
        try:
            fcntl.flock(fd, fcntl.LOCK_EX)
            info = os.fstat(fd)
            require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_uid == os.geteuid()
                    and stat.S_IMODE(info.st_mode) == 0o600 and info.st_size <= ORDINARY_RECORD_MAX_BYTES, 'BUDGET_OWNER_SHAPE')
            raw = os.read(fd, 65537); budget = json.loads(raw)
            require(budget['campaign_identity'] == self.manifest['campaign_identity'], 'BUDGET_BINDING')
            require(not budget['stopped'] and time.monotonic_ns() < budget['deadline_ns'], 'CAMPAIGN_STOPPED_OR_DEADLINE')
            next_value = dict(budget, written_bytes=budget['written_bytes'] + amount)
            # Charge the accounting rewrite as well; conservative, no refunds.
            for unused in range(8):
                encoded = canonical(next_value)
                charged = budget['written_bytes'] + amount + len(encoded)
                if next_value['written_bytes'] == charged: break
                next_value['written_bytes'] = charged
            else: raise BootstrapError('BUDGET_ENCODING')
            require(next_value['written_bytes'] <= LIMITS['CAMPAIGN_WRITTEN_BYTES'] - (0 if critical else reserve),
                    'OUTPUT_BUDGET_OR_CRITICAL_RESERVE')
            os.lseek(fd, 0, os.SEEK_SET); _write_all(fd, encoded); os.ftruncate(fd, len(encoded)); os.fsync(fd)
        except BaseException as error:
            causal = error
            raise
        finally:
            for handle in (fd, directory):
                try: os.close(handle)
                except OSError as later:
                    if causal is None: raise
                    try: causal.bootstrap_secondary = tuple(getattr(causal, 'bootstrap_secondary', ())) + ({'phase':'budget_close','type':type(later).__name__,'message':str(later)},)
                    except BaseException: pass

    def fixture(self, fixture_id):
        require(fixture_id in self.manifest['fixtures'], 'UNSEALED_FIXTURE')
        return self.manifest['fixtures'][fixture_id]


def authorize_campaign(entry_pin):
    verify_construction_authority()
    manifest = read_root_entry(entry_pin)
    require(set(manifest) == {'schema', 'identity', 'grant_sha', 'campaign_identity', 'root',
            'source_hashes', 'proof_pins', 'fixtures', 'limits', 'repair_reference'}, 'CAMPAIGN_ENTRY_FIELDS')
    body = dict(manifest); claimed = body.pop('identity')
    require(manifest['schema'] == ROOT_ENTRY_SCHEMA and
            claimed == identity(body, 'bootstrap-inert-campaign-entry-v2'), 'CAMPAIGN_ENTRY_IDENTITY')
    require(manifest['grant_sha'] == GRANT_SHA and manifest['limits'] == LIMITS and
            set(manifest['source_hashes']) == set(SOURCE_PATHS), 'CAMPAIGN_SCOPE')
    require(all(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == value
                for name, value in manifest['source_hashes'].items()), 'SOURCE_IDENTITY')
    require(set(manifest['proof_pins']) == set(ENTRY_PROOFS), 'INCOMPLETE_ENTRY_PROOFS')
    root = pathlib.Path(manifest['root']); allowed = EVIDENCE / 'bootstrap-trust-authority-89/future-inert-campaign'
    require(allowed in root.parents and root.resolve() == root and root.name.startswith('campaign-'), 'CAMPAIGN_ROOT_BOUNDARY')
    require(root.name == ROOT_ENTRY_DIRECTORY, 'ROOT_CAMPAIGN_IDENTITY')
    require(len(manifest['fixtures']) == 21, 'EXACT_VARIANT_SET')
    verify_entry_repair_reference(manifest)
    for fixture in manifest['fixtures'].values():
        for label in ('store_device', 'store_inode'):
            value = fixture['entry'][label]
            require(type(value) is int and 0 <= value <= (1 << 64) - 1, 'STORE_UINT64')
    fd = owned_directory(root); os.close(fd)
    for label, p in manifest['proof_pins'].items():
        receipt = read_pin(p)
        require(receipt['schema'] == 'BOOTSTRAP-INDEPENDENT-ENTRY-PROOF-1' and receipt['predicate'] == label
                and receipt['result'] == 'PASS' and receipt['campaign_identity'] == manifest['campaign_identity'],
                'UNQUALIFIED_ENTRY_PROOF')
    return CampaignPermit(_SECRET, manifest)


ROOT_ENTRY_MAX_BYTES = 207444
ORDINARY_RECORD_MAX_BYTES = 65536
ROOT_ENTRY_SCHEMA = 'BOOTSTRAP-INERT-ENTRY-93-V2'
MAX_JSON_DEPTH = 10
MAX_JSON_NODES = 6465
REPAIR_SUBJECT_SHA = '2c3da2af0e05904127e405bc498b350fc7ad04fb7d58746e7ac5d57e35510257'
REPAIR_GRANT_SHA = '8684cd1ca4c3ba06c3eb006b0435ddcac4565da31266684404c98b9d90dfc717'
REPAIR_REFERENCE_SHA = 'fc482311f2ebb57e12ef319382d58b539d1648338a0a83e5575c318d528de490'
ROOT_ENTRY_DIRECTORY = 'campaign-1b817d930557a993eda86b8f28f91a657900812b27a229d0294a13f9abf6f0e5'


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'DUPLICATE_JSON_KEY')
        result[key] = value
    return result


def _invalid_number(value):
    raise BootstrapError('UNSUPPORTED_JSON_NUMBER')


def decode_root_bytes(raw):
    """Byte bound and lexical allocation envelope precede any JSON parsing."""
    require(isinstance(raw, bytes) and len(raw) <= ROOT_ENTRY_MAX_BYTES, 'ROOT_ENTRY_SIZE')
    text = raw.decode('utf-8', errors='strict')
    depth = nodes = 0; quoted = escaped = atom = False
    for char in text:
        if quoted:
            if escaped: escaped = False
            elif char == '\\': escaped = True
            elif char == '"': quoted = False
            continue
        if char == '"': quoted = True; nodes += 1; atom = False
        elif char in '[{': depth += 1; nodes += 1; atom = False
        elif char in ']}': depth -= 1; atom = False
        elif char in ',:' or char.isspace(): atom = False
        elif not atom: nodes += 1; atom = True
        require(0 <= depth <= MAX_JSON_DEPTH and nodes <= MAX_JSON_NODES, 'ROOT_JSON_ENVELOPE')
    require(not quoted and not escaped and depth == 0, 'ROOT_JSON_INCOMPLETE')
    value = json.loads(text, object_pairs_hook=_unique_object,
                       parse_float=_invalid_number, parse_constant=_invalid_number)
    require(raw == canonical(value), 'ROOT_NOT_CANONICAL')
    def check_depth(item, level):
        require(level <= MAX_JSON_DEPTH, 'ROOT_JSON_DEPTH')
        if isinstance(item, dict):
            for child in item.values(): check_depth(child, level + 1)
        elif isinstance(item, list):
            for child in item: check_depth(child, level + 1)
    check_depth(value, 1)
    return value


def _document_hash(path):
    digest = hashlib.sha256()
    with pathlib.Path(path).open('rb') as stream:
        while True:
            part = stream.read(4096)
            if not part: break
            digest.update(part)
    return digest.hexdigest()


def verify_repair_authority():
    """Authenticate issued authority before granting a root-only read role."""
    verify_construction_authority()
    base = EVIDENCE / 'bootstrap-repair-grant-issuance-94'
    refpath = base / 'effective-bootstrap-repair-grant-reference.json'
    require(_document_hash(refpath) == REPAIR_REFERENCE_SHA, 'REPAIR_REFERENCE_PIN')
    ref = json.loads(refpath.read_text())
    require(ref['REPAIR_GRANT_EFFECTIVE'] is True and ref['REPAIR_PHASE_PERMITTED'] is True,
            'REPAIR_NOT_EFFECTIVE')
    require(ref['GRANT_IDENTITY']['sha256'] == REPAIR_GRANT_SHA and
            ref['APPROVED_SUBJECT_IDENTITY']['sha256'] == REPAIR_SUBJECT_SHA, 'REPAIR_AUTHORITY_IDENTITY')
    record_path = ROOT / ref['GRANT_RECORD_PIN']['path']
    require(_document_hash(record_path) == ref['GRANT_RECORD_PIN']['raw_sha256'], 'REPAIR_RECORD_PIN')
    envelope = json.loads(record_path.read_text()); body = envelope['CONTENT']
    require(identity(body, envelope['IDENTITY']['namespace']) == envelope['IDENTITY'] == ref['GRANT_IDENTITY'],
            'REPAIR_CONTENT_IDENTITY')
    require(body['ISSUER_ROLE'] == ISSUER and body['GOVERNING_CHARTER_IDENTITY']['sha256'] == CHARTER_SHA
            and body['EXACT_SOURCE_ALLOWLIST'] == SOURCE_PATHS and body['RESOURCE_LIMITS'] == LIMITS
            and body['ROOT_ENTRY_MAX_BYTES'] == ROOT_ENTRY_MAX_BYTES
            and body['ORDINARY_RECORD_MAX_BYTES'] == ORDINARY_RECORD_MAX_BYTES
            and body['ROOT_ENTRY_SCHEMA'] == ROOT_ENTRY_SCHEMA and body['NO_RETRY_POLICY'] == 0
            and body['REAL_PROBE_GRANT'] is None and body['A15_EXECUTION_GRANT'] is None
            and body['A15_CAPTURE_GRANT'] is None, 'REPAIR_SCOPE')
    for p in ref['VERIFICATION_PINS']:
        require(_document_hash(ROOT / p['path']) == p['raw_sha256'], 'REPAIR_ISSUANCE_PIN')
    # Future campaign activation receipt must independently establish current
    # unrevoked combined authority; issuance snapshots cannot assert freshness.
    return ref


def read_root_entry(entry_pin):
    """Fixed role/path/authority classification; no sender-selected size flag."""
    verify_repair_authority()  # Happens BEFORE the enlarged-size operation.
    require(set(entry_pin) == {'path', 'raw_sha256'}, 'ROOT_PIN_FIELDS')
    path = pathlib.Path(entry_pin['path'])
    expected = EVIDENCE / 'bootstrap-trust-authority-89/future-inert-campaign' / ROOT_ENTRY_DIRECTORY / 'entry.json'
    require(path.is_absolute() and path == expected and path.resolve() == path, 'ROOT_ROLE_PATH')
    directory = owned_directory(path.parent)
    fd = None; causal = None
    try:
        fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory)
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_uid == os.geteuid()
                and stat.S_IMODE(before.st_mode) == 0o600, 'ROOT_OWNER_SHAPE')
        require(before.st_size <= ROOT_ENTRY_MAX_BYTES, 'ROOT_ENTRY_SIZE')
        remaining = ROOT_ENTRY_MAX_BYTES + 1; parts = []
        while remaining:
            data = os.read(fd, min(4096, remaining))
            if not data: break
            parts.append(data); remaining -= len(data)
        raw = b''.join(parts)
        require(len(raw) <= ROOT_ENTRY_MAX_BYTES and len(raw) == before.st_size, 'ROOT_ENCODED_LENGTH')
        after = os.fstat(fd); alias = os.stat(path.name, dir_fd=directory, follow_symlinks=False)
        fingerprint = lambda value: (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns, value.st_ctime_ns)
        require(fingerprint(before) == fingerprint(after) == fingerprint(alias), 'ROOT_CHANGED_DURING_READ')
        require(hashlib.sha256(raw).hexdigest() == entry_pin['raw_sha256'], 'ROOT_RAW_PIN')
        manifest = decode_root_bytes(raw)
        require(isinstance(manifest, dict) and manifest.get('schema') == ROOT_ENTRY_SCHEMA, 'ROOT_ENTRY_TYPE')
        return manifest
    except BaseException as error:
        causal = error
        raise
    finally:
        for handle in (fd, directory):
            if handle is not None:
                try: os.close(handle)
                except OSError as error:
                    if causal is None: raise
                    try: causal.bootstrap_secondary = tuple(getattr(causal, 'bootstrap_secondary', ())) + ({'phase': 'root_close', 'type': type(error).__name__, 'message': str(error)},)
                    except BaseException: pass

def verify_entry_repair_reference(manifest):
    ref = manifest['repair_reference']
    require(set(ref) == {'approved_subject_identity', 'effective_reference_pin'}, 'ENTRY_REPAIR_FIELDS')
    require(ref['approved_subject_identity'] == {'kind': 'CONTENT_IDENTITY',
            'namespace': 'qualification-bootstrap-entry-oracle-repair-subject-v1',
            'sha256': REPAIR_SUBJECT_SHA}, 'ENTRY_REPAIR_SUBJECT')
    p = ref['effective_reference_pin']
    require(p['path'] == str(pathlib.Path(manifest['root']) / 'proofs/effective-repair-authority.json'),
            'ENTRY_REPAIR_PIN_PATH')
    copied = read_pin(p)
    original = verify_repair_authority()
    require(copied == original, 'ENTRY_REPAIR_REFERENCE_SUBSTITUTION')
    epoch = read_pin(manifest['proof_pins']['CAMPAIGN_ENTRY'])
    require(epoch.get('authority_currentness') == {'repair_grant_sha': REPAIR_GRANT_SHA,
            'base_grant_sha': GRANT_SHA, 'unrevoked': True, 'fresh': True, 'campaign_available': True},
            'AUTHORITY_CURRENTNESS_UNVERIFIED')


def consumption_key(grant, subject, retained, command, context):
    for item in (grant, subject, retained, command, context): check_identity(item, synthetic=True)
    fields = {'schema': 'SYSTEM-PIDS-SINGLE-ATTEMPT-KEY-1', 'issued_grant_identity': grant,
              'approved_probe_subject_identity': subject, 'retained_package86_subject_identity': retained,
              'exact_command_identity': command, 'qualified_execution_context_identity': context,
              'authorized_attempt_number': 1}
    return fields, identity(fields, 'qualification-h87-system-probe-consumption-key-v1')


def _write_all(fd, raw):
    offset = 0
    while offset < len(raw):
        n = os.write(fd, raw[offset:]); require(n > 0, 'SHORT_WRITE'); offset += n


def _publish(directory, name, value, permit, reserved=None, hook=None):
    raw = canonical(value); require(len(raw) <= ORDINARY_RECORD_MAX_BYTES, 'RECORD_BUDGET')
    critical = name == 'campaign-first-failure.json' or (value.get('schema') == 'BOOTSTRAP-AUDIT-1' and
                value.get('phase') == 'unknown' and name.endswith('.unknown.json'))
    permit.charge(len(raw), critical=critical)
    fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=directory)
    causal = None
    try:
        inode = os.fstat(fd).st_ino
        if reserved: reserved()
        if hook: hook('DURING_CLAIM')
        _write_all(fd, raw); os.fsync(fd)
    except BaseException as error:
        causal = error
        raise
    finally:
        try: os.close(fd)
        except OSError as cleanup:
            if causal is None: raise
            try: causal.bootstrap_secondary = ({'type': type(cleanup).__name__, 'message': str(cleanup)},)
            except BaseException: pass
    os.fsync(directory)
    return inode


def confirm_consumption(directory, name, expected, inode):
    """Separate readonly byte/inode/identity calculation, no launch capability."""
    raw, info = read_at(directory, name)
    require(info.st_ino == inode and raw == canonical(expected) and json.loads(raw) == expected,
            'INDEPENDENT_CONFIRMATION_FAILED')
    body = expected['content']
    require(expected['identity'] == identity(body, 'bootstrap-inert-consumption-record-v1'), 'CLAIM_CONTENT_IDENTITY')
    return expected['identity']


def _validate(entry, permit, directory, epoch):
    require(isinstance(permit, CampaignPermit), 'NO_VERIFIED_CAMPAIGN_PERMIT'); permit.check()
    require(set(entry) == {'schema', 'mode', 'fixture_id', 'test_id', 'grant', 'effective', 'context',
            'command', 'limits', 'store', 'store_device', 'store_inode', 'epoch_identity', 'attempt'}, 'ENTRY_FIELDS')
    require(entry['schema'] == 'BOOTSTRAP-INERT-REQUEST-1' and entry['mode'] == 'INERT', 'REAL_PROBE_DISABLED')
    require(entry['test_id'] in TEST_IDS and entry['attempt'] == 1 and type(entry['attempt']) is int, 'OPERATION_SCOPE')
    sealed = permit.fixture(entry['fixture_id'])
    require(entry == sealed['entry'], 'FIXTURE_BINDING')
    require(entry['command'] == {'operation': 'INERT_CALLBACK', 'argv': []} and entry['limits'] == LIMITS,
            'COMMAND_OR_RESOURCE_MISMATCH')
    grant = entry['grant']; body = grant['content']
    require(set(grant) == {'content', 'identity'} and grant['identity'] == identity(body, 'bootstrap-inert-grant-v1'), 'GRANT_IDENTITY')
    require(set(body) == {'schema', 'subject_identity', 'retained_identity', 'command_identity', 'context_identity',
                         'issuer', 'scope', 'limits', 'attempts', 'retries'} and body['schema'] == 'BOOTSTRAP-SYNTHETIC-GRANT-1'
            and body['issuer'] == 'SYNTHETIC_ONLY_NOT_PROJECT_AUTHORITY' and body['scope'] == 'INERT_CALLBACK'
            and body['limits'] == LIMITS and body['attempts'] == 1 and body['retries'] == 0, 'GRANT_SCOPE')
    for name in ('subject_identity', 'retained_identity', 'command_identity', 'context_identity'):
        check_identity(body[name], synthetic=True)
    require(body['command_identity'] == identity(entry['command'], 'bootstrap-inert-command-v1') and
            body['context_identity'] == identity(entry['context'], 'bootstrap-inert-context-v1'), 'COMMAND_OR_CONTEXT_IDENTITY')
    require(entry['effective'] == {'schema': 'BOOTSTRAP-SYNTHETIC-EFFECTIVE-1', 'grant_identity': grant['identity'],
                                  'effective': True}, 'EFFECTIVE_GRANT_IDENTITY')
    require(set(epoch) == {'schema', 'grant_identity', 'status', 'expiration_checked', 'freshness_verified'} and
            epoch['schema'] == 'BOOTSTRAP-INERT-EPOCH-1' and epoch['grant_identity'] == grant['identity'] and
            epoch['status'] == 'EFFECTIVE' and epoch['expiration_checked'] is True and epoch['freshness_verified'] is True
            and entry['epoch_identity'] == identity(epoch, 'bootstrap-inert-epoch-v1'), 'REVOKED_EXPIRED_OR_UNKNOWN')
    info = os.fstat(directory)
    require((info.st_dev, info.st_ino) == (entry['store_device'], entry['store_inode']), 'STORE_REPLACED')
    return consumption_key(grant['identity'], body['subject_identity'], body['retained_identity'],
                           body['command_identity'], body['context_identity'])


def consume_inert(entry, permit, callback, witness, fault=None):
    """One synchronous irreversible call; no exported or reusable launch token."""
    require(isinstance(entry, dict) and entry.get('mode') == 'INERT', 'REAL_PROBE_DISABLED')
    require(REAL_PROBE_BINDING is None, 'REAL_BINDING_MUST_STAY_DISABLED')
    require(isinstance(permit, CampaignPermit), 'NO_VERIFIED_CAMPAIGN_PERMIT')
    # Only the pinned approved test source may provide inert observer/callback code.
    approved_file = (ROOT / SOURCE_PATHS[1]).resolve()
    for function in (callback, witness) + ((fault,) if fault else ()):
        code = getattr(function, '__code__', None)
        require(callable(function) and code is not None and pathlib.Path(code.co_filename).resolve() == approved_file,
                'UNAPPROVED_INERT_FUNCTION')
    entry = json.loads(canonical(entry)); store = pathlib.Path(entry['store'])
    require(permit.root in store.parents and store.resolve() == store, 'STORE_BOUNDARY')
    directory = owned_directory(store); epochfd = None; claimed = False; key = None
    first = None; secondary = []; causal_exception = None
    def stage(point):
        witness('stage', {'point': point})
        if fault: fault(point)
    def mark_reserved():
        nonlocal claimed
        claimed = True
    def audit(phase, value):
        _publish(directory, key['sha256'] + '.' + phase + '.json',
                 {'schema': 'BOOTSTRAP-AUDIT-1', 'key': key, 'phase': phase, 'value': value}, permit)
    try:
        epochfd = os.open('epoch.json', os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory)
        fcntl.flock(epochfd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        raw, info = read_at(directory, 'epoch.json')
        require(info.st_ino == os.fstat(epochfd).st_ino, 'EPOCH_REPLACED')
        fields, key = _validate(entry, permit, directory, json.loads(raw))
        name = key['sha256'] + '.claim.json'
        stage('BEFORE_CLAIM')
        body = {'schema': 'BOOTSTRAP-CONSUMPTION-1', 'key': fields, 'state': 'CONSUMED'}
        record = {'content': body, 'identity': identity(body, 'bootstrap-inert-consumption-record-v1')}
        inode = _publish(directory, name, record, permit, reserved=mark_reserved, hook=stage)
        confirmed = confirm_consumption(directory, name, record, inode)
        stage('AFTER_CLAIM_BEFORE_LAUNCH')
        current, current_info = read_at(directory, 'epoch.json')
        require(current == raw and current_info.st_ino == info.st_ino, 'EPOCH_CHANGED')
        _validate(entry, permit, directory, json.loads(current))
        permit.charge(0)  # Fresh deadline/accounting check before one handoff.
        witness('consumption.confirmed', {'identity': confirmed, 'key': key})
        audit('consumed', {'identity': confirmed})
        # A single local capability is spent before callback entry and never returned.
        launch_available = True
        require(launch_available, 'CAPABILITY_SPENT'); launch_available = False
        audit('attempt', {'attempt': 1})
        stage('DURING_LAUNCH'); witness('callback.entry', {'attempt': 1, 'arguments': []})
        try: outcome = callback()
        except BaseException as original:
            try: witness('callback.exception', {'type': type(original).__name__, 'message': str(original)})
            except BaseException as error: secondary.append({'type': type(error).__name__, 'message': str(error)})
            raise
        witness('callback.return', {'value': outcome})
        stage('AFTER_LAUNCH_BEFORE_OBSERVATION')
        witness('completion.observed', {'value': outcome, 'synthetic': True})
        stage('AFTER_COMPLETION_BEFORE_AUDIT'); audit('completed', {'value': outcome})
        return {'schema': 'BOOTSTRAP-INERT-RESULT-1', 'key': key, 'consumption': confirmed,
                'consumed': True, 'outcome': outcome, 'retry_allowed': False}
    except BaseException as original:
        causal_exception = original
        first = {'type': type(original).__name__, 'message': str(original)}
        secondary.extend(getattr(original, 'bootstrap_secondary', ()))
        if claimed and key is not None:
            try: audit('unknown', {'state': 'CONSUMED_OUTCOME_UNKNOWN', 'first': first, 'retry_allowed': False})
            except BaseException as error: secondary.append({'type': type(error).__name__, 'message': str(error)})
        try: witness('first_failure', {'first': first, 'secondary': list(secondary), 'retry_allowed': False})
        except BaseException as error: secondary.append({'type': type(error).__name__, 'message': str(error)})
        # Preserve the original exception type/object; annotate secondary evidence.
        try: original.bootstrap_first = first; original.bootstrap_secondary = tuple(secondary)
        except BaseException: pass
        raise
    finally:
        # Cleanup failures cannot replace an active causal exception.
        for fd in (epochfd, directory):
            if fd is not None:
                try: os.close(fd)
                except OSError as error:
                    if first is None: raise
                    secondary.append({'type': type(error).__name__, 'message': str(error)})
        if causal_exception is not None:
            try: causal_exception.bootstrap_secondary = tuple(secondary)
            except BaseException: pass


def recover_inert(store, key_sha):
    require(isinstance(key_sha, str) and len(key_sha) == 64 and all(c in '0123456789abcdef' for c in key_sha), 'KEY_HASH')
    directory = owned_directory(store)
    try:
        try:
            raw, unused = read_at(directory, key_sha + '.claim.json'); value = json.loads(raw)
            body = value['content']
            require(value['identity'] == identity(body, 'bootstrap-inert-consumption-record-v1') and
                    body['state'] == 'CONSUMED' and
                    identity(body['key'], 'qualification-h87-system-probe-consumption-key-v1')['sha256'] == key_sha,
                    'RECOVERY_RECORD')
            state = 'CONSUMED'
        except (OSError, ValueError, KeyError, BootstrapError): state = 'OUTCOME_UNKNOWN'
        return {'state': state, 'launch_permitted': False, 'retry_allowed': False}
    finally: os.close(directory)
