"""Static corrected-representation contract checks; no correction is applied."""
import hashlib,json
from copy import deepcopy
from pathlib import Path
O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_bytes())
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
base=read(O/'minimum-correction-contract.json');a=base['SOURCE_FILE_BYTE_COMMITMENTS']['A'];b=base['SOURCE_FILE_BYTE_COMMITMENTS']['B']
class Reject(ValueError):pass
def need(x,reason):
 if not x:raise Reject(reason)
def validate(v):
 need(v['APPLIED'] is False and v['EXECUTABLE'] is False,'CORRECTION_MUST_REMAIN_UNAPPLIED_AND_UNAUTHORIZED')
 need(v['BASE_SNAPSHOT_IDENTITY']==base['BASE_SNAPSHOT_IDENTITY'],'HISTORICAL_IDENTITY_RELABEL')
 need(set(v['SOURCE_FILE_BYTE_COMMITMENTS'])=={'A','B'},'MISSING_OR_COLLAPSED_SOURCE')
 paths=v['SOURCE_ROLE_PATHS'];need(set(paths)=={'A','B'} and paths['A']!=paths['B'],'DUPLICATE_RAW_KEY')
 for sid in ['A','B']:
  source=v['SOURCE_FILE_BYTE_COMMITMENTS'][sid];expected=base['SOURCE_FILE_BYTE_COMMITMENTS'][sid];path=paths[sid]
  need(set(source)==set(expected),'PARTIAL_OR_COLLAPSED_SOURCE_RECORD')
  need(bool(path) and not Path(path).is_absolute() and '..' not in Path(path).parts and Path(path).as_posix()==path,'NONCANONICAL_TRAVERSAL_ALIAS')
  need(path==base['SOURCE_ROLE_PATHS'][sid],'UNAPPROVED_DIFFERENT_CANONICAL_PATH')
  need(source['HASH_PROFILE']=='raw-file-sha256' and source['PIN_POINTER']=='','WRONG_IDENTITY_DOMAIN_OR_RAW_PROJECTION')
  need(source['SHA256']==expected['SHA256'],'WRONG_SOURCE_ROLE_OR_CONTENT_IDENTITY')
  need(hashlib.sha256(source['RAW_BYTES_UTF8'].encode()).hexdigest()==source['SHA256'],'PROVENANCE_LAUNDERING')
 need(v['PROVENANCE_PATH_ASSIGNMENTS']==base['PROVENANCE_PATH_ASSIGNMENTS'],'MISSING_OR_WRONG_ROLE_OCCURRENCE')
 payloadA=json.loads(v['SOURCE_FILE_BYTE_COMMITMENTS']['A']['RAW_BYTES_UTF8']);payloadB=json.loads(v['SOURCE_FILE_BYTE_COMMITMENTS']['B']['RAW_BYTES_UTF8'])
 need(payloadB['choice']==v['SOURCE_FILE_BYTE_COMMITMENTS']['A']['SHA256'],'CHOICE_GRANT_LINKAGE')
 need(payloadA['dossier']==payloadB['dossier'] and payloadA['scope']==payloadB['scope'] and payloadA['lineage']==payloadB['lineage'],'SCOPE_DOSSIER_LINEAGE_LAUNDERING')
 need(v==base,'SEALED_CORRECTION_SUBJECT_DRIFT')
 return True
validate(base);rows=[]
def reject(name,mutate):
 v=deepcopy(base);mutate(v)
 try:validate(v)
 except Reject as exc:rows.append({'CASE':name,'STATUS':'REJECTED','REASON':str(exc)})
 else:raise AssertionError(name)
reject('duplicate raw key',lambda v:v['SOURCE_ROLE_PATHS'].update(B=v['SOURCE_ROLE_PATHS']['A']))
reject('missing source A',lambda v:v['SOURCE_FILE_BYTE_COMMITMENTS'].pop('A'))
reject('missing source B',lambda v:v['SOURCE_FILE_BYTE_COMMITMENTS'].pop('B'))
reject('source A substituted for B',lambda v:v['SOURCE_FILE_BYTE_COMMITMENTS'].update(B=deepcopy(v['SOURCE_FILE_BYTE_COMMITMENTS']['A'])))
reject('source B substituted for A',lambda v:v['SOURCE_FILE_BYTE_COMMITMENTS'].update(A=deepcopy(v['SOURCE_FILE_BYTE_COMMITMENTS']['B'])))
reject('wrong semantic role',lambda v:v['PROVENANCE_PATH_ASSIGNMENTS'][0].update(SOURCE_LABEL='B'))
reject('wrong identity domain',lambda v:v['SOURCE_FILE_BYTE_COMMITMENTS']['A'].update(HASH_PROFILE='planner-json-v1'))
reject('noncanonical path',lambda v:v['SOURCE_ROLE_PATHS'].update(A='qualification://E2-P02-human-decision'))
reject('different canonical path',lambda v:v['SOURCE_ROLE_PATHS'].update(A='docs/plans/OTHER.json'))
reject('path traversal/alias',lambda v:v['SOURCE_ROLE_PATHS'].update(A='docs/../choice.json'))
reject('source omitted after normalization',lambda v:v['PROVENANCE_PATH_ASSIGNMENTS'].pop())
reject('two entries collapsed incorrectly',lambda v:v['SOURCE_FILE_BYTE_COMMITMENTS'].update(B={'SHA256':a['SHA256']}))
reject('historical identity relabeled',lambda v:v['BASE_SNAPSHOT_IDENTITY'].update(sha256='0'*64))
reject('provenance laundering',lambda v:v['SOURCE_FILE_BYTE_COMMITMENTS']['A'].update(RAW_BYTES_UTF8='{}'))
reject('correction silently applied',lambda v:v.update(APPLIED=True))
result={'STATUS':'PASS_15_STATIC_CORRECTION_CONTRACT_NEGATIVES','CASES':rows,'NATIVE_REPLAY_EXECUTED':False,'CORRECTED_SOURCE_FILES_MATERIALIZED':False,'CORRECTED_SNAPSHOT_CREATED':False,'SCOPE_DECISION_SELECTED':False,'LIMIT':'Validates proposed unselected correction metadata and content commitments; not native replay or executable A14 qualification.'}
(O/'negative-suite.json').write_bytes(canon(result)+b'\n');print('STATIC_CORRECTION_CONTRACT_NEGATIVES=15/15')
