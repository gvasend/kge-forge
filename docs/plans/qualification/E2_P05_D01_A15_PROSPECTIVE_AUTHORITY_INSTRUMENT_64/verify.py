"""Independent static qualification from retained 63/62/61 inputs; no native effects."""
import pathlib,json,hashlib,copy,ast
from jsonschema import Draft7Validator
E=pathlib.Path(__file__).parent;Q=E.parent;C=Q/'E2_P05_D01_A15_AUTHORITY_ROOT_RECONCILIATION_63';B=Q/'E2_P05_D01_A15_BOUNDED_AUTHORITY_QUALIFICATION_62';A=Q/'E2_P05_D01_A15_CAPTURE_PERSISTENCE_RESUME_CLOSURE_61'
def read(p):return json.loads(pathlib.Path(p).read_text())
def cb(x):return ''.join(json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).iterencode(x)).encode()
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def need(x,r):
 if not x:raise ValueError(r)
for p,h in read(E/'authentication.json')['FILES'].items():need(sha(p)==h,'INPUT_CHANGED:'+p)
proposal=read(C/'proposed-authority-instrument.json');source_subject=read(B/'authority-subject-manifest.json');content=read(E/'proposed-instrument-content.json');schema=read(E/'typed-instrument-schema.json');ident=read(E/'instrument-identity-separation.json');body=source_subject['TECHNICAL_BODY'];ctx=body['CHECKPOINT']['CONTEXT'];variants=read(B/'two-variant-authorization-inventory.json');targets=read(A/'save-target-contracts.json')
Draft7Validator.check_schema(schema['JSON_SCHEMA']);validator=Draft7Validator(schema['JSON_SCHEMA']);validator.validate(content)
fields=['INSTRUMENT_ID','INSTRUMENT_VERSION','INSTRUMENT_STATUS','ISSUER_IDENTITY','ISSUER_ROLE','ISSUER_AUTHORITY_EVIDENCE','AUTHORIZED_SUBJECT','NORMATIVE_SCOPE_MANDATE','EXECUTION_MANDATE','CAPTURE_PERSISTENCE_MANDATE','EFFECTIVE_BOUNDARY','SCOPE','LINEAGE','GENERATION','PROTECTED_IDENTITIES','FAILURE_RETRY_LIMITS','HISTORICAL_EXCLUSIONS','EVIDENCE_PINS','ADOPTION_REQUIREMENTS','ISSUANCE_REQUIREMENTS','REVOCATION_OR_EXPIRATION_RULE']
need(set(schema['JSON_SCHEMA']['required'])==set(content)==set(fields),'FIELD_SET')
model=ast.parse(pathlib.Path('adapter/planner/model.py').read_text());node=next(n for n in model.body if isinstance(n,ast.ClassDef) and n.name=='IdentityKind');native_kinds=[n.targets[0].id for n in node.body if isinstance(n,ast.Assign)]
need(schema['IDENTITY_TYPE']['properties']['kind']['properties']['value']['enum']==native_kinds,'NATIVE_IDENTITY_DOMAIN_EXPANDED')
expected={
 'INSTRUMENT_ID':proposal['PROPOSED_INSTRUMENT_ID'],'INSTRUMENT_VERSION':proposal['PROPOSED_VERSION'],'INSTRUMENT_STATUS':'PROPOSED_INCOMPLETE_NOT_ISSUED','ISSUER_IDENTITY':None,'ISSUER_ROLE':None,'AUTHORIZED_SUBJECT':source_subject['TECHNICAL_PREPARATION_IDENTITY'],
 'NORMATIVE_SCOPE_MANDATE':proposal['NORMATIVE_MANDATE'],'EXECUTION_MANDATE':proposal['EXECUTION_MANDATE'],'CAPTURE_PERSISTENCE_MANDATE':proposal['CAPTURE_MANDATE'],'SCOPE':ctx['scope'],'LINEAGE':ctx['lineage'],'GENERATION':ctx['generation'],'HISTORICAL_EXCLUSIONS':proposal['HISTORICAL_EXCLUSIONS']}
