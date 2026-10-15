"""Static reader/spec/oracle reconstruction; run_reader is not imported or launched."""
import json,hashlib,ast,runpy
from pathlib import Path
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;Q=O.parent
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
runpy.run_path(str(Q/'E2_P05_D01_A14_WRITER_HANDOFF_CLOSURE_28/verify.py'),run_name='__prior_guarded_contract_verification__')
process=read(O/'reader-process-contract.json');restore=read(O/'native-restore-and-replay-contract.json');output=read(O/'reader-output-and-success-contract.json');fail=read(O/'reader-failure-contract.json');specs=[read(O/n) for n in ['reader-spec-operands.json','reader-spec-oracle.json']];oracle=read(O/'expected-restored-identity-oracle.json')
for spec in specs:
 assert spec['EXPECTED_BUNDLE_ID']==oracle['BUNDLE_ID'] and spec['EXPECTED_SNAPSHOT_ID']==oracle['SNAPSHOT_ID'] and spec['EXPECTED_SOURCE_PINS']==oracle['SOURCE_PINS'] and len(spec['EXPECTED_SOURCE_PINS'])==10
 assert spec['EXPECTED_POLICY_VERSION']=='E1-SELECTION-1-P06' and spec['EXPECTED_NATIVE_REPLAY_SCOPE']=='PARTIAL_HISTORICAL_REPLAY' and not spec['RUNTIME_GUARDS_SATISFIED_NOW']
 assert not Path(spec['TARGET_PATH']).exists() and not Path(spec['HANDOFF_PATH']).exists()
 assert sha(canon(spec['EXPECTED_HANDOFF_RECORD']))==spec['EXPECTED_HANDOFF_HASH']
p=process['ENTRYPOINT_SOURCE'];assert sha((R/p['path']).read_bytes())==p['raw_sha256'];tree=ast.parse((R/p['path']).read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run_reader');calls=[ast.dump(n) for n in ast.walk(fn) if isinstance(n,ast.Call)];assert any("attr='restore'" in c for c in calls) and not any("attr='save_bundle'" in c or "attr='recompute'" in c for c in calls)
identity='qualification-A14-cold-reader-contract-v1:'+sha(canon({'specs':specs,'process':process,'restore':restore,'output':output,'failures':fail}));assert identity==read(O/'reader-contract-identity.json')['IDENTITY']
assert read(O/'guard-order-and-ownership.json')['GUARDS_SATISFIED_COUNT']==0
print(json.dumps({'STATUS':'PASS_STATIC_READER_CONTRACT','CONTRACT_IDENTITY':identity,'EXPECTED_IDENTITIES':oracle,'TARGETS':[s['TARGET_PATH'] for s in specs],'HASH_SEEDS':process['HASH_SEEDS'],'RUNTIME_GUARDS_SATISFIED':0,'READER_LAUNCHED':False,'RESOLVED':58,'UNRESOLVED':53},sort_keys=True))
