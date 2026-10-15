"""Read-only independent reconstruction. Does not execute service payload or commands."""
import ast,copy,hashlib,json,pathlib
OUT=pathlib.Path(__file__).resolve().parent;ROOT=pathlib.Path(__file__).resolve().parents[5]
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def check(spec,admin,proc,compat):
 argv=spec['EXACT_COMMAND_ARGV'];assert argv[0]=='/usr/bin/systemd-run' and not any(a in ('--user','--scope','--remain-after-exit') for a in argv),'system instance'
 assert '--uid=1000' in argv and '--gid=1000' in argv and spec['SERVICE_USER']['ROOT_EXECUTION_PERMITTED'] is False,'nonroot execution'
 required={'--property=TasksMax=8','--property=RuntimeMaxSec=20s','--property=MemoryMax=67108864','--property=Restart=no','--property=PrivateNetwork=yes','--property=ProtectSystem=strict','--property=ProtectHome=yes','--property=LimitCPU=5','--property=LimitAS=134217728','--property=LimitFSIZE=65536','--property=LimitNOFILE=32','--property=TimeoutStopSec=2s','--property=KillMode=control-group'}
 assert required<=set(argv),'bounded resource/security properties'
 assert '--collect' in argv and '--wait' in argv,'cleanup'
 assert spec['LIMITS']['AUTOMATIC_RETRIES']==0 and spec['LIMITS']['MAX_SERVICE_LAUNCHES']==1 and spec['LIMITS']['MAX_SERVICE_TASKS']==8
 assert admin['VERIFIED'] is False and admin['PROJECT_OWNER_CHARTER_GRANTS_OS_PERMISSION'] is False,'unknown admin permission'
 assert proc['INDEPENDENT_OBSERVER_REQUIRED'] is True and 'SERVICE_PIDS_CGROUP' in proc['EVIDENCE_FIELDS'],'own pids membership'
 payload=argv[-1];tree=ast.parse(payload);compile(tree,'<syntax-only>','exec')
 assert "entries.get('pids')" in payload and "entries.get('name=systemd')" in payload and "'/sys/fs/cgroup/pids'" in payload,'independent hierarchy'
 assert "maximum!='8'" in payload and "os.geteuid()!=1000" in payload
 assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('fork','execv','Popen','system') for n in ast.walk(tree)),'no workload launch'
 assert compat['FULL_CAMPAIGN_QUALIFIED'] is False and compat['H77_OR_A15_EXECUTION_INCLUDED'] is False,'scope expansion'
 assert spec['EXECUTED'] is False,'no service execution'
 return {'RESULT':'PARTIAL','SYSTEM_LEVEL_PROFILE_COMPLETE':'NO','ADMINISTRATIVE_AUTHORITY_VERIFIED':'NO','PROBE_COMMAND_COMPLETE':'YES','RESOURCE_BOUNDARY_COMPLETE':'YES','EVIDENCE_CONTRACT_COMPLETE':'YES','SYSTEM_LEVEL_PROBE_DECISION_READY':'NO','SYSTEM_LEVEL_PROBE_EXECUTION_READY':'NO'}
def main():
 old=load(OUT.parent/'direct-host-enforcement-85/evidence-index.json')
 for p,h in old['FILES'].items():assert sha(ROOT/p)==h
 assert sha(ROOT/'adapter/tests/test_h77_02_launch_gate.py')=='a2814c74ab10358c2c508eaf35728e9b14879f74a04ce5aea9f5a9310baaf02e'
 spec=load(OUT/'transient-service-specification.json');admin=load(OUT/'administrative-authority-assessment.json');proc=load(OUT/'cgroup-verification-procedure.json');compat=load(OUT/'h77-compatibility-assessment.json')
 seed=spec['UNIT_NAME_SEED'];expected='kge-h86-pids-'+hashlib.sha256(canon(seed)).hexdigest()[:32]+'.service';assert spec['UNIT_NAME']==expected and '--unit='+expected in spec['EXACT_COMMAND_ARGV']
 assert sha(OUT/'prospective-payload.txt')==spec['SOURCE_PROGRAM_SHA256']
 for p,h in spec['EXECUTABLE_PINS'].items():assert sha(pathlib.Path(p))==h
 subject=load(OUT/'proposed-authorization-subject.json');body=dict(subject);identity=body.pop('PROPOSED_CONTENT_IDENTITY');assert hashlib.sha256(canon(body)).hexdigest()==identity['sha256'];assert subject['ADMINISTRATIVE_AUTHORITY']['EVIDENCE'] is None and subject['DECISION_OPTIONS']==[]
 readiness=check(spec,admin,proc,compat);negatives=[]
 cases=['user instance','missing pids membership','root execution','unbounded runtime','wrong TasksMax','permission invented','missing cleanup','network uncontrolled','H77 included','A15 included','automatic retry','full campaign claim']
 for name in cases:
  s,a,p,c=copy.deepcopy((spec,admin,proc,compat))
  if name=='user instance':s['EXACT_COMMAND_ARGV'].insert(1,'--user')
  elif name=='missing pids membership':p['EVIDENCE_FIELDS'].remove('SERVICE_PIDS_CGROUP')
  elif name=='root execution':s['EXACT_COMMAND_ARGV']=[arg.replace('--uid=1000','--uid=0') for arg in s['EXACT_COMMAND_ARGV']]
  elif name=='unbounded runtime':s['EXACT_COMMAND_ARGV'].remove('--property=RuntimeMaxSec=20s')
  elif name=='wrong TasksMax':s['EXACT_COMMAND_ARGV']=[arg.replace('TasksMax=8','TasksMax=999') for arg in s['EXACT_COMMAND_ARGV']]
  elif name=='permission invented':a['VERIFIED']=True
  elif name=='missing cleanup':s['EXACT_COMMAND_ARGV'].remove('--collect')
  elif name=='network uncontrolled':s['EXACT_COMMAND_ARGV'].remove('--property=PrivateNetwork=yes')
  elif name in ('H77 included','A15 included'):c['H77_OR_A15_EXECUTION_INCLUDED']=True
  elif name=='automatic retry':s['LIMITS']['AUTOMATIC_RETRIES']=1
  else:c['FULL_CAMPAIGN_QUALIFIED']=True
  try:check(s,a,p,c)
  except AssertionError:negatives.append({'CONTROL':name,'RESULT':'REJECTED'})
  else:raise AssertionError('negative accepted '+name)
 result={'READINESS':readiness,'UNIT_NAME':expected,'PROPOSED_SUBJECT_IDENTITY':identity,'EXECUTABLE_PINS':spec['EXECUTABLE_PINS'],'PAYLOAD_SHA256':spec['SOURCE_PROGRAM_SHA256'],'CGROUP_EXPECTATION':{'SERVICE_PIDS_CGROUP':'/system.slice/'+expected,'KERNEL_PIDS_MAX':'8','SYSTEMD_TASKS_MAX':8,'EXCESS_TASK_REJECTION_PROVEN':False},'NEGATIVE_CONTROLS':negatives,'SYSTEM_LEVEL_PROBES_EXECUTED':0}
 result['SEMANTIC_IDENTITY']={'kind':'CONTENT_IDENTITY','namespace':'qualification-h86-independent-reconstruction-v1','sha256':hashlib.sha256(canon(result)).hexdigest()}
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
