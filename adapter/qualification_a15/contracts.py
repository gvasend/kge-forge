"""Closed fake-protocol contracts. Identity is data, never default authority."""
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

VERSION = 1
PHASE = 'FAKE_PROTOCOL'
GRANT_SHA = '25395fb3c06be58a8c538c618b9e50b9d118aa415d0843968254d3f8e83dd8fa'
SUBJECT_SHA = 'a2505f248e929f0226d20d813673faa87b8b09fa0e08b071e413d4d7779a9869'
GRANT_NAMESPACE = 'qualification-A15-implementation-test-issued-grant-v1'
SCOPE = 'KGE-FORGE-A15-SYNTHETIC-IMPLEMENTATION-QUALIFICATION'
LIMITS = {'live': 4, 'launches': 128, 'wall': 60, 'cpu': 30,
          'as': 1073741824, 'file': 16777216, 'fds': 64,
          'campaign_wall': 600, 'campaign_bytes': 67108864, 'retries': 0}
PAYLOADS = {
    'SUPERVISOR_REQUEST': {'case_id', 'variant_requests'},
    'WORKER_REQUEST': {'case_id', 'variant_id', 'initial_snapshot_identity',
                       'source_identity', 'operation'},
    'WORKER_RESULT': {'request_identity', 'published_output_identity', 'handoff_identity'},
    'PUBLISHED_OUTPUT': {'request_identity', 'initial_snapshot_identity',
                         'source_identity', 'event_identity', 'after_snapshot_identity',
                         'typed_state', 'proof_validation', 'proof_usability',
                         'target_satisfaction', 'admission_stale', 'control',
                         'resume', 'ordered_trace', 'protected_state'},
    'HANDOFF_RECORD': {'request_identity', 'published_output_identity',
                       'publication_bytes_sha256'},
    'READER_REQUEST': {'case_id', 'variant_id', 'published_output_identity',
                       'expected_output_identity', 'seed'},
    'READER_RESULT': {'request_identity', 'published_output_identity',
                      'expected_output_identity', 'matched'},
    'SUPERVISOR_RESULT': {'request_identity', 'variant_results'},
}
ROLES = {'SUPERVISOR_REQUEST': 'SUPERVISOR', 'SUPERVISOR_RESULT': 'SUPERVISOR',
         'WORKER_REQUEST': 'WORKER', 'WORKER_RESULT': 'WORKER',
         'PUBLISHED_OUTPUT': 'WORKER', 'HANDOFF_RECORD': 'WORKER',
         'READER_REQUEST': 'READER', 'READER_RESULT': 'READER'}
BINDING_KEYS = {'schema', 'role', 'request_identity', 'request_path',
                'fixture_path', 'expected_path', 'output_directory',
                'proof_path', 'code_hashes', 'fault', 'exit_evidence'}
FIXTURE_KEYS = {'schema', 'scope', 'variant_id', 'source_content',
                'source_identity', 'initial_state', 'initial_snapshot_identity'}
FAULTS = {'NONE', 'NONZERO', 'TIMEOUT', 'NO_PUBLICATION', 'BAD_HANDOFF'}

class ProtocolError(ValueError):
    pass

def require(value, message):
    if not value:
        raise ProtocolError(message)

def raw_hash(raw):
    return hashlib.sha256(raw).hexdigest()

def _value(value):
    if value is None or type(value) in (str, bool, int):
        return
    if type(value) is list:
        for item in value:
            _value(item)
        return
    if type(value) is dict and all(type(k) is str for k in value):
        for item in value.values():
            _value(item)
        return
    raise ProtocolError('NON_CANONICAL_JSON_TYPE')

def canonical(value):
    _value(value)
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False, allow_nan=False).encode('utf-8')

def parse(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'DUPLICATE_JSON_KEY')
            result[key] = value
        return result
    def reject(value):
        raise ProtocolError('NON_INTEGER_JSON_NUMBER')
    try:
        result = json.loads(raw, object_pairs_hook=pairs,
                            parse_float=reject, parse_constant=reject)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ProtocolError('INVALID_JSON') from exc
    _value(result)
    return result

