"""Independent expected byte/target reconstruction; no save/read transaction."""
import json,hashlib,runpy
from dataclasses import replace
from pathlib import Path
from adapter.planner import codec
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;Q=O.parent
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
runpy.run_path(str(Q/'E2_P05_D01_A14_P06_POLICY_REPLAY_CLOSURE_26/verify.py'),run_name='__exact_native_candidate_and_frozen_52__')
c=read(O/'save-contract.json');input=read(O/'save-input-pin.json');p=R/input['INPUT_SOURCE']['path'];raw=p.read_bytes();assert sha(raw)==input['INPUT_SOURCE']['raw_sha256'];bundle=codec._unwire(read(p)['bundle']);expected=codec.bundle_bytes(bundle);assert expected==raw and len(expected)==c['EXPECTED_SAVE_BYTE_LENGTH'] and sha(expected)==c['EXPECTED_SAVE_HASH']==c['EXPECTED_NATIVE_IDENTITY']['sha256'];codec._verify_sources(bundle,R)
assert expected==(R/c['EXPECTED_REPRESENTATION']['path']).read_bytes()
targets=read(Q/'E2_P05_D01_A14_HANDOFF_CLOSURE_5/save-contract.json')['SAVE_TARGETS'];paths=[]
for t in c['SAVE_TARGETS']:
 directory=Path(targets[t['OBLIGATION_ID']]['DIRECTORY']);target=directory/('bundle-'+sha(expected)+'.json');assert str(target)==t['EXPECTED_TARGET'] and directory.resolve()==directory and not target.is_symlink()
 assert target.exists()==t['TARGET_CURRENTLY_EXISTS'];assert not target.exists() or target.read_bytes()==raw;paths.append(str(target))
assert codec.bundle_bytes(replace(bundle,sources=tuple(reversed(bundle.sources))))==raw
assert input['INPUT_BUNDLE_ID']==c['EXPECTED_NATIVE_IDENTITY'] and sha((R/c['NATIVE_SOURCE']['path']).read_bytes())==c['NATIVE_SOURCE']['raw_sha256']
front=read(O/'operand-frontier.json');assert len(front['FROZEN_52'])+len(front['PREVIOUS_BUNDLE_RESOLUTIONS'])+len(front['RESOLVED_BY_SAVE_CONTRACT_ROWS'])+len(front['UNRESOLVED'])==111 and front['TOTAL_RESOLVED']==58 and front['TOTAL_UNRESOLVED']==53
print(json.dumps({'STATUS':'PASS_STATIC_SAVE_RECONSTRUCTION','INPUT_BUNDLE_ID':input['INPUT_BUNDLE_ID'],'EXPECTED_SAVE_IDENTITY':c['EXPECTED_NATIVE_IDENTITY'],'EXPECTED_BYTES':len(expected),'EXPECTED_HASH':sha(expected),'EXPECTED_TARGETS':paths,'UNORDERED_SOURCE_PRESENTATION':'IDENTICAL_BYTES','RESOLVED':58,'UNRESOLVED':53,'SAVES_PERFORMED':0,'NEXT_BLOCKER':'WRITER_TERMINATION'},sort_keys=True))
