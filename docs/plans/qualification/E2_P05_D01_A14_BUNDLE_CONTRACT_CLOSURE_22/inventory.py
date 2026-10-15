"""Retained state/history inventory. No replay/apply/recompute/bundle creation."""
import json,hashlib,subprocess
from pathlib import Path
from adapter.planner import codec,model
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p,ptr=''):return {'path':str(p.relative_to(R)),'pointer':ptr,'raw_sha256':sha(p.read_bytes())}
def save(n,v):(O/n).write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
source=O.parent/'E2_P05_D01_A14_PROVENANCE_FIXTURE_CORRECTION_7/corrected-prospective-snapshot.json';wanted=codec.decode_snapshot(source.read_bytes());wid=codec._wire(codec.snapshot_id(wanted));cache={};states={};histories=[];errors=[];files=[]
def snapshotinfo(w):
 key=sha(codec.canonical_bytes(w))
 if key in cache:return cache[key]
 try:
  s=codec._unwire(w);sid=codec._wire(codec.snapshot_id(s));valid=True;error=None
  try:model.validate_model(s)
  except (ValueError,TypeError) as e:valid=False;error=str(e)
  context=codec._wire(s.context) if s.context else None
  if sid==wid:classification='EXACT_MATCH'
  elif not valid:classification='OTHER'
  elif context and context['scope']!=wanted.context.scope:classification='WRONG_SCOPE'
  elif context and context['generation']!=wanted.context.generation:classification='WRONG_GENERATION'
  elif sid['sha256']=='91017c3947096a0470ba44aff95901872768fa205205d39c7bf60f840f848c9c':classification='SEMANTIC_MATCH'
  else:classification='WRONG_BOUNDARY'
  info={'STATE_ID':sid,'CLASSIFICATION':classification,'CONTEXT':context,'STRUCTURAL_VALIDATION':'PASS' if valid else 'FAIL','STRUCTURAL_ERROR':error,'EXTERNAL_RULE_KNOWN':[r.rule_known for r in s.evidence_requirements],'ACTION_STATES':codec._wire(s.statuses),'KNOWLEDGE_IDS':[k.id.value for k in s.knowledge]}
 except (ValueError,TypeError,KeyError) as e:info={'STATE_ID':None,'CLASSIFICATION':'OTHER','STRUCTURAL_VALIDATION':'FAIL','STRUCTURAL_ERROR':str(e)}
 cache[key]=info;return info
paths=subprocess.run(['rg','--files','docs/plans'],cwd=str(R),capture_output=True,text=True,check=True).stdout.splitlines()
for name in sorted(paths):
 p=R/name
 if p.suffix!='.json' or O in p.parents or p.is_symlink():continue
 raw=p.read_bytes()
 if b'E2-' not in raw and b'PLANNER-BUNDLE-1' not in raw:continue
 try:v=json.loads(raw)
 except ValueError:continue
 pp=pin(p);files.append(pp)
 def walk(v,ptr=''):
  if isinstance(v,dict):
   if v.get('$type')=='Snapshot':
    info=snapshotinfo(v);key=sha(codec.canonical_bytes(v))
    if key not in states:states[key]={**info,'CONTENTS':v,'SOURCES':[],'QUALIFICATION_STATUS':'Retained native state; structural validity does not establish D01 applicability'}
    states[key]['SOURCES'].append({**pp,'pointer':ptr})
   if all(k in v for k in ['initial','current','events','sources','policy','policy_version','scope']) and isinstance(v['initial'],dict) and v['initial'].get('$type')=='Snapshot':
    initial=snapshotinfo(v['initial']);current=snapshotinfo(v['current']);previous=None;parent=initial['STATE_ID'];chain=[];status=True
    for i,e in enumerate(v['events'],1):
     ok=e.get('sequence')==i and e.get('parent_snapshot')==parent and e.get('parent_event')==previous
     try:
      native=codec._unwire(e);ok=ok and codec._wire(codec._event_identity(native.sequence,native.parent_snapshot,native.parent_event,native.result,native.after_snapshot,native.resume_binding))==e['identity']
     except (ValueError,TypeError,KeyError,AttributeError):ok=False
     chain.append({'POSITION':i,'EVENT_ID':e.get('identity'),'PARENT_SNAPSHOT':e.get('parent_snapshot'),'PARENT_EVENT':e.get('parent_event'),'AFTER_SNAPSHOT':e.get('after_snapshot'),'EVENT_TYPE':e.get('result',{}).get('$type'),'METADATA_CHAIN_VALID':ok});status=status and ok;previous=e.get('identity');parent=e.get('after_snapshot')
    endpoint=parent==current['STATE_ID'];exact=current['STATE_ID']==wid
    histories.append({'SOURCE':{**pp,'pointer':ptr},'RETAINED_CANONICAL_ENVELOPE_COMPARISON_HASH':sha(codec.canonical_bytes({'schema':'PLANNER-BUNDLE-1','bundle':v})),'START_STATE':initial['STATE_ID'],'END_STATE':current['STATE_ID'],'INITIAL_CLASSIFICATION':initial['CLASSIFICATION'],'CURRENT_CLASSIFICATION':current['CLASSIFICATION'],'EVENT_COUNT':len(chain),'EVENTS':chain,'LEDGER_ROOT':chain[0]['EVENT_ID'] if chain else None,'APPEND_HEAD':previous,'LEDGER_METADATA_VALID':status and endpoint,'POLICY_PIN':v['policy'],'POLICY_VERSION':v['policy_version'],'REPLAY_SCOPE':v['scope'],'SOURCE_PINS':v['sources'],'CONTEXT':current.get('CONTEXT'),'EXACT_CORRECTED_A14_END':exact,'CLASSIFICATION':'EXACT_MATCH' if exact and status and endpoint else 'WRONG_GENERATION' if current['CLASSIFICATION']=='WRONG_GENERATION' else 'WRONG_BOUNDARY','NATIVE_REPLAY_NOT_RUN':True})
   for k,x in v.items():walk(x,ptr+'/'+k.replace('~','~0').replace('/','~1'))
  elif isinstance(v,list):
   for i,x in enumerate(v):walk(x,ptr+'/'+str(i))
 walk(v)
save('retained-state-candidates.json',{'COUNT':len(states),'ROWS':[states[k] for k in sorted(states)],'REQUIRED_A14_CURRENT_SNAPSHOT':wid,'BOUNDARY_NOTE':'Exact current Snapshot occurrences do not select native bundle.initial; original 91017 source is only semantic provenance predecessor, never byte/native-ID substitute'})
save('retained-history-candidates.json',{'COUNT':len(histories),'EXACT_CORRECTED_A14_END_COUNT':sum(h['EXACT_CORRECTED_A14_END'] for h in histories),'ROWS':histories,'ORDERING':'Exact native sequence, parent_snapshot, parent_event, identity and after_snapshot links; no report chronology used','LIMIT':'Metadata/identity checks only; no event application or historical replay'})
save('inventory-search.json',{'SCOPE':'All JSON under docs/plans selected by E2 marker or native PLANNER-BUNDLE-1; includes native Snapshots nested in bundles/reports/fixtures. E1 remains read-only and is not a source of foreign E2 history. New package excluded.','FILES':files,'COUNT':len(files),'STATE_BODY_CACHE':len(cache)})
print(json.dumps({'STATE_VARIANTS':len(states),'BUNDLE_HISTORY_CANDIDATES':len(histories),'EXACT_A14_NATIVE_BUNDLE_ENDS':sum(h['EXACT_CORRECTED_A14_END'] for h in histories)}))
