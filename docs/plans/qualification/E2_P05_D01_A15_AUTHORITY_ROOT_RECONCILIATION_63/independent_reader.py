"""Independent source-pointer reader and authority compatibility verifier.
No native modules or effect entrypoints. Historical role authentication is
checked separately from currently applicable A15 decision power.
"""
import pathlib,json,hashlib,copy
E=pathlib.Path(__file__).parent;Q=E.parent;B=Q/'E2_P05_D01_A15_BOUNDED_AUTHORITY_QUALIFICATION_62'
def read(p):return json.loads(pathlib.Path(p).read_text())
def cb(x):return ''.join(json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).iterencode(x)).encode()
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def ensure(x,why):
 if not x:raise ValueError(why)
def pointer(value,ptr):
 for t in ptr.split('/')[1:]:
  if t=='':continue
  t=t.replace('~1','/').replace('~0','~');value=value[int(t)] if isinstance(value,list) else value[t]
 return value
catalog=read(E/'retained-authority-source-catalog.json');auth=read(E/'authentication.json');inventory=read(E/'authority-root-inventory.json');ready=read(E/'decision-readiness.json');target=read(B/'authority-subject-manifest.json')['TECHNICAL_PREPARATION_IDENTITY']
ensure(all(sha(p)==h for p,h in auth['FILES'].items()),'SOURCE_CHANGED')
ensure(all(sha(p)==h for p,h in read(B/'evidence-index.json')['FILES'].items()),'PACKAGE62_CHANGED')
ensure(catalog['TARGET_SUBJECT']==inventory['TARGET_SUBJECT']==target,'WRONG_SUBJECT')
# Source values independently reread at exact pointers; opaque text remains
# text evidence, not parsed into a fabricated authority identity.
reconstructed=[]
ambiguous={'A15_NORMATIVE_SCHEMA','A15_AUTHORITY_PREPARATION','P05_AUTHORITY_READINESS','E2_PROOF_AUTHORITY_INVENTORY'}
for item in catalog['RECORDS']:
 path=pathlib.Path(item['SOURCE']['PATH']);ensure(sha(path)==item['SOURCE']['RAW_SHA256'],'ROOT_SOURCE_CHANGED')
 actual=pointer(read(path),item['SOURCE_POINTER']) if path.suffix=='.json' else {'EXACT_TEXT':path.read_text()}
 ensure(actual==item['RECORD'],'ROOT_POINTER_OR_TYPE_CHANGED')
 kind=item['KIND'];identifier=str(path)+'#'+item['SOURCE_POINTER'];row=next(r for r in inventory['ROWS'] if r['RECORD_ID']==identifier)
 ensure(row['RECORD_KIND']==kind and row['SOURCE_POINTER']==item['SOURCE_POINTER'] and row['EVIDENCE_SOURCE']==item['SOURCE'],'ROOT_LINEAGE_CHANGED')
 ensure(row['APPLICABILITY']==('UNDETERMINED' if kind in ambiguous else 'INAPPLICABLE'),'UNSUPPORTED_APPLICABILITY')
 ensure(not row['CURRENT_A15_ISSUER_DESIGNATED'] and not row['A15_AUTHORITY_VERSION_APPLIES'] and row['DELEGATION_CHAIN']['TARGET_A15_DELEGATION_EVIDENCE'] is None,'HISTORICAL_ROOT_PROMOTED')
 ensure(row['AUTHORITY_VERSION'] is None,'SCHEMA_OR_POLICY_USED_AS_AUTHORITY_VERSION')
 if kind in ('ATTEST_HUMAN_DECISION','ROOT_SLOT_HUMAN_DECISIONS'):
  ensure(actual['issuer']=='AUTHENTICATED_HUMAN_USER' and actual.get('issuer_role',actual.get('role'))=='QUALIFICATION_AUTHORITY','HUMAN_ROLE_CHANGED')
 if kind=='ROOT_SLOT_HUMAN_DECISIONS':ensure(actual['permits_canonical_lifecycle_execution'] is False,'FIXTURE_DECISION_BROADENED')
 if kind in ('INSTALL_GRANT','OPERATING_ATTEST_GRANT'):ensure(actual['delegation'] is False,'DELEGATION_BROADENED')
 if kind in ('INSTALL_ADMISSION','P04_INSTALL_ADMISSION'):
  ensure(actual['schema']=='PLANNER-INSTALL-AUTHORITY-ADMISSION-1','ADMISSION_TYPE_COLLISION')
  grant=json.loads(actual['grant']) if isinstance(actual['grant'],str) else actual['grant'];ensure(grant['authority_class']=='INSTALL' and grant['delegation'] is False,'INSTALL_INFERRED_AS_OPERATING')
 if kind=='OPERATING_ATTEST_ADMISSION':
  ensure(actual['schema']=='PLANNER-ATTEST-DEFINITION-ADMISSION-1' and json.loads(actual['exact_grant_json'])['authority_class']=='ATTEST','ATTEST_ADMISSION_TYPE')
 if kind=='NATIVE_CHECKPOINT_AUTHORITY':
  ensure(row['AUTHORITY_ID']==actual['identity'] and row['SUBJECT_SCOPE']['subject']==actual['target'] and row['PERMITTED_ACTIONS']==actual['permissions'],'NATIVE_AUTHORITY_MAPPING_CHANGED')
  ensure(actual['scope']==catalog['NATIVE_CONTEXT']['scope'] and actual['valid_until']>=catalog['NATIVE_CONTEXT']['tick'],'NATIVE_CURRENTNESS_CHANGED')
  # Native validity is at sealed tick, not current wall-clock date; does not
  # establish broader human issuer competence.
  provenance=json.loads(actual['provenance']['excerpt'])
  if provenance.get('no_delegation') is True:ensure(row['DELEGATION_CHAIN']['DECLARED_DELEGATION'] is False,'NO_DELEGATION_INVERTED')
 if kind=='E1_CONTINUATION_DELEGATION':
  ensure('within the existing E1 runtime lineage' in actual['EXACT_TEXT'] and 'separate exact adoption authorization' in actual['EXACT_TEXT'],'E1_SCOPE_CHANGED')
  ensure(row['SUBJECT_SCOPE']['scope']=='Existing E1 runtime lineage' and row['ISSUER_ROLE']=='Architect','E1_ROLE_SCOPE_MAPPING')
 reconstructed.append({'RECORD_ID':identifier,'CLASSIFICATION':row['APPLICABILITY'],'SOURCE_HASH':sha(path),'ISSUER':row['ISSUER_IDENTITY'],'ROLE':row['ISSUER_ROLE'],'EXPLICIT_VERSION':None})
