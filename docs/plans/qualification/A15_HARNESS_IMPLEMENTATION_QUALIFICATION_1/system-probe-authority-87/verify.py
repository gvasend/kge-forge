"""Independent metadata/AST authority reconstruction, no probe or gate invocation."""
import ast,copy,hashlib,json,pathlib,subprocess,sys
OUT=pathlib.Path(__file__).resolve().parent;ROOT=pathlib.Path(__file__).resolve().parents[5]
def read(p):return json.loads(p.read_text())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def classify(s):
 assert s['host']=='ubuntu01','wrong host'
 assert s['argv']==s['retained_argv'],'changed command'
 assert s['binary']=='15c14831822016fd68ab3e2f265223463c46b4cf7fcc4595a91f09c5bbd950eb','binary'
 assert '--uid=1000' in s['argv'] and '--gid=1000' in s['argv'],'root service'
 assert '--property=TasksMax=8' in s['argv'] and '--property=RuntimeMaxSec=20s' in s['argv'],'resource bounds'
 assert s['sudo_current']=='UNVERIFIED' and s['owner_admin']=='OWNER_ATTESTED','attestation not permission'
 assert s['service_pids']=='/system.slice/'+s['unit'],'own service pids'
 assert s['attempt']==1 and s['limit']==1 and s['retries']==0,'duplicate attempt/retry'
 assert s['persistent_changes'] is False and s['H77_scope'] is False and s['A15_scope'] is False,'scope expansion'
 assert s['issued_grant'] is None and s['gate_real_binding'] is None,'premature grant/binding'
 assert s['mechanism_qualified'] is False and s['failure_reopens'] is False and s['unknown_reopens'] is False,'one-use claim'
 return {'RESULT':'PARTIAL','ADMINISTRATOR_DESIGNATION':'OWNER_DECLARED','HOST_ADMINISTRATIVE_AUTHORITY':'OWNER_ATTESTED','CHARTER_EFFECTIVE':'YES','PACKAGE_86_COMMAND_VERIFIED':'YES','PROBE_SCOPE_COMPLETE':'YES','ONE_ATTEMPT_CONTRACT_COMPLETE':'NO','SYSTEM_PROBE_DECISION_READY':'NO','SYSTEM_PROBE_EXECUTION_READY':'NO','DECISION_OPTIONS':[]}
