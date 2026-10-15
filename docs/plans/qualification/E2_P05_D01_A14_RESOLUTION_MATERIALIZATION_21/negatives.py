"""Materialization and sealed recovery controls, in-memory only."""
import hashlib,json
from copy import deepcopy
from pathlib import Path
from adapter.planner import codec,model
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;C20=O.parent/'E2_P05_D01_A14_RESOLUTION_SOURCE_RECOVERY_20'
def read(p):return json.loads(p.read_bytes())
s=read(C20/'bounded-materialization-subject.json');raw=(R/'resolution.json').read_bytes();snapshot=read(R/s['BASE_SNAPSHOT_SOURCE']['path'])['snapshot']
base={'bytes':raw,'hash':s['EXPECTED_SHA256'],'identity':s['EXPECTED_CONTENT_IDENTITY'],'path':'resolution.json','root':str(R),'provenance':s['EXISTING_PROVENANCE'],'snapshot':snapshot,'snapshot_id':s['BASE_SNAPSHOT_ID'],'recovery_source':s['AUTHORITATIVE_BYTE_SOURCE'],'lossless':True,'method':'RAW_DECODE','repin':False,'authorized_option':'AUTHORIZE_BOUNDED_A14_RESOLUTION_LOSSLESS_SOURCE_MATERIALIZATION','promoted':0,'bundle_ready':False,'alias':False,'duplicate_key':False}
base['sealed_source_oracle']=read(R/s['POST_MATERIALIZATION_SOURCE_ORACLE']['path'])
def validate(v):
 assert len(v['bytes'])==1430 and v['bytes']==raw and hashlib.sha256(v['bytes']).hexdigest()==v['hash']==s['EXPECTED_SHA256']
 assert v['identity']==s['EXPECTED_CONTENT_IDENTITY'] and v['path']=='resolution.json' and v['root']==str(R);codec._path(R,v['path'])
 assert v['provenance']==s['EXISTING_PROVENANCE'] and v['snapshot']==snapshot and codec._wire(codec.snapshot_id(codec._unwire(v['snapshot'])))==v['snapshot_id']==s['BASE_SNAPSHOT_ID']
 assert v['recovery_source']==s['AUTHORITATIVE_BYTE_SOURCE'] and v['lossless'] and v['method']=='RAW_DECODE' and not v['repin']
 assert v['authorized_option']=='AUTHORIZE_BOUNDED_A14_RESOLUTION_LOSSLESS_SOURCE_MATERIALIZATION' and v['promoted']==0 and not v['bundle_ready'] and not v['alias'] and not v['duplicate_key']
 assert v['sealed_source_oracle']==base['sealed_source_oracle'] and v['sealed_source_oracle']['NOT_CURRENT_RESULT'] is True
validate(base);rows=[]
def reject(name,fn):
 v=deepcopy(base);fn(v)
 try:validate(v)
 except (AssertionError,model.PlannerError):rows.append({'CASE':name,'STATUS':'REJECTED'})
 else:raise AssertionError(name)
reject('1429-byte source',lambda v:v.update(bytes=raw[:-1]))
reject('1431-byte source',lambda v:v.update(bytes=raw+b'\n'))
reject('one-byte mutation',lambda v:v.update(bytes=b'['+raw[1:]))
reject('semantic-equivalent byte-different JSON',lambda v:v.update(bytes=json.dumps(json.loads(raw),indent=2).encode()))
reject('wrong hash',lambda v:v.update(hash='0'*64))
reject('wrong content identity',lambda v:v['identity'].update(namespace='planner-snapshot-v1'))
reject('wrong path',lambda v:v.update(path='other/resolution.json'))
reject('noncanonical path',lambda v:v.update(path='./resolution.json'))
reject('alternate filename',lambda v:v.update(path='resolution-copy.json'))
reject('wrong root',lambda v:v.update(root='/tmp'))
reject('repinning',lambda v:v.update(repin=True))
reject('changed provenance',lambda v:v['provenance'][0]['PROVENANCE'].update(scope='OTHER'))
reject('changed Snapshot field',lambda v:v['snapshot']['context'].update(tick=1))
reject('changed Snapshot identity',lambda v:v['snapshot_id'].update(sha256='0'*64))
reject('report substituted',lambda v:v.update(bytes=b'{"result":"PASS"}'))
reject('another A14 source substituted',lambda v:v.update(bytes=(R/'source.json').read_bytes()))
reject('wrong retained candidate',lambda v:v['recovery_source'].update(pointer='/snapshot/actions/0/source/excerpt'))
reject('lossy embedded representation',lambda v:v.update(lossless=False))
reject('unverified semantic regeneration',lambda v:v.update(method='SEMANTIC_PROJECTION'))
reject('unauthorized materialization option',lambda v:v.update(authorized_option='AUTHORIZE_E2_PREPARE'))
reject('operand promotion from source closure alone',lambda v:v.update(promoted=1))
reject('10/10 sources treated as complete bundle',lambda v:v.update(bundle_ready=True))
reject('source alias',lambda v:v.update(alias=True))
reject('duplicate raw pin key',lambda v:v.update(duplicate_key=True))
reject('missing pin in sealed ten-source oracle',lambda v:v['sealed_source_oracle']['ROWS'].pop())
reject('historical future oracle rewritten as actual result',lambda v:v['sealed_source_oracle'].update(NOT_CURRENT_RESULT=False))
assert (R/'resolution.json').read_bytes()==raw
(O/'materialization-negatives.json').write_text(json.dumps({'STATUS':'PASS','COUNT':len(rows),'ROWS':rows,'SEALED_RECOVERY_CONTROL_MAPPING':'Exact bytes/hash/domain/path/pointer/lossless/substitution/authorization/repinning guards retained; premature 10/10 control superseded by actual complete-source validation. Premature operand promotion and future-oracle currentness boundaries preserved.','MODE':'Static in-memory candidates only; actual sources unchanged'},sort_keys=True,indent=2)+'\n')
print(json.dumps({'NEGATIVES':'PASS','COUNT':len(rows)}))