for k,v in expected.items():need(content[k]==v,'WRONG_RETAINED_FIELD:'+k)
need(content['ISSUER_AUTHORITY_EVIDENCE']['VERIFIED'] is False and content['ISSUER_AUTHORITY_EVIDENCE']['ACTUAL_DESIGNATION_PIN'] is None and content['ISSUER_AUTHORITY_EVIDENCE']['DIRECT_OR_DELEGATED_POWER'] is None,'SELF_DESIGNATED_ISSUER')
for pin in content['EVIDENCE_PINS']:need(sha(pin['PATH'])==pin['RAW_SHA256'],'EVIDENCE_CHANGED')
effect=content['EFFECTIVE_BOUNDARY'];need(effect==read(E/'exact-subject-effective-boundary.json'),'BOUNDARY_RECORD_DIFFERENT')
need(effect['SUBJECT']==source_subject['TECHNICAL_PREPARATION_IDENTITY'] and effect['CHECKPOINT']==body['CHECKPOINT']['SNAPSHOT_IDENTITY'] and effect['CHECKPOINT_BUNDLE']==body['CHECKPOINT']['BUNDLE_IDENTITY'],'WRONG_CHECKPOINT_SUBJECT')
need(effect['VARIANTS']==variants and effect['ORACLE_IDENTITIES']==[v['INDEPENDENT_ORACLE_IDENTITY'] for v in variants] and effect['STATIC_HARNESS_IDENTITY']==body['HARNESS_IDENTITY'] and effect['STATIC_HARNESS_PINS']==body['HARNESS_PINS'],'VARIANT_ORACLE_HARNESS_MISMATCH')
need(effect['OUTPUT_PATHS_AND_NATIVE_PUBLICATION_MANIFESTS']==targets and not effect['WILDCARD_ALLOWED'],'OUTPUT_SCOPE_EXPANSION')
need(effect['OPERATION_BUDGET']=={'SUPERVISORS':1,'WRITERS':2,'INITIAL_RESTORES':2,'RECORD_RESULT':2,'SAVE_BUNDLE':2,'COLD_READERS_RESTORES':8,'DIRECT_PRE_APPLY_EVENT':0,'RETRIES':0},'OPERATION_BUDGET')
need(content['FAILURE_RETRY_LIMITS']['MAX_RETRIES']==0 and content['FAILURE_RETRY_LIMITS']['FAILURE_MATRIX']==read(B/'failure-retry-authority-matrix.json'),'RETRY_OR_FAILURE_CHANGE')
policy=read(Q/'E2_P05_D01_A15_PROSPECTIVE_SCENARIO_DESIGN_59/protected-effect-policy.json')
need(content['PROTECTED_IDENTITIES']['DIRECT_PROTECTED_CONTENT_IDENTITIES']==policy['DIRECT_PROTECTED_IDENTITIES'] and len(policy['DIRECT_PROTECTED_IDENTITIES'])==53 and content['PROTECTED_IDENTITIES']['PROTECTED_OBJECTS']==policy['PROTECTED_OBJECTS'],'UNPROTECTED_IDENTITY')
need(content['PROTECTED_IDENTITIES']['EXACT_FRAME_ORACLES']==[v['INDEPENDENT_ORACLE_PIN'] for v in variants],'PROTECTED_FRAME_ORACLE')
need(all(not content['ADOPTION_REQUIREMENTS'][k] for k in ['NORMATIVE_ADOPTED','EXECUTION_APPROVED','CAPTURE_APPROVED']) and content['ADOPTION_REQUIREMENTS']['COMBINED_APPROVAL_ALREADY_PERMITTED'] is None,'ADOPTION_OR_COMBINATION_INFERRED')
need(content['REVOCATION_OR_EXPIRATION_RULE']['ACTUAL_REVOCATION_OR_EXPIRATION_AUTHORITY'] is None and not content['REVOCATION_OR_EXPIRATION_RULE']['CLOCK_OR_TIME_WINDOW_INVENTED'],'LIFECYCLE_AUTHORITY_INVENTED')
for pin in effect['STATIC_HARNESS_PINS']:need(sha(pin['PATH'])==pin['RAW_SHA256'],'HARNESS_PIN')
# Exact incomplete draft content digest; this calculation grants no authority.
draft={'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':'qualification-A15-incomplete-instrument-content-v1','sha256':hashlib.sha256(cb(content)).hexdigest()}
need(ident['PROPOSED_INSTRUMENT_CONTENT_IDENTITY']==draft and not ident['CONTENT_COMPLETE'],'DRAFT_IDENTITY')
need(all(ident[k] is None for k in ['ISSUED_INSTRUMENT_IDENTITY','ISSUANCE_EVENT_IDENTITY','AUTHORIZED_EXECUTION_GRANT_IDENTITY']),'ISSUED_ID_INVENTED')
# Immutable hashes have one-way provenance; an external issuer-power record
# must NEVER derive its validity from a candidate it has not yet authorized.
nodes=['EXTERNAL_ISSUER_POWER','VERIFIED_ISSUER','PROPOSED_DRAFT_CONTENT','FINAL_CONTENT','NORMATIVE_APPROVAL','EXECUTION_APPROVAL','CAPTURE_APPROVAL','ISSUED_DOCUMENT','ISSUANCE_OCCURRENCE','EXECUTION_GRANT']
edges=[['EXTERNAL_ISSUER_POWER','VERIFIED_ISSUER'],['PROPOSED_DRAFT_CONTENT','FINAL_CONTENT'],['VERIFIED_ISSUER','FINAL_CONTENT'],['FINAL_CONTENT','NORMATIVE_APPROVAL'],['VERIFIED_ISSUER','NORMATIVE_APPROVAL'],['NORMATIVE_APPROVAL','EXECUTION_APPROVAL'],['VERIFIED_ISSUER','EXECUTION_APPROVAL'],['EXECUTION_APPROVAL','CAPTURE_APPROVAL'],['VERIFIED_ISSUER','CAPTURE_APPROVAL'],['FINAL_CONTENT','ISSUED_DOCUMENT'],['NORMATIVE_APPROVAL','ISSUED_DOCUMENT'],['EXECUTION_APPROVAL','ISSUED_DOCUMENT'],['CAPTURE_APPROVAL','ISSUED_DOCUMENT'],['ISSUED_DOCUMENT','ISSUANCE_OCCURRENCE'],['ISSUANCE_OCCURRENCE','EXECUTION_GRANT']]
def acyclic(es):
 remaining=set(nodes);order=[]
 while remaining:
  ready=sorted(n for n in remaining if not any(b==n and a in remaining for a,b in es))
  need(bool(ready),'CIRCULAR_AUTHORITY_IDENTITY');order+=ready;remaining.difference_update(ready)
 return order
