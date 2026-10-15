"""Run only the presealed independent reproduction/determinism dimensions."""
import json
import os
import subprocess
import sys

from common import OUT, ROOT, save


def invoke(run, variant, seed, mode, *extra):
    command = [sys.executable, str(OUT / 'worker.py'), mode, '--run', run, '--variant', variant] + list(extra)
    env = dict(os.environ, PYTHONHASHSEED=str(seed), PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(ROOT))
    process = subprocess.run(command, cwd=str(ROOT), env=env, capture_output=True, text=True)
    result = {'run': run, 'variant': variant, 'seed': seed, 'mode': mode,
              'arguments': list(extra), 'exit_code': process.returncode,
              'stdout': process.stdout.strip(), 'stderr': process.stderr.strip()}
    if process.returncode:
        save(OUT / 'STOP-independent-process.json', result)
        print(json.dumps(result), flush=True)
        sys.exit(1)
    return result


def run_case(run, variant, seed, presentation, full_readers):
    checks = [invoke(run, variant, seed, 'bootstrap', '--presentation', presentation)]
    if full_readers:
        for index in (1, 2, 3):
            checks.append(invoke(run, variant, seed, 'read', '--boundary', 'start', '--reader', str(index)))
    checks.append(invoke(run, variant, seed, 'commit', '--phase', '1'))
    # A fresh process consumes the immutable request-ready checkpoint. Writers
    # always terminate, including when only reproduction final readers are required.
    for index in ((1, 2, 3) if full_readers else (1,)):
        checks.append(invoke(run, variant, seed, 'read', '--boundary', 'ready', '--reader', str(index)))
    checks.append(invoke(run, variant, seed, 'commit', '--phase', '2'))
    for index in (1, 2, 3):
        checks.append(invoke(run, variant, seed, 'read', '--boundary', 'wait', '--reader', str(index)))
    save(OUT / 'dimensions' / (run + '.json'), {'RESULT': 'PASS', 'run': run,
         'variant': variant, 'seed': seed, 'presentation': presentation, 'checks': checks})
    print(json.dumps({'RESULT': 'PASS', 'run': run, 'processes': len(checks)}), flush=True)


if __name__ == '__main__':
    # The actual primary seed-0 occurrence has already executed, once.
    for seed in (1, 7, 101):
        run_case('primary-seed-' + str(seed), 'primary', seed, 'original', True)
    for number in (1, 2, 3):
        name = 'reproduction-' + str(number)
        run_case(name, name, 0, 'original', False)
    for seed in (0, 1, 7, 101):
        for presentation in ('reversed', 'rotated'):
            run_case('permutation-%s-%s' % (seed, presentation), 'primary', seed, presentation, True)
