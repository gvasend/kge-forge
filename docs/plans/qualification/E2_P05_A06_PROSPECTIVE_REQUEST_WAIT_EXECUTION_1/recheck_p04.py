"""Reuse the sealed read-only 37-term inspector; redirect only its report destination."""
import ast
import json

from common import ROOT, OUT, c, equal, ref, save


source = ROOT / 'docs/plans/qualification/E2_P05_READINESS_1/inspect_target.py'
raw = source.read_text()
old_write = "(OUT / 'target-inspection.json').write_bytes(c.canonical_bytes(result))"
equal('single old inspector report write', raw.count(old_write), 1)
adapted = raw.replace(old_write, 'capture_result(result)')
ast.parse(adapted, str(source))


def capture_result(result):
    equal('37 independent initial checks', len(result['checks']), 37)
    equal('P04 initial oracle', result['RESULT'], 'PASS')
    save(OUT / 'P04-initial-oracle-recheck.json', result)
    save(OUT / 'P04-inspector-reuse.json', {
        'RESULT': 'PASS', 'source': ref(source), 'runtime_or_oracle_change': False,
        'only_harness_change': 'Replace the inspector report-write destination with this execution evidence directory',
        'actual_initial_checks': 37, 'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO',
    })


namespace = {'__name__': 'sealed_read_only_inspector', '__file__': str(source),
             'capture_result': capture_result}
exec(compile(adapted, str(source), 'exec'), namespace)
namespace['main']()
