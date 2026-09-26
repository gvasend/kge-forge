"""Offline release evidence construction; no adapter edits, activation or model call."""
from pathlib import Path
from dataclasses import replace
from collections import Counter
import hashlib,json,sys,uuid
ROOT=Path('/home/gvasend/app/kge-forge');sys.path.insert(0,str(ROOT))
from adapter.context_binding import CommittedContext
from adapter.runnable_profile import authorization,canonical
from adapter.governed_host import GovernedHost
from adapter.orchestrator import ReasoningOrchestrator
from adapter.responses_orchestrator import ResponsesReasoning
from adapter.model_transmission import digest
PRE=ROOT/'docs/experiments/E1/pre_dispatch';OUT=PRE/'pd06_final_clearance'
REF=json.loads((PRE/'pd06_release_evidence/CAPTURE_REFERENCE.json').read_text())
M=Path(REF['manifest']);CAP=json.loads(M.read_text());BLOBS=M.parent/'blobs'
sha=lambda data:hashlib.sha256(data).hexdigest()
def write(name,value): (OUT/name).write_text(json.dumps(value,indent=2)+'\n')
assert sha(M.read_bytes())==REF['capture_sha256'] and len(CAP['inputs'])==186
for path,row in CAP['inputs'].items():
 assert sha((BLOBS/row['sha256']).read_bytes())==row['sha256']
 assert sha(Path(path).read_bytes())==row['sha256'],path
b=CommittedContext(PRE/'CONTEXT_MANIFEST.json','5871bdce4f5b6539c84f69f4f2b2f94ee31be5cd');assert b.verify()
def captured(path):return (BLOBS/CAP['inputs'][str(path)]['sha256']).read_bytes()
wp=PRE/'E1-WP-001.md';protocol=PRE/'CONTEXT_PROTOCOL.md'
req=ROOT/'docs/EXPERIMENT_1_REQUIREMENTS_SYNTHESIS.md';arch=ROOT/'docs/EXPERIMENT_1_ARCHITECTURE.md'
decisions=PRE/'DECISIONS.md';oldprofile=PRE/'pd06_release_evidence/PROPOSED_PRODUCTION_PROFILE.json'
selected={}
def add(path,kind,reason,spans):
 data=captured(path);rows=[]
 for start,end,label in spans:
  part=data[start:end];assert part
  rows.append({'start_byte':start,'end_byte_exclusive':end,'sha256':sha(part),
               'start_line':data[:start].count(b'\n')+1,'end_line':data[:end].count(b'\n'),
               'label':label})
 selected[str(path)]={'designation':kind,'reason':reason,'spans':rows}
def full(path,reason):add(path,'COMPLETE_FILE',reason,[(0,len(captured(path)),'complete captured file')])
def section(path,start,end,label):
 data=captured(path);a=data.index(start.encode());z=data.index(end.encode(),a);return (a,z,label)
def rows(path,prefixes):
 data=captured(path);out=[];offset=0
 for line in data.splitlines(keepends=True):
  if any(line.startswith(p.encode()) for p in prefixes):out.append((offset,offset+len(line),line.split(b'|')[1].strip().decode()))
  offset+=len(line)
 assert len(out)==len(prefixes)
 return out
full(wp,'Exact production task expressly selected; includes all implementation, acceptance, stop and result obligations.')
full(protocol,'E1-WP-001 explicitly names this input contract; all fields, provenance, error and gate semantics are needed to implement the validator.')
add(req,'BOUNDED_CONTENT','E1-WP-001 names F-01 through F-11 and bounded A-13 through A-15 obligations; service-only requirements and unrelated review findings excluded.',
 rows(req,['| F-%02d |'%n for n in range(1,12)]+['| A-%02d |'%n for n in range(13,16)]))
add(arch,'BOUNDED_CONTENT','E1-WP-001 explicitly governed by D-01 through D-03 and architecture sections 3-5; section 4 contains the AR-04/AR-05 corrections, so separate review evidence is unnecessary.',
 rows(arch,['| D-%02d |'%n for n in range(1,4)])+[section(arch,'## 3. Forge knowledge','## 6. Task-service','Sections 3-5')])
add(decisions,'BOUNDED_CONTENT','PD-04 supplies the selected Python 3.8.10/stdlib compatibility obligation; other preparation/gate/publication decisions are not needed as model content.',
 [section(decisions,'## PD-04','## PD-05','PD-04 tooling only')])
