"""104 documentary verifier;no bridge imports/native/OS probe execution."""
import copy,hashlib,json,os,pathlib
R=pathlib.Path(__file__).resolve().parents[5];B=R/'docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1';O=pathlib.Path(__file__).parent

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def require(x,m):
 if not x:raise ValueError(m)
expected={'DECLARATION_TYPE':'QUALIFICATION_GOVERNANCE_INTERPRETATION','ISSUER_ROLE':'KGE-FORGE-PROJECT-OWNER-QUALIFICATION-GOVERNING-AUTHORITY','SCOPE':'PACKAGE_86_FIXED_SYSTEM_LEVEL_METADATA_PROBE','AUTHORIZED_GRANT_ACTOR':'DESIGNATED_INDEPENDENTLY_QUALIFIED_KGE_FORGE_LAUNCH_CONTROLLER','OTHER_ACTORS_MAY_EXERCISE_GRANT':'NO','HOST_WIDE_TECHNICAL_EXCLUSIVITY_CLAIM':'NO','TECHNICAL_ENFORCEMENT_REQUIRED_BEFORE_ACTIVATION':'YES','PROBE_EXECUTION_AUTHORIZED':'NO'}
a=read(O/'entry-authentication.json');decl=read(O/'owner-declaration-content.json');prov=read(O/'owner-declaration-provenance.json');iw=read(O/'interpretation-content.json');approval=read(O/'owner-approval-record.json')
require(decl['CONTENT']==expected,'exactownerdeclaration');require((O/'owner-declaration-source.txt').read_text()=='\n\n'.join('`'+k+' = '+v+'`' for k,v in expected.items())+'\n','exactsourceexcerpt')
for x in [decl,iw,approval]:require(hashlib.sha256(enc(x['CONTENT'])).hexdigest()==x['IDENTITY']['sha256'],'contentid')
p=prov['SOURCE_PIN'];require(sha(R/p['path'])==p['raw_sha256'],'declrawpin');require(prov['SIGNATURE'] is None and prov['AUTHENTICATION_CREDENTIAL'] is None,'noinventedauthentication')
require(iw['CONTENT']['DECLARATION']==expected and iw['CONTENT']['OWNER_DECLARATION_IDENTITY']==decl['IDENTITY'],'interpretationbind');require(approval['CONTENT']['EXACT_INTERPRETATION_IDENTITY']==iw['IDENTITY'] and approval['CONTENT']['OWNER_DECLARATION_IDENTITY']==decl['IDENTITY'],'approvallinks')
p=a['ADOPTION_RECORD_PIN'];require(sha(R/p['path'])==p['raw_sha256'],'adoptionraw');rw=read(R/p['path']);require(hashlib.sha256(enc(rw['CONTENT'])).hexdigest()==rw['IDENTITY']['sha256']==a['ADOPTION_RECORD_IDENTITY']['sha256'],'adoptionidentity');record=rw['CONTENT']
require(record['CONTENT_IDENTITY']==iw['IDENTITY'] and record['OWNER_APPROVAL_IDENTITY']==approval['IDENTITY'],'noncircularrecordlinks');require(record['STATUS']=='ADOPTION_RECORDED_PENDING_INDEPENDENT_EFFECTIVENESS_VERIFICATION','immutablependingrecord')
require(record['PROBE_EXECUTION_GRANT'] is None and record['CONSTRUCTION_GRANT'] is None and not record['FROZEN_ACCEPTANCE_AMENDED'] and not record['TECHNICAL_ENFORCEMENT_VERIFIED'],'noeffectexpansion')
charter=read(R/'docs/plans/qualification/KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_65/charter-content.json');require(expected['ISSUER_ROLE']==charter['GOVERNING_AUTHORITY']['ROLE_ID'],'issuerrole');require(record['CHARTER_BINDING']==iw['CONTENT']['CHARTER_BINDING']==a['CHARTER_BINDING'],'charterlink');require(hashlib.sha256(enc(charter)).hexdigest()==a['CHARTER_BINDING']['sha256'],'chartercontent')
for folder in ['launch-exclusivity-closure-103','fixed-command-bridge-102','host-capability-bootstrap-reassessment-101','system-probe-authority-87','system-process-enforcement-86']:
 for n,h in read(B/folder/'evidence-index.json').get('FILES',{}).items():
  if isinstance(h,str):require(sha(R/n if (R/n).is_file() else B/folder/n)==h,'priorpin')
for r in a['GRANT_REFERENCES']:
 require(sha(R/r['path'])==r['raw_sha256'],'grantref');ref=read(R/r['path']);p=ref['GRANT_RECORD_PIN'];require(sha(R/p['path'])==p['raw_sha256'],'grantpin');g=read(R/p['path']);body=g.get('CONTENT',g.get('RECORD'));require(hashlib.sha256(enc(body)).hexdigest()==r['identity']['sha256'],'grantcontent')
 for p in ref['VERIFICATION_PINS']:require(sha(R/p['path'])==p['raw_sha256'],'grantchecks')
