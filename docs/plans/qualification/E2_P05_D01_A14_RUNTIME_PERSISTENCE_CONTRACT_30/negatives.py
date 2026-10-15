"""Static sequence/authority/effect guards only; no runtime operation."""
import json
from copy import deepcopy
from pathlib import Path
O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_bytes())
i=read(O/'execution-input-manifest.json');g=read(O/'runtime-guards.json');sequence=read(O/'runtime-sequence.json')
base={'bundle':i['BUNDLE_ID'],'target':i['SAVE_TARGETS'][0]['TARGET_PATH'],'bytes':153602,'sequence':sequence['ORDERED_STEPS'],'guards':g['GUARDS'],'writer_exit_owner':'SUPERVISOR','reader_model':'FRESH_EXEC','reader_source':i['SAVE_TARGETS'][0]['TARGET_PATH'],'HEAD_mutated':False,'source_mutated':False,'policy_mutated':False,'A14_executed':False,'directory_fsync_claim':False,'crash_claim':False,'mode':'EMPTY_EVENT_HISTORICAL_VALIDATION','P06':i['POLICY_VERSION'],'replay_scope':i['NATIVE_REPLAY_SCOPE'],'events':[],'execution_authorized':False}
def validate(v):assert v==base
validate(base);rows=[]
def reject(name,fn):
 v=deepcopy(base);fn(v)
 try:validate(v)
 except AssertionError:rows.append({'CASE':name,'STATUS':'REJECTED'})
 else:raise AssertionError(name)
reject('wrong bundle',lambda v:v['bundle'].update(sha256='0'*64))
reject('wrong target',lambda v:v.update(target='OTHER'))
reject('wrong expected bytes',lambda v:v.update(bytes=153601))
reject('reader before save',lambda v:v['sequence'].insert(0,v['sequence'].pop(9)))
reject('reader before publication verification',lambda v:v['guards'][4].update(PREDECESSORS=[]))
reject('reader before writer exit',lambda v:v['guards'][4].update(PREDECESSORS=['G1_SAVE_RETURN']))
reject('writer self-attests exit',lambda v:v.update(writer_exit_owner='WRITER'))
reject('warm reader',lambda v:v.update(reader_model='WRITER_PROCESS'))
reject('wrong reader source',lambda v:v.update(reader_source='STATIC_CANDIDATE'))
reject('HEAD mutation',lambda v:v.update(HEAD_mutated=True))
reject('source mutation',lambda v:v.update(source_mutated=True))
reject('policy mutation',lambda v:v.update(policy_mutated=True))
reject('A14 execution',lambda v:v.update(A14_executed=True))
reject('directory fsync claim',lambda v:v.update(directory_fsync_claim=True))
reject('general crash durability claim',lambda v:v.update(crash_claim=True))
reject('replay converted to execution',lambda v:v.update(mode='NEW_LIFECYCLE_EXECUTION'))
reject('wrong P06 binding',lambda v:v.update(P06='E1-SELECTION-1-P05'))
reject('wrong replay scope',lambda v:v.update(replay_scope='FULL_FROZEN_E1_REPLAY'))
reject('nonzero history',lambda v:v['events'].append({'event':'NEW'}))
reject('execution before authority selected',lambda v:v.update(execution_authorized=True))
(O/'negative-suite.json').write_text(json.dumps({'STATUS':'PASS_STATIC_RUNTIME_CONTRACT_GUARDS','COUNT':len(rows),'ROWS':rows,'MODE':'In-memory plan/authority validation only; runtime guards remain unsatisfied'},sort_keys=True,indent=2)+'\n')
print(json.dumps({'NEGATIVES':'PASS_STATIC','COUNT':len(rows)}))
