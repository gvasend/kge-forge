"""Read-only documentary reconstruction; never imports or invokes target native code."""
import pathlib,json,hashlib,copy,os
R=pathlib.Path.cwd();B=R/'docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1';O=B/'p86-minimal-host-procedure-127'
def read(p):return json.loads(p.read_text())
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def acyclic(edges):
 nodes={n for e in edges for n in e};done=set()
 while nodes-done:
  ready={n for n in nodes-done if all(a in done for a,b in edges if b==n)}
  if not ready:return False
  done|=ready
 return True
idx=read(O/'input-authentication.json')
for p,h in idx['PINS'].items():assert raw(R/p)==h,p
for p,x in idx['NATIVE_PINS'].items():assert raw(pathlib.Path(p))==x['RAW_SHA256'],p
for p,x in idx['DOCUMENTATION_PINS'].items():assert raw(pathlib.Path(p))==x['RAW_SHA256'],p
profile=read(B/'p86-isolation-capability-124/exact-candidate-profile.json')
assert digest(profile['CONTENT'])==profile['IDENTITY']['sha256']=='2f36be1b7123770d889be302a090cfef16149b270140a9ea901ba992095f46ca'
wrap=read(O/'prospective-parent-procedure.json');c=wrap['CONTENT'];assert digest(c)==wrap['IDENTITY']['sha256']
expected_prefix=['/usr/bin/prlimit','--cpu=60:60','--as=268435456:268435456','--nofile=64:64','--','/bin/bash','--noprofile','--norc','-c','umask 077\n"$@"\nresult=$?\nprintf "P127_PARENT_EXIT=%s\\n" "$result" >&2\nexit "$result"\n','P127_FIXED_PARENT','/usr/bin/timeout','--signal=KILL','200s']
matrix=read(O/'entry-execution-matrix.json');original=read(B/'p86-construction-isolation-promotion-122/36-requirement-trace-matrix.json')
assert len(matrix['ROWS'])==36
assert [(x['REQUIREMENT_ID'],x['PHASE'],x['ORIGINAL_CLASS']) for x in matrix['ROWS']]==[(x['REQUIREMENT_ID'],x['PHASE'],x['ORIGINAL_CLASS']) for x in original['ROWS']]
evidence=read(O/'bounded-evidence-model.json');retained=read(B/'p86-isolation-capability-124/evidence-allocation.json')
assert sum(x['MAX_RECORD_BYTES']*x['MAX_OCCURRENCES'] for x in retained['PRODUCERS'].values())==5542
assert 5542+8658872+2336==8666750
assert evidence['NEW_PARENT_TAG_MAX_BYTES']==len(b'P127_PARENT_EXIT=255\n')
assert evidence['WITNESS_AND_OTHER_STDIO_ALLOWANCE_WITH_TAG']+evidence['NEW_PARENT_TAG_MAX_BYTES']==8658872
graph=read(O/'dependency-graph.json');assert acyclic(graph['EDGES'])
# Independent admission predicate: deficient proposal must never become a launch-ready subject.
facts={'pins':True,'profile':True,'witness':True,'mounts':True,'protected_writable':False,'fd_closed_verified':False,'permission_verified':False,'all_limits':False,'scratch_bounded':False,'tree_termination_verified':False,'observer_qualified':False,'output_bounded_verified':False,'durability_verified':False,'attempts':1,'retry':0,'grant_issued':False,'decision_ready':False,'options':[],'scope':['PASSIVE_P124'],'measure':'logical_distinct_submitted_transferred_durable','history':True,'future_result_entry':False,'graph':graph['EDGES'],'argv':c['ARGV'],'binary_pins':c['BINARY_PINS'],'environment':c['ENVIRONMENT']}
def validate(x):
 if x['argv']!=expected_prefix+profile['CONTENT']['ARGV']:return False
 if x['binary_pins']!=idx['NATIVE_PINS']:return False
 if x['environment']!={'PATH':'/bin','LC_ALL':'C','LANG':'C','HOME':'/nonexistent'}:return False
 if not all(x[k] for k in ['pins','profile','witness','mounts','history']):return False
 if x['protected_writable'] or x['attempts']!=1 or x['retry']!=0 or x['grant_issued'] or x['scope']!=['PASSIVE_P124']:return False
 if x['measure']!='logical_distinct_submitted_transferred_durable' or x['future_result_entry'] or not acyclic(x['graph']):return False
 # A static proposal cannot assert any of these without independent pre-entry receipts.
 for k in ['fd_closed_verified','permission_verified','all_limits','scratch_bounded','tree_termination_verified','observer_qualified','output_bounded_verified','durability_verified']:
  if x[k] is not False:return False
 return x['decision_ready'] is False and x['options']==[]
