"""Sealed A04 execution/restore/replay harness. No Planner/runtime changes."""
import argparse
from dataclasses import fields, is_dataclass, replace
from enum import Enum
import hashlib
import json
import os
from pathlib import Path
from unittest.mock import patch

from adapter.planner import codec as c, core, dossier_transaction as dt, model as m
import bounded_prepare

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
PLANS = ROOT / 'docs/plans'
BASE = OUT.with_name('E2_P05_A04_PROSPECTIVE_ANCESTRY_CONTRACT_1')
DA = OUT.with_name('E2_P05_A04_DURABLE_ADMISSION_CONTRACT_1')
REP = OUT.with_name('E2_P05_A04_EVENT_VALIDATION_RECONCILIATION_1')
LABELS = {'QUALIFICATION_TYPE': 'PROSPECTIVE_REPLACEMENT',
    'ORIGINAL_A04_HISTORICAL_ANCESTRY': 'UNPROVEN', 'ORIGINAL_A03_HISTORICAL_OCCURRENCE': 'UNPROVEN',
    'HISTORICAL_RECONSTRUCTION': 'NO', 'PROSPECTIVE_A04_EVENT_IS_ORIGINAL_EVENT': 'NO'}


class Divergence(Exception):
    def __init__(self, name, actual, expected):
        super().__init__(name)
        self.name, self.actual, self.expected = name, actual, expected


def read(path): return json.loads(Path(path).read_bytes())
def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')
def uid(identity): return identity.namespace + ':' + identity.sha256
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def equal(name, actual, expected):
    if actual != expected: raise Divergence(name, actual, expected)
def native_equal(name, actual, expected):
    equal(name, c.canonical_bytes(c._wire(actual)), c.canonical_bytes(c._wire(expected)))
def typed(value):
    if is_dataclass(value):
        return {'$type': type(value).__name__, **{f.name: typed(getattr(value, f.name)) for f in fields(value)}}
    if isinstance(value, Enum): return {'$enum': type(value).__name__, 'value': value.value}
    if isinstance(value, (tuple, list)): return [typed(x) for x in value]
    if isinstance(value, dict): return {str(k): typed(v) for k, v in value.items()}
    return value


def verify_entry():
    report = read(PLANS/'DETERMINISTIC_PLANNER_V0_1_DURABLE_ADMISSION_D01_RESULT.json')
    for key, value in {'RESULT':'PASS','DURABLE_ADMISSION_CAPABILITY':'PASS',
        'A04_DURABLE_TRANSACTION_COMPATIBILITY':'PASS','PROSPECTIVE_A04_EXECUTION_READY':'YES',
        'PROSPECTIVE_A04_EXECUTED':'NO','ORIGINAL_A04_HISTORICAL_ANCESTRY':'UNPROVEN'}.items():
        equal('ENTRY:' + key, report[key], value)
    for pin in report['evidence'].values(): equal('D01_EVIDENCE:'+pin['path'], sha(ROOT/pin['path']), pin['raw_sha256'])
    for name, digest in read(OUT.with_name('DURABLE_ADMISSION_D01')/'final-runtime-process-check.json')['runtime_hashes'].items():
        equal('D01_RUNTIME:'+name, sha(ROOT/name), digest)
    overlay = read(DA/'versioned-overlay.json')
    equal('SCOPE_SELECTION', overlay['scope_decision'], 'AUTHORIZE_PROSPECTIVE_P05_A04_ANCESTRY_QUALIFICATION')
    pins = read(DA/'source-pins.json')['pins'] + overlay['preserved_files']
    for pin in pins:
        if pin['path'] in ('adapter/planner/codec.py','adapter/planner/model.py'): continue
        equal('SEALED:'+pin['path'], sha(ROOT/pin['path']), pin['raw_sha256'])
    for key, value in LABELS.items(): equal('LABEL:'+key, overlay[key], value)
    auth = read(BASE/'authority.json')
    equal('ADDITIONAL_AUTHORITY', auth['ADDITIONAL_AUTHORITY_REQUIRED'], 'NO')
    equal('AUTHORIZATION_SUBJECT', auth['QUALIFICATION_SCOPE_AUTHORIZATION']['subject_identity'], overlay['authorization_subject'])
    mappings = read(BASE/'N12-N13-assurance-mapping.json')
    for name in ('N12','N13'): equal(name+'_SEALED_MAPPING', mappings[name][name+'_MAPPING_PRESERVED'], 'YES')
    return read(BASE/'prospective-start.json')


