"""Documentary proposals only; no authority-store provisioning or adoption."""
import json,sys
from pathlib import Path
O=Path(__file__).resolve().parent;Q=O.parent/'runtime_r3_self_hosting_qualified_2026-09-19'
pin=json.loads((O/'AUTHORIZED_ENROLLMENT_SELECTION.json').read_bytes());q=json.loads((Q/'RUNTIME_QUALIFICATION_FINAL.json').read_bytes());row=json.loads((O/'ENROLLMENT_RESULT.json').read_bytes());d=json.loads((O/'PRODUCTION_DELEGATION.json').read_bytes());rec=json.loads((O/'INDEPENDENT_RECONSTRUCTION.json').read_bytes());assert rec['result']=='PASS'
sys.path.insert(0,pin['consumer_root'])
from adapter import runtime_adoption as r
from adapter.controller_authority_store import encoded,sha
# Required exact material integration decision payload, proposed only. No trusted
# integration-decision alias or authorizing source is supplied to production.
material_payload={'authority':'Architect','decision':'ADOPT_ORDINARY_ENROLLED_ADOPTION_CONSUMER','lineage':d['lineage'],'delegation':d['id'],'implementation_sha256':q['integration']['implementation_sha256'],'binding_kind':'PRODUCTION_ENROLLMENT'}
reserved={'authority_id':'sha256:'+sha(encoded(material_payload)),'sha256':sha(encoded(material_payload))}
integration=dict(q['integration']);integration.pop('id');integration.update(binding_kind='PRODUCTION_ENROLLMENT',delegation=d['id'],authority=reserved,journal='production:ordinary-runtime')
integration=r.seal('ORDINARY-ADOPTION-INTEGRATION',integration)
amendment=r.seal('PROPOSED-R3-PRODUCTION-INTEGRATION',{'schema':'PROPOSED-MATERIAL-RUNTIME-INTEGRATION-1','status':'PROPOSED_NOT_APPLIED','classification':'MATERIAL_RUNTIME_CONSUMPTION_INTEGRATION','candidate':pin['candidate'],'R1':pin['R1'],'R3':pin['runtime']['identity'],'current_context':d['context'],'runtime_head_authority':d['lineage'],'integration':integration,'required_decision_payload':material_payload,'architect_integration_authorization':None,'enrollment':row['id'],'qualification':pin['qualification'],'accepted_applicability_source':pin['intake']['source'],'no_bootstrap_change':True})
body={'schema':'ENROLLED-RUNTIME-ADOPTION-DECISION-1','authority':None,'decision':'ADOPT_EXACT_ENROLLED_CONTINUATION','binding_kind':'PRODUCTION_ENROLLMENT','lineage':d['lineage'],'delegation':d['id'],'candidate':pin['candidate'],'enrollment':row['id'],'qualification':pin['qualification'],'predecessor':pin['R1'],'successor':pin['runtime']['identity'],'head_event':pin['base_binding']['head_event']}
proposal=r.seal('PROPOSED-R3-ADOPTION',{'schema':'PROPOSED-EXACT-ENROLLED-RUNTIME-ADOPTION-1','status':'AWAITING_SEPARATE_ARCHITECT_ADOPTION','decision_fields':body,'architect_adoption_authority':None,'material_integration_proposal':amendment['id'],'release_context':d['context'],'qualification_closure':json.loads((Q/'QUALIFICATION_CLOSURE.json').read_bytes())['id'],'enrollment_file_sha256':sha(encoded(row)),'lineage':['R0 HISTORICAL','C1 ADOPTED',pin['R1'],q['continuation']['id'],pin['runtime']['identity']],'no_invocation_authority':True})
for name,value in [('PROPOSED_PRODUCTION_INTEGRATION.json',amendment),('PROPOSED_ADOPTION.json',proposal)]:
 with (O/name).open('xb') as f:f.write(encoded(value))
print(json.dumps({'adoption_proposal':proposal['id'],'adoption_file_sha256':sha(encoded(proposal)),'material_integration_proposal':amendment['id'],'integration_policy_proposed':integration['id'],'authorizing_sources':None,'production_mutation':False},indent=2))
