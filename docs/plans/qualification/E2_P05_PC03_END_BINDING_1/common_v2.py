"""Versioned checker correction; prior sources/oracle values stay immutable."""
from copy import deepcopy
from functools import lru_cache
import sys
import common as base
from common import *

BASE_OUT = base.OUT
OUT = BASE_OUT / 'v2'


def save(name, value):
    path = OUT / name
    raw = (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode()
    if path.exists():
        equal('immutable v2 qualification evidence ' + name, path.read_bytes(), raw)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)


@lru_cache(maxsize=1)
def process():
    value = deepcopy(base.process()['definition'])
    value['code'] = [ref(BASE_OUT / name) for name in ('select_sources.py', 'common.py', 'binding.py', 'oracle.py',
        'common_v2.py', 'binding_v2.py', 'oracle_v2.py')]
    value['checker_revision'] = {'classification': 'HARNESS_COMPARISON_ERROR_CORRECTION',
        'diagnostic': ref(BASE_OUT / 'attempt-1-diagnostic.json'),
        'source_lifecycle_oracle_values_changed': False,
        'A03': 'Complete post-state knowledge is the union of both presealed per-result output sets',
        'unordered_comparison': 'Snapshot-declared knowledge/validation/goal sets use unchanged native canonical ordering'}
    value['invocations'] = {'seal': [sys.executable, str((BASE_OUT / 'oracle_v2.py').relative_to(ROOT))],
        'materialize': [sys.executable, str((BASE_OUT / 'binding_v2.py').relative_to(ROOT)), 'materialize'],
        'preflight': [sys.executable, str((BASE_OUT / 'binding_v2.py').relative_to(ROOT)), 'preflight'],
        'negatives': [sys.executable, str((BASE_OUT / 'binding_v2.py').relative_to(ROOT)), 'negatives'],
        'readers': [[sys.executable, str((BASE_OUT / 'binding_v2.py').relative_to(ROOT)), 'reader',
            '--seed', str(seed), '--index', str(index), '--presentation', form]
            for seed in (0, 1, 7, 101) for index in (1, 2, 3)
            for form in ('original', 'reversed', 'rotated')]}
    return {'identity': qid('qualification-PC03-END-process-v2', value), 'definition': value}


def metadata_body():
    value = deepcopy(base.metadata_body())
    value['process'] = process()
    return value


def input_plan():
    rows = base.input_plan()
    return [(name, typ, ref(OUT / 'expected-oracle.json') if name == 'INDEPENDENT_BINDING_ORACLE' else source, role)
        for name, typ, source, role in rows]