data=captured(oldprofile)
a=data.index(b'    "argv":');z=data.index(b'    "executables":',a)
x=data.index(b'    "acceptance":',z);value_start=data.index(b'{',x)
_,end=json.JSONDecoder().raw_decode(data[value_start:].decode());y=value_start+end
add(oldprofile,'BOUNDED_CONTENT','Explicitly released test context: exact argv, cwd, input list, environment, shell/network posture and committed acceptance identity needed to invoke the authorized test and real-context acceptance case. All binary/host-control/ledger/audit/identity/gate/transport fields excluded.',
 [(a,z,'runtime argv/cwd/inputs/environment/network/shell'),(x,y,'exact committed acceptance input identity')])
source_ids={str(b.repos[s['repository']]/s['path']):sid for sid,s in b.sources.items()}
items=[]
private_names={'STATE.json','INACTIVE_VERIFICATION.json','OWNERSHIP_VERIFICATION.json','FINAL_SCOPE_VERIFICATION.json',
 'PRODUCTION_LAUNCH_RECORD.json','HOST_RECEIPT.json','configuration_observations.json','LIVE_REPORT.json',
 'PROPOSED_E1_PROFILE.json','PROPOSED_PRODUCTION_PROFILE.json'}
for path,row in CAP['inputs'].items():
 p=Path(path);selection=selected.get(path)
 if selection:
  classification='TRANSMIT';reason=selection['reason'];category='released execution/test context' if p==oldprofile else 'required E1 governing/task contract'
 elif not any(p==r or r in p.parents for r in b.repos.values()):
  classification='NEVER_TRANSMIT';reason='Outside released E1 read grants; runtime/host-control or controller-private audit/ownership information.';category='outside read grants'
 elif any(part in ('.git','.codex','.agents') for part in p.parts):
  classification='NEVER_TRANSMIT';reason='Architect hidden-path prohibition.';category='hidden path'
 elif p.suffix=='.jsonl' or p.name in private_names or 'snapshots' in p.parts:
  classification='NEVER_TRANSMIT';reason='Controller-private state, execution identity, raw audit, authorization or host-control state; not required model context.';category='controller-private state/audit/host control'
 else:
  classification='LOCAL_ONLY';reason='Not necessary as model context for this bounded task; retained solely for local governing provenance, qualification, gate, implementation, release or unrelated service review.';category='local evidence/implementation/release or unrelated governing input'
 item={'source_identity':source_ids.get(path,path),'canonical_path':path,'captured_sha256':row['sha256'],
  'captured_bytes':row['bytes'],'candidate_capture_sha256':REF['capture_sha256'],
  'classification':classification,'category':category,'reason':reason}
 if selection:
  item.update(selection);item['remainder_classification']=('NEVER_TRANSMIT' if p==oldprofile else 'LOCAL_ONLY') if selection['designation']=='BOUNDED_CONTENT' else 'NONE'
  item['authority_source']='ARCHITECT_SELECTIONS.md: eligible content categories and minimum-necessary selection mandate'
 else:item['designation']='COMPLETE_FILE';item['authority_source']='ARCHITECT_SELECTIONS.md: local-only/never-transmit exclusions'
 items.append(item)
counts=dict(Counter(r['classification'] for r in items))
manifest={'schema':'E1-CONTENT-CLEARANCE-1','candidate':REF,'universe_count':186,
 'selection_authority_sha256':sha((OUT/'ARCHITECT_SELECTIONS.md').read_bytes()),
 'content_rule':'Only exact selected bytes; bounded TRANSMIT never clears the remainder. No clearance transfers to changed content, another path, a containing evidence record, or an alternate representation.',
 'counts':counts,'unresolved_classifications':0,'inputs':items,
 'additional_never_categories':['credentials/secrets (none accessed)','controller-private state','.git/.codex/.agents','outside read grants','unneeded host-control information']}
write('CONTENT_CLEARANCE_MANIFEST.json',manifest)
context={'schema':'E1-CLEARED-CONTEXT-1','sources':[]}
for path,selection in selected.items():
 if path==str(wp):continue
 data=captured(Path(path));context['sources'].append({'source':path,'selections':[
  {'label':span['label'],'content':data[span['start_byte']:span['end_byte_exclusive']].decode()} for span in selection['spans']]})
