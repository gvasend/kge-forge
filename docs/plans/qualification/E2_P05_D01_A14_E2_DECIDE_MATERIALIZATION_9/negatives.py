"""Static validation of rejected candidates; accepted source never modified."""
import hashlib,json
from copy import deepcopy
from pathlib import Path
from adapter.planner import codec,model
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification';C8=Q/'E2_P05_D01_A14_E2_DECIDE_SOURCE_RECOVERY_8'
def read(p):return json.loads(p.read_bytes())
subject=read(C8/'bounded-source-materialization-subject.json');source=R/'E2-DECIDE.json';raw=source.read_bytes();s=read(R/subject['BASE_CORRECTED_SNAPSHOT_SOURCE']['path'])['snapshot'];identity=subject['EXPECTED_RAW_IDENTITY']
base={'bytes':raw,'root':str(R),'path':'E2-DECIDE.json','provenance':deepcopy(subject['EXPECTED_EXISTING_PROVENANCE']),'snapshot':s,'snapshot_id':subject['BASE_CORRECTED_SNAPSHOT_ID'],'alias':False,'duplicate_raw_key':False,'embedded_source':subject['AUTHORITATIVE_EMBEDDED_BYTE_SOURCE']}
class Reject(ValueError):pass
def need(x,r):
 if not x:raise Reject(r)
def validate(v):
 need(len(v['bytes'])==90 and v['bytes']==raw,'BYTE_LENGTH_OR_EXACT_BYTES')
 need(hashlib.sha256(v['bytes']).hexdigest()==identity['sha256'],'WRONG_HASH')
 need(v['root']==str(R) and v['path']=='E2-DECIDE.json','WRONG_ROOT_OR_EXACT_TARGET')
 codec._path(Path(v['root']),v['path'])
 need(not v['alias'] and not v['duplicate_raw_key'],'ALIAS_OR_DUPLICATE_RAW_KEY')
 need(v['provenance']==subject['EXPECTED_EXISTING_PROVENANCE'],'PROVENANCE_OR_CONTENT_IDENTITY_REPIN')
 need(v['snapshot']==s,'SNAPSHOT_OR_AUTHORITY_OR_SCHEMA_CHANGED')
 actual=codec._wire(codec.snapshot_id(codec._unwire(v['snapshot'])));need(actual==v['snapshot_id']==subject['BASE_CORRECTED_SNAPSHOT_ID'],'SNAPSHOT_IDENTITY_CHANGED')
 need(v['embedded_source']==subject['AUTHORITATIVE_EMBEDDED_BYTE_SOURCE'],'WRONG_EMBEDDED_SOURCE')
 return True
validate(base);rows=[]
def reject(name,mutate):
 v=deepcopy(base);mutate(v)
 try:validate(v)
 except (Reject,model.PlannerError) as e:rows.append({'CASE':name,'STATUS':'REJECTED','REASON':str(e)})
 else:raise AssertionError(name)
reject('89-byte source',lambda v:v.update(bytes=raw[:-1]))
reject('91-byte source',lambda v:v.update(bytes=raw+b'\n'))
reject('one-byte mutation',lambda v:v.update(bytes=b'['+raw[1:]))
reject('semantic-equivalent reserialization',lambda v:v.update(bytes=json.dumps(json.loads(raw),indent=2).encode()))
reject('wrong hash',lambda v:v['provenance']['identity'].update(sha256='0'*64))
reject('wrong target path',lambda v:v.update(path='docs/E2-DECIDE.json'))
reject('alternate filename',lambda v:v.update(path='E2-DECIDE-copy.json'))
reject('wrong repository root',lambda v:v.update(root='/tmp'))
reject('repinned provenance',lambda v:v['provenance'].update(path='OTHER.json'))
reject('changed content identity',lambda v:v['provenance']['identity'].update(namespace='planner-snapshot-v1'))
reject('changed authority',lambda v:v['snapshot']['entities'][0]['identity'].update(sha256='0'*64))
reject('changed Snapshot field',lambda v:v['snapshot']['context'].update(tick=1))
reject('changed Snapshot identity',lambda v:v['snapshot_id'].update(sha256='0'*64))
reject('source alias',lambda v:v.update(alias=True))
reject('duplicate raw provenance key',lambda v:v.update(duplicate_raw_key=True))
reject('report text substituted',lambda v:v.update(bytes=b'{"result":"PASS"}'))
reject('different embedded provenance candidate',lambda v:v['embedded_source'].update(pointer='/snapshot/actions/1/source/excerpt'))
assert source.read_bytes()==raw
(O/'negative-suite.json').write_text(json.dumps({'STATUS':'PASS_17_STATIC_MATERIALIZATION_NEGATIVES','COUNT':len(rows),'ROWS':rows,'CANDIDATE_MUTATIONS_IN_MEMORY_ONLY':True,'ACCEPTED_SOURCE_FILE_UNCHANGED':True,'NO_NATIVE_TRANSITIONS_EXECUTED':True},sort_keys=True,indent=2)+'\n');print('MATERIALIZATION_NEGATIVES=17/17; ACTUAL_SOURCE_UNCHANGED')