def load_start(presentation='original'):
    spec = verify_entry()
    path = ROOT/spec['START_PATH']['path']
    expected = c._identity(path.read_bytes(), 'planner-bundle-v1')
    before = c.restore(path, expected, ROOT)
    equal('START_BUNDLE', uid(expected), spec['START_BUNDLE_ID'])
    equal('START_STATE', uid(c.snapshot_id(before.current)), spec['START_STATE_ID'])
    equal('START_ROOT', uid(before.events[0].identity), spec['LEDGER_ROOT'])
    equal('START_HEAD', uid(before.events[-1].identity), spec['APPEND_HEAD'])
    equal('START_PARENT', uid(before.events[-1].identity), spec['PARENT_EVENT_ID'])
    equal('START_LEDGER_COUNT', len(before.events), 2)
    action = next(a for a in before.current.actions if a.id.value == 'E2-PREPARE')
    equal('A04_NOT_EXECUTED', action.prepared_dossier, None)
    equal('VALIDATIONS_NOT_CREATED', before.current.validation_instances, ())
    equal('AUTHORITY_NONE', action.authority, None)
    equal('SELECTED_PREPARE', core.recompute(before.current).selection.selected, action.id)
    if presentation != 'original':
        permute = (lambda v: v[::-1]) if presentation == 'reverse' else (lambda v: v[1:]+v[:1])
        def state(s): return replace(s, actions=permute(s.actions), statuses=permute(s.statuses), knowledge=permute(s.knowledge))
        before = replace(before, initial=state(before.initial), current=state(before.current), sources=permute(before.sources))
        equal('UNORDERED_START_ID', uid(c.bundle_id(before)), spec['START_BUNDLE_ID'])
    pin = c._unwire(read(DA/'snapshot-event-binding.json')['A04_expected_source_additions'][0])
    raw = (ROOT/pin.path).read_bytes()
    equal('ACTUAL_INPUT_RAW_ID', c._identity(raw,'raw-file-sha256'), pin.identity)
    return before, expected, ((pin, raw),)


def oracles():
    result = read(BASE/'oracles/expected-result-and-state.json')
    native = read(DA/'oracles/prospective-native-binding.json')
    event = read(REP/'oracles/composite-representation.json')['native_event']
    return result, native, c._unwire(event)


def check_effect(before, after, event):
    result, native, expected_event = oracles()
    native_equal('ACTUAL_PREPARE_RESULT', event.result, c._unwire(result['expected_result']))
    equal('POST_SNAPSHOT_BYTES', c.snapshot_bytes(after), c.snapshot_bytes(c._unwire(result['expected_post_state'])))
    native_equal('ACTUAL_EVENT', event, expected_event)
    equal('POST_SNAPSHOT_ID', uid(c.snapshot_id(after)), native['EXPECTED_POST_SNAPSHOT_ID'])
    equal('EVENT_ID', uid(event.identity), native['EXPECTED_EVENT_ID'])
    equal('CONTROL', core.recompute(after).control.value, result['expected_control'])
    equal('SIX_TYPED_VALIDATIONS', len(after.validation_instances), 6)
    return True


