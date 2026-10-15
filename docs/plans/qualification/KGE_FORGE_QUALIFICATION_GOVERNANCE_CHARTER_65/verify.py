"""Independent static charter qualification; no lifecycle/grant issuance or native operations."""
import pathlib,json,hashlib,copy
E=pathlib.Path(__file__).parent;Q=E.parent;B=Q/'E2_P05_D01_A15_BOUNDED_AUTHORITY_QUALIFICATION_62'
def read(p):return json.loads(pathlib.Path(p).read_text())
def cb(x):return ''.join(json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).iterencode(x)).encode()
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def need(v,why):
 if not v:raise ValueError(why)
for p,h in read(E/'input-authentication.json')['FILES'].items():need(sha(p)==h,'PRIOR_EVIDENCE_CHANGED:'+p)
decl=read(E/'owner-declaration-provenance.json');source=pathlib.Path(decl['SOURCE_PIN']['PATH']).read_text();charter=read(E/'charter-content.json');ident=read(E/'charter-content-identity.json');dossier=read(E/'charter-adoption-decision-dossier.json');mapping=read(E/'a15-authority-mapping.json');gates=read(E/'readiness-gates.json')
# Exact user-declaration excerpts are the independently captured initiating
# evidence. They do not contain a charter selection, execution grant or invented
# signature, actor legal name or repository-owner inferred credential.
exact=['The project owner has explicitly declared authority to establish and approve KGE-Forge qualification governance rules.','The project owner has explicitly limited the proposed charter to **qualification governance only**.','Treat these declarations as initiating governance evidence, not as an already issued charter or execution authorization.']
need(all(s in source for s in exact),'DECLARATION_OR_SCOPE_TEXT')
need(decl['EXACT_OWNER_AUTHORITY_DECLARATION']==exact[0] and decl['EXACT_SCOPE_LIMITATION']==exact[1] and decl['EXACT_INITIATING_LIMIT']==exact[2],'DECLARATION_RECORD')
need(sha(decl['SOURCE_PIN']['PATH'])==decl['SOURCE_PIN']['RAW_SHA256'] and decl['SOURCE_KIND']=='USER_ROLE_CURRENT_API_CONVERSATION' and decl['SOURCE_WORK_PACKAGE']=='KGE-FORGE-QUALIFICATION-GOVERNANCE-CHARTER-65','DECLARATION_PROVENANCE')
need(decl['LEGAL_NAME_OR_ACCOUNT_ID'] is None and not decl['CHARTER_ADOPTED'] and not decl['A15_GRANTED'] and not decl['EXTERNAL_CREDENTIALS_INVENTED'] and not decl['MESSAGE_ID_OR_SIGNATURE_INVENTED'],'DECLARATION_AS_GRANT_OR_CREDENTIAL')
need(charter['CHARTER_VERSION']=='1.0' and charter['CHARTER_ID']=='KGE-FORGE-QUALIFICATION-GOVERNANCE-CHARTER' and charter['QUALIFICATION_SCOPE']=='KGE-Forge qualification governance only','VERSION_OR_SCOPE')
need(charter['GOVERNING_AUTHORITY']['DECLARATION_PIN']['RAW_SHA256']==sha(E/'owner-declaration-provenance.json') and charter['OWNER_DECLARATION_SOURCE_PIN']['RAW_SHA256']==sha(E/'owner-declaration-source.txt'),'DECLARATION_BINDING')
exclusions=['General engineering governance authority','Production execution authority','External system permissions','Government-controlled environment permissions','Authority to bypass organizational security controls','Unrestricted native execution','Automatic approval of prospective qualification scenarios','Automatic A15 execution authority']
need(charter['EXCLUSIONS']==exclusions and all(x in source for x in exclusions),'MISSING_EXCLUSION')
need(charter['RESOURCE_AND_SECURITY_BOUNDARY']['NO_EXTERNAL_PRIVILEGE_CREATION'] and charter['RESOURCE_AND_SECURITY_BOUNDARY']['ORG_SECURITY_CONTROLS_BINDING'] and not charter['RESOURCE_AND_SECURITY_BOUNDARY']['GOVERNMENT_ENVIRONMENT_PERMISSION_CREATED'],'RESOURCE_PRIVILEGE_EXPANSION')
need(charter['QUALIFICATION_EXECUTION_AUTHORITY']['REQUIRED_AUTHORIZATION_FIELDS']==['Exact qualification subject','Permitted operations','Starting state','Input identities','Execution environment','Output boundaries','Failure/retry limits','Historical exclusions'],'UNBOUNDED_EXECUTION_FIELDS')
need(not charter['NORMATIVE_QUALIFICATION_AUTHORITY']['MANDATE_TO_EXECUTE_IMPLIED'] and 'No silent modification' in charter['NORMATIVE_QUALIFICATION_AUTHORITY']['FROZEN_ACCEPTANCE'],'FROZEN_REQUIREMENT_CHANGE')
lifecycle=read(E/'charter-lifecycle-specification.json');expected_edges=[('DRAFT','REVIEWED'),('REVIEWED','APPROVED'),('APPROVED','EFFECTIVE'),('EFFECTIVE','SUPERSEDED'),('EFFECTIVE','REVOKED')]
need([(x['FROM'],x['TO']) for x in lifecycle['TRANSITIONS']]==expected_edges and all(x['EVIDENCE'] and x['ACTOR'] for x in lifecycle['TRANSITIONS']),'LIFECYCLE_GAPS')
need(lifecycle['CURRENT_LIFECYCLE_STATE']=='DRAFT' and lifecycle['APPROVAL_EVIDENCE'] is None and lifecycle['EFFECTIVE_EVIDENCE'] is None,'PREMATURE_LIFECYCLE')
need(charter['LIFECYCLE_POLICY']=={k:v for k,v in lifecycle.items() if k not in ['CURRENT_LIFECYCLE_STATE','APPROVAL_EVIDENCE','EFFECTIVE_EVIDENCE']},'LIFECYCLE_CONTENT_MISMATCH')
delegation=read(E/'delegation-contract.json');need(charter['DELEGATION']==delegation and delegation['EXISTING_DELEGATIONS_CREATED']==[] and not delegation['EFFECTIVE_AUTHORITY_GRANTED'],'DELEGATION_CREATED')
need('No transitive delegation or subdelegation; delegate cannot delegate onward' in delegation['RULES'] and all(f in delegation['REQUIRED_FIELDS'] for f in ['delegate_identity_or_explicit_role','exact_delegation_scope','permitted_mandates_and_operations','effective_boundary','revocation_or_expiration_rule','charter_content_identity_and_version']),'DELEGATION_NOT_BOUNDED')
composition=charter['MANDATE_COMPOSITION'];need(composition['ONE_INSTRUMENT_THREE_MANDATES_PERMITTED_CONDITIONALLY'] and not composition['CURRENT_COMBINED_A15_GRANT_PERMITTED_BY_EFFECTIVE_CHARTER'] and not composition['CHARTER_ADOPTION_INCLUDES_A15_MANDATES'],'COMBINATION_AS_AUTOMATIC_GRANT')
need('Charter actually EFFECTIVE' in composition['CONDITIONS'] and len(composition['CONDITIONS'])==5,'COMBINED_WITHOUT_POWER')
id={'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':'kge-forge-qualification-governance-charter-v1','sha256':hashlib.sha256(cb(charter)).hexdigest()}
need(id==ident['CHARTER_CONTENT_IDENTITY']==mapping['CHARTER_CONTENT_IDENTITY']==dossier['SUBJECT_CONTENT_IDENTITY']==gates['CHARTER_CONTENT_IDENTITY'],'CONTENT_IDENTITY')
need(ident['CHARTER_APPROVAL_IDENTITY'] is None and ident['CHARTER_EFFECTIVE_LIFECYCLE_IDENTITY'] is None and ident['A15_GRANT_IDENTITIES']==[],'CIRCULAR_ISSUANCE')
need(mapping['EXACT_A15_SUBJECT']==read(B/'authority-subject-manifest.json')['TECHNICAL_PREPARATION_IDENTITY'] and mapping['VARIANT_BINDINGS']==read(B/'two-variant-authorization-inventory.json'),'WRONG_A15_SUBJECT')
need([x['BOUNDARY'] for x in mapping['FOUR_DISTINCT_BOUNDARIES']]==['CHARTER_ADOPTION','A15_NORMATIVE_SCOPE_APPROVAL','A15_EXECUTION_AUTHORIZATION','A15_CAPTURE_PERSISTENCE_AUTHORIZATION'],'MANDATE_BOUNDARIES_COLLAPSED')
need(not mapping['CURRENT_A15_NORMATIVE_DECISION_READY'] and not mapping['CURRENT_A15_EXECUTION_DECISION_READY'],'A15_READY_FROM_DRAFT')
for pin in dossier['INDEPENDENT_QUALIFICATION_EVIDENCE']:need(sha(pin['PATH'])==pin['RAW_SHA256'],'DOSSIER_EVIDENCE_PIN')
need('actual explicit owner selection' in dossier['OPTIONS'][0]['EFFECTIVE_BOUNDARY'] and 'in order' in dossier['OPTIONS'][0]['EFFECTIVE_BOUNDARY'],'ADOPTION_BOUNDARY')
report=read('docs/plans/KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_V1_0_DRAFT.json')
need(report['CHARTER_CONTENT']==charter and report['CHARTER_CONTENT_IDENTITY']==id and report['CHARTER_ADOPTED']=='NO' and report['CHARTER_EFFECTIVE']=='NO','COMPANION_CONTENT_OR_STATE')
preserved=read(E/'lessons-register-preservation.json')
for pin in preserved['LIVE_PINS']:need(sha(pin['PATH'])==pin['RAW_SHA256'],'LESSONS_REGISTER_CHANGED')
need(dossier['SELECTION'] is None and dossier['DECISION_READY'] and dossier['ISSUING_ROLE']==charter['GOVERNING_AUTHORITY']['ROLE_ID'] and len(dossier['OPTIONS'])==2,'ADOPTION_DOSSIER')
need([x['OPTION_ID'] for x in dossier['OPTIONS']]==['ADOPT_KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_V1_0','DECLINE_KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_V1_0'] and all(not x['A15_AUTHORITY_ISSUED'] for x in dossier['OPTIONS']),'ADOPTION_AS_A15_GRANT')
need(gates['CHARTER_CONTENT_COMPLETE'] and gates['CHARTER_ADOPTION_READY'] and not gates['CHARTER_EFFECTIVE'] and not gates['CHARTER_ADOPTED'] and not gates['A15_NORMATIVE_AUTHORITY_ISSUED'] and not gates['A15_EXECUTION_AUTHORITY_ISSUED'],'READINESS_AS_ADOPTION')
# External owner declaration precedes immutable charter content; approval,
# lifecycle and qualification-grant identities point forwards, never into the
# content or declaration they approve.
nodes=['OWNER_DECLARATION','CHARTER_CONTENT','QUALIFICATION_REPORT','OWNER_ADOPTION_DECISION','REVIEWED_RECORD','APPROVED_RECORD','EFFECTIVE_RECORD','EXACT_DELEGATION','NORMATIVE_APPROVAL','EXECUTION_APPROVAL','EVIDENCE_APPROVAL','QUALIFICATION_EXECUTION']
edges=[['OWNER_DECLARATION','CHARTER_CONTENT'],['CHARTER_CONTENT','QUALIFICATION_REPORT'],['OWNER_DECLARATION','OWNER_ADOPTION_DECISION'],['CHARTER_CONTENT','OWNER_ADOPTION_DECISION'],['QUALIFICATION_REPORT','OWNER_ADOPTION_DECISION'],['OWNER_ADOPTION_DECISION','REVIEWED_RECORD'],['REVIEWED_RECORD','APPROVED_RECORD'],['APPROVED_RECORD','EFFECTIVE_RECORD'],['EFFECTIVE_RECORD','EXACT_DELEGATION'],['EFFECTIVE_RECORD','NORMATIVE_APPROVAL'],['NORMATIVE_APPROVAL','EXECUTION_APPROVAL'],['EXECUTION_APPROVAL','EVIDENCE_APPROVAL'],['EVIDENCE_APPROVAL','QUALIFICATION_EXECUTION']]
def sort(es):
 todo=set(nodes);result=[]
 while todo:
  first=sorted(n for n in todo if not any(b==n and a in todo for a,b in es));need(bool(first),'CIRCULAR_AUTHORITY');result+=first;todo.difference_update(first)
 return result
