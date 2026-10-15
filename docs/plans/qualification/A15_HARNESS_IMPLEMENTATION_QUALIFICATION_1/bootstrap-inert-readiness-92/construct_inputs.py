"""Static documentary encoder. No target imports, stores, callbacks or launches."""
import ast, hashlib, json, os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]; OUT=Path(__file__).resolve().parent
BASE=OUT.parent; OLD=BASE/'bootstrap-trust-authority-89'; P91=BASE/'minimal-bootstrap-construction-91'
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def ident(v,ns):return {'kind':'CONTENT_IDENTITY','namespace':ns,'sha256':hashlib.sha256(canon(v)).hexdigest()}
def seal(v,ns):return {'CONTENT':v,'IDENTITY':ident(v,ns)}
def read(p):return json.loads(p.read_text())
def save(n,v):(OUT/n).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def pin(p):return {'path':str(p.relative_to(ROOT)),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
subject=read(OLD/'proposed-construction-test-authority-subject.json');spec=read(OLD/'inert-synthetic-qualification-specification.json')
limits=subject['RESOURCE_LIMITS'];paths=subject['EXACT_SOURCE_PATHS'];test_text=(ROOT/paths[1]).read_text();tree=ast.parse(test_text)
locations={n.name:n.lineno for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)}
retained=ident({'purpose':'synthetic retained subject marker, not Package86','package':92},'bootstrap-inert-retained-subject-v1')
command={'operation':'INERT_CALLBACK','argv':[]};command_id=ident(command,'bootstrap-inert-command-v1')
crashes=['BEFORE_CLAIM','DURING_CLAIM','AFTER_CLAIM_BEFORE_LAUNCH','DURING_LAUNCH','AFTER_LAUNCH_BEFORE_OBSERVATION','AFTER_COMPLETION_BEFORE_AUDIT']
F={'directory':False};D={'directory':True}
def event(name,v):return {'event':name,'value':v}
def stage(p):return event('stage',{'point':p})
fixtures=[];oracles=[];inventory=[]
for test in spec['TESTS']:
 tid=test['TEST_ID'];short=tid[4:]
 variants=['first','primary'] if short in ('DUPLICATE_CONSUMPTION','ZERO_RETRIES') else crashes if short=='CRASH_AFTER_CONSUMPTION' else ['primary']
 inputs=[];ops=[]
 for variant in variants:
  context={'schema':'BOOTSTRAP-SYNTHETIC-CONTEXT-92-1','test_id':tid,'variant':variant if short=='CRASH_AFTER_CONSUMPTION' else 'shared','mode':'INERT','network':'NO_NETWORK_APIS','physical_paths_excluded_from_identity':True}
  context_id=ident(context,'bootstrap-inert-context-v1')
  synth_subject=ident({'test_id':tid,'scope':'INERT_CALLBACK_ONLY'},'bootstrap-inert-subject-v1')
  grant_body={'schema':'BOOTSTRAP-SYNTHETIC-GRANT-1','subject_identity':synth_subject,'retained_identity':retained,'command_identity':command_id,'context_identity':context_id,'issuer':'SYNTHETIC_ONLY_NOT_PROJECT_AUTHORITY','scope':'INERT_CALLBACK','limits':limits,'attempts':1,'retries':0}
  grant={'content':grant_body,'identity':ident(grant_body,'bootstrap-inert-grant-v1')}
  key_body={'schema':'SYSTEM-PIDS-SINGLE-ATTEMPT-KEY-1','issued_grant_identity':grant['identity'],'approved_probe_subject_identity':synth_subject,'retained_package86_subject_identity':retained,'exact_command_identity':command_id,'qualified_execution_context_identity':context_id,'authorized_attempt_number':1}
  key=ident(key_body,'qualification-h87-system-probe-consumption-key-v1')
  epoch={'schema':'BOOTSTRAP-INERT-EPOCH-1','grant_identity':grant['identity'],'status':'REVOKED' if short=='REVOCATION' else 'EFFECTIVE','expiration_checked':True,'freshness_verified':True}
  eff={'schema':'BOOTSTRAP-SYNTHETIC-EFFECTIVE-1','grant_identity':grant['identity'],'effective':True}
  assigned_command=dict(command);assigned_limits=dict(limits)
  if short=='COMMAND_REJECTION':assigned_command={'operation':'INERT_CALLBACK','argv':['UNAPPROVED_INERT_ARGUMENT']}
  if short=='GRANT_REJECTION':eff['grant_identity']=ident({'wrong_synthetic_grant':tid},'bootstrap-inert-grant-v1')
  if short=='RESOURCE_MISMATCH':assigned_limits['CHILD_CPU_SECONDS']=4
  point='DURING_CLAIM' if short=='PARTIAL_RECORD' else 'AFTER_CLAIM_BEFORE_LAUNCH' if short=='CRASH_BEFORE_LAUNCH' else 'AFTER_LAUNCH_BEFORE_OBSERVATION' if short=='UNKNOWN_COMPLETION' else variant if short=='CRASH_AFTER_CONSUMPTION' else None
  fault={'point':point,'kind':'controlled_process_exit_77' if short=='CRASH_AFTER_CONSUMPTION' else 'InertFailure' if point else 'callback_exception' if short=='LAUNCH_FAILURE' or (short=='ZERO_RETRIES' and variant=='first') else 'audit_publication_exception' if short=='AUDIT_FAILURE' else 'validation_mutation' if short in ('COMMAND_REJECTION','GRANT_REJECTION','RESOURCE_MISMATCH','REVOCATION') else 'none'}
  relative='cases/'+tid+('/'+variant if short=='CRASH_AFTER_CONSUMPTION' else '')+'/store'
  basis={'SCHEMA_VERSION':'BOOTSTRAP-INERT-FIXTURE-92-1','TEST_ID':tid,'VARIANT':variant,'SYNTHETIC_GRANT':grant,'SYNTHETIC_SUBJECT_IDENTITY':synth_subject,'SYNTHETIC_COMMAND':assigned_command,'SYNTHETIC_COMMAND_IDENTITY':ident(assigned_command,'bootstrap-inert-command-v1'),'SYNTHETIC_EXECUTION_CONTEXT':context,'CONSUMPTION_KEY':key,'CONSUMPTION_KEY_CONTENT':key_body,'FAULT_CONFIGURATION':fault,'EPOCH':epoch,'EFFECTIVE_SYNTHETIC_REFERENCE':eff,'ASSIGNED_LIMITS':assigned_limits,'RELATIVE_STORE_PATH':relative,'PROVENANCE':{'governing_contract':pin(OLD/'one-attempt-consumption-contract.json'),'test_specification':pin(OLD/'inert-synthetic-qualification-specification.json'),'derivation':'Independent JSON construction, no target execution'}}
  input_id=ident(basis,'bootstrap-inert-input-v1')
  cb_fail=short=='LAUNCH_FAILURE' or (short=='ZERO_RETRIES' and variant=='first')
  rejection={'COMMAND_REJECTION':'COMMAND_OR_RESOURCE_MISMATCH','GRANT_REJECTION':'EFFECTIVE_GRANT_IDENTITY','RESOURCE_MISMATCH':'COMMAND_OR_RESOURCE_MISMATCH','REVOCATION':'REVOKED_EXPIRED_OR_UNKNOWN'}.get(short)
  claim_body={'schema':'BOOTSTRAP-CONSUMPTION-1','key':key_body,'state':'CONSUMED'}
  claim={'content':claim_body,'identity':ident(claim_body,'bootstrap-inert-consumption-record-v1')}
  records={};events=[];barriers=[];confirmation=[];result=None;failure=None;count=0;audits=[]
  def audit(phase,value):
   doc={'schema':'BOOTSTRAP-AUDIT-1','key':key,'phase':phase,'value':value}
   records[key['sha256']+'.'+phase+'.json']=canon(doc).hex();audits.append(doc)
  def fail(error_type,message,secondary=()):
   nonlocal_dummy=None
   cause={'type':error_type,'message':message}
   return cause,{'type':error_type,'message':message,'first':cause,'secondary':list(secondary)}
  complete=True;unknown=[]
  if rejection:
   cause,failure=fail('BootstrapError',rejection)
   events=[event('first_failure',{'first':cause,'secondary':[],'retry_allowed':False})];state='UNCLAIMED'
  elif short in ('DUPLICATE_CONSUMPTION','ZERO_RETRIES') and variant=='primary':
   state='CONSUMED'
   records=dict(ops[-1]['CONTENT']['EXPECTED_DURABLE_RECORD'])
   events=[stage('BEFORE_CLAIM')];barriers=[F]
   message=str(FileExistsError(17,os.strerror(17),key['sha256']+'.claim.json'))
   cause,failure=fail('FileExistsError',message)
   events.append(event('first_failure',{'first':cause,'secondary':[],'retry_allowed':False}))
  elif short=='CRASH_AFTER_CONSUMPTION':
   count=1 if variant in ('AFTER_LAUNCH_BEFORE_OBSERVATION','AFTER_COMPLETION_BEFORE_AUDIT') else 0
   state='UNCLAIMED' if variant=='BEFORE_CLAIM' else 'OUTCOME_UNKNOWN' if variant=='DURING_CLAIM' else 'CONSUMED'
   if variant!='BEFORE_CLAIM':records[key['sha256']+'.claim.json']='' if variant=='DURING_CLAIM' else canon(claim).hex()
   if variant in ('DURING_LAUNCH','AFTER_LAUNCH_BEFORE_OBSERVATION','AFTER_COMPLETION_BEFORE_AUDIT'):
    audit('consumed',{'identity':claim['identity']});audit('attempt',{'attempt':1})
   crash={'point':variant,'callback_count':count,'retry_count':0};records['crash-witness.json']=canon(crash).hex()
   events=[{'independent_parent_exit':77,'controlled_crash':True,**crash}]
  else:
   state='OUTCOME_UNKNOWN' if short=='PARTIAL_RECORD' else 'CONSUMED'
   records[key['sha256']+'.claim.json']='' if short=='PARTIAL_RECORD' else canon(claim).hex()
   events=[stage('BEFORE_CLAIM'),stage('DURING_CLAIM')];barriers=[F]
   if short=='PARTIAL_RECORD':
    events.append(event('independent.fault',{'point':point}));cause,failure=fail('InertFailure','INERT_FAULT:'+point)
   else:
    barriers += [F,D];confirmation=[claim['identity']];events.append(stage('AFTER_CLAIM_BEFORE_LAUNCH'))
    if short=='CRASH_BEFORE_LAUNCH':
     events.append(event('independent.fault',{'point':point}));cause,failure=fail('InertFailure','INERT_FAULT:'+point)
    else:
     barriers += [F];events.append(event('consumption.confirmed',{'identity':claim['identity'],'key':key}))
     if short=='AUDIT_FAILURE':
      cause,failure=fail('InertFailure','INERT_AUDIT_FAILURE',[{'type':'InertFailure','message':'INERT_AUDIT_FAILURE'}])
      events += [event('independent.audit.failure',{'name':key['sha256']+'.consumed.json'}),event('independent.audit.failure',{'name':key['sha256']+'.unknown.json'})]
     else:
      for phase,value in [('consumed',{'identity':claim['identity']}),('attempt',{'attempt':1})]:audit(phase,value);barriers += [F,F,D]
      events += [stage('DURING_LAUNCH'),event('callback.entry',{'attempt':1,'arguments':[]}),event('independent.callback.entry',{'arguments':[],'order':1})];count=1
      if cb_fail:
       cause,failure=fail('InertFailure','INERT_CALLBACK_FAILURE')
       events += [event('independent.callback.exception',cause),event('callback.exception',cause)]
      else:
       events += [event('independent.callback.return',{'value':{'inert':True}}),event('callback.return',{'value':{'inert':True}}),stage('AFTER_LAUNCH_BEFORE_OBSERVATION')]
       if short=='UNKNOWN_COMPLETION':
        events.append(event('independent.fault',{'point':point}));cause,failure=fail('InertFailure','INERT_FAULT:'+point)
       else:
        events += [event('completion.observed',{'value':{'inert':True},'synthetic':True}),stage('AFTER_COMPLETION_BEFORE_AUDIT')]
        audit('completed',{'value':{'inert':True}});barriers += [F,F,D]
        result={'schema':'BOOTSTRAP-INERT-RESULT-1','key':key,'consumption':claim['identity'],'consumed':True,'outcome':{'inert':True},'retry_allowed':False}
   if failure:
    if short!='AUDIT_FAILURE':
     audit('unknown',{'state':'CONSUMED_OUTCOME_UNKNOWN','first':failure['first'],'retry_allowed':False});barriers += [F,F,D]
    events.append(event('first_failure',{'first':failure['first'],'secondary':failure['secondary'],'retry_allowed':False}))
   if short=='CONCURRENT_CLAIMS':
    # Both precise losing branches are independently derived below; scheduling is not fixed.
    pass
  observation={'result':result,'failure':failure,'events':events,'callback_count':count,'barriers':barriers,'confirmations':confirmation,'records':records,'retry_count':0}
  recovery={'state':'OUTCOME_UNKNOWN' if state in ('UNCLAIMED','OUTCOME_UNKNOWN') else 'CONSUMED','launch_permitted':False,'retry_allowed':False}
  oracle={'SCHEMA_VERSION':'BOOTSTRAP-INDEPENDENT-ORACLE-92-1','INPUT_IDENTITY':input_id,'TEST_ID':tid,'VARIANT':variant,'EXPECTED_CLAIM_RESULT':'REJECTED' if rejection or (short in ('DUPLICATE_CONSUMPTION','ZERO_RETRIES') and variant=='primary') else 'PARTIAL_RESERVED' if short=='PARTIAL_RECORD' else 'ONE_CLAIM_OR_DECLARED_CRASH', 'EXPECTED_CONSUMPTION_STATE':state,'EXPECTED_DURABLE_RECORD':records,'EXPECTED_CALLBACK_COUNT':{'maximum':1,'aggregate_exact':1,'winner':'UNDETERMINED_BY_DESIGN'} if short=='CONCURRENT_CLAIMS' else count,'EXPECTED_CALLBACK_ORDER':events,'EXPECTED_FAILURE_CLASS':failure['type'] if failure else 'CONTROLLED_EXIT_77' if short=='CRASH_AFTER_CONSUMPTION' else None,'EXPECTED_FIRST_COUNTEREXAMPLE':failure['first'] if failure else None,'EXPECTED_SECONDARY_FAILURES':failure['secondary'] if failure else [],'EXPECTED_RETRY_ELIGIBILITY':False,'EXPECTED_AUDIT_EVIDENCE':audits,'EXPECTED_RECOVERY':recovery,'SOURCE_OBSERVATION_VECTOR':observation,'COMPARISON_RULE':'Exact canonical bytes/semantic fields where determined. Concurrent aggregate invariants and independently bound per-run observations; no scheduling normalization.','ORACLE_COMPLETENESS':'COMPLETE_STATIC_VARIANT' if complete else 'PARTIAL','UNBOUND_FIELDS':unknown,'DERIVATION_RULE':'Package89 irreversible consumption plus Package91 AST-observed phase, callback and publication ordering. This encoder does not execute those operations.','ADAPTER_OUTPUT_USED':False}
  oracle['EXCEPTION_FORMAT_ENTRY_RULE']='Before any future target call independently verify pinned interpreter/libc exception-format profile exactly matches this sealed metadata. Unknown/different format blocks; no target output may fill expectations.'
  oracle['CONCURRENT_COMPARISON']=None
  if short=='CONCURRENT_CLAIMS':
   alternatives=[]
   for error_type,message,bars,stages in [('BlockingIOError',str(BlockingIOError(11,os.strerror(11))),[],[]),('FileExistsError',str(FileExistsError(17,os.strerror(17),key['sha256']+'.claim.json')),[F],[stage('BEFORE_CLAIM')])]:
    cause,err=fail(error_type,message)
    alternatives.append({'result':None,'failure':err,'events':stages+[event('first_failure',{'first':cause,'secondary':[],'retry_allowed':False})],'callback_count':0,'barriers':bars,'confirmations':[],'retry_count':0})
   winner={k:v for k,v in observation.items() if k!='records'}
   oracle['CONCURRENT_COMPARISON']={'WINNERS_EXACT':1,'CALLBACKS_EXACT':1,'LOSER_FAILURES':[a['failure'] for a in alternatives],'ACCEPTED_HELPER_VECTORS':[winner]+alternatives,'EXPECTED_FINAL_RECORDS':records,'PER_RUN_SNAPSHOT_RULE':'Retain exact raw helper JSON hash, actor PID and parent exit observations. Snapshot filenames must be a subset of EXPECTED_FINAL_RECORDS and bytes an exact prefix of that file canonical final byte string; empty is allowed only during exclusive incomplete publication. Winner snapshot must equal complete final records. Do not compare winner PID or scheduling to a fabricated constant.','CURRENT_SOURCE_GAP':'Existing tests retain per-run snapshots but omit prefix/subset validation; independently qualified observer or approved source repair required.'}
  oracle_seal=seal(oracle,'bootstrap-inert-oracle-v1');ops.append(oracle_seal)
  body={'INPUT':basis,'INPUT_IDENTITY':input_id,'EXPECTED_ORACLE_IDENTITY':oracle_seal['IDENTITY'],'RUNTIME_BINDING':'Future independently sealed exact request: mode INERT; schema BOOTSTRAP-INERT-REQUEST-1; grant/effective/context/command/limits/epoch from this INPUT; test_id exact; fixture_id variant identity below; attempt 1; store absolute campaign-root + RELATIVE_STORE_PATH; store_device/store_inode observed after permitted creation, never invented.'}
  inputs.append(seal(body,'bootstrap-inert-runtime-fixture-v1'))
 oracle_case=seal({'TEST_ID':tid,'VARIANTS':ops,'ORACLE_COMPLETENESS':'COMPLETE' if all(o['CONTENT']['ORACLE_COMPLETENESS']=='COMPLETE_STATIC_VARIANT' for o in ops) else 'PARTIAL','NOT_ACTIVE_TEST_EVIDENCE':True},'bootstrap-inert-case-oracle-v1')
 fixture_case=seal({'SCHEMA_VERSION':'BOOTSTRAP-INERT-CASE-FIXTURE-92-1','TEST_ID':tid,'VARIANTS':inputs,'EXPECTED_ORACLE_IDENTITY':oracle_case['IDENTITY'],'SHARED_GRANT_RULE':'first and primary intentionally reuse same synthetic grant/key/store; first consumes, duplicate must reject' if short in ('DUPLICATE_CONSUMPTION','ZERO_RETRIES') else 'two concurrent actors share one synthetic grant/key/store' if short=='CONCURRENT_CLAIMS' else 'crash variants have distinct grants/keys/stores' if short=='CRASH_AFTER_CONSUMPTION' else 'one isolated synthetic grant/key/store','PROVENANCE':pin(OLD/'inert-synthetic-qualification-specification.json')},'bootstrap-inert-case-fixture-v1')
 fixtures.append(fixture_case);oracles.append(oracle_case)
 inventory.append({'TEST_ID':tid,'SOURCE_LOCATION':paths[1]+':'+str(locations['test_'+short]),'TEST_PURPOSE':test['SYNTHETIC_INPUT_RULE'],'FIXTURE_IDENTITY':fixture_case['IDENTITY'],'ORACLE_IDENTITY':oracle_case['IDENTITY'],'EXPECTED_RESULT':test['EXPECTED_RESULT'],'PROCESS_EFFECTS':'two fixed helpers' if short=='CONCURRENT_CLAIMS' else 'six fixed crash helpers' if short=='CRASH_AFTER_CONSUMPTION' else 'restart helper' if short=='DUPLICATE_CONSUMPTION' else 'parent inert operation','RESOURCE_REQUIREMENTS':limits,'CURRENT_READINESS':'BLOCKED_NO_CAMPAIGN_ENTRY'})
