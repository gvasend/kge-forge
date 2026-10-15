"""Fresh structural source/contract verifier; bundle identity remains unsealed."""
import json,hashlib,runpy
from pathlib import Path
from adapter.planner import codec,selector
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
runpy.run_path(str(O.parent/'E2_P05_D01_A14_RESOLUTION_MATERIALIZATION_21/verify.py'),run_name='__prior_source_and_52_binding_verification__')
source=read(O/'frozen-ten-sources.json');assert len(source['ROWS'])==10
for row in source['ROWS']:
 raw=codec.load_pinned(R,codec._unwire(row['PIN']));assert sha(raw)==row['BYTE_HASH']
policy=read(O/'policy-contract-and-candidates.json')
for row in policy['CANDIDATES']:
 b=selector.validate_policy(codec._unwire(row['SOURCE_PIN']),row['VERSION']);assert sha(selector.policy_contract_bytes(b))==row['SEMANTIC_CONTRACT_HASH'];assert row['SELECTED'] is False
histories=read(O/'retained-history-candidates.json');assert histories['EXACT_CORRECTED_A14_END_COUNT']==sum(r['EXACT_CORRECTED_A14_END'] for r in histories['ROWS'])==0
assert all(r['END_STATE']!=source['SNAPSHOT_IDENTITY'] for r in histories['ROWS'])
result=read(O/'bundle-closure-result.json');assert result['A14_BUNDLE_CONTRACT']=='FAIL' and result['A14_BUNDLE_IDENTITY'] is None and not result['SAVE_PREFLIGHT_ELIGIBLE']
for k in ['INITIAL_STATE_CONTRACT','POLICY_CONTRACT','ORDERED_HISTORY_CONTRACT','REPLAY_SCOPE_CONTRACT']:
 p=result[k];assert sha((R/p['path']).read_bytes())==p['raw_sha256']
refs=read(O/'full-111-reference-audit.json');assert len(refs['ROWS'])==111 and refs['TOTAL_RESOLVED']==52 and refs['TOTAL_UNRESOLVED']==59
print(json.dumps({'STATUS':'PASS_SOURCE_AND_UNRESOLVED_CONTRACT_DETERMINISM','SOURCE_CLOSURE':'10/10','SNAPSHOT_IDENTITY':source['SNAPSHOT_IDENTITY'],'POLICY_CANDIDATES':2,'EXACT_HISTORY_CANDIDATES':0,'A14_BUNDLE_IDENTITY':None,'BUNDLE_IDENTITY_DETERMINISM':'NOT_RUN_NO_BUNDLE','FIRST_REMAINING_BLOCKER':'HISTORY_BINDING','RESOLVED':52,'UNRESOLVED':59,'NATIVE_OPERATIONS_EXECUTED':0},sort_keys=True))
