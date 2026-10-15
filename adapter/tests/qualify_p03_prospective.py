"""Authorized prospective P03 qualification. Never executes FINISH or edits E1.

Seal phase authors fixtures/oracles only. Writer/reader are distinct subprocesses.
Native runtime remains unchanged; historical records are comparison references.
"""
from dataclasses import replace,fields,is_dataclass
from enum import Enum
from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile
from adapter.planner import codec as c, model as m, core, typed_proofs as t
from adapter.planner.selector import POLICY_PIN
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'docs/plans';P='DETERMINISTIC_PLANNER_V0_1_';PREFIX=P+'P03_PROSPECTIVE_CHECKPOINT'
A=D/'qualification/P03_PROSPECTIVE_CHECKPOINT_1';SCOPE='E2-QUALIFICATION-ONLY';LINEAGE='E2-P03-PROSPECTIVE-QUALIFICATION-1';GEN='E2-P03-PROSPECTIVE-GENERATION-1'
ZERO=m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'placeholder','0'*64)

def identity(raw,ns='raw-file-sha256'):return c._identity(raw,ns)
def jbytes(x):return c.canonical_bytes(x)
def write(p,raw):
 p.parent.mkdir(parents=True,exist_ok=True);return c._write_immutable(p.parent,p.name,raw)
def source(name,body):
 raw=jbytes(body);p=A/'sources'/name;write(p,raw);pin=m.ArtifactPin(str(p.relative_to(ROOT)),identity(raw));return m.Provenance(pin.path,pin.identity,'/',raw.decode(),'PROSPECTIVE_AUTHORED_INPUT',SCOPE),pin

def serialize(x):
 if isinstance(x,Enum):return {'type':type(x).__name__,'value':x.value}
 if is_dataclass(x):return {'type':type(x).__name__,**{f.name:serialize(getattr(x,f.name))for f in fields(x)}}
 if isinstance(x,(tuple,list)):return [serialize(y)for y in x]
 if isinstance(x,dict):return {k:serialize(v)for k,v in x.items()}
 return x

def descendants(x):
 if isinstance(x,dict):
  yield x
  for v in x.values():yield from descendants(v)
 elif isinstance(x,list):
  for v in x:yield from descendants(v)

def author_template(filename,label):
 old=c.decode_snapshot((D/(P+filename)).read_bytes());w=c._wire(old)
 originals={jbytes(x) for x in descendants(w)if x.get('$type')=='Provenance'};provmap={};idmap={};pins=[]
 for i,b in enumerate(sorted(originals)):
  x=json.loads(b);pv,pin=source(label+'-source-%02d.json'%i,{'qualification_type':'PROSPECTIVE_REPLACEMENT','authored_initial_premise':True,'scope':SCOPE,'lineage':LINEAGE,'generation':GEN,'template_provenance':x,'scope_decision':'AUTHORIZE_PROSPECTIVE_P03_CHECKPOINT_QUALIFICATION','historical_reconstruction':False})
  provmap[b]=c._wire(pv);idmap[jbytes(x['identity'])]=c._wire(pin.identity);pins.append(pin)
 def rewrite(x):
  if isinstance(x,list):return [rewrite(v)for v in x]
  if isinstance(x,dict):
   if x.get('$type')=='Provenance':return provmap[jbytes(x)]
   if x.get('$type')=='ArtifactIdentity'and jbytes(x)in idmap:return idmap[jbytes(x)]
   return {k:(LINEAGE if k=='lineage' else GEN if k=='generation'else rewrite(v))for k,v in x.items()}
  return x
 return c._unwire(rewrite(w)),pins

def bundle(s,pins):return m.PersistenceBundle(s,(),s,tuple(pins),POLICY_PIN,'E1-SELECTION-1-P06','PARTIAL_HISTORICAL_REPLAY')
def load_bundle(path):return c._unwire(json.loads(Path(path).read_text())['bundle'])
def view(b):
 return {'state':c._wire(b.current),'state_id':c._wire(c.snapshot_id(b.current)),'bundle_id':c._wire(c.bundle_id(b)),'sources':c._wire(b.sources),'policy':c._wire(b.policy),'policy_version':b.policy_version,'context':c._wire(b.current.context),'authority':c._wire(b.current.entities),'ledger':c._wire(b.events),'computation':serialize(core.recompute(b.current))}