actor=read(O/'launch-actor-contract.json');require(actor['LAUNCH_ACTOR_ROLE']==expected['AUTHORIZED_GRANT_ACTOR'] and actor['ACTUAL_QUALIFIED_ACTOR_IDENTITY'] is None and not actor['REAL_INTERFACE_ENABLED'],'futureactoronly')
require(actor['HOST_LAUNCH_EXCLUSIVITY']=='UNVERIFIED' and actor['QUALIFIED_LAUNCH_CONTROLLER']=='NOT_ESTABLISHED','nopromotion')
f=read(B/'fixed-command-bridge-102/logical-synthetic-identity-manifest.json');sizes=[len(enc(x)) for x in f['CONTENT']['FIXTURES']];model=read(O/'twelve-case-resource-model.json');require(len(sizes)==12 and sum(sizes)==model['CANONICAL_FIXTURE_BYTES']==36710 and len(enc(f))==model['MANIFEST_BYTES']==37056,'fixturefigures')
require(not model['NUMERIC_INERT_BUDGET_COMPLETE'] and model['TOTAL_MAX_WRITES'] is None,'incompletebudget');reserve=read(O/'critical-failure-reserve.json');require(not reserve['RESERVE_COMPLETE'] and reserve['MAX_CRITICAL_RESERVE_BYTES'] is None,'noarbitraryreserve')
paths=a['PACKAGE102_TWO_PROPOSED_PATHS'];require(len(paths)==2 and not any((R/p).exists() for p in paths),'nosource')
reg=read(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');prev='0'*64
for e in reg['EVENTS']:
 require(e['PREVIOUS_EVENT_HASH']==prev,'lessonprevious');require(hashlib.sha256(json.dumps({k:v for k,v in e.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()==e['EVENT_HASH'],'lessonhash');prev=e['EVENT_HASH']
require(prev==a['LL11_HEAD'],'LL11head');require(sha(B/'campaign-budget.jsonl')==a['STOPPED_JOURNAL_SHA256'],'journal')
s={'hostwide':False,'declaration_is_enforcement':False,'real_probe_grant':False,'qualified_actor':False,'duplicate_consumption':False,'fsync_required':True,'arbitrary_numeric_limit':False,'critical_reserve_assumed':False,'budget_is_enforcement':False,'paths':paths,'systemd_sudo':False,'H77A15':False,'grant_issued':False}
def valid(x):
 require(not x['hostwide'],'hostwidefalseclaim');require(not x['declaration_is_enforcement'],'declarationasenforcement');require(not x['real_probe_grant'],'probegrantinferred');require(not x['qualified_actor'],'actorpromoted');require(not x['duplicate_consumption'],'duplicated');require(x['fsync_required'],'missingbarrier');require(not x['arbitrary_numeric_limit'],'arbitrarylimit');require(not x['critical_reserve_assumed'],'missingreservepromoted');require(not x['budget_is_enforcement'],'budgetasenforcement');require(x['paths']==paths,'scopeexpansion');require(not x['systemd_sudo'],'realsystemd');require(not x['H77A15'],'H77A15');require(not x['grant_issued'],'prematuregrant')
valid(s)
mut=[('hostwideclaim','hostwide',True),('ownerdeclarationtechnical','declaration_is_enforcement',True),('realprobegrant','real_probe_grant',True),('unqualifiedactorpromoted','qualified_actor',True),('duplicateconsumption','duplicate_consumption',True),('missingfsync','fsync_required',False),('arbitrarynumericcaps','arbitrary_numeric_limit',True),('missingreserveaccepted','critical_reserve_assumed',True),('budgetenforcementinferred','budget_is_enforcement',True),('unauthorizedsource','paths',paths+['adapter/unauthorized.py']),('systemd/sudo','systemd_sudo',True),('H77/A15','H77A15',True),('prematuregrant','grant_issued',True)]
neg=[]
for name,k,v in mut:
 x=copy.deepcopy(s);x[k]=v
 try:valid(x)
 except ValueError as e:neg.append({'CONTROL':name,'RESULT':'REJECTED','CAUSE':str(e)})
 else:raise ValueError('accepted:'+name)
# Authenticatedrecordprefix maybecomeeffectiveonlyvia separatepublishedreference,not mutatingadoption.
r={'OWNER_DECLARATION':decl['IDENTITY'],'INTERPRETATION_CONTENT':iw['IDENTITY'],'ADOPTION_RECORD':rw['IDENTITY'],'QUALIFICATION_ONLY':True,'NO_HOSTWIDE_TECHNICAL_CLAIM':True,'NO_PROBE_OR_CONSTRUCTION_PERMISSION':True,'ACTUAL_QUALIFIED_CONTROLLER':None,'ONEATTEMPT_PRESERVED':True,'CANONICAL_CASE_BYTES':36710,'MANIFEST_BYTES':37056,'NUMERIC_BUDGET_COMPLETE':False,'CRITICAL_RESERVE_COMPLETE':False,'CONSTRUCTION_DECISION_READY':False,'LL11_HEAD':prev,'NEGATIVES':neg,'CONTRACT_PINS':{p.name:sha(p) for p in O.glob('*.json') if p.name not in ['preservation-before.json','independent-persisted-record-verification.json','independent-static-verification.json','four-seed-reconstruction.json','negative-control-results.json','preservation-audit.json','report.json','evidence-index.json','effective-launch-actor-interpretation-reference.json','effective-reference-verification.json','governance-lifecycle-finalization.json','governance-authentication.json']},'ASSURANCE':'ownerprovidedcontent/issuer/charter/scope/persistedmetadata checks;notcryptographicpersonauthentication or technicalactivation/enforcement'}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':r,'SEMANTIC_SHA256':hashlib.sha256(enc(r)).hexdigest()},sort_keys=True))