task=captured(wp).decode();assert task.encode()==captured(wp)
write('PRODUCTION_CONTEXT.json',context)
(OUT/'PRODUCTION_TASK.md').write_bytes(captured(wp))
write('PRODUCTION_TASK_IDENTITY.json',{'source':str(wp),'captured_sha256':sha(captured(wp)),
 'candidate_capture_sha256':REF['capture_sha256'],'designation':'COMPLETE_FILE','bytes':len(captured(wp))})
profile=json.loads(captured(oldprofile));oldlaunch=json.loads(captured(PRE/'pd06_release_evidence/PRODUCTION_LAUNCH_RECORD.json'))
policy=profile['model_transmission']
policy['authority_source']='ARCHITECT_SELECTIONS.md and content-clearance manifest SHA256 '+sha(canonical(manifest).encode())
policy['clearance_manifest_sha256']=sha(canonical(manifest).encode())
policy['initial_clearances']=[{'category':'cleared-reasoning-context','authority_source':policy['authority_source'],
 'sha256':digest({'task':task,'context':context}), 'task_sha256':sha(task.encode())}]
policy['file_clearances']=[{'path':path,'sha256':CAP['inputs'][path]['sha256'],
 'category':'explicitly-cleared-governing','authority_source':policy['authority_source']}
 for path,selection in selected.items() if selection['designation']=='COMPLETE_FILE']
# The coarse pre_dispatch evidence-root exclusion is replaced with exact excluded sources;
# this is a policy selection only, and does not clear any directory or sibling.
policy['evidence_paths']=[r['canonical_path'] for r in items if r['classification']=='LOCAL_ONLY']
policy['private_paths']=[r['canonical_path'] for r in items if r['classification']=='NEVER_TRANSMIT']+[str(OUT)]
profile['schema']='E1-PROPOSED-LAUNCH-5';profile['revision']=5
profile['model_information_categories']={'authority':'CONTENT_CLEARANCE_MANIFEST.json',
 'TRANSMIT':'Exact task, five selected context sources (bounded as recorded); no unapproved status/diagnostics/hash channel',
 'LOCAL_ONLY':'All other local evidence/implementation/release and unrelated governing sources',
 'NEVER_TRANSMIT':manifest['additional_never_categories']}
profile['release_preconditions']=[{'id':'CLEARED_CONTEXT_COMPATIBILITY','status':'GAP',
 'detail':'Qualified ResponsesReasoning.run requires full binding.model_context(), including local-only gate/state; it rejects the selected minimum context.'}]
profile['qualification_state']='PD05 accepted; transmission mechanism qualified; final selected context incompatible with current loop'
profile['architect_status']['PD-06']='UNRELEASED / final context compatibility failed'
ids={'authorization':'auth-e1-wp-001-r5-'+uuid.uuid4().hex,'session':'session-e1-'+uuid.uuid4().hex,'turn':'turn-e1-'+uuid.uuid4().hex}
profile['identity']['authorization']='auth-e1-wp-001-r5-<controller UUID4>';profile['identity']['allocated']=ids
profile['production_task_sha256']=sha(task.encode());profile['production_context_sha256']=sha(canonical(context).encode())
profile['content_clearance_sha256']=sha(canonical(manifest).encode())
profile['authority_sources']['current_supplement']='pd06_final_clearance/ARCHITECT_SELECTIONS.md'
profile['field_attribution']['model_transmission']={'classification':'Architect-selected','source':policy['authority_source']}
profile['field_attribution']['release_preconditions']={'classification':'verification failure, not unresolved authority','source':'VERIFICATION.json'}
auth=authorization(b,b,ids['authorization'],5,ids['session'],ids['turn']);auth=replace(auth,model_transmission=canonical(policy))
assert auth.state=='INACTIVE'
audit=Path('/tmp/kge-forge-e1-evidence')/ids['authorization']/ids['session']/ids['turn']/'controller.jsonl'
host=GovernedHost(auth,audit);runner=ResponsesReasoning(ReasoningOrchestrator(host))
assert host.scope is None and not host.invocations
# Offline exact-policy checks, no governed E1 operations or API/credential use.
observations=[]
for row in items:
 p=Path(row['canonical_path']);base=next((r for r in b.repos.values() if r==p or r in p.parents),p.parent)
 content=captured(p).decode(errors='replace')
 call={'name':'governed_read','arguments':json.dumps({'repository':str(base),'path':str(p.relative_to(base)),'limit':65536})}
 result=runner.transmission.result(call,{'result':'SUCCEEDED','data':{'path':str(p),'content':content}})
 expected=row['classification']=='TRANSMIT' and row['designation']=='COMPLETE_FILE'
 assert (result['transmission']=='CLEARED')==expected,row['canonical_path']
 if row['classification']=='TRANSMIT': assert host._path(str(base),str(p.relative_to(base)))==p
 for name in ('governed_list','governed_search','governed_status','governed_exec','governed_write','governed_patch','finish_task','authority_expansion_request'):
  alt=runner.transmission.result({'name':name}, {'result':'SUCCEEDED','data':{'content':content,'hash':row['captured_sha256'],'error':content}})
  assert set(alt)=={'transmission','notice'} and alt['transmission']=='REDACTED'
 if expected:
  changed=runner.transmission.result(call,{'result':'SUCCEEDED','data':{'path':str(p),'content':content+'CHANGED'}})
  assert changed['transmission']=='REDACTED'
 observations.append({'path':str(p),'classification':row['classification'],'complete_read_projection':result['transmission'],
 'alternate_representations':'REDACTED','read_authority_checked':row['classification']=='TRANSMIT'})
