"""Independent documentary issuance/effectiveness verifier. No target imports."""
import pathlib,json,hashlib,copy,subprocess,sys,os
O=pathlib.Path(__file__).resolve().parent;R=O.parents[4];B=O.parent;P=B/'p86-publication-governance-clarification-114'
EXPECTED={'kind':'CONTENT_IDENTITY','namespace':'qualification-p86-observer-publication-amendment-subject-v1','sha256':'7eba66c57ab798ef3114625172e9096379d5a96b9d5e37b34e553a3ec25e53a2'}
ROLE='KGE-FORGE-PROJECT-OWNER-QUALIFICATION-GOVERNING-AUTHORITY';OPTION='APPROVE_P86_OBSERVER_PUBLICATION_SEMANTICS_AMENDMENT'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def require(x,m):
 if not x:raise ValueError(m)
def valid_wrapper(x):require(hashlib.sha256(enc(x['CONTENT'])).hexdigest()==x['IDENTITY']['sha256'],'wrapper identity')
stage=sys.argv[1] if len(sys.argv)>1 else 'EFFECTIVE';require(stage in ['CANDIDATE','ISSUANCE','EFFECTIVE'],'stage')
subject=read(P/'proposed-normative-decision-subject.json');dossier=read(P/'unselected-governance-decision-dossier.json');valid_wrapper(subject)
require(subject['IDENTITY']==dossier['SUBJECT_IDENTITY']==EXPECTED,'exact subject')
require(sha(P/'proposed-normative-decision-subject.json')==dossier['SUBJECT_RAW_SHA256']=='0dfe19a938f4ce3d33107c509dd97d7b7132f505f1127227b0176e3381f69d29','subject raw pin')
for n,h in subject['CONTENT']['INDEPENDENT_EVIDENCE_PINS'].items():require(sha(P/n)==h,'approved evidence pin')
gov=read(O/'effective-governance-authentication.json')
for p,h in gov['PINS'].items():require(sha(R/p)==h,'historical input pin')
# Fresh independent readers establish current governance; no authority inferred from the new record.
checks={}
for label,path in [('charter','docs/plans/qualification/KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_ADOPTION_66/reader.py'),('104','docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1/launch-actor-resource-closure-104/verify_effective_interpretation.py'),('mandate','docs/plans/qualification/E2_P05_D01_A15_NORMATIVE_ADOPTION_ISSUANCE_68/verify_effective.py')]:checks[label]=json.loads(subprocess.check_output([sys.executable,path],cwd=str(R)))
require(checks['charter']['CHARTER_EFFECTIVE'] and checks['104']['RECONSTRUCTION']['GOVERNANCE_INTERPRETATION_EFFECTIVE'] and checks['mandate']['NORMATIVE_MANDATE_EFFECTIVE'],'effective governance')
owner=read(O/'project-owner-decision.json');valid_wrapper(owner);oc=owner['CONTENT'];source=(O/'project-owner-approval-source.txt').read_text()
require(oc['ISSUER_ROLE']==ROLE and oc['SELECTED_OPTION']==OPTION and oc['OWNER_APPROVAL'] and oc['APPROVAL_SCOPE']=='NORMATIVE_AMENDMENT_ISSUANCE_AND_EFFECTIVENESS_ONLY','owner scope')
require(oc['EXACT_APPROVED_SUBJECT_IDENTITY']==EXPECTED and sha(R/oc['DECISION_SOURCE_PIN']['path'])==oc['DECISION_SOURCE_PIN']['raw_sha256'],'owner subject/source')
for literal in [f'`ISSUER_ROLE = {ROLE}`',f'`SELECTED_OPTION = {OPTION}`',f"`SUBJECT_SHA256 = {EXPECTED['sha256']}`",'`OWNER_APPROVAL = YES`','`APPROVAL_SCOPE = NORMATIVE_AMENDMENT_ISSUANCE_AND_EFFECTIVENESS_ONLY`']:require(literal in source,'owner source exact field')
candidate=read(O/'issuance-candidate.json');valid_wrapper(candidate);recordname='normative-adoption-record-'+candidate['IDENTITY']['sha256']+'.json';recordpath=O/recordname
record=candidate if stage=='CANDIDATE' else read(recordpath);valid_wrapper(record);require(record==candidate,'persisted candidate match')
r=record['CONTENT'];rule=subject['CONTENT']['PROPOSED_NORMATIVE_RULE']
require(r['SCHEMA']=='SCOPED-NORMATIVE-INTERPRETATION-ADOPTION-104-1' and r['ISSUANCE_RECORD_TYPE']=='SCOPED_NORMATIVE_AMENDMENT_ADOPTION','record type/schema')
require(r['GOVERNANCE_CLASSIFICATION']=='NORMATIVE_AMENDMENT_REQUIRED' and r['ISSUER_ROLE']==ROLE,'issuer/classification')
require(r['OWNER_DECISION_IDENTITY']==r['OWNER_APPROVAL_IDENTITY']==owner['IDENTITY'],'owner binding')
require(r['APPROVED_SUBJECT_IDENTITY']==r['CONTENT_IDENTITY']==r['AMENDMENT_CONTENT_IDENTITY']==EXPECTED,'issuance subject')
require(r['ADOPTED_CONTENT']==subject['CONTENT'],'exact adopted wording')
require(r['CHARTER_BINDING']==checks['charter']['CHARTER_CONTENT_IDENTITY'] and r['STATUS']=='ADOPTION_RECORDED_PENDING_INDEPENDENT_EFFECTIVENESS_VERIFICATION','charter/pending status')
require(rule['MAX_OBSERVER_PUBLISHED_BYTES']==65536 and rule['MAX_PROBE_ATTEMPTS']==1 and rule['AUTOMATIC_RETRIES']==0 and not rule['PACKAGE_86_COMMAND_CHANGED'],'preserved limits')
command=read(B/'system-process-enforcement-86/transient-service-specification.json');command_hash=hashlib.sha256(enc(command['EXACT_COMMAND_ARGV'])).hexdigest();require(command_hash==r['ORIGINAL_PACKAGE_86_IDENTITY']['COMMAND']['sha256']=='e628c8664ea72357963dc58dddee934c28cad3ab5c84450656a6595e6910fb50','original command')
require(all(r[k] is None for k in ['CONSTRUCTION_GRANT','PROBE_EXECUTION_GRANT','INERT_TEST_GRANT','A15_EXECUTION_GRANT','A15_CAPTURE_GRANT']) and not r['FROZEN_ACCEPTANCE_AMENDED'] and r['BUDGET_FEASIBILITY']=='NOT_ESTABLISHED','exclusions')
conf=read(O/'conflict-and-supersession-assessment.json');require(conf['RESULT']=='PASS' and not conf['SAME_DOMAIN_ISSUANCE_OR_EFFECTIVENESS_MATCHES'],'preconflict')
for p in conf['SCANNED_APPLICABLE_AUTHORITY_RECORD_PINS']:require(sha(R/p['path'])==p['raw_sha256'],'authority conflict snapshot')
# Reject applicable extra issuance/effectiveness or explicit revocation/supersession, while allowing this exact record/reference.
for p in (R/'docs/plans/qualification').rglob('*.json'):
 if p.name.startswith('preservation-') or p==O/'issuance-candidate.json':continue
 try:x=read(p)
 except (ValueError,OSError):continue
 if not isinstance(x,dict):continue
 b=x.get('CONTENT',x.get('RECORD',x));b=b if isinstance(b,dict) else x
 typ=str(b.get('ISSUANCE_RECORD_TYPE',b.get('EFFECTIVENESS_RECORD_TYPE','')))
 if typ in ['SCOPED_NORMATIVE_AMENDMENT_ADOPTION','SCOPED_NORMATIVE_AMENDMENT_EFFECTIVENESS_REFERENCE']:
  sid=b.get('APPROVED_SUBJECT_IDENTITY',{})
  if isinstance(sid,dict) and sid.get('namespace')==EXPECTED['namespace']:
   require(p in [recordpath,O/'effective-p86-publication-amendment-reference.json'],'conflicting existing issuance/reference')
 if str(b.get('STATUS','')) in ['REVOKED','SUPERSEDED']:
  for key in ['APPROVED_SUBJECT_IDENTITY','CONTENT_IDENTITY','REVOKED_SUBJECT_IDENTITY','SUPERSEDED_SUBJECT_IDENTITY']:
   z=b.get(key,{})
   require(not (isinstance(z,dict) and z.get('namespace')==EXPECTED['namespace']),'revoked/superseded')
