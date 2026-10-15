"""Static byte/JSON/AST verification only. Never executes bwrap, findmnt or target modules."""
import pathlib,json,hashlib,struct,gzip,sys,subprocess,os,copy,ast
O=pathlib.Path(__file__).resolve().parent;B=pathlib.Path('docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1');P=B/'p86-existing-isolation-construction-123'
def load(p):return json.loads(p.read_text())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def need(x,r):
 if not x:raise ValueError(r)
def acyclic(edges):
 adj={};on=set();done=set()
 for a,b in edges:adj.setdefault(a,[]).append(b)
 def visit(n):
  need(n not in on,'cycle')
  if n in done:return
  on.add(n)
  for v in adj.get(n,[]):visit(v)
  on.remove(n);done.add(n)
 for n in adj:visit(n)
 return True
manifest=load(O/'authenticated-input-index.json')
for p,h in manifest['PINS'].items():need(sha(pathlib.Path(p).read_bytes())==h,'input pin '+p)
for p,h in load(O/'preservation-before.json')['FILES'].items():need(sha(pathlib.Path(p).read_bytes())==h,'history '+p)
paths=manifest['EXACT_CONSTRUCTION_PATHS'];need(all(not pathlib.Path(p).exists() for p in paths),'no source construction')
wrapper=load(O/'exact-candidate-profile.json');profile=wrapper['CONTENT'];need(wrapper['IDENTITY']['sha256']==sha(canon(profile)),'profile canonical identity');need(profile['ARGV_SHA256']==sha(canon(profile['ARGV'])),'argv digest')
need(sha(pathlib.Path(profile['BWRAP_PIN']['PATH']).read_bytes())==profile['BWRAP_PIN']['RAW_SHA256']=='af662c55cd85178a58da083220a9348c4a7d3c24333fd0bc7badb18c93392987','bwrap pin')
# Independently parse dynamic dependency bytes using program-header offsets rather than running a loader.
inputs=load(O/'mount-source-identity-manifest.json');dest={x['DESTINATION']:x['SOURCE'] for x in inputs['MOUNTS']}
for source,f in inputs['FILES'].items():
 p=pathlib.Path(source);b=p.read_bytes();need(sha(b)==f['RAW_SHA256'] and len(b)==f['RAW_BYTES'],'ELF input pin');need(b[:6]==b'\x7fELF\x02\x01','ELF64LE')
 offset=struct.unpack_from('<Q',b,32)[0];size=struct.unpack_from('<H',b,54)[0];count=struct.unpack_from('<H',b,56)[0];headers=[]
 for i in range(count):headers.append(struct.unpack_from('<IIQQQQQQ',b,offset+size*i))
 interps=[b[h[2]:h[2]+h[5]].rstrip(b'\0').decode() for h in headers if h[0]==3];tags=[]
 for h in headers:
  if h[0]==2:
   for off in range(h[2],h[2]+h[5],16):
    key,value=struct.unpack_from('<qQ',b,off)
    if key==0:break
    tags.append((key,value))
 needed=[];sv=next((v for k,v in tags if k==5),None)
 if sv is not None:
  segment=next(h for h in headers if h[0]==1 and h[3]<=sv<h[3]+h[5]);strings=segment[2]+sv-segment[3]
  for k,v in tags:
   if k==1:needed.append(b[strings+v:b.index(b'\0',strings+v)].decode())
 need(interps==f['ELF_INTERPRETERS'] and needed==f['DT_NEEDED'],'ELF declared dependencies')
 for x in interps:need(x in dest and dest[x]==str(pathlib.Path(x).resolve()),'interpreter mount closure')
 for x in needed:need('/lib/x86_64-linux-gnu/'+x in dest,'DT_NEEDED mount closure')
