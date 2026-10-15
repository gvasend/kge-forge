"""F02 sealed boundary/negative checks and cold-reader orchestration for F03."""
import json,sys,os,subprocess,hashlib,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from dataclasses import replace,fields,is_dataclass
from pathlib import Path
from adapter.tests import qualify_finish_f03 as q
from adapter.planner import codec as c,model as m,core,gates,installation as i,proof_installation as pi,typed_proofs as tp
from adapter.tests.test_planner_typed_proofs import candidate
R,D,O,Q=q.R,q.D,q.O,q.Q

def load_manifest(man):return c.restore(Path(man['path']),c._unwire(man['bundle_id']),R)
def load(name):return load_manifest(c.parse_json((O/'isolated-checkpoints.json').read_bytes())[name])
def input_bundle(path):return c._unwire(c.parse_json(Path(path).read_bytes())['bundle'])
def permute(value,mode):
 if is_dataclass(value):
  updates={f.name:permute(getattr(value,f.name),mode) for f in fields(value)}
  for f in c.SET_FIELDS.get(type(value),()):
   seq=updates[f];updates[f]=tuple(reversed(seq)) if mode=='reverse' else seq[1:]+seq[:1]
  return replace(value,**updates)
 if type(value) is tuple:return tuple(permute(x,mode) for x in value)
 return value

def boundaries():
 man=c.parse_json((O/'isolated-checkpoints.json').read_bytes());sealed=c.parse_json((Q/'boundary-oracles.json').read_bytes())['oracles'];rows={}
 mapping={'POST_A12_PRE_SUPPORT':'post-a12','POST_SUPPORT':'slot-contract','POST_SLOT_PROOF':'post-slot-proof','POST_ROOT_PROOF':'post-root-proof','POST_ROOT_SATISFACTION':'post-root-proof','PRE_FINISH':'post-root-proof','POST_FINISH':'isolated-p04-target','P04_TARGET':'isolated-p04-target'}
 for name,checkpoint in mapping.items():
  b=load_manifest(man[checkpoint]);s=b.current;expected=sealed[name];comp=core.recompute(s);fin=next(a for a in s.actions if a.id.value=='E2-FINISH');stat=next(x for x in comp.statuses if x.id==fin.id)
  checks={'control':comp.control.value==expected['control'],'slot':s.slots[0].state.value==expected['slot'],
   'root':s.roots[0].state.value==expected['root'],'proofs':{i.simple(p.id)['sha256'] for p in s.typed_proofs}=={x['sha256'] for x in expected['typed_proofs']},
   'goals':c.canonical_bytes(c._wire(s.goals))==c.canonical_bytes(expected['goal_inventory']),
   'reenter_completed':gates.current_completion(s,m.ActionId('E2-REENTER')),
   'actual_reenter_output':next(k for k in s.knowledge if k.id.value=='E2-K-REENTER')==next(a for a in s.actions if a.id.value=='E2-REENTER').accepted_inventory[0],
   'current_sources':all(i.current(b,r) for r in pi.records(s,'ROOT_SLOT_CONFIGURATION_SET')),
   'proof_usability':all(tp.usable(s,p) for p in s.typed_proofs),
   'unrelated_completed':all(x.state is m.ActionState.COMPLETED for x in s.statuses if x.id!=fin.id),
   'finishing_inventory_unchanged':fin.accepted_inventory==next(a for a in b.initial.actions if a.id==fin.id).accepted_inventory}
  if name in ('POST_A12_PRE_SUPPORT','POST_SUPPORT','POST_SLOT_PROOF'):
   checks.update(nonterminal_hold=stat.state is m.ActionState.BLOCKED and not stat.terminal_failure and not fin.blocked_terminal,finish_unexecuted=not gates.current_completion(s,fin.id))
  elif name in ('POST_ROOT_PROOF','POST_ROOT_SATISFACTION','PRE_FINISH'):
   checks.update(finishing_selected=comp.selection.selected==fin.id,finish_unexecuted=not gates.current_completion(s,fin.id))
  else:
   checks.update(finish_completed=gates.current_completion(s,fin.id),actual_finish_output=next(k for k in s.knowledge if k.id.value=='E2-K-FINISH')==fin.accepted_inventory[0],all_goals_proven=all(r.state is m.ConditionState.SATISFIED for r in s.roots),no_further_action=not comp.actionable)
  assert all(checks.values()),(name,checks);rows[name]={'status':'PASS','checks':checks,'checkpoint':man[checkpoint]}
  print('BOUNDARY',name,'PASS',flush=True)
 q.emit('boundary-comparisons.json',rows)

