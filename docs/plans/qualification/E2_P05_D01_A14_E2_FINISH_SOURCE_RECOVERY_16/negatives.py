"""Static in-memory fail-closed recovery/scope negatives."""
import hashlib,json
from copy import deepcopy
from pathlib import Path
from adapter.planner import codec,model
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_bytes())
s=read(O/'bounded-materialization-subject.json');raw=(R/s['ISOLATED_CANDIDATE']['path']).read_bytes();base={'bytes':raw,'hash':s['EXPECTED_SHA256'],'identity':s['EXPECTED_CONTENT_IDENTITY'],'path':'E2-FINISH.json','root':str(R),'recovery_source':s['AUTHORITATIVE_BYTE_SOURCE'],'lossless':True,'method':'RAW_DECODE','materialize':False,'repin':False,'later_materialize':False}
comparison=read(O/'historical-current-finish-comparison.json')
expected_action=comparison['A14_EXPECTED_FINISH_SOURCE']['NATIVE_ACTION_FIELDS']
base['action_contract']=expected_action
def validate(v):
 assert v['bytes']==raw and len(v['bytes'])==90 and hashlib.sha256(v['bytes']).hexdigest()==v['hash']==s['EXPECTED_SHA256']
 assert v['identity']==s['EXPECTED_CONTENT_IDENTITY'] and v['path']=='E2-FINISH.json' and v['root']==str(R);codec._path(R,v['path'])
 assert v['recovery_source']==s['AUTHORITATIVE_BYTE_SOURCE'] and v['lossless'] is True and v['method']=='RAW_DECODE'
 assert v['materialize'] is False and v['repin'] is False and v['later_materialize'] is False
 assert v['action_contract']==expected_action
validate(base);rows=[]
def reject(name,fn):
 v=deepcopy(base);fn(v)
 try:validate(v)
 except (AssertionError,model.PlannerError):rows.append({'CASE':name,'STATUS':'REJECTED'})
 else:raise AssertionError(name)
reject('current P04 FINISH substituted without byte identity',lambda v:v.update(bytes=(R/comparison['CURRENT_P04_PHYSICAL_SOURCE']['path']).read_bytes()))
reject('wrong FINISH version',lambda v:v.update(action_contract=comparison['CURRENT_P04_FINISH_DEFINITION']['NATIVE_ACTION_FIELDS']))
reject('wrong accepted inventory',lambda v:v['action_contract']['accepted_inventory'][0]['id'].update(value='E2-K-CHECK'))
reject('wrong E2-FINISH bytes',lambda v:v.update(bytes=raw[:-1]+b' '))
reject('semantic-equivalent byte-different JSON',lambda v:v.update(bytes=json.dumps(json.loads(raw),indent=2).encode()))
reject('wrong hash',lambda v:v.update(hash='0'*64))
reject('wrong content identity',lambda v:v['identity'].update(namespace='planner-snapshot-v1'))
reject('wrong path',lambda v:v.update(path='other/E2-FINISH.json'))
reject('noncanonical path',lambda v:v.update(path='./E2-FINISH.json'))
reject('wrong root',lambda v:v.update(root='/tmp'))
reject('wrong retained candidate',lambda v:v['recovery_source'].update(pointer='/snapshot/actions/0/source/excerpt'))
reject('lossy embedded representation',lambda v:v.update(lossless=False))
reject('report substituted',lambda v:v.update(bytes=b'{"result":"PASS"}'))
reject('E2-COLLECT substituted',lambda v:v.update(bytes=(R/'E2-COLLECT.json').read_bytes()))
reject('E2-CHECK substituted',lambda v:v.update(bytes=(R/'E2-CHECK.json').read_bytes()))
reject('E2-DECIDE substituted',lambda v:v.update(bytes=(R/'E2-DECIDE.json').read_bytes()))
reject('source.json substituted',lambda v:v.update(bytes=(R/'source.json').read_bytes()))
sp=read(R/s['BASE_SNAPSHOT_SOURCE']['path']);paths=[]
def walk(v):
 if isinstance(v,dict):
  if v.get('$type')=='Provenance' and 'E2_P05_D01_A14_PROSPECTIVE_SOURCE_CORRECTION_1/sources/' in v.get('path',''):paths.append(v['path'])
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
walk(sp)
reject('choice source substituted',lambda v:v.update(bytes=(R/next(p for p in paths if '/choice-' in p)).read_bytes()))
reject('grant source substituted',lambda v:v.update(bytes=(R/next(p for p in paths if '/grant-' in p)).read_bytes()))
reject('unauthorized materialization',lambda v:v.update(materialize=True))
reject('hidden repinning',lambda v:v.update(repin=True))
reject('later missing source materialized under E2-FINISH authority',lambda v:v.update(later_materialize=True))
reject('unverified regeneration',lambda v:v.update(method='SEMANTIC_REGENERATION'))
assert not (R/'E2-FINISH.json').exists()
(O/'negative-suite.json').write_text(json.dumps({'STATUS':'PASS','COUNT':len(rows),'ROWS':rows,'MODE':'in-memory recovery and scope metadata validation; no source materialization or native transition'},sort_keys=True,indent=2)+'\n')
print(json.dumps({'NEGATIVES':'PASS','COUNT':len(rows)}))