assert runner.transmission.initial(task,context)=={'task':task,'context':context}
try:runner.transmission.initial(task+'\n',context)
except ValueError:pass
else:raise AssertionError('changed production task cleared')
try:runner.transmission.initial(task,b.model_context())
except ValueError:pass
else:raise AssertionError('local gate context cleared')
assert context!=b.model_context()
# Never set ACTIVE to test this mismatch. The required equality is explicit in
# the current qualified source; bind its bytes and exact incompatible values.
write('OFFLINE_TRANSMISSION_VERIFICATION.json',{'result':'PASS','method':'Controller-only evaluation of final policy against all captured inputs; no dispatch or API call',
 'observations':observations,'input_count':len(observations),'model_calls':0,'host_invocations':len(host.invocations),
 'E1_state':auth.state,'selected_initial_payload_allowed':True,'changed_task_denied':True,'legacy_gate_context_denied':True,
 'audit_path':str(audit)})
write('CONTEXT_COMPATIBILITY_FAILURE.json',{'result':'FAIL','source':'adapter/responses_orchestrator.py:110',
 'source_sha256':sha((ROOT/'adapter/responses_orchestrator.py').read_bytes()),
 'enforced_condition':'context == binding.model_context()',
 'required_context_sha256':digest(b.model_context()),'selected_context_sha256':digest(context),
 'incompatible_required_fields':['mandatory_sources includes local evidence identities','knowledge_status includes qualification/state assessments','prerequisites contains gate evidence/status','unresolved_issues contains controller dispatch state'],
 'reason':'The full required controller context is not cleared, and the qualified loop rejects the minimum selected context. No configurable projection exists.',
 'no_activation_or_model_call':True})
profile_hash=sha(canonical(profile).encode());write('PRODUCTION_PROFILE.json',profile)
record=dict(auth.__dict__);record['context_binding']={'capture_commit':b.capture_commit,'context_sha256':b.digest}
launch=dict(oldlaunch);launch.update({'schema':'E1-PRODUCTION-LAUNCH-PROPOSAL-5','profile_sha256':profile_hash,
 'authorization':record,'audit_destination':str(audit),'identity':profile['identity'],
 'model_transmission':policy,'production_task_sha256':sha(task.encode()),
 'production_context_sha256':sha(canonical(context).encode()),'clearance_manifest_sha256':sha(canonical(manifest).encode()),
 'state':'INACTIVE','RELEASED':False,'ELIGIBLE':False,'DISPATCHED':False,
 'launch_compatibility':'BLOCKED by fixed model_context equality requirement'})
write('PRODUCTION_LAUNCH_RECORD.json',launch)
print(json.dumps({'counts':counts,'profile_sha256':profile_hash,'task_sha256':sha(task.encode()),'transmit_sources':list(selected),'context_compatibility':'FAIL'}))
