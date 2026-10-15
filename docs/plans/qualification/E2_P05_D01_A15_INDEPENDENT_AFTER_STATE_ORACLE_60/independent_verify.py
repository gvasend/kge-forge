"""Separate declarative overlay verifier, using retained inputs, not oracle output as its input."""
import pathlib,json,copy,hashlib
P=pathlib.Path('docs/plans');Q=P/'qualification';E=Q/'E2_P05_D01_A15_INDEPENDENT_AFTER_STATE_ORACLE_60'
def read(p):return json.loads(p.read_text())
def bytesof(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def aid(x,namespace):return {'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':namespace,'sha256':hashlib.sha256(bytesof(x)).hexdigest()}
def stateid(x):return aid({'schema':'PLANNER-SNAPSHOT-1','snapshot':x},'planner-snapshot-v1')
def en(t,v):return {'$enum':t,'value':v}
# Native stable set ordering; statuses originally sorted by ID and explicit record overlays sorted here.
SETS=('actions','statuses','roots','slots','knowledge','assertions','entities','predicates','information','decisions','evidence_requirements','external_gates','receipt_admissions','boundaries','goals','validation_instances','proof_contracts','typed_proofs','installed_definitions','ingress_contracts','validation_contracts','validation_support_contracts','validation_transaction_contracts','validation_results','validation_support_records')
def order(x):
 for k in SETS:
  if k in x:x[k].sort(key=bytesof)
 return x

g=read(Q/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json');bundle=read(pathlib.Path(g['CAPSULE_SOURCE']['path']))['canonical_content']['bundle'];original=order(copy.deepcopy(bundle['current']));assert stateid(original)==g['PRESTATE_ID']
# Independent traversal of serialized native request provenances, not Package59's expected touched-role list.
def request_sources(request):
 found=[]
 for p in [request['definition']['provenance'],request['authority']['admission_provenance']]+request.get('definition_sources',[])+[x['accepted_admission_provenance'] for x in request.get('authority_bindings',[])]:found.append(p['identity'])
 return found
prov=min(original['proof_contracts'],key=lambda p:p['id']['sha256'])['provenance'];results=[]
for current in original['typed_proofs']:
 source=current['provenance']['identity'];expected=copy.deepcopy(original)
 for p in expected['proof_contracts']+expected['typed_proofs']:
  if p['provenance']['identity']==source:p['validation']=en('ValidationState','STALE')
 for entity in expected['entities']:
  if entity['provenance']['identity']==source:entity['validation']=en('ValidationState','STALE')
 touched=[]
 for role in expected['installed_definitions']:
  if source in request_sources(role['request']):role['validation']=en('ValidationState','STALE');touched.append(role['id'])
 assert len(touched)==2
 for slot in expected['slots']:slot['state']=en('SlotState','UNRESOLVED')
 for root in expected['roots']:root['state']=en('ConditionState','UNRESOLVED')
 order(expected);support=stateid(expected)
 status=next(p for p in expected['statuses'] if p['id']['value']=='E2-FINISH');status['state']=en('ActionState','BLOCKED')
 expected['reevaluations'].append({'$type':'ReevaluationRecord','dependencies':[source],'action':{'$type':'ActionId','value':'E2-FINISH'},'old_state':en('ActionState','ACTIONABLE'),'support_state':support,'new_state':en('ActionState','BLOCKED'),'provenance':prov});order(expected)
 afterid=stateid(expected);result={'$type':'SourceInvalidation','changed':[source],'expected_snapshot':g['PRESTATE_ID']};eventid=aid({'sequence':20,'parent':g['PRESTATE_ID'],'parent_event':bundle['events'][-1]['identity'],'result':result,'after':afterid},'planner-event-v1')
 event={'$type':'ExecutionEvent','sequence':20,'parent_snapshot':g['PRESTATE_ID'],'parent_event':bundle['events'][-1]['identity'],'result':result,'after_snapshot':afterid,'identity':eventid}
 eb=copy.deepcopy(bundle);eb['current']=expected;eb['events'].append(event);bid=aid({'schema':'PLANNER-BUNDLE-1','bundle':eb},'planner-bundle-v1')
 name='PROPOSED-'+current['proof_type']['value']+'-PROVENANCE-WITHDRAWAL';oracle=read(E/(name+'-expected-output.json'))
 assert oracle['EXPECTED_STATE']==expected and oracle['EXPECTED_STATE_IDENTITY']==afterid
 assert oracle['ORDERED_TRACE']['EXPECTED_NEXT_EVENT']==event and oracle['CAPTURE_EXPECTATION']['EXPECTED_UPDATED_BUNDLE']==eb and oracle['CAPTURE_EXPECTATION']['EXPECTED_BUNDLE_ID']==bid
 assert expected['reevaluations'][:len(original['reevaluations'])]==original['reevaluations']
 results.append({'VARIANT':name,'AFTER_STATE':afterid,'EVENT':eventid,'BUNDLE':bid,'INDEPENDENT_STATE_COMPARISON':'PASS','TOUCHED_ROLES':touched})
print(json.dumps(results,sort_keys=True))