def seal():
 dossier=D/(P+'P03_CHECKPOINT_SCOPE_DECISION_DOSSIER_1.json');authority={'schema':'P03-QUALIFICATION-SCOPE-DECISION-1','subject':'P03 irreproducible historical checkpoint qualification','selected_option':'AUTHORIZE_PROSPECTIVE_P03_CHECKPOINT_QUALIFICATION','dossier':str(dossier.relative_to(ROOT)),'dossier_raw_sha256':hashlib.sha256(dossier.read_bytes()).hexdigest(),'dossier_md_raw_sha256':hashlib.sha256((D/(P+'P03_CHECKPOINT_SCOPE_DECISION_DOSSIER_1.md')).read_bytes()).hexdigest(),'issuer':'authenticated human user of this session','authentication':'Explicit user-role decision supplied through trusted conversation transport; no signature or external issuer fabricated','scope':SCOPE,'lineage':LINEAGE,'sequence':1,'issuance_time':'2026-10-03','provenance':'User instruction P03 AUTHORIZED PROSPECTIVE CHECKPOINT QUALIFICATION 1, AUTHORITATIVE HUMAN DECISION','permissions':['Prospective contract adopted from selected Option B','New physical source/policy fixture inputs and authored HUMAN_HANDOFF initial premises','Bounded synthetic ALLOW_QUALIFICATION_MAPPING capture','Revised P03 historical checkpoint clause and P04 gate only after all retained acceptance terms pass'],'exclusions':['historical reconstruction','unrelated P03 acceptance changes','N-REAL','aggregate release','E1 mutation','FINISH execution','P04 execution']}
 authprov,authpin=source('qualification-scope-authority.json',authority)
 s,pins=author_template('E2_AUTHORITATIVE_HANDOFF_SNAPSHOT_1.json','mainline');pins.append(authpin)
 # Materialize current choice/USE permissions as authored initial fixture inputs.
 # The qualification scope authority is separate and is not a native permission.
 d=s.decisions[0];did=identity(jbytes(c._wire(d.dossier)),'planner-dossier-sha256')
 cp,cpin=source('choice-evidence.json',{'decision':d.action.value,'option':'ALLOW_QUALIFICATION_MAPPING','dossier':c._wire(did),'issuer':authority['issuer'],'scope_authority':c._wire(authpin.identity),'scope':SCOPE,'lineage':LINEAGE,'sequence':1});pins.append(cpin)
 gp,gpin=source('grant-source.json',{'subject':'E2-REENTER','permission':'USE','dossier':c._wire(did),'choice':c._wire(cpin.identity),'scope':SCOPE,'lineage':LINEAGE,'qualification_only':True});pins.append(gpin)
 record=m.GraphEntity(m.EntityId('E2-PROSPECTIVE-CHOICE'),m.EntityKind.AUTHORITY,m.ArtifactIdentity(m.IdentityKind.AUTHORITY_IDENTITY,'prospective-choice-authority-v1',hashlib.sha256(jbytes(c._wire(cpin))).hexdigest()),cp,SCOPE,LINEAGE,GEN,100,permissions=(m.AuthorityClass.DECIDE,),target=d.dossier.provenance.identity,decision=d.action,choice='ALLOW_QUALIFICATION_MAPPING')
 grant=m.GraphEntity(m.EntityId('E2-GRANT'),m.EntityKind.AUTHORITY,m.ArtifactIdentity(m.IdentityKind.AUTHORITY_IDENTITY,'prospective-use-authority-v1',hashlib.sha256(jbytes(c._wire(gpin))).hexdigest()),gp,SCOPE,LINEAGE,GEN,100,permissions=(m.AuthorityClass.USE,),target=did,decision=d.action,choice='ALLOW_QUALIFICATION_MAPPING')
 witness=m.GraphEntity(m.EntityId('PROSPECTIVE-SEAL-WITNESS'),m.EntityKind.SOURCE,authpin.identity,authprov,SCOPE,LINEAGE,GEN,100)
 pred=m.Predicate(m.PredicateId('E2-PROSPECTIVE-CHOICE-AUTHORITY'),m.PredicateKind.AUTHORITY,entity=record.id,expected=d.dossier.provenance.identity,permission=m.AuthorityClass.DECIDE)
 use=m.Predicate(m.PredicateId('E2-USE-AUTHORITY'),m.PredicateKind.AUTHORITY,entity=grant.id,expected=did,permission=m.AuthorityClass.USE)
 choice=m.KnowledgeRecord(m.KnowledgeId('decision-choice:E2-DECIDE'),m.KnowledgeState.KNOWN_COMPLETE,'ALLOW_QUALIFICATION_MAPPING',cp)
 s=replace(s,entities=s.entities+(record,grant,witness),predicates=s.predicates+(pred,use),knowledge=s.knowledge+(choice,))
 # Independent oracle authors the exact expected Decision transition from contract.
 # No apply_event/record_result is used during fixture/oracle sealing.
 ed=replace(d,stage=m.DecisionStage.DECISION_RECORDED,history=d.history+(m.DecisionStage.DECISION_RECORDED,),record=record.id,recorded_choice='ALLOW_QUALIFICATION_MAPPING')
 expected=replace(s,decisions=(ed,),statuses=tuple(replace(x,state=m.ActionState.COMPLETED)if x.id==d.action else x for x in s.statuses))
 fixtures={'mainline':(bundle(s,pins),expected)}
 # Independent unknown route fixture, never a patch of executed mainline.
 g,pp=author_template('E2_P03_GATE_QUALIFIED_SNAPSHOT.json','unknown');g=replace(g,entities=g.entities+(witness,));pp.append(authpin);fixtures['unknown']=(bundle(g,pp),g)
 # Adopt accepted-support receipt fixture for disjoint SourceInvalidation controls.
 a,ap=author_template('E2_P03_E05_TARGET_SNAPSHOT.json','accepted-support');a=replace(a,entities=a.entities+(witness,));ap.append(authpin);fixtures['accepted-support']=(bundle(a,ap),a)
 # New proof fixture: all contracts and support fingerprints computed from declared
 # data BEFORE events, never from observed admitted proofs.
 from adapter.tests.test_planner_typed_proofs import fixture,candidate
 v=fixture(SCOPE,LINEAGE)
 kp,kpin=source('typed-knowledge-source.json',{'role':'KNOWLEDGE','statement':'bounded result','scope':SCOPE,'lineage':LINEAGE})
 vp,vpin=source('typed-authority-source.json',{'role':'PROOF_AUTHORITY','permission':'DECIDE','scope':SCOPE,'lineage':LINEAGE})
 sp,spin=source('typed-slot-contract-source.json',{'role':'SLOT_PROOF','proposition':'bounded slot proposition','target':'slot','scope':SCOPE,'lineage':LINEAGE})
 rp,rpin=source('typed-root-contract-source.json',{'role':'ROOT_PROOF','proposition':'independent root proposition','target':'root','scope':SCOPE,'lineage':LINEAGE})
 actp,actpin=source('typed-action-ordering-source.json',{'role':'ACTION_AND_ORDERING','requirement':'root satisfied','scope':SCOPE,'lineage':LINEAGE})
 v=replace(v,context=replace(v.context,generation=GEN),knowledge=tuple(replace(x,provenance=kp)for x in v.knowledge),entities=tuple(replace(x,identity=vpin.identity,provenance=vp,generation=GEN)for x in v.entities),actions=tuple(replace(x,source=actp)for x in v.actions))
 sc=replace(v.proof_contracts[0],scope=SCOPE,lineage=LINEAGE,generation=GEN,provenance=sp,authority_identity=vpin.identity,support_identities=(t.support_identity(v,v.knowledge[0].id),));sc=replace(sc,id=t.identity(sc));slotproof=candidate(sc)
 rootfingerprint=identity(jbytes(c._wire((slotproof.id,))),'planner-proof-support-v1')
 rc=replace(sc,proof_type=m.TypedProofKind.ROOT_PROOF,proposition='independent root proposition',target=v.roots[0].id,supports=(v.slots[0].id,),support_identities=(rootfingerprint,),provenance=rp);rc=replace(rc,id=t.identity(rc))
 v=replace(v,proof_contracts=(sc,rc),entities=v.entities+(witness,),assertions=(m.GraphAssertion(m.AssertionId('retained-order'),actp,relation=m.Relation.REQUIRES,subject=m.ActionId('dependent'),object=v.roots[0].id,ordering_justification='Proof-derived prerequisite remains required after invalidation'),))
 fixtures['typed-support']=(bundle(v,[kpin,vpin,spin,rpin,actpin,authpin]),None)
 # Pin the authority/source contract and sealed negative case definitions, attestor
 # declarations and explicit unresolved root/slot model before execution.
 contract={'schema':'P03-PROSPECTIVE-EXECUTION-CONTRACT-1','dossier':authority['dossier_raw_sha256'],'authority':c._wire(authpin.identity),'scope':SCOPE,'lineage':LINEAGE,'generation':GEN,'boundary':'After RecordedDecision; before EvidenceSourceAdmission/RECEIVED','history':'AUTHOR_DECLARED_INITIAL_PREMISES; PRE_GENESIS_HISTORY=NOT_REPRESENTED','ledger_start':'Actual native no-op ActionReevaluation of independent source witness establishes the first ExecutionEvent before mainline','historical_correspondence':'NOT_ESTABLISHED','historical_reconstruction':False,'known_rule':True,'checkpoint_control':'EXTERNAL_WAIT','checkpoint_actionable':[],'later_functional_target':'Unchanged E06 target is separate evidence; no receipt, REENTER or FINISH mainline event in this boundary suite','negative_cases':['wrong_source_binding','wrong_physical_source','wrong_source_contract','wrong_policy','wrong_policy_identity','wrong_authority','wrong_scope','wrong_lineage','missing_provenance','later_checkpoint','earlier_checkpoint','G04_checkpoint','unrelated_event_lineage','post_hoc_pin_creation','similar_different_pins'],'hashseeds':[0,1,7,101],'cold_readers_per_seed':3,'repeat_writers':2,'variants':['unknown A14','accepted support A15','typed support A15','unknown invalidation A16'],'all_variants_sealed_before_execution':True,'no_production_effect':True}
 conprov,conpin=source('qualification-contract.json',contract)
 extra=[]
 for name,body in [('attestor-and-evidence-contract.json',{'scope':SCOPE,'lineage':LINEAGE,'source_template':str(D/(P+'E2_P03_SEMANTIC_NATIVE_EVIDENCE_BINDING_1_CANDIDATE.json')),'admission_at_mainline':'ABSENT; sealed declaration only; future T01 requires independent transaction','historical_assertion':False}),('root-slot-model.json',{'mainline':c._wire(s.roots),'slots':c._wire(s.slots),'proofs_at_mainline':'NONE','later_E06':'independent retained result'}),('negative-contract.json',contract['negative_cases'])]:
  _,pin=source(name,body);extra.append(pin)
 fixture_records={};file_pins=[]
 for name,(b,expected)in fixtures.items():
  b=replace(b,sources=b.sources+(conpin,)+tuple(extra));m.validate_model(b.current);c._verify_sources(b,ROOT);c.bundle_bytes(b)
  fn=A/(name+'-start.json');write(fn,c.bundle_bytes(b));fpin=m.ArtifactPin(str(fn.relative_to(ROOT)),identity(fn.read_bytes()));file_pins.append(fpin)
  oracle={'schema':'P03-PREEXECUTION-ORACLE-1','fixture':name,'start':c._wire(b.current),'checkpoint':c._wire(expected)if expected else None,'state_expectation_source':'Contract-authored dataclass oracle, not observed apply_event/recompute output','start_control':'HUMAN_HANDOFF'if name=='mainline'else 'EXTERNAL_WAIT'if name=='unknown'else None,'checkpoint_control':'EXTERNAL_WAIT'if name in ('mainline','unknown')else None,'pins':c._wire(b.sources),'policy':c._wire(b.policy),'context':c._wire(b.current.context),'ancestry':{'start':'one real ActionReevaluation event','checkpoint':'one subsequent RecordedDecision event'if name=='mainline'else 'same start/no extra action','parent_snapshot':'Derived from sealed pre-state','parent_event':'Derived by native event identity, never fabricated'},'authority':c._wire(expected.entities if expected else b.current.entities)}
  op=A/(name+'-oracle.json');write(op,jbytes(oracle));file_pins.append(m.ArtifactPin(str(op.relative_to(ROOT)),identity(op.read_bytes())))
  fixture_records[name]={'file':str(fn.relative_to(ROOT)),'oracle':str(op.relative_to(ROOT)),'start_id':c._wire(c.snapshot_id(b.current)),'source_pins':c._wire(b.sources),'policy':c._wire(b.policy),'bundle_id':c._wire(c.bundle_id(b))}
 manifest={'schema':'P03-PREEXECUTION-SEAL-1','authority':authority,'authority_pin':c._wire(authpin),'contract_pin':c._wire(conpin),'fixtures':fixture_records,'files':c._wire(tuple(file_pins)),'runtime_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in (ROOT/'adapter/planner').glob('*.py')},'procedure_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'sequence':1,'execution_started':False,'historical_reconstruction':False,'all_pins_before_execution':True}
 write(A/'seal-final.json',jbytes(manifest));print(json.dumps({'seal':str(A/'seal-final.json'),'id':c._wire(identity(jbytes(manifest),'planner-prospective-fixture-v1'))}))