ensure(len(reconstructed)==42 and sum(r['CLASSIFICATION']=='INAPPLICABLE' for r in reconstructed)==38 and sum(r['CLASSIFICATION']=='UNDETERMINED' for r in reconstructed)==4,'ROOT_COUNTS')
ensure(inventory['APPLICABLE']==0 and inventory['CONFLICT']==0,'UNSUPPORTED_ROOT')
versions=read(E/'authority-version-comparison.json');ensure(versions['GOVERNING_A15_INSTRUMENT_ID'] is None and versions['GOVERNING_A15_VERSION'] is None,'INVENTED_INSTRUMENT')
mandates=read(E/'mandate-matrix.json');composition=read(E/'combined-separate-grant-analysis.json');proposal=read(E/'proposed-authority-instrument.json');gap=read(E/'authority-definition-gap.json')
ensure(all(mandates[k]=='UNDETERMINED' for k in ('NORMATIVE_SCOPE_ADOPTION_MANDATE','NATIVE_EXECUTION_MANDATE','CAPTURE_PERSISTENCE_MANDATE')),'MANDATE_INFERENCE')
ensure(composition['COMBINED_GRANT_PERMITTED']==composition['SEPARATE_GRANTS_REQUIRED']=='UNDETERMINED' and not composition['CURRENT_COMBINED_GRANT_SELECTED'],'COMPOSITION_INFERENCE')
ensure(proposal['PROPOSED_VERSION']==1 and proposal['ISSUER_IDENTITY'] is None and proposal['GRANT_IDENTITY'] is None and not proposal['AUTHORITY_ISSUED'] and not proposal['SELECTABLE'],'PROPOSAL_TREATED_AS_ISSUED')
ensure(proposal['EXACT_SUBJECT']==target and sha(proposal['EXACT_SUBJECT_MANIFEST']['PATH'])==proposal['EXACT_SUBJECT_MANIFEST']['RAW_SHA256'],'PROPOSAL_WRONG_SUBJECT')
ensure(proposal['EXECUTION_MANDATE']==read(B/'native-execution-authority-requirement.json') and proposal['HISTORICAL_EXCLUSIONS']==read(B/'historical-exclusions.json'),'PROPOSAL_SCOPE_CHANGED')
ensure(proposal['SCOPE']['variant_oracle_bindings']==read(B/'two-variant-authorization-inventory.json') and proposal['SCOPE']['checkpoint']==read(B/'checkpoint-ledger-verification.json')['SNAPSHOT_IDENTITY'],'PROPOSAL_IDENTITY_CHANGED')
ensure(gap['MINIMUM_GAP']=='A63-EXACT-A15-ISSUING-INSTRUMENT' and gap['CURRENT_INSTRUMENT'] is None and gap['CURRENT_VERSION'] is None and not gap['FUTURE_ISSUED_GRANT_REQUIRED_BEFORE_PROPOSAL'],'MINIMUM_GAP_CHANGED')
def readiness(value):ensure(not value['DECISION_READY'] and not value['AUTHORITY_SUBJECT_COMPLETE'] and value['DECISION_OPTIONS']==[] and not value['NORMATIVE_AUTHORITY_ISSUED'] and not value['EXECUTION_AUTHORITY_ISSUED'],'INCOMPLETE_AUTHORITY_READY')
readiness(ready)
# Counterfactual authority tuple: ALL dimensions must be independently supplied
# and match the exact proposed subject; no normative/execution/capture coercion.
# Test fixture tokens below are synthetic CONTROL values, not recovered issuers.
ref={'issuer':'CONTROL_ISSUER','role':'CONTROL_QUALIFICATION_ROLE','version':'CONTROL_VERSION','subject':target,'scope':proposal['SCOPE'],'delegation':['CONTROL_EVIDENCED_DESIGNATION'],'effective':True,'normative':True,'execution':True,'capture':True,'combined':False,'checkpoint':proposal['SCOPE']['checkpoint'],'variants':proposal['SCOPE']['variant_oracle_bindings'],'exclusions':proposal['HISTORICAL_EXCLUSIONS'],'a14_reused':False}
def qualification(a):
 for k in ('issuer','role','version','subject','scope','delegation','checkpoint','variants','exclusions'):ensure(a[k]==ref[k],'AUTHORITY_DIMENSION:'+k)
 ensure(a['effective'] and a['normative'] and a['execution'] and a['capture'] and not a['combined'] and not a['a14_reused'],'MANDATE_OR_EFFECTIVE_BOUNDARY')
