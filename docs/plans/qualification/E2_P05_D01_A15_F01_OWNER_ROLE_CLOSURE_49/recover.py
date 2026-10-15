import pathlib,json,hashlib,sys
from adapter.planner import codec as c, model as m,typed_proofs as tp,proof_installation as pi,gates
P=pathlib.Path('docs/plans/qualification');E=P/'E2_P05_D01_A15_F01_OWNER_ROLE_CLOSURE_49'
def load(p):return json.loads(p.read_text())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def pin(p):return {'path':str(p),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def write(n,x):(E/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
auth={}
for package in ['E2_P05_D01_A15_NORMATIVE_INSTANCE_CLOSURE_PLANNING_47','E2_P05_D01_A15_OWNER_SUPPORT_BINDING_RECOVERY_48','E2_P05_D01_A15_GOVERNED_SEMANTIC_ELICITATION_46','E2_P05_D01_A15_RETAINED_DATA_BINDING_45','E2_P05_D01_SOURCE_BYTES_DISPATCH_CORRECTION_33']:
 for name,h in load(P/package/'evidence-index.json')['FILES'].items():
  p=pathlib.Path(name)
  if not p.exists():p=P/package/name
  assert hashlib.sha256(p.read_bytes()).hexdigest()==h,name
  auth[str(p)]=h
fpath=P/'E2_P05_D01_A15_NORMATIVE_INSTANCE_CLOSURE_PLANNING_47/minimal-independent-closure-frontier.json';front=load(fpath)['ITEMS'];f01=front[0];assert f01['FRONTIER_ID']=='F01'
f48=load(P/'E2_P05_D01_A15_OWNER_SUPPORT_BINDING_RECOVERY_48/updated-seven-family-frontier.json')[0];assert all(f48[k]==v for k,v in f01.items())
oldgap=load(P/'E2_P05_D01_A15_APPLICABILITY_GAP_DECOMPOSITION_44/typed-gap-inventory.json')
accept={'EXACT_F01':f01,'SOURCE':pin(fpath),'POINTER':'/ITEMS/0','REQUIRED_INPUTS':[f01['MISSING_VALUE']],'DEPENDENT_GAPS':f01['DEPENDENT_GAPS'],'PREREQUISITES_BY_DEPENDENT_GAP':{r['GAP_ID']:r['DEPENDENCIES'] for r in oldgap if r['GAP_ID'] in f01['DEPENDENT_GAPS']},'ACCEPTANCE_RULE':{'VALUE':f01['VALIDATION_RULE'],'CLASSIFICATION':'EXACT_RETAINED_VALIDATION_RULE'},'CLOSURE_CONDITION':{'VALUE':'Every required owner role/currentness/support fact or authoritative justified exclusion independently established; normative adoption separate','CLASSIFICATION':'Derived from F01 missing-value/validation and user Package49 gate; not a literal original field'},'AUTHORITY_REQUIREMENT':f01['AUTHORITY_REQUIRED'],'ORIGINAL_FIELDS_ABSENT':['PREREQUISITES','ACCEPTANCE_RULE','CLOSURE_CONDITION'],'NOTE':'Derived views preserve original names and exact source; absent fields are not fabricated as retained fields'}
gpath=P/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json';g=load(gpath);assert len(g['NODES'])==131 and len(g['EDGES'])==474
cap=pathlib.Path(g['CAPSULE_SOURCE']['path']);assert hashlib.sha256(cap.read_bytes()).hexdigest()==g['CAPSULE_SOURCE']['raw_sha256'];s=c._unwire(load(cap)['canonical_content']['bundle']).current;assert c._wire(c.snapshot_id(s))==g['PRESTATE_ID']
roots=load(P/'E2_P05_D01_A15_RETAINED_DATA_BINDING_45/binding-D01.json')['VALUE'];prior=load(P/'E2_P05_D01_A15_OWNER_SUPPORT_BINDING_RECOVERY_48/owner-role-evidence-inventory.json');proposed=load(P/'E2_P05_D01_A15_GOVERNED_SEMANTIC_ELICITATION_46/K01-root-applicability.json')
# Select native definitions by exact type, not generic ID index (ActionStatus shares ActionId).
expected={'ActionId':'Action','ConditionId':'RootCondition','SlotId':'ValueSlot','KnowledgeId':'KnowledgeRecord','EntityId':'GraphEntity','EvidenceId':'EvidenceRequirement'}
rows=[];defects=[]
for j,r in enumerate(roots):
 matches=[(i,n) for i,n in enumerate(g['NODES']) if n.get('NATIVE_IDENTITY')==r['ROOT_ID'] and n.get('TYPE')==expected[r['ROOT_ID']['$type']] and n.get('NATIVE_RECORD')]
 assert len(matches)==1,(r['ROOT_ID'],len(matches));i,n=matches[0];v=n['NATIVE_RECORD']
 prs=[p for p in s.typed_proofs if c._wire(p.target)==r['ROOT_ID']];usable=[tp.usable(s,p) for p in prs];action=v['$type']=='Action'
 if prior[j]['NATIVE_TYPE']!=v['$type']:defects.append({'SUBJECT_ID':r['ROOT_ID'],'48_SELECTED_TYPE':prior[j]['NATIVE_TYPE'],'49_RECOVERED_TYPE':v['$type'],'CAUSE':'Generic identity index collapsed Action/ActionStatus shared ActionId','49_RULE':'Exact type+identity selection from graph and native model; no source change'})
 current={'typed_proof_usability':usable,'native_current_completion':gates.current_completion(s,next(a.id for a in s.actions if c._wire(a.id)==r['ROOT_ID'])) if action else None,'other_role_currentness':'Not inferred solely from serialized acceptance'}
 yes=bool(prs) and all(usable) or action
 rows.append({'SUBJECT_ID':r['ROOT_ID'],'NATIVE_TYPE':v['$type'],'ROLE':'Declared Action source/operation consumer' if action else 'Typed proof target/consumer' if prs else v['$type'],'ACCEPTANCE_STATUS':r['ACCEPTANCE_STATUS'],'CURRENTNESS':current,'PROOF_CONSUMER_STATUS':[{'PROOF_ID':c._wire(p.id),'CONTRACT_ID':c._wire(p.contract),'SUPPORTS':c._wire(p.supports),'FINGERPRINTS':c._wire(p.support_identities)} for p in prs],'SUPPORT_DEPENDENCY_STATUS':{'NATIVE_FIELDS':{k:v[k] for k in ['source','evidence','requirements','prerequisites','producer','target','permissions'] if k in v},'A15_NECESSITY':'UNDETERMINED'},'AUTHORITY':c._wire(prs[0].authority) if prs else v.get('authority'),'CONTEXT':g['CONTEXT'],'SCOPE':n['SCOPE'],'LINEAGE':n['LINEAGE'],'GENERATION':n['GENERATION'],'PROVENANCE':v.get('provenance',v.get('source')),'EVIDENCE':{'source':pin(gpath),'pointer':f'/NODES/{i}/NATIVE_RECORD','native_rule':'codec.invalidate_sources: Action source identity can hold Action; typed_proofs.usable: declared supports determine proof usability'},'NATIVE_SUPPORT_CONSUMER':'YES' if yes else 'UNDETERMINED','A15_OWNER_APPLICABILITY':proposed[j]['PROPOSED_CLASSIFICATION'],'A15_OWNERSHIP_AUTHORIZED':'NO','MISSING_OWNERSHIP_DISCRIMINATOR':'A15-qualified relevance/inclusion or authoritative exclusion for this native role; current typed consumer alone does not issue ownership authority' if yes else 'Complete role-qualified A15 inclusion/exclusion rule and applicable operative consumer relationship; no closed-world exclusion rule','MISSING_REASON':['NORMATIVE_APPLICABILITY_RULE_MISSING'] if yes else ['ROLE_EVIDENCE_MISSING','NORMATIVE_APPLICABILITY_RULE_MISSING'],'PROPOSED_VS_NATIVE_NOTE':'Native YES does not upgrade proposed UNDETERMINED or adopted applicability'})
old_candidates=[r for r in load(P/'E2_P05_D01_A15_OWNER_SUPPORT_BINDING_RECOVERY_48/source-support-binding-inventory.json') if r['BINDING_TYPE']=='SEMANTIC_CORRESPONDENCE_ONLY'];assert len(old_candidates)==4
source_nodes=[n for n in g['NODES'] if n.get('TYPE')=='SOURCE_CONTENT'];candidates=[]
configs=[]
for record in pi.records(s,'ROOT_SLOT_CONFIGURATION_SET'):
 d,body=pi.descriptor(record.request.definition);config=pi.configuration(record.request);configs.append((record,config,pi.support_current(s,record)))
for r in old_candidates:
 ci=r['SOURCE_CONTENT_IDENTITY'];pinmatch=[n['SOURCE_PIN'] for n in source_nodes if n['NATIVE_IDENTITY']==ci];assert len(pinmatch)==1
 links=[]
 for record,config,live in configs:
  entities,contracts=config[-2],config[-1]
  for entity in entities:
   if c._wire(entity.identity)==ci:
    cs=[x for x in contracts if x.provenance.identity==entity.identity or x.authority==entity.id]
    for contract in cs:
     if c._wire(contract.target)==r['OWNER_ROOT']:
      links.append({'INSTALLED_CONFIGURATION_ID':c._wire(record.id),'SOURCE_ENTITY_ID':c._wire(entity.id),'SOURCE_ENTITY_IDENTITY':c._wire(entity.identity),'CONTRACT_ID':c._wire(contract.id),'CONFIGURATION_CURRENT':live,'CONTRACT_CURRENT':pi.contract_current(s,contract),'ROLE_RULE_SOURCE':pin(pathlib.Path('adapter/planner/proof_installation.py')),'ROLE_RULE_LOCATION':'configuration + contract_current + normalize_dependencies: matching source entity identity/authority contributes exact contract dependency'})
 exact=bool(links) and all(x['CONFIGURATION_CURRENT'] and x['CONTRACT_CURRENT'] for x in links)
 candidates.append({'CANDIDATE_ID':'qualification-A15-proof-source-candidate-v1:'+hashlib.sha256(canon([ci,r['PROOF_ID']])).hexdigest(),'CONTENT_IDENTITY':ci,'SOURCE_PIN':pinmatch[0],'PROOF_ID':r['PROOF_ID'],'SUPPORT_ID':r['NATIVE_SUPPORT_IDENTITY'],'DECLARED_ROLE':'Installed proof-configuration source entity / contract dependency' if exact else 'Referenced proof provenance; operative role unestablished','CURRENTNESS':links,'SCOPE':r['SCOPE'],'LINEAGE':r['LINEAGE'],'GENERATION':r['GENERATION'],'PROVENANCE':r['PROVENANCE'],'CLASSIFICATION':'EXACT_OPERATIVE_SUPPORT' if exact else 'UNDETERMINED','MISSING_OPERATIVE_ROLE_DISCRIMINATOR':None if exact else 'Explicit current installed source-entity-to-contract dependency binding','ROLE_LIMIT':'Native configuration dependency, not equality to a declared support fingerprint and not A15 invalidation target selection','FAMILY':'F02','A15_TARGET_MEMBERSHIP':'UNDETERMINED'})
closed={'SUBJECT_INVENTORY_COMPLETE':True,'COMPLETENESS_DOMAIN':'The exact 21 retained D01 subjects only','A15_OWNER_SET_COMPLETE':False,'CLOSED_WORLD_RULE':'NONE_RECOVERED_FOR_A15_OWNERSHIP','SOURCE':'D01 enumerates subjects; no governing rule makes absent proof an authoritative ownership exclusion','EXCLUSIONS_FROM_ABSENCE_ALLOWED':False}
minimal={'STATUS':'FOCUSED_NORMATIVE_GAP_NOT_SELECTABLE','MINIMUM_MISSING_TERM':'A complete A15-specific role-to-responsibility inclusion/exclusion discriminator over retained typed subjects, including whether the retained 21-subject universe is exhaustive for owner coverage','ALREADY_PROPOSED':['Candidate subject types','Native currentness conjunction','Exact pre-state/context','Missing evidence → UNDETERMINED','No metadata-only necessity'],'NEEDS_VALUE':['For each native role: governing qualified support-consumer relationship that makes A15 responsible, or justified exclusion','Closed-world applicability coverage, if exclusions by absent role are intended'],'REQUIRED_RULE_FIELDS':['Applicable native types','Operative support-consumer role','Currentness','Exact state/scope/lineage/generation','Inclusion','Exclusion','Missing role handling','Verified normative issuing owner and adoption subject'],'AUTHORITY':'Preparation only; eventual bounded normative scope decision required','CANDIDATE_CLOSURE_CONTRACT_CREATED':False,'REASON':'No new finite complete predicate can be instantiated without supplying missing responsibility values; K01 cannot classify all subjects from native roles alone'}
updated=load(P/'E2_P05_D01_A15_OWNER_SUPPORT_BINDING_RECOVERY_48/updated-seven-family-frontier.json')
for f in updated:
 f['49_STATUS']='PARTIALLY_REDUCED' if f['FRONTIER_ID'] in ('F01','F02') else f['48_STATUS'];f['REMOVED']=False
semantic={'F01':accept,'subjects':rows,'source_candidates':candidates,'closed_world':closed,'gap':minimal,'frontier':updated,'projection_defects':defects}
id='qualification-A15-F01-evidence-v1:'+hashlib.sha256(canon(semantic)).hexdigest()
if '--stdout' in sys.argv:print(json.dumps({'IDENTITY':id,'NATIVE_SUPPORT_CONSUMERS_CONFIRMED':sum(r['NATIVE_SUPPORT_CONSUMER']=='YES' for r in rows),'OPERATIVE_CANDIDATES':sum(r['CLASSIFICATION']=='EXACT_OPERATIVE_SUPPORT' for r in candidates),'DEFECTS_CORRECTED_IN_NEW_INVENTORY':len(defects)},sort_keys=True));sys.exit()
for name,x in [('F01-acceptance-inventory.json',accept),('subject-role-applicability-matrix.json',rows),('four-proof-source-candidates.json',candidates),('closed-world-analysis.json',closed),('focused-normative-gap-dossier.json',minimal),('updated-seven-family-frontier.json',updated),('retained-projection-defect.json',defects)]:write(name,x)
write('cross-family-boundary.json',{'FOUR_CANDIDATES_BELONG_TO':'F02','F01_REQUIRES':'Exact native owner-role/currentness/support evidence or governing justified exclusions','NOT_REQUIRED_FOR_F01':'All four proof-provenance/configuration source mappings as an independent blanket prerequisite','PACKAGE_47_GRAPH':'Original S01/S08 dependencies retained; S07 source projection separate; related support evidence does not justify expanding F01','UNKNOWN_A15_RELEVANCE':'Native mapping facts do not close consumer responsibility or necessity'})
write('authentication.json',{'F01_AUTHENTICATED':True,'PINNED_FILES':auth,'GRAPH':pin(gpath),'CAPSULE':pin(cap),'PRESTATE':g['PRESTATE_ID'],'SEMANTIC_IDENTITY':id,'READ_ONLY_QUERIES_ONLY':True})
