"""Focused semantic policy tests; immutable actual r11 bytes and copied mutations."""
import json,sys,copy,tempfile,hashlib
from pathlib import Path
O=Path(__file__).parent;sys.path.insert(0,str(O/'candidate'))
from adapter.attempt_chain import classify_terminal
from adapter.evidence_semantics import REGISTRY,REGISTRY_ID,classify_record
from adapter.context_projection import canonical,sha,read_exact
from adapter.run_control import events,E1_POLICY,assert_admission,BudgetExceeded
capture=json.loads((O/'R11_AUTHENTICATED_CAPTURE.json').read_bytes());t=capture['terminal'];identity=capture['authorization']['authorization_id']
raw=read_exact(t['audit'],t['audit_sha256']);rows=events(Path(t['audit']));checks={}
def verdict(r=rows,term=t):return classify_terminal(r,term,identity,True)
def expect(name,fn,fail=False):
 try:result=fn()
 except (ValueError,KeyError,BudgetExceeded) as e:
  if not fail:raise
  checks[name]={'result':'PASS_REJECTED','reason':str(e)}
 else:
  if fail:raise AssertionError(name+' accepted')
  checks[name]={'result':'PASS','observed':result}
def mutate(event,details=None,**extra):
 r=copy.deepcopy(rows);x=copy.deepcopy(next(x for x in r if x.get('event')=='span_start'));x['event']=event
 if details is not None:x['details']=details
 x.update(extra);r.insert(-1,x);return r
expect('actual_r11_safe_predecessor',verdict)
expect('legacy_frozen_predicate_still_rejects',lambda:classify_terminal(rows,t,identity),True)
control=next(r for r in rows if r.get('schema')=='E1-RUN-CONTROL-1');expected=control['identity']
for kind,name in [('event','budget_exhausted'),('span','attempt_history_ancestry'),('span','attempt_history_decision'),('span','attempt_history_historical_capture'),('activity','attempt_history_ancestry'),('activity','model_projection')]:
 selected=[r for r in rows if (r.get('event')==name if kind=='event' else r.get('event') in ('span_start','span_end') and r['details']['name']==name if kind=='span' else r.get('event')=='activity' and r['details']['operation']==name)]
 assert selected
 expect(kind+':'+name,lambda selected=selected:sorted({classify_record(r,expected) for r in selected}))
for name,r in {
 'unknown_span':mutate('span_start',{'name':'unknown_harmless_claim'}),
 'unknown_activity':mutate('activity',{'operation':'unknown_activity'}),
 'unknown_event':mutate('unknown_event',{}),
 'model_start':mutate('model_request_start',{}),
 'model_sent':mutate('model_request_sent',{}),
 'provider_accepted':mutate('provider_request_accepted',{}),
 'execution':mutate('execution_scope_created',{}),
 'repository_effect':mutate('repository_effect',{}),
 'knowledge_effect':mutate('knowledge_effect',{}),
 'uncertainty':mutate('uncertainty',{}),
 'caller_class':mutate('span_start',{'name':'model_projection'},evidence_class='NON_EFFECTING_OBSERVATION'),
 'hidden_effect_field':mutate('span_start',{'name':'model_projection','effect':True}),
 'hidden_uncertainty':mutate('budget_exhausted',{'budget':'no_progress','value':300,'last_progress':0,'operation':'validation','uncertainty':'unknown'}),
 'wrong_cycle':mutate('activity',{'operation':'model_projection'},cycle=1),
 'wrong_identity':mutate('activity',{'operation':'model_projection'},identity=dict(expected,authorization_id='other')),
 'wrong_policy':mutate('activity',{'operation':'model_projection'},policy_sha256='0'*64),
}.items():expect(name,lambda r=r:verdict(r),True)
uncertain=copy.deepcopy(t);uncertain['lifecycle']['uncertain']=True
expect('independent_uncertainty_cannot_be_cleared',lambda:verdict(term=uncertain),True)
effect=copy.deepcopy(t);effect['actions']['results']=['effect']
expect('independent_effect_cannot_be_cleared',lambda:verdict(term=effect),True)
expect('admission_remains_closed',lambda:assert_admission(Path(t['audit']),E1_POLICY,expected),True)
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'altered.jsonl';p.write_bytes(raw.replace(b'model_projection',b'model_projectioX',1))
 expect('historical_byte_change',lambda:read_exact(str(p),t['audit_sha256']),True)
 expect('telemetry_hash_change',lambda:events(p),True)
 p.write_bytes(raw);expect('independent_byte_reconstruction',lambda:classify_terminal(events(p),t,identity,True))
node=capture
while 'terminal' in node:
 terminal=node['terminal'];a=node['authorization']['authorization_id'];data=read_exact(terminal['audit'],terminal['audit_sha256'])
 expect('history:'+a,lambda terminal=terminal,a=a:classify_terminal(events(Path(terminal['audit'])),terminal,a,a==identity))
 g=node['governance'];state=g.get('run7',g.get('run6',g.get('run5')));node=state['predecessor']
projection=copy.deepcopy(rows)
next(r for r in projection if r.get('event')=='context_projection_verified')['ModelPayloadDigest']='0'*64
expect('projection_identity_substitution',lambda:verdict(projection),True)
for x in (t['lifecycle']['state']=='CANCELLED',not t['lifecycle']['uncertain'],t['ownership'] is None,t['scope'] is None,not t['actions']['results'],not t['actions']['incomplete'],t['actions']['scope'] is None):assert x
assert any(r.get('event')=='architectural_state' and r.get('state')=='QUIESCENT' for r in rows)
counts={e:sum(r.get('event')==e for r in rows) for e in ('model_request_start','model_request_sent','provider_request_accepted','model_content_binding','action_request','action_result','execution_scope_created','repository_effect','knowledge_effect','implementation_effect')};assert not any(counts.values())
assert Path(t['audit']).read_bytes()==raw
result={'result':'PASS','classification':'MATERIAL_SAFE_PREDECESSOR_POLICY_EVOLUTION','registry_id':REGISTRY_ID,'registry':REGISTRY,'audit_sha256':sha(raw),'checks':checks,'counts':counts,'terminal':t['lifecycle'],'ownership':t['ownership'],'scope':t['scope'],'no_real_invocation':True,'candidate_files':{p.name:sha(p.read_bytes()) for p in (O/'candidate/adapter').glob('*.py')}}
(O/'SEMANTIC_QUALIFICATION.json').write_text(canonical(result));(O/'EVIDENCE_SEMANTICS_REGISTRY.json').write_text(canonical(REGISTRY))
print(canonical({'result':'PASS','checks':len(checks),'registry_id':REGISTRY_ID,'r11':verdict()}))
