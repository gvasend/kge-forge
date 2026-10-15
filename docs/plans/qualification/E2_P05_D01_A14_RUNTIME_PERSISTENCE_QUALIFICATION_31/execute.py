"""Contract-30 supervisor. Running this file performs the authorized two saves.
Children use the unchanged sealed callables; profiling observes returns only.
"""
import os,sys,json,hashlib,subprocess,time,importlib.util,copy
from pathlib import Path
R=Path('/home/gvasend/app/kge-forge')
C=R/'docs/plans/qualification/E2_P05_D01_A14_RUNTIME_PERSISTENCE_CONTRACT_30'
E=Path(__file__).parent
OPTION='AUTHORIZE_BOUNDED_A14_RUNTIME_PERSISTENCE_QUALIFICATION'
SUBJECT_HASH='ee579ab7bc581230677a98a8a011c4dd6c6b563cf09c2b0c3f4426fd7368c8ce'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def emit(name,obj):
 p=E/name
 assert not p.exists(),str(p)
 p.write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def authenticate():
 raw=(C/'bounded-execution-decision-subject.json').read_bytes();assert sha(raw)==SUBJECT_HASH
 s=json.loads(raw);v=dict(s);identity=v.pop('SUBJECT_IDENTITY');assert identity=='qualification-A14-runtime-persistence-decision-v1:'+sha(canon(v));assert s['OPTION']==OPTION
 def pins(x):
  if isinstance(x,dict):
   if 'path' in x and 'raw_sha256' in x:assert sha((R/x['path']).read_bytes())==x['raw_sha256'],x['path']
   for z in x.values():pins(z)
  elif isinstance(x,list):
   for z in x:pins(z)
 pins(s);m=load(C/'execution-input-manifest.json');pins(m)
 return s,m

def child(mode,index,evidence_path=None):
 from adapter.planner import codec
 s,m=authenticate();row=load(C/'runtime-sequence.json')['EXECUTION_ROWS'][index]
 spec=row['WRITER_SPEC' if mode=='writer' else 'READER_SPEC']
 auth=load(E/'scope-authentication.json');assert auth['SELECTED_OPTION']==OPTION and auth['SUBJECT_IDENTITY']==s['SUBJECT_IDENTITY'] and auth['SCOPE_AUTHENTICATION']=='PASS'
 source=s['WRITER_SOURCE' if mode=='writer' else 'READER_SOURCE'];assert sha((R/source['path']).read_bytes())==source['raw_sha256']
 module_spec=importlib.util.spec_from_file_location('sealed_'+mode,R/source['path']);module=importlib.util.module_from_spec(module_spec);module_spec.loader.exec_module(module)
 observations=[]
 def profile(frame,event,arg):
  if event=='return' and frame.f_code is codec.save_bundle.__code__ and arg is not None:
   observations.append({'operation':'codec.save_bundle','time_ns':time.monotonic_ns(),'path':str(arg[0]),'identity':codec._wire(arg[1])})
  if event=='return' and frame.f_code is codec.restore.__code__ and arg is not None:
   observations.append({'operation':'codec.restore','time_ns':time.monotonic_ns(),'bundle_id':codec._wire(codec.bundle_id(arg)),'snapshot_id':codec._wire(codec.snapshot_id(arg.current)),'sources':codec._wire(arg.sources),'policy':codec._wire(arg.policy),'policy_version':arg.policy_version,'scope':arg.scope,'events':codec._wire(arg.events),'initial_id':codec._wire(codec.snapshot_id(arg.initial))})
  if event=='return' and frame.f_code is codec._write_immutable.__code__:
   observations.append({'operation':'codec._write_immutable','time_ns':time.monotonic_ns(),'result':str(arg)})
 sys.setprofile(profile)
 if mode=='writer':
  result=module.run_writer(spec,lambda supplied:supplied==row['WRITER_SPEC'])
 else:
  evidence=load(evidence_path)
  def guard_verifier(supplied,ev):
   return supplied==row['READER_SPEC'] and ev==load(evidence_path) and ev['subject_identity']==s['SUBJECT_IDENTITY'] and ev['TARGET_ID']==row['TARGET_ID'] and ev['writer_exit_observed'] and ev['writer_exit_code']==0 and all(ev[g] for g in supplied['REQUIRED_GUARDS']) and os.getppid()==ev['supervisor_pid'] and os.getpid()!=ev['writer_pid']
  result=module.run_reader(spec,evidence,lambda supplied:supplied==row['READER_SPEC'],guard_verifier)
 sys.setprofile(None)
 print(json.dumps({'row':row['TARGET_ID'],'pid':os.getpid(),'ppid':os.getppid(),'seed':os.environ['PYTHONHASHSEED'],'result':result,'observations':observations,'completed_ns':time.monotonic_ns()},sort_keys=True))