def check_bundle(before, bundle, resolver):
    result, native, event = oracles()
    equal('BUNDLE_EVENT_COUNT', len(bundle.events), 3)
    native_equal('PRESERVED_PREFIX', bundle.events[:2], before.events)
    check_effect(before.current, bundle.current, bundle.events[2])
    equal('COMPLETE_BUNDLE_WIRE', {'schema':'PLANNER-BUNDLE-1','bundle':c._wire(bundle)}, native['future_bundle_wire'])
    equal('BUNDLE_COMPARISON_ID', uid(c.bundle_id(bundle,snapshot_resolver=resolver)),
          native['EXPECTED_FUTURE_BUNDLE_ID_COMPARISON_ONLY'])
    prefix = c._prefix_bundle(bundle,2,snapshot_resolver=resolver)
    equal('REPLAY_START_PREFIX', c.bundle_bytes(prefix), c.bundle_bytes(before))
    archived = resolver(event.after_snapshot)
    equal('ARCHIVE_SNAPSHOT', c.snapshot_bytes(archived), c.snapshot_bytes(bundle.current))
    bindings = read(DA/'snapshot-event-binding.json')['A04_member_bindings']
    for member in bindings:
        matches = [v for v in archived.validation_instances if v.predicate == c._unwire(member['predicate'])]
        equal('MEMBER_UNIQUE',len(matches),1)
        v = matches[0]
        equal('MEMBER_SUBJECT',v.dossier,c._unwire(member['dossier']))
        equal('MEMBER_ORDERED_INPUTS',v.inputs,c._unwire(member['ordered_inputs']))
        equal('MEMBER_SNAPSHOT',event.after_snapshot,c._unwire(member['snapshot']))
    return True


def writer(directory, presentation):
    directory = Path(directory).resolve()
    equal('NEW_WRITER_STORE', directory.exists(), False)
    before, bid, artifacts = load_start(presentation)
    audit = {'producer_invocations':0}
    # Load all immutable comparison objects before the actual producer begins.
    expected_result, expected_native, expected_event = oracles()
    def oracle(pre, post, event):
        native_equal('ACTUAL_PREPARE_RESULT',event.result,c._unwire(expected_result['expected_result']))
        equal('POST_SNAPSHOT_BYTES',c.snapshot_bytes(post),c.snapshot_bytes(c._unwire(expected_result['expected_post_state'])))
        native_equal('ACTUAL_EVENT',event,expected_event)
        equal('PRECOMMIT_BUNDLE_ID', uid(c._identity(c._bundle_bytes_admitted(replace(before,
            events=before.events+(event,),current=post,sources=before.sources+(artifacts[0][0],),
            dossier_materializations=(m.DossierMaterializationBinding(event.identity,bid,(artifacts[0][0],)),))),
            'planner-bundle-v1')), expected_native['EXPECTED_FUTURE_BUNDLE_ID_COMPARISON_ONLY'])
        return True
    operation = dt.register_producer(m.ActionId('E2-PREPARE'),lambda s,a: bounded_prepare.execute(s,a,before,audit,presentation))
    bundle, post_id, noop = dt.execute(before,bid,operation,artifacts,directory,ROOT,postcondition=oracle)
    equal('PRIMARY_NOT_RETRY',noop,False)
    equal('EXACTLY_ONE_PRODUCER_INVOCATION',audit['producer_invocations'],1)
    resolver = c.snapshot_resolver(directory)
    check_bundle(before,bundle,resolver)
    event=bundle.events[-1]
    trace = {**LABELS,'result':'PASS','run_id':str(directory.relative_to(OUT)),
        'hash_seed':os.environ.get('PYTHONHASHSEED'),'presentation':presentation,**audit,
        'ACTUAL_A04_RESULT':c._wire(event.result),'A04_EVENT_ID':uid(event.identity),'EVENT_TYPE':'ExecutionEvent',
        'EVENT_PAYLOAD':c._wire(event),'PARENT_EVENT_ID':uid(event.parent_event),
        'PRE_STATE_ID':uid(event.parent_snapshot),'POST_SNAPSHOT_ID':uid(event.after_snapshot),
        'LEDGER_ID':read(BASE/'prospective-start.json')['LEDGER_ID'],'LEDGER_POSITION':3,'ledger_index':2,
        'POST_LEDGER_ROOT':uid(bundle.events[0].identity),'POST_APPEND_HEAD':uid(event.identity),
        'POST_A04_BUNDLE_ID':uid(post_id),'POST_A04_STATE_ID':uid(c.snapshot_id(bundle.current)),
        'native_bundle_path':str((directory/('bundle-'+post_id.sha256+'.json')).relative_to(ROOT)),
        'bundle_binding':c._wire(bundle.dossier_materializations[0]),
        'typed_validation_members':c._wire(bundle.current.validation_instances),
        'post_computation':typed(core.recompute(bundle.current)),
        'native_authority_issued':False,'install_events':0,'new_occurrence_count':1,
        'actual_native_transaction':True,'original_historical_event_ids':None,'original_history_splice':False}
    write(directory.parent/'writer-result.json',trace)
    return trace


