"""Fail-closed recovered byte-source evidence tests; no fixture integration."""
import hashlib,json
from copy import deepcopy
from pathlib import Path
from adapter.planner import codec,model
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;contract=json.loads((O/'source-contract.json').read_bytes());raw=(O/'candidates/E2-DECIDE.json').read_bytes();decoded=codec.parse_json(raw)
class Reject(ValueError):pass
def need(x,m):
 if not x:raise Reject(m)
base={'raw':raw,'identity':deepcopy(contract['EXPECTED_CONTENT_IDENTITY']),'source_path':'E2-DECIDE.json','byte_provenance':'PC01_source_raw.decode_literal_excerpt','historical_physical_retention':False}
def validate(v):
 need(v['raw']==raw,'BYTE_DIFFERENCE_NOT_SEMANTIC_EQUALITY')
 need(hashlib.sha256(v['raw']).hexdigest()==v['identity']['sha256'],'HASH_MISMATCH')
 need(v['identity']==contract['EXPECTED_CONTENT_IDENTITY'],'WRONG_CONTENT_IDENTITY_DOMAIN_OR_HASH')
 need(v['source_path']=='E2-DECIDE.json','WRONG_EXPECTED_SOURCE_PATH')
 codec._path(R,v['source_path']);need(codec.parse_json(v['raw'])==decoded,'SCHEMA_OR_NATIVE_SOURCE_ENVELOPE_MISMATCH')
 need(v['byte_provenance']==base['byte_provenance'],'UNVERIFIED_REGENERATION_OR_REPORT_SUBSTITUTION')
 need(v['historical_physical_retention'] is False,'PROSPECTIVE_COPY_IS_NOT_ORIGINAL_PHYSICAL_RETENTION')
 return True
validate(base);rows=[]
def reject(name,mutate):
 v=deepcopy(base);mutate(v)
 try:validate(v)
 except (Reject,model.PlannerError) as e:rows.append({'CASE':name,'STATUS':'REJECTED','REASON':str(e)})
 else:raise AssertionError(name)
reject('wrong E2-DECIDE bytes',lambda v:v.update(raw=b'{}'))
reject('semantic equivalent byte-different JSON',lambda v:v.update(raw=json.dumps(decoded,indent=2).encode()))
reject('wrong hash',lambda v:v['identity'].update(sha256='0'*64))
reject('wrong content identity',lambda v:v['identity'].update(namespace='planner-snapshot-v1'))
reject('wrong source path',lambda v:v.update(source_path='OTHER.json'))
reject('noncanonical source path',lambda v:v.update(source_path='qualification://E2-DECIDE.json'))
reject('wrong encoding',lambda v:v.update(raw=raw.decode().encode('utf-16')))
reject('wrong newline whitespace',lambda v:v.update(raw=raw+b'\n'))
reject('report summary substituted',lambda v:v.update(raw=b'{"result":"PASS"}'))
reject('RecordedDecision substituted',lambda v:v.update(raw=b'{"$type":"RecordedDecision"}'))
reject('choice source substituted',lambda v:v.update(raw=b'{"option":"ALLOW_QUALIFICATION_MAPPING"}'))
reject('grant source substituted',lambda v:v.update(raw=b'{"permission":"USE"}'))
reject('unverified regenerated JSON',lambda v:v.update(byte_provenance='semantic_fields_only'))
reject('historical retention claim from reproduction',lambda v:v.update(historical_physical_retention=True))
(O/'negative-suite.json').write_text(json.dumps({'STATUS':'PASS_14_STATIC_SOURCE_NEGATIVES','COUNT':len(rows),'ROWS':rows,'ACCEPTED_FIXTURE_SOURCE_CREATED':False,'SOURCE_FIXTURE_NOT_MUTATED':True},sort_keys=True,indent=2)+'\n');print('STATIC_SOURCE_NEGATIVES=14/14')