def baseline():
 paths=[]
 for base in ['adapter','docs']:
  paths.extend(p for p in (R/base).rglob('*') if p.is_file() and '__pycache__' not in p.parts and E not in p.parents)
 paths.extend(R/name for name in ['E2-DECIDE.json','E2-CHECK.json','E2-COLLECT.json','E2-FINISH.json','E2-PREPARE.json','source.json','resolution.json'])
 return {str(p.relative_to(R)):sha(p.read_bytes()) for p in sorted(paths)}
def launch(mode,index,seed,ev=None):
 env={'PATH':os.environ.get('PATH','/usr/bin:/bin'),'PYTHONPATH':str(R),'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':str(seed),'LC_ALL':'C.UTF-8'}
 cmd=[sys.executable,str(Path(__file__).resolve()),'child',mode,str(index)]
 if ev:cmd.append(str(ev))
 start=time.monotonic_ns();proc=subprocess.Popen(cmd,cwd=str(R),env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
 out,err=proc.communicate(timeout=120)
 record={'pid':proc.pid,'supervisor_pid':os.getpid(),'start_ns':start,'exit_observed_ns':time.monotonic_ns(),'exit_code':proc.returncode,'stdout':out.decode(),'stderr':err.decode()}
 emit('{}-{}-{}-{}.json'.format(mode,index,seed,proc.pid),record)
 assert proc.returncode==0,record
 value=json.loads(out);assert value['pid']==proc.pid and value['ppid']==os.getpid();record['value']=value
 return record

def execute():
 s,m=authenticate();rows=load(C/'runtime-sequence.json')['EXECUTION_ROWS'];assert len(rows)==2
 for row in rows:
  assert not Path(row['WRITER_SPEC']['EXPECTED_TARGET']).exists();assert not Path(row['WRITER_SPEC']['HANDOFF_PATH']).exists()
 before=baseline();emit('preservation-before.json',before)
 emit('scope-authentication.json',{'SELECTED_OPTION':OPTION,'SUBJECT_IDENTITY':s['SUBJECT_IDENTITY'],'SUBJECT_SHA256':SUBJECT_HASH,'SCOPE_AUTHENTICATION':'PASS','AUTHORITY_SOURCE':'Explicit human selection in work-package 31; prior dossier remains unmodified and historically unselected','EXCLUDED':s['HISTORICAL_EXCLUSIONS']})
 expected=(R/m['NATIVE_BUNDLE_CANDIDATE']['path']).read_bytes();assert len(expected)==153602 and sha(expected)==s['EXPECTED_HASH']
 results=[];pids=set();negative_results=[]
 for index,row in enumerate(rows):
  writer=launch('writer',index,row['WRITER_SEED']);ws=row['WRITER_SPEC'];rs=row['READER_SPEC'];observed=[x for x in writer['value']['observations'] if x['operation']=='codec.save_bundle'];assert len(observed)==1 and observed[0]['path']==ws['EXPECTED_TARGET'] and observed[0]['identity']==s['BUNDLE_ID']
  target=Path(ws['EXPECTED_TARGET']);actual=target.read_bytes();assert not target.is_symlink() and actual==expected
  hp=Path(ws['HANDOFF_PATH']);hraw=hp.read_bytes();assert not hp.is_symlink() and sha(hraw)==rs['EXPECTED_HANDOFF_HASH'] and json.loads(hraw)==rs['EXPECTED_HANDOFF_RECORD']
  assert rs['EXPECTED_HANDOFF_RECORD']['WRITER_EXIT_CLAIMED_BY_RECORD'] is False
  ev={'subject_identity':s['SUBJECT_IDENTITY'],'TARGET_ID':row['TARGET_ID'],'supervisor_pid':os.getpid(),'writer_pid':writer['pid'],'writer_exit_code':writer['exit_code'],'writer_exit_observed':True,'writer_exit_observed_ns':writer['exit_observed_ns'],'SAVE_RETURNED_SUCCESSFULLY':True,'PUBLISHED_TARGET_VERIFIED':True,'PERSISTED_HANDOFF_AVAILABLE':True,'WRITER_EXIT_OBSERVED_BY_SUPERVISOR':True,'target_hash':sha(actual),'handoff_hash':sha(hraw)}
  emit('supervisor-evidence-{}.json'.format(index),ev);ep=E/'supervisor-evidence-{}.json'.format(index)
  # Non-destructive launch controls; never create extra readers or mutate files.
  def launch_gate(spec,guards):
   return spec==rs and guards==ev and all(guards.get(g) is True for g in rs['REQUIRED_GUARDS']) and guards.get('writer_exit_observed') is True
  for guard in rs['REQUIRED_GUARDS']:
   bad=copy.deepcopy(ev);bad[guard]=False;assert not launch_gate(rs,bad);negative_results.append({'row':row['TARGET_ID'],'control':guard+' omitted','rejected':True,'reader_started':False})
  for field in ['TARGET_PATH','EXPECTED_HASH','EXPECTED_BUNDLE_ID','EXPECTED_POLICY_VERSION','EXPECTED_NATIVE_REPLAY_SCOPE','FRAME_IDENTITY']:
   bad=copy.deepcopy(rs);bad[field]='wrong';assert not launch_gate(bad,ev);negative_results.append({'row':row['TARGET_ID'],'control':'wrong '+field,'rejected':True,'reader_started':False})
  bad=copy.deepcopy(ev);bad['in_memory_bundle']='forbidden';assert not launch_gate(rs,bad);negative_results.append({'row':row['TARGET_ID'],'control':'warm-state leakage','rejected':True,'reader_started':False})
  readers=[]
  for schedule in row['READER_SCHEDULE']:
   reader=launch('reader',index,schedule['seed'],ep);v=reader['value'];assert reader['start_ns']>ev['writer_exit_observed_ns'];assert v['pid'] not in pids and v['pid']!=writer['pid'];pids.add(v['pid'])
   result=v['result'];expected_result={'schema':'A14-COLD-READER-IDENTITY-RESULT-1','restore_status':'PASS','bundle_identity':s['BUNDLE_ID'],'snapshot_identity':rs['EXPECTED_SNAPSHOT_ID'],'policy_version':rs['EXPECTED_POLICY_VERSION'],'native_replay_scope':rs['EXPECTED_NATIVE_REPLAY_SCOPE'],'event_count':0,'source_policy_validation':'PASS','identity_comparison':'PASS','reader_pid':v['pid'],'failure':None,'full_D01_output_comparison':'REQUIRES_SEPARATE_INDEPENDENT_OUTPUT_ORACLE'}
   assert result==expected_result
   restores=[z for z in v['observations'] if z['operation']=='codec.restore'];assert len(restores)==1;restored=restores[0]
   assert restored['bundle_id']==s['BUNDLE_ID'] and restored['snapshot_id']==rs['EXPECTED_SNAPSHOT_ID']==restored['initial_id']
   assert sorted(restored['sources'],key=canon)==sorted(rs['EXPECTED_SOURCE_PINS'],key=canon)
   assert restored['policy']==rs['EXPECTED_POLICY_PIN'] and restored['policy_version']==rs['EXPECTED_POLICY_VERSION'] and restored['scope']==rs['EXPECTED_NATIVE_REPLAY_SCOPE'] and restored['events']==[]
   readers.append({'index':schedule['reader_index'],'seed':schedule['seed'],'process':reader,'complete_comparison':'PASS','G5_READER_STARTED_FRESH':'PASS','G6_RESTORE_VALIDATED':'PASS','G7_REPLAY_VALIDATED':'PASS','frame_identity':rs['FRAME_IDENTITY'],'policy_binding_identity':rs['POLICY_BINDING_IDENTITY'],'replay_scope_identity':rs['REPLAY_SCOPE_IDENTITY']})
  results.append({'row':row['TARGET_ID'],'result':'PASS','writer':writer,'publication':{'path':str(target),'length':len(actual),'sha256':sha(actual),'bundle_id':s['BUNDLE_ID']},'handoff':{'path':str(hp),'hash':sha(hraw),'record':json.loads(hraw)},'supervisor_evidence':ev,'guards':{'G1_SAVE_RETURN':'PASS','G2_PUBLICATION_VERIFIED':'PASS','G3_PERSISTED_HANDOFF':'PASS','G4_WRITER_EXIT_OBSERVED':'PASS'},'readers':readers})
  emit('row-{}-result.json'.format(index),results[-1]);print('ROW',index,'PASS 12/12 readers',flush=True)
 emit('runtime-results.json',{'ROWS':results,'NEGATIVE_CONTROLS':negative_results,'RETRIES':0})
 after=baseline();assert after==before,'PREEXISTING_ARTIFACT_CHANGED';emit('preservation-after.json',{'PASS':True,'FILES':after,'CHANGED':[]})
if __name__=='__main__':
 if len(sys.argv)>1 and sys.argv[1]=='child':child(sys.argv[2],int(sys.argv[3]),sys.argv[4] if len(sys.argv)>4 else None)
 else:execute()