need(len(inputs['FILES'])==11 and len(inputs['MOUNTS'])==12,'thin exact source/alias set');need(inputs['MOUNTS']==profile['READ_ONLY_FILE_MOUNTS'] and all(x['READ_ONLY'] for x in inputs['MOUNTS']),'readonly file bindings')
# Rebuild exact argv from the independently checked file manifest; no unqualified broad binds.
expected=['/usr/bin/bwrap','--unshare-user','--uid','1000','--gid','1000','--unshare-pid','--unshare-net','--unshare-ipc','--unshare-uts','--cap-drop','ALL','--die-with-parent']
for d in ['/bin','/lib','/lib/x86_64-linux-gnu','/lib64','/dev','/proc','/work']:expected+=['--dir',d]
for x in inputs['MOUNTS']:expected+=['--ro-bind',x['SOURCE'],x['DESTINATION']]
expected+=['--proc','/proc','--remount-ro','/proc','--tmpfs','/work','--remount-ro','/','--chdir','/work','--setenv','PATH','/bin','--setenv','LC_ALL','C','--setenv','LANG','C','--','/bin/findmnt','--json','--output','TARGET,SOURCE,FSTYPE,OPTIONS']
need(profile['ARGV']==expected,'single exact candidate argv');man=gzip.decompress(pathlib.Path('/usr/share/man/man1/bwrap.1.gz').read_bytes()).decode().replace('\\-','-')
delimiter=expected.index('--')
for token in set(t for t in expected[:delimiter] if t.startswith('--')):need(token in man,'installed documented bwrap flag '+token)
findmntman=gzip.decompress(pathlib.Path('/usr/share/man/man8/findmnt.8.gz').read_bytes()).decode().replace('\\-','-')
for token in set(t for t in expected[delimiter+1:] if t.startswith('--')):need(token in findmntman,'installed documented witness flag '+token)
w=load(O/'passive-witness-specification.json');old=load(P/'prospective-minimum-capability-check.json');need(w['EXACT_ARGV']==old['PAYLOAD_ARGUMENT_VECTOR'] and w['ARGV_SHA256']==sha(canon(w['EXACT_ARGV']))==old['ARGUMENT_VECTOR_SHA256'],'unchanged witness');need(w['PAYLOAD_EXECUTABLE_PIN']['SHA256']==sha(pathlib.Path(w['PAYLOAD_EXECUTABLE_PIN']['PATH']).read_bytes()),'findmnt pin')
policy=load(O/'resource-observer-contract.json');need(policy['RETAINED_PROPOSED_NUMERIC_LIMITS']==old['PROPOSED_SAFETY_LIMITS_FROM_P120_NOT_AUTHORITY'] and not policy['RESOURCE_SAFETY_COMPLETE'] and not policy['INDEPENDENT_OBSERVER_COMPLETE'],'known proposals/unverified safety')
evidence=load(O/'evidence-allocation.json');total=0
for typ,r in evidence['PRODUCERS'].items():
 x=r['MAXIMAL_INSTANCE'];need(x['type']==typ and x['status']=='INCOMPLETE' and x['operation_ordinal']==x['raw_bytes']==18446744073709551615,'strict metadata maxima')
 need(r['MAX_OCCURRENCES']==1 and len(canon(x))==r['MAX_RECORD_BYTES'],'record size/count');total+=r['MAX_RECORD_BYTES']
need(total==5542==evidence['ORDINARY_FIXED_RECORD_MAX_BYTES'],'normal record sum');need(evidence['COMBINED_STDOUT_STDERR_CAPTURE_MAX_BYTES']==8664414-total==8658872,'shared capture allowance');need(total+8658872+2336==evidence['TOTAL_PROPOSED_ALLOCATION_BYTES']==8666750 and not evidence['EVIDENCE_BUDGET_COMPLETE'],'allocation versus missing producers')
critical=len(canon(evidence['P124_CRITICAL_SCHEMA_MAXIMAL_INSTANCE']));need(critical==581 and critical*4==2324 and evidence['RESERVE_HEADROOM_BYTES']==12,'check-specific critical schema/reserve');need(evidence['CRITICAL_RESERVE_BYTES']==2336 and evidence['RETAINED_RESERVED_SLOT_BYTES']==584,'retained reserved slots')
orig=load(B/'p86-construction-isolation-promotion-122/36-requirement-trace-matrix.json')['ROWS'];phase=load(O/'36-requirement-phase-matrix.json');need(phase['COUNT']==len(phase['RETAINED_REQUIREMENTS'])==36 and phase['RETAINED_REQUIREMENTS']==orig and phase['EARLIEST_PHASE_REASSIGNMENTS']==[],'36 phases')
allowed={'STATICALLY_SPECIFIED','INDEPENDENTLY_VERIFIED_PRE_ENTRY','ENTRY_PREDICATE_PENDING','EXECUTION_OBSERVATION_REQUIRED','POST_EXECUTION_QUALIFICATION_REQUIRED','UNDETERMINED'};need(all(r['CLASS'] in allowed for r in load(O/'capability-entry-execution-classification.json')['ROWS']),'capability phase classes')
slot=load(O/'publication-slot-preservation.json');need(slot==load(P/'publication-slot-reconciliation.json') and slot['SELECTED'] is None,'slots unchanged/unselected')
claim=load(O/'one-attempt-contract.json');key=claim['CANONICAL_KEY_FIELDS'];need(key['attempt_number']==1 and key['candidate_profile_identity']==wrapper['IDENTITY'] and key['passive_witness_command_identity']['sha256']==w['ARGV_SHA256'],'separate capability key');need(not claim['FUTURE_GRANT_INVENTED'] and not claim['CONTRACT_COMPLETE'] and '/var/tmp/' in claim['STORE_ROOT_RULE'],'no real grant/active store')
protected=load(O/'protected-path-escape-assessment.json');need(not protected['BOUNDARY_COMPLETE'] and not protected['LINK_DESCRIPTOR_ESCAPE_CLOSURE'],'escape gaps not qualified')
for r in protected['PROTECTED_IDENTITIES']:
 if 'RAW_SHA256' in r:need(sha(pathlib.Path(r['HOST_PATH']).read_bytes())==r['RAW_SHA256'],'protected raw identity')