def reconstruct():
 base=OUT.parent;old=base/'system-process-enforcement-86';idx=read(old/'evidence-index.json')
 for p,h in idx['FILES'].items():assert sha(ROOT/p)==h
 spec=read(old/'transient-service-specification.json');command=read(OUT/'package86-command-authentication.json');provenance=read(OUT/'administrator-declaration-provenance.json');subject=read(OUT/'proposed-system-level-probe-subject.json');one=read(OUT/'one-attempt-consumption-requirements.json');entry=read(OUT/'host-entry-predicate-contract.json');evidence=read(OUT/'probe-evidence-contract.json')
 assert provenance['EXACT_DECLARATION']=='The project owner is also the administrator of `ubuntu01`, with authority to use sudo and manage system-level services.'
 assert provenance['INDEPENDENT_AUTHENTICATION_EVIDENCE'] is None and provenance['PERSONAL_OR_ACCOUNT_IDENTITY'] is None and provenance['ACTUAL_SUDO_PERMISSION_VERIFIED'] is False
 prov_body=dict(provenance);prov_id=prov_body.pop('IDENTITY');assert hashlib.sha256(canon(prov_body)).hexdigest()==prov_id['sha256']
 assert command['COMMAND_ARGUMENT_VECTOR']==spec['EXACT_COMMAND_ARGV']==subject['COMMAND_ARGUMENT_VECTOR']
 assert command['RESOURCE_LIMITS']==subject['RESOURCE_LIMITS']==spec['LIMITS']
 for p,h in spec['EXECUTABLE_PINS'].items():assert sha(pathlib.Path(p))==h
 assert hashlib.sha256(canon(spec['EXACT_COMMAND_ARGV'])).hexdigest()==command['CANONICAL_ARGV_CONTENT_IDENTITY']['sha256']
 tree=ast.parse((ROOT/'adapter/qualification_h77_02_gate/gate.py').read_text());binding=next(n.value.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='QUALIFIED_REAL_AUTHORITY_BINDING' for t in n.targets));assert binding is None
 assert all(p['CURRENT'] in ('UNVERIFIED','NOT_ISSUED') and p['RESULT']=='BLOCK_EXECUTION' for p in entry['PREDICATES'])
 assert len(entry['PREDICATES'])==10 and one['QUALIFIED_MECHANISM_FOR_THIS_PROBE'] is None
 assert '--collect' in spec['EXACT_COMMAND_ARGV'] and one['SYSTEMD_UNIT_NAME_IS_NOT_CONSUMPTION']
 body=dict(subject);subjectid=body.pop('PROPOSED_CONTENT_IDENTITY');assert hashlib.sha256(canon(body)).hexdigest()==subjectid['sha256']
 assert subject['FUTURE_PROJECT_APPROVAL'] is None and subject['FUTURE_ISSUED_GRANT'] is None and subject['DECISION_OPTIONS']==[]
 # Independently re-read effective lifecycle rather than promoting old draft text.
 charter=json.loads(subprocess.check_output([sys.executable,'docs/plans/qualification/KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_ADOPTION_66/reader.py'],cwd=str(ROOT),text=True));assert charter['CHARTER_EFFECTIVE'] and [e['STATE'] for e in charter['ORDERED_LIFECYCLE']]==['DRAFT','REVIEWED','APPROVED','EFFECTIVE'];assert subject['EFFECTIVE_CHARTER']==charter['CHARTER_CONTENT_IDENTITY'] and subject['EFFECTIVE_LIFECYCLE']==charter['ORDERED_LIFECYCLE'][-1]['EVIDENCE_IDENTITY']
 # Symbolic future key is reconstructed with inert metadata identities only;
 # this invokes neither consumption nor a synthetic gate test.
 keys=one['KEY_INPUTS'];assert len(keys)==6 and all(x not in one['KEY_EXCLUDES'] for x in keys)
 example={'schema':one['KEY_SCHEMA'],'issued_probe_grant_identity':{'kind':'CONTENT_IDENTITY','namespace':'METADATA_ONLY_NOT_A_GRANT','sha256':'1'*64},'approved_probe_subject_identity':subjectid,'retained_package86_probe_subject_identity':command['PACKAGE86_SUBJECT_IDENTITY'],'exact_command_identity':command['CANONICAL_ARGV_CONTENT_IDENTITY'],'qualified_direct_host_context_identity':{'kind':'CONTENT_IDENTITY','namespace':'METADATA_ONLY_NOT_A_HOST_PROFILE','sha256':'2'*64},'authorized_attempt_number':1}
 key_example=hashlib.sha256(canon(example)).hexdigest()
 state={'host':subject['EXACT_HOST'],'argv':command['COMMAND_ARGUMENT_VECTOR'],'retained_argv':spec['EXACT_COMMAND_ARGV'],'binary':spec['EXECUTABLE_PINS']['/usr/bin/systemd-run'],'sudo_current':next(p['CURRENT'] for p in entry['PREDICATES'] if p['PREDICATE']=='SUDO_PERMISSION'),'owner_admin':provenance['HOST_ADMINISTRATIVE_AUTHORITY'],'service_pids':evidence['FIELD_BINDINGS']['SERVICE_PIDS_CGROUP'],'unit':spec['UNIT_NAME'],'attempt':1,'limit':one['MAX_PROBE_ATTEMPTS'],'retries':one['AUTOMATIC_RETRIES'],'persistent_changes':False,'H77_scope':False,'A15_scope':False,'issued_grant':subject['FUTURE_ISSUED_GRANT'],'gate_real_binding':binding,'mechanism_qualified':one['QUALIFIED_MECHANISM_FOR_THIS_PROBE'] is not None,'failure_reopens':one['FAILURE_REOPENS_PERMISSION'],'unknown_reopens':one['UNKNOWN_OUTCOME_REOPENS_PERMISSION']}
 ready=classify(state);negatives=[]
 cases=[('wrong host','host','other'),('wrong executable','binary','0'*64),('wrong args','argv',state['argv']+['extra']),('root service','argv',[a.replace('--uid=1000','--uid=0') for a in state['argv']]),('missing TasksMax','argv',[a for a in state['argv'] if a!='--property=TasksMax=8']),('unbounded wall','argv',[a for a in state['argv'] if a!='--property=RuntimeMaxSec=20s']),('sudo assumed verified','sudo_current','VERIFIED'),('parent manager cgroup','service_pids','/user.slice/user-1000.slice'),('duplicate attempt','attempt',2),('automatic retry','retries',1),('persistent changes','persistent_changes',True),('H77 included','H77_scope',True),('A15 included','A15_scope',True),('premature issuance','issued_grant',{'pretend':True}),('static gate treated as qualified','mechanism_qualified',True),('failure reopens permission','failure_reopens',True),('unknown reopens permission','unknown_reopens',True)]
 for name,key,value in cases:
  mutation=copy.deepcopy(state);mutation[key]=value
  try:classify(mutation)
  except AssertionError:negatives.append({'CONTROL':name,'RESULT':'REJECTED'})
  else:raise AssertionError('negative accepted: '+name)
 result={'READINESS':ready,'DECLARATION_IDENTITY':prov_id,'PROPOSED_SUBJECT_IDENTITY':subjectid,'PACKAGE86_SUBJECT_IDENTITY':command['PACKAGE86_SUBJECT_IDENTITY'],'COMMAND_IDENTITY':command['CANONICAL_ARGV_CONTENT_IDENTITY'],'UNIT_NAME':spec['UNIT_NAME'],'LIFECYCLE_IDENTITIES':[e['EVIDENCE_IDENTITY'] for e in charter['ORDERED_LIFECYCLE']],'KEY_RULE_EXAMPLE_METADATA_ONLY':key_example,'NEGATIVES':negatives,'SERVICES_TESTS_OR_PROBES_EXECUTED':0}
 result['SEMANTIC_IDENTITY']={'kind':'CONTENT_IDENTITY','namespace':'qualification-h87-independent-reconstruction-v1','sha256':hashlib.sha256(canon(result)).hexdigest()};return result
if __name__=='__main__':print(json.dumps(reconstruct(),sort_keys=True))
