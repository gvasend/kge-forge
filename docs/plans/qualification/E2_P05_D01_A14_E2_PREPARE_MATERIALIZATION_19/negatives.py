"""In-memory fail-closed materialization negatives; accepted files untouched."""
import hashlib,json
from copy import deepcopy
from pathlib import Path
from adapter.planner import codec,model
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;C18=O.parent/'E2_P05_D01_A14_E2_PREPARE_SOURCE_RECOVERY_18'
def read(p):return json.loads(p.read_bytes())
s=read(C18/'bounded-materialization-subject.json');raw=(R/'E2-PREPARE.json').read_bytes();snapshot=read(R/s['BASE_SNAPSHOT_SOURCE']['path'])['snapshot']
comparison=read(R/s['HISTORICAL_CURRENT_PREPARE_COMPARISON']['path'])
base={'bytes':raw,'hash':s['EXPECTED_SHA256'],'identity':s['EXPECTED_CONTENT_IDENTITY'],'root':str(R),'path':'E2-PREPARE.json','provenance':s['EXISTING_PROVENANCE'],'snapshot':snapshot,'snapshot_id':s['BASE_SNAPSHOT_ID'],'later_source_materialized':False,'alias':False,'duplicate_key':False}
base['action_contract']=comparison['A14_EXPECTED_PREPARE_SOURCE']['NATIVE_ACTION_FIELDS']
def validate(v):
 assert len(v['bytes'])==91 and v['bytes']==raw and hashlib.sha256(v['bytes']).hexdigest()==v['hash']==s['EXPECTED_SHA256']
 assert v['identity']==s['EXPECTED_CONTENT_IDENTITY'] and v['root']==str(R) and v['path']=='E2-PREPARE.json';codec._path(Path(v['root']),v['path'])
 assert v['provenance']==s['EXISTING_PROVENANCE'] and v['snapshot']==snapshot
 assert codec._wire(codec.snapshot_id(codec._unwire(v['snapshot'])))==v['snapshot_id']==s['BASE_SNAPSHOT_ID']
 assert v['later_source_materialized'] is False and not v['alias'] and not v['duplicate_key']
 assert v['action_contract']==comparison['A14_EXPECTED_PREPARE_SOURCE']['NATIVE_ACTION_FIELDS']
validate(base);rows=[]
def reject(name,fn):
 v=deepcopy(base);fn(v)
 try:validate(v)
 except (AssertionError,model.PlannerError):rows.append({'CASE':name,'STATUS':'REJECTED'})
 else:raise AssertionError(name)
reject('90-byte source',lambda v:v.update(bytes=raw[:-1]))
reject('92-byte source',lambda v:v.update(bytes=raw+b'\n'))
reject('one-byte mutation',lambda v:v.update(bytes=b'['+raw[1:]))
reject('current P04 PREPARE substituted',lambda v:v.update(bytes=(R/comparison['CURRENT_P04_PHYSICAL_SOURCE']['path']).read_bytes()))
reject('wrong PREPARE version',lambda v:v.update(action_contract=comparison['CURRENT_P04_PREPARE_DEFINITION']['NATIVE_ACTION_FIELDS']))
reject('semantic-equivalent byte-different JSON',lambda v:v.update(bytes=json.dumps(json.loads(raw),indent=2).encode()))
reject('wrong hash',lambda v:v.update(hash='0'*64))
reject('wrong content identity',lambda v:v['identity'].update(namespace='planner-snapshot-v1'))
reject('wrong path',lambda v:v.update(path='docs/E2-PREPARE.json'))
reject('noncanonical path',lambda v:v.update(path='./E2-PREPARE.json'))
reject('alternate filename',lambda v:v.update(path='E2-PREPARE-copy.json'))
reject('wrong repository root',lambda v:v.update(root='/tmp'))
reject('repinning',lambda v:v['provenance'][0]['PROVENANCE'].update(path='OTHER.json'))
reject('changed provenance',lambda v:v['provenance'][0]['PROVENANCE'].update(scope='OTHER'))
reject('changed authority',lambda v:v['snapshot']['entities'][0]['identity'].update(sha256='0'*64))
reject('changed Snapshot field',lambda v:v['snapshot']['context'].update(tick=1))
reject('changed Snapshot identity',lambda v:v['snapshot_id'].update(sha256='0'*64))
reject('E2-FINISH substitution',lambda v:v.update(bytes=(R/'E2-FINISH.json').read_bytes()))
reject('E2-COLLECT substitution',lambda v:v.update(bytes=(R/'E2-COLLECT.json').read_bytes()))
reject('E2-CHECK substitution',lambda v:v.update(bytes=(R/'E2-CHECK.json').read_bytes()))
reject('E2-DECIDE substitution',lambda v:v.update(bytes=(R/'E2-DECIDE.json').read_bytes()))
reject('source.json substitution',lambda v:v.update(bytes=(R/'source.json').read_bytes()))
reject('report substituted for source',lambda v:v.update(bytes=b'{"result":"PASS"}'))
reject('later missing source materialized under authorization',lambda v:v.update(later_source_materialized=True))
reject('source alias',lambda v:v.update(alias=True))
reject('duplicate raw pin key',lambda v:v.update(duplicate_key=True))
assert (R/'E2-PREPARE.json').read_bytes()==raw
(O/'negative-suite.json').write_text(json.dumps({'STATUS':'PASS','COUNT':len(rows),'ROWS':rows,'MODE':'static in-memory candidate validation; no qualification operation or physical mutation','ACCEPTED_SOURCE_UNCHANGED':True},sort_keys=True,indent=2)+'\n')
print(json.dumps({'NEGATIVES':'PASS','COUNT':len(rows)}))