order=sort(edges)
controls=[]
def reject(label,fn):
 try:fn()
 except (ValueError,AssertionError,KeyError):controls.append({'CONTROL':label,'RESULT':'REJECTED'});return
 raise AssertionError('Escaped negative:'+label)
def exact_value(a,b):need(a==b,'EXACT_VALUE_MISMATCH')
reject('OWNER_DECLARATION_CHANGED',lambda:exact_value(decl['EXACT_OWNER_AUTHORITY_DECLARATION']+' invented authority',exact[0]))
reject('SCOPE_LIMIT_REMOVED',lambda:need('engineering governance only' in source,'SCOPE_NOT_DECLARED'))
reject('WRONG_CHARTER_CONTENT_IDENTITY',lambda:exact_value(dict(id,sha256='0'*64),id))
reject('WRONG_VERSION',lambda:exact_value('LATEST',charter['CHARTER_VERSION']))
reject('LIFECYCLE_SKIPPED',lambda:exact_value(expected_edges[1:],expected_edges))
reject('TRANSITIVE_DELEGATION',lambda:need('Subdelegation automatically permitted' in delegation['RULES'],'NOT_AUTHORIZED'))
reject('IMPLICIT_DELEGATE',lambda:need('engineer_title' in delegation['REQUIRED_FIELDS'],'ROLE_NOT_EVIDENCE'))
for label,term in [('GENERAL_ENGINEERING_INCLUDED',exclusions[0]),('PRODUCTION_INCLUDED',exclusions[1]),('EXTERNAL_SYSTEM_PERMISSION',exclusions[2]),('GOVERNMENT_ENVIRONMENT_PERMISSION',exclusions[3]),('SECURITY_BYPASS',exclusions[4]),('UNRESTRICTED_NATIVE_EXECUTION',exclusions[5]),('AUTOMATIC_SCENARIO_APPROVAL',exclusions[6]),('AUTOMATIC_A15_EXECUTION',exclusions[7])]:
 bad=list(exclusions);bad.remove(term);reject(label,lambda bad=bad:exact_value(bad,charter['EXCLUSIONS']))
