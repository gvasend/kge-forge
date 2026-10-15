"""Independent AST/JSON reader. Never imports or executes the harness or gate."""
import ast, copy, hashlib, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[5]
OUT=pathlib.Path(__file__).resolve().parent
SOURCE=ROOT/'adapter/tests/test_h77_02_launch_gate.py'
OLD=OUT.parent/'synthetic-harness-repair-83'
def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def identity(x,domain): return {'kind':'CONTENT_IDENTITY','namespace':domain,'sha256':hashlib.sha256(canon(x)).hexdigest()}
def verify(source,doc):
 tree=ast.parse(source); compile(tree,'<static-only>','exec')
 cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='GateSyntheticTests')
 names=sorted(n.name for n in cls.body if isinstance(n,ast.FunctionDef) and n.name.startswith('test_'))
 oldtree=ast.parse((OUT/'package-83-test-source.txt').read_text())
 oldcls=next(n for n in oldtree.body if isinstance(n,ast.ClassDef) and n.name=='GateSyntheticTests')
 oldnames=sorted(n.name for n in oldcls.body if isinstance(n,ast.FunctionDef) and n.name.startswith('test_'))
 assert names==oldnames and len(names)==18 and sorted(doc['tests'])==names,'original test selection'
 requirements={
 'operation identity':"'qualification-h77-02-synthetic-operation-v1'",
 'exact comparison':'_compare_operation_traces(row, content, specification)',
 'fixture closure':"raise HarnessError('INCOMPLETE_OR_DUPLICATE_FIXTURE_CATALOG')",
 'exact callback':'EXACT_OPERATION_TRACE_MISMATCH',
 'fsync comparison':"'barrier.confirmed'",
 'confirmation comparison':"'readonly-confirmation.confirmed'",
 'callback ceiling':'CONCURRENT_WINNER_OR_CALLBACK_MISMATCH',
 'first failure latch':'if self._first_failure is None:',
 'secondary preservation':'self._secondary_errors.append(detail)',
 'durable failure':'self.failure_evidence(self.root / \'first-counterexample.json\'',
 'deadline':'UNSEALED_CAMPAIGN_ACCOUNTING_HEADER',
 'inclusive accounting':'MAX_ACTUAL_PROCESS_SLOTS',
 'bounded termination':'process.kill(); process.join(timeout=2)',
 'independent tracker exit':'os.waitpid(pid, os.WNOHANG)',
 'exact campaign controller':'def run_campaign_controller():',
 'no bypass':'UNCONTROLLED_TEST_DISCOVERY_DENIED',
 'no retry':'break  # Never launch a later seed or retry after first failure.',
 'cleanup retention':"'consumption_cleanup_permitted': False",
 'output confinement':'UNEXPECTED_STORE_OUTPUT',
 'resource ceiling':'resource.setrlimit(getattr(resource, name), (value, value))'}
 for k,v in requirements.items(): assert v in source,k
 assert 'unittest.main(' not in source
 assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('unlink','rmdir','rmtree') for n in ast.walk(tree)), 'unauthorized cleanup'
 assert 'QUALIFIED_REAL_AUTHORITY_BINDING = None' in (ROOT/'adapter/qualification_h77_02_gate/gate.py').read_text()
 old=json.loads((OLD/'independent-executable-oracle-specification.json').read_text())
 successes={'test_first_and_duplicate_claim','test_concurrent_claimants_at_most_one','test_process_restart_preserves_claim','test_no_real_launcher_reachable_in_synthetic_mode'}
 count=0
 for name,test in doc['tests'].items():
  assert set(test['variants'])==set(old['tests'][name]['variants'])
  for variant,model in test['variants'].items():
   rule=test['operation_comparisons'][variant]
   assert rule['retry_count']==0 and rule['unmatched_operation_allowed'] is False and rule['unexpected_event_allowed'] is False
   assert rule['successful_claims']==(1 if name in successes else 0)
   assert len(rule['slots'])==model['request_constraints']['count']
   assert len({(s['actor'],s['ordinal']) for s in rule['slots']})==len(rule['slots'])
   for slot in rule['slots']:
    for option in slot['alternatives']:
     events=option['events']; kinds=[e['kind'] for e in events]; mode=option['classification']
     assert kinds[0]=='claim.request' and kinds.count('claim.request')==1
     assert kinds.count('callback.invoked')==(1 if mode in ('success','callback') or (mode=='crash' and model['controlled_crash_point'] in ('AFTER_LAUNCH_BEFORE_OBSERVATION','AFTER_COMPLETION_BEFORE_AUDIT')) else 0)
     assert all(set(e)=={'kind','value'} for e in events)
     # Separate normative reconstruction: barriers, callback and first-failure
     # obligations come from the retained transition sequence, not this oracle.
     counts={'success':(8,8,1,0,8),'callback':(8,8,1,1,6),'partial':(2,2,0,2,2),
       'file':(2,0,0,3,2),'directory':(4,2,0,3,3),'reread':(4,4,0,2,5),
       'before':(0,0,0,2,1),'duplicate':(0,0,0,1,1),
       'invalid':(0,0,0,1,0),'command':(0,0,0,1,0),'resource':(0,0,0,1,0),
       'permission':(0,0,0,1,0),'revoked':(0,0,0,1,0),'locked':(0,0,0,1,0),'symlink':(0,0,0,1,0)}
     if mode!='crash':
      actual=tuple(kinds.count(k) for k in ('barrier.request','barrier.confirmed','readonly-confirmation.confirmed','fault.observed','stage'))
      assert actual==counts[mode], 'independent per-operation occurrence counts'
     else:
      points=['DURING_CLAIM','AFTER_FILE_FSYNC','AFTER_DIRECTORY_FSYNC','AFTER_CLAIM_BEFORE_LAUNCH','DURING_LAUNCH','AFTER_LAUNCH_BEFORE_OBSERVATION','AFTER_COMPLETION_BEFORE_AUDIT']
      i=points.index(model['controlled_crash_point']); barriers=[0,1,2,2,6,6,6][i]
      assert kinds.count('barrier.request')==barriers and kinds.count('barrier.confirmed')==barriers
     error_origins={'before':'stage:BEFORE_CLAIM','partial':'stage:DURING_CLAIM','file':'fsync:$FILE:claim',
       'directory':'fsync:directory','reread':'readonly-confirmation'}
     fault_events=[e['value'] for e in events if e['kind']=='fault.observed']
     if fault_events: assert fault_events[0]['first']['origin']==error_origins.get(mode,'gate-exception')

     if mode=='success':
      assert kinds[-1]=='claim.returned' and kinds.count('barrier.confirmed')==8 and kinds.count('readonly-confirmation.confirmed')==1
     elif mode=='crash': assert kinds[-1]=='fault.injected' and events[-1]['value']['point']==model['controlled_crash_point']
     else: assert kinds[-1]=='claim.failed' and 'fault.observed' in kinds
     faults=[e['value'] for e in events if e['kind']=='fault.observed']
     if faults:
      first=faults[0]['first']; assert faults[0]['secondary'] is False
      assert all(f['first']==first and f['secondary']==(f['observed']!=first) for f in faults)
     assert 'gate-output' not in canon(events).decode()
    count+=1
 body=dict(doc); supplied=body.pop('identity')
 assert supplied==identity(body,'qualification-h77-02-executable-oracles-v1'),'oracle identity'
 return {'tests':names,'operation_slots':count,'oracle_identity':supplied,'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'static_checks':sorted(requirements),'synthetic_tests_executed':0,'active_readiness':False}
def main():
 source=SOURCE.read_text(); doc=json.loads((OUT/'independent-executable-oracle-specification.json').read_text())
 result=verify(source,doc)
 negatives=[]
 for label,old,new in [('omitted comparison','_compare_operation_traces(row, content, specification)','pass'),('altered fixture acceptance','INCOMPLETE_OR_DUPLICATE_FIXTURE_CATALOG','IGNORED'),('lost first failure','if self._first_failure is None:','if True:'),('lost secondary error','self._secondary_errors.append(detail)','pass'),('duplicate callbacks','CONCURRENT_WINNER_OR_CALLBACK_MISMATCH','IGNORED'),('missing timeout','process.kill(); process.join(timeout=2)','process.join()'),('unobserved tracker','os.waitpid(pid, os.WNOHANG)','(0, 0)'),('incomplete accounting','UNSEALED_CAMPAIGN_ACCOUNTING_HEADER','IGNORED'),('unbounded campaign','def run_campaign_controller():','def other_controller():'),('retry','break  # Never launch a later seed or retry after first failure.','continue'),('unrestricted discovery','UNCONTROLLED_TEST_DISCOVERY_DENIED','IGNORED'),('scope/cleanup expansion',"'consumption_cleanup_permitted': False","'consumption_cleanup_permitted': True")]:
  assert old in source
  try: verify(source.replace(old,new),doc)
  except (AssertionError,SyntaxError,StopIteration):negatives.append({'control':label,'result':'REJECTED'})
  else: raise AssertionError('negative accepted: '+label)
 for label in ('omitted fsync observation','altered oracle identity','unexpected operation','retry allowed'):
  mutation=copy.deepcopy(doc); rule=mutation['tests']['test_first_and_duplicate_claim']['operation_comparisons']['main']
  if label=='omitted fsync observation': rule['slots'][0]['alternatives'][0]['events']=[e for e in rule['slots'][0]['alternatives'][0]['events'] if e['kind']!='barrier.confirmed']
  elif label=='altered oracle identity':mutation['identity']['sha256']='0'*64
  elif label=='unexpected operation':rule['slots'].append(copy.deepcopy(rule['slots'][0]))
  else:rule['retry_count']=1
  try: verify(source,mutation)
  except AssertionError:negatives.append({'control':label,'result':'REJECTED'})
  else:raise AssertionError('negative accepted: '+label)
 result['negative_controls']=negatives
 result['semantic_identity']=identity(result,'qualification-h77-02-static-closure-verification-v1')
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
