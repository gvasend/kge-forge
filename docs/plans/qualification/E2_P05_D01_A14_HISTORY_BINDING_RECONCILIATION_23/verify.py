"""Read-only independent relationship/inventory/proposal reconstruction."""
import json,hashlib,runpy
from copy import deepcopy
from pathlib import Path
from adapter.planner import codec
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
runpy.run_path(str(O.parent/'E2_P05_D01_A14_RESOLUTION_MATERIALIZATION_21/verify.py'),run_name='__complete_sources_and_frozen_bindings__')
r=read(O/'snapshot-relationship.json');old=read(R/r['ORIGINAL_SOURCE']['path'])['canonical_content']['subject'];new=read(R/r['CORRECTED_SOURCE']['path'])['snapshot'];assert codec._wire(codec.snapshot_id(codec._unwire(old)))==r['ORIGINAL_A14_SNAPSHOT'] and codec._wire(codec.snapshot_id(codec._unwire(new)))==r['CORRECTED_A14_SNAPSHOT']
restored=deepcopy(new)
for change in r['CHANGED_FIELDS']:
 parts=change['POINTER'].split('/')[1:];v=restored
 for k in parts[:-1]:v=v[int(k)] if isinstance(v,list) else v[k]
 assert v[parts[-1]]==change['CORRECTED'];v[parts[-1]]=change['ORIGINAL']
assert restored==codec._wire(codec._unwire(old)) and len(r['CHANGED_FIELDS'])==3
h=read(O/'original-history-inventory.json');rows=read(R/h['RETAINED_BUNDLE_HISTORY_INVENTORY']['path'])['ROWS'];assert not any(x['END_STATE']==r['CORRECTED_A14_SNAPSHOT'] for x in rows+h['ADDITIONAL_NATIVE_JOURNALS_GENESIS'])
for entry in h['ADDITIONAL_NATIVE_JOURNALS_GENESIS']:
 p=entry['SOURCE'];assert sha((R/p['path']).read_bytes())==p['raw_sha256']
 raw=read(R/p['path'])
 for k in p['pointer'].split('/')[1:]:raw=raw[int(k)] if isinstance(raw,list) else raw[k.replace('~1','/').replace('~0','~')]
 if entry['TYPE']=='STANDALONE_NATIVE_EVENT_JOURNAL_NOT_FULL_BUNDLE':
  start=codec._wire(codec.snapshot_id(codec._unwire(raw['initial'])));assert start==entry['START_STATE'] and raw['events']==entry['EVENTS'];assert (raw['events'][-1]['after_snapshot'] if raw['events'] else start)==entry['END_STATE']
 else:assert codec._wire(codec.snapshot_id(codec._unwire(raw['current'])))==entry['END_STATE'] and raw['genesis_event']==entry['EVENTS'][0]
assert not any(x['EVENT']['after_snapshot']==r['CORRECTED_A14_SNAPSHOT'] for x in h['DIRECT_TERMINAL_EVENT_MATCHES'])
frame=read(O/'prospective-checkpoint-frame-proposal.json');assert frame['START_STATE']==frame['END_STATE']==r['CORRECTED_A14_SNAPSHOT'] and frame['OWNED_EVENT_SET']==[] and frame['OWNED_EVENT_COUNT']==0 and frame['LOCAL_APPEND_HEAD'] is None and frame['LOCAL_LEDGER_ROOT'] is None
subject=read(O/'bounded-history-decision-subject.json');b=dict(subject);identity=b.pop('SUBJECT_IDENTITY');assert identity=='qualification-A14-history-frame-v1:'+sha(canon(b)) and subject['SELECTED'] is False and subject['RETAINED_ORIGINAL_HISTORY_IDENTITY'] is None
for k in ['RETAINED_HISTORY_INVENTORY','EXACT_PROPOSED_MECHANISM','SNAPSHOT_RELATIONSHIP','ASSURANCE_CONSEQUENCES']:
 p=subject[k];assert sha((R/p['path']).read_bytes())==p['raw_sha256']
d=read(O/'bounded-history-decision-dossier.json');assert d['SELECTION']=='NOT_SELECTED' and d['SUBJECT_IDENTITY']==identity and sha((R/d['EXACT_SUBJECT']['path']).read_bytes())==d['EXACT_SUBJECT']['raw_sha256']
print(json.dumps({'STATUS':'PASS','ORIGINAL_SNAPSHOT':r['ORIGINAL_A14_SNAPSHOT'],'CORRECTED_SNAPSHOT':r['CORRECTED_A14_SNAPSHOT'],'NO_CORRECTED_TERMINAL_HISTORY':True,'ORIGINAL_TERMINAL_HISTORY_RECOVERED':False,'MECHANISM':'EXPLICIT_PROSPECTIVE_CHECKPOINT_HISTORY_FRAME','OWNED_EVENTS':0,'SUBJECT_IDENTITY':identity,'HISTORY_BINDING':'UNRESOLVED','RESOLVED':52,'UNRESOLVED':59,'POLICY_SELECTED':False,'REPLAY_SCOPE_SELECTED':False},sort_keys=True))
