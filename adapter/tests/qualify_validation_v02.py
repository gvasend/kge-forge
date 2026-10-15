"""Reproducible V02 qualification and bounded authorized configuration publication."""
import hashlib,json,os,shutil,subprocess,sys,unittest
from pathlib import Path
from dataclasses import replace,is_dataclass,fields
from unittest.mock import patch
from adapter.planner import codec as c,model as m,installation as i,validation_transaction as vt,validation_installation as vi,evidence_transaction as tx,evidence_attestation as ea,core,gates
from adapter.tests import test_planner_validation_support as tests
R=Path(__file__).resolve().parents[2];D=R/'docs/plans';Q=D/'qualification/VALIDATION_V01_1';O=D/'qualification/VALIDATION_V02_1'

def computation_wire(snapshot):
 def witness(x):
  if is_dataclass(x) and type(x).__name__ not in c.TYPES:
   return {'type':type(x).__name__,**{f.name:witness(getattr(x,f.name)) for f in fields(x)}}
  if type(x) is tuple:return [witness(z) for z in x]
  if type(x) is dict:return {k:witness(v) for k,v in x.items()}
  return c._wire(x)
 return witness(core.recompute(snapshot))

def emit(name,obj):
 (O/name).write_bytes(c.canonical_bytes(obj))
def hashes():return {str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((R/'adapter/planner').glob('*.py'))}
def fresh(checkpoints):
 program='''from pathlib import Path
import json,sys
from unittest.mock import patch
from adapter.planner import codec as c,model as m,validation_transaction as vt,core,installation as i
from adapter.tests.qualify_validation_v02 import computation_wire
x=json.loads(Path(sys.argv[1]).read_text());out=[]
with patch.object(vt,'assess',side_effect=AssertionError('replay must not decide')):
 for t in x:
  b=c.restore(Path(t['path']),c._unwire(t['bundle_id']),Path(t['root']))
  assert c._wire(c.snapshot_id(b.current))==t['state_id']
  assert computation_wire(b.current)==t['computation']
  assert sorted(c._wire(b.sources),key=c.canonical_bytes)==t['sources']
  assert c._wire(b.events)==t['events']
  assert all(i.current(b,r) for r in b.current.installed_definitions)
  out.append(t['name'])
print(json.dumps(out))'''
 path=O/'reader-manifest.json';path.write_bytes(c.canonical_bytes(checkpoints));results=[]
 for seed in ('0','1','7','101'):
  for repeat in range(3):
   proc=subprocess.run([sys.executable,'-c',program,str(path)],env=dict(os.environ,PYTHONHASHSEED=seed,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(R)),text=True,capture_output=True)
   if proc.returncode:raise AssertionError(proc.stderr)
   results.append({'seed':seed,'reader':repeat,'checks':json.loads(proc.stdout),'result':'PASS'})
 emit('fresh-readers.json',results);return results

