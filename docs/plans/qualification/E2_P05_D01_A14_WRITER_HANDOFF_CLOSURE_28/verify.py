"""Fresh static contract reconstruction; future writer callable never invoked."""
import json,hashlib,ast,runpy
from pathlib import Path
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;Q=O.parent
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
runpy.run_path(str(Q/'E2_P05_D01_A14_SAVE_CONTRACT_CLOSURE_27/verify.py'),run_name='__prior_static_save_verification__')
targets=read(O/'two-targets-and-guarded-handoff.json')['ROWS'];boundary=read(O/'writer-termination-boundary.json');prereqs=read(O/'cold-reader-prerequisites.json');order=[r['STEP'] for r in read(O/'future-execution-order-and-retries.json')['ORDERED_STEPS']]
for row in targets:
 raw=canon(row['EXPECTED_RECORD']);assert len(raw)==row['EXPECTED_HANDOFF_BYTE_LENGTH'] and sha(raw)==row['EXPECTED_HANDOFF_HASH']
 assert not row['PRESENT_AS_RUNTIME_QUALIFICATION_FACT'];assert Path(row['HANDOFF_PATH']).exists()==row['ACTUAL_HANDOFF_FILE_EXISTS'];assert not Path(row['TARGET_PATH']).exists()
 assert row['EXPECTED_RECORD']['WRITER_EXIT_CLAIMED_BY_RECORD'] is False
w=read(O/'writer-contract.json');assert sha((R/w['SOURCE']['path']).read_bytes())==w['SOURCE']['raw_sha256'];tree=ast.parse((R/w['SOURCE']['path']).read_text());fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='run_writer');calls=[ast.dump(x) for x in ast.walk(fn) if isinstance(x,ast.Call)];assert any("attr='save_bundle'" in c for c in calls) and not any("attr='restore'" in c or "attr='recompute'" in c for c in calls)
identity='qualification-A14-persisted-handoff-contract-v1:'+sha(canon({'targets':targets,'boundary':boundary,'prerequisites':prereqs,'ordered_steps':order}));assert identity==read(O/'static-preflight.json')['HANDOFF_CONTRACT_IDENTITY']
front=read(O/'operand-frontier.json');assert front['TOTAL_RESOLVED']==58 and front['TOTAL_UNRESOLVED']==53 and not front['GUARDED_DEPENDENCIES_SATISFIED_NOW']
assert not prereqs['HEAD_REQUIRED'] and not prereqs['DIRECTORY_FSYNC_REQUIRED'] and not prereqs['RUNTIME_PREREQUISITES_OCCURRED']
print(json.dumps({'STATUS':'PASS_STATIC_WRITER_HANDOFF','HANDOFF_CONTRACT_IDENTITY':identity,'TARGET_COMMITMENTS':[{'id':t['TARGET_ID'],'path':t['TARGET_PATH'],'bundle_id':t['EXPECTED_BUNDLE_ID'],'guard':t['GUARD_CONDITION'],'handoff_hash':t['EXPECTED_HANDOFF_HASH']} for t in targets],'TERMINATION_BOUNDARY':boundary,'READER_PREREQUISITES':prereqs,'RUNTIME_GUARDS_MET':False,'RESOLVED':58,'UNRESOLVED':53,'SAVES_PERFORMED':0,'QUALIFICATION_WRITERS_TERMINATED':0},sort_keys=True))
