"""Deterministic local replay CLI. Never executes a selected action."""
import argparse
import sys
from pathlib import Path

from . import codec as c, model as m, replay

ROOT = Path(__file__).resolve().parents[2]


def load(path):
    data = c.parse_json(Path(path).read_bytes())
    schema = data.get('schema') if type(data) is dict else None
    if schema == 'E1-RESUME-MANIFEST-1':
        return replay.import_e1(path, ROOT), (), {}
    if schema == 'PLANNER-BUNDLE-1':
        # Native immutable filename is the required out-of-band content pin.
        name = Path(path).name
        if not name.startswith('bundle-') or not name.endswith('.json'):
            raise m.PlannerError('native bundle requires content-addressed filename')
        identity = m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, 'planner-bundle-v1', name[7:-5])
        return c.restore(path, identity, ROOT), (), {}
    return replay.import_fixture(path, ROOT)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    for name in ('validate', 'plan', 'apply', 'replay', 'restore'):
        sub = commands.add_parser(name)
        sub.add_argument('input')
        if name in ('apply', 'replay', 'restore'):
            sub.add_argument('--out', required=True)
        if name == 'apply':
            sub.add_argument('--event', required=True)
    admission = commands.add_parser('admit-evidence')
    admission.add_argument('input')
    admission.add_argument('--request', required=True)
    admission.add_argument('--payload', required=True)
    admission.add_argument('--expected-identity', required=True)
    admission.add_argument('--source-root', required=True)
    admission.add_argument('--out', required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'admit-evidence':
            expected = c._unwire(c.parse_json(Path(args.expected_identity).read_bytes()))
            bundle = c.restore(args.input, expected, args.source_root)
            request = c._unwire(c.parse_json(Path(args.request).read_bytes()))
            m.validate_types(request, m.EvidenceSourceAdmission)
            if len(request.source_additions) != 1:
                raise m.PlannerError('exactly one evidence payload required')
            result, identity, noop = c.admit_external_evidence(bundle, request,
                {request.source_additions[0].path: Path(args.payload).read_bytes()}, args.out, args.source_root)
            sys.stdout.buffer.write(c.canonical_bytes({'current':c._wire(c.bundle_id(result)),
                'transaction':c._wire(identity),'idempotent_noop':noop}) + b'\n')
            return 0
        bundle, events, expected = load(args.input)
        if args.command == 'apply':
            event = c._unwire(c.parse_json(Path(args.event).read_bytes()))
            if any(type(e.result) is m.EvidenceSourceAdmission for e in bundle.events):
                bundle, _ = c.commit_event(bundle, event, args.out, ROOT)
            else:
                bundle = c.record_result(bundle, event)
        elif args.command == 'replay':
            step_oracles = expected.get('steps')
            if step_oracles is not None and (type(step_oracles) is not list or len(step_oracles) != len(events)):
                raise m.PlannerError('per-step oracle count mismatch')
            for index, event in enumerate(events):
                bundle = c.record_result(bundle, event)
                if step_oracles is not None:
                    actual = replay.plan_output(bundle, ROOT)
                    if type(step_oracles[index]) is not dict:
                        raise m.PlannerError('invalid step oracle')
                    if any(key not in actual or actual[key] != value for key, value in step_oracles[index].items()):
                        sys.stderr.write('replay step expectation mismatch\n')
                        return 3
        output = replay.plan_output(bundle, ROOT)
        if args.command == 'replay':
            final = expected.get('final', {}) if 'steps' in expected else expected
            if type(final) is not dict:
                raise m.PlannerError('invalid final oracle')
            if any(key not in output or output[key] != value for key, value in final.items()):
                sys.stderr.write('replay expectation mismatch\n')
                return 3
        if args.command in ('apply', 'replay', 'restore'):
            c.save_bundle(bundle, args.out, ROOT)
        sys.stdout.buffer.write(c.canonical_bytes(output) + b'\n')
        return 0
    except (m.PlannerError, OSError, ValueError, KeyError, TypeError) as exc:
        sys.stderr.write(str(exc) + '\n')
        return 2


if __name__ == '__main__':
    sys.exit(main())
