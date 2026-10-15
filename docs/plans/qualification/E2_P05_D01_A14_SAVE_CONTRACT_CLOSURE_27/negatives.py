"""Static save-input/target/serializer/output controls; never call save_bundle."""
import json,hashlib
from copy import deepcopy
from pathlib import Path
from adapter.planner import codec
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_bytes())
c=read(O/'save-contract.json');input=read(O/'save-input-pin.json');raw=(R/input['INPUT_SOURCE']['path']).read_bytes();bundle=read(R/input['INPUT_SOURCE']['path']);targets=c['SAVE_TARGETS']
base={'bundle':bundle,'identity':input['INPUT_BUNDLE_ID'],'target':targets[0]['EXPECTED_TARGET'],'format':'PLANNER-BUNDLE-1','serializer':'codec.bundle_bytes','bytes':raw,'scope':c['HANDOFF']['SCOPE'],'lineage':c['HANDOFF']['LINEAGE'],'provenance':c['HANDOFF']['PROVENANCE'],'conflicting_target':False,'lifecycle_advance':False,'operation':'save_bundle_contract_only','ordered_semantics':'ORDERED_EVENTS'}
def validate(v):
 b=v['bundle']['bundle'];assert b['events']==[] and b['initial']==bundle['bundle']['initial'] and b['current']==bundle['bundle']['current'] and b['policy']==bundle['bundle']['policy'] and b['policy_version']=='E1-SELECTION-1-P06' and b['scope']=='PARTIAL_HISTORICAL_REPLAY'
 assert len(b['sources'])==10 and v['identity']==input['INPUT_BUNDLE_ID'];encoded=codec.bundle_bytes(codec._unwire(b));assert encoded==raw==v['bytes'] and hashlib.sha256(encoded).hexdigest()==v['identity']['sha256']
 assert v['target']==targets[0]['EXPECTED_TARGET'] and v['format']=='PLANNER-BUNDLE-1' and v['serializer']=='codec.bundle_bytes'
 assert v['scope']==c['HANDOFF']['SCOPE'] and v['lineage']==c['HANDOFF']['LINEAGE'] and v['provenance']==c['HANDOFF']['PROVENANCE'] and not v['conflicting_target'] and not v['lifecycle_advance'] and v['operation']=='save_bundle_contract_only' and v['ordered_semantics']=='ORDERED_EVENTS'
validate(base);rows=[]
def reject(name,fn):
 v=deepcopy(base);fn(v)
 try:validate(v)
 except (AssertionError,ValueError,TypeError):rows.append({'CASE':name,'STATUS':'REJECTED'})
 else:raise AssertionError(name)
reject('wrong bundle',lambda v:v['bundle']['bundle'].update(policy_version='E1-SELECTION-1-P05'))
reject('equivalent different native bundle identity',lambda v:v['identity'].update(sha256='0'*64))
reject('wrong Snapshot',lambda v:v['bundle']['bundle']['current']['context'].update(tick=1))
reject('wrong P06 policy',lambda v:v['bundle']['bundle']['policy']['identity'].update(sha256='0'*64))
reject('wrong replay scope',lambda v:v['bundle']['bundle'].update(scope='FULL_FROZEN_E1_REPLAY'))
reject('nonzero history',lambda v:v['bundle']['bundle']['events'].append({'event':'NEW'}))
reject('missing source',lambda v:v['bundle']['bundle']['sources'].pop())
reject('wrong target',lambda v:v.update(target='/tmp/other/bundle.json'))
reject('noncanonical target',lambda v:v.update(target=v['target']+'/../other'))
reject('wrong serializer',lambda v:v.update(serializer='json.dumps'))
reject('wrong format',lambda v:v.update(format='REPORT-JSON'))
reject('wrong save identity',lambda v:v['identity'].update(namespace='planner-snapshot-v1'))
reject('partial representation',lambda v:v.update(bytes=raw[:-1]))
reject('ordered field reordered',lambda v:v['bundle']['bundle']['events'].append({'reordered':'history'}))
reject('unordered presentation treated as different identity',lambda v:v['identity'].update(sha256='1'*64))
reject('existing conflicting target',lambda v:v.update(conflicting_target=True))
reject('wrong scope',lambda v:v.update(scope='OTHER'))
reject('wrong lineage',lambda v:v.update(lineage='OTHER'))
reject('wrong provenance',lambda v:v.update(provenance=[]))
reject('save advances lifecycle',lambda v:v.update(lifecycle_advance=True))
reject('cold-reader invocation substituted for save',lambda v:v.update(operation='restore'))
reject('ordered history normalized as unordered',lambda v:v.update(ordered_semantics='UNORDERED_EVENTS'))
permuted=deepcopy(base);permuted['bundle']['bundle']['sources'].reverse();validate(permuted)
(O/'negative-suite.json').write_text(json.dumps({'STATUS':'PASS_STATIC_SAVE_CONTRACT_GUARDS','COUNT':len(rows),'ROWS':rows,'UNORDERED_PRESENTATION':'ACCEPTED_IDENTICAL_NATIVE_BYTES','LIMIT':'Contract/metadata controls only; no target mutation, write failure injection or save/restore operations','SAVES_PERFORMED':0},sort_keys=True,indent=2)+'\n')
print(json.dumps({'NEGATIVES':'PASS_STATIC','COUNT':len(rows)}))
