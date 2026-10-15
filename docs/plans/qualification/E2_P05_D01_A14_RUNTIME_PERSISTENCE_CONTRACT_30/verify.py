"""Static contract reconstruction; never launches qualification processes."""
import json,hashlib,runpy
from pathlib import Path
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;Q=O.parent
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
runpy.run_path(str(Q/'E2_P05_D01_A14_COLD_READER_BINDING_CLOSURE_29/verify.py'),run_name='__prior_static_reader_contracts__')
i=read(O/'execution-input-manifest.json');assert i['EXPECTED_BYTES']==153602 and sha((R/i['NATIVE_BUNDLE_CANDIDATE']['path']).read_bytes())==i['BUNDLE_ID']['sha256']
for p in [i['WRITER_SOURCE'],i['READER_SOURCE'],i['P06_POLICY_BINDING'],i['REPLAY_SCOPE_BINDING'],i['FRAME']]:assert sha((R/p['path']).read_bytes())==p['raw_sha256']
sequence=read(O/'runtime-sequence.json');assert [x['POSITION'] for x in sequence['ORDERED_STEPS']]==list(range(1,21)) and sequence['EXPECTED_COLD_READERS']==24
guards=read(O/'runtime-guards.json');assert [x['ID'] for x in guards['GUARDS']]==['G1_SAVE_RETURN','G2_PUBLICATION_VERIFIED','G3_PERSISTED_HANDOFF','G4_WRITER_EXIT_OBSERVED','G5_READER_STARTED_FRESH','G6_RESTORE_VALIDATED','G7_REPLAY_VALIDATED'] and guards['CURRENT_SATISFIED_COUNT']==0
subject=read(O/'bounded-execution-decision-subject.json');body=dict(subject);identity=body.pop('SUBJECT_IDENTITY');assert identity=='qualification-A14-runtime-persistence-decision-v1:'+sha(canon(body)) and not subject['SELECTED']
for k in ['INPUT_MANIFEST','SEQUENCE','GUARDS','PROCESS_ISOLATION','ALLOWED_PROHIBITED_EFFECTS','FAILURE_CONTRACT','RETRY_CONTRACT','EXPECTED_EVIDENCE','POST_AUDIT']:
 p=subject[k];assert sha((R/p['path']).read_bytes())==p['raw_sha256']
d=read(O/'bounded-execution-decision-dossier.json');assert d['SELECTION']=='NOT_SELECTED' and d['SUBJECT_IDENTITY']==identity and sha((R/d['EXACT_SUBJECT']['path']).read_bytes())==d['EXACT_SUBJECT']['raw_sha256']
for target in i['SAVE_TARGETS']:assert not Path(target['TARGET_PATH']).exists()
print(json.dumps({'STATUS':'PASS_STATIC_EXECUTION_CONTRACT','SUBJECT_IDENTITY':identity,'BUNDLE_ID':i['BUNDLE_ID'],'ORDERED_SEQUENCE':[x['STEP'] for x in sequence['ORDERED_STEPS']],'GUARDS':guards['GUARDS'],'EXPECTED_EVIDENCE_IDENTITY':subject['EXPECTED_EVIDENCE']['raw_sha256'],'AUTHORITY_REQUIRED':True,'EXECUTION_READY':False,'CURRENT_OPERANDS':'58/53','RUNTIME_GUARDS':0},sort_keys=True))