def keys(value, exact):
    require(type(value) is dict and set(value) == set(exact), 'WRONG_FIELD_SET')

def identity(value, namespace):
    return {'kind': 'CONTENT_IDENTITY', 'namespace': namespace,
            'sha256': raw_hash(canonical(value))}

def validate_identity(value, namespace=None):
    keys(value, {'kind', 'namespace', 'sha256'})
    require(value['kind'] == 'CONTENT_IDENTITY' and type(value['namespace']) is str,
            'WRONG_IDENTITY_DOMAIN')
    require(type(value['sha256']) is str and re.fullmatch('[0-9a-f]{64}', value['sha256']),
            'WRONG_IDENTITY_HASH')
    if namespace:
        require(value['namespace'] == namespace, 'WRONG_IDENTITY_NAMESPACE')

def grant_identity():
    return {'kind': 'CONTENT_IDENTITY', 'namespace': GRANT_NAMESPACE, 'sha256': GRANT_SHA}

def record(kind, payload):
    require(kind in PAYLOADS, 'UNKNOWN_PROTOCOL_KIND')
    keys(payload, PAYLOADS[kind])
    body = {'schema': 'KGE-A15-' + kind + '-1', 'version': VERSION,
            'role': ROLES[kind], 'phase': PHASE,
            'grant_identity': grant_identity(), 'payload': payload}
    body['identity'] = identity(body, 'qualification-a15-protocol-' + kind.lower() + '-v1')
    return body

def validate(value, kind):
    require(kind in PAYLOADS, 'UNKNOWN_PROTOCOL_KIND')
    keys(value, {'schema', 'version', 'role', 'phase', 'grant_identity', 'payload', 'identity'})
    require(value['schema'] == 'KGE-A15-' + kind + '-1' and
            type(value['version']) is int and value['version'] == VERSION,
            'WRONG_SCHEMA_VERSION')
    require(value['role'] == ROLES[kind] and value['phase'] == PHASE,
            'WRONG_ROLE_PHASE')
    validate_identity(value['grant_identity'], GRANT_NAMESPACE)
    require(value['grant_identity'] == grant_identity(), 'WRONG_GRANT_IDENTITY')
    keys(value['payload'], PAYLOADS[kind])
    body = dict(value)
    supplied = body.pop('identity')
    require(supplied == identity(body, 'qualification-a15-protocol-' + kind.lower() + '-v1'),
            'PROTOCOL_IDENTITY_MISMATCH')
    _value(body)
    p = value['payload']
    for name in p:
        if name.endswith('_identity'):
            validate_identity(p[name])
    if kind == 'WORKER_REQUEST':
        require(p['operation'] == 'FAKE_RECORD_SAVE', 'UNAUTHORIZED_OPERATION')
        require(type(p['case_id']) is str and p['case_id'].startswith('T70-'), 'WRONG_CASE')
        require(p['variant_id'] in ('SYNTHETIC-ONE', 'SYNTHETIC-TWO'), 'WRONG_VARIANT')
        validate_identity(p['initial_snapshot_identity'], 'qualification-a15-fake-snapshot-v1')
        validate_identity(p['source_identity'], 'raw-file-sha256')
    if kind == 'READER_REQUEST':
        require(type(p['seed']) is int and p['seed'] in (0, 1, 7, 101), 'WRONG_READER_SEED')
    if kind == 'READER_RESULT':
        require(p['matched'] is True, 'READER_MISMATCH')
    if kind == 'PUBLISHED_OUTPUT':
        keys(p['resume'], {'allowed', 'actions', 'reasons', 'supporting_identities'})
    return value

def read_exact(path):
    path = Path(path)
    require(path.is_file() and not path.is_symlink(), 'MISSING_OR_SYMLINK_INPUT')
    raw = path.read_bytes()
    require(len(raw) <= 4194304, 'INPUT_TOO_LARGE')
    result = parse(raw)
    require(raw == canonical(result), 'NON_CANONICAL_INPUT')
    return result

