"""Independent metadata/AST reconstruction; no gate, harness or host probe execution."""
import ast,copy,hashlib,json,pathlib,re
OUT=pathlib.Path(__file__).resolve().parent;ROOT=pathlib.Path(__file__).resolve().parents[5]
def load(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def classify(state):
 assert state['test_source']=='a2814c74ab10358c2c508eaf35728e9b14879f74a04ce5aea9f5a9310baaf02e','source pin'
 assert state['managed_context']=='CODEX_MANAGED_CURRENT_NOT_DIRECT_SHELL','context substitution'
 assert all(row['CURRENT_STATUS']=='UNQUALIFIED' for row in state['resources']),'unverified qualification'
 assert state['limits']=={'CHILD_AS':1073741824,'CHILD_CPU':30,'CHILD_FDS':64,'CHILD_FSIZE':16777216,'CHILD_WALL':60,'MAX_ACTUAL_PROCESS_SLOTS':4,'MAX_PAYLOAD_LAUNCHES':128,'RETRIES':0,'TOTAL_WALL':600,'TOTAL_WRITES':67108864},'approved limits'
 assert set(row['CONTROL_ID'] for row in state['resources'])==set(state['limits'])
 supported=set(re.findall(r'^\s+(--[a-z0-9-]+)',(OUT/'installed-bwrap-help.txt').read_text(),re.M))
 flags={x for x in state['argv'] if x.startswith('--')};assert flags<=supported,'unsupported flag'
 assert '--unshare-net' in flags and '--share-net' not in flags,'network isolation'
 assert state['writable_repository'] is False and state['writable_stopped_journal'] is False and state['real_inputs'] is False,'protected inputs'
 assert state['descendant_policy']=='UNQUALIFIED_REQUIRED' and state['cumulative_write_policy']=='UNQUALIFIED_REQUIRED','unbounded processes or bytes'
 assert state['probe_executed'] is False and state['campaign_execution_ready'] is False and state['H77_A15_scope'] is False,'premature execution'
 assert state['options']==[],'incomplete selectable decision'
 return {'RESULT':'PARTIAL','READ_ONLY_HOST_INVENTORY_COMPLETE':'NO','ENFORCEMENT_DESIGN_COMPLETE':'NO','HOST_CONTROL_PROCEDURE_COMPLETE':'NO','HOST_CONTROLS_VERIFIED':'NO','FILESYSTEM_CONFINEMENT_VERIFIED':'NO','RESOURCE_ENFORCEMENT_VERIFIED':'NO','CONTROLLER_HOST_BINDING_COMPLETE':'NO','HOST_CONTROL_TEST_DECISION_READY':'NO','SYNTHETIC_CAMPAIGN_DECISION_READY':'NO','SYNTHETIC_CAMPAIGN_EXECUTION_READY':'NO'}
def reconstruct():
 old=OUT.parent/'executable-oracle-controller-closure-84';index=load(old/'evidence-index.json')
 for path,sha in {**index['FILES'],**index['CURRENT_SOURCE']}.items():assert digest(ROOT/path)==sha
 src=ROOT/'adapter/tests/test_h77_02_launch_gate.py';tree=ast.parse(src.read_text());cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='GateSyntheticTests');assert len([n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')])==18
 oracle=load(old/'independent-executable-oracle-specification.json');assert sum(len(m['slots']) for t in oracle['tests'].values() for m in t['operation_comparisons'].values())==39
 ref=load(OUT.parent/'gate-construction-grant-80/effective-gate-construction-grant-reference.json');assert ref['GRANT_EFFECTIVE'] is True and digest(ROOT/ref['GRANT_RECORD_PIN']['PATH'])==ref['GRANT_RECORD_PIN']['RAW_SHA256']
 grant=load(ROOT/ref['GRANT_RECORD_PIN']['PATH']);assert hashlib.sha256(canonical(grant['RECORD'])).hexdigest()==ref['GRANT_IDENTITY']['sha256']
 matrix=load(OUT/'resource-enforcement-matrix.json');assert matrix['LIMITS']==grant['RECORD']['RESOURCE_LIMITS']
 context=load(OUT/'read-only-managed-context-observations.json');fs=load(OUT/'filesystem-network-confinement-specification.json');subject=load(OUT/'proposed-host-control-authorization-subject.json');steps=load(OUT/'host-control-verification-procedure.json');assert len(steps['STEPS'])==14 and all(s['EXECUTABLE_BINDING'] is None for s in steps['STEPS'])
 state={'test_source':digest(src),'managed_context':context['CONTEXT'],'resources':matrix['ROWS'],'limits':matrix['LIMITS'],'argv':fs['FIXED_BWRAP_PREFIX_ARGV'],'writable_repository':fs['WRITABLE_REPOSITORY'],'writable_stopped_journal':False,'real_inputs':False,'descendant_policy':'UNQUALIFIED_REQUIRED','cumulative_write_policy':'UNQUALIFIED_REQUIRED','probe_executed':False,'campaign_execution_ready':False,'H77_A15_scope':False,'options':subject['DECISION_OPTIONS']}
 result=classify(state)
 negatives=[]
 mutants=[('wrong source hash','test_source','0'*64),('Codex substituted for direct shell','managed_context','DIRECT_HOST_VERIFIED'),('unsupported bwrap option','argv',state['argv']+['--unsupported85']),('network disabled','argv',[x for x in state['argv'] if x!='--unshare-net']),('repository writable','writable_repository',True),('stopped journal writable','writable_stopped_journal',True),('real checkpoint input','real_inputs',True),('unbounded descendants','descendant_policy','COUNTER_ONLY_QUALIFIED'),('missing cumulative-byte enforcement','cumulative_write_policy','QUOTA_ONLY_QUALIFIED'),('unauthorized probe','probe_executed',True),('premature campaign','campaign_execution_ready',True),('actual H77 or A15 scope','H77_A15_scope',True),('unverified control qualified','resources',[dict(r,CURRENT_STATUS='VERIFIED') for r in state['resources']]),('automatic retry','limits',dict(state['limits'],RETRIES=1))]
 for name,key,value in mutants:
  mutation=copy.deepcopy(state);mutation[key]=value
  try:classify(mutation)
  except AssertionError:negatives.append({'CONTROL':name,'RESULT':'REJECTED'})
  else:raise AssertionError('negative accepted: '+name)
 reconstruction={'ENTRY_AUTHENTICATED':True,'ORIGINAL_TESTS':18,'ORACLE_SLOTS':39,'GRANT_IDENTITY':ref['GRANT_IDENTITY'],'PACKAGE84_ORACLE_IDENTITY':oracle['identity'],'HOST_INPUT_RECORD_SHA256':digest(OUT/'direct-host-profile.json'),'SOURCE_SHA256':digest(src),'READINESS':result,'NEGATIVES':negatives,'PROBES_OR_TESTS_EXECUTED':0}
 reconstruction['SEMANTIC_IDENTITY']={'kind':'CONTENT_IDENTITY','namespace':'qualification-h85-independent-reconstruction-v1','sha256':hashlib.sha256(canonical(reconstruction)).hexdigest()}
 return reconstruction
if __name__=='__main__':print(json.dumps(reconstruct(),sort_keys=True))
