"""Static documentary verifier. No prospective launcher/native witness imports or calls."""
import pathlib,json,hashlib,ast,copy,os
R=pathlib.Path.cwd();B=R/'docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1';O=B/'p86-descriptor-closure-128'
def read(p):return json.loads(p.read_text())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def digest(x):return hashlib.sha256(canon(x)).hexdigest()
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def acyclic(edges):
 nodes={n for e in edges for n in e};done=set()
 while nodes-done:
  ready={n for n in nodes-done if all(a in done for a,b in edges if b==n)}
  if not ready:return False
  done|=ready
 return True
idx=read(O/'input-authentication.json')
for n,h in idx['PINS'].items():assert raw(R/n)==h,n
for n,x in idx['LOCAL_STATIC_SOURCE_PINS'].items():assert raw(pathlib.Path(n))==x['RAW_SHA256'],n
for n,x in idx['EXISTING_NATIVE_PINS'].items():assert raw(pathlib.Path(n))==x['RAW_SHA256'],n
p127=read(B/'p86-minimal-host-procedure-127/prospective-parent-procedure.json');p124=read(B/'p86-isolation-capability-124/exact-candidate-profile.json')
assert digest(p127['CONTENT'])==p127['IDENTITY']['sha256']==idx['P127_IDENTITY']['sha256']
assert digest(p124['CONTENT'])==p124['IDENTITY']['sha256']==idx['P124_IDENTITY']['sha256']
assert p127['CONTENT']['ARGV'][-len(p124['CONTENT']['ARGV']):]==p124['CONTENT']['ARGV']
src=pathlib.Path('/usr/lib/python3.8/subprocess.py').read_text();tree=ast.parse(src)
# Reconstruct relevant Python control flow without importing subprocess or native implementation.
functions=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='_execute_child']
posix=[n for n in functions if '_posixsubprocess.fork_exec' in ast.get_source_segment(src,n)][0]
condition=[n for n in ast.walk(posix) if isinstance(n,ast.If) and '_USE_POSIX_SPAWN' in ast.get_source_segment(src,n.test)][0]
assert any(isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.Not) and isinstance(n.operand,ast.Name) and n.operand.id=='close_fds' for n in ast.walk(condition.test))
forkcalls=[n for n in ast.walk(posix) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='fork_exec'];assert len(forkcalls)==1
assert isinstance(forkcalls[0].args[2],ast.Name) and forkcalls[0].args[2].id=='close_fds'
api=read(O/'candidate-python-invocation.json');kw=api['KEYWORD_ARGUMENTS']
assert kw['close_fds'] is True and kw['pass_fds']==[] and kw['shell'] is False and kw['preexec_fn'] is None
assert api['QUALIFICATION_COMPLETE'] is False
policy=read(O/'descriptor-policy.json');assert policy['PASS_FDS']==[] and policy['PRE_ENTRY_CLOSURE_VERIFIED'] is False
m=read(O/'entry-execution-matrix.json');old=read(B/'p86-minimal-host-procedure-127/entry-execution-matrix.json');assert len(m['ROWS'])==36 and m['ROWS']==old['ROWS']
g=read(O/'dependency-graph.json');assert acyclic(g['EDGES'])
facts={'pins':True,'stdio_protected':False,'directory_passed':False,'socket_passed':False,'extra_intermediate':False,'unsafe_redirect':False,'pass_fds':[],'cloexec_assumed_verified':False,'protected_writable_mount':False,'future_census_entry':False,'observer_claimed_qualified':False,'aggregate_claimed_enforced':False,'auto_retry':0,'authority_issued':False,'profile':p124['IDENTITY'],'argv':p127['CONTENT']['ARGV'],'safe_upstream_verified':False,'native_closure_verified':False,'close_fds':True,'shell':False,'preexec_fn':None,'decision_ready':False,'scope':['STATIC_P128'],'graph':g['EDGES']}
def validate(x):
 if not x['pins'] or x['profile']!=p124['IDENTITY'] or x['argv']!=p127['CONTENT']['ARGV']:return False
 if any(x[k] for k in ['stdio_protected','directory_passed','socket_passed','extra_intermediate','unsafe_redirect','cloexec_assumed_verified','protected_writable_mount','future_census_entry','observer_claimed_qualified','aggregate_claimed_enforced','authority_issued','safe_upstream_verified','native_closure_verified','decision_ready']):return False
 if x['pass_fds']!=[] or x['auto_retry']!=0 or x['close_fds'] is not True or x['shell'] is not False or x['preexec_fn'] is not None:return False
 return x['scope']==['STATIC_P128'] and acyclic(x['graph'])