def verify_seal():
 manifest=json.loads((A/'seal-final.json').read_text())
 assert manifest['authority']['selected_option']=='AUTHORIZE_PROSPECTIVE_P03_CHECKPOINT_QUALIFICATION'
 dossier=D/(P+'P03_CHECKPOINT_SCOPE_DECISION_DOSSIER_1.json');assert hashlib.sha256(dossier.read_bytes()).hexdigest()==manifest['authority']['dossier_raw_sha256']
 assert manifest['execution_started']is False and manifest['all_pins_before_execution']is True
 for w in manifest['files']:c.load_pinned(ROOT,c._unwire(w))
 for f,h in manifest['runtime_hashes'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h
 assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest()==manifest['procedure_sha256']
 for name,info in manifest['fixtures'].items():
  b=load_bundle(ROOT/info['file']);assert c.bundle_id(b)==c._unwire(info['bundle_id']);c._verify_sources(b,ROOT)
 return manifest

def writer(label):
 manifest=verify_seal();outputs={};traces={};invalidations=[]
 for name,info in manifest['fixtures'].items():
  b=load_bundle(ROOT/info['file']);oracle=json.loads((ROOT/info['oracle']).read_text());out=A/'runs'/label/name
  # This is an executed no-op with a named independent source dependency,
  # not a counterfeit GENESIS or a past event reconstructed from a Snapshot.
  witness=next(x for x in b.current.entities if x.id.value=='PROSPECTIVE-SEAL-WITNESS')
  start_event=m.ActionReevaluation((witness.id,),c.snapshot_id(b.current),witness.provenance)
  b=c.record_result(b,start_event);assert b.current==b.initial
  startpath,startid=c.save_bundle(b,out/'starting',ROOT)
  restored=c.restore(startpath,startid,ROOT);assert view(restored)==view(b)
  fresh=subprocess.run([sys.executable,str(Path(__file__)), 'reader',str(startpath.relative_to(ROOT)),startid.sha256],cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(ROOT)),capture_output=True,text=True)
  if fresh.returncode:raise RuntimeError(fresh.stderr)
  fresh_result=json.loads(fresh.stdout);assert fresh_result['view']==view(b)
  if name=='mainline':
   record=next(x for x in b.current.entities if x.id.value=='E2-PROSPECTIVE-CHOICE')
   event=m.RecordedDecision(m.ActionId('E2-DECIDE'),'ALLOW_QUALIFICATION_MAPPING',record.id,m.PredicateId('E2-PROSPECTIVE-CHOICE-AUTHORITY'),c.snapshot_id(b.current))
   b=c.record_result(restored,event)
  if name in ('mainline','unknown'):
   expected=c._unwire(oracle['checkpoint']);assert c.snapshot_bytes(b.current)==c.snapshot_bytes(expected)
   rr=core.recompute(b.current);assert rr.control.value=='EXTERNAL_WAIT'and not rr.actionable
   assert not b.current.receipt_admissions and not b.current.receipt_observations
  if name=='typed-support':
   from adapter.tests.test_planner_typed_proofs import candidate
   for contract in b.current.proof_contracts:
    b=c.record_result(b,m.TypedProofAdmission(candidate(contract),c.snapshot_id(b.current)))
   assert core.recompute(b.current).actionable==(m.ActionId('dependent'),)
  path,bid=c.save_bundle(b,out/'checkpoint',ROOT)
  outputs[name]={'checkpoint_path':str(path.relative_to(ROOT)),'checkpoint_id':c._wire(bid),'state_id':c._wire(c.snapshot_id(b.current)),'starting_path':str(startpath.relative_to(ROOT)),'starting_id':c._wire(startid),'writer_pid':os.getpid(),'start_fresh_reader_pid':fresh_result['pid'],'start_fresh_reader_result':'PASS','view':view(b)}
  traces[name]=c._wire(b.events)
  if name in ('accepted-support','typed-support'):
   # Disjoint raw supports: every source actually used by current state.
   provs={jbytes(x['identity'])for x in descendants(c._wire(b.current))if x.get('$type')=='Provenance'}
   for index,pin in enumerate(b.sources):
    if jbytes(c._wire(pin.identity))not in provs:continue
    changed=c.record_result(b,m.SourceInvalidation((pin.identity,),c.snapshot_id(b.current)))
    assert len(changed.current.actions)==len(b.current.actions)and len(changed.current.assertions)==len(b.current.assertions)
    assert len(changed.current.roots)==len(b.current.roots)and len(changed.current.slots)==len(b.current.slots)
    stale=[x for x in changed.current.knowledge if x.provenance.identity==pin.identity]
    assert all(x.validation is m.ValidationState.STALE for x in stale)
    if name=='typed-support'and pin.path.endswith(('typed-knowledge-source.json','typed-authority-source.json','typed-slot-contract-source.json','typed-root-contract-source.json','typed-action-ordering-source.json')):
     assert m.ActionId('dependent')not in core.recompute(changed.current).actionable
    ip,ii=c.save_bundle(changed,out/('invalidation-%02d'%index),ROOT)
    assert view(c.restore(ip,ii,ROOT))==view(changed)
    invalidations.append({'fixture':name,'source':c._wire(pin),'path':str(ip.relative_to(ROOT)),'id':c._wire(ii),'after_state':c._wire(c.snapshot_id(changed.current)),'oracle':'mandatory obligations retained; direct knowledge stale; typed dependent held; no shortcut','result':'PASS'})
  if name=='unknown':
   route=b.current.external_gates[0].resolution_contracts[0].provenance.identity
   changed=c.record_result(b,m.SourceInvalidation((route,),c.snapshot_id(b.current)));assert core.recompute(changed.current).control.value=='PLAN_DEFECT'
   ip,ii=c.save_bundle(changed,out/'route-invalidation',ROOT)
   assert view(c.restore(ip,ii,ROOT))==view(changed)
   invalidations.append({'fixture':'unknown','case':'A16','path':str(ip.relative_to(ROOT)),'id':c._wire(ii),'result':'PASS_PLAN_DEFECT'})
 report={'writer_pid':os.getpid(),'label':label,'outputs':outputs,'trace':traces,'invalidations':invalidations,'no_FINISH_result':True,'sealed_fixture_unchanged':True}
 write(A/'runs'/label/'writer-result.json',jbytes(report));print(json.dumps({'writer_pid':os.getpid(),'report':str(A/'runs'/label/'writer-result.json')}))

def reader(path,sha):
 verify_seal();b=c.restore(ROOT/path,m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'planner-bundle-v1',sha),ROOT)
 replay=c._replay(b);assert c.snapshot_id(replay)==c.snapshot_id(b.current)
 print(json.dumps({'pid':os.getpid(),'view':view(b),'source_policy_replay':'PASS','events':len(b.events)}))

if __name__=='__main__':
 os.chdir(ROOT)
 mode=sys.argv[1]
 if mode=='seal':seal()
 elif mode=='writer':writer(sys.argv[2])
 elif mode=='reader':reader(sys.argv[2],sys.argv[3])
