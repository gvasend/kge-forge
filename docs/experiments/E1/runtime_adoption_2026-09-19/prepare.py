"""Prepare reviewable MATERIAL records. No production selection/adoption/issuance."""
import json,sys,tempfile,shutil
from pathlib import Path
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O/'candidate'))
from adapter.runtime_adoption import seal,RULES
from adapter.controller_authority_store import encoded,sha
Q=O.parent/'run2_control_plane_binding_2026-09-18';oldpub=json.loads((Q/'QUALIFIED_PUBLICATION.json').read_bytes());exact=json.loads((O/'EXACT_C1_QUALIFICATION.json').read_bytes())
root=Path(tempfile.mkdtemp(prefix='forge-runtime-consumer-candidate-'));root.chmod(0o700);shutil.copytree(O/'candidate/adapter',root/'adapter',ignore=shutil.ignore_patterns('__pycache__'))
files={p.name:sha(p.read_bytes()) for p in (root/'adapter').glob('*.py')};rid='sha256:'+sha(encoded(files))
mechanism={'authority_id':'sha256:'+files['runtime_adoption.py'],'sha256':files['runtime_adoption.py']}
ancestry=dict(oldpub['real_historical_context'],release_authority=oldpub['real_release_authority'])
body={'schema':'RUNTIME-CONSUMPTION-AMENDMENT-1','classification':'MATERIAL','release_context':ancestry,'mechanism':mechanism,'rules':RULES,
 'candidate_consumer_runtime':{'identity':rid,'root':str(root),'files':files},
 'original_implementation_continuation':oldpub['proposed_continuation_ref'],
 'original_implementation_continuation_id':oldpub['proposed_production_continuation'],
 'qualified_control_plane_runtime':oldpub['implementation'],
 'qualification':{'journal_and_exact_C1':'PASS','ordinary_production_context_and_premodel':'NOT_ESTABLISHED'},
 'preserved':{'ModelPayloadDigest':'d675d581c80f43e691a31da73ccf17fd4bcc6b00d3a5331f26b9294e294e1538','historical_attempts':'IMMUTABLE','budget_and_progress_semantics':'UNCHANGED','supervisor_authority':'UNCHANGED'},
 'Architect_material_decision':None,'status':'PROPOSED_NOT_RELEASED'}
a=seal('RUNTIME-CONSUMPTION-AMENDMENT',body);(O/'PROPOSED_MATERIAL_AMENDMENT.json').write_bytes(encoded(a));ar={'authority_id':'sha256:'+sha(encoded(a)),'sha256':sha(encoded(a))}
p=seal('RUNTIME-HEAD-AUTHORITY',{'schema':'RUNTIME-HEAD-AUTHORITY-1','binding_kind':'PRODUCTION_ADOPTION','material_amendment':ar,'material_decision':None,'release_context':ancestry,'mechanism':mechanism,
 'genesis_runtime':exact['runtime_before'],'candidate_successor_runtime':exact['runtime_after'],'candidate_continuation':oldpub['proposed_continuation_ref'],'Architect_adoption_decision':None,'state':'PROPOSED_NOT_SELECTED'})
(O/'PROPOSED_RUNTIME_HEAD_AUTHORITY.json').write_bytes(encoded(p))
publication={'verdict':'BLOCKED_NOT_PRODUCTION_ADOPTED','mechanism_classification':'MATERIAL','control_plane_delta_classification':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION','proposed_amendment':a['id'],'amendment_file_sha256':ar['sha256'],'proposed_runtime_head_authority':p['id'],'runtime_head_authority_file_sha256':sha(encoded(p)),'consumer_candidate_runtime':rid,'consumer_runtime_root':str(root),'existing_control_plane_continuation':oldpub['proposed_production_continuation'],'existing_control_plane_continuation_file_sha256':oldpub['proposed_production_continuation_file_sha256'],'intended_successor_runtime':oldpub['implementation'],'adopted_continuation':None,'current_real_runtime':exact['runtime_before'],'current_release':oldpub['real_release_authority'],'current_context':oldpub['real_historical_context'],'ordinary_production_premodel_timing':None,'production_adoption':False,'r13_created':False,'real_model_requests':0,'real_effects':0}
(O/'PUBLICATION.json').write_bytes(encoded(publication));print(json.dumps(publication))
