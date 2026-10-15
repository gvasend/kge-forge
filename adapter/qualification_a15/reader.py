"""Fresh fake-protocol reader. Never applies, saves, or loads native A15 state."""
from pathlib import Path
import sys
from . import contracts as c

def run_reader(binding, scratch, scope_verifier):
    c.require(callable(scope_verifier), 'EXTERNAL_SCOPE_VERIFIER_REQUIRED')
    request = c.read_exact(binding['request_path'])
    c.validate(request, 'READER_REQUEST')
    c.validate_binding(binding, 'READER', request, scratch)
    c.require(scope_verifier(binding, request) is True, 'SCOPE_NOT_AUTHORIZED')
    output = c.read_exact(Path(binding['output_directory']) / 'published-output.json')
    expected = c.read_exact(binding['expected_path'])
    c.require(output['identity'] == request['payload']['published_output_identity']
              and expected['identity'] == request['payload']['expected_output_identity'],
              'READER_IDENTITY_MISMATCH')
    c.compare_complete_output(output, expected)
    return c.record('READER_RESULT', {'request_identity': request['identity'],
        'published_output_identity': output['identity'], 'expected_output_identity': expected['identity'],
        'matched': True})

def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    c.require(len(argv) == 3, 'EXACT_READER_ARGUMENTS_REQUIRED')
    binding = c.read_exact(argv[0]);scratch = argv[1]
    c.require(c.raw_hash(c.canonical(binding)) == argv[2], 'INVOCATION_BYTES_MISMATCH')
    proof = c.read_exact(binding['proof_path'])
    result = run_reader(binding, scratch, lambda b, r: c.authorize_proof(proof))
    print(c.canonical(result).decode())
    return 0

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except c.ProtocolError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)
