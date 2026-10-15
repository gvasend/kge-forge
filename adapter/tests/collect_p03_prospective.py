"""Read-only qualification comparisons and output publication; no fixture edits."""
from dataclasses import replace
from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile
from adapter.tests import qualify_p03_prospective as q
from adapter.tests import revise_p03_support as revision
from adapter.planner import codec as c, model as m, core, gates
ROOT=q.ROOT;A=q.A;D=q.D

def jsonread(p):return json.loads(Path(p).read_text())
def admit(b,expected_bundle,oracle,seal):
 expected=c._unwire(oracle['checkpoint']);src=c._unwire(oracle['pins'])
 if sorted(c._wire(b.sources),key=c.canonical_bytes)!=sorted(c._wire(src),key=c.canonical_bytes):raise m.PlannerError('SEALED_SOURCE_SET_MISMATCH_OR_POST_HOC_PIN')
 if b.policy!=c._unwire(oracle['policy'])or b.policy_version!='E1-SELECTION-1-P06':raise m.PlannerError('SEALED_POLICY_MISMATCH')
 if b.current.context.scope!=q.SCOPE:raise m.PlannerError('SEALED_SCOPE_MISMATCH')
 if b.current.context.lineage!=q.LINEAGE:raise m.PlannerError('SEALED_LINEAGE_MISMATCH')
 if c._wire(b.current.entities)!=c._wire(expected.entities):raise m.PlannerError('SEALED_AUTHORITY_MISMATCH')
 c._verify_sources(b,ROOT);c._replay(b)
 if c.snapshot_bytes(b.current)!=c.snapshot_bytes(expected):raise m.PlannerError('CHECKPOINT_BOUNDARY_OR_PROVENANCE_MISMATCH')
 if c.bundle_id(b)!=expected_bundle:raise m.PlannerError('SEALED_EVENT_LINEAGE_MISMATCH')
 return True

def negatives(b,expected,oracle,manifest):
 zero=m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'raw-file-sha256','0'*64)
 mutants={
 'wrong_source_binding':replace(b,sources=(replace(b.sources[0],path='wrong-source.json'),)+b.sources[1:]),
 'wrong_source_contract':replace(b,current=replace(b.current,external_gates=(replace(b.current.external_gates[0],provenance=replace(b.current.external_gates[0].provenance,identity=zero)),))),
 'wrong_policy':replace(b,policy_version='E1-SELECTION-1-P01-SUBSET'),
 'wrong_policy_identity':replace(b,policy=replace(b.policy,identity=zero)),
 'wrong_authority':replace(b,current=replace(b.current,entities=tuple(replace(e,consumed=True)if e.id.value=='E2-GRANT'else e for e in b.current.entities))),
 'wrong_scope':replace(b,current=replace(b.current,context=replace(b.current.context,scope='WRONG'))),
 'wrong_lineage':replace(b,current=replace(b.current,context=replace(b.current.context,lineage='WRONG'))),
 'missing_provenance':replace(b,current=replace(b.current,knowledge=tuple(replace(k,provenance=replace(k.provenance,method=''))for k in b.current.knowledge))),
 'earlier_checkpoint':replace(b,events=b.events[:1],current=b.initial),
 'later_checkpoint':c.record_result(b,m.ActionReevaluation((m.EntityId('PROSPECTIVE-SEAL-WITNESS'),),c.snapshot_id(b.current),next(e.provenance for e in b.current.entities if e.id.value=='PROSPECTIVE-SEAL-WITNESS'))),
 'unrelated_event_lineage':replace(b,events=(replace(b.events[0],parent_event=zero),)+b.events[1:]),
 'post_hoc_pin_creation':replace(b,sources=b.sources+(m.ArtifactPin('post-hoc.json',zero),)),
 'similar_different_pins':replace(b,sources=tuple(replace(x,identity=replace(x.identity,namespace='wrong-domain'))if i==0 else x for i,x in enumerate(b.sources)))
 }
 results={}
 for name,v in mutants.items():
  try:admit(v,expected,oracle,manifest)
  except (m.PlannerError,ValueError)as ex:results[name]={'result':'PASS_REJECTED','reason':str(ex),'level':'Native validation/replay or independently sealed qualification oracle, as stated by reason'}
  else:raise AssertionError('mutation admitted: '+name)
 from adapter.planner.genesis_bundle import decode_bundle,bundle_identity
 g=decode_bundle((D/(q.P+'E2_GENESIS_PERSISTENCE_BUNDLE.json')).read_bytes())
 assert c.snapshot_id(g.current)!=c.snapshot_id(b.current)and bundle_identity(g)!=expected
 results['G04_checkpoint']={'result':'PASS_REJECTED','reason':'Different native bundle schema/identity, checkpoint context and unknown rule; never accepted as source-pinned prospective checkpoint','g04_bundle':c._wire(bundle_identity(g)),'g04_state':c._wire(c.snapshot_id(g.current))}
 # A wrong physical source is tested in a private file tree with original pins;
 # the canonical fixture and frozen E1 files are never mutated.
 with tempfile.TemporaryDirectory(prefix='p03-wrong-physical-')as td:
  root=Path(td)
  for pin in b.sources+(b.policy,):
   target=root/pin.path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((ROOT/pin.path).read_bytes())
  (root/b.sources[0].path).write_bytes(b'wrong physical source')
  try:c._verify_sources(b,root)
  except m.PlannerError as ex:results['wrong_physical_source']={'result':'PASS_REJECTED','reason':str(ex),'level':'Native physical raw pin verification'}
  else:raise AssertionError('wrong physical source admitted')
 return results