need(all(r['INSIDE_NAMESPACE']=='ABSENT' for r in protected['PROTECTED_IDENTITIES']),'protected paths absent policy')
for p in ['adapter/qualification_bootstrap/systemd_pids_once.py','adapter/tests/test_systemd_pids_bootstrap.py']:ast.parse(pathlib.Path(p).read_text())
cp=subprocess.run([sys.executable,str(B/'p86-publication-amendment-issuance-115/verify_independent.py'),'EFFECTIVE'],capture_output=True,text=True);need(cp.returncode==0,'fresh charter/104/115/A15 lifecycle');json.loads(cp.stdout)
ready=load(O/'authority-readiness-assessment.json');need(ready['DECISION_OPTIONS']==[] and not ready['CAPABILITY_CHECK_DECISION_READY'] and not ready['CAPABILITY_CHECK_ENTRY_READY'],'no ready incomplete subject');edges=load(O/'dependency-graph.json')['EDGES'];acyclic(edges)
model={'profile_digest':wrapper['IDENTITY']['sha256'],'argv':expected,'pins':{p:f['RAW_SHA256'] for p,f in inputs['FILES'].items()},'mounts':inputs['MOUNTS'],'protected_rw':False,'link_escape':False,'fd_escape':False,'mutation_api':False,'mount_propagation_escape':False,'namespace_types':profile['NAMESPACE_SETTINGS'],'limit_values':policy['RETAINED_PROPOSED_NUMERIC_LIMITS'],'qualified_safety':False,'qualified_observer':False,'occupancy_limit':'UNDETERMINED','evidence_complete':False,'capture_bytes':8658872,'attempt_number':1,'duplicate_admitted':False,'unknown_exit_result':'INCOMPLETE','automatic_retries':0,'construction_enabled':False,'probe_enabled':False,'source_scope':paths,'authority_issued':False,'own_future_output_before_authority':False,'submitted_equals_logical':False,'transfer_equals_durable':False,'pair_slots_selected':None,'edges':edges}
def valid(m):
 need(m['profile_digest']==wrapper['IDENTITY']['sha256'] and m['argv']==expected,'forged/expanded profile identity')
 need(m['pins']==model['pins'] and m['mounts']==inputs['MOUNTS'],'input pin/mount identity')
 need(not any(m[k] for k in ['protected_rw','link_escape','fd_escape','mutation_api','mount_propagation_escape']),'credible protected escape')
 need(m['namespace_types']==profile['NAMESPACE_SETTINGS'],'wrong namespace')
 need(m['limit_values']==policy['RETAINED_PROPOSED_NUMERIC_LIMITS'],'missing/changed finite limit')
 need(not m['qualified_safety'] and not m['qualified_observer'] and m['occupancy_limit']=='UNDETERMINED' and not m['evidence_complete'],'unverified safety/budget not complete')
 need(m['capture_bytes']==8658872,'unbounded/expanded output')
 need(m['attempt_number']==1 and not m['duplicate_admitted'] and m['automatic_retries']==0,'one separate attempt/no retry')
 need(m['unknown_exit_result']=='INCOMPLETE','unknown exit not success')
 need(not m['construction_enabled'] and not m['probe_enabled'] and m['source_scope']==paths and not m['authority_issued'],'no authority expansion')
 need(not m['own_future_output_before_authority'] and not m['submitted_equals_logical'] and not m['transfer_equals_durable'] and m['pair_slots_selected'] is None,'scope/accounting separate')
 acyclic(m['edges'])
