"""Verify sealed reconciliation metadata without invoking qualification operations."""
import json,hashlib
from pathlib import Path
R=Path('/home/gvasend/app/kge-forge');E=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification'
def load(p):return json.loads(Path(p).read_bytes())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
c=load(E/'source-collection.json');m=c['MEMBERS'];assert len(m)==c['COUNT']==51
assert len({canon(x['PIN']) for x in m})==51 and all(x['ELIGIBILITY']=='ELIGIBLE' and not x['ELIGIBLE_AS_SOLE_COLLECTION_REPRESENTATIVE'] for x in m)
for x in m:assert sha((R/x['PATH']).read_bytes())==x['RAW_HASH']==x['CONTENT_IDENTITY']['sha256']
assert len(c['BROADER_CANDIDATE_CONTEXTS'])==16 and all(not x['SELECTED'] for x in c['BROADER_CANDIDATE_CONTEXTS'])
assert [x['AVAILABLE_COUNT'] for x in c['PREFIXES']]==[16,16,16,18,25,27,35,37,49,51]
assert len(load(E/'runner-candidate-inspection.json'))==11
proposal=load(E/'dispatch-correction-proposal.json');identity=proposal.pop('PROPOSAL_IDENTITY');assert identity=='qualification-source-bytes-dispatch-correction-v1:'+sha(canon(proposal));assert proposal['STATUS']=='SEALED_PROPOSAL_ONLY_NOT_APPLIED'
for key in ['CURRENT_DISPATCH','CURRENT_CAPSULE','FROZEN_OBLIGATIONS']:
 p=proposal[key];assert sha((R/p['path']).read_bytes())==p['raw_sha256']
dispatch=load(R/proposal['CURRENT_DISPATCH']['path'])['D01-DISPATCH:SOURCE_BYTES'];assert dispatch['steps'][0]['args'][1]=={'fixture_field':'pin'} and len(dispatch['steps'])==1
front=load(E/'operand-frontier.json');previous=load(R/front['PRIOR_AUDIT']['path']);assert len(front['REFERENCES'])==111 and front['TOTAL_RESOLVED']==58 and front['TOTAL_UNRESOLVED']==53
for current,old in zip(front['REFERENCES'],previous['ROWS']):assert current['REFERENCE']==old['REFERENCE'] and current['POST_RECONCILIATION_STATUS']==old['POST_RUNTIME_STATUS'] and not current['PROMOTED']
assert front['NEXT_UNRESOLVED_AFTER_SOURCE_BYTES']['OBLIGATION_ID']=='D01-OBL:E2-A15_OPERANDS'
assert load(E/'negative-suite.json')['RESULT']=='PASS' and load(E/'negative-suite.json')['PASS']==21
assert len({x['SEMANTIC_SHA256'] for x in load(E/'determinism.json')['FRESH_PROCESSES']})==1
assert len({x['HYPOTHETICAL_SINGLE_MEMBER_INVOCATION_IDENTITY'] for x in load(E/'selection-identity-impact.json')})==51
oldindex=load(Q/'E2_P05_D01_A14_RUNTIME_PERSISTENCE_QUALIFICATION_31/evidence-index.json')
for p,h in oldindex['FILES'].items():assert sha((R/p).read_bytes())==h,p
for p in load(E/'preservation.json')['QUALIFIED_RUNTIME_OUTPUTS']:assert sha(Path(p['path']).read_bytes())==p['sha256']
assert load(E/'authority-analysis.json')['DECISION_REQUIRED'] is False
print('PASS: 51 sources; 11 runner candidates; 21 negatives; four-seed identity; unchanged V2/A14/A16; 111 audit references retained')