def main():
 os.chdir(ROOT);manifest=revision.verify_revision();a=jsonread(A/'runs/revision-3-a/writer-result.json');b=jsonread(A/'runs/revision-3-b/writer-result.json')
 assert a['label']!=b['label']  # separate executor processes may reuse PID numbers in different namespaces
 for name in a['outputs']:
  assert a['outputs'][name]['view']==b['outputs'][name]['view']
  assert a['trace'][name]==b['trace'][name]
 assert a['invalidations']==b['invalidations'] or [(x['fixture'],x['id'],x['result'])for x in a['invalidations']]==[(x['fixture'],x['id'],x['result'])for x in b['invalidations']]
 # Verify withdrawal starts from a genuinely native PROVED receipt, not just validation labels.
 accepted=c.restore(ROOT/a['outputs']['accepted-support']['checkpoint_path'],c._unwire(a['outputs']['accepted-support']['checkpoint_id']),ROOT)
 receipt_entity=next(x for x in accepted.current.entities if x.kind is m.EntityKind.EVIDENCE)
 assert gates._check_receipt(accepted.current,accepted.current.external_gates[0],receipt_entity.id).state is m.ProofState.PROVED
 receipt_withdrawals=[]
 for inv in a['invalidations']:
  if inv['fixture']=='accepted-support' and inv.get('source',{}).get('identity')==c._wire(receipt_entity.identity):
   after=c.restore(ROOT/inv['path'],c._unwire(inv['id']),ROOT)
   proof=gates._check_receipt(after.current,after.current.external_gates[0],receipt_entity.id)
   assert proof.state is not m.ProofState.PROVED
   receipt_withdrawals.append({'before':'PROVED','after':proof.state.value,'reasons':list(proof.reasons),'bundle':inv['id']})
 assert receipt_withdrawals
 output=a['outputs']['mainline'];bid=c._unwire(output['checkpoint_id']);mainbundle=c.restore(ROOT/output['checkpoint_path'],bid,ROOT);oracle=jsonread(A/'mainline-oracle.json')
 # Exact event IDs are derived from presealed start+checkpoint oracle, not
 # observed results. The event-only root witness has no state effect.
 initial=c._unwire(oracle['start']);checkpoint=c._unwire(oracle['checkpoint']);w=next(e for e in initial.entities if e.id.value=='PROSPECTIVE-SEAL-WITNESS');sid=c.snapshot_id(initial)
 startcommand=m.ActionReevaluation((w.id,),sid,w.provenance);first=c._event_identity(1,sid,None,startcommand,sid)
 secondcommand=m.RecordedDecision(m.ActionId('E2-DECIDE'),'ALLOW_QUALIFICATION_MAPPING',m.EntityId('E2-PROSPECTIVE-CHOICE'),m.PredicateId('E2-PROSPECTIVE-CHOICE-AUTHORITY'),sid)
 last=c._event_identity(2,sid,first,secondcommand,c.snapshot_id(checkpoint))
 assert mainbundle.events[0].identity==first and mainbundle.events[1].identity==last
 # Closed algebraic bundle oracle uses only presealed snapshots/pins plus
 # specified event commands, and never invokes apply_event to make an oracle.
 expected_events=(m.ExecutionEvent(1,sid,None,startcommand,sid,first),m.ExecutionEvent(2,sid,first,secondcommand,c.snapshot_id(checkpoint),last))
 seed=q.load_bundle(A/'mainline-start.json')
 expected_bundle=replace(seed,events=expected_events,current=checkpoint)
 expected_bundle_id=q.identity(c._bundle_bytes_admitted(expected_bundle),'planner-bundle-v1')
 assert expected_bundle_id==bid
 assert not core.resume_eligibility(mainbundle,ROOT).allowed
 assert admit(mainbundle,bid,oracle,manifest)
 readers=[];reader_code="import json,os,sys; from pathlib import Path; from adapter.planner import codec as c,model as m; from adapter.tests.qualify_p03_prospective import view; b=c.restore(Path(sys.argv[1]),m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'planner-bundle-v1',sys.argv[2]),Path.cwd()); assert c.snapshot_id(c._replay(b))==c.snapshot_id(b.current); print(json.dumps({'pid':os.getpid(),'view':view(b)}))"
 scripts=reader_code
 for name in ('mainline','unknown','typed-support'):
  info=a['outputs'][name]
  for seed in (0,1,7,101):
   for repeat in range(3):
    env=dict(os.environ,PYTHONHASHSEED=str(seed),PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(ROOT))
    p=subprocess.run([sys.executable,'-c',scripts,info['checkpoint_path'],info['checkpoint_id']['sha256']],cwd=ROOT,env=env,capture_output=True,text=True)
    if p.returncode:raise RuntimeError(p.stderr)
    result=json.loads(p.stdout);assert result['view']==info['view']
    readers.append({'fixture':name,'writer_context':'revision-3-a / executor 53562','seed':seed,'repeat':repeat,'reader_pid':result['pid'],'writer_pid':a['writer_pid'],'writer_terminated':True,'exit_status':p.returncode,'semantic_state':'PASS','snapshot_identity':'PASS','bundle_identity':'PASS','source_pins':'PASS','policy_pins':'PASS','authority':'PASS','scope_lineage':'PASS','provenance':'PASS','event_ancestry':'PASS','replay':'PASS','computation':'PASS','input_allowlist':[info['checkpoint_path'],'trusted expected bundle identity','sealed physical source files','sealed supported policy','native modules/sealed contracts']})
 # Cold readers for every isolated invalidation, beyond each writer's restore.
 invalid_readers=[]
 for inv in a['invalidations']:
  p=subprocess.run([sys.executable,'-c',scripts,inv['path'],inv['id']['sha256']],cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(ROOT)),capture_output=True,text=True)
  if p.returncode:raise RuntimeError(p.stderr)
  result=json.loads(p.stdout);direct=c.restore(ROOT/inv['path'],c._unwire(inv['id']),ROOT);assert result['view']==q.view(direct)
  invalid_readers.append({'fixture':inv['fixture'],'source':inv.get('source'),'case':inv.get('case','A15'),'reader_pid':result['pid'],'exit_status':0,'domain_comparisons':'PASS_ALL_NATIVE_VIEW_DOMAINS','bundle':inv['id']})
 neg=negatives(mainbundle,bid,oracle,manifest)
 # In-memory input collection permutations keep all pins and chronological events.
 permutations=[]
 for order in ('reverse','rotate'):
  base=q.load_bundle(A/'mainline-start.json')
  def perm(x):return tuple(reversed(x))if order=='reverse'else x[1:]+x[:1]
  s=replace(base.initial,actions=perm(base.initial.actions),statuses=perm(base.initial.statuses),knowledge=perm(base.initial.knowledge),predicates=perm(base.initial.predicates),entities=perm(base.initial.entities))
  variant=replace(base,initial=s,current=s,sources=perm(base.sources))
  assert c.bundle_id(variant)==c.bundle_id(base)
  variant=c.record_result(variant,startcommand);variant=c.record_result(variant,secondcommand)
  variant_view=q.view(variant);expected_view=q.view(mainbundle)
  # Native codec declares sources/entities unordered; standalone tuple
  # serialization preserves presentation order, not semantic set order.
  for domain in ('sources','authority'):
   variant_view[domain]=sorted(variant_view[domain],key=c.canonical_bytes)
   expected_view[domain]=sorted(expected_view[domain],key=c.canonical_bytes)
  assert variant_view==expected_view
  permutations.append({'order':order,'result':'PASS_COMPLETE_VIEW_AND_NATIVE_IDENTITIES'})
 # Publish native output exactly, with the ledger artifacts required by restore.
 q.write(D/(q.P+'P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1.json'),c.bundle_bytes(mainbundle))
 for event in mainbundle.events:q.write(D/('event-'+event.identity.sha256+'.json'),q.jbytes(c._wire(event)))
 assert q.view(c.restore(D/(q.P+'P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1.json'),bid,ROOT))==q.view(mainbundle)
 report={'authorization_authentication':'PASS_EXPLICIT_USER_DECISION_TRUSTED_TRANSPORT','qualification_scope_authority':'PASS_BOUNDED_METADATA_SCOPE_AUTHORITY; DISTINCT_FROM_NATIVE_ACTION_PERMISSION','authority':manifest['authority'],'fixture_id':c._wire(q.identity((A/'revision-3-seal.json').read_bytes(),'planner-prospective-fixture-v1')),'source_pin_set_id':c._wire(q.identity(q.jbytes(sorted(oracle['pins'],key=c.canonical_bytes)),'planner-source-pin-set-v1')),'policy_pin_set_id':c._wire(q.identity(q.jbytes({'policy':oracle['policy'],'version':mainbundle.policy_version}),'planner-policy-pin-set-v1')),'qualification_contract_id':manifest['contract_pin']['identity'],'seal':str((A/'revision-3-seal.json').relative_to(ROOT)),'historical_correspondence':'UNPROVEN','historical_reconstruction':False,'qualification_type':'PROSPECTIVE_REPLACEMENT','checkpoint':{'state_id':c._wire(c.snapshot_id(mainbundle.current)),'bundle_id':c._wire(bid),'ledger_id':None,'ledger_id_reason':'Native PersistenceBundle has an ordered ExecutionEvent tuple, no separate LedgerId field; no report-created identity substituted','ledger_root':c._wire(first),'ledger_root_domain':'Actual first native ExecutionEvent identity; not a GenesisLedger.root','append_head':c._wire(last),'boundary':'Post-RecordedDecision known-rule EXTERNAL_WAIT before RECEIVED','actionable':[],'mainline_FINISH_non_actionable':True,'before_execution_oracle':str((A/'mainline-oracle.json').relative_to(ROOT)),'event_ancestry_expected_from_sealed_oracle':[c._wire(first),c._wire(last)],'algebraic_expected_bundle_identity':c._wire(expected_bundle_id),'resume_eligibility':q.serialize(core.resume_eligibility(mainbundle,ROOT))},'event_backed_start':'PASS_ACTUAL_NATIVE_REEVALUATION_EVENT_AND_FRESH_READER_BEFORE_CONTINUATION','pre_execution_oracle':'PASS_AUTHORED_BEFORE_EVENTS; EXACT_STATE/PINS/AUTHORITY/CONTEXT_AND_ALGEBRAIC_ANCESTRY','equality':{k:'PASS'for k in ['semantic_state','source_pin','policy_pin','authority','scope_lineage','provenance','control','persistence','fresh_reader','cold_restore','replay','independent_reproduction','determinism','event_ancestry']},'writers':[{'label':r['label'],'pid':r['writer_pid'],'executor_session':53562 if r['label']=='revision-3-a' else 10406,'pid_namespace_note':'Independent sandbox executions can reuse PID 2; executor session and run label distinguish writers','exit_status':0,'source':'native writer-result.json; both processes terminated before collected cold readers'}for r in (a,b)],'starting_fresh_readers':[{'fixture':name,'writer':r['label'],'reader_pid':info['start_fresh_reader_pid'],'result':info['start_fresh_reader_result']}for r in (a,b)for name,info in r['outputs'].items()],'fresh_reader_comparisons':readers,'fresh_reader_count':len(readers),'invalidations':a['invalidations'],'native_receipt_support_withdrawal':receipt_withdrawals,'invalidation_fresh_readers':invalid_readers,'negative_controls':neg,'unordered_input_permutations':permutations,'comparison_domain_correction':'Standalone source/authority tuple presentation order differs under legal set permutations; native canonical bytes, complete Computation and per-record identities equal. Compare those two declared unordered collections as canonical multisets.','driver_correction':{'failed_attempts':['writer-a','writer-b','corrected-a','corrected-b','revision-2 accepted-support premise comparison'],'reason':'Initial driver ROOT-first correctly rejected; corrected driver revealed native A14 source grammar mismatch; preserved failed attempt and sealed distinct revisions with native contract/payload source grammar before accepted runs','fixture_changed_between_accepted_reproductions':False,'earlier_failed_fixture_encoding_preserved':True,'revision_sealed_before_accepted_reproductions':True,'runtime_changed':False,'corrected_driver':'adapter/tests/run_p03_prospective.py','corrected_driver_hash':hashlib.sha256((ROOT/'adapter/tests/run_p03_prospective.py').read_bytes()).hexdigest(),'driver_sealed_before_corrected_runs':True,'scope':'Dependency ordering already mandated by sealed contracts; no source/policy/contract/oracle pin added or changed'},'prospective_p03_checkpoint_qualification':'PASS','e2_finish_executed':False,'mainline_actions_executed':['E2-DECIDE via RecordedDecision'],'E2_FINISH_actionable_current_continuation':True,'N_REAL_SATISFIED':False,'production_effect':False,'runtime_modified':False,'e1_artifacts_modified':0,'run_evidence':{'first':str((A/'runs/revision-3-a/writer-result.json').relative_to(ROOT)),'second':str((A/'runs/revision-3-b/writer-result.json').relative_to(ROOT))},'runtime_hashes':manifest['runtime_hashes'],'procedure_hash':manifest['procedure_sha256'],'all_sealed_inputs_verified_unchanged':True}
 revision.verify_revision();q.write(D/(q.P+'P03_PROSPECTIVE_CHECKPOINT_COMPARISONS_1.json'),q.jbytes(report));print(json.dumps({'result':'PASS','checkpoint':report['checkpoint'],'readers':len(readers),'invalidation_readers':len(invalid_readers),'negatives':len(neg)}))

if __name__=='__main__':main()