order=acyclic(edges)
# New proposed requirements are checked as unadopted terms, not authority.
prereqs=read(E/'issuance-prerequisite-inventory.json')['PREREQUISITES'];need(content['ISSUANCE_REQUIREMENTS']['PREREQUISITES']==prereqs,'PREREQ_BINDING')
need({'ISSUER_VERIFIED','DELEGATION_VERIFIED','VERSION_SEALED','SUBJECT_VERIFIED','MANDATES_COMPLETE','SCOPE_VERIFIED','PROTECTION_VERIFIED','HISTORICAL_EXCLUSIONS_VERIFIED','INDEPENDENT_QUALIFICATION_PASS'}.issubset({r['PREREQUISITE'] for r in prereqs}),'MISSING_ISSUANCE_PREREQ')
need(any(r['STATUS']=='UNRESOLVED' for r in prereqs) and not content['ISSUANCE_REQUIREMENTS']['ISSUED'] and not content['ISSUANCE_REQUIREMENTS']['APPROVAL_OPTIONS_CREATED'],'PREMATURE_ISSUANCE')
roles=read(E/'issuer-delegation-qualification-matrix.json');need(roles['QUALIFIED_A15_ISSUERS']==0 and roles['CURRENT_ISSUER_ROLE'] is None and roles['CURRENT_ISSUER_IDENTITY'] is None,'ROLE_CREDENTIAL_INVENTED')
old=read(C/'authority-root-inventory.json')
for candidate in roles['ROWS']:
 if candidate['CANDIDATE_KIND']=='SPECIFICALLY_DELEGATED_ENGINEERING_AUTHORITY':need(candidate['ROLE_IDENTITY'] is None and candidate['DELEGATION_SOURCE'] is None and candidate['EVIDENCE'] is None,'ENGINEERING_DELEGATION_INVENTED');continue
 retained=next(r for r in old['ROWS'] if r['RECORD_KIND']==candidate['CANDIDATE_KIND']);need(candidate['ROLE_IDENTITY']==retained['ISSUER_ROLE'] and candidate['EVIDENCE']==retained['EVIDENCE_SOURCE'],'ROLE_EVIDENCE_CHANGE')
 need(candidate['A15_CLASSIFICATION'] in ['UNDETERMINED','UNQUALIFIED'],'HISTORICAL_ROLE_AS_CURRENT')