qualification(ref);controls=[]
def reject(label,fn):
 try:fn()
 except (ValueError,AssertionError,KeyError):controls.append({'CONTROL':label,'RESULT':'REJECTED'});return
 raise AssertionError('Negative escaped:'+label)
for k,label,badvalue in [('issuer','WRONG_ISSUER','FOREIGN'),('role','WRONG_AUTHORITY_ROLE','FOREIGN'),('version','WRONG_VERSION','NEWEST_SCHEMA_VERSION'),('subject','WRONG_SUBJECT',proposal['SCOPE']['checkpoint']),('scope','WRONG_SCOPE',{'scope':'PRODUCTION'}),('delegation','MISSING_DELEGATION',[]),('effective','INAPPLICABLE_OR_EXPIRED',False),('checkpoint','WRONG_CHECKPOINT',target),('a14_reused','A14_GRANT_REUSED',True),('combined','UNAUTHORIZED_COMBINED_GRANT',True)]:
 a=copy.deepcopy(ref);a[k]=badvalue;reject(label,lambda a=a:qualification(a))
a=copy.deepcopy(ref);a['subject']='OLD_HISTORICAL_SUBJECT';reject('HISTORICAL_GRANT_AS_CURRENT',lambda:qualification(a))
a=copy.deepcopy(ref);a['normative']=False;reject('NORMATIVE_FROM_EXECUTION',lambda:qualification(a))
a=copy.deepcopy(ref);a['execution']=False;reject('EXECUTION_FROM_NORMATIVE',lambda:qualification(a))
a=copy.deepcopy(ref);a['capture']=False;reject('CAPTURE_ASSUMED',lambda:qualification(a))
a=copy.deepcopy(ref);a['variants'][0]['VARIANT_ID']='FOREIGN';reject('WRONG_VARIANT_IDENTITY',lambda:qualification(a))
a=copy.deepcopy(ref);a['variants'][0]['INDEPENDENT_ORACLE_IDENTITY']['sha256']='0'*64;reject('WRONG_ORACLE_IDENTITY',lambda:qualification(a))
for label,excluded in [('HISTORICAL_OCCURRENCE_CLAIM','Original historical A15 execution'),('E1_INCLUDED','E1 modification'),('PRODUCTION_INCLUDED','Production effects')]:
 a=copy.deepcopy(ref);a['exclusions']['EXCLUDED_CLAIMS_AND_OPERATIONS'].remove(excluded);reject(label,lambda a=a:qualification(a))
