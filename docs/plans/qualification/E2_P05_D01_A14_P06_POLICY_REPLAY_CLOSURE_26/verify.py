"""Fresh zero-event native candidate reconstruction and permutation checks."""
import json,hashlib,runpy
from dataclasses import replace
from pathlib import Path
from adapter.planner import codec,model,selector
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;Q=O.parent
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
runpy.run_path(str(Q/'E2_P05_D01_A14_CHECKPOINT_HISTORY_FRAME_24/verify.py'),run_name='__prior_frame_structural_verification__')
p=read(O/'p06-policy-binding.json');r=read(O/'replay-scope-binding.json');assert p['POLICY_BINDING_IDENTITY']=='qualification-A14-P06-policy-binding-v1:'+sha(canon(p['BINDING'])) and r['REPLAY_SCOPE_IDENTITY']=='qualification-A14-replay-scope-v1:'+sha(canon(r['BINDING']))
frame=read(Q/'E2_P05_D01_A14_CHECKPOINT_HISTORY_FRAME_24/prospective-checkpoint-frame.json')['FRAME'];snap=codec.decode_snapshot((R/frame['PROVENANCE']['SNAPSHOT_SOURCE']['path']).read_bytes());policy=selector.validate_policy(codec._unwire(p['BINDING']['SOURCE']),p['BINDING']['VERSION']);pins=tuple(codec._unwire(x) for x in frame['SOURCE_IDENTITIES'])
bundle=model.PersistenceBundle(initial=snap,events=(),current=snap,sources=pins,policy=policy.artifact,policy_version='E1-SELECTION-1-P06',scope='PARTIAL_HISTORICAL_REPLAY',dossier_materializations=())
raw=codec.bundle_bytes(bundle);codec._verify_sources(bundle,R);identity=codec._wire(codec._identity(raw,'planner-bundle-v1'));v=read(O/'bundle-validation.json');assert raw==(R/v['CANDIDATE']['path']).read_bytes() and identity==v['BUNDLE_ID']
permuted=replace(bundle,sources=tuple(reversed(pins)),initial=replace(snap,actions=tuple(reversed(snap.actions)),knowledge=tuple(reversed(snap.knowledge))),current=replace(snap,actions=tuple(reversed(snap.actions)),knowledge=tuple(reversed(snap.knowledge))))
assert codec.bundle_bytes(permuted)==raw
assert bundle.events==() and codec._replay(bundle)==snap
audit=read(O/'full-111-reference-audit.json');assert audit['TOTAL_RESOLVED']==56 and audit['TOTAL_UNRESOLVED']==55
print(json.dumps({'STATUS':'PASS_NATIVE_EMPTY_FRAME_BUNDLE','POLICY_BINDING_IDENTITY':p['POLICY_BINDING_IDENTITY'],'REPLAY_SCOPE_IDENTITY':r['REPLAY_SCOPE_IDENTITY'],'BUNDLE_ID':identity,'SNAPSHOT_ID':codec._wire(codec.snapshot_id(snap)),'UNORDERED_PERMUTATION':'PASS_IDENTICAL_BYTES','EVENT_COUNT':0,'SOURCE_COUNT':10,'RESOLVED':56,'UNRESOLVED':55,'SAVE_RESTORE_EXECUTED':False},sort_keys=True))
