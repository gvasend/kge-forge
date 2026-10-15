import dataclasses,enum,hashlib,json,os,pathlib,subprocess,sys
ROOT=pathlib.Path.cwd();D=ROOT/'docs/plans';P='DETERMINISTIC_PLANNER_V0_1_'
from adapter.planner import codec as c,model as m
from adapter.planner.core import recompute,apply_event
from adapter.planner.genesis_bundle import decode_bundle,encode_bundle,bundle_identity

def wire(x):
 if isinstance(x,enum.Enum):return {'type':type(x).__name__,'value':x.value}
 if dataclasses.is_dataclass(x):return {'type':type(x).__name__,**{f.name:wire(getattr(x,f.name))for f in dataclasses.fields(x)}}
 if isinstance(x,(tuple,list)):return [wire(v)for v in x]
 if isinstance(x,dict):return {k:wire(v)for k,v in x.items()}
 return x

def walk(x):
 if isinstance(x,dict):
  yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)

def load(stage):
 name,key=STAGES[stage];p=D/(P+name+'.json');raw=p.read_bytes();d=json.loads(raw)
 b=decode_bundle(raw)if d.get('schema')=='PLANNER-GENESIS-BUNDLE-1'else None
 s=b.current if b else c._unwire(d[key])if key else c.decode_snapshot(raw)
 return p,raw,d,b,s
STAGES={
 'EXTERNAL_WAIT':('E2_HUMAN_DECISION_ALLOW_POST_SNAPSHOT_1',None),
 'GOVERNED_UNKNOWN':('E2_P03_GATE_QUALIFIED_SNAPSHOT',None),
 'G04_GENESIS':('E2_GENESIS_PERSISTENCE_BUNDLE',None),
 'RECEIVED':('E2_P03_POST_RECEIPT_BUNDLE',None),
 'VALIDATED':('E2_P03_E04_LIFECYCLE_SNAPSHOTS','validated'),
 'PROVED':('E2_P03_E04_LIFECYCLE_SNAPSHOTS','proved'),
 'REENTRY_ELIGIBLE':('E2_P03_E04_LIFECYCLE_SNAPSHOTS','reentry_eligible'),
 'REENTER_COMPLETED':('E2_P03_E05_TARGET_SNAPSHOT',None),
 'SLOT_SATISFIED':('EVIDENCE_E06_SLOT_BOUNDARY_SNAPSHOT',None),
 'ROOT_SLOT_SATISFIED_FINISH_READY':('EVIDENCE_E06_P03_TARGET_SNAPSHOT',None)}

def inspect(stage):
 p,raw,d,b,s=load(stage);r=recompute(s);provs=sorted({json.dumps(x,sort_keys=True)for x in walk(c._wire(s))if x.get('$type')=='Provenance'})
 pins=[]
 for v in provs:
  x=json.loads(v);path=ROOT/x['path'];expected=x['identity']['sha256'];actual=hashlib.sha256(path.read_bytes()).hexdigest()if path.is_file()else None
  pins.append({'provenance':x,'physical_source_exists':path.is_file(),'raw_sha256':actual,'physical_pin_check':'PASS'if actual==expected else 'ABSENT'if actual is None else 'MISMATCH','excerpt_raw_sha256':hashlib.sha256(x['excerpt'].encode()).hexdigest()})
 return {'pid':os.getpid(),'file':str(p.relative_to(ROOT)),'file_sha256':hashlib.sha256(raw).hexdigest(),'snapshot_identity':c._wire(c.snapshot_id(s)),'bundle_identity':c._wire(bundle_identity(b))if b else None,'bundle_type':type(b).__name__ if b else None,'snapshot':c._wire(s),'computation':wire(r),'ledger':wire(b.ledger)if b else None,'bundle_canonical_sha256':hashlib.sha256(encode_bundle(b)).hexdigest()if b else None,'provenance':pins,'rule_known':[x.rule_known for x in s.evidence_requirements],'scope_lineage':wire(s.context),'policy_pin':d.get('policy'),'source_index':d.get('sources')}
if len(sys.argv)>1:
 print(json.dumps(inspect(sys.argv[1]),sort_keys=True));sys.exit()
BASE={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in (ROOT/'adapter/planner').glob('*.py')}
records={};comparisons={}
for stage in STAGES:
 expected=inspect(stage);runs=[]
 for seed in (0,1,7,101)if stage in ('EXTERNAL_WAIT','GOVERNED_UNKNOWN')else (0,):
  for repeat in range(3)if stage in ('EXTERNAL_WAIT','GOVERNED_UNKNOWN')else range(1):
   env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED=str(seed),PYTHONPATH=str(ROOT))
   proc=subprocess.run([sys.executable,__file__,stage],env=env,capture_output=True,text=True)
   assert proc.returncode==0,proc.stderr
   actual=json.loads(proc.stdout)
   domains={k:expected[k]==actual[k]for k in ['file_sha256','snapshot_identity','bundle_identity','snapshot','computation','ledger','bundle_canonical_sha256','provenance','scope_lineage','policy_pin','source_index']}
   assert all(domains.values())
   runs.append({'reader_pid':actual['pid'],'exit_status':proc.returncode,'seed':seed,'repeat':repeat,'domains':domains,'input_allowlist':[expected['file'],'native runtime modules','physical provenance paths enumerated in checkpoint'],'writer_pid':None,'writer_termination_qualified':False})
 records[stage]=expected;comparisons[stage]={'runs':runs,'available_state_comparison':'PASS','full_source_pinned_bundle_comparison':'UNQUALIFIED'if expected['bundle_identity']is None or expected['policy_pin']is None or expected['source_index']is None else 'PASS','byte_equality':'PASS_ORIGINAL_FILE_HASH_UNCHANGED','canonical_snapshot_identity':'PASS','canonical_bundle_identity':'PASS_GENESIS_DOMAIN_ONLY'if expected['bundle_identity']else 'NOT_APPLICABLE_NO_BUNDLE','semantic_state':'PASS_SNAPSHOT_AND_COMPLETE_COMPUTATION','event_ledger':'PASS_GENESIS_LEDGER_RESTORED'if expected['ledger']else 'ABSENT','source_pin':'PASS_SERIALIZED_PROVENANCE_ONLY_PHYSICAL_PINS_INCOMPLETE','provenance':'PASS_SERIALIZED_RECORDS','scope_lineage':'PASS','policy':'ABSENT_BUNDLE_PIN'}
