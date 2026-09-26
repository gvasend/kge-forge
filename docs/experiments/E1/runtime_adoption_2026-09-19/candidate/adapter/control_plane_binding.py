"""Exact controller implementation continuation and isolated qualification binding.

This schema authorizes no real attempt or effect. It composes the released
production predicates with explicitly isolated qualification lifecycle identities.
Neither the source record nor a successful qualification grants a model request.
"""
import json, os
from pathlib import Path
from .context_projection import canonical,digest,sha,read_exact
from .controller_authority_store import current,outside
from .attempt_context import require,read,ident,peer
from .attempt_chain import historical_capture,predecessor_nodes,classify_terminal,state_of
from .attempt_ownership import observe,attribute
from .run_control import events
from .continuation_envelope import BODY_KEYS,seal

SCHEMA=8
SOURCE_DECISION='BIND_EXACT_CONTROL_PLANE_AND_QUALIFY_SYNTHETIC_PREMODEL_ONLY'

def selected():
 s=current();require(s is not None,'private qualification store required')
 v=json.loads(s.resolve(s.applicability['authorization_id']+':control-plane'))
 require(v['mode']=='QUALIFICATION_ONLY','not a real invocation authority')
 return v

def verify(owner):
 s=current();spec=owner.spec
 require(spec['schema']==SCHEMA and digest(spec)==owner._issued_digest,'control-plane context changed')
 selection=selected();require(selection['binding']==spec['binding'],'unselected qualification binding')
 b=read(spec['binding']);source=read(b['authority_source'])
 require(source['decision']==SOURCE_DECISION and source['authority']=='Architect' and source['channel']=='user','qualification source absent')
 require(source['real_invocation_authorized'] is False and source['model_requests_authorized'] is False and source['effects_authorized'] is False,'qualification scope broadened')
 require(b['schema']=='CONTROL-PLANE-QUALIFICATION-BINDING-1' and b['mode']=='QUALIFICATION_ONLY','unknown binding')
 require({'invocation_identity':b['invocation_identity'],'qualification_root':b['qualification_root']} in source['qualification_slots'] and b['invocation_identity']['authorization_id']==s.applicability['authorization_id'],'wrong qualification identity')
 require(b['invocation_identity']['authorization_id'].startswith('qualification-control-plane-'),'real attempt cannot use qualification binding')
 c=read(b['continuation']);require(c==seal({k:c[k] for k in BODY_KEYS},c['approval']) and c['approval']==b['authority_source'],'continuation substitution')
 require(c['classification']=='NON_MATERIAL_IMPLEMENTATION_CONTINUATION','unclassified implementation')
 runtime=read(b['runtime']);require(runtime['identity']=='sha256:'+digest(runtime['files']),'runtime fingerprint')
 root=Path(runtime['root']);outside(root,s.catalog['programmer_roots'])
 require(Path(__file__).resolve().parent==root/'adapter' and {p.name:sha(p.read_bytes()) for p in (root/'adapter').glob('*.py')}==runtime['files'],'unaccounted bound runtime')
 require(c['authority_invariants']==b['preserved_bindings'] and source['runtime_identity']==runtime['identity'],'unbound implementation/authority invariants')
 proof=historical_capture({'predecessor_capture':b['parent_capture'],'predecessor_publication':b['parent_publication']})
 old=proof['governance'];oldop=json.loads(proof['authorization']['operational_binding'])
 require(b['release_authority']==old['run7']['release_authority'],'release authority changed')
 require(c['predecessor_OperationalContextId']==old['identities']['OperationalContextId'] and c['predecessor_chain_digest']==old['identities']['continuation_chain_digest'],'continuation ancestry mismatch')
 parent_pub=json.loads(read_exact(b['parent_publication']['path'],b['parent_publication']['sha256']))
 require(source['parent_publication']==b['parent_publication'],'unbound parent authority')
 from .history_catalogs import historical_store
 with historical_store(parent_pub['selected_store']) as parent_store:
  previous_runtime=json.loads(parent_store.resolve(parent_pub['controller_runtime']['authority_id']))
 artifacts=c['artifacts'];changed={n for n in set(previous_runtime['files'])|set(runtime['files']) if previous_runtime['files'].get(n)!=runtime['files'].get(n)}
 require({Path(r['path']).name for r in artifacts}==changed,'incomplete continuation delta')
 for row in artifacts:
  n=Path(row['path']).name
  require(row['old_sha256']==previous_runtime['files'].get(n) and row['new_sha256']==runtime['files'][n],'implementation delta substitution')
 require(read(c['evidence'])['candidate_files']==runtime['files'],'implementation evidence changed')
 for key in ('release_basis','release_decision','released_profile','clearance'):
  require(spec[key]==oldop['governance'][key],'release authority selection changed')
 expected=dict(old['run7']['proposal']['bindings']);expected.update(old['identities']);expected.update({k:proof['context'][k] for k in ('FullContextDigest','ModelPayloadDigest','ModelProjectionBindingDigest')})
 expected.update(release_authority=b['release_authority'],controller_runtime_identity=previous_runtime['identity'])
 require(expected==b['preserved_bindings'],'authority or model payload changed')
 # Every historical audit is re-read and checked; qualification never rewrites
 # attempts or inherits their state. Current shared ownership is checked freshly.
 nodes,failed=predecessor_nodes(proof);ancestors=[{k:failed[k] for k in ('authorization_id','audit','audit_sha256')}]
 for node in nodes:
  term=node['terminal'];aid=node['authorization']['authorization_id']
  read_exact(term['audit'],term['audit_sha256'])
  semantic=aid==proof['authorization']['authorization_id'] or node['governance'].get('run7',{}).get('amendment',{}).get('schema')=='E1-RUN2-ATTEMPT-CHAIN-2'
  # Earlier nodes keep the eligibility semantics of their authenticated successor.
  # r11 was accepted by r12's semantic amendment, whereas r9's old suffix remains legacy.
  if aid==old['run7']['predecessor']['authorization']['authorization_id']:semantic=True
  require(classify_terminal(events(term['audit']),term,aid,semantic)=='ACTIVE_CANCELLED_PRE_MODEL_NO_EFFECTS','unsafe predecessor')
  ancestors.append({'authorization_id':aid,'audit':term['audit'],'audit_sha256':term['audit_sha256']})
 require(ancestors==b['predecessors'],'attempt ancestry changed')
 owner_now,scope,_=observe(proof['authorization']['ownership_ledger']);require(owner_now is None and scope is None,'real ownership or scope active')
 qroot=Path(b['qualification_root']);outside(qroot,s.catalog['programmer_roots'])
 require(qroot.is_dir() and qroot.stat().st_uid==os.getuid() and qroot.stat().st_mode&0o077==0,'qualification boundary invalid')
 require(b['audit']==str(qroot/'controller.jsonl') and b['ownership_ledger']==str(qroot/'ownership.jsonl'),'qualification state location substitution')
 require(s.catalog['private_state'][s.applicability['authorization_id']+':audit']['path']==b['audit'] and s.catalog['private_state'][s.applicability['authorization_id']+':ownership']['path']==b['ownership_ledger'],'state selection changed')
 qowner,qscope,_=observe(b['ownership_ledger']);attribute(qowner,qscope,[x['authorization_id'] for x in ancestors],b['invocation_identity'],b['audit'])
 ids={k:old['identities'][k] for k in ('ReleaseBasisId','ReleaseDecisionId')}
 ids.update(OperationalContextId=ident('E1-OPERATIONAL-CONTEXT',{'continuation':c['continuation_id'],'qualification_binding':spec['binding']}),continuation_chain_digest=digest({'predecessor':old['identities']['continuation_chain_digest'],'continuation':c['continuation_id'],'qualification_binding':spec['binding']}))
 require(ids==spec['identities'] and s.applicability==dict(ids,authorization_id=b['invocation_identity']['authorization_id']),'context head substitution')
 for k in ('changes','authority_invariants','anchor_projection','anchor_op','ancestor_ops'):setattr(owner,k,old[k])
 owner.identities=ids;owner.supplement=json.loads(canonical(old['supplement']));owner.supplement['controller_runtime']={'identity':runtime['identity'],'authority':spec['binding'],'corrections':b['continuation']}
 owner.ancestry=old['ancestry']+[{'control_plane_continuation':c['continuation_id'],'qualification_binding':spec['binding'],**ids}]
 owner.run8={'binding':b,'predecessor':proof,'continuation':c,'release_authority':b['release_authority']}
 return ids

