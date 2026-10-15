import json,pathlib,hashlib,copy
P=pathlib.Path('docs/plans/qualification');E=P/'E2_P05_D01_A15_NORMATIVE_INSTANCE_CLOSURE_PLANNING_47'
def read(p):return json.loads(p.read_text())
old=read(P/'E2_P05_D01_A15_APPLICABILITY_GAP_DECOMPOSITION_44/typed-gap-inventory.json');rows=read(E/'normalized-gap-inventory.json')
assert len(rows)==40 and len({r['GAP_ID'] for r in rows})==40
assert {r['GAP_ID'] for r in old if not r['GAP_ID'].startswith('D')} <= {r['GAP_ID'] for r in rows}
g=read(E/'cross-track-prerequisite-graph.json');historic=read(P/'E2_P05_D01_A15_APPLICABILITY_GAP_DECOMPOSITION_44/gap-dependency-graph.json')
original={(x['PREREQUISITE'],x['BLOCKED']) for x in historic['EDGES']};actual={(x['PREREQUISITE'],x['BLOCKED']) for x in g['EDGES']};assert original<=actual
# Independent Kahn traversal, distinct from producer incoming-set layering.
def acyclic(nodes,edges):
 indeg={i:0 for i in nodes};out={i:[] for i in nodes}
 for a,b in set(edges):indeg[b]+=1;out[a].append(b)
 ready=sorted(i for i in nodes if not indeg[i]);done=[]
 while ready:
  i=ready.pop(0);done.append(i)
  for v in sorted(out[i]):
   indeg[v]-=1
   if not indeg[v]:ready.append(v);ready.sort()
 return len(done)==len(nodes)
assert acyclic(g['NODES'],actual)
assert not acyclic(g['NODES'],actual|{('A02','V02')})
front=read(E/'minimal-independent-closure-frontier.json')['ITEMS'];assert len(front)==7 and len({x['MISSING_VALUE'] for x in front})==7
# N readiness intentionally independent of E oracle; exact compatibility is still necessary.
def nready(x):return all(x.get(i,False) for i in ['owner','binding','necessity','closure','partition','issuer','version','normative_tests','compatibility'])
def eready(x):return nready(x) and all(x.get(i,False) for i in ['normative_authority','descriptor','capture','oracle','acceptance','retry','execution_authority_subject'])
b={k:True for k in ['owner','binding','necessity','closure','partition','issuer','version','normative_tests','compatibility','normative_authority','descriptor','capture','oracle','acceptance','retry','execution_authority_subject']}
checks=[]
for k in b:
 x={**b,k:False};assert not (nready(x) if k in ['owner','binding','necessity','closure','partition','issuer','version','normative_tests','compatibility'] else eready(x));checks.append(k+' missing rejected')
x={**b,'oracle':False};assert nready(x) and not eready(x);checks.append('Complete N not blocked solely by execution oracle')
assert not eready({**b,'normative_authority':False});assert not eready({**b,'execution_authority_subject':False})
checks.extend(['Authority types remain distinct','Original missing-edge mutation rejected' if not original <= actual-{next(iter(original))} else 'FAIL','Inserted cycle detected','Duplicate frontier question rejected' if len({i['FRONTIER_ID'] for i in front+[front[0]]})!=len(front)+1 else 'FAIL'])
assert 'FAIL' not in checks
x={'normalized':[(r['GAP_ID'],r['TRACK'],r['PRIMARY_MECHANISM']) for r in rows],'edges':sorted(actual),'frontier':front,'gates':read(E/'readiness-gates.json'),'checks':checks}
print(json.dumps({'SEMANTIC_IDENTITY':hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'CHECKS':len(checks),'ACYCLIC':True,'COUNTS':{'N':sum(r['TRACK']=='N' for r in rows),'E':sum(r['TRACK']=='E' for r in rows)},'LIMITATION':'Independent structural/gate verification; not proof that unavailable domain facts or global minimum elicitation count are known'},sort_keys=True))
