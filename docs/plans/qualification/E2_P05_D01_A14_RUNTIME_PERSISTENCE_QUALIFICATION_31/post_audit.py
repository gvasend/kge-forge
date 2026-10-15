"""Read-only post-audit; never launches a writer/reader or applies events."""
import json,hashlib,sys
from pathlib import Path
R=Path('/home/gvasend/app/kge-forge');E=Path(__file__).resolve().parent
sys.path.insert(0,str(R))
from adapter.planner import codec
C=R/'docs/plans/qualification/E2_P05_D01_A14_RUNTIME_PERSISTENCE_CONTRACT_30'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def emit(n,v):(E/n).write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
before=load(E/'preservation-before.json')
changed=[p for p,h in before.items() if not (R/p).is_file() or sha((R/p).read_bytes())!=h]
assert not changed,changed
# Baseline inclusion of execute.py was harmless; compare original paths directly.
emit('preservation-after.json',{'PASS':True,'FILES_CHECKED':len(before),'CHANGED':changed,'METHOD':'Direct raw-hash comparison of every pre-runtime path, including original supervisor source; new bounded evidence excluded','E1_ARTIFACTS_MODIFIED':0,'RUNTIME_IMPLEMENTATION_MODIFIED':False,'SOURCE_FIXTURE_MODIFIED':False,'BOOKKEEPING_EXCEPTION':'Initial relative-path evidence exclusion included execute.py; set equality therefore included newly produced evidence. Direct checks show zero preexisting content changes.'})
runtime=load(E/'runtime-results.json');assert len(runtime['ROWS'])==2
for row in runtime['ROWS']:
 assert row['result']=='PASS' and len(row['readers'])==12
 for reader in row['readers']:assert reader['complete_comparison']=='PASS'
front=load(R/'docs/plans/qualification/E2_P05_D01_A14_COLD_READER_BINDING_CLOSURE_29/operand-frontier.json')
resolved=front['PREVIOUS_BINDINGS']['FROZEN_52']+front['PREVIOUS_BINDINGS']['PREVIOUS_BUNDLE_RESOLUTIONS']+front['PREVIOUS_BINDINGS']['RESOLVED_BY_SAVE_CONTRACT_ROWS'];assert len(resolved)==58
unresolved=front['UNRESOLVED'];assert len(unresolved)==53
pins=[]
def validate_pins(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and x.get('raw_sha256'):
   p=Path(x['path']);p=p if p.is_absolute() else R/p;assert p.is_file() and sha(p.read_bytes())==x['raw_sha256'],str(p);pins.append({'path':str(p),'sha256':x['raw_sha256'],'PASS':True})
  for z in x.values():validate_pins(z)
 elif isinstance(x,list):
  for z in x:validate_pins(z)
validate_pins(front)
audit=[]
for status,records in [('RESOLVED',resolved),('UNRESOLVED',unresolved)]:
 for ref in records:
  audit.append({'REFERENCE':ref,'PREVIOUS_STATUS':status,'POST_RUNTIME_STATUS':status,'RUNTIME_EVIDENCE_IF_CHANGED':None,'PIN_REVALIDATION':'PASS','REMAINING_BLOCKER':ref.get('CURRENT_GAP') if status=='UNRESOLVED' else None})
assert len(audit)==111
keys=[(x['REFERENCE']['OBLIGATION_ID'],x['REFERENCE']['CAPSULE_ID'],x['REFERENCE']['OPERAND_NAME'],x['REFERENCE'].get('STEP')) for x in audit];assert len(set(keys))==111
capsule=load(R/'docs/plans/qualification/E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2/fixtures/D01-VARIANT__E2-A16__CANONICAL_REQUIRED_BEHAVIOR.json')
cs=codec._unwire(capsule['canonical_content']['arguments']['snapshot']);capsule_id=codec._wire(codec.snapshot_id(cs))
restored_id=runtime['ROWS'][0]['readers'][0]['process']['value']['result']['snapshot_identity']
assert capsule_id!=restored_id
conditionals=[x for x in audit if x['REFERENCE']['CASE_ID']=='E2-A16'];assert len(conditionals)==2
emit('a16-conditional-audit.json',{'CONDITIONAL_REFERENCES':conditionals,'OBSERVED_COLD_RESTORE':'PASS_24_OF_24','RESTORED_SNAPSHOT':restored_id,'EXISTING_A16_CAPSULE_SNAPSHOT':capsule_id,'COMPLETE_ACCEPTANCE_CONDITION':'Exact post-restore pre-state association and native SourceInvalidation changed-source/expected_snapshot binding must independently be sealed; persistence success is not that binding','A16_REFERENCES_RESOLVED':0,'REASON':'Actual corrected cold-restored baseline now exists, but the sealed A16 capsule uses a different Snapshot identity and its event operand is still absent. Contract30 does not authorize rewriting/rebinding that capsule or constructing a new invalidation event. No baseline-only promotion.','SOURCE_ROLE_CANDIDATES':{'gate_source':'source.json','resolution_contract_provenance':'resolution.json'},'EVENT_CONSTRUCTED':False,'INVALIDATION_APPLIED':False})
emit('operand-post-audit.json',{'ROWS':audit,'TOTAL_REFERENCES':111,'PREVIOUSLY_RESOLVED':58,'RESOLVED_BY_RUNTIME_SEQUENCE':0,'TOTAL_RESOLVED':58,'TOTAL_UNRESOLVED':53,'PIN_OCCURRENCES_REVALIDATED':len(pins),'FROZEN_58_UNCHANGED':True,'FIRST_REMAINING_BLOCKER':{'CLASS':'OTHER_OPERAND_BINDING','OBLIGATION_ID':unresolved[0]['OBLIGATION_ID'],'OPERAND_NAME':unresolved[0]['OPERAND_NAME'],'EXACT_ROOT_CAUSE':unresolved[0]['EXACT_ROOT_CAUSE']},'INVOCATION_STATIC_PREFLIGHT':'NOT_RUN','FULL_OUTPUT_ORACLES':'0/128'})
emit('operand-source-pin-checks.json',pins)
print('POST_AUDIT PASS 111 references; 58 resolved / 53 unresolved; A16 0 promoted; preservation PASS')