def qualification(readers=True):
 starting_hashes=hashes()
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(tests.ValidationSupportTests)
 # Retain the independently authored roots while exercising the same public APIs.
 saved={}
 oldtear=tests.ValidationSupportTests.tearDownClass
 def retain():
  for name,data in [('accepted',tests.ValidationSupportTests.positive),('rejected',tests.ValidationSupportTests.negative)]:
   h,b,r,installed,x,received,cmd=data
   a,post=vt.prepare(received,cmd,h.root)
   end,bid,_=vt.commit(received,a,h.root/'qualified-validation',h.root)
   target=O/('generic-'+name)
   if not target.exists():shutil.copytree(h.root,target)
   else:
    for p in h.root.rglob('*'):
     if p.is_file():
      dest=target/p.relative_to(h.root);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes())
   saved[name]=(target,installed,received,end,bid,a)
  oldtear()
 tests.ValidationSupportTests.tearDownClass=staticmethod(retain)
 with (O/'generic-tests.log').open('w') as stream:result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
 assert result.wasSuccessful(),(O/'generic-tests.log').read_text()
 checkpoints=[]
 for name,(root,installed,received,end,bid,a) in saved.items():
  for boundary,b in [('installed',installed),('received',received),('validated',end)]:
   path=root/(boundary+'.json');c.save_bundle(b,root,root);path.write_bytes(c.bundle_bytes(b))
   checkpoints.append({'name':name+'-'+boundary,'path':str(path),'root':str(root),'bundle_id':c._wire(c.bundle_id(b)),'state_id':c._wire(c.snapshot_id(b.current)),'computation':computation_wire(b.current),'sources':sorted(c._wire(b.sources),key=c.canonical_bytes),'events':c._wire(b.events)})
  emit(name+'-validation-event.json',c._wire(a))
 emit('reader-manifest.json',checkpoints)
 if not readers:
  assert hashes()==starting_hashes,'runtime changed during qualification'
  emit('writer-qualification.json',{'RESULT':'WRITER_TESTS_PASS_READERS_PENDING','tests_run':result.testsRun,'runtime_hashes':starting_hashes,'writer_pid':os.getpid()})
  print('WRITER_TESTS_PASS_READERS_PENDING',flush=True)
  return
 readers=fresh(checkpoints)
 assert hashes()==starting_hashes,'runtime changed during qualification'
 result={'RESULT':'PASS','tests_run':result.testsRun,'generic_fixture_types':['TEST-SEMANTIC-PAYLOAD-1 PASS','TEST-SEMANTIC-PAYLOAD-1 authorized semantic FAIL'],'fresh_reader_processes':len(readers),'fresh_reader_comparisons':sum(len(z['checks']) for z in readers),'runtime_hashes':hashes(),'capability':'PASS','adapter':'PASS','replay_validator_invocations':0}
 emit('generic-qualification.json',result)
 print(json.dumps(result),flush=True)

def qualification_read():
 prior=c.parse_json((O/'writer-qualification.json').read_bytes())
 assert prior['RESULT']=='WRITER_TESTS_PASS_READERS_PENDING' and prior['runtime_hashes']==hashes()
 checks=c.parse_json((O/'reader-manifest.json').read_bytes());readers=fresh(checks)
 result={'RESULT':'PASS','tests_run':prior['tests_run'],'runtime_hashes':hashes(),'capability':'PASS','adapter':'PASS','fresh_reader_processes':len(readers),'fresh_reader_comparisons':sum(len(x['checks']) for x in readers),'writer_terminated_before_reads':True,'replay_validator_invocations':0,'generic_fixture_types':['TEST semantic PASS','independent bound TEST semantic FAIL']}
 emit('generic-qualification.json',result);print(json.dumps(result),flush=True)

def authorize():
 sealed=c.parse_json((Q/'closure-seal.json').read_bytes())
 assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in sealed['artifacts'].items())
 dossier=c.parse_json((Q/'p04-installation-decision-dossier.json').read_bytes());grant=copy_json(dossier['grant_blueprint'])
 capture={'schema':'VALIDATION-V02-HUMAN-SELECTION-1','selected_option':'AUTHORIZE_P04_A10_VALIDATION_INSTALLATION','issuer':'AUTHENTICATED_HUMAN_USER','issuer_role':'QUALIFICATION_AUTHORITY','authentication':'EXPLICIT_CURRENT_SESSION_HUMAN_DECISION_TRANSPORT','decision_subject':dossier['decision_subject'],'V01_contract':i.simple(c._identity((D/'DETERMINISTIC_PLANNER_V0_1_VALIDATION_V01_A10_CONTRACT.json').read_bytes(),'raw-file-sha256')),'bounded_members':dossier['bounded_members'],'definition_set':grant['definition_id'],'content':grant['content_id'],'contract':grant['contract_id'],'scope':grant['scope'],'lineage':grant['lineage'],'generation':grant['generation'],'consumer':grant['subject']['consumer'],'operation':'INSTALL','pre_bundle':grant['pre_bundle'],'pre_state':grant['pre_state'],'parent_event':grant['parent_event'],'policy':grant['policy'],'policy_version':grant['policy_version'],'expected_install_sequence':6,'transport_date':'2026-10-04','provenance':'Explicit user decision in this session; not inferred from earlier route/ATTEST permissions','excludes':['A09 execution','A10 execution','ValidationResult','support instance','proof admission','unrelated installation']}
 emit('authenticated-selection.json',capture);decision=c._identity(c.canonical_bytes(capture),'raw-file-sha256');grant.update(decision_id=i.simple(decision),provenance=i.simple(decision))
 aid=i.digest(grant,'planner-install-authority-v1',m.IdentityKind.AUTHORITY_IDENTITY)
 authority=i.admit_authority(grant,expected_grant=aid,expected_decision=decision,trusted_issuer='QUALIFICATION_AUTHORITY',receipt_path=str((O/'install-authority-admission.json').relative_to(R)))
 emit('authorization.json',{'authentication':'PASS','authority_id':c._wire(aid),'decision_id':c._wire(decision),'authority':c._wire(authority),'grant':grant,'seal_verified':True})
 return authority,decision,dossier

