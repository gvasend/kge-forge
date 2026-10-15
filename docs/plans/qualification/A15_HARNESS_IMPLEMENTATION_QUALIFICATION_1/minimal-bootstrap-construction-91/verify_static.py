"""Metadata-only independent AST/JSON review. Never imports target modules."""
import ast
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
BASE = Path(__file__).resolve().parent
PATHS = ['adapter/qualification_bootstrap/systemd_pids_once.py', 'adapter/tests/test_systemd_pids_bootstrap.py']
def sha(raw): return hashlib.sha256(raw).hexdigest()
def encoded(v): return json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
def check(core, tests):
    c = ast.parse(core); t = ast.parse(tests)
    functions = {n.name: n for n in ast.walk(c) if isinstance(n, ast.FunctionDef)}
    methods = sorted(n.name for n in ast.walk(t) if isinstance(n, ast.FunctionDef) and n.name.startswith('test_'))
    assert len(methods) == 14
    forbidden = {'subprocess', 'socket', 'multiprocessing'}
    assert not any(isinstance(n, ast.Import) and any(a.name.split('.')[0] in forbidden for a in n.names) for n in ast.walk(c))
    assert not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in {'eval', 'exec', 'compile'} for n in ast.walk(c))
    for marker in ["GRANT_SHA = '38120e22ad910456ccc4096d59b619fa79efcd6903d3d769c9524495c8c88165'",
                   "SUBJECT_SHA = '596a92d446ae2f4b8de57f02b977302577845586c2a45f40d01479e9827a2b3d'",
                   "entry['command'] == {'operation': 'INERT_CALLBACK', 'argv': []}",
                   "sort_keys=True, separators=(',', ':')", 'os.O_EXCL',
                   "os.fsync(fd)", 'os.fsync(directory)', 'confirm_consumption(directory, name, record, inode)',
                   "state = 'OUTCOME_UNKNOWN'", "'launch_permitted': False", "'retry_allowed': False",
                   'causal_exception = original', "'AUTOMATIC_RETRIES': 0", "REAL_PROBE_BINDING = None",
                   "self.root = pathlib.Path(manifest['root'])"]:
        assert marker in core, marker
    assert 'confirm_consumption' in functions and 'recover_inert' in functions
    consume = ast.get_source_segment(core, functions['consume_inert'])
    assert consume.index('confirmed = confirm_consumption') < consume.index('outcome = callback()')
    assert 'launch_available = False' in consume
    assert "{'event': event, 'value':" in tests
    assert "self.assertEqual(observation, fixture['expected'])" in tests
    assert 'subprocess.Popen(argv' in tests and "'--inert-helper'" in tests
    assert 'core.consume_inert' not in core  # No internal retry recursion.
    return methods
core, tests = [(ROOT / p).read_text() for p in PATHS]
methods = check(core, tests)
negative_markers = [
 ('wrong_grant', "GRANT_SHA = '38120e22ad910456ccc4096d59b619fa79efcd6903d3d769c9524495c8c88165'"),
 ('wrong_subject', "SUBJECT_SHA = '596a92d446ae2f4b8de57f02b977302577845586c2a45f40d01479e9827a2b3d'"),
 ('wrong_command', "entry['command'] == {'operation': 'INERT_CALLBACK', 'argv': []}"),
 ('unstable_key', "sort_keys=True, separators=(',', ':')"),
 ('duplicate_admitted', 'os.O_EXCL'), ('missing_atomic_reservation', 'os.O_EXCL'),
 ('missing_file_fsync', 'os.fsync(fd)'), ('missing_directory_fsync', 'os.fsync(directory)'),
 ('missing_reread', 'confirm_consumption(directory, name, record, inode)'),
 ('partial_reopened', "state = 'OUTCOME_UNKNOWN'"),
 ('crash_reopened', "'launch_permitted': False"),
 ('first_failure_replaced', 'causal_exception = original'),
 ('automatic_retry', "'AUTOMATIC_RETRIES': 0"),
 ('unauthorized_source_boundary', "self.root = pathlib.Path(manifest['root'])"),
 ('real_system_execution', 'REAL_PROBE_BINDING = None'),
 ('real_probe_execution', "'retry_allowed': False")]
negatives = {}
for name, marker in negative_markers:
    mutated = core.replace(marker, marker.replace(marker[0], '_', 1))
    try: check(mutated, tests)
    except (AssertionError, SyntaxError): negatives[name] = 'REJECTED'
    else: raise AssertionError('negative accepted: ' + name)
before = json.loads((BASE / 'preservation-before.json').read_text())
changed = [p for p, expected in before.items() if not (ROOT/p).is_file() or sha((ROOT/p).read_bytes()) != expected]
assert not changed, changed
register = json.loads((ROOT/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json').read_text())
head = '0'*64; ll11 = False
for event in register['EVENTS']:
    assert event['PREVIOUS_EVENT_HASH'] == head
    body = {k:v for k,v in event.items() if k != 'EVENT_HASH'}
    assert sha(json.dumps(body, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()) == event['EVENT_HASH']
    head = event['EVENT_HASH']
    if 'LL-11' in json.dumps(event.get('LESSON', {})): ll11 = True
assert ll11
result = {'source_hashes': {p:sha((ROOT/p).read_bytes()) for p in PATHS},
          'test_methods': methods, 'negative_controls': negatives,
          'preservation_changed': changed, 'lessons_head': head, 'LL_11_preserved': ll11,
          'active_tests_executed': 0, 'behaviorally_qualified': False,
          'review_scope': 'AST structure and independent retained bytes; not behavioral proof'}
print(json.dumps({'semantic_sha256': sha(encoded(result)), 'reconstruction': result}, sort_keys=True))