# Historical E06 proof events only; retain its declared boundary.
j=json.loads((D/(P+'EVIDENCE_E06_EVENT_REPLAY.json')).read_text());state=c._unwire(j['initial']);parent=None
for w in j['events']:
 e=c._unwire(w);assert e.parent_snapshot==c.snapshot_id(state)and e.parent_event==parent
 assert e.identity==c._event_identity(e.sequence,e.parent_snapshot,parent,e.result,e.after_snapshot)
 state=apply_event(state,e.result).snapshot;assert c.snapshot_id(state)==e.after_snapshot;parent=e.identity
assert c.snapshot_id(state)==c._unwire(j['target'])
assert c.snapshot_bytes(state)==c.snapshot_bytes(load('ROOT_SLOT_SATISFIED_FINISH_READY')[-1])
# Post-receipt historical ledger event can replay from the existing G04 state.
pre=load('G04_GENESIS')[-1];post=load('RECEIVED')[3];event=post.ledger.events[-1]
try:
 replayed=apply_event(pre,event.result).snapshot
 receipt_replay={'result':'PASS'if c.snapshot_id(replayed)==c.snapshot_id(post.current)else 'MISMATCH','expected':c._wire(c.snapshot_id(post.current)),'actual':c._wire(c.snapshot_id(replayed))}
except Exception as ex:receipt_replay={'result':'UNQUALIFIED','error':str(ex),'reason':'Do not invent missing transaction inputs from result-only event.'}
# Compare binding-bearing records through later stages, separately from expected added support.
chain={};previous=None
for stage in ['RECEIVED','VALIDATED','PROVED','REENTRY_ELIGIBLE','REENTER_COMPLETED','SLOT_SATISFIED','ROOT_SLOT_SATISFIED_FINISH_READY']:
 s=load(stage)[-1]
 binding={'evidence_entities':[c._wire(x)for x in s.entities if x.kind is m.EntityKind.EVIDENCE],'receipt_admissions':[c._wire(x)for x in s.receipt_admissions],'requirements':[c._wire(x)for x in s.evidence_requirements],'attestor_authorities':[c._wire(x)for x in s.entities if x.id.value.startswith('E2-SYNTHETIC-ATTESTOR:')],'context':c._wire(s.context)}
 chain[stage]={'bindings':binding,'equality_to_previous':{k:binding[k]==previous[k]for k in binding}if previous else None};previous=binding
# Native invalidation controls, no persistence or canonical mutation.
g=load('GOVERNED_UNKNOWN')[-1];route=g.external_gates[0].resolution_contracts[0].provenance.identity
invalid=apply_event(g,m.SourceInvalidation((route,),c.snapshot_id(g))).snapshot
main=load('EXTERNAL_WAIT')[-1];grant=next(x for x in main.entities if x.id.value=='E2-GRANT')
withdrawn=apply_event(main,m.SourceInvalidation((grant.provenance.identity,),c.snapshot_id(main))).snapshot
invalidation={'A16':{'control':recompute(invalid).control.value,'snapshot':c._wire(c.snapshot_id(invalid))},'A15_grant':{'control':recompute(withdrawn).control.value,'snapshot':c._wire(c.snapshot_id(withdrawn)),'scope':'one existing authority dependency; complete disjoint-source coverage not established'}}
assert BASE=={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in (ROOT/'adapter/planner').glob('*.py')}
output={'runtime_hashes':BASE,'checkpoints':records,'cold_restore_comparisons':comparisons,'replay_comparisons':{'E06':{'result':'PASS_NATIVE_EVENT_BOUNDARY','history_boundary':j['history_boundary'],'target':c._wire(c.snapshot_id(state))},'T01_D':receipt_replay,'original_mainline':'UNQUALIFIED_NO_PERSISTENCE_BUNDLE','governed_unknown':'UNQUALIFIED_NO_PERSISTENCE_BUNDLE'},'source_chain':chain,'invalidation_controls':invalidation}
pathlib.Path('/tmp/p03_checkpoint_audit.json').write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
print(json.dumps({'checkpoints':len(records),'reader_processes':sum(len(x['runs'])for x in comparisons.values()),'receipt_replay':receipt_replay,'invalidation':invalidation}))
