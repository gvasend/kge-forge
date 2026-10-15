"""Static launch/spec/schema controls; no actual guards or reader invocation."""
import json
from copy import deepcopy
from pathlib import Path
O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_bytes())
spec=read(O/'reader-spec-operands.json');base={'spec':spec,'required_guards':spec['REQUIRED_GUARDS'],'exit_owner':'SUPERVISOR','process_model':'EXEC_FRESH_INTERPRETER','input_kind':'PERSISTED_REFERENCES_ONLY','transfer_open_fd':False,'policy_version':'E1-SELECTION-1-P06','scope':'PARTIAL_HISTORICAL_REPLAY','events':[],'HEAD_required':False,'directory_fsync_claim':False,'crash_durability_claim':False,'success_predicate':'GUARDS_AND_IDENTITIES_AND_SEMANTIC_COMPARISONS'}
def validate(v):
 assert v==base and v['spec']['RUNTIME_GUARDS_SATISFIED_NOW'] is False and len(v['required_guards'])==4
rows=[]
def reject(name,fn):
 v=deepcopy(base);fn(v)
 try:validate(v)
 except AssertionError:rows.append({'CASE':name,'STATUS':'REJECTED'})
 else:raise AssertionError(name)
reject('reader before save',lambda v:v['required_guards'].remove('SAVE_RETURNED_SUCCESSFULLY'))
reject('reader before publication verification',lambda v:v['required_guards'].remove('PUBLISHED_TARGET_VERIFIED'))
reject('reader before writer exit',lambda v:v['required_guards'].remove('WRITER_EXIT_OBSERVED_BY_SUPERVISOR'))
reject('writer self-attests exit',lambda v:v.update(exit_owner='WRITER'))
reject('warm reader',lambda v:v.update(process_model='WRITER_PROCESS'))
reject('in-memory bundle supplied',lambda v:v.update(input_kind='PYTHON_BUNDLE_OBJECT'))
reject('open descriptor supplied',lambda v:v.update(transfer_open_fd=True))
reject('wrong target',lambda v:v['spec'].update(TARGET_PATH='OTHER'))
reject('wrong bundle identity',lambda v:v['spec']['EXPECTED_BUNDLE_ID'].update(namespace='planner-snapshot-v1'))
reject('wrong hash',lambda v:v['spec'].update(EXPECTED_HASH='0'*64))
reject('wrong Snapshot',lambda v:v['spec']['EXPECTED_SNAPSHOT_ID'].update(sha256='0'*64))
reject('wrong P06 policy',lambda v:v['spec']['EXPECTED_POLICY_PIN']['identity'].update(sha256='0'*64))
reject('P05 substituted',lambda v:v.update(policy_version='E1-SELECTION-1-P05'))
reject('wrong replay scope',lambda v:v.update(scope='FULL_FROZEN_E1_REPLAY'))
reject('nonzero history',lambda v:v['events'].append({'event':'NEW'}))
reject('missing source',lambda v:v['spec']['EXPECTED_SOURCE_PINS'].pop())
reject('wrong source',lambda v:v['spec']['EXPECTED_SOURCE_PINS'][0]['identity'].update(sha256='0'*64))
reject('HEAD implicitly required',lambda v:v.update(HEAD_required=True))
reject('directory fsync claim introduced',lambda v:v.update(directory_fsync_claim=True))
reject('crash durability claim introduced',lambda v:v.update(crash_durability_claim=True))
reject('success based only on exit code',lambda v:v.update(success_predicate='EXIT_ZERO'))
reject('static guards treated satisfied',lambda v:v['spec'].update(RUNTIME_GUARDS_SATISFIED_NOW=True))
(O/'negative-suite.json').write_text(json.dumps({'STATUS':'PASS_STATIC_COLD_READER_GUARDS','COUNT':len(rows),'ROWS':rows,'MODE':'In-memory contract/schema tests; no actual runtime guard constructed and no reader operation invoked'},sort_keys=True,indent=2)+'\n')
print(json.dumps({'NEGATIVES':'PASS_STATIC','COUNT':len(rows)}))
