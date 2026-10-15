"""Fail-closed binding and native empty-bundle controls; never apply an event."""
import json,hashlib
from copy import deepcopy
from pathlib import Path
from adapter.planner import codec,model
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_bytes())
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
policy=read(O/'p06-policy-binding.json')['BINDING'];scope=read(O/'replay-scope-binding.json')['BINDING'];expected=read(O/'prospective-a14-bundle.json');bid=read(O/'bundle-validation.json')['BUNDLE_ID']
base={'policy':policy,'scope':scope,'bundle':expected,'policies_selected':['P06'],'mode':'READ_ONLY_EMPTY_FOLD','normalization':{'sources':'UNORDERED','events':'ORDERED'},'native_identity':bid}
def validate(v):
 assert v['policies_selected']==['P06'] and v['policy']==policy and v['scope']==scope
 assert v['mode']=='READ_ONLY_EMPTY_FOLD' and v['normalization']=={'sources':'UNORDERED','events':'ORDERED'} and v['native_identity']==bid
 b=v['bundle']['bundle'];assert b['events']==[] # Guard before native decoder/replay.
 assert b['initial']==expected['bundle']['initial'] and b['current']==expected['bundle']['current']
 assert b['policy']==expected['bundle']['policy'] and b['policy_version']=='E1-SELECTION-1-P06' and b['scope']=='PARTIAL_HISTORICAL_REPLAY'
 assert len(b['sources'])==10 and sorted(b['sources'],key=canon)==sorted(expected['bundle']['sources'],key=canon)
 native=codec._unwire(b);raw=codec.bundle_bytes(native);codec._verify_sources(native,R);assert codec._wire(codec._identity(raw,'planner-bundle-v1'))==bid
validate(base);rows=[]
def reject(name,fn):
 v=deepcopy(base);fn(v)
 try:validate(v)
 except (AssertionError,model.PlannerError,ValueError,TypeError):rows.append({'CASE':name,'STATUS':'REJECTED'})
 else:raise AssertionError(name)
reject('P05 silently selected',lambda v:v.update(policies_selected=['P05']))
reject('both policies selected',lambda v:v.update(policies_selected=['P05','P06']))
reject('no policy selected',lambda v:v.update(policies_selected=[]))
reject('wrong P06 version',lambda v:v['policy'].update(VERSION='E1-SELECTION-1-P05'))
reject('wrong policy source',lambda v:v['policy']['SOURCE']['identity'].update(sha256='0'*64))
reject('wrong configuration identity',lambda v:v['policy']['CONFIGURATION_IDENTITY'].update(SHA256='0'*64))
reject('wrong generation',lambda v:v['policy'].update(GENERATION='OTHER'))
reject('wrong frame',lambda v:v['policy'].update(FRAME_IDENTITY='OTHER'))
reject('wrong Snapshot',lambda v:v['policy']['CHECKPOINT'].update(sha256='0'*64))
reject('wrong scope',lambda v:v['policy'].update(SCOPE='OTHER'))
reject('wrong lineage',lambda v:v['policy'].update(LINEAGE='OTHER'))
reject('ranking rule change',lambda v:v['policy']['CONFIGURATION']['rules'].append('NEW'))
reject('historical lineage binding',lambda v:v['policy'].update(HISTORICAL_ANCESTRY_BOUND=True))
reject('nonempty replay event range',lambda v:v['scope']['EVENTS'].append({'event':'NEW'}))
reject('historical event in replay',lambda v:v['scope']['EVENTS'].append({'event':'HISTORICAL'}))
reject('wrong replay checkpoint',lambda v:v['scope']['CURRENT_SNAPSHOT'].update(sha256='0'*64))
reject('P05 replay substitution',lambda v:v['scope'].update(POLICY_VERSION='E1-SELECTION-1-P05'))
reject('missing replay source',lambda v:v['scope']['SOURCE_SET'].pop())
reject('extra replay source',lambda v:v['scope']['SOURCE_SET'].append(deepcopy(v['scope']['SOURCE_SET'][0])))
reject('wrong replay provenance',lambda v:v['scope']['PROVENANCE'].update(AUTHORIZATION_SUBJECT='OTHER'))
reject('replay start changed',lambda v:v['scope']['INITIAL_SNAPSHOT'].update(sha256='0'*64))
reject('replay end changed',lambda v:v['scope']['CURRENT_SNAPSHOT'].update(sha256='0'*64))
reject('reexecution instead of replay',lambda v:v.update(mode='LIVE_EXECUTION'))
reject('wrong bundle Snapshot',lambda v:v['bundle']['bundle']['current']['context'].update(tick=1))
reject('missing bundle source',lambda v:v['bundle']['bundle']['sources'].pop())
reject('wrong bundle source',lambda v:v['bundle']['bundle']['sources'][0]['identity'].update(sha256='0'*64))
reject('P05 native bundle substituted',lambda v:v['bundle']['bundle'].update(policy_version='E1-SELECTION-1-P05'))
reject('nonzero bundle history',lambda v:v['bundle']['bundle']['events'].append({'event':'NEW'}))
reject('historical parent inserted',lambda v:v['bundle']['bundle']['events'].append({'parent_event':'OLD'}))
reject('wrong native replay scope',lambda v:v['bundle']['bundle'].update(scope='FULL_FROZEN_E1_REPLAY'))
reject('wrong bundle generation',lambda v:v['bundle']['bundle']['initial']['context'].update(generation='OTHER'))
reject('wrong bundle scope',lambda v:v['bundle']['bundle']['initial']['context'].update(scope='OTHER'))
reject('wrong bundle lineage',lambda v:v['bundle']['bundle']['initial']['context'].update(lineage='OTHER'))
reject('wrong bundle provenance',lambda v:v['bundle']['bundle']['initial']['actions'][0]['source'].update(method='OTHER'))
reject('unordered presentation declared different identity',lambda v:v['native_identity'].update(sha256='0'*64))
reject('ordered history treated as unordered',lambda v:v['normalization'].update(events='UNORDERED'))
permuted=deepcopy(base);permuted['bundle']['bundle']['sources'].reverse();validate(permuted)
(O/'negative-suite.json').write_text(json.dumps({'STATUS':'PASS_BINDING_AND_NATIVE_EMPTY_BUNDLE_GUARDS','COUNT':len(rows),'ROWS':rows,'UNORDERED_PRESENTATION':'ACCEPTED_IDENTICAL_NATIVE_IDENTITY','ORDERED_HISTORY':'Must remain ordered by schema; nonempty histories rejected before any replay call','NATIVE_EVENT_APPLICATIONS':0,'SAVE_RESTORE_EXECUTED':False},sort_keys=True,indent=2)+'\n')
print(json.dumps({'NEGATIVES':'PASS','COUNT':len(rows),'PERMUTATION':'PASS'}))