def copy_json(x):return c.parse_json(c.canonical_bytes(x))
def application():
 qualified=c.parse_json((O/'generic-qualification.json').read_bytes());assert qualified['RESULT']=='PASS' and qualified['runtime_hashes']==hashes()
 authority,decision,dossier=authorize();g=dossier['grant_blueprint']
 b=c.restore(D/'DETERMINISTIC_PLANNER_V0_1_E2_P04_POST_ATTEST_INSTALL_BUNDLE_1.json',c._unwire(g['pre_bundle']),R)
 assert c._wire(c.snapshot_id(b.current))==g['pre_state'] and c._wire(b.events[-1].identity)==g['parent_event']
 dd=c.parse_json((Q/'p04-definition-set-descriptor.json').read_bytes());raw=(Q/'p04-definition-set.json').read_text()
 p=m.Provenance(dd['source_pin']['path'],i.identity(dd['content_id']),'/',raw,dd['provenance']['method'],dd['scope'])
 defn=m.InstallableDefinition(i.identity(g['definition_id']),c.canonical_bytes(dd).decode(),p)
 extra=[]
 for name in ('generic-validation-support-protocol.json','p04-semantic-native-binding-template.json'):
  path=Q/name;z=path.read_bytes();extra.append(m.Provenance(str(path.relative_to(R)),c._identity(z,'raw-file-sha256'),'/',z.decode(),'VALIDATION-V01-SEALED-SOURCE',g['scope']))
 path=D/'qualification/E2_P04_CONTINUATION_INPUT_CLOSURE_1/semantic-payload.json';z=path.read_bytes();extra.append(m.Provenance(str(path.relative_to(R)),c._identity(z,'raw-file-sha256'),'/',z.decode(),'VALIDATION-V01-SEALED-SOURCE',g['scope']))
 request=m.InstallDefinition('INSTALL_DEFINITION',1,vt.ZERO,c.bundle_id(b),c.snapshot_id(b.current),b.events[-1].identity,6,defn,authority,m.InstallationOperation.INSTALL,None,b.policy,b.policy_version,(),(),tuple(extra))
 request=replace(request,source_additions=tuple(m.ArtifactPin(z.path,z.identity) for z in i.request_provenances(request) if m.ArtifactPin(z.path,z.identity) not in b.sources));request=replace(request,command_key=i.command_key(request))
 i.validate_authority(request,b.current.context)
 assert all(i.grant_fields(request)[k]==v for k,v in g.items() if k in i.grant_fields(request))
 after,bid,no=i.commit(b,request,O/'p04-install-store',R,expected_authority=authority.id,expected_decision=decision)
 assert not no or c.bundle_id(after)==bid
 output=D/'DETERMINISTIC_PLANNER_V0_1_E2_P04_POST_A10_INSTALL_BUNDLE_1.json';c.save_bundle(after,D,R);output.write_bytes(c.bundle_bytes(after))
 cold=c.restore(output,bid,R)
 installed_record=next(z for z in cold.current.installed_definitions if z.id==i.installed_id(request))
 assert c.bundle_bytes(cold)==c.bundle_bytes(after) and i.current(cold,installed_record)
 replay_prefix=c._prefix_bundle(cold,5)
 assert c.bundle_bytes(replay_prefix)==c.bundle_bytes(b) and not replay_prefix.current.validation_contracts
 independent,independent_id,_=i.commit(b,request,O/'independent-p04-install-store',R,expected_authority=authority.id,expected_decision=decision)
 assert independent_id==bid and c.bundle_bytes(independent)==c.bundle_bytes(after)
 retry,retry_id,noop=i.commit(b,request,O/'p04-install-store',R,expected_authority=authority.id,expected_decision=decision)
 assert noop and retry_id==bid and len(retry.events)==6
 assert not cold.current.validation_results and not cold.current.validation_support_records
 from adapter.tests.qualify_p04_a09_control import inputs,view
 initial,old,expected=inputs();assert c.bundle_id(initial)==c.bundle_id(b)
 raw={z.path:(R/z.path).read_bytes() for z in old.source_additions}
 try:c.preflight_external_evidence(cold,old,raw,R,expected_binding=expected)
 except m.PlannerError as exc:stale=str(exc)
 else:raise AssertionError('old candidate not stale')
 assert 'PARENT' in stale or 'STATE' in stale or 'BUNDLE' in stale,stale
 old_checks=[]
 for path in sorted((D/'qualification').glob('*/a09*candidate.json')):
  if 'VALIDATION_V02' in str(path):continue
  prior=c._unwire(c.parse_json(path.read_bytes()))
  if type(prior) is not m.EvidenceSourceAdmission:continue
  assert prior.expected_parent_event!=cold.events[-1].identity
  wrapped=tx.bind(prior,old.attestation_operand.attestation,expected)
  try:c.preflight_external_evidence(cold,wrapped,{z.path:(R/z.path).read_bytes() for z in prior.source_additions},R,expected_binding=expected)
  except m.PlannerError as exc:old_checks.append({'path':str(path.relative_to(R)),'status':'STALE','reason':str(exc),'archive_unchanged':True,'E07_operand_wrapper_preserves_old_parent_and_pre_state':True})
  else:raise AssertionError('obsolete A09 candidate accepted')
 emit('old-candidate-checks.json',old_checks)
 freshx=replace(old,expected_bundle=bid,expected_snapshot=c.snapshot_id(cold.current),expected_parent_event=cold.events[-1].identity)
 transient_fields=dict(vars(old.attestation_operand.attestation));transient_fields.pop('attestation_id')
 transient=ea.materialize(**transient_fields)
 freshx=tx.bind(freshx,transient,expected)
 received=c.preflight_external_evidence(cold,freshx,raw,R,expected_binding=expected)
 from adapter.planner import evidence_transaction
 oracle=evidence_transaction.receipt_oracle(cold.current,freshx);evidence_transaction.check_receipt_postcondition(oracle,received.current)
 cmd=vt.command(received,freshx.entity.id,installed_record.id)
 a,validated=vt.prepare(received,cmd,R)
 entity=next(x for x in validated.current.entities if x.id==freshx.entity.id)
 checks={'Evidence_present':any(e.id==freshx.entity.id for e in received.current.entities),'receipt_present':len(received.current.receipt_admissions)==1,'received_only':received.current.external_gates[0].stage is m.ExternalStage.EVIDENCE_RECEIVED,'validation_not_evaluated':not received.current.validation_results,'definitions_current':i.current(cold,installed_record),'validation_accepted':entity.validation is m.ValidationState.ACCEPTED and entity.validated,'result_PASS':a.validation_result.outcome is m.ValidationOutcome.PASS,'support_present':a.support.observation.accepted,'external_complete':gates.external_complete(validated.current,validated.current.external_gates[0]),'A11_proof_absent':validated.current.typed_proofs==cold.current.typed_proofs==(),'reentry_false':validated.current.external_gates[0].stage is m.ExternalStage.EVIDENCE_VALIDATED,'action_completion_unchanged':validated.current.statuses==received.current.statuses,'knowledge_unchanged':validated.current.knowledge==cold.current.knowledge,'root_slot_unchanged':validated.current.roots==cold.current.roots and validated.current.slots==cold.current.slots,'control':core.recompute(validated.current).control.value=='EXTERNAL_WAIT','canonical_received_absent':not cold.current.receipt_admissions,'canonical_results_absent':not cold.current.validation_results and not cold.current.validation_support_records,'canonical_proof_absent':not cold.current.typed_proofs}
 assert all(checks.values()),checks
 emit('p04-install-event.json',c._wire(request));emit('fresh-a09-candidate.json',c._wire(freshx));emit('private-a10-precommit.json',c._wire(a))
 a09checks={'control':core.recompute(received.current).control.value=='EXTERNAL_WAIT','actionable':not core.recompute(received.current).actionable,'selected':core.recompute(received.current).selection is None or core.recompute(received.current).selection.selected is None,'decision_ready':not core.recompute(received.current).human_batches,'received':received.current.external_gates[0].stage is m.ExternalStage.EVIDENCE_RECEIVED,'unvalidated':not next(e for e in received.current.entities if e.id==freshx.entity.id).validated,'no_validation':received.current.validation_instances==cold.current.validation_instances,'no_proof':received.current.typed_proofs==cold.current.typed_proofs,'no_proof_contract_admission':received.current.proof_contracts==cold.current.proof_contracts,'no_observation_acceptance':received.current.receipt_observations==cold.current.receipt_observations,'no_resume':not core.resume_eligibility(received,R).allowed,'no_external_complete':not gates.external_complete(received.current,received.current.external_gates[0]),'no_knowledge':received.current.knowledge==cold.current.knowledge,'root_slot_unchanged':received.current.roots==cold.current.roots and received.current.slots==cold.current.slots,'no_action_completion':{s.id for s in received.current.statuses if s.state is m.ActionState.COMPLETED}=={s.id for s in cold.current.statuses if s.state is m.ActionState.COMPLETED},'two_private_events':len(received.events)==len(cold.events)+2,'canonical_unchanged':c.bundle_bytes(cold)==c.bundle_bytes(after),'no_canonical_commit':not cold.current.receipt_admissions}
 assert len(a09checks)==18 and all(a09checks.values()),a09checks
 emit('p04-preflights.json',{'A09':'PASS','A09_oracle_terms':a09checks,'A10':'PASS','A10_oracle_terms':checks,'before':view(cold),'private_received':view(received),'private_validated':view(validated),'old_candidate':stale,'no_canonical_lifecycle_commit':True})
 readers=fresh([{'name':'P04-A10-definitions-installed','path':str(output),'root':str(R),'bundle_id':c._wire(bid),'state_id':c._wire(c.snapshot_id(cold.current)),'computation':computation_wire(cold.current),'sources':sorted(c._wire(cold.sources),key=c.canonical_bytes),'events':c._wire(cold.events)}])
 emit('p04-application.json',{'RESULT':'PASS','bundle_id':c._wire(bid),'state_id':c._wire(c.snapshot_id(cold.current)),'append_head':c._wire(cold.events[-1].identity),'install_event':c._wire(cold.events[-1]),'authority_id':c._wire(authority.id),'definition_ids':{k:c._wire(z.id) for k,z in vi.descriptor(defn)[1][1].items()},'currentness':'PASS','cold_restore':'PASS','replay':'PASS','fresh_reader_comparisons':len(readers),'old_A09':'STALE','A09':'PASS','A10':'PASS','P04_EXECUTION_READY':'NO','NEXT_PACKAGE':'A11 reference/currentness closure; then authorized A12 Action/result and A13 root/slot/FINISH definition installation','A09_A10_EXECUTED':'NO'})
 print('P04_CONFIGURATION_AND_PRIVATE_PREFLIGHTS_PASS',flush=True)
if __name__=='__main__':
 if sys.argv[1]=='qualify':qualification()
 elif sys.argv[1]=='authorize':authorize()
 elif sys.argv[1]=='apply':application()
