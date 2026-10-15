"""Independent frame reconstruction and fresh structural reader."""
import json,hashlib,runpy
from pathlib import Path
from adapter.planner import codec,model,replay,selector
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;Q=O.parent
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def pin(p):return {'path':str(p.relative_to(R)),'raw_sha256':sha(p.read_bytes())}
runpy.run_path(str(Q/'E2_P05_D01_A14_RESOLUTION_MATERIALIZATION_21/verify.py'),run_name='__sources_and_frozen_operand_reader__')
s=read(Q/'E2_P05_D01_A14_HISTORY_BINDING_RECONCILIATION_23/bounded-history-decision-subject.json');proposal=read(R/s['EXACT_PROPOSED_MECHANISM']['path']);sp=R/proposal['SNAPSHOT_SOURCE']['path'];assert sha(sp.read_bytes())==proposal['SNAPSHOT_SOURCE']['raw_sha256'];snap=codec.decode_snapshot(sp.read_bytes());model.validate_model(snap);sid=codec._wire(codec.snapshot_id(snap));assert sid==s['CORRECTED_SNAPSHOT_ID']
rows=read(Q/'E2_P05_D01_A14_RESOLUTION_MATERIALIZATION_21/complete-source-validation.json')['ROWS'];pins=[]
for r in rows:assert sha(codec.load_pinned(R,codec._unwire(r['PIN'])))==r['SHA256'];pins.append(r['PIN'])
expected={'FRAME_TYPE':'PROSPECTIVE_ZERO_EVENT_CHECKPOINT','CHECKPOINT_STATE':sid,'INITIAL_STATE':sid,'EXPECTED_CURRENT_STATE':sid,'EVENT_COLLECTION':[],'EVENT_COUNT':0,'HISTORICAL_PARENT':None,'LOCAL_LEDGER_ROOT':None,'LOCAL_APPEND_HEAD':None,'HISTORICAL_OCCURRENCE_CLAIM':False,'HISTORICAL_ANCESTRY_CLAIM':False,'SOURCE_ROOT':str(R),'SOURCE_IDENTITIES':sorted(pins,key=canon),'SCOPE':snap.context.scope,'LINEAGE':snap.context.lineage,'GENERATION':snap.context.generation,'PROVENANCE':{'AUTHORIZATION_SUBJECT':s['SUBJECT_IDENTITY'],'SNAPSHOT_SOURCE':proposal['SNAPSHOT_SOURCE'],'SOURCE_SET_VALIDATION':pin(Q/'E2_P05_D01_A14_RESOLUTION_MATERIALIZATION_21/complete-source-validation.json'),'NATIVE_SNAPSHOT_PROVENANCES':sorted([codec._wire(p) for p in replay.provenance_records(snap)],key=canon)},'HISTORICAL_EXCLUSIONS':{'ORIGINAL_A14_HISTORY_PROVEN':False,'CORRECTED_SNAPSHOT_IS_HISTORICAL_TERMINAL':False,'ORIGINAL_HISTORY_REWRITTEN':False,'ORIGINAL_HISTORY_REPINNED':False,'PROSPECTIVE_FRAME_IS_ORIGINAL_HISTORY':False},'IDENTITY_DOMAIN':'QUALIFICATION_ONLY_NOT_NATIVE_EVENT_LEDGER_OR_BUNDLE','POLICY_VERSION_SELECTED':False,'REPLAY_SCOPE_SELECTED':False}
packet=read(O/'prospective-checkpoint-frame.json');assert expected==packet['FRAME'];identity='qualification-A14-checkpoint-frame-v1:'+sha(canon(expected));assert identity==packet['FRAME_IDENTITY']
for row in read(O/'policy-reentry.json')['CANDIDATES']:
 b=selector.validate_policy(codec._unwire(row['SOURCE_PIN']),row['VERSION']);assert sha(selector.policy_contract_bytes(b))==row['SEMANTIC_CONTRACT_SHA256'] and row['SELECTED'] is False
assert not read(O/'policy-reentry.json')['POLICY_VERSION_SELECTED'] and not read(O/'replay-scope-reentry.json')['REPLAY_SCOPE_SELECTED']
assert read(O/'operand-frontier.json')['TOTAL_RESOLVED']==52 and read(O/'operand-frontier.json')['TOTAL_UNRESOLVED']==59
print(json.dumps({'STATUS':'PASS','FRAME_IDENTITY':identity,'SNAPSHOT_IDENTITY':sid,'SOURCE_IDENTITIES':expected['SOURCE_IDENTITIES'],'EVENT_COLLECTION':[],'EVENT_COUNT':0,'POLICY_SELECTED':False,'REPLAY_SCOPE_SELECTED':False,'SOURCE_CLOSURE':'10/10','RESOLVED':52,'UNRESOLVED':59},sort_keys=True))
