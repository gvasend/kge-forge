"""Independent evidence verifier: no save, restore or process launch."""
import json,hashlib,sys
from pathlib import Path
R=Path('/home/gvasend/app/kge-forge');E=Path(__file__).resolve().parent
sys.path.insert(0,str(R))
from adapter.planner import codec
C=R/'docs/plans/qualification/E2_P05_D01_A14_RUNTIME_PERSISTENCE_CONTRACT_30'
def load(p):return json.loads(Path(p).read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
s=load(C/'bounded-execution-decision-subject.json');sequence=load(C/'runtime-sequence.json');runtime=load(E/'runtime-results.json');pids=set();distribution={str(x):0 for x in [0,1,7,101]}
for expected,row in zip(sequence['EXECUTION_ROWS'],runtime['ROWS']):
 ws=expected['WRITER_SPEC'];rs=expected['READER_SPEC'];assert row['row']==expected['TARGET_ID'] and row['result']=='PASS'
 writer=row['writer'];assert writer['exit_code']==0 and writer['pid']==writer['value']['pid'];assert writer['value']['result'] is None
 native_returns=[x for x in writer['value']['observations'] if x['operation']=='codec.save_bundle'];assert len(native_returns)==1 and native_returns[0]['identity']==s['BUNDLE_ID'] and native_returns[0]['path']==ws['EXPECTED_TARGET']
 assert native_returns[0]['time_ns']<writer['value']['completed_ns']<writer['exit_observed_ns']
 target=Path(ws['EXPECTED_TARGET']);raw=target.read_bytes();assert len(raw)==153602 and sha(raw)==s['EXPECTED_HASH'] and not target.is_symlink()
 source=(R/ws['INPUT_SOURCE']['path']).read_bytes();assert raw==source
 bundle=codec._unwire(json.loads(raw)['bundle']);assert codec._wire(codec.bundle_id(bundle))==s['BUNDLE_ID']
 assert codec._wire(codec.snapshot_id(bundle.current))==rs['EXPECTED_SNAPSHOT_ID'];assert not bundle.events and not bundle.dossier_materializations
 handoff=Path(ws['HANDOFF_PATH']);assert sha(handoff.read_bytes())==rs['EXPECTED_HANDOFF_HASH'] and load(handoff)==rs['EXPECTED_HANDOFF_RECORD'];assert load(handoff)['WRITER_EXIT_CLAIMED_BY_RECORD'] is False
 assert sorted(p.name for p in target.parent.iterdir())==sorted([target.name,handoff.name]),'Unauthorized store output'
 ev=row['supervisor_evidence'];assert ev['writer_pid']==writer['pid'] and ev['writer_exit_observed_ns']==writer['exit_observed_ns'] and ev['writer_exit_code']==0 and ev['writer_exit_observed']
 assert all(ev[g] for g in rs['REQUIRED_GUARDS'])
 assert len(row['readers'])==12
 for slot,reader in zip(expected['READER_SCHEDULE'],row['readers']):
  p=reader['process'];v=p['value'];assert reader['seed']==slot['seed'] and reader['index']==slot['reader_index'];distribution[str(slot['seed'])]+=1
  assert p['exit_code']==0 and p['start_ns']>writer['exit_observed_ns'] and p['pid']==v['pid'] and v['pid']!=writer['pid'] and v['ppid']==p['supervisor_pid'] and v['seed']==str(slot['seed']) and v['pid'] not in pids;pids.add(v['pid'])
  result=v['result'];assert result['bundle_identity']==s['BUNDLE_ID'] and result['snapshot_identity']==rs['EXPECTED_SNAPSHOT_ID'];assert result['policy_version']==rs['EXPECTED_POLICY_VERSION'] and result['native_replay_scope']==rs['EXPECTED_NATIVE_REPLAY_SCOPE'] and result['event_count']==0 and result['failure'] is None
  observed=[x for x in v['observations'] if x['operation']=='codec.restore'];assert len(observed)==1;ob=observed[0]
  assert ob['snapshot_id']==ob['initial_id']==rs['EXPECTED_SNAPSHOT_ID'] and ob['policy']==rs['EXPECTED_POLICY_PIN'] and ob['events']==[]
  assert sorted(ob['sources'],key=codec.canonical_bytes)==sorted(rs['EXPECTED_SOURCE_PINS'],key=codec.canonical_bytes)
  assert reader['complete_comparison']=='PASS' and all(reader[g]=='PASS' for g in ['G5_READER_STARTED_FRESH','G6_RESTORE_VALIDATED','G7_REPLAY_VALIDATED'])
assert distribution=={'0':6,'1':6,'7':6,'101':6} and len(pids)==24
for path,h in load(E/'preservation-before.json').items():assert sha((R/path).read_bytes())==h,path
for control in runtime['NEGATIVE_CONTROLS']:assert control['rejected'] and not control['reader_started']
audit=load(E/'operand-post-audit.json');assert len(audit['ROWS'])==111 and audit['TOTAL_RESOLVED']+audit['TOTAL_UNRESOLVED']==111 and audit['TOTAL_RESOLVED']==58 and audit['TOTAL_UNRESOLVED']==53
assert load(E/'a16-conditional-audit.json')['A16_REFERENCES_RESOLVED']==0
print(json.dumps({'PASS':True,'ROWS':2,'SAVES':2,'READERS':24,'READERS_BY_SEED':distribution,'GUARD_CONTROLS':len(runtime['NEGATIVE_CONTROLS']),'OPERANDS':[58,53]},sort_keys=True))
