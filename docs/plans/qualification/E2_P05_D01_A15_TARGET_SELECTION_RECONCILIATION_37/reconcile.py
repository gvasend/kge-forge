"""Membership/semantic reconciliation only; no invalidation/capture/oracle operation."""
import json,hashlib,sys
from pathlib import Path
R=Path('/home/gvasend/app/kge-forge');E=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification';P=Q/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36'
def load(p):return json.loads(Path(p).read_bytes())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def pin(p):return {'path':str(p.relative_to(R)),'raw_sha256':sha(p.read_bytes())}
def emit(n,x):(E/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def walk(x,p=''):
 yield p,x
 if isinstance(x,dict):
  for k,v in x.items():yield from walk(v,p+'/'+k.replace('~','~0').replace('/','~1'))
 elif isinstance(x,list):
  for i,v in enumerate(x):yield from walk(v,p+'/'+str(i))
def reconstruct(graph):
 sources={canon(x['NATIVE_IDENTITY']):x for x in graph['NODES'] if x['TYPE']=='SOURCE_CONTENT'};records=[n for n in graph['NODES'] if n['TYPE']!='SOURCE_CONTENT'];a=set();b=set();c=set()
 types={'KnowledgeRecord','TypedProof','TypedProofContract','GraphEntity'}
 for n in records:
  direct=set();refs=set()
  for ptr,x in walk(n['NATIVE_RECORD']):
   if isinstance(x,dict):
    if x.get('$type')=='Provenance':direct.add(canon(x['identity']))
    if x.get('$type')=='ArtifactPin':refs.add(canon(x['identity']))
    if x.get('$type')=='ArtifactIdentity' and canon(x) in sources:refs.add(canon(x))
   if isinstance(x,str) and ptr.endswith('/grant_json'):
    for field,value in json.loads(x).items():
     if isinstance(value,dict) and value.get('kind')=='CONTENT_IDENTITY':
      value={'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':value['namespace'],'sha256':value['sha256']}
      if canon(value) in sources:refs.add(canon(value))
  a.update(direct);b.update(refs)
  if n['TYPE'] in types:c.update(direct|refs)
 return {'P45':a&set(sources),'P49':b&set(sources),'P14':c&set(sources)}
def recover():
 graph=load(P/'accepted-support-graph.json');g=dict(graph);identity=g.pop('GRAPH_IDENTITY');assert identity=='qualification-A15-support-graph-v1:'+sha(canon(g));assert len(graph['NODES'])==131 and len(graph['EDGES'])==474
 sources={canon(x['NATIVE_IDENTITY']):x for x in graph['NODES'] if x['TYPE']=='SOURCE_CONTENT'};assert len(sources)==54
 sets=reconstruct(graph);assert [len(sets[x]) for x in ['P45','P49','P14']]==[45,49,14]
 prior=load(P/'target-contract.json')['CANDIDATE_PROJECTIONS'];assert all(sets[name]=={canon(x) for x in prior[i]['CONTENT_IDENTITIES']} for i,name in enumerate(['P45','P49','P14']))
 nodes={n['NODE_ID']:n for n in graph['NODES']};source_by_node={n['NODE_ID']:key for key,n in sources.items()}
 edge_sets={'P45':set(),'P49':set(),'P14':set()}
 for edge in graph['EDGES']:
  if edge['FROM'] not in source_by_node:continue
  key=source_by_node[edge['FROM']];consumer=nodes[edge['TO']]
  if edge['ROLE']=='PROVENANCE_SUPPORT':edge_sets['P45'].add(key)
  if edge['ROLE'] in ['NATIVE_TYPED_REFERENCE','INSTALLATION_GRANT_SUPPORT']:edge_sets['P49'].add(key)
  if consumer['TYPE'] in {'KnowledgeRecord','TypedProof','TypedProofContract','GraphEntity'} and edge['ROLE'] in ['PROVENANCE_SUPPORT','NATIVE_TYPED_REFERENCE','INSTALLATION_GRANT_SUPPORT']:edge_sets['P14'].add(key)
 assert edge_sets==sets
 def memberships(keys):
  output=[]
  for key in sorted(keys):
   node=sources[key];associations=[e for e in graph['EDGES'] if e['FROM']==node['NODE_ID'] or e['TO']==node['NODE_ID']]
   output.append({'SOURCE_NODE_ID':node['NODE_ID'],'SOURCE_IDENTITY':node['NATIVE_IDENTITY'],'PIN':node['SOURCE_PIN'],'SCOPE':node['SCOPE'],'LINEAGE':node['LINEAGE'],'GENERATION':node['GENERATION'],'PROJECTIONS':[name for name in ['P45','P49','P14'] if key in sets[name]],'ASSOCIATIONS':[dict(e,CONSUMER_TYPE=nodes[e['TO']]['TYPE']) for e in associations],'SUPPORT_ROLES':sorted({e['ROLE'] for e in associations}),'PROVENANCE':[e['PROVENANCE'] for e in associations if e['ROLE']=='PROVENANCE_SUPPORT']})
  return output
 intersections={};differences={}
 for a,b in [('P45','P49'),('P45','P14'),('P49','P14')]:
  intersections[a+'&'+b]={'COUNT':len(sets[a]&sets[b]),'MEMBERS':memberships(sets[a]&sets[b])}
  for x,y in [(a,b),(b,a)]:differences[x+'-'+y]={'COUNT':len(sets[x]-sets[y]),'MEMBERS':memberships(sets[x]-sets[y])}
 assert sets['P14']<sets['P45']<sets['P49']
 extra=memberships(sets['P49']-sets['P45']);assert len(extra)==4 and all(m['SUPPORT_ROLES']==['NATIVE_TYPED_REFERENCE'] and all('/source_additions/' in a['FIELD_PATH'] for a in m['ASSOCIATIONS']) for m in extra)
 terminology={'accepted_support':{'FROZEN_TERM':'Restored accepted knowledge/proof/authority state in isolated copy','DEFINITION_LIMIT':'Native records encode accepted/currentness/status/proof roles; frozen A15 does not enumerate required consumer/root set or define a source-selection predicate for the installed P04 state'},'dependency':{'NATIVE_MEANING':'Specific typed evidence/predicate/proof/authority/installation relations consumed by invalidation and reevaluation','DISTINCTION':'An ArtifactPin in source_additions is availability/declaration membership, not by itself a mandatory influence edge'},'source_target':{'NATIVE_MEANING':'Exact source content identity consumed in SourceInvalidation.changed, tied to qualified pin/provenance/dependency role','DISTINCTION':'The 54-source eligible index and three observational predicates do not prove actual target membership'},'disjointness':{'FROZEN_TERM':'SourceInvalidation event for each disjoint required source','RECOVERED_COMPONENT':'Local P03 suite tests singleton content identities from its direct-Provenance predicate in independent variants','NOT_RECOVERED':'No original formal pairwise/group/protected-set predicate or mapping of required consumer roots to target groups for current A15'},'invalidation_target':{'NATIVE_MEANING':'changed content identities drive semantic withdrawal/staleness; expected_snapshot binds exact optimistic pre-state'},'content_identity_target':{'NATIVE_MEANING':'CONTENT_IDENTITY required; authority, event and path identity cannot substitute; equal full kind/namespace/hash identities share target membership even if paths differ'}}
 classification={'CLASS':'DIFFERENT_RECORDED_SOURCE_ROLE_AND_REFERENCE_VIEWS','NESTING_PROVEN':'P14 strict subset P45 strict subset P49','P45':'Direct current native Provenance occurrence, restricted to the bundle source index; matches local P03 driver predicate','P49':'Current record occurrence of raw source identities/pins plus grant support; includes source_additions-only declarations; broad recorded-reference superset, not a proven transitive mandatory dependency closure','P14':'Record-type slice (knowledge, typed proof/contract, GraphEntity) of provenance/reference membership; not a proven required accepted-support root closure and not restricted automatically to authority entities','COMPETING_TARGET_RULES':'They become competing candidates only if promoted without authority; as recovered they measure different static properties','SELECTION_PIPELINE_ESTABLISHED':False,'WHY_NOT_PIPELINE':'Counts and subset relations do not establish normative filtering order or final required-support predicate; frozen contract supplies no stage mapping','HISTORICAL_VS_PROSPECTIVE_MEMBERSHIP':False,'WHY':'All projections use the same frozen A15 graph/state/generation; extra sources are installed definition declarations, not another timeline','PROSPECTIVE_RUNNER_PROJECTION_DEFECT_PROVEN':False,'WHY':'V3 A15 target projection is unbound, not an implemented 45/49/14 heuristic; no code correction is justified solely by these counts','FOUR_DIFFERING_DECLARATIONS':extra}
 predicates={name:{'INPUT_TYPE':'Frozen native source index + current typed native records/graph associations','OUTPUT_TYPE':'Unordered set of exact ArtifactIdentity CONTENT_IDENTITY members','PREDICATE':classification[name],'COUNT':len(sets[name]),'MEMBERSHIP_IDENTITY':'qualification-A15-'+name+'-membership-v1:'+sha(canon(sorted([json.loads(k) for k in sets[name]],key=canon))),'ACCEPTANCE':'Exact identity membership reconstructed independently from both native records and directed graph associations','TARGET_QUALIFIED':False} for name in ['P45','P49','P14']}
 return {'GRAPH_SOURCE':pin(P/'accepted-support-graph.json'),'GRAPH_IDENTITY':identity,'GRAPH_NODES':131,'GRAPH_ASSOCIATIONS':474,'SOURCE_PINS':54,'CONTEXT':graph['CONTEXT'],'PRESTATE':graph['PRESTATE_ID'],'TERMINOLOGY':terminology,'MEMBERSHIPS':{name:memberships(sets[name]) for name in ['P45','P49','P14']},'INTERSECTIONS':intersections,'DIFFERENCES':differences,'OUTSIDE_P49':memberships(set(sources)-sets['P49']),'SEMANTIC_CLASSIFICATION':classification,'RECOVERED_PREDICATES':predicates,'DISJOINTNESS':{'PAIRWISE_CONTENT_IDENTITIES_DISTINCT_IN_THIS_GRAPH':len(sources)==54,'PATH_DISTINCTNESS_IS_PROOF':False,'SINGLETON_ISOLATED_VARIANT_COMPONENT_RECIPE':True,'DEPENDENCY_BRANCH_DISJOINTNESS_PROVEN':False,'GROUP_OR_PROTECTED_SET_RULE_RECOVERED':False,'EXACT_FROZEN_DISJOINTNESS_PREDICATE':None},'TARGET_SELECTION_UNIQUE':False,'SELECTED_TARGETS':None,'MISSING_DISCRIMINATOR':'An authoritative required-support consumer/root and source-role predicate for the exact P04 post-root-proof A15 state: distinguish source declaration availability from operative provenance and native mandatory dependency influence; specify whether singleton provenance sources or another support partition exhaust every required variant. No protected-set/group/pairwise branch criterion is supplied.','TARGET_SELECTION_PIPELINE':None}
if __name__=='__main__':
 d=recover()
 if '--identity' in sys.argv:print(sha(canon(d)));raise SystemExit
 emit('membership-semantic-reconciliation.json',d);emit('membership-comparison.json',{'INTERSECTIONS':d['INTERSECTIONS'],'DIFFERENCES':d['DIFFERENCES'],'MEMBERSHIPS':d['MEMBERSHIPS'],'OUTSIDE_P49':d['OUTSIDE_P49']});emit('recovered-predicates.json',d['RECOVERED_PREDICATES']);print('Membership verified: P14 < P45 < P49; extra 4 are source-addition declarations; no target rule selected')