def negatives():
 b=load('root-contract');s=b.current;sc,rc=s.proof_contracts;sc=next(p for p in s.proof_contracts if p.proof_type is m.TypedProofKind.SLOT_PROOF);rc=next(p for p in s.proof_contracts if p.proof_type is m.TypedProofKind.ROOT_PROOF)
 root_entity=next(e for e in s.entities if e.provenance.identity==rc.provenance.identity);cases={}
 def reject(n,fn):
  try:fn()
  except m.PlannerError as e:cases[n]={'status':'PASS','reason':str(e)}
  else:raise AssertionError(n)
 def oracle(n,ok,reason):
  assert ok,n;cases[n]={'status':'PASS','reason':reason}
 def proof_on(state):return core.apply_event(state,m.TypedProofAdmission(candidate(rc),c.snapshot_id(state)))
 for n,change in [('F02-N01',{'provenance':sc.provenance,'identity':sc.provenance.identity}),('F02-N02',{'identity':sc.provenance.identity}),('F02-N03',{'proposition':{'id':'wrong'}}),('F02-N04',{'provenance_origin':json.loads(sc.provenance.excerpt)['provenance_origin']}),('F02-N25',{'asserts_satisfaction':True})]:
  if 'proposition' in change or 'provenance_origin' in change or 'asserts_satisfaction' in change:
   raw=c.canonical_bytes(dict(json.loads(root_entity.provenance.excerpt),**change));p=replace(root_entity.provenance,excerpt=raw.decode(),identity=c._identity(raw,'raw-file-sha256'));change={'identity':p.identity,'provenance':p}
  state=replace(s,entities=tuple(replace(e,**change) if e.id==root_entity.id else e for e in s.entities))
  reject(n,lambda state=state:proof_on(state))
 for n,change in [('F02-N05',{'lineage':'foreign'}),('F02-N06',{'generation':'foreign'}),('F02-N07',{'authority':m.EntityId('PC02-old-baseline-authority')})]:
  wrong=replace(candidate(rc),**change);wrong=replace(wrong,id=tp.identity(wrong))
  reject(n,lambda wrong=wrong:core.apply_event(s,m.TypedProofAdmission(wrong,c.snapshot_id(s))))
 conf=pi.records(s,'ROOT_SLOT_CONFIGURATION_SET')[0].request;initial=input_bundle(D/(q.P+'E2_P04_POST_REENTER_DEFINITION_INSTALL_BUNDLE_1.json')).current
 def config_bad(n,change):
  bad=replace(conf,**change);bad=replace(bad,command_key=i.command_key(bad));reject(n,lambda:i.apply(initial,bad))
 config_bad('F02-N08',{'authority':replace(conf.authority,authority_class=m.AuthorityClass.DECIDE)})
 config_bad('F02-N09',{'authority_bindings':(replace(conf.authority_bindings[0],authority_class=m.AuthorityClass.INSTALL),)})
 wrong=replace(candidate(sc),contract=rc.id);wrong=replace(wrong,id=tp.identity(wrong));reject('F02-N10',lambda:core.apply_event(s,m.TypedProofAdmission(wrong,c.snapshot_id(s))))
 root=load('post-root-proof');fin=next(a for a in root.current.actions if a.id.value=='E2-FINISH');supplied=m.SuppliedResult(fin.id,fin.accepted_result,fin.accepted_inventory,c.snapshot_id(root.current))
 invalid=core.apply_event(root.current,m.ProofDependencyChange((root_entity.id,),c.snapshot_id(root.current),rc.provenance)).snapshot
 oracle('F02-N11',invalid.roots[0].state is m.ConditionState.UNRESOLVED,'Independent root-source invalidation withdraws root satisfaction')
 post=load('post-a12');oracle('F02-N12',fin.id not in core.recompute(post.current).actionable,'Unsatisfied root keeps FINISH non-actionable')
 for terminal in (False,True):
  state=replace(root.current,actions=tuple(replace(a,blocked_terminal=True) if a.id==fin.id else a for a in root.current.actions),statuses=tuple(replace(x,state=m.ActionState.BLOCKED,terminal_failure=terminal) if x.id==fin.id else x for x in root.current.statuses))
  assert fin.id not in core.recompute(tp.reevaluate(state,state,(rc.target,),rc.provenance)).actionable
 oracle('F02-N13',True,'Terminal prerequisite hold and failed execution both remain closed')
 oracle('F02-N14',all(x.state is m.ActionState.COMPLETED for x in root.current.statuses if x.id!=fin.id),'No unrelated completed Action reopens at root admission')
 for n,change in [('F02-N15',{'result':m.ActionResult.FAIL}),('F02-N16',{'knowledge':()}),('F02-N17',{'knowledge':supplied.knowledge+(replace(supplied.knowledge[0],id=m.KnowledgeId('extra')), )})]:
  reject(n,lambda change=change:core.apply_event(root.current,replace(supplied,**change)))
 sr=pi.records(s,'SLOT_PROOF_CONTRACT_DEFINITION')[0].request;rr=pi.records(s,'ROOT_PROOF_CONTRACT_DEFINITION')[0].request
 d,body=pi.descriptor(sr.definition)
 before=load_manifest(c.parse_json((O/'configuration-manifest.json').read_bytes()))
 reject('F02-N18',lambda:pi.apply(before.current,sr,d,body))
 changed=replace(post.current,knowledge=tuple(replace(k,statement='changed actual output') if k.id.value=='E2-K-REENTER' else k for k in post.current.knowledge))
 reject('F02-N19',lambda:pi.apply(changed,sr,d,body))
 dr,br=pi.descriptor(rr.definition);reject('F02-N20',lambda:pi.apply(post.current,rr,dr,br))
 config_bad('F02-N21',{'definition':replace(conf.definition,provenance=replace(conf.definition.provenance,excerpt='{"metadata_wrapper":true}'))})
 config_bad('F02-N22',{'expected_snapshot':c.snapshot_id(before.current)})
 wrongbody=dict(body,contract=c._wire(candidate(sc)));wrongraw=c.canonical_bytes(wrongbody)
 wrong=replace(sr.definition,provenance=replace(sr.definition.provenance,excerpt=wrongraw.decode(),identity=c._identity(wrongraw,'raw-file-sha256')))
 reject('F02-N23',lambda:pi.descriptor(wrong))
 config_bad('F02-N24',{'authority_bindings':()})
 altered=replace(candidate(rc),support_identities=(c._identity(b'invented','planner-proof-support-v1'),));altered=replace(altered,id=tp.identity(altered))
 reject('F02-N26',lambda:core.apply_event(s,m.TypedProofAdmission(altered,c.snapshot_id(s))))
 reject('F02-N27',lambda:pi.apply(before.current,rr,dr,br))
 old=c._unwire(c.parse_json((D/'qualification/INSTALLATION_I05_1/fresh-a09-candidate.json').read_bytes()));_,_,binding=q.inputs();raw={p.path:(R/p.path).read_bytes() for p in old.source_additions}
 reject('F02-N28',lambda:c.preflight_external_evidence(before,old,raw,R,expected_binding=binding))
 oracle('F02-N29',fin.id not in core.recompute(invalid).actionable,'Independent root-source invalidation withdraws FINISH readiness')
 target=load('isolated-p04-target');after=core.apply_event(target.current,m.ProofDependencyChange((root_entity.id,),c.snapshot_id(target.current),rc.provenance)).snapshot
 oracle('F02-N30',not core.recompute(after).actionable and gates.current_completion(after,fin.id),'Completed FINISH remains historical and cannot rerun after invalidation')
 reject('F02-N30',lambda:core.apply_event(after,replace(supplied,expected_snapshot=c.snapshot_id(after))))
 cases['F02-N30']['historical_completion_retained']=True
 assert set(cases)=={x['id'] for x in c.parse_json((Q/'negative-contract.json').read_bytes())['cases']}
 for x in c.parse_json((Q/'negative-contract.json').read_bytes())['cases']:cases[x['id']]['sealed_case']=x['case']
 q.emit('f02-negative-results.json',cases);print('F02_NEGATIVES_PASS',len(cases),flush=True)