reject('CHARTER_SELF_AUTHORITY_CYCLE',lambda:sort(edges+[['EFFECTIVE_RECORD','OWNER_DECLARATION']]))
reject('APPROVAL_INCLUDED_IN_CONTENT_HASH',lambda:exact_value(hashlib.sha256(cb(dict(charter,APPROVAL_EVIDENCE='invented'))).hexdigest(),id['sha256']))
reject('WRONG_A15_SUBJECT',lambda:exact_value(mapping['CHECKPOINT_IDENTITY'],mapping['EXACT_A15_SUBJECT']))
reject('WRONG_A15_VARIANT',lambda:exact_value(mapping['VARIANT_BINDINGS'][0]['VARIANT_ID'],mapping['VARIANT_BINDINGS'][1]['VARIANT_ID']))
reject('OWNER_DECLARATION_AS_ADOPTION',lambda:need(decl['CHARTER_ADOPTED'],'DECLARATION_NOT_ADOPTION'))
reject('DRAFT_COMBINATION_AS_EXECUTION',lambda:need(composition['CURRENT_COMBINED_A15_GRANT_PERMITTED_BY_EFFECTIVE_CHARTER'],'NOT_EFFECTIVE_OR_GRANTED'))
reject('FROZEN_ACCEPTANCE_SILENTLY_CHANGED',lambda:need(charter['NORMATIVE_QUALIFICATION_AUTHORITY']['MANDATE_TO_EXECUTE_IMPLIED'],'NO_EXECUTION_FROM_INTERPRETATION'))
print(json.dumps({'RESULT':'PASS_DRAFT_QUALIFICATION','CHARTER_CONTENT_IDENTITY':id,'VERSION':'1.0','CHARTER_CONTENT_COMPLETE':True,'CHARTER_ADOPTION_READY':True,'CHARTER_EFFECTIVE':False,'CHARTER_ADOPTED':False,'A15_NORMATIVE_DECISION_READY':False,'A15_EXECUTION_DECISION_READY':False,'DELEGATIONS_ISSUED':0,'A15_GRANTS_ISSUED':0,'NON_CIRCULARITY':{'NODES':nodes,'EDGES':edges,'TOPOLOGICAL_ORDER':order,'ACYCLIC':True},'NEGATIVE_CONTROLS':controls,'NATIVE_EFFECTS':0},sort_keys=True))
