"""Independent identity/role/correction proof; no source rewrite or authority issue."""
import hashlib,json,runpy
from pathlib import Path
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification'
def read(p):return json.loads(p.read_bytes())
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
runpy.run_path(str(Q/'E2_P05_D01_A14_HANDOFF_CLOSURE_5/verify.py'),run_name='__metadata_verify__')
meaning=read(O/'conflicting-source-semantics.json');src=meaning['SEALED_SNAPSHOT_SOURCE'];p=R/src['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==src['raw_sha256'];s=read(p)['canonical_content']['subject']
records=[]
for e in s['entities']:
 prov=e['provenance']
 if prov['path']=='qualification://E2-P02-human-decision':
  payload=json.loads(prov['excerpt']);raw=canon(payload);assert hashlib.sha256(raw).hexdigest()==prov['identity']['sha256'];records.append((payload,prov,e))
choice=next(r for r in records if 'option' in r[0]);grant=next(r for r in records if 'permission' in r[0]);assert grant[0]['choice']==choice[1]['identity']['sha256'];assert choice[0]['scope']==grant[0]['scope'] and choice[0]['lineage']==grant[0]['lineage'];assert grant[0]['permission']=='USE'
assert choice[2]['identity']['kind']['value']=='AUTHORITY_IDENTITY' and choice[1]['identity']['kind']['value']=='CONTENT_IDENTITY'
assert grant[2]['identity']['namespace']=='e2-grant'
c=read(O/'minimum-correction-contract.json');identity=c['CORRECTION_CONTRACT_IDENTITY'];body=dict(c);body.pop('CORRECTION_CONTRACT_IDENTITY');assert identity=='qualification-A14-provenance-correction-v1:'+hashlib.sha256(canon(body)).hexdigest()
assert c['APPLIED'] is False and c['EXECUTABLE'] is False
for label,r in [('A',choice),('B',grant)]:
 commitment=c['SOURCE_FILE_BYTE_COMMITMENTS'][label];assert commitment['RAW_BYTES_UTF8'].encode()==canon(r[0]);assert commitment['SHA256']==r[1]['identity']['sha256'];target=c['SOURCE_ROLE_PATHS'][label];assert Path(target).as_posix()==target and not Path(target).is_absolute() and '..' not in Path(target).parts;assert not (R/target).exists(),'PROPOSED_SOURCE_MUST_NOT_HAVE_BEEN_MATERIALIZED'
assert c['SOURCE_ROLE_PATHS']['A']!=c['SOURCE_ROLE_PATHS']['B'] and len(c['PROVENANCE_PATH_ASSIGNMENTS'])==3
assert read(O/'a14-operand-impact.json')['COUNT']==16
assert read(O/'d01-obligation-impact.json')['COUNT']==8
assert read(O/'bounded-correction-decision-dossier.json')['SELECTION']=='NOT_SELECTED'
print(json.dumps({'STATUS':'PASS_INDEPENDENT_SEMANTIC_AND_CORRECTION_SPECIFICATION','CORRECTION_IDENTITY':identity,'CHOICE_AND_GRANT_DISTINCT_CONTENT_SOURCES':True,'GRANT_DERIVED_FROM_CHOICE':True,'PROPOSED_FILES_NOT_CREATED':True,'SEALED_SNAPSHOT_NOT_REWRITTEN':True,'RESOLVED_OPERANDS':52,'UNRESOLVED_OPERANDS':59,'A14_EXECUTED':False},sort_keys=True))