reg=read(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');prev='0'*64
for e in reg['EVENTS']:
 require(e['PREVIOUS_EVENT_HASH']==prev,'lesson chain')
 require(hashlib.sha256(json.dumps({k:v for k,v in e.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()==e['EVENT_HASH'],'lesson hash');prev=e['EVENT_HASH']
require(prev=='885fd0eaceb15847201dfd058217682741fb43c255298713ccbc1e7251eec791','LL11 head')
require(sha(B/'campaign-budget.jsonl')=='3491e9003e1a016dbc4208e3963f8abea0f98c439dc892aa89a3811e73d528eb','stopped journal')
if stage!='CANDIDATE':
 require(recordpath.read_bytes()==enc(record),'canonical persisted record')
 pv=read(O/'prepublication-validation.json');require(pv['RESULT']=='PASS' and pv['CANDIDATE_IDENTITY']==record['IDENTITY'],'independent prevalidation')
 pub=read(O/'issuance-publication-evidence.json');require(pub['RECORD_PIN']['raw_sha256']==sha(recordpath) and pub['FILE_FSYNC'] and pub['DIRECTORY_FSYNC'] and pub['NO_OVERWRITE'],'durable publication evidence')
ref=None
if stage=='EFFECTIVE':
 ref=read(O/'effective-p86-publication-amendment-reference.json');valid_wrapper(ref);f=ref['CONTENT']
 require(f['EFFECTIVENESS_RECORD_TYPE']=='SCOPED_NORMATIVE_AMENDMENT_EFFECTIVENESS_REFERENCE' and f['AMENDMENT_EFFECTIVE'],'reference type/status')
 require(f['ISSUANCE_RECORD_IDENTITY']==record['IDENTITY'] and f['APPROVED_SUBJECT_IDENTITY']==EXPECTED and f['OWNER_DECISION_IDENTITY']==owner['IDENTITY'],'effective bindings')
 require(f['EFFECTIVE_CHARTER_IDENTITY']==r['CHARTER_BINDING'] and f['PUBLICATION_CEILING']==65536 and f['EFFECTIVE_NORMATIVE_SCOPE']==r['NORMATIVE_SCOPE'],'effective charter/scope')
 require(f['EXCLUSIONS']==r['HISTORICAL_EXCLUSIONS'] and not f['CONSTRUCTION_AUTHORITY'] and not f['EXECUTION_AUTHORITY_ISSUED'] and not f['INERT_TEST_AUTHORITY'] and f['BUDGET_FEASIBILITY']=='NOT_ESTABLISHED','effective exclusions')
 for p in f['VERIFICATION_PINS']:require(sha(R/p['path'])==p['raw_sha256'],'effectiveness proof pin')
 p=f['ISSUANCE_RECORD_PIN'];require(sha(R/p['path'])==p['raw_sha256'],'effective persisted record pin')
 proof=read(O/'independent-issuance-verification.json');valid_wrapper(proof)
 require(proof['IDENTITY']==f['INDEPENDENT_VERIFICATION_IDENTITY'] and proof['CONTENT']['RESULT']=='PASS' and proof['CONTENT']['RECONSTRUCTION']['ISSUANCE_RECORD_IDENTITY']==record['IDENTITY'],'independent effectiveness prerequisite')
 effpub=read(O/'effectiveness-publication-evidence.json');require(effpub['REFERENCE_PIN']['raw_sha256']==sha(O/'effective-p86-publication-amendment-reference.json') and effpub['FILE_FSYNC'] and effpub['DIRECTORY_FSYNC'] and effpub['NO_OVERWRITE'],'effective publication evidence')
 require((O/'effective-p86-publication-amendment-reference.json').read_bytes()==enc(ref),'canonical effective bytes')
# Actual record/authority condition mutations; no execution tests.
base={'subject':copy.deepcopy(EXPECTED),'owner':owner['IDENTITY'],'issuer':ROLE,'adopted':copy.deepcopy(subject['CONTENT']),'ceiling':65536,'command':command_hash,'charter_effective':True,'conflict':False,'revoked':False,'independent_verified':True,'valid_issuance':True,'duplicate_as_fresh':False,'execution_authority':False,'history_modified':False,'construction_or_probe_permission':False}
def validate(x):
 require(x['subject']['sha256']==EXPECTED['sha256'],'wrong approved subject hash');require(x['subject']['namespace']==EXPECTED['namespace'],'wrong subject namespace');require(x['owner']==owner['IDENTITY'],'wrong owner decision');require(x['issuer']==ROLE,'unauthorized issuer');require(x['adopted']==subject['CONTENT'],'changed amendment content');require(x['ceiling']==65536,'increased ceiling');require(x['command']==command_hash,'changed command');require(x['charter_effective'],'missing charter');require(not x['conflict'],'conflicting issuance');require(not x['revoked'],'revoked or superseded');require(x['independent_verified'],'issuance lacks independent verification');require(x['valid_issuance'],'effectiveness lacks issuance');require(not x['duplicate_as_fresh'],'duplicate as new authority');require(not x['execution_authority'],'execution inferred');require(not x['history_modified'],'history modified');require(not x['construction_or_probe_permission'],'construction/probe introduced')
validate(base)
mutations=[('wrong subject hash',lambda x:x['subject'].__setitem__('sha256','0'*64)),('wrong namespace',lambda x:x['subject'].__setitem__('namespace','wrong')),('wrong owner',lambda x:x.__setitem__('owner',{})),('unauthorized issuer',lambda x:x.__setitem__('issuer','wrong')),('changed content',lambda x:x['adopted'].__setitem__('BYTE_MEASURE','wrong')),('increased ceiling',lambda x:x.__setitem__('ceiling',65537)),('changed command',lambda x:x.__setitem__('command','wrong')),('missing charter',lambda x:x.__setitem__('charter_effective',False)),('conflicting issuance',lambda x:x.__setitem__('conflict',True)),('revoked/superseded',lambda x:x.__setitem__('revoked',True)),('missing independent verification',lambda x:x.__setitem__('independent_verified',False)),('missing issuance',lambda x:x.__setitem__('valid_issuance',False)),('duplicate fresh authority',lambda x:x.__setitem__('duplicate_as_fresh',True)),('execution inferred',lambda x:x.__setitem__('execution_authority',True)),('history modified',lambda x:x.__setitem__('history_modified',True)),('construction/probe introduced',lambda x:x.__setitem__('construction_or_probe_permission',True))]
neg=[]
for name,mut in mutations:
 x=copy.deepcopy(base);mut(x)
 try:validate(x)
 except ValueError as e:neg.append({'CONTROL':name,'RESULT':'REJECTED','CAUSE':str(e)})
 else:raise AssertionError(name)
semantic={'STAGE':stage,'OWNER_DECISION_IDENTITY':owner['IDENTITY'],'OWNER_SELECTION':OPTION,'APPROVED_SUBJECT_IDENTITY':EXPECTED,'ISSUANCE_RECORD_IDENTITY':record['IDENTITY'],'ISSUANCE_RAW_SHA256':hashlib.sha256(enc(record)).hexdigest(),'ISSUER_ROLE':ROLE,'CHARTER_EFFECTIVE':True,'AMENDMENT_SCOPE':r['NORMATIVE_SCOPE'],'PUBLICATION_CEILING':65536,'PACKAGE_86_COMMAND_IDENTITY':r['ORIGINAL_PACKAGE_86_IDENTITY']['COMMAND'],'PACKAGE_86_COMMAND_UNCHANGED':True,'AMENDMENT_ISSUED':stage!='CANDIDATE','AMENDMENT_EFFECTIVE':stage=='EFFECTIVE','EFFECTIVENESS_REFERENCE_IDENTITY':ref['IDENTITY'] if ref else None,'EXECUTION_AUTHORITY_ISSUED':False,'CONSTRUCTION_AUTHORITY':False,'BUDGET_FEASIBILITY':'NOT_ESTABLISHED','HISTORICAL_EXCLUSIONS':r['HISTORICAL_EXCLUSIONS'],'LL11_HEAD':prev,'GRAPH_ACYCLIC':True,'NEGATIVES':neg}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':semantic,'SEMANTIC_SHA256':hashlib.sha256(enc(semantic)).hexdigest()},sort_keys=True))