valid(model);neg=[]
def reject(name,mut):
 m=copy.deepcopy(model);mut(m)
 try:valid(m)
 except ValueError as e:neg.append({'DESIGN':name,'RESULT':'REJECTED','CAUSE':str(e),'MUTATION_SHA256':sha(canon(m))});return
 raise AssertionError('negative admitted:'+name)
def change(k,v):return lambda m:m.__setitem__(k,v)
reject('forged profile pin',change('profile_digest','0'*64))
reject('forged ELF source pin',lambda m:m['pins'].__setitem__('/bin/findmnt','0'*64))
reject('writable readonly source mount',lambda m:m['mounts'][0].__setitem__('READ_ONLY',False))
reject('missing readonly fence',lambda m:m['argv'].remove('--remount-ro'))
for name,key in [('writable protected path','protected_rw'),('symlink hardlink escape','link_escape'),('inherited writable descriptor','fd_escape'),('writable API/socket','mutation_api'),('mount propagation escape','mount_propagation_escape'),('unqualified observer accepted','qualified_observer'),('unverified resources qualified','qualified_safety'),('incomplete evidence complete','evidence_complete'),('duplicate attempt','duplicate_admitted'),('premature construction','construction_enabled'),('premature real probe','probe_enabled'),('grant inferred','authority_issued'),('own witness before authority','own_future_output_before_authority'),('submitted equals logical','submitted_equals_logical'),('transfer equals durability','transfer_equals_durable')]:reject(name,change(key,True))
reject('wrong namespace',lambda m:m['namespace_types'].pop())
reject('missing CPU limit',lambda m:m['limit_values'].__setitem__('MAX_CPU_SECONDS_PER_PROCESS',None))
reject('missing memory limit',lambda m:m['limit_values'].__setitem__('MAX_MEMORY_BYTES_AGGREGATE',None))
reject('unbounded output',change('capture_bytes',None))
reject('occupancy invented as qualified',change('occupancy_limit',2147483648))
reject('second attempt',change('attempt_number',2))
reject('unknown exit PASS',change('unknown_exit_result','PASS'))
reject('silent retry',change('automatic_retries',1))
reject('extra writable namespace mount',lambda m:m['argv'].extend(['--tmpfs','/other']))
reject('widened construction source allowlist',lambda m:m['source_scope'].append('adapter/planner/core.py'))
reject('four-slot choice silently selected',change('pair_slots_selected','EXPLICIT_REVISED_FOUR'))
reject('outer guard qualified by own future result cycle',lambda m:m['edges'].append(['ACTUAL_NAMESPACE_MOUNT_EXIT','EXISTING_OUTER_SAFETY_PROFILE']))
contracts=['protected-path-escape-assessment.json','host-workspace-identity-and-storage-contract.json','resource-observer-contract.json','one-attempt-contract.json','evidence-allocation.json','passive-witness-specification.json','qualification-expectations.json','capability-entry-execution-classification.json','remaining-gap-dossier.json']
semantic={'VERIFIER_RAW_SHA256':sha(pathlib.Path(__file__).read_bytes()),'INPUT_PINS_SHA256':sha(canon(manifest['PINS'])),'PROFILE_IDENTITY':wrapper['IDENTITY'],'ARGV_SHA256':profile['ARGV_SHA256'],'ELF_SOURCE_FILES':11,'RO_FILE_BINDS':12,'WITNESS_SHA256':w['ARGV_SHA256'],'NORMAL_RECORD_BYTES':5542,'RAW_CAPTURE_POLICY_BYTES':8658872,'CRITICAL_RECORD_BYTES':581,'CRITICAL_RESERVED_SLOTS':2336,'TOTAL_PROPOSED_ALLOCATION':8666750,'PHASE_REQUIREMENTS':36,'CONTRACT_IDENTITIES':{n:sha(canon(load(O/n))) for n in contracts},'READINESS':ready,'GRAPH_ACYCLIC':True,'PRIOR_PRESERVATION':'PASS','NEGATIVES':neg}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':semantic,'SEMANTIC_SHA256':sha(canon(semantic))},sort_keys=True))
