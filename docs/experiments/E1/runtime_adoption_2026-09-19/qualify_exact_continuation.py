"""Exact existing C1 in isolated qualification runtime-head store, no invocation."""
import sys,json,tempfile,time,multiprocessing
from pathlib import Path
O=Path(__file__).resolve().parent;Q=O.parent/'run2_control_plane_binding_2026-09-18';sys.path.insert(0,str(O));from test_runtime_adoption import Fixture,r,ControllerAuthorityStore,encoded,sha
pub=json.loads((Q/'QUALIFIED_PUBLICATION.json').read_bytes());original=json.loads((Q/'PROPOSED_PRODUCTION_CONTINUATION.json').read_bytes())
assert sha((Q/'PROPOSED_PRODUCTION_CONTINUATION.json').read_bytes())==pub['proposed_production_continuation_file_sha256']
f=Fixture.__new__(Fixture);f.root=Path(tempfile.mkdtemp(prefix='runtime-exact-c1-qualification-'));f.root.chmod(0o700);f.records={};f.kind='QUALIFICATION_BINDING';f.ledger=f.root/'runtime.jsonl';f.ledger.touch(mode=0o600)
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
f.p['adoptions']=[{'continuation':c,'grant':g}];f.p['qualified_evidence']=[qref];f.finish();start=time.monotonic()
before=r.reconstruct(f.s);s=r.adopt(f.s,c,g,binding_kind='QUALIFICATION_BINDING');seconds=time.monotonic()-start
queue=multiprocessing.Queue()
def fresh():
 st=ControllerAuthorityStore(**f.pin)
 try:queue.put(r.reconstruct(st))
 finally:st.close()
p=multiprocessing.Process(target=fresh);p.start();p.join(30);assert not p.is_alive();recovered=queue.get(timeout=2);assert recovered==s
result={'result':'PASS_EXACT_C1_IN_ISOLATED_ADOPTION_QUALIFICATION','production_adoption':False,'synthetic_decisions_only':True,'ordinary_continuation':original['continuation_id'],'ordinary_file_sha256':pub['proposed_production_continuation_file_sha256'],'runtime_before':before['current_runtime'],'runtime_after':s['current_runtime'],'wrapper':f.obj(c)['id'],'authority':f.p['id'],'store':f.pin,'journal':str(f.ledger),'seconds':seconds,'independent_reconstruction':'PASS','real_invocations':0,'real_model_requests':0,'real_effects':0}
(O/'EXACT_C1_QUALIFICATION.json').write_bytes(encoded(result));f.s.close();print(json.dumps(result))