def private_path(path, root):
    path, root = Path(path).absolute(), Path(root).absolute()
    require(root.name.startswith('kge-a15-harness-test-') and
            re.fullmatch('kge-a15-harness-test-[0-9a-f]{32}', root.name), 'WRONG_SCRATCH_ROOT')
    require(root.parent == Path('/tmp') and root.is_dir(), 'WRONG_SCRATCH_PARENT')
    require(path == root or root in path.parents, 'OUTSIDE_SCRATCH')
    for item in [path] + list(path.parents):
        require(not item.is_symlink(), 'SYMLINK_PATH')
    require(root.stat().st_uid == os.geteuid(), 'FOREIGN_SCRATCH_OWNER')
    return path

def publish(directory, name, value):
    directory = Path(directory)
    require(directory.is_dir() and not directory.is_symlink(), 'INVALID_OUTPUT_DIRECTORY')
    require(name in ('published-output.json', 'handoff.json'), 'UNAUTHORIZED_PUBLICATION_NAME')
    target = directory / name
    require(not target.exists() and not target.is_symlink(), 'IMMUTABLE_OUTPUT_CONFLICT')
    raw = canonical(value)
    require(len(raw) <= LIMITS['file'], 'PUBLICATION_TOO_LARGE')
    fd, temporary = tempfile.mkstemp(prefix='.fake-', dir=str(directory))
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, target)
        except FileExistsError as exc:
            raise ProtocolError('IMMUTABLE_OUTPUT_CONFLICT') from exc
    finally:
        os.unlink(temporary)
    require(target.read_bytes() == raw, 'PUBLICATION_BYTES_MISMATCH')
    return target

def compare_complete_output(actual, expected):
    validate(actual, 'PUBLISHED_OUTPUT')
    validate(expected, 'PUBLISHED_OUTPUT')
    require(canonical(actual) == canonical(expected), 'COMPLETE_OUTPUT_MISMATCH')

def validate_synthetic_input(fixture, request):
    keys(fixture, FIXTURE_KEYS)
    validate(request, 'WORKER_REQUEST')
    p = request['payload']
    require(fixture['schema'] == 'A15-FAKE-FIXTURE-1' and fixture['scope'] == SCOPE,
            'NON_FAKE_FIXTURE')
    require(fixture['variant_id'] == p['variant_id'], 'CROSS_VARIANT_INPUT')
    require(type(fixture['source_content']) is str and
            fixture['source_content'].startswith('SYNTHETIC-A15-TEST:'), 'NON_SYNTHETIC_SOURCE')
    source = {'kind': 'CONTENT_IDENTITY', 'namespace': 'raw-file-sha256',
              'sha256': raw_hash(fixture['source_content'].encode())}
    require(source == fixture['source_identity'] == p['source_identity'], 'SOURCE_IDENTITY_MISMATCH')
    keys(fixture['initial_state'], {'scope', 'support_current', 'protected'})
    require(fixture['initial_state']['scope'] == SCOPE and
            fixture['initial_state']['support_current'] is True, 'WRONG_INITIAL_STATE')
    initial = identity(fixture['initial_state'], 'qualification-a15-fake-snapshot-v1')
    require(initial == fixture['initial_snapshot_identity'] == p['initial_snapshot_identity'],
            'INITIAL_SNAPSHOT_IDENTITY_MISMATCH')
    return fixture

def validate_handoff(value, request, published, raw):
    validate(value, 'HANDOFF_RECORD')
    require(value['payload'] == {'request_identity': request['identity'],
            'published_output_identity': published['identity'],
            'publication_bytes_sha256': raw_hash(raw)}, 'HANDOFF_BINDING_MISMATCH')

