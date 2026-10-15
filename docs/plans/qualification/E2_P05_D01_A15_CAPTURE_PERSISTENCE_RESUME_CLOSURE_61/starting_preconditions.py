"""Non-effecting queries of retained BEFORE metadata only; no replay/restore."""
import pathlib,sys,json,dataclasses,enum
sys.path.insert(0,str(pathlib.Path('.').resolve()))
from adapter.planner import codec,core,typed_proofs
E=pathlib.Path(__file__).parent
f=json.loads((E.parent/'E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2/fixtures/D01-VARIANT__E2-A15__CANONICAL_REQUIRED_BEHAVIOR.json').read_text());state=codec._unwire(f['canonical_content']['bundle']['current'])
def normal(v):
 if codec.TYPES.get(type(v).__name__) is type(v):return codec._wire(v)
 if isinstance(v,enum.Enum):return {'$enum':type(v).__name__,'value':v.value}
 if dataclasses.is_dataclass(v):return {'qualification_type':type(v).__name__,**{x.name:normal(getattr(v,x.name)) for x in dataclasses.fields(v)}}
 if isinstance(v,(tuple,list)):return [normal(x) for x in v]
 return v
comp=core.recompute(state);proofs=[{'proof':codec._wire(p.id),'usable':typed_proofs.usable(state,p)} for p in state.typed_proofs]
assert comp.control.value=='RUNNABLE' and [a.value for a in comp.actionable]==['E2-FINISH'] and all(p['usable'] for p in proofs)
record={'BEFORE_SNAPSHOT':codec._wire(codec.snapshot_id(state)),'EXPECTED_BEFORE_COMPUTATION':normal(comp),'EXPECTED_BEFORE_TYPED_PROOF_USABILITY':proofs,'AFTER_QUERIES_CALLED':False,'INITIAL_RESTORE_EXECUTED':False,'NATIVE_EFFECTS':0,'FUTURE_STARTING_COMPARISON':'Immediately after initial native restore, compare full bundle/current Snapshot and this complete recomputation/usability list before record_result'}
(E/'starting-state-precondition-oracle.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
print(json.dumps({'BEFORE_CONTROL':comp.control.value,'PROOFS_USABLE':len(proofs),'FINISH_ACTIONABLE':True,'NATIVE_EFFECTS':0}))
