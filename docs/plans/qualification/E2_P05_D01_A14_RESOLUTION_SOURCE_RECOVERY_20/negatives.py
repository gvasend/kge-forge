"""In-memory recovery and future/current-boundary guards."""
import hashlib,json
from copy import deepcopy
from pathlib import Path
from adapter.planner import codec,model
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_bytes())
s=read(O/'bounded-materialization-subject.json');raw=(R/s['ISOLATED_CANDIDATE']['path']).read_bytes();base={'bytes':raw,'hash':s['EXPECTED_SHA256'],'identity':s['EXPECTED_CONTENT_IDENTITY'],'path':'resolution.json','root':str(R),'recovery_source':s['AUTHORITATIVE_BYTE_SOURCE'],'lossless':True,'method':'RAW_DECODE','materialize':False,'repin':False,'current_present':9,'promoted_operands':0,'future_oracle':read(O/'post-materialization-source-oracle.json')}
def validate(v):
 assert v['bytes']==raw and len(v['bytes'])==1430 and hashlib.sha256(v['bytes']).hexdigest()==v['hash']==s['EXPECTED_SHA256']
 assert v['identity']==s['EXPECTED_CONTENT_IDENTITY'] and v['path']=='resolution.json' and v['root']==str(R);codec._path(R,v['path'])
 assert v['recovery_source']==s['AUTHORITATIVE_BYTE_SOURCE'] and v['lossless'] is True and v['method']=='RAW_DECODE'
 assert v['materialize'] is False and v['repin'] is False and v['current_present']==9 and v['promoted_operands']==0
 assert v['future_oracle']==base['future_oracle'] and v['future_oracle']['NOT_CURRENT_RESULT'] is True
validate(base);rows=[]
def reject(name,fn):
 v=deepcopy(base);fn(v)
 try:validate(v)
 except (AssertionError,model.PlannerError):rows.append({'CASE':name,'STATUS':'REJECTED'})
 else:raise AssertionError(name)
reject('wrong resolution bytes',lambda v:v.update(bytes=raw[:-1]+b' '))
reject('semantic-equivalent byte-different JSON',lambda v:v.update(bytes=json.dumps(json.loads(raw),indent=2).encode()))
reject('wrong hash',lambda v:v.update(hash='0'*64))
reject('wrong content identity',lambda v:v['identity'].update(namespace='planner-snapshot-v1'))
reject('wrong path',lambda v:v.update(path='other/resolution.json'))
reject('noncanonical path',lambda v:v.update(path='./resolution.json'))
reject('wrong repository root',lambda v:v.update(root='/tmp'))
reject('wrong retained candidate',lambda v:v['recovery_source'].update(pointer='/snapshot/actions/0/source/excerpt'))
reject('lossy embedded representation',lambda v:v.update(lossless=False))
reject('report substituted for source',lambda v:v.update(bytes=b'{"result":"PASS"}'))
reject('another A14 source substituted',lambda v:v.update(bytes=(R/'source.json').read_bytes()))
reject('unauthorized materialization',lambda v:v.update(materialize=True))
reject('hidden repinning',lambda v:v.update(repin=True))
reject('claim 10/10 before materialization',lambda v:v.update(current_present=10))
reject('operand promotion before source closure',lambda v:v.update(promoted_operands=1))
reject('unverified semantic regeneration',lambda v:v.update(method='SEMANTIC_PROJECTION'))
reject('future oracle reported as current',lambda v:v['future_oracle'].update(NOT_CURRENT_RESULT=False))
reject('missing pin in future source oracle',lambda v:v['future_oracle']['ROWS'].pop())
assert not (R/'resolution.json').exists()
(O/'negative-suite.json').write_text(json.dumps({'STATUS':'PASS','COUNT':len(rows),'ROWS':rows,'MODE':'static in-memory recovery/metadata checks; no qualifier operation or materialization'},sort_keys=True,indent=2)+'\n')
print(json.dumps({'NEGATIVES':'PASS','COUNT':len(rows)}))
