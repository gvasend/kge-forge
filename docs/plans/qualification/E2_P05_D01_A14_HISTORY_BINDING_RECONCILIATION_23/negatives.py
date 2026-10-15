"""Static no-alias/no-invented-history controls; no native transitions."""
import json
from copy import deepcopy
from pathlib import Path
O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_bytes())
r=read(O/'snapshot-relationship.json');frame=read(O/'prospective-checkpoint-frame-proposal.json');h=read(O.parent/'E2_P05_D01_A14_BUNDLE_CONTRACT_CLOSURE_22/negative-history-control.json')
base={'old_end':r['ORIGINAL_A14_SNAPSHOT'],'corrected_end':r['CORRECTED_A14_SNAPSHOT'],'events':h['EVENTS'],'root':h['LEDGER_ROOT'],'lineage':h['CONTEXT']['lineage'],'generation':h['CONTEXT']['generation'],'policy':h['POLICY_VERSION'],'semantic_is_identity':False,'prospective_labeled_historical':False,'selected_policy':False,'invented_replay_range':False,'frame':frame}
def validate(v):
 assert v['old_end']==r['ORIGINAL_A14_SNAPSHOT'] and v['corrected_end']==r['CORRECTED_A14_SNAPSHOT'] and v['old_end']!=v['corrected_end']
 assert v['events']==h['EVENTS'] and v['root']==h['LEDGER_ROOT'] and v['lineage']==h['CONTEXT']['lineage'] and v['generation']==h['CONTEXT']['generation'] and v['policy']==h['POLICY_VERSION']
 assert not v['semantic_is_identity'] and not v['prospective_labeled_historical'] and not v['selected_policy'] and not v['invented_replay_range'] and v['frame']==frame
validate(base);rows=[]
def reject(name,fn):
 v=deepcopy(base);fn(v)
 try:validate(v)
 except AssertionError:rows.append({'CASE':name,'STATUS':'REJECTED'})
 else:raise AssertionError(name)
reject('original history relabeled corrected endpoint',lambda v:v.update(old_end=r['CORRECTED_A14_SNAPSHOT']))
reject('corrected Snapshot ID inserted in historical event',lambda v:v['events'][-1].update(AFTER_SNAPSHOT=r['CORRECTED_A14_SNAPSHOT']))
reject('historical parent rewritten',lambda v:v['events'][0]['PARENT_SNAPSHOT'].update(sha256='0'*64))
reject('historical ledger root rewritten',lambda v:v['root'].update(sha256='0'*64))
reject('semantic equivalence treated as native equality',lambda v:v.update(semantic_is_identity=True))
reject('prospective event labeled historical',lambda v:v.update(prospective_labeled_historical=True))
reject('wrong event order',lambda v:v['events'].reverse())
reject('missing event',lambda v:v['events'].pop())
reject('extra forbidden event',lambda v:v['events'].append(deepcopy(v['events'][-1])))
reject('wrong lineage',lambda v:v.update(lineage='FOREIGN'))
reject('wrong policy generation',lambda v:v.update(generation='FOREIGN'))
reject('replay range invented before selection',lambda v:v.update(invented_replay_range=True))
reject('policy selected before history compatibility',lambda v:v.update(selected_policy=True))
reject('unselected frame claimed historical reconstruction',lambda v:v['frame'].update(QUALIFICATION_TYPE='HISTORICAL_RECONSTRUCTION'))
(O/'negative-suite.json').write_text(json.dumps({'STATUS':'PASS_STATIC_METADATA_GUARDS','COUNT':len(rows),'ROWS':rows,'CONTROL':'Retained non-A14 history metadata only; no native replay or event creation'},sort_keys=True,indent=2)+'\n')
print(json.dumps({'NEGATIVES':'PASS_STATIC','COUNT':len(rows)}))
