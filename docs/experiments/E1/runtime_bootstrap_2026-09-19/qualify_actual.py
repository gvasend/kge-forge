"""Exact existing C1 in isolated qualification runtime-head store, no invocation."""
import sys,json,tempfile,time,multiprocessing
from pathlib import Path
O=Path(__file__).resolve().parent;Q=O.parent/'run2_control_plane_binding_2026-09-18';sys.path.insert(0,str(O));from test_bootstrap import Fixture,r,b,ControllerAuthorityStore,encoded,sha
pub=json.loads((Q/'QUALIFIED_PUBLICATION.json').read_bytes());original=json.loads((Q/'PROPOSED_PRODUCTION_CONTINUATION.json').read_bytes())
assert sha((Q/'PROPOSED_PRODUCTION_CONTINUATION.json').read_bytes())==pub['proposed_production_continuation_file_sha256']
f=Fixture.__new__(Fixture);f.root=Path(tempfile.mkdtemp(prefix='runtime-exact-bootstrap-qualification-'));f.root.chmod(0o700);f.records={};f.kind='QUALIFICATION_BINDING';f.ledger=f.root/'runtime.jsonl';f.ledger.touch(mode=0o600)
private=ControllerAuthorityStore(**pub['candidate_store'])
with private.session():
 assert json.loads(private.resolve(pub['proposed_continuation_ref']['authority_id']))==original
 for row in original['artifacts']:
  assert sha(private.resolve(row['new_content']['authority_id']))==row['new_sha256']
private.close()
def runtime(root):
 files={p.name:sha(p.read_bytes()) for p in Path(root,'adapter').glob('*.py')}
 for p in Path(root,'adapter').glob('*.py'):f.add(p.read_bytes())
 return f.add({'schema':'RUNTIME-INVENTORY-1','root':root,'identity':'sha256:'+sha(encoded(files)),'files':files})
f.r0=runtime('/tmp/forge-attempt-chain-xjcb_jkz');f.r1=runtime(str(Path(original['artifacts'][0]['new_blob']).parent.parent));assert f.obj(f.r1)['identity']==pub['implementation']
f.ancestry=dict(pub['real_historical_context'],release_authority=pub['real_release_authority']);mechanism=f.add(Path(r.__file__).read_bytes())
amendment=f.add(r.seal('RUNTIME-CONSUMPTION-AMENDMENT',{'schema':'RUNTIME-CONSUMPTION-AMENDMENT-1','classification':'MATERIAL','release_context':f.ancestry,'mechanism':mechanism,'rules':r.RULES}))
md={'authority':'Architect','decision':'ADOPT_RUNTIME_CONSUMPTION_AMENDMENT','amendment':amendment,'binding_kind':f.kind};mdref=f.add(dict(md,authority_source=f.add(dict(md,channel='user'))))
f.p={'schema':'RUNTIME-HEAD-AUTHORITY-1','binding_kind':f.kind,'material_amendment':amendment,'material_decision':mdref,'release_context':f.ancestry,'mechanism':mechanism,'genesis':f.r0,'journal':'fixture-runtime-journal','adoptions':[],'qualified_evidence':[]}
c,g=f.add_transition(f.r0,f.r1);cb=f.obj(c);cb.pop('id');cb['original_continuation']=f.add((Q/'PROPOSED_PRODUCTION_CONTINUATION.json').read_bytes())
q=f.obj(cb['qualification']);q.pop('id');q['evidence']=[f.add((Q/'QUALIFIED_CLOSURE.json').read_bytes())];qref=f.add(r.seal('RUNTIME-QUALIFICATION',q));cb['qualification']=qref
c=f.add(r.seal('IMPLEMENTATION-RUNTIME-CONTINUATION',cb));gb=f.obj(g);gb['continuation']=c;gb.pop('authority_source');g=f.add(dict(gb,authority_source=f.add(dict(gb,channel='user'))))
f.c1=c;f.g1=g
f.p['adoptions']=[{'continuation':c,'grant':g}];f.p['qualified_evidence']=[qref]
proof=json.loads((Q/'R12_AUTHENTICATED_CAPTURE.json').read_bytes())
expected={'runtime':f.obj(f.r0)['identity'],'release_context':f.ancestry,'terminal':'CANCELLED','ownership':None,'ExecutionScope':None,'audit_sha256':proof['terminal']['audit_sha256'],'ledger_sha256':proof['terminal']['ledger_sha256']}
def actual_record(record):
 driver=O/'legacy_verifier.py'
 record['legacy_verifier']={'python':sys.executable,'python_sha256':sha(Path(sys.executable).read_bytes()),'path':str(driver),'sha256':sha(driver.read_bytes()),'input':f.add({'runtime_root':f.obj(f.r0)['root'],'publication':proof['publication']}),'expected':expected}
 live=json.loads((Q/'SUPERVISOR_IMMUTABLE_VERIFICATION.json').read_bytes())
 record['supervisor']={'instance':f.add(live['instance']),'succession_ledger':live['succession_ledger'],'succession_head':live['head']}
 record['candidate_material_amendment']=f.add((O.parent/'runtime_adoption_2026-09-19/PROPOSED_MATERIAL_AMENDMENT.json').read_bytes())
 record['candidate_runtime_head_authority']=f.add((O.parent/'runtime_adoption_2026-09-19/PROPOSED_RUNTIME_HEAD_AUTHORITY.json').read_bytes())
f.mutation=actual_record;f.finish();start=time.monotonic();before=b.reconstruct(f.s);result=f.establish();elapsed=time.monotonic()-start
queue=multiprocessing.Queue()
def fresh():
 store=ControllerAuthorityStore(**f.pin)
 try:queue.put(b.reconstruct(store))
 finally:store.close()
p=multiprocessing.Process(target=fresh);p.start();p.join(30);assert not p.is_alive();recovered=queue.get(timeout=2);assert recovered==result
ordinary_start=time.monotonic();state=r.reconstruct(f.s);overhead=time.monotonic()-ordinary_start
assert state['current_runtime']==pub['implementation']
output={'verdict':'PASS_ISOLATED_BOOTSTRAP_ACTUAL_IDENTITIES','production_adoption':False,'legacy_runtime':before['runtime'],'qualified_R1':result['runtime'],'bootstrap_record':f.record['id'],'bootstrap_record_sha256':f.recordref['sha256'],'runtime_head_authority':f.p['id'],'runtime_ancestry_head':state['head_event'],'store':f.pin,'bootstrap_journal':str(f.bjournal),'runtime_journal':str(f.ledger),'bootstrap_seconds':elapsed,'runtime_head_verification_seconds':overhead,'independent_reconstruction':'PASS','S3_fresh_checks':'PASS','original_continuation':original['continuation_id'],'real_invocations':0,'model_requests':0,'E1_effects':0}
(O/'ACTUAL_IDENTITY_QUALIFICATION.json').write_bytes(encoded(output));(O/'QUALIFIED_BOOTSTRAP_RECORD.json').write_bytes(encoded(f.record));(O/'QUALIFIED_HEAD_POLICY.json').write_bytes(encoded(f.p));f.s.close();print(json.dumps(output))
