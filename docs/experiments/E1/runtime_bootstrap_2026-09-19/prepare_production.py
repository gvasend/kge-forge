"""Freeze proposed bodies only. No production authority store/journal is created."""
import sys,json
from pathlib import Path
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O/'candidate'))
from adapter import runtime_adoption as r
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha
q=json.loads((O/'ACTUAL_IDENTITY_QUALIFICATION.json').read_bytes());store=ControllerAuthorityStore(**q['store']);new={}
def add(v):
 data=encoded(v);h=sha(data);new['sha256:'+h]=v;return {'authority_id':'sha256:'+h,'sha256':h}
def proposed_grant(body):
 source=add(dict(body,channel='user'));return add(dict(body,authority_source=source))
with store.session():
 p=json.loads((O/'QUALIFIED_HEAD_POLICY.json').read_bytes());p.pop('id');p['binding_kind']='PRODUCTION_ADOPTION'
 record=json.loads((O/'QUALIFIED_BOOTSTRAP_RECORD.json').read_bytes());record.pop('id')
 lineage=r.identity('RUNTIME-AUTHORITY-LINEAGE',{'legacy_runtime':record['legacy_runtime'],'legacy_publication':r.read(store,record['legacy_verifier']['input'])['publication'],'release_context':record['release_context']})
 p.update(bootstrap_lineage=lineage,bootstrap_journal='controller:runtime-bootstrap-journal',journal='controller:runtime-head-journal')
 amendment=r.read(store,p['material_amendment']);amendment.pop('id');amendment['candidate_predecessor']=record['candidate_material_amendment'];amendment['bounded_bootstrap_schema']='RUNTIME-AUTHORITY-BOOTSTRAP-1';amendment['bootstrap_consumer_files']=record['consumer_files']
 amendment=r.seal('RUNTIME-CONSUMPTION-AMENDMENT',amendment);ar=add(amendment);p['material_amendment']=ar
 p['material_decision']=proposed_grant({'authority':'Architect','decision':'ADOPT_RUNTIME_CONSUMPTION_AMENDMENT','amendment':ar,'binding_kind':'PRODUCTION_ADOPTION'})
 cref=record['first_continuation'];c=r.read(store,cref);before=r.descriptor(store,c['predecessor']);after=r.descriptor(store,c['successor'])
 grant=proposed_grant({'authority':'Architect','decision':'ADOPT_EXACT_RUNTIME_CONTINUATION','continuation':cref,'predecessor':before['identity'],'successor':after['identity'],'release_context':p['release_context'],'binding_kind':'PRODUCTION_ADOPTION','material_amendment':ar})
 p['adoptions']=[{'continuation':cref,'grant':grant}];p=r.seal('RUNTIME-HEAD-AUTHORITY',p);pr=add(p)
 record.update(lineage=lineage,binding_kind='PRODUCTION_ADOPTION',runtime_head_authority=p['id'],material_amendment=ar,first_adoption_authority=grant)
 record=r.seal('RUNTIME-AUTHORITY-BOOTSTRAP',record);br=add(record)
 ba=proposed_grant({'authority':'Architect','decision':'AUTHORIZE_ONE_TIME_RUNTIME_AUTHORITY_BOOTSTRAP','record':br,'lineage':lineage,'binding_kind':'PRODUCTION_ADOPTION'})
 selector={'record':br,'Architect_authorization':ba}
store.close()
package={'status':'PROPOSED_NOT_AUTHORIZED_NOT_MATERIALIZED','objects':new,'proposed_selector':selector,'head_policy':pr,'base_objects':q['store'],
 'intended_private_lineage_directory':'/tmp/kge-forge-runtime-authority/'+lineage.split(':')[-1],
 'production_authority_established':False,'requires':'Explicit Architect adoption of these exact bootstrap/material/head-policy bodies; no decision is inferred from qualification'}
for name,value in [('PROPOSED_MATERIAL_AMENDMENT.json',amendment),('PROPOSED_RUNTIME_HEAD_AUTHORITY.json',p),('PROPOSED_BOOTSTRAP_RECORD.json',record),('PROPOSED_AUTHORIZATION_PACKAGE.json',package)]:
 (O/name).write_bytes(encoded(value))
publication={'verdict':'BLOCKED_AWAITING_ARCHITECT_BOOTSTRAP_ADOPTION','legacy_runtime':before['identity'],'proposed_bootstrap':record['id'],'bootstrap_file_sha256':br['sha256'],'proposed_material_amendment':amendment['id'],'material_amendment_file_sha256':ar['sha256'],'proposed_runtime_head_authority':p['id'],'head_authority_file_sha256':pr['sha256'],'candidate_R1':after['identity'],'original_continuation':q['original_continuation'],'applied_bootstrap':None,'applied_material_amendment':None,'production_current_runtime':before['identity'],'current_release_context':p['release_context'],'qualification':q,'production_premodel_timing':None,'r13_created':False,'real_model_requests':0,'E1_effects':0}
(O/'PUBLICATION.json').write_bytes(encoded(publication));print(json.dumps({k:v for k,v in publication.items() if k!='qualification'}))
