"""Fail-closed handoff metadata negatives; no writer, reader, or state mutation."""
import json
from copy import deepcopy
from pathlib import Path
O=Path(__file__).resolve().parent
base=json.loads((O/'handoff-manifest.json').read_bytes())
class Reject(ValueError):pass
def validate(v):
 if v['STATUS']!='BLOCKED_NON_EXECUTABLE_CONTRACT_MANIFEST':raise Reject('UNSATISFIABLE_SOURCE_CANNOT_BE_PROMOTED')
 if v['NATIVE_SAVE_PERFORMED'] or v['READER_LAUNCHED']:raise Reject('OPERATION_FORBIDDEN')
 if v!=base:raise Reject('SEALED_BOUNDARY_SOURCE_IDENTITY_PHASE_OR_PROCESS_CONTRACT_DRIFT')
 return True
validate(base);rows=[]
def check(name,mutate):
 v=deepcopy(base);mutate(v)
 try:validate(v)
 except Reject as e:rows.append({'CASE':name,'STATUS':'REJECTED','REASON':str(e)})
 else:raise AssertionError(name)
check('wrong A14 source',lambda v:v.update(A14_SOURCE={'report_path':'WRONG'}))
check('wrong pre-state',lambda v:v.update(WRITER_INPUT_BOUNDARY={'post_operation':True}))
check('wrong operation',lambda v:v.update(OPERATION='admit_external_evidence'))
check('wrong bundle type',lambda v:v.update(BUNDLE_CONTRACT={'type':'GenesisBoundBundle'}))
check('wrong Snapshot',lambda v:v.update(SNAPSHOT_IDENTITY='WRONG'))
check('wrong bundle identity domain',lambda v:v.update(SAVE_IDENTITY_VALUE={'namespace':'planner-snapshot-v1'}))
check('wrong save target',lambda v:v.update(SAVE_TARGETS={'output_dir':'docs/experiments/E1'}))
check('wrong save format',lambda v:v.update(SAVE_FORMAT='REPORT-ONLY'))
check('wrong save identity',lambda v:v.update(SAVE_IDENTITY_VALUE={'sha256':'0'*64}))
check('reader before save completion',lambda v:v['WRITER_TERMINATION'].update(BARRIER='before save return'))
check('reader before writer termination',lambda v:v['WRITER_TERMINATION'].update(BARRIER='writer still running'))
check('warm reader substituted for cold reader',lambda v:v['WRITER_TERMINATION'].update(ISOLATION='same interpreter'))
check('wrong reader source',lambda v:v.update(READER_SOURCE={'path':'wrong-bundle.json'}))
check('report substituted for bundle',lambda v:v.update(READER_SOURCE={'path':'handoff-manifest.json'}))
check('wrong reader entrypoint',lambda v:v['READER_ENTRYPOINT'].update(ENTRYPOINT='adapter.planner.codec.decode_snapshot'))
check('wrong reader operand',lambda v:v['READER_OPERANDS'][1].update(CLASS='DERIVED_FROM_UNTRUSTED_BUNDLE'))
check('wrong ledger root/head',lambda v:v.update(LEDGER_VALUES={'root':'WRONG','head':'WRONG'}))
check('wrong scope',lambda v:v['SCOPE_LINEAGE_GENERATION'].update(scope='PRODUCTION'))
check('wrong lineage',lambda v:v['SCOPE_LINEAGE_GENERATION'].update(lineage='OTHER'))
check('wrong provenance',lambda v:v.update(PROVENANCE=[]))
check('future post-state supplied as invocation input',lambda v:v.update(WRITER_INPUT_BOUNDARY={'future_result':'post_state'}))
check('A14 pre/post boundary swap',lambda v:v.update(POST_STATE_CONTRACT='PRE_STATE_IS_READER_OUTPUT'))
check('blocked source closure promoted to ready',lambda v:v.update(STATUS='READY'))
result={'STATUS':'PASS_23_FAIL_CLOSED_METADATA_GUARDS','COUNT':len(rows),'ROWS':rows,'LIMITATION':'Guards preserve the recovered BLOCKED contract and reject promotion/substitution. They are not a passing executable handoff validator or native qualification negatives.','QUALIFICATION_CASES_EXECUTED':0,'SAVES_PERFORMED':0,'COLD_READERS_EXECUTED':0}
(O/'negative-suite.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print('HANDOFF_METADATA_NEGATIVES=23/23; EXECUTABLE_HANDOFF=BLOCKED')