provenance=read(E/'field-value-provenance.json');need({r['FIELD_NAME'] for r in provenance}==set(content) and all(r['VALUE']==content[r['FIELD_NAME']] for r in provenance),'FIELD_PROVENANCE')
ready=read(E/'readiness-gates.json');separation=read(E/'mandate-separation-analysis.json')
def closed(r):
 need(r['INSTRUMENT_SCHEMA_COMPLETE'] and not r['PROPOSED_INSTRUMENT_COMPLETE'] and not r['PROPOSED_INSTRUMENT_CONTENT_COMPLETE'] and not r['ISSUER_AUTHORITY_VERIFIED'] and not r['ISSUANCE_READY'] and not r['EXECUTION_AUTHORIZATION_READY'] and not r['DECISION_READY'] and r['DECISION_OPTIONS']==[],'SELF_AUTHORIZATION_OR_INCOMPLETE_READY')
closed(ready);need(ready['COMBINED_INSTRUMENT_PERMITTED']==separation['COMBINED_INSTRUMENT_PERMITTED']=='UNDETERMINED','COMBINED_PERMISSION_INFERRED')
controls=[]
def reject(label,fn):
 try:fn()
 except Exception as e:
  if isinstance(e,(ValueError,AssertionError,KeyError)) or type(e).__name__=='ValidationError':controls.append({'CONTROL':label,'RESULT':'REJECTED'});return
  raise
 raise AssertionError('Negative escaped:'+label)
def exact_field(k,value):
 v=copy.deepcopy(content);v[k]=value;validator.validate(v);need(v[k]==content[k],'WRONG_FIELD')
reject('WRONG_ISSUER',lambda:exact_field('ISSUER_IDENTITY','ATTACKER'))
reject('MISSING_DELEGATION',lambda:exact_field('ISSUER_AUTHORITY_EVIDENCE',dict(content['ISSUER_AUTHORITY_EVIDENCE'],VERIFIED=True)))
reject('WRONG_AUTHORITY_VERSION',lambda:exact_field('INSTRUMENT_VERSION',2))
reject('WRONG_SUBJECT_IDENTITY',lambda:exact_field('AUTHORIZED_SUBJECT',effect['CHECKPOINT']))
bad=copy.deepcopy(content['NORMATIVE_SCOPE_MANDATE']);bad.pop('REQUIREDNESS_RULE');reject('MISSING_MANDATE',lambda:exact_field('NORMATIVE_SCOPE_MANDATE',bad))
reject('SCOPE_EXPANSION',lambda:exact_field('SCOPE','PRODUCTION'))
bad=copy.deepcopy(ready);bad['COMBINED_INSTRUMENT_PERMITTED']='YES';reject('UNAUTHORIZED_COMBINED_MANDATE',lambda:need(bad['COMBINED_INSTRUMENT_PERMITTED']==separation['COMBINED_INSTRUMENT_PERMITTED'],'COMBINED'))
reject('A14_GRANT_SUBSTITUTION',lambda:exact_field('AUTHORIZED_SUBJECT',read(Q/'E2_P05_D01_A14_RUNTIME_PERSISTENCE_QUALIFICATION_31/scope-authentication.json')['SUBJECT_IDENTITY']))
bad=copy.deepcopy(effect);bad['VARIANTS'][0]['EXPECTED_EVENT_IDENTITY']['sha256']='0'*64;reject('HISTORICAL_PROOF_OR_EVENT_MUTATION',lambda:exact_field('EFFECTIVE_BOUNDARY',bad))
bad=copy.deepcopy(effect);bad['VARIANTS'].append(copy.deepcopy(bad['VARIANTS'][0]));reject('NEW_INVALIDATION_VARIANT',lambda:exact_field('EFFECTIVE_BOUNDARY',bad))
bad=copy.deepcopy(effect);bad['CHECKPOINT']=effect['SUBJECT'];reject('WRONG_CHECKPOINT',lambda:exact_field('EFFECTIVE_BOUNDARY',bad))
bad=copy.deepcopy(effect);bad['ORACLE_IDENTITIES'][0]['sha256']='0'*64;reject('WRONG_ORACLE',lambda:exact_field('EFFECTIVE_BOUNDARY',bad))
bad=copy.deepcopy(content['PROTECTED_IDENTITIES']);bad['DIRECT_PROTECTED_CONTENT_IDENTITIES']=[];reject('UNPROTECTED_REQUIRED_IDENTITY',lambda:exact_field('PROTECTED_IDENTITIES',bad))
bad=copy.deepcopy(content['FAILURE_RETRY_LIMITS']);bad['MAX_RETRIES']=10;reject('UNBOUNDED_RETRY',lambda:exact_field('FAILURE_RETRY_LIMITS',bad))
for label,excluded in [('E1_MUTATION','E1 modification'),('PRODUCTION_EFFECT','Production effects')]:
 bad=copy.deepcopy(content['HISTORICAL_EXCLUSIONS']);bad['EXCLUDED_CLAIMS_AND_OPERATIONS'].remove(excluded);reject(label,lambda bad=bad:exact_field('HISTORICAL_EXCLUSIONS',bad))
