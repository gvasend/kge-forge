"""Apply documentary operand overlays to draft records; no native object mutation."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;C3=R/'docs/plans/qualification/E2_P05_D01_OPERAND_CLOSURE_3'
def read(p):return json.loads(p.read_bytes())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def at(x,ptr):
 for k in ptr.split('/')[1:]:x=x[int(k)] if isinstance(x,list) else x[k]
 return x
old=read(C3/'invocation-records.partial.json');new=read(O/'new-source-bindings.json')['ROWS'];overrides=read(O/'a03-invocation-source-overrides.json');front=read(O/'remaining-frontier.json')['ROWS']
lookup={(r['OBLIGATION_ID'],r['STATE_VARIANT_ID'],r['STEP'],r['OPERAND_NAME']):r for r in new};ov={r['OBLIGATION_ID']:r for r in overrides}
for row in old['ROWS']:
 for v in row['VARIANTS']:
  v['MISSING_INITIAL_REFERENCE_OCCURRENCES']=sum(r['OBLIGATION_ID']==row['OBLIGATION_ID'] and r['STATE_VARIANT_ID']==v['STATE_VARIANT_ID'] for r in front)
  v['MISSING_REFERENCES']=v['MISSING_INITIAL_REFERENCE_OCCURRENCES'];v['COMPLETE']=False
  for step in v['INVOCATION_STEPS']:
   for operand in step['POSITIONAL_OPERANDS']:
    field=operand['BINDING'].get('fixture_field');key=(row['OBLIGATION_ID'],v['STATE_VARIANT_ID'],step['STEP'],field)
    if key in lookup:
     binding=lookup[key];operand.update(STATUS='RECONCILED_DOCUMENTARY_BINDING; complete operation preflight not run',IDENTITY=binding['SOURCE_IDENTITY'],NATIVE_TYPE=binding['NATIVE_TYPE'],SOURCE=binding['SOURCE_ARTIFACT'],DERIVATION_RULE=binding['DERIVATION_RULE'])
     if 'VALUE' in binding:operand['VALUE']=binding['VALUE']
     else:operand['VALUE_REFERENCE']=binding['VALUE_REFERENCE']
    if row['OBLIGATION_ID'] in ov and field in ov[row['OBLIGATION_ID']]['OPERAND_SOURCE_OVERRIDES']:
     source=ov[row['OBLIGATION_ID']]['OPERAND_SOURCE_OVERRIDES'][field];value=at(read(R/source['path']),source['pointer']);operand.pop('VALUE',None);operand.update(STATUS='EXPLICIT_A03_PRESTATE_SOURCE_OVERRIDE',VALUE_REFERENCE=source,SOURCE=source,IDENTITY='qualification-D01-reconciliation-v1:'+hashlib.sha256(canon(value)).hexdigest(),DERIVATION_RULE='Versioned source rebind: original A03 acquisition boundary; retained prefix after CHECK. Original capsule bytes unchanged.')
  if row['OBLIGATION_ID'] in ov:v['REQUIRES_SOURCE_OVERLAY']=ov[row['OBLIGATION_ID']]
old.update(ROW_COUNT=128,COMPLETE_ROWS=0,MISSING_INITIAL_REFERENCE_OCCURRENCES=59,NOTE='Documentary prospective draft only; capsule sources are not edited. A03 operand overlays must be honored by later materialization. 59 gaps remain. No runner invocation or oracle handoff is enabled.')
(O/'reconciled-invocation-drafts.json').write_bytes(canon(old)+b'\n');assert len(old['ROWS'])==128;print('RECONCILED_DRAFT_ROWS=128; COMPLETE=0; NO_OPERATION_EXECUTED')
