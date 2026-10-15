import copy,json,hashlib
from pathlib import Path
from adapter.planner import codec as c,model as m
R=Path(__file__).resolve().parents[4];D=R/'docs/plans';Q=D/'qualification/INSTALLATION_I05_1';P='DETERMINISTIC_PLANNER_V0_1_'
x=json.loads((D/(P+'E2_PC01_FIXTURES.json')).read_text());ref=json.loads((D/(P+'C06A_3_PREFLIGHT_CLOSURE_1.json')).read_text())['reference'];assert hashlib.sha256(ref['program'].encode()).hexdigest()==ref['sha256'];ns={};exec(ref['program'],ns)
manifest=json.loads((Q/'p04-manifest.json').read_text());b=c.restore(Path(manifest['path']),c._unwire(manifest['bundle_id']),R)
ctx={k:getattr(b.current.context,k) for k in ('scope','lineage','generation')};p=copy.deepcopy(x['profile']);p['context']=ctx
for a in b.current.actions:
 d=p['definitions'][a.id.value];d['scope']=ctx['scope'];d['lineage']=ctx['lineage'];d['provenance']=c._wire(a.source);d['primary_operation_class']=a.operation.value;d['effect_boundary']=a.effect.value;d['stage_role']=a.stage.value
 d['prerequisite_actions']=[{'domain':'ActionId','id':g.target.value} for g in a.prerequisites if g.kind is m.GateKind.ACTION_COMPLETED]
 d['result_contract']['accepted_outcome']=a.accepted_result.value
 d['result_contract']['knowledge_outputs']=[{'id':k.id.value,'type':'KnowledgeRecord','statement':k.statement,'producer':k.producer.value,'outcome':k.outcome.value} for k in a.accepted_inventory]
plan={'schema':'E2-CANONICAL-ACTION-PLAN-1','resolution_actions':list(p['definitions'].values())};h=lambda z:hashlib.sha256(c.canonical_bytes(z)).hexdigest();p['pins']['plan']=h(plan)
s=copy.deepcopy(x['submission']);s['context']=ctx;s['sources']['plan']=plan;s['profile_pin']=h(p);v={'context':ctx,'sources':{'plan':{'identity':h(plan),'state':'CURRENT'}}}
r=ns['evaluate'](p,s,v,'ACTION');assert r['accepted'],r;assert len(r['output'])==6
(Q/'p04-o01-qualification.json').write_bytes(c.canonical_bytes({'profile':p,'submission':s,'validity':v,'result':r,'program_sha256':ref['sha256'],'native_actions':c._wire(b.current.actions),'all_fields_preserved_except_R06_frame':True}));print('O01 6/6 PASS')