r=copy.deepcopy(ready);r['DECISION_READY']=True;reject('INCOMPLETE_AUTHORITY_DECISION_READY',lambda:readiness(r))
# Current actual records are NOT the positive synthetic test tuple. The current
# applicable-root count remains zero; no synthetic identity leaks into evidence.
reg=read(E/'lessons-register-snapshot.json');prior=read(B/'lessons-register-snapshot.json');ensure(reg['EVENTS'][:len(prior['EVENTS'])]==prior['EVENTS'],'LESSON_HISTORY_CHANGED')
head='0'*64
for e in reg['EVENTS']:
 ensure(e['PREVIOUS_EVENT_HASH']==head and hashlib.sha256(json.dumps({k:v for k,v in e.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':')).encode()).hexdigest()==e['EVENT_HASH'],'LESSON_HASH_CHANGED');head=e['EVENT_HASH']
ensure(len([e for e in reg['EVENTS'] if e['EVENT_TYPE']=='LESSON_RECORDED'])==10 and len([e for e in reg['EVENTS'] if e.get('WORK_PACKAGE')=='63'])==10,'LESSON_COUNT_CHANGED')
print(json.dumps({'RESULT':'PASS_PARTIAL_RECONCILIATION_CONFIRMED','ROOTS':reconstructed,'AUTHORITY_ROOTS_FOUND':42,'APPLICABLE_AUTHORITY_ROOTS':0,'INAPPLICABLE':38,'UNDETERMINED':4,'EXACT_TARGET':target,'GOVERNING_A15_VERSION':None,'COMBINED_GRANT_PERMITTED':'UNDETERMINED','SEPARATE_GRANTS_REQUIRED':'UNDETERMINED','MISSING_INSTRUMENT':'A63-EXACT-A15-ISSUING-INSTRUMENT','PROPOSAL_CONTENT_HASH':hashlib.sha256(cb(proposal)).hexdigest(),'DECISION_READY':False,'DECISION_OPTIONS':[],'NEGATIVE_CONTROLS':controls,'CONTROL_ISSUERS_ARE_SYNTHETIC':True,'NATIVE_EFFECTS':0},sort_keys=True))
