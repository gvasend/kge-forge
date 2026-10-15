"""Static metadata checks only; never imports/executes the gate or synthetic suite."""
import ast,hashlib,json,os,pathlib,subprocess
P=pathlib.Path(__file__).parent;V=P/'static_verify.py'
def write(n,x):
    n=n.replace('.json','-final.json')
    if (P/n).exists():
        assert json.loads((P/n).read_text())==x, 'METADATA_CONFLICT:'+n
        return
    with (P/n).open('x') as f:f.write(json.dumps(x,sort_keys=True,indent=2)+'\n')
rows=[]
for seed in [0,1,7,101]:
    q=subprocess.run(['python3',str(V)],text=True,capture_output=True,check=True,env=dict(os.environ,PYTHONHASHSEED=str(seed),PYTHONDONTWRITEBYTECODE='1'))
    r=json.loads(q.stdout);rows.append({'SEED':seed,'RECONSTRUCTION':r,'SEMANTIC_SHA256':hashlib.sha256(json.dumps(r,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
assert len({x['SEMANTIC_SHA256'] for x in rows})==1
write('independent-static-verification.json',rows[0]['RECONSTRUCTION'])
write('four-seed-static-reconstruction.json',{'RESULT':'PASS_STATIC_SOURCE_RECONSTRUCTION','FRESH_METADATA_PROCESSES':4,'SEEDS':rows,'GATE_IMPORTS':0,'GATE_TESTS_EXECUTED':0})
gp='adapter/qualification_h77_02_gate/gate.py';tp='adapter/tests/test_h77_02_launch_gate.py'
gs=pathlib.Path(gp).read_text();ts=pathlib.Path(tp).read_text();cases=[]
def mutation(label,path,old,new,count=1):
    source=gs if path==gp else ts;assert old in source,label
    cases.append((label,{path:source.replace(old,new,count)}))
mutation('Wrong grant identity accepted',gp,"identity(grant['content'], grant['identity']['namespace']) == grant['identity']","identity(grant['content'], grant['identity']['namespace']) != grant['identity']")
mutation('Wrong approved subject',gp,"SUBJECT_SHA = '762b88071476cea67c08c8e57d5b893f61c2d8843cc7f0f04a07f05b52fe3a80'","SUBJECT_SHA = '"+'0'*64+"'")
mutation('Wrong exact command',gp,"EXACT_COMMAND_SHA = '8c6ebe1406c74e740e1ed9150e62e49a1aeb0466b2aaaa01b9b977a9dfb49a6b'","EXACT_COMMAND_SHA = '"+'0'*64+"'")
mutation('Unstable process-based key',gp,"'authorized_attempt_number': 1}","'authorized_attempt_number': 1, 'pid': os.getpid()}")
mutation('Duplicate claim accepted',gp,'os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW','os.O_CREAT | os.O_NOFOLLOW')
mutation('Missing file fsync',gp,'os.fsync(fd)','pass')
mutation('Missing directory fsync',gp,'os.fsync(directory)','pass')
mutation('Launch before durable verification',gp,'inode = _exclusive_record(directory, name, value, hook if synthetic else None,','synthetic_callback()\n        inode = _exclusive_record(directory, name, value, hook if synthetic else None,')
mutation('Stale lock treated as unused',gp,'fcntl.LOCK_EX | fcntl.LOCK_NB','fcntl.LOCK_SH')
mutation('Partial record admits recovery launch',gp,"'launch_permitted': False","'launch_permitted': True")
mutation('Crash reopens permission',gp,"'retry_allowed': False","'retry_allowed': True",-1)
mutation('Automatic retry enabled',gp,"'TOTAL_WALL': 600, 'RETRIES': 0}","'TOTAL_WALL': 600, 'RETRIES': 1}")
mutation('Unrestricted subprocess argv',gp,"subprocess.Popen(command['ARGV']","subprocess.Popen(['/bin/sh', '-c', 'unapproved']")
cases.append(('Unauthorized source path',{'adapter/planner/codec.py':gs}))
cases.append(('Actual H77 probe invocation in tests',{tp:ts+"\ndef unauthorized_probe():\n    gate.subprocess.Popen(['/usr/bin/bwrap'])\n"}))
cases.append(('Real A15 execution import',{tp:ts+'\nimport adapter.planner.core\n'}))
results=[]
for label,override in cases:
    q=subprocess.run(['python3',str(V),'--candidate'],input=json.dumps(override),text=True,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    assert q.returncode!=0,(label,q.stdout)
    results.append({'CONTROL':label,'RESULT':'REJECTED','COUNTEREXAMPLE':q.stderr.splitlines()[-1]})
write('negative-controls.json',{'RESULT':'16/16 PASS STATIC AST/SOURCE CONTROLS','CONTROLS':results,'QUALIFICATION_LIMIT':'In-memory source corruption only; no gate code imported or executed and no concurrency/crash behavior empirically demonstrated'})
manifest=[]
for f,h in rows[0]['RECONSTRUCTION']['SOURCE_SHA256'].items():
    source=pathlib.Path(f).read_text();tree=ast.parse(source)
    manifest.append({'SOURCE_PATH':f,'SOURCE_SHA256':h,'ENTRYPOINTS':[n.name for n in tree.body if isinstance(n,ast.FunctionDef)],'IMPORTS':[ast.get_source_segment(source,n) for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom))]})
write('source-identity-manifest.json',{'SOURCE_FILES':manifest,'SOURCE_IDENTITIES_SEALED':True,'INTERPRETER_REQUIREMENT':'Python3.8+ on Linux/POSIX with dir_fd/O_NOFOLLOW/flock/fsync; actual interpreter and operating controls unqualified for active entry','DEPENDENCIES':'Python standard library only; no installation performed','CONSUMPTION_SCHEMA_VERSION':'H77-02-CONSUMPTION-RECORD-1 / H77-02-CONSUMPTION-KEY-1','ENTRYPOINT':'python -m adapter.qualification_h77_02_gate.gate --mode {claim-and-launch,recover} --manifest <exact protected entry>; no invocation performed; REAL entry denied pending qualified reader/profile','SYNTHETIC_TEST_SUITE':'adapter.tests.test_h77_02_launch_gate.GateSyntheticTests; every active suite entry requires independently sealed controller/environment/fixture/oracle/campaign receipts','RUNTIME_EXECUTABLE_QUALIFIED':False,'H77_PROBE_AUTHORIZED':False})
print('Static reconstruction and 16/16 controls PASS; no gate execution')
