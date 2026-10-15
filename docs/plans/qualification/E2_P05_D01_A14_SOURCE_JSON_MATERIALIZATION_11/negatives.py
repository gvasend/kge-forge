"""Static candidate mutations only; accepted source remains unchanged."""
import hashlib,json
from copy import deepcopy
from pathlib import Path
from adapter.planner import codec,model
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;C10=O.parent/'E2_P05_D01_A14_SOURCE_JSON_RECOVERY_10'
def read(p):return json.loads(p.read_bytes())
s=read(C10/'bounded-materialization-subject.json');raw=(R/'source.json').read_bytes();snap=read(R/s['BASE_SNAPSHOT_SOURCE']['path'])['snapshot']
base={'bytes':raw,'hash':s['EXPECTED_SHA256'],'root':str(R),'path':'source.json','provenance':s['EXISTING_PROVENANCE_REFERENCES'],'snapshot':snap,'snapshot_id':s['BASE_SNAPSHOT_ID'],'retained_copy':s['AUTHORITATIVE_EXACT_BYTE_SOURCES'][0],'alias':False,'duplicate_key':False}
def validate(v):
 assert len(v['bytes'])==617 and v['bytes']==raw and hashlib.sha256(v['bytes']).hexdigest()==v['hash']==s['EXPECTED_SHA256']
 assert v['root']==str(R) and v['path']=='source.json';codec._path(Path(v['root']),v['path'])
 assert v['provenance']==s['EXISTING_PROVENANCE_REFERENCES'] and v['snapshot']==snap and not v['alias'] and not v['duplicate_key']
 assert codec._wire(codec.snapshot_id(codec._unwire(v['snapshot'])))==v['snapshot_id']==s['BASE_SNAPSHOT_ID']
 assert v['retained_copy'] in s['AUTHORITATIVE_EXACT_BYTE_SOURCES'] and (R/v['retained_copy']['path']).read_bytes()==v['bytes']
validate(base);rows=[]
def reject(name,fn):
 v=deepcopy(base);fn(v)
 try:validate(v)
 except (AssertionError,model.PlannerError) as e:rows.append({'CASE':name,'STATUS':'REJECTED','REASON':str(e) or 'exact byte/identity/provenance/Snapshot contract mismatch'})
 else:raise AssertionError(name)
reject('616-byte source',lambda v:v.update(bytes=raw[:-1]))
reject('618-byte source',lambda v:v.update(bytes=raw+b'\n'))
reject('one-byte mutation',lambda v:v.update(bytes=b'['+raw[1:]))
reject('semantic-equivalent reserialization',lambda v:v.update(bytes=json.dumps(json.loads(raw),indent=2).encode()))
reject('wrong retained copy',lambda v:v['retained_copy'].update(path='E2-DECIDE.json'))
reject('wrong hash',lambda v:v.update(hash='0'*64))
reject('wrong content identity',lambda v:v['provenance'][0]['PROVENANCE']['identity'].update(namespace='planner-snapshot-v1'))
reject('wrong path',lambda v:v.update(path='docs/source.json'))
reject('noncanonical path',lambda v:v.update(path='./source.json'))
reject('alternate filename',lambda v:v.update(path='source-copy.json'))
reject('wrong repository root',lambda v:v.update(root='/tmp'))
reject('repinned source',lambda v:v['provenance'][0]['PROVENANCE'].update(path='OTHER.json'))
reject('changed provenance',lambda v:v['provenance'][0]['PROVENANCE'].update(scope='OTHER'))
reject('changed authority',lambda v:v['snapshot']['entities'][0]['identity'].update(sha256='0'*64))
reject('changed Snapshot field',lambda v:v['snapshot']['context'].update(tick=1))
reject('changed Snapshot identity',lambda v:v['snapshot_id'].update(sha256='0'*64))
reject('report substituted',lambda v:v.update(bytes=b'{"result":"PASS"}'))
reject('E2-DECIDE substituted',lambda v:v.update(bytes=(R/'E2-DECIDE.json').read_bytes()))
correction=read(O.parent/'E2_P05_D01_A14_PROVENANCE_FIXTURE_CORRECTION_7/corrected-prospective-snapshot.json')['snapshot']
paths=[]
def walk(v):
 if isinstance(v,dict):
  if v.get('$type')=='Provenance' and 'E2_P05_D01_A14_PROSPECTIVE_SOURCE_CORRECTION_1/sources/' in v.get('path',''):paths.append(v['path'])
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
walk(correction)
choice=next(p for p in paths if '/choice-' in p);grant=next(p for p in paths if '/grant-' in p)
reject('choice source substituted',lambda v:v.update(bytes=(R/choice).read_bytes()))
reject('grant source substituted',lambda v:v.update(bytes=(R/grant).read_bytes()))
reject('source alias',lambda v:v.update(alias=True))
reject('duplicate raw pin key',lambda v:v.update(duplicate_key=True))
assert (R/'source.json').read_bytes()==raw
(O/'negative-suite.json').write_text(json.dumps({'STATUS':'PASS','COUNT':len(rows),'ROWS':rows,'MODE':'in-memory metadata/source candidate validation; no qualification case operations','ACCEPTED_SOURCE_UNCHANGED':True},sort_keys=True,indent=2)+'\n')
print(json.dumps({'NEGATIVES':'PASS','COUNT':len(rows)}))