bad=copy.deepcopy(ready);bad['ISSUANCE_READY']=True;bad['DECISION_READY']=True;reject('INSTRUMENT_SELF_AUTHORIZATION',lambda:closed(bad))
reject('CIRCULAR_IDENTITY_FROM_GRANT_TO_ISSUER',lambda:acyclic(edges+[['EXECUTION_GRANT','EXTERNAL_ISSUER_POWER']]))
bad=copy.deepcopy(ident);bad['ISSUED_INSTRUMENT_IDENTITY']=draft;reject('DRAFT_HASH_AS_ISSUED_IDENTITY',lambda:need(bad['ISSUED_INSTRUMENT_IDENTITY'] is None,'ISSUED_ID'))
reg=read(E/'lessons-register-snapshot.json');old=read(C/'lessons-register-snapshot.json');need(reg['EVENTS'][:len(old['EVENTS'])]==old['EVENTS'],'LESSON_PREFIX_CHANGED')
head='0'*64
for ev in reg['EVENTS']:
 need(ev['PREVIOUS_EVENT_HASH']==head and hashlib.sha256(json.dumps({k:v for k,v in ev.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':')).encode()).hexdigest()==ev['EVENT_HASH'],'LESSON_HASH_CHAIN');head=ev['EVENT_HASH']
need(len([ev for ev in reg['EVENTS'] if ev['EVENT_TYPE']=='LESSON_RECORDED'])==10 and len([ev for ev in reg['EVENTS'] if ev.get('WORK_PACKAGE')=='64'])==10,'LESSON_COUNT')
print(json.dumps({'RESULT':'PASS_STATIC_PARTIAL_ISSUANCE','SCHEMA_ID':schema['SCHEMA_ID'],'SCHEMA_COMPLETE':True,'PROPOSED_CONTENT_IDENTITY':draft,'CONTENT_COMPLETE':False,'SUBJECT':content['AUTHORIZED_SUBJECT'],'MANDATE_CONTENT_COMPLETE':separation['MANDATE_CONTENT_COMPLETE'],'ISSUER_VERIFIED':False,'COMBINED_INSTRUMENT_PERMITTED':'UNDETERMINED','ISSUANCE_READY':False,'DECISION_READY':False,'DECISION_OPTIONS':[],'IDENTITY_DEPENDENCY_GRAPH':{'NODES':nodes,'EDGES':edges,'TOPOLOGICAL_ORDER':order,'ACYCLIC':True,'EXTERNAL_ISSUER_POWER_SUPPLIED':False},'NEGATIVE_CONTROLS':controls,'NATIVE_EFFECTS':0},sort_keys=True))
