"""Static contract/metadata negatives; control is not an A14 candidate."""
import json,hashlib
from copy import deepcopy
from pathlib import Path
from adapter.planner import codec,selector,model
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_bytes())
h=read(O/'negative-history-control.json');source=read(O/'frozen-ten-sources.json')['ROWS'][0]
base={'initial':h['START_STATE'],'end':h['END_STATE'],'events':h['EVENTS'],'root':h['LEDGER_ROOT'],'head':h['APPEND_HEAD'],'policy':codec._wire(selector.POLICY_PIN),'policy_version':h['POLICY_VERSION'],'replay_scope':h['REPLAY_SCOPE'],'replay_start':h['START_STATE'],'replay_end':h['END_STATE'],'generation':h['CONTEXT']['generation'],'scope':h['CONTEXT']['scope'],'lineage':h['CONTEXT']['lineage'],'mode':'HISTORICAL_REPLAY_METADATA_ONLY','source_pin':source['PIN'],'claim_A14_bundle_selected':False}
def validate(v):
 assert v['initial']==h['START_STATE'] and v['end']==h['END_STATE']
 selector.validate_policy(codec._unwire(v['policy']),v['policy_version']);assert v['policy_version']==h['POLICY_VERSION']
 assert v['events']==h['EVENTS'] and v['root']==h['LEDGER_ROOT'] and v['head']==h['APPEND_HEAD']
 previous=None;parent=v['initial']
 for i,e in enumerate(v['events'],1):
  assert e['POSITION']==i and e['PARENT_SNAPSHOT']==parent and e['PARENT_EVENT']==previous
  previous=e['EVENT_ID'];parent=e['AFTER_SNAPSHOT']
 assert parent==v['end'] and v['replay_start']==v['initial'] and v['replay_end']==v['end'] and v['replay_scope']==h['REPLAY_SCOPE']
 assert v['generation']==h['CONTEXT']['generation'] and v['scope']==h['CONTEXT']['scope'] and v['lineage']==h['CONTEXT']['lineage']
 assert v['mode']=='HISTORICAL_REPLAY_METADATA_ONLY' and v['source_pin']==source['PIN'] and v['claim_A14_bundle_selected'] is False
validate(base);rows=[]
def reject(name,fn):
 v=deepcopy(base);fn(v)
 try:validate(v)
 except (AssertionError,model.PlannerError):rows.append({'CASE':name,'STATUS':'REJECTED'})
 else:raise AssertionError(name)
reject('wrong initial state',lambda v:v['initial'].update(sha256='0'*64))
reject('later state substituted for initial',lambda v:v.update(initial=h['END_STATE']))
reject('wrong policy',lambda v:v['policy']['identity'].update(sha256='0'*64))
reject('different current policy substituted for declared historical version',lambda v:v.update(policy_version='E1-SELECTION-1-P06' if h['POLICY_VERSION']!='E1-SELECTION-1-P06' else 'E1-SELECTION-1-P05'))
reject('wrong policy version',lambda v:v.update(policy_version='UNKNOWN'))
reject('missing history event',lambda v:v['events'].pop())
reject('extra history event',lambda v:v['events'].append(deepcopy(v['events'][-1])))
reject('reordered history',lambda v:v['events'].reverse())
reject('wrong parent',lambda v:v['events'][1]['PARENT_SNAPSHOT'].update(sha256='0'*64))
reject('wrong ledger position',lambda v:v['events'][0].update(POSITION=2))
reject('wrong ledger root/head',lambda v:v['head'].update(sha256='0'*64))
reject('foreign history',lambda v:v['events'][0]['EVENT_ID'].update(namespace='FOREIGN'))
reject('wrong replay start',lambda v:v['replay_start'].update(sha256='0'*64))
reject('wrong replay end',lambda v:v['replay_end'].update(sha256='0'*64))
reject('replay scope omits required event',lambda v:v['events'].pop(0))
reject('replay includes forbidden later event',lambda v:v['events'].append(deepcopy(v['events'][-1])))
reject('reexecution substituted for replay',lambda v:v.update(mode='LIVE_EXECUTION'))
reject('wrong source pin',lambda v:v['source_pin']['identity'].update(sha256='0'*64))
reject('mixed generation',lambda v:v.update(generation='OTHER'))
reject('wrong scope',lambda v:v.update(scope='OTHER'))
reject('wrong lineage',lambda v:v.update(lineage='OTHER'))
reject('unselected A14 bundle claimed complete',lambda v:v.update(claim_A14_bundle_selected=True))
(O/'negative-suite.json').write_text(json.dumps({'STATUS':'PASS_STATIC_CONTRACT_GUARDS','COUNT':len(rows),'ROWS':rows,'CONTROL_SOURCE':h['SOURCE'],'LIMITATION':'Retained native-chain metadata and exact declared binding guards only. This control is foreign to corrected A14, not selected as its bundle; no A14 native bundle validation or replay was executed.'},sort_keys=True,indent=2)+'\n')
print(json.dumps({'NEGATIVES':'PASS_STATIC','COUNT':len(rows)}))
