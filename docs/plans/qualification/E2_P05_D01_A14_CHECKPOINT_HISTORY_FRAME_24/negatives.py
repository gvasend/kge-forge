"""Frame metadata controls only; no event is created or applied."""
import json,hashlib
from copy import deepcopy
from pathlib import Path
O=Path(__file__).resolve().parent
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
p=json.loads((O/'prospective-checkpoint-frame.json').read_bytes());base=p['FRAME']
def validate(v):
 assert v==base and v['FRAME_TYPE']=='PROSPECTIVE_ZERO_EVENT_CHECKPOINT' and v['EVENT_COLLECTION']==[] and v['EVENT_COUNT']==0
 assert v['HISTORICAL_PARENT'] is None and v['LOCAL_LEDGER_ROOT'] is None and v['LOCAL_APPEND_HEAD'] is None and not v['HISTORICAL_OCCURRENCE_CLAIM'] and not v['HISTORICAL_ANCESTRY_CLAIM']
 assert 'qualification-A14-checkpoint-frame-v1:'+hashlib.sha256(canon(v)).hexdigest()==p['FRAME_IDENTITY']
validate(base);rows=[]
def reject(name,fn):
 v=deepcopy(base);fn(v)
 try:validate(v)
 except AssertionError:rows.append({'CASE':name,'STATUS':'REJECTED'})
 else:raise AssertionError(name)
reject('one event inserted',lambda v:v['EVENT_COLLECTION'].append({'event':'NEW'}))
reject('historical event copied',lambda v:v['EVENT_COLLECTION'].append({'event':'HISTORICAL'}))
reject('synthetic parent added',lambda v:v.update(HISTORICAL_PARENT='synthetic'))
reject('historical parent asserted',lambda v:v.update(HISTORICAL_PARENT='historical'))
reject('wrong Snapshot',lambda v:v['CHECKPOINT_STATE'].update(sha256='0'*64))
reject('equivalent different Snapshot identity',lambda v:v['CHECKPOINT_STATE'].update(sha256='91017c3947096a0470ba44aff95901872768fa205205d39c7bf60f840f848c9c'))
reject('missing source',lambda v:v['SOURCE_IDENTITIES'].pop())
reject('wrong source pin',lambda v:v['SOURCE_IDENTITIES'][0]['identity'].update(sha256='0'*64))
reject('wrong scope',lambda v:v.update(SCOPE='OTHER'))
reject('wrong lineage',lambda v:v.update(LINEAGE='OTHER'))
reject('wrong provenance',lambda v:v['PROVENANCE'].update(AUTHORIZATION_SUBJECT='OTHER'))
reject('historical occurrence claim',lambda v:v.update(HISTORICAL_OCCURRENCE_CLAIM=True))
reject('historical ancestry claim',lambda v:v.update(HISTORICAL_ANCESTRY_CLAIM=True))
reject('ledger root invented',lambda v:v.update(LOCAL_LEDGER_ROOT='root'))
reject('append head invented',lambda v:v.update(LOCAL_APPEND_HEAD='head'))
reject('historical PersistenceBundle representation',lambda v:v.update(FRAME_TYPE='PLANNER-BUNDLE-1'))
reject('genesis event inserted',lambda v:v['EVENT_COLLECTION'].append({'$type':'GenesisEvent'}))
reject('ledger position invented',lambda v:v.update(ledger_position=0))
reject('policy selection inserted into frame',lambda v:v.update(POLICY_VERSION_SELECTED=True))
reject('replay selection inserted into frame',lambda v:v.update(REPLAY_SCOPE_SELECTED=True))
(O/'negative-suite.json').write_text(json.dumps({'STATUS':'PASS_STATIC_FRAME_GUARDS','COUNT':len(rows),'ROWS':rows,'LIFECYCLE_EVENTS_CREATED':0,'MODE':'in-memory candidate metadata only'},sort_keys=True,indent=2)+'\n')
print(json.dumps({'NEGATIVES':'PASS_STATIC','COUNT':len(rows)}))
