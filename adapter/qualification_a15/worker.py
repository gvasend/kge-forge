"""Fake-only worker; does not certify its own exit or import native Planner code."""
import json
import os
from pathlib import Path
import sys
import time
from . import contracts as c

def record_synthetic_result(fixture, request):
    c.validate_synthetic_input(fixture, request)
    p = request['payload']
    state = dict(fixture['initial_state'], support_current=False)
    event = c.identity({'initial': p['initial_snapshot_identity'],
                        'source': p['source_identity'], 'variant': p['variant_id']},
                       'qualification-a15-fake-event-v1')
    return c.record('PUBLISHED_OUTPUT', {
        'request_identity': request['identity'], 'initial_snapshot_identity': p['initial_snapshot_identity'],
        'source_identity': p['source_identity'], 'event_identity': event,
        'after_snapshot_identity': c.identity(state, 'qualification-a15-fake-snapshot-v1'),
        'typed_state': state, 'proof_validation': 'FAKE_STALE', 'proof_usability': False,
        'target_satisfaction': False, 'admission_stale': 'FAKE_CURRENT_VALIDATION_WITHDRAWN',
        'control': 'FAKE_BLOCKED', 'resume': {'allowed': False, 'actions': [],
            'reasons': ['FAKE_SUPPORT_WITHDRAWN'], 'supporting_identities': []},
        'ordered_trace': ['FAKE_RESTORE', 'FAKE_RECORD_RESULT', 'FAKE_SAVE'],
        'protected_state': fixture['initial_state']['protected']})

def publish_synthetic_bundle(output, request, directory, fault='NONE'):
    c.validate(output, 'PUBLISHED_OUTPUT')
    path = c.publish(directory, 'published-output.json', output)
    handoff = c.record('HANDOFF_RECORD', {'request_identity': request['identity'],
        'published_output_identity': output['identity'], 'publication_bytes_sha256': c.raw_hash(path.read_bytes())})
    if fault == 'BAD_HANDOFF':
        handoff['payload']['publication_bytes_sha256'] = '0' * 64
        handoff = c.record('HANDOFF_RECORD', handoff['payload'])
    c.publish(directory, 'handoff.json', handoff)
    return handoff

def run_worker(binding, scratch, scope_verifier):
    c.require(callable(scope_verifier), 'EXTERNAL_SCOPE_VERIFIER_REQUIRED')
    request = c.read_exact(binding['request_path'])
    c.validate(request, 'WORKER_REQUEST')
    c.validate_binding(binding, 'WORKER', request, scratch)
    c.require(scope_verifier(binding, request) is True, 'SCOPE_NOT_AUTHORIZED')
    fixture = c.read_exact(binding['fixture_path'])
    c.validate_synthetic_input(fixture, request)
    if binding['fault'] == 'NONZERO':
        raise c.ProtocolError('EXPECTED_FAKE_WORKER_FAILURE')
    if binding['fault'] == 'TIMEOUT':
        time.sleep(61)
        raise c.ProtocolError('TIMEOUT_NOT_TERMINATED')
    output = record_synthetic_result(fixture, request)
    if binding['fault'] == 'NO_PUBLICATION':
        raise c.ProtocolError('EXPECTED_NO_PUBLICATION')
    handoff = publish_synthetic_bundle(output, request, binding['output_directory'], binding['fault'])
    return c.record('WORKER_RESULT', {'request_identity': request['identity'],
        'published_output_identity': output['identity'], 'handoff_identity': handoff['identity']})

def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    c.require(len(argv) == 3, 'EXACT_WORKER_ARGUMENTS_REQUIRED')
    binding = c.read_exact(argv[0]);scratch = argv[1]
    c.require(c.raw_hash(c.canonical(binding)) == argv[2], 'INVOCATION_BYTES_MISMATCH')
    proof = c.read_exact(binding['proof_path'])
    result = run_worker(binding, scratch, lambda b, r: c.authorize_proof(proof))
    print(c.canonical(result).decode())
    return 0

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except c.ProtocolError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)