assert validate(facts)
mutations=[('wrong_binary_pin',lambda x:x['binary_pins']['/usr/bin/bwrap'].update(RAW_SHA256='0'*64)),('wrong_profile',lambda x:x.update(profile=False)),('changed_witness',lambda x:x['argv'].append('--extra')),('expanded_mount',lambda x:x['argv'].insert(-5,'--bind')),('writable_protected_path',lambda x:x.update(protected_writable=True)),('descriptor_leak_claimed_closed',lambda x:x.update(fd_closed_verified=True)),('unsupported_permission',lambda x:x.update(permission_verified=True)),('absent_resource_limit_accepted',lambda x:x.update(all_limits=True)),('parent_kill_called_whole_tree',lambda x:x.update(tree_termination_verified=True)),('unqualified_observer_accepted',lambda x:x.update(observer_qualified=True)),('unbounded_output_accepted',lambda x:x.update(output_bounded_verified=True)),('write_return_called_durable',lambda x:x.update(durability_verified=True)),('implicit_retry',lambda x:x.update(retry=1)),('duplicate_attempt',lambda x:x.update(attempts=2)),('circular_evidence',lambda x:x['graph'].append(['MOUNT_WITNESS','QUALIFIED_OUTER_CONTEXT'])),('premature_authority',lambda x:x.update(grant_issued=True)),('P86_scope_added',lambda x:x['scope'].append('P86')),('H77_scope_added',lambda x:x['scope'].append('H77-02')),('A15_scope_added',lambda x:x['scope'].append('A15')),('scratch_unbounded_accepted',lambda x:x.update(scratch_bounded=True)),('future_output_required_at_entry',lambda x:x.update(future_result_entry=True)),('history_modified',lambda x:x.update(history=False)),('submitted_is_publication',lambda x:x.update(measure='submitted')),('incomplete_proposal_decision_ready',lambda x:x.update(decision_ready=True)),('option_manufactured',lambda x:x.update(options=['AUTHORIZE'])),('startup_environment_leak',lambda x:x['environment'].update(BASH_ENV='/unsafe'))]
out=[]
for name,mutation in mutations:
 x=copy.deepcopy(facts);mutation(x);accepted=validate(x);assert not accepted,name
 out.append({'DESIGN':name,'MUTATION_SHA256':digest(x),'RESULT':'REJECTED'})
before=read(O/'preservation-before.json');changed=[p for p,h in before.items() if not (R/p).is_file() or raw(R/p)!=h];assert not changed,changed
extra=[str(p.relative_to(R)) for root in ['docs','adapter','rust'] for p in (R/root).rglob('*') if p.is_file() and not p.is_symlink() and str(p.relative_to(R)) not in before and O not in p.parents];assert not extra,extra
semantic={'PROFILE_IDENTITY':profile['IDENTITY'],'PROCEDURE_IDENTITY':wrap['IDENTITY'],'INPUT_PINS':digest(idx['PINS']),'PHASE_ROWS':digest(matrix),'GRAPH_ACYCLIC':True,'PRIOR_PRESERVATION':'PASS','PRIOR_FILES':len(before),'DECISION_READY':False,'OPTIONS':[],'NEGATIVES':out,'EVIDENCE_MODEL':digest(evidence),'NO_NATIVE_PROCEDURE_EXECUTION':True}
print(json.dumps({'SEED':os.environ.get('PYTHONHASHSEED'),'SEMANTIC_SHA256':digest(semantic),'SEMANTIC':semantic},sort_keys=True))