def prepare_readers():
 manifests=c.parse_json((O/'isolated-checkpoints.json').read_bytes());manifests['final-preexecution']=c.parse_json((O/'configuration-manifest.json').read_bytes())
 head=c.parse_json((O/'install-store-0/HEAD.json').read_bytes())
 config_path=O/'install-store-0'/('bundle-'+head['bundle']['sha256']+'.json')
 config=c._unwire(c.parse_json(config_path.read_bytes())['bundle'])
 manifests['installed-source-configuration']={'path':str(config_path),'root':str(R),'bundle_id':head['bundle'],'state_id':c._wire(c.snapshot_id(config.current)),'head':c._wire(config.events[-1].identity),'event_count':len(config.events),'boundary':'installed-source-configuration'}
 folder=O/'reader-manifests';folder.mkdir(exist_ok=True)
 for name,man in manifests.items():
  b=load_manifest(man);path=O/'cold-reader-bundles'/name/(name+'.json');path.parent.mkdir(parents=True,exist_ok=True)
  copied=q.save(b,path);assert copied['bundle_id']==man['bundle_id'] and copied['state_id']==man['state_id'];man.update(copied)
  man['semantic_oracle']=q.semantic_view(b);man['writer_terminated']=True
  (folder/(name+'.json')).write_bytes(c.canonical_bytes(man))
 q.emit('reader-plan.json',{'seeds':[0,1,7,101],'readers_per_boundary_per_seed':3,'boundaries':list(manifests),'writer_process_terminated':True,'status':'SEALED_COMPARISON_MANIFESTS'})
 print('READERS_PREPARED',len(manifests),flush=True)

