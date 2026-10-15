"""Independent native binding/configuration comparison; no policy choice."""
import json,hashlib,runpy
from pathlib import Path
from adapter.planner import codec,selector
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
runpy.run_path(str(O.parent/'E2_P05_D01_A14_CHECKPOINT_HISTORY_FRAME_24/verify.py'),run_name='__frame_source_and_frozen_binding_verification__')
rows=read(O/'candidate-inventory.json')['ROWS'];configs=[]
for row in rows:
 b=selector.validate_policy(codec._unwire(row['SOURCE']),row['VERSION']);raw=codec.load_pinned(R,b.artifact);config=json.loads(selector.policy_contract_bytes(b));assert config==row['CONFIGURATION'] and sha(raw)==row['SOURCE_SHA256'] and sha(selector.policy_contract_bytes(b))==row['CONFIGURATION_IDENTITY']['SHA256'];assert row['SELECTED'] is False;configs.append(config)
assert [k for k in configs[0] if configs[0][k]!=configs[1][k]]==['version']
comparison=read(O/'p05-p06-comparison.json');assert comparison['P05_P06_RELATIONSHIP']=='SAME_POLICY_DIFFERENT_VERSION' and comparison['SELECTOR_ALGORITHM_EQUAL']
subject=read(O/'bounded-policy-decision-subject.json');s=dict(subject);identity=s.pop('SUBJECT_IDENTITY');assert identity=='qualification-A14-policy-decision-v1:'+sha(canon(s)) and not subject['POLICY_VERSION_SELECTED'] and not subject['REPLAY_SCOPE_SELECTED']
for key in ['FRAME_SOURCE','COMPARISON','SELECTION_ANALYSIS','REPLAY_SCOPE_PREPARATION']:
 p=subject[key];assert sha((R/p['path']).read_bytes())==p['raw_sha256']
for p in subject['RUNTIME_PINS'].values():assert sha((R/p['path']).read_bytes())==p['raw_sha256']
d=read(O/'bounded-policy-decision-dossier.json');assert d['SELECTION']=='NOT_SELECTED' and d['SUBJECT_IDENTITY']==identity and sha((R/d['EXACT_SUBJECT']['path']).read_bytes())==d['EXACT_SUBJECT']['raw_sha256']
assert read(O/'selection-rule-and-authority.json')['POLICY_BINDING_UNIQUE'] is False
print(json.dumps({'STATUS':'PASS','CANDIDATE_IDENTITIES':[{'version':r['VERSION'],'content':r['CONTENT_IDENTITY'],'configuration':r['CONFIGURATION_IDENTITY']} for r in rows],'RELATIONSHIP':'SAME_POLICY_DIFFERENT_VERSION','ONLY_CONFIG_DIFFERENCE':'version','COMPATIBLE':[True,True],'POLICY_BINDING_UNIQUE':False,'SUBJECT_IDENTITY':identity,'POLICY_SELECTED':False,'REPLAY_SELECTED':False,'RESOLVED':52,'UNRESOLVED':59},sort_keys=True))