def validate_binding(binding, role, request, root):
    keys(binding, BINDING_KEYS)
    require(binding['schema'] == 'A15-EXECUTION-BINDING-1' and binding['role'] == role,
            'WRONG_INVOCATION_BINDING')
    require(binding['request_identity'] == request['identity'], 'WRONG_BOUND_REQUEST')
    require(binding['fault'] in FAULTS, 'UNKNOWN_FAULT')
    for name in ['request_path', 'fixture_path', 'expected_path', 'proof_path', 'output_directory']:
        private_path(binding[name], root)
    exact_code = {'adapter/qualification_a15/' + n for n in ('__init__.py', 'contracts.py', 'supervisor.py', 'worker.py', 'reader.py')} | {'adapter/tests/test_qualification_a15_harness.py'}
    require(type(binding['code_hashes']) is dict and set(binding['code_hashes']) == exact_code, 'UNSEALED_CODE')
    for file, digest in binding['code_hashes'].items():
        validate_identity({'kind': 'CONTENT_IDENTITY', 'namespace': 'raw-file-sha256', 'sha256': digest})
        here = Path('/code') / file if Path('/code').exists() else Path(__file__).resolve().parents[2] / file
        require(here.is_file() and raw_hash(here.read_bytes()) == digest, 'CODE_SEAL_MISMATCH')
    require(Path(binding['output_directory']).parts[-3:] == ('outputs', request['payload']['case_id'], request['payload']['variant_id']), 'WRONG_VARIANT_OUTPUT_ROW')
    if role == 'READER':
        keys(binding['exit_evidence'], {'writer_exit_observed', 'writer_exit_code',
              'publication_verified', 'handoff_verified'})
        require(binding['exit_evidence'] == {'writer_exit_observed': True,
            'writer_exit_code': 0, 'publication_verified': True, 'handoff_verified': True},
            'READER_BEFORE_VERIFIED_WRITER_EXIT')
    else:
        require(binding['exit_evidence'] is None, 'WORKER_CANNOT_ASSERT_EXIT')

def authorize_proof(proof):
    """Hash-bound readonly proof supplied by independently authenticated controller.
    Live revocation/freshness and enforcement are controller duties, not a wire flag.
    """
    keys(proof, {'grant', 'effective_reference', 'owner_decision', 'approved_subject'})
    g, e, d, s = (proof[k] for k in ('grant', 'effective_reference', 'owner_decision', 'approved_subject'))
    require(raw_hash(canonical(g['RECORD'])) == GRANT_SHA, 'WRONG_ISSUED_GRANT_CONTENT')
    require(g['GRANT_IDENTITY']['sha256'] == GRANT_SHA and
            e['GRANT_IDENTITY'] == g['GRANT_IDENTITY'] and
            e['IMPLEMENTATION_TEST_GRANT_EFFECTIVE'] is True, 'INEFFECTIVE_GRANT')
    require(raw_hash(canonical(s['CONTENT'])) == SUBJECT_SHA and
            g['RECORD']['APPROVED_SUBJECT_IDENTITY'] == s['IDENTITY'], 'WRONG_APPROVED_SUBJECT')
    require(d['CONTENT']['SELECTION'] == 'AUTHORIZE_BOUNDED_A15_ADAPTER_IMPLEMENTATION_SYNTHETIC_TEST'
            and d['CONTENT']['APPROVED_SUBJECT_IDENTITY'] == s['IDENTITY'], 'WRONG_OWNER_DECISION')
    require(d['IDENTITY'] == g['RECORD']['PROJECT_OWNER_DECISION_EVIDENCE']['IDENTITY'],
            'DECISION_IDENTITY_MISMATCH')
    require(raw_hash(canonical(d['CONTENT'])) == d['IDENTITY']['sha256'], 'DECISION_CONTENT_MISMATCH')
    require(g['RECORD']['A15_EXECUTION_GRANT'] is None and
            g['RECORD']['A15_CAPTURE_GRANT'] is None, 'UNAUTHORIZED_REAL_A15_GRANT')
    return True
