"""Candidate-schema and fail-closed ownership guards; never select a policy."""
import json
from copy import deepcopy
from pathlib import Path
from adapter.planner import codec,selector,model
O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_bytes())
inventory=read(O/'candidate-inventory.json')['ROWS'];frame=read(O/'bounded-policy-decision-subject.json')
# One native binding is a structural reference control only, not selection.
row=inventory[0];base={'binding_candidates':[row],'generation':row['APPLICABLE_FRAME_GENERATION'],'scope':row['APPLICABLE_FRAME_SCOPE'],'lineage':row['APPLICABLE_FRAME_LINEAGE'],'selection_reason':'NO_SELECTION_PROPOSED_ONLY','currentness_claim':'EXACT_PIN_CONFIG','phase_is_version':False,'historical_applicability':True,'replay_policy':None,'hidden_selection':False}
def validate(v):
 assert len(v['binding_candidates'])==1 and v['binding_candidates'][0] in inventory
 r=v['binding_candidates'][0];selector.validate_policy(codec._unwire(r['SOURCE']),r['VERSION'])
 assert v['generation']==r['APPLICABLE_FRAME_GENERATION'] and v['scope']==r['APPLICABLE_FRAME_SCOPE'] and v['lineage']==r['APPLICABLE_FRAME_LINEAGE']
 assert v['selection_reason']=='NO_SELECTION_PROPOSED_ONLY' and v['currentness_claim']=='EXACT_PIN_CONFIG' and not v['phase_is_version'] and v['historical_applicability'] and v['replay_policy'] is None and not v['hidden_selection']
validate(base);rows=[]
def reject(name,fn):
 v=deepcopy(base);fn(v)
 try:validate(v)
 except (AssertionError,model.PlannerError):rows.append({'CASE':name,'STATUS':'REJECTED'})
 else:raise AssertionError(name)
reject('P05 selected because earlier',lambda v:v.update(selection_reason='EARLIER'))
reject('P06 selected because later',lambda v:v.update(selection_reason='LATER'))
reject('currentness inferred without rule',lambda v:v.update(currentness_claim='LATEST'))
reject('phase label treated as policy version',lambda v:v.update(phase_is_version=True))
reject('policy source substituted',lambda v:v['binding_candidates'][0]['SOURCE']['identity'].update(sha256='0'*64))
reject('wrong configuration generation',lambda v:v.update(generation='OTHER'))
reject('wrong scope',lambda v:v.update(scope='FULL_FROZEN_E1'))
reject('wrong lineage',lambda v:v.update(lineage='HISTORICAL_OTHER'))
reject('historical policy applied without applicability',lambda v:v.update(historical_applicability=False))
reject('replay sealed against different or unselected policy',lambda v:v.update(replay_policy='E1-SELECTION-1-P06'))
reject('both policies simultaneously bound',lambda v:v['binding_candidates'].append(inventory[1]))
reject('no policy in complete-binding candidate schema',lambda v:v.update(binding_candidates=[]))
reject('policy selection hidden as fixture construction',lambda v:v.update(hidden_selection=True))
reject('reviewed configuration digest changed',lambda v:v['binding_candidates'][0]['CONFIGURATION_IDENTITY'].update(SHA256='0'*64))
(O/'negative-suite.json').write_text(json.dumps({'STATUS':'PASS_STATIC_POLICY_OWNERSHIP_GUARDS','COUNT':len(rows),'ROWS':rows,'ACTUAL_POLICY_SELECTED':False,'LIMITATION':'One-binding schema control is hypothetical candidate validation only, not a selected native bundle or A14 execution'},sort_keys=True,indent=2)+'\n')
print(json.dumps({'NEGATIVES':'PASS_STATIC','COUNT':len(rows)}))