assert validate(facts)
designs=[('wrong_executable_pin','pins',False),('FD0_protected_regular','stdio_protected',True),('FD1_protected_file','stdio_protected',True),('FD2_protected_file','stdio_protected',True),('inherited_directory','directory_passed',True),('inherited_socket','socket_passed',True),('intermediate_exec_before_closure','extra_intermediate',True),('unsafe_shell_redirection','unsafe_redirect',True),('unknown_pass_fds','pass_fds',[9]),('unverified_CLOEXEC','cloexec_assumed_verified',True),('writable_protected_mount','protected_writable_mount',True),('future_census_is_entry_proof','future_census_entry',True),('unqualified_observer','observer_claimed_qualified',True),('invented_aggregate_enforcement','aggregate_claimed_enforced',True),('automatic_retry','auto_retry',1),('authority_from_preparation','authority_issued',True),('new_python_startup_safe_assumed','safe_upstream_verified',True),('native_semantics_from_callsite','native_closure_verified',True),('close_fds_disabled','close_fds',False),('shell_before_prlimit','shell',True),('preexec_callback','preexec_fn','closure'),('incomplete_subject_ready','decision_ready',True),('P86_permission_added','scope',['STATIC_P128','P86']),('H77_permission_added','scope',['STATIC_P128','H77-02']),('A15_permission_added','scope',['STATIC_P128','A15'])]
out=[]
for name,k,v in designs:
 x=copy.deepcopy(facts);x[k]=v;assert not validate(x),name;out.append({'DESIGN':name,'MUTATION_SHA256':digest(x),'RESULT':'REJECTED'})
x=copy.deepcopy(facts);x['graph'].append(['CHILD_CENSUS_OR_MOUNT_RESULT','PRE_ENTRY_FD_ROOT']);assert not validate(x);out.append({'DESIGN':'own_future_census_cycle','MUTATION_SHA256':digest(x),'RESULT':'REJECTED'})
x=copy.deepcopy(facts);x['argv'].append('--extra');assert not validate(x);out.append({'DESIGN':'sealed_argv_changed','MUTATION_SHA256':digest(x),'RESULT':'REJECTED'})
before=read(O/'preservation-before.json');assert all((R/n).is_file() and raw(R/n)==h for n,h in before.items())
extra=[str(p.relative_to(R)) for root in ['docs','adapter','rust'] for p in (R/root).rglob('*') if p.is_file() and not p.is_symlink() and str(p.relative_to(R)) not in before and O not in p.parents];assert not extra,extra
semantic={'INPUT_PINS_SHA256':digest(idx['PINS']),'LOCAL_SOURCE_PINS':idx['LOCAL_STATIC_SOURCE_PINS'],'P127_IDENTITY':p127['IDENTITY'],'P124_IDENTITY':p124['IDENTITY'],'SOURCE_AST_FACTS':{'CLOSE_FDS_EXCLUDES_POSIX_SPAWN':True,'FORK_EXEC_RECEIVES_CLOSE_FDS':True,'NATIVE_IMPLEMENTATION_NOT_QUALIFIED':True},'API_SHA256':digest(api),'FD_POLICY_SHA256':digest(policy),'MATRIX_SHA256':digest(m),'GRAPH_SHA256':digest(g),'GRAPH_ACYCLIC':True,'PRE_ENTRY_VERIFIED':False,'DECISION_READY':False,'DECISION_OPTIONS':[],'PRIOR_FILES':len(before),'PRESERVATION':'PASS','NEGATIVES':out}
print(json.dumps({'SEED':os.environ.get('PYTHONHASHSEED'),'SEMANTIC_SHA256':digest(semantic),'SEMANTIC':semantic},sort_keys=True))