def verify_authorization(auth):
 g=auth.context_binding.governance;g.verify();b=g.run8['binding'];op=json.loads(auth.operational_binding)
 expected=json.loads(canonical(g.run8['predecessor']['authorization']));expected.update(b['invocation_identity']);expected['ownership_ledger']=b['ownership_ledger'];expected.pop('operational_binding')
 actual=dict(auth.__dict__);actual.pop('operational_binding');actual['context_binding']={'path':str(auth.context_binding.path),'capture_commit':auth.context_binding.capture_commit}
 require(auth.state in ('INACTIVE','ACTIVE'),'unexpected effective template state');expected['state']=auth.state
 require(json.loads(canonical(actual))==expected,'qualification changes task/grants/profile/payload')
 oldop=json.loads(g.run8['predecessor']['authorization']['operational_binding'])
 require(op['governance']==g.spec and op['released_launch']==oldop['released_launch'] and op['invocation_identity']==b['invocation_identity'],'qualification operation mismatch')
 return op

def derive_dispatch(auth):
 g=auth.context_binding.governance;b=g.run8['binding'];op=json.loads(auth.operational_binding)
 d=dict(g.run8['predecessor']['dispatch']);d.update(g.identities);d.update(op['context_identities'])
 d.update(invocation_identity=b['invocation_identity'],decision='QUALIFICATION_PATH_AUTHORIZED',authority_source=b['authority_source'],qualification_binding=g.spec['binding'],release_authority=b['release_authority'])
 original=dict(op);original.pop('dispatch_authorization',None)
 d['all_authorized_bindings']=dict(d['all_authorized_bindings'],audit=b['audit'],ownership_ledger=b['ownership_ledger'],operational_binding_sha256=digest(original))
 return d