fixture_manifest=seal({'SCHEMA':'BOOTSTRAP-FIXTURE-MANIFEST-92-1','FIXTURES':fixtures,'CASE_COUNT':14,'RUNTIME_VARIANT_COUNT':sum(len(x['CONTENT']['VARIANTS']) for x in fixtures),'REAL_INPUTS_USED':False},'bootstrap-inert-fixture-manifest-v1')
oracle_manifest=seal({'SCHEMA':'BOOTSTRAP-ORACLE-MANIFEST-92-1','ORACLES':oracles,'CASE_COUNT':14,'DERIVED_WITHOUT_TARGET_IMPORT_OR_EXECUTION':True,'COMPLETE_CASES':sum(x['CONTENT']['ORACLE_COMPLETENESS']=='COMPLETE' for x in oracles)},'bootstrap-inert-oracle-manifest-v1')
save('exception-format-profile.json',{'INTERPRETER_BINARY_PIN':{'path':'/usr/bin/python3.8','raw_sha256':hashlib.sha256(Path('/usr/bin/python3.8').read_bytes()).hexdigest()},'STRERROR_11':os.strerror(11),'STRERROR_17':os.strerror(17),'DERIVATION':'Construct Python exception values from normative errno/filename, then encode. No flock, exclusive creation, coordinator or test ran. Actual future formatter match remains fail-closed entry condition.'});save('sealed-synthetic-fixture-manifest.json',fixture_manifest);save('independent-oracle-manifest.json',oracle_manifest);save('fourteen-test-inventory.json',inventory)
print(json.dumps({'logical_fixtures':14,'runtime_variants':fixture_manifest['CONTENT']['RUNTIME_VARIANT_COUNT'],'complete_case_oracles':oracle_manifest['CONTENT']['COMPLETE_CASES'],'fixture_manifest_identity':fixture_manifest['IDENTITY'],'oracle_manifest_identity':oracle_manifest['IDENTITY']},sort_keys=True))
