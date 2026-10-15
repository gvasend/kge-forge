import pathlib,json,hashlib
P=pathlib.Path('docs/plans/qualification');E=P/'E2_P05_D01_A15_F01_F02_NORMATIVE_RELATIONSHIP_DECISION_51'
def read(p):return json.loads(p.read_text())
# Independent source reconstruction; no producer import.
f=read(P/'E2_P05_D01_A15_NORMATIVE_INSTANCE_CLOSURE_PLANNING_47/minimal-independent-closure-frontier.json')['ITEMS'];assert [x['FRONTIER_ID'] for x in f[:2]]==['F01','F02']
r=read(P/'E2_P05_D01_A15_F01_OWNER_ROLE_CLOSURE_49/subject-role-applicability-matrix.json');assert len(r)==21 and sum(x['NATIVE_SUPPORT_CONSUMER']=='YES' for x in r)==8
native=read(P/'E2_P05_D01_A15_GRAPH_SEMANTIC_PROJECTION_41/existing-native-proof-correspondence.json');assert len(native)==4
sources=read(P/'E2_P05_D01_A15_F02_SUPPORT_BINDING_CLOSURE_50/four-candidate-binding-evidence.json');assert len(sources)==4 and all(x['PROOF_SUPPORT_CLASSIFICATION']=='CONFIGURATION_ONLY' for x in sources)
for x in sources:
 n=next(n for n in native if n['NATIVE_IDENTITY']==x['PROOF_IDENTITY'])
 assert x['SOURCE_CONTENT_IDENTITY'] not in n['DECLARED_SUPPORTS'] and x['SOURCE_CONTENT_IDENTITY'] not in n['SUPPORT_FINGERPRINTS']
counts={'subject_count':len(r),'native_consumers':8,'configuration_records':len(sources),'content_count':len({json.dumps(x['SOURCE_CONTENT_IDENTITY'],sort_keys=True) for x in sources}),'complete_prospective_relations':0,'adoption':False}
assert counts['content_count']==2
schema=read(P/'E2_P05_D01_A15_NORMATIVE_KNOWLEDGE_CONTRACT_42/normative-knowledge-schema.json')
assert 'exclude its own ID and later selection/authorization receipt' in schema['FIELDS']['KNOWLEDGE_CONTRACT_ID']
questions=read(E/'focused-elicitation-catalog.json');assert len(questions)==3 and len({q['EXACT_MISSING_RELATIONSHIP'] for q in questions})==3
assert not read(E/'normative-relationship-gap-dossier.json')['DECISION_READY']
for filename,fields in [('owner-relationship-schema.json',['CONSUMER_IDENTITY','ROOT_IDENTITY','NATIVE_ROLE','APPLICABILITY_PREDICATE','CURRENTNESS','SCOPE','LINEAGE','GENERATION','AUTHORITY','PROVENANCE']),('source-support-relationship-schema.json',['SOURCE_CONTENT_IDENTITY','NATIVE_SUPPORT_IDENTITY','PROOF_IDENTITY','CONSUMER_ROOT_IDENTITY','DECLARED_SUPPORT_ROLE','CURRENTNESS','SCOPE','LINEAGE','GENERATION','AUTHORITY','PROVENANCE'])]:
 assert set(fields)<=set(read(E/filename)['REQUIRED_FIELDS'])
# Abstract fail-closed gates; this does not instantiate an A15 owner/support relation.
b={'owner':'exact','proof':'exact','support':'exact_declared_member','content':'full_exact','state':'exact','scope':'exact','lineage':'exact','generation':'exact','authority':'verified','evidence':'native_binding','native_rewrite':False,'complete':True,'authorized_claim':False,'closed_world':'explicit','acceptance':'unchanged','role_assignment':'governed'}
def valid(x):return x==b
mut=[('role_assignment','native_type_alone'),('support','configuration_only'),('support','necessary_from_current_content'),('owner','wrong'),('proof','wrong'),('support','wrong'),('content','wrong'),('state','later'),('scope','foreign'),('lineage','foreign'),('generation','later'),('authority','missing'),('evidence','provenance_only'),('evidence','declaration_only'),('native_rewrite',True),('complete',False),('authorized_claim',True),('closed_world','assumed_from_21'),('acceptance','weakened')]
assert valid(b)
for k,v in mut:assert not valid({**b,k:v})
result={'SOURCE_COUNTS':counts,'NEGATIVE_CHECKS':len(mut),'STRUCTURAL_RELATIONSHIP_FIELD_CHECKS':'PASS','KNOWLEDGE_ID_AUTHORITY_SEPARATION':'PASS','DECISION_READY':False,'MUTATIONS':mut}
result['IDENTITY']=hashlib.sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest()
print(json.dumps(result,sort_keys=True))