def readers(generic=False):
 paths=[O/'generic-reader-manifest.json'] if generic else sorted((O/'reader-manifests').glob('*.json'));results=[]
 output='generic-fresh-reader-results.json' if generic else 'fresh-reader-results.json'
 def run(path,seed,index):
  env=dict(os.environ,PYTHONHASHSEED=str(seed),PYTHONDONTWRITEBYTECODE='1',PYTHONPATH='.')
  p=subprocess.run([sys.executable,'adapter/tests/qualify_finish_f03.py','reader',str(path)],cwd=R,env=env,text=True,capture_output=True)
  log=O/'reader-logs';log.mkdir(exist_ok=True);(log/(path.stem+'-'+str(seed)+'-'+str(index)+'.log')).write_text(p.stdout+p.stderr)
  assert p.returncode==0,(path,seed,index,p.stderr)
  return {'boundary':path.stem,'seed':seed,'reader':index,'exit':p.returncode,'result':json.loads(p.stdout)}
 with ThreadPoolExecutor(max_workers=6) as pool:
  tasks=[pool.submit(run,path,seed,index) for path in paths for seed in (0,1,7,101) for index in range(3)]
  for done in as_completed(tasks):
   results.append(done.result());q.emit(output,sorted(results,key=lambda x:(x['boundary'],x['seed'],x['reader'])))
   print('COLD_READERS_PASS',len(results),'/',len(tasks),flush=True)

def permutations():
 results={}
 for name,man in c.parse_json((O/'isolated-checkpoints.json').read_bytes()).items():
  b=load_manifest(man);expected=q.semantic_view(b);rows={}
  for mode in ('reverse','rotate'):
   changed=permute(b,mode)
   assert c._bundle_bytes_admitted(changed)==Path(man['path']).read_bytes()
   m.validate_model(changed.current);assert q.semantic_view(changed)==expected
   assert c.snapshot_id(c._replay(changed))==c.snapshot_id(b.current)
   rows[mode]={'canonical_bytes':'PASS','native_identity':'PASS','model':'PASS','full_computation':'PASS','proofs_C03':'PASS','replay':'PASS'}
  results[name]=rows;print('PERMUTATIONS_PASS',name,flush=True)
 q.emit('unordered-permutations.json',results)

if __name__=='__main__':{'boundaries':boundaries,'negatives':negatives,'prepare-readers':prepare_readers,'readers':readers,'generic-readers':lambda:readers(True),'permutations':permutations}[sys.argv[1]]()
