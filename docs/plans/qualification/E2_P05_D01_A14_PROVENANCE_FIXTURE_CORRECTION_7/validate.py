"""Read-only validation and candidate metadata negatives for authorized fixture."""
import hashlib,json
from copy import deepcopy
from pathlib import Path
from adapter.planner import codec,model
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;C6=R/'docs/plans/qualification/E2_P05_D01_A14_SOURCE_PROVENANCE_RECONCILIATION_6'
def read(p):return json.loads(p.read_bytes())
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
contract=read(C6/'minimum-correction-contract.json');original_packet=read(R/contract['BASE_SNAPSHOT_SOURCE']['path']);original=original_packet['canonical_content']['subject'];fixture=read(O/'corrected-prospective-fixture.json');actual=read(O/'corrected-prospective-snapshot.json')['snapshot']
def at(v,ptr):
 for k in ptr.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k]
 return v
def put(v,ptr,value):
 keys=ptr.split('/')[1:];node=v
 for k in keys[:-1]:node=node[int(k)] if isinstance(node,list) else node[k]
 node[keys[-1]]=value
class Reject(ValueError):pass
def need(v,s):
 if not v:raise Reject(s)
def validate(subject,sources,claimed_id,historical_rewritten=False):
 need(not historical_rewritten,'HISTORICAL_REWRITE')
 need(set(sources)=={'A','B'},'MISSING_SOURCE')
 for label,commit in contract['SOURCE_FILE_BYTE_COMMITMENTS'].items():
  need(sources[label]==commit['RAW_BYTES_UTF8'].encode(),'PAYLOAD_BYTES_CHANGED_OR_SUBSTITUTED')
  need(hashlib.sha256(sources[label]).hexdigest()==commit['SHA256'],'CONTENT_IDENTITY_CHANGED')
 for assign in contract['PROVENANCE_PATH_ASSIGNMENTS']:
  ptr=assign['POINTER'].replace('/canonical_content/subject','',1);need(at(subject,ptr)==assign['PROPOSED_VALUE'],'WRONG_OR_NONCANONICAL_ROLE_PATH')
 reverted=deepcopy(subject)
 for assign in contract['PROVENANCE_PATH_ASSIGNMENTS']:put(reverted,assign['POINTER'].replace('/canonical_content/subject','',1),assign['EXPECTED_ORIGINAL_VALUE'])
 need(reverted==original,'FOURTH_FIELD_AUTHORITY_CONTENT_OR_SEMANTIC_CHANGE')
 native=codec._unwire(subject);model.validate_model(native);identity=codec._wire(codec.snapshot_id(native));need(identity==claimed_id and identity!=contract['BASE_SNAPSHOT_IDENTITY'],'WRONG_OR_RETAINED_SNAPSHOT_IDENTITY')
 return identity
sources={label:(R/path).read_bytes() for label,path in contract['SOURCE_ROLE_PATHS'].items()};assert validate(actual,sources,fixture['CORRECTED_SNAPSHOT_ID'])==fixture['CORRECTED_SNAPSHOT_ID']
neg=[]
def reject(name,mutate):
 state=deepcopy(actual);files=dict(sources);arg={'claimed_id':deepcopy(fixture['CORRECTED_SNAPSHOT_ID']),'historical_rewritten':False};mutate(state,files,arg)
 try:validate(state,files,**arg)
 except (Reject,model.PlannerError) as e:neg.append({'CASE':name,'STATUS':'REJECTED','REASON':str(e)})
 else:raise AssertionError(name)
A=contract['PROVENANCE_PATH_ASSIGNMENTS'][0]['POINTER'].replace('/canonical_content/subject','',1);B=contract['PROVENANCE_PATH_ASSIGNMENTS'][2]['POINTER'].replace('/canonical_content/subject','',1)
reject('choice/grant sharing one source path',lambda s,f,a:put(s,B,at(s,A)))
reject('choice bytes changed',lambda s,f,a:f.update(A=f['A']+b'\n'))
reject('grant bytes changed',lambda s,f,a:f.update(B=f['B']+b'\n'))
reject('content identity changed',lambda s,f,a:s['entities'][0]['provenance']['identity'].update(sha256='0'*64))
reject('authority identity changed',lambda s,f,a:s['entities'][1]['identity'].update(sha256='0'*64))
reject('semantic decision changed',lambda s,f,a:s['entities'][0].update(choice='DECLINE'))
reject('semantic grant changed',lambda s,f,a:s['entities'][1].update(permissions=[]))
reject('noncanonical choice path',lambda s,f,a:put(s,A,'qualification://choice'))
reject('noncanonical grant path',lambda s,f,a:put(s,B,'../grant.json'))
reject('duplicate raw key',lambda s,f,a:put(s,B,at(s,A)))
reject('choice source substituted for grant',lambda s,f,a:f.update(B=f['A']))
reject('grant source substituted for choice',lambda s,f,a:f.update(A=f['B']))
reject('missing choice source',lambda s,f,a:f.pop('A'))
reject('missing grant source',lambda s,f,a:f.pop('B'))
reject('fourth provenance path modified',lambda s,f,a:s['actions'][0]['source'].update(path='other.json'))
reject('original Snapshot identity retained',lambda s,f,a:a.update(claimed_id=deepcopy(contract['BASE_SNAPSHOT_IDENTITY'])))
reject('historical artifact rewritten',lambda s,f,a:a.update(historical_rewritten=True))
result={'STATUS':'PASS_17_STATIC_FIXTURE_NEGATIVES','ROWS':neg,'COUNT':len(neg),'NATIVE_MODEL_VALIDATION':'PASS_FOR_ACTUAL_CORRECTED_FIXTURE','CANDIDATE_TESTS_ARE_IN_MEMORY_ONLY':True,'NO_RUNTIME_TRANSITIONS':True,'NO_HISTORICAL_FILE_WRITES':True}
(O/'negative-suite.json').write_bytes(canon(result)+b'\n');print('CORRECTED_FIXTURE_NEGATIVES=17/17_REJECTED')