def verify_dispatch(auth,decision):
 verify_authorization(auth);require(decision==derive_dispatch(auth),'qualification dispatch changed');return 'QUALIFICATION_ONLY'

def ledger_for(auth,profile):
 verify_authorization(auth);b=auth.context_binding.governance.run8['binding']
 require(profile['ownership']['ledger']==auth.context_binding.governance.run8['predecessor']['authorization']['ownership_ledger'],'released ledger changed')
 return b['ownership_ledger']

def readiness(auth,store,historical,check_scopes,legacy):
 g=auth.context_binding.governance;g.verify();binding=g.run8['binding']
 from .supervisor_verification import verified_readiness
 evidence=read(g.run8['continuation']['evidence'])
 require(evidence['supervisor_verification']==binding['supervisor_verification'],'unbound supervisor verification evidence')
 node=g.run8['predecessor']
 while 'run7' in node['governance'] or 'run6' in node['governance']:node=state_of(node['governance'])['predecessor']
 return verified_readiness(evidence['supervisor_verification'],node['governance']['run5']['amendment']['predecessor_publication'],binding['preserved_bindings'],check_scopes,legacy)

def forbid_effect(auth):
 if auth.operational_binding and json.loads(auth.operational_binding)['governance'].get('schema')==SCHEMA:
  raise ValueError('qualification-only context cannot transmit a model request or execute governed effects')