def reader(directory):
    directory=Path(directory).resolve()
    before,bid,artifacts=load_start()
    head=read(directory/'HEAD.json');post_id=c._unwire(head['bundle'])
    def barred(*args,**kwargs):raise AssertionError('RESTORE_REPLAY_MAY_NOT_EXECUTE_OR_PUBLISH')
    with patch.object(dt,'register_producer',side_effect=barred),patch.object(dt,'prepare',side_effect=barred),\
         patch.object(dt,'execute',side_effect=barred),patch.object(dt,'commit',side_effect=barred),\
         patch.object(c,'_publish_head',side_effect=barred),patch.object(bounded_prepare,'execute',side_effect=barred):
        bundle=c.restore(directory/('bundle-'+post_id.sha256+'.json'),post_id,ROOT)
        resolver=c.snapshot_resolver(directory)
        c._read_head(directory,before,ROOT)
        check_bundle(before,bundle,resolver)
        computations=[]
        for unused in range(3):
            state=c._replay(bundle,snapshot_resolver=resolver)
            equal('READ_ONLY_REPLAY_STATE',c.snapshot_bytes(state),c.snapshot_bytes(bundle.current))
            computations.append(typed(core.recompute(state)))
        equal('REPLAY_IDEMPOTENT_COMPUTATION',computations[0],computations[2])
    trace=read(directory.parent/'writer-result.json')
    equal('FRESH_READER_COMPUTATION',computations[0],trace['post_computation'])
    return {**LABELS,'result':'PASS','hash_seed':os.environ.get('PYTHONHASHSEED'),
        'POST_A04_BUNDLE_ID':uid(post_id),'state':uid(c.snapshot_id(bundle.current)),
        'event':uid(bundle.events[-1].identity),'replays':3,'live_operation_invocations':0,
        'validators_rerun':False,'new_occurrences':0,'full_computation':computations[0]}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=('writer','reader'))
    parser.add_argument('directory');parser.add_argument('--presentation',default='original');parser.add_argument('--output')
    args=parser.parse_args()
    try:
        value=writer(args.directory,args.presentation) if args.mode=='writer' else reader(args.directory)
        if args.output:write(args.output,value)
        print(json.dumps({k:value[k] for k in ('result','POST_A04_BUNDLE_ID')}))
    except Exception as exc:
        record={**LABELS,'result':'FAIL','FIRST_COUNTEREXAMPLE':getattr(exc,'name',type(exc).__name__),
            'EXPECTED':repr(getattr(exc,'expected',None)),'ACTUAL':repr(getattr(exc,'actual',str(exc))),
            'STATE_ID':None,'EVENT_ID':None,'CLASSIFICATION':'SEALED_EXECUTION_DIVERGENCE','no_live_repair':True}
        write(OUT/'STOP.json',record)
        print(json.dumps(record));raise
