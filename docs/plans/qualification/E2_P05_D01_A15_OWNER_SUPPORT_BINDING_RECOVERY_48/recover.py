import pathlib,json,hashlib,sys
P=pathlib.Path('docs/plans/qualification');E=P/'E2_P05_D01_A15_OWNER_SUPPORT_BINDING_RECOVERY_48'
def load(p):return json.loads(p.read_text())
def pin(p):return {'path':str(p),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def key(x):return canon(x).decode()
def write(name,x):(E/name).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
auth={}
for package in ['E2_P05_D01_A15_NORMATIVE_INSTANCE_CLOSURE_PLANNING_47','E2_P05_D01_A15_GOVERNED_SEMANTIC_ELICITATION_46','E2_P05_D01_A15_RETAINED_DATA_BINDING_45']:
 for f,h in load(P/package/'evidence-index.json')['FILES'].items():
  path=pathlib.Path(f)
  if not path.exists():path=P/package/f
  assert hashlib.sha256(path.read_bytes()).hexdigest()==h,f
  auth[str(path)]=h
front=load(P/'E2_P05_D01_A15_NORMATIVE_INSTANCE_CLOSURE_PLANNING_47/minimal-independent-closure-frontier.json')['ITEMS'];assert [f['FRONTIER_ID'] for f in front]==['F01','F02','F03','F04','F05','F06','F07']
Gpath=P/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json';g=load(Gpath);assert len(g['NODES'])==131 and len(g['EDGES'])==474 and g['SOURCE_COUNT']==54
assert hashlib.sha256(Gpath.read_bytes()).hexdigest()=='6bd38c5d5d0af811e8ccf7423bf3ecaee4602260e7a183cb61fad43654f2d895'
cap=pathlib.Path(g['CAPSULE_SOURCE']['path']);assert hashlib.sha256(cap.read_bytes()).hexdigest()==g['CAPSULE_SOURCE']['raw_sha256']
auth[str(Gpath)]=pin(Gpath)['raw_sha256'];auth[str(cap)]=pin(cap)['raw_sha256']
# Only immutable decode and native read-only predicates, no restore/replay/application.
from adapter.planner import codec as c, typed_proofs as tp, gates,model as m
bundle=c._unwire(load(cap)['canonical_content']['bundle']);state=bundle.current
assert c._wire(c.snapshot_id(state))==g['PRESTATE_ID']
for f in ['adapter/planner/codec.py','adapter/planner/typed_proofs.py','adapter/planner/gates.py','adapter/planner/proof_installation.py','adapter/planner/installation.py']:
 auth[f]=pin(pathlib.Path(f))['raw_sha256']
proofs=load(P/'E2_P05_D01_A15_RETAINED_DATA_BINDING_45/binding-D02.json')['VALUE'];rootrows=load(P/'E2_P05_D01_A15_RETAINED_DATA_BINDING_45/binding-D01.json')['VALUE'];proposed=load(P/'E2_P05_D01_A15_GOVERNED_SEMANTIC_ELICITATION_46/K01-root-applicability.json')
records={key(n['NATIVE_IDENTITY']):(i,n) for i,n in enumerate(g['NODES']) if n.get('NATIVE_RECORD') and n.get('NATIVE_IDENTITY')}
source_nodes=[(i,n) for i,n in enumerate(g['NODES']) if n.get('TYPE')=='SOURCE_CONTENT'];sources=[]
for i,n in source_nodes:
 p=n['SOURCE_PIN'];f=pathlib.Path(p['path']);assert p['identity']==n['NATIVE_IDENTITY'];assert p['profile']['value']=='raw-file-sha256' and p['pointer']==''
 assert hashlib.sha256(f.read_bytes()).hexdigest()==p['identity']['sha256'],str(f)
 auth[str(f)]=pin(f)['raw_sha256']
 sources.append({'CONTENT_IDENTITY':n['NATIVE_IDENTITY'],'SOURCE_PATHS':[p['path']],'SOURCE_PINS':[p],'NATIVE_SOURCE_ROLE':'Retained pin; role determined per native record binding, not presence','PROVENANCE':{'graph_pointer':f'/NODES/{i}','graph_source':pin(Gpath)},'SCOPE':n['SCOPE'],'LINEAGE':n['LINEAGE'],'GENERATION':n['GENERATION'],'CURRENTNESS':{'PHYSICAL_BYTES':'PASS','OPERATIVE_ROLE':'NOT_INFERRED_FROM_BYTES'}})
source_by={key(s['CONTENT_IDENTITY']):s for s in sources}
owner=[]
for i,r in enumerate(rootrows):
 ni,n=records[key(r['ROOT_ID'])];v=n['NATIVE_RECORD'];uses=[p for p in proofs if p['TARGET']==r['ROOT_ID']];native=[p for p in state.typed_proofs if c._wire(p.target)==r['ROOT_ID']]
 current=[tp.usable(state,p) for p in native]
 confirmed=bool(native) and all(current)
 role='Typed proof target/consumer' if confirmed else 'Action operation/source consumer' if v['$type']=='Action' else 'Accepted knowledge record; support role separate' if v['$type']=='KnowledgeRecord' else 'Authority/evidence entity role' if v['$type']=='GraphEntity' else v['$type']
 missing=[] if confirmed else ['Complete independently qualified consumer/root responsibility for A15; native role alone does not establish coverage','Complete applicable support relationship/source-role binding under a governing scope rule']
 owner.append({'SUBJECT_ID':r['ROOT_ID'],'NATIVE_TYPE':v['$type'],'DECLARED_ROLE':role,'NATIVE_ROLE_FIELDS':{k:v[k] for k in ('operation','source','producer','kind','permissions','target','requirements','prerequisites','evidence') if k in v},'ACCEPTANCE_STATUS':r['ACCEPTANCE_STATUS'],'CURRENTNESS':{'proof_usability':current,'other_native_record_currentness':'Not asserted solely from acceptance/status','source_bytes':'Physical pins independently checked'},'PROOF_CONSUMER_RELATIONSHIP':[{'proof':p['NATIVE_IDENTITY'],'target':p['TARGET'],'supports':p['DECLARED_SUPPORTS']} for p in uses],'AUTHORITY_BINDING':[p['AUTHORITY'] for p in uses] or v.get('authority'),'CONTEXT_BINDING':g['CONTEXT'],'SCOPE':r['SCOPE'],'LINEAGE':r['LINEAGE'],'GENERATION':r['GENERATION'],'PROVENANCE':v.get('provenance',v.get('source')),'EVIDENCE_SOURCE':{'source':pin(Gpath),'pointer':f'/NODES/{ni}/NATIVE_RECORD','D01_pointer':f'/VALUE/{i}'},'NATIVE_EVIDENCE_CLASSIFICATION':'EVIDENCE_CONFIRMED_APPLICABLE' if confirmed else 'INSUFFICIENT_EVIDENCE','CLASSIFICATION_MEANING':'Native current typed-proof consumer confirmed, not adopted A15 ownership' if confirmed else 'Native facts retained; exact A15-qualified consumer applicability insufficient','PROPOSED_K01_CLASSIFICATION':proposed[i]['PROPOSED_CLASSIFICATION'],'AUTHORIZED_NORMATIVE_APPLICABILITY':'UNDETERMINED_NOT_AUTHORIZED','MISSING_DISCRIMINATORS':missing})
proof_inv=[]
for p in state.typed_proofs:
 contract=next(x for x in state.proof_contracts if x.id==p.contract)
 assert tp.identity(p)==p.id and tp.identity(contract)==contract.id
 support_checks=[tp.support_identity(state,r)==h for r,h in zip(p.supports,p.support_identities)];assert all(support_checks)
 proof_inv.append({'PROOF_ID':c._wire(p.id),'PROOF_CONTRACT_ID':c._wire(p.contract),'OWNER_ROOT':c._wire(p.target),'DECLARED_SUPPORTS':c._wire(p.supports),'SUPPORT_FINGERPRINTS':c._wire(p.support_identities),'SUPPORT_GROUP_TYPE':'ALL within proof, ANY applicable usable proofs for target','CURRENTNESS':{'native_usable':tp.usable(state,p),'fingerprints_match':support_checks},'AUTHORITY':c._wire(p.authority),'CONTEXT':c._wire(state.context),'SCOPE':p.scope,'LINEAGE':p.lineage,'GENERATION':p.generation,'PROVENANCE':c._wire(p.provenance),'NATIVE_IDENTITY_DOMAIN_NOTE':'Support fingerprints are planner-proof-support-v1, not raw file content IDs'})
bindings=[]
slotproof=next(p for p in state.typed_proofs if p.target==m.SlotId('E2-SLOT'));kp=next(k for k in state.knowledge if k.id==m.KnowledgeId('E2-K-REENTER'))
source=source_by[key(c._wire(kp.provenance.identity))]
# Explicit native rule: codec.invalidate_sources.knowledge checks record.provenance.identity in changed.
# No transition performed; this binds content to native Knowledge support, not source to fingerprint equality.
for owner_root,support,btype,path in [('E2-SLOT',c._wire(kp.id),'EXACT_NATIVE_BINDING',['KnowledgeRecord.provenance.identity','SLOT_PROOF.supports[0]']),('E2-ROOT',c._wire(m.SlotId('E2-SLOT')),'DETERMINISTICALLY_DERIVED_BINDING',['Knowledge content dependency','SLOT proof mandatory support','ROOT proof mandatory Slot support'])]:
 proof=next(p for p in state.typed_proofs if p.target.value==owner_root)
 bindings.append({'SOURCE_CONTENT_IDENTITY':source['CONTENT_IDENTITY'],'NATIVE_SUPPORT_IDENTITY':support,'PROOF_ID':c._wire(proof.id),'OWNER_ROOT':c._wire(proof.target),'BINDING_EVIDENCE':[{'source':pin(Gpath),'pointer':f'/NODES/{records[key(c._wire(kp.id))][0]}/NATIVE_RECORD/provenance/identity'},{'source':pin(pathlib.Path('adapter/planner/codec.py')),'location':'invalidate_sources knowledge(record): exact provenance identity is an explicit source invalidation condition'},{'source':pin(pathlib.Path('adapter/planner/typed_proofs.py')),'location':'support_identity / usable: all declared support fingerprints/usability required'}],'BINDING_TYPE':btype,'IDENTITY_DOMAIN':'Raw content identity → native support relation; not identity equality to support fingerprint','CURRENTNESS':{'source_bytes':'PASS','typed_proof':tp.usable(state,proof),'support_fingerprint':'PASS','A15_coverage':'UNAUTHORIZED_UNDETERMINED'},'SCOPE':proof.scope,'LINEAGE':proof.lineage,'GENERATION':proof.generation,'PROVENANCE':{'source_paths':source['SOURCE_PATHS'],'knowledge':c._wire(kp.provenance),'proof':c._wire(proof.provenance)},'ROLE':'OPERATIVE_PROOF_SUPPORT' if btype=='EXACT_NATIVE_BINDING' else 'QUALIFIED_DEPENDENCY','RELATION_PATH':path,'NECESSITY_NOTE':'Native required-by-proof dependency is established; A15 target membership and absence of other usable alternatives are not inferred'})
# Keep direct proof provenance/configuration source candidates distinct from declared-support identity.
for p in proofs:
 ci=p['PROVENANCE']['identity'];s=source_by.get(key(ci))
 bindings.append({'SOURCE_CONTENT_IDENTITY':ci,'NATIVE_SUPPORT_IDENTITY':p['NATIVE_IDENTITY'],'PROOF_ID':p['NATIVE_IDENTITY'],'OWNER_ROOT':p['TARGET'],'BINDING_TYPE':'SEMANTIC_CORRESPONDENCE_ONLY','ROLE':'UNDETERMINED','BINDING_EVIDENCE':[{'source':pin(P/'E2_P05_D01_A15_RETAINED_DATA_BINDING_45/binding-D02.json'),'pointer':'/VALUE'}],'CURRENTNESS':{'record_usable':p['USABILITY'],'pin_present':s is not None},'SCOPE':p['SCOPE'],'LINEAGE':p['LINEAGE'],'GENERATION':p['GENERATION'],'PROVENANCE':p['PROVENANCE'],'MISSING_DISCRIMINATOR':'Role-specific installed definition/contract-source applicability is a different binding from declared support; no raw-content = native-proof-ID equality or A15 necessity inferred'})
missing={'OWNER':[{'SUBJECT_ID':r['SUBJECT_ID'],'MISSING':r['MISSING_DISCRIMINATORS']} for r in owner if r['MISSING_DISCRIMINATORS']],'SUPPORT':[{'IDENTITY':r['NATIVE_SUPPORT_IDENTITY'],'MISSING':r.get('MISSING_DISCRIMINATOR')} for r in bindings if r['ROLE']=='UNDETERMINED'],'UNENUMERATED_RELEVANCE':'No complete unknown source-support universe cardinality asserted while 19 owner roles and additional qualified dependencies remain unspecified'}
updates=[]
for f in front:
 status='PARTIALLY_REDUCED' if f['FRONTIER_ID'] in ('F01','F02') else 'BLOCKED_BY_NORMATIVE_KNOWLEDGE' if f['FRONTIER_ID'] in ('F03','F04') else 'BLOCKED_BY_AUTHORITY' if f['FRONTIER_ID']=='F05' else 'BLOCKED_BY_EXECUTION_ACCEPTANCE'
 updates.append({**f,'48_STATUS':status,'REMOVED':False})
semantic={'owner':owner,'proofs':proof_inv,'sources':sources,'bindings':bindings,'missing':missing,'frontier':updates}
identity='qualification-A15-owner-support-recovery-v1:'+hashlib.sha256(canon(semantic)).hexdigest()
if '--stdout' in sys.argv:print(json.dumps({'IDENTITY':identity,'COUNTS':{'owners_confirmed':2,'owners_insufficient':19,'source_records':54,'exact':1,'derived':1,'correspondence_only':4}},sort_keys=True));sys.exit()
for name,value in [('owner-role-evidence-inventory.json',owner),('per-subject-applicability.json',[{k:r[k] for k in ('SUBJECT_ID','NATIVE_EVIDENCE_CLASSIFICATION','PROPOSED_K01_CLASSIFICATION','AUTHORIZED_NORMATIVE_APPLICABILITY','MISSING_DISCRIMINATORS')} for r in owner]),('typed-proof-support-inventory.json',proof_inv),('source-content-identity-inventory.json',sources),('source-support-binding-inventory.json',bindings),('missing-discriminators.json',missing),('updated-seven-family-frontier.json',updates)]:write(name,value)
write('authentication.json',{'PACKAGE_47_AUTHENTICATED':True,'RECOVERY_FAMILIES':['F01','F02'],'SOURCE_PINS':auth,'A15_SNAPSHOT':g['PRESTATE_ID'],'NATIVE_QUERY_OPERATIONS':['Decode retained wire representation','snapshot_id','typed_proofs.identity','typed_proofs.usable','typed_proofs.support_identity'],'NATIVE_TRANSITIONS_SAVES_REPLAYS':0,'RECOVERY_IDENTITY':identity})
write('track-impact.json',{'N':[{'GAP_ID':i,'PREVIOUS_STATUS':'Incomplete applicability or mapping','RECOVERED_EVIDENCE':'Explicit native knowledge content dependency and ROOT/SLOT support fingerprint/currentness facts','NEW_STATUS':'FACTUAL_INPUT_PARTIALLY_REDUCED','REMAINING_NORMATIVE_REQUIREMENT':'Complete owner/support applicability and relevance/necessity; proposed knowledge not adopted'} for i in ('S01','S07','S08','S16','N27')],'E':[{'GAP_ID':'E01','NEW_STATUS':'MORE_TYPED_INPUT_EVIDENCE; descriptor not ready','REMAINING':'Complete authorized target universe'}],'OPERAND_PROMOTIONS':0})
write('readiness-assessment.json',{'NORMATIVE_INSTANCE_COMPLETE':False,'NORMATIVE_DECISION_READY':False,'A15_EXECUTION_CONTRACT_READY':False,'F01_COMPLETE':False,'F02_COMPLETE':False,'FIRST_REMAINING_INPUT_FAMILY':'F01','NEXT_BOUNDED_ACTION':'Focused normative discrimination of the retained subjects still lacking qualified consumer responsibility; no broad elicitation or execution launched','FOCUSED_QUESTION':{'QUESTION_ID':'F01-OWNER-ROLE-REMAINDER','SUBJECT_IDS':[r['SUBJECT_ID'] for r in owner if r['MISSING_DISCRIMINATORS']],'QUESTION':'For each listed retained subject, which authoritative native role/qualified dependency establishes A15 consumer responsibility, or which finite role-based normative inclusion/exclusion rule supplies the missing responsibility? Identify exact evidence or retain UNDETERMINED; accepted status and graph membership cannot suffice.','STATUS':'PREPARED_ONLY_NOT_ANSWERED'},'E_ORACLE_NOT_USED_TO_BLOCK_N':'Native owner/source applicability remains independently incomplete'})
