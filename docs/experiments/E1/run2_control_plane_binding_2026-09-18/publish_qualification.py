"""Freeze qualification closure and an unapproved production continuation.
Never selects a real invocation, rewrites a predecessor, or grants dispatch.
"""
import ast,json,sys,tempfile,hashlib
from pathlib import Path
O=Path(__file__).resolve().parent;pubs=json.loads((O/'QUALIFICATION_BINDINGS.json').read_text());p=pubs[0];sys.path.insert(0,p['runtime_root'])
from adapter.context_projection import canonical,sha,digest
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.continuation_envelope import seal,BODY_KEYS,invariants
from adapter.run_control import E1_POLICY
measure=json.loads((O/'PRODUCTION_MEASUREMENTS.json').read_text());samples=measure['samples'];normal=[s for s in samples if s['case']!='hard-cancellation'];hard=next(s for s in samples if s['case']=='hard-cancellation')
assert len(normal)==4 and all(s['performance_pass'] and not s['warnings'] for s in normal)
assert all(s['result']=='PASS' and not s['forbidden_real_request_effect_records'] and not s['substantive_progress_events'] for s in samples)
assert all(s['terminal_recovery']['lifecycle_state']=='CANCELLED' and s['terminal_recovery']['ownership'] is None and not s['terminal_recovery']['reconciliation_required'] for s in samples)
assert all(s['freshness_counts']=={'FRESH':sum(s['freshness_counts'].values())} for s in samples)
assert hard['exhaustion'][0]['details']['budget']=='no_progress' and hard['exhaustion'][0]['details']['value']>=300
assert all(s['terminal_status']=={'freshness':'FRESH','lifecycle_state':'CANCELLED','ownership':'RELEASED','architectural_state':'QUIESCENT','uncertainty':None} for s in samples)
assert json.loads((O/'HISTORICAL_PRESERVATION.json').read_text())['result']=='PASS'
assert json.loads((O/'BOUND_NEGATIVES.json').read_text())['result']=='PASS'
assert json.loads((O/'REUSE_QUALIFICATION.json').read_text())['result']=='PASS'
assert json.loads((O/'QUALIFICATION.json').read_text())['result']=='PASS'
assert 'Ran 30 tests' in (O/'BOUND_REGRESSION.log').read_text() and (O/'BOUND_REGRESSION.log').read_text().rstrip().endswith('OK')
old=json.loads((O/'SUPERVISOR_IMMUTABLE_VERIFICATION.json').read_text());fresh=json.loads((O/'SUPERVISOR_COLD_RECHECK.json').read_text());exclude={'id','seconds','producer'}
assert {k:v for k,v in old.items() if k not in exclude}=={k:v for k,v in fresh.items() if k not in exclude}
final_s3=json.loads((O/'FINAL_S3_READINESS.json').read_text());assert final_s3['result']=='PASS' and final_s3['observation']==old['original_readiness']
proof=json.loads((O/'R12_AUTHENTICATED_CAPTURE.json').read_text());original=Path('/tmp/forge-attempt-chain-xjcb_jkz/adapter')
def functions(path,cls=None):
 t=ast.parse(path.read_text());nodes=t.body if cls is None else next(n for n in t.body if isinstance(n,ast.ClassDef) and n.name==cls).body
 return {n.name:ast.dump(n,include_attributes=False) for n in nodes if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
current=Path(p['runtime_root'])/'adapter';before=functions(original/'run_control.py','RunControl');after=functions(current/'run_control.py','RunControl')
for name in ('check','progress_event','next_cycle','span'):assert before[name]==after[name],name
assert functions(original/'responses_orchestrator.py')['tool_definitions']==functions(current/'responses_orchestrator.py')['tool_definitions']
qcont=json.loads((O/'PROPOSED_IMPLEMENTATION_CONTINUATION.json').read_text());assert qcont==seal({k:qcont[k] for k in BODY_KEYS},qcont['approval'])
assert p['controller_runtime_identity']=='sha256:'+digest({f.name:sha(f.read_bytes()) for f in current.glob('*.py')})
transitions=[json.loads(x) for x in (Path(pubs[-1]['audit']).parent/'TRANSITION_STATUS.jsonl').read_text().splitlines()]
required={'authorization_lifecycle_activation_intent':('ACTIVATING','NONE'),'invocation_reserved':('ACTIVATING','HELD_FOR_RECONCILIATION'),'authorization_lifecycle_activated':('ACTIVE','OWNERSHIP_HELD'),'invocation_released':('CANCELLED','RELEASED')}
for row in transitions:
 expected=required.pop(row['committed_event']);v=row['snapshot'];assert v['freshness']=='FRESH' and (v['operational_state'],v['ownership'])==expected
assert not required
(O/'TRANSITION_STATUS.json').write_text(canonical(transitions))
closure={'schema':'CONTROL-PLANE-QUALIFICATION-CLOSURE-1','verdict':'RUN2_CONTROL_PLANE_READY_FOR_NEXT_ATTEMPT',
 'implementation':p['controller_runtime_identity'],'qualification_continuation':p['continuation_id'],
 'scope':'Real released authority objects, complete original history and live S3; isolated synthetic lifecycle/ownership namespaces; shared production validators; no provider/effect permission',
 'production_functions_mocked':False,'real_release_authority':p['release_authority'],'real_historical_context':proof['governance']['identities'],
 'qualified_contexts':[{k:x[k] for k in ('name','authorization_id','selected_store','operational_identities','context_identities')} for x in pubs],
 'gates':{k:'PASS' for k in ('production_pre_model_path','production_performance','automatic_cancellation','live_status','fresh_S3','r12_safe_predecessor','historical_preservation','reuse_negatives','regressions')},
 'r12_classification':'ACTIVE_CANCELLED_PRE_MODEL_NO_EFFECTS','r12_disposition':'CANCELLED / INTERRUPTED_NO_EFFECTS',
 'normal_cumulative_seconds':[x['cumulative_model_request_ready_seconds'] for x in normal],
 'max_normal_phase_seconds':max(x['maximum_individual_phase_seconds'] for x in normal),
 'periodic_status_samples':sum(sum(x['freshness_counts'].values()) for x in samples),'transition_status_samples':len(transitions),
 'no_progress_exhaustion_seconds':hard['exhaustion'][0]['details']['value'],
 'budgets':E1_POLICY,'budget_semantics':'UNCHANGED','substantive_progress_semantics':'UNCHANGED',
 'ModelPayloadDigest':p['context_identities']['ModelPayloadDigest'],'material_release_amendment_applied':False,
 'real_invocations_created':0,'real_model_requests':0,'real_governed_effects':0,'r13_created':False,
 'evidence':{n:sha((O/n).read_bytes()) for n in ('PRODUCTION_MEASUREMENTS.json','QUALIFICATION_BINDINGS.json','HISTORICAL_PRESERVATION.json','FINAL_S3_READINESS.json','SUPERVISOR_COLD_RECHECK.json','BOUND_NEGATIVES.json','REUSE_QUALIFICATION.json','QUALIFICATION.json','BOUND_REGRESSION.log','TRANSITION_STATUS.json')}}
closure['id']='CONTROL-PLANE-QUALIFICATION-sha256:'+digest(closure)
(O/'QUALIFIED_CLOSURE.json').write_text(canonical(closure))
# Prepare the ordinary canonical envelope separately from the finite synthetic
# qualification envelope. No approval or real context selection is fabricated.
parent=ControllerAuthorityStore(**p['selected_store']);records={}
def add(data):
 if not isinstance(data,bytes):data=canonical(data).encode()
 h=sha(data);records['sha256:'+h]={'bytes':data,'evidence':[]};return {'authority_id':'sha256:'+h,'sha256':h}
try:
 with parent.session():
  evidence_ref=add({'status':'PASS_SYNTHETIC_CORRECTIONS_NON_ADOPTED','production_qualification':'PASS','qualification_closure':add(closure),
   'candidate_files':{f.name:sha(f.read_bytes()) for f in current.glob('*.py')},'supervisor_verification':add((O/'SUPERVISOR_IMMUTABLE_VERIFICATION.json').read_bytes()),
   'model_and_effect_authority':'NONE','real_invocation_created':False})
  source_ref=add({'authority':'Architect','channel':'user','decision':'CONSTRUCT_QUALIFIED_CONTROL_PLANE_IMPLEMENTATION_CONTINUATION',
   'qualification_closure':closure['id'],'scope':'implementation qualification and proposed continuation only; no r13, issuance, activation, real ownership, model request or dispatch'})
  protected=invariants(json.loads(proof['authorization']['operational_binding']),proof['context']['projection'])
  artifacts=[]
  for row in qcont['artifacts']:
   row=dict(row);data=Path(row['new_blob']).read_bytes();assert sha(data)==row['new_sha256'];row['new_content']=add(data);artifacts.append(row)
  c=seal({'schema':'OPERATIONAL-CONTINUATION-1','type':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION','sequence':proof['governance']['run7']['continuation']['sequence']+1,
   'predecessor_OperationalContextId':proof['governance']['identities']['OperationalContextId'],'predecessor_chain_digest':proof['governance']['identities']['continuation_chain_digest'],
   'artifacts':artifacts,'authority':source_ref,'classification':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION','evidence':evidence_ref,'authority_invariants':protected,
   'reason':'Qualified control-plane performance, cancellation and read-only status corrections; no change to task, authority, payload, budgets or progress semantics'},None)
  cref=add(c);roots=parent.catalog['programmer_roots'];ids={k:proof['governance']['identities'][k] for k in ('ReleaseBasisId','ReleaseDecisionId')}
 root=Path(tempfile.mkdtemp(prefix='kge-control-plane-qualified-'));root.chmod(0o700)
 store=ControllerAuthorityStore.materialize(root/'objects',records,{}, {'authority_source':source_ref,'release_identities':ids},
  {'purpose':'QUALIFIED_IMPLEMENTATION_CANDIDATE_NOT_INVOCATION','qualification_id':closure['id'],**ids},roots)
 try:
  with store.session():
   assert json.loads(store.resolve(cref['authority_id']))==c
   for row in artifacts:assert sha(store.resolve(row['new_content']['authority_id']))==row['new_sha256']
  private={'root':str(store.root),'catalog_sha256':store.catalog_sha256,'applicability':store.applicability}
 finally:store.close()
finally:parent.close()
(O/'PROPOSED_PRODUCTION_CONTINUATION.json').write_text(canonical(c))
publication={'schema':'QUALIFIED-CONTROL-PLANE-PUBLICATION-1','verdict':closure['verdict'],'closure_id':closure['id'],'implementation':p['controller_runtime_identity'],
 'qualification_continuation':p['continuation_id'],'qualification_continuation_ref':p['continuation'],
 'proposed_production_continuation':c['continuation_id'],'proposed_production_continuation_file_sha256':sha((O/'PROPOSED_PRODUCTION_CONTINUATION.json').read_bytes()),'proposed_continuation_ref':cref,'candidate_store':private,
 'proposed_continuation_context_id':c['OperationalContextId'],'proposed_continuation_chain_digest':c['continuation_chain_digest'],
 'real_release_authority':p['release_authority'],'real_historical_context':proof['governance']['identities'],
 'production_continuation_applied':False,'real_invocation_authorized':False,'qualified_contexts':closure['qualified_contexts']}
(O/'QUALIFIED_PUBLICATION.json').write_text(canonical(publication))
print(canonical({k:publication[k] for k in ('verdict','implementation','qualification_continuation','proposed_production_continuation','proposed_continuation_context_id')}))
