"""In-memory metadata negatives; never materializes an accepted source."""
import copy,hashlib,json
from pathlib import Path
O=Path(__file__).resolve().parent; R=O.parents[3]
s=json.loads((O/'bounded-materialization-subject.json').read_bytes()); raw=(R/s['ISOLATED_RECOVERED_CANDIDATE']['path']).read_bytes()
base={'bytes':raw,'hash':s['EXPECTED_SHA256'],'identity':s['EXPECTED_CONTENT_IDENTITY'],'path':'source.json','pointer':s['AUTHORITATIVE_A14_EMBEDDED_POINTER'],'lossless':True,'method':'EXACT_RETAINED','materialize':False,'repin':False}
def validate(c):
 assert c['bytes']==raw and hashlib.sha256(c['bytes']).hexdigest()==c['hash']==s['EXPECTED_SHA256']
 assert c['identity']==s['EXPECTED_CONTENT_IDENTITY'] and c['path']==s['EXISTING_RELATIVE_PATH']
 assert c['pointer']==s['AUTHORITATIVE_A14_EMBEDDED_POINTER'] and c['lossless'] is True
 assert c['method']=='EXACT_RETAINED' and c['materialize'] is False and c['repin'] is False
validate(base); rows=[]
tests=[('wrong bytes',{'bytes':raw[:-1]+b' '}),('semantic equivalent byte different',{'bytes':json.dumps(json.loads(raw),indent=2).encode()}),('wrong hash',{'hash':'0'*64}),('wrong content identity',{'identity':{**s['EXPECTED_CONTENT_IDENTITY'],'namespace':'planner-snapshot-v1'}}),('wrong path',{'path':'other/source.json'}),('noncanonical path',{'path':'./source.json'}),('wrong embedded pointer',{'pointer':{**s['AUTHORITATIVE_A14_EMBEDDED_POINTER'],'pointer':'/snapshot/actions/0/source/excerpt'}}),('lossy representation',{'lossless':False}),('report summary substituted',{'bytes':b'synthetic source summary'}),('E2-DECIDE substituted',{'bytes':(R/'E2-DECIDE.json').read_bytes()}),('choice substituted',{'bytes':b'{"choice":true}'}),('grant substituted',{'bytes':b'{"grant":true}'}),('unverified regeneration',{'method':'UNVERIFIED_REGENERATION'}),('unauthorized materialization',{'materialize':True}),('repinning hidden as materialization',{'repin':True})]
for name,change in tests:
 c=copy.deepcopy(base); c.update(change)
 try: validate(c)
 except AssertionError: rows.append({'CASE':name,'REJECTED':True})
 else: raise AssertionError(name)
assert not (R/'source.json').exists()
(O/'negative-suite.json').write_text(json.dumps({'STATUS':'PASS','COUNT':len(rows),'ROWS':rows,'MODE':'in-memory source/recovery contract validation; no qualification operations'},sort_keys=True,indent=2)+'\n')
print(json.dumps({'NEGATIVES':'PASS','COUNT':len(rows)}))
