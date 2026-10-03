"""PC01 definition qualification only. Never executes a Planner Action/event."""
import copy
import hashlib
import json
import pathlib
import sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from adapter.planner import model as m, codec as c, selector
P = ROOT / 'docs/plans'
S = 'DETERMINISTIC_PLANNER_V0_1_E2_PC01'
def canon(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
def digest(x):
    return hashlib.sha256(canon(x)).hexdigest()
def load(s):
    return json.loads((P / (S+s+'.json')).read_text())
def qualify():
    fixture, source, roles = load('_FIXTURES'), load('_SOURCES'), load('_SOURCE_ROLES')
    governing = json.loads((P/'DETERMINISTIC_PLANNER_V0_1_C06A_3_PREFLIGHT_CLOSURE_1.json').read_text())
    program = governing['reference']['program']
    assert hashlib.sha256(program.encode()).hexdigest() == governing['reference']['sha256']
    ns = {}; exec(compile(program, 'PINNED_O01_SPECIFICATION', 'exec'), ns)
    p, s, v = fixture['profile'], fixture['submission'], fixture['validity']
    # Trusted authored definition semantics, not implementation-computed outputs.
    assert len(source['declarations']) == len(p['definitions']) == 6
    assert sum(len(x) for x in p['definitions'].values()) == 78
    for d in source['declarations']:
        a = p['definitions'][d['id']]
        assert a['primary_operation_class'] == d['operation']
        assert a['effect_boundary'] == d['effect'] == 'NON_EFFECTING'
        assert a['scope'] == d['scope'] and a['lineage'] == d['lineage']
        assert [x['id'] for x in a['prerequisite_actions']] == d['prerequisites']
        assert set(a['knowledge_requirements']) == set(d['knowledge'])
        assert a['result_contract']['knowledge_outputs'] == ([] if d['output'] is None else [d['output']])
        assert not a['result_contract']['execution_asserted']
    accept = ns['evaluate'](p,s,v,'ACTION'); assert accept['accepted']
    native = [c._unwire(x) for x in fixture['native_actions']]
    for action in native:
        m.validate_types(action,m.Action);m.validate_provenance(action.source)
        for k in action.accepted_inventory:m.validate_knowledge(k)
        assert action.id.value in accept['output']
        assert c._wire(action) == next(x for x in fixture['native_actions'] if x['id']['value']==action.id.value)
    assert fixture['native_actual_knowledge']==fixture['execution_ledger']==[]
    negatives=[]
    for i,row in enumerate(s['sources']['plan']['resolution_actions']):
        for field in row:
            mutant=copy.deepcopy(s);del mutant['sources']['plan']['resolution_actions'][i][field]
            result=ns['evaluate'](p,mutant,v,'ACTION');assert not result['accepted']
            negatives.append({'action':row['id'],'mutation':'delete '+field,'result':result['failed_clause']})
    for field,value in [('primary_operation_class','OTHER'),('effect_boundary','PRODUCTION_EFFECT'),('scope','WRONG'),('lineage','WRONG'),('prerequisite_actions',[{'domain':'KnowledgeId','id':'E2-CHECK'}]),('prerequisite_actions',[{'domain':'ActionId','id':'MISSING'}])]:
        mutant=copy.deepcopy(s);mutant['sources']['plan']['resolution_actions'][0][field]=value
        result=ns['evaluate'](p,mutant,v,'ACTION');assert not result['accepted']
        negatives.append({'mutation':field,'result':result['failed_clause']})
    vv=copy.deepcopy(v);vv['sources']['plan']['state']='STALE'
    result=ns['evaluate'](p,s,vv,'ACTION');assert not result['accepted'];negatives.append({'mutation':'stale plan','result':result['failed_clause']})
    # Exact source-role signature is a fixture contract, not inferred from shape.
    bound=roles['bound_rows']
    def role_valid(row):
        expected=next((r for r in bound if r['target']==row.get('target')),None)
        if row!=expected:return False
        pin=c._unwire(row['source_pin'])
        return hashlib.sha256((ROOT/pin.path).read_bytes()).hexdigest()==pin.identity.sha256
    assert all(role_valid(r) for r in bound)
    role_negatives=[]
    for field,value in [('role','GRANT'),('scope','WRONG'),('lineage','WRONG'),('currentness','HISTORICAL_ONLY')]:
        r=copy.deepcopy(bound[0]);r[field]=value;assert not role_valid(r);role_negatives.append(field)
    r=copy.deepcopy(bound[0]);r['source_pin']['identity']['kind']={'$enum':'IdentityKind','value':'AUTHORITY_IDENTITY'}
    assert not role_valid(r);role_negatives.append('same digest wrong domain')
    r=copy.deepcopy(bound[0]);r['source_pin']['identity']['sha256']='0'*64
    assert not role_valid(r);role_negatives.append('substituted source')
    selector.validate_policy(selector.POLICY_PIN,fixture['persistence']['policy_version'])
    # Metamorphic independent identity rules: definitions are a keyed inventory;
    # prerequisite lists keep their authored canonical order. No ledger reordered.
    normal=lambda x:sorted(x,key=lambda a:a['id']['value'])
    identity=digest(normal(fixture['native_actions']))
    assert identity==digest(normal(list(reversed(fixture['native_actions']))))
    swapped=json.loads(json.dumps(fixture['native_actions'],sort_keys=False))
    assert identity==digest(normal(swapped))
    assert digest(sorted(bound,key=lambda r:canon(r['target'])))==digest(sorted(list(reversed(bound)),key=lambda r:canon(r['target'])))
    return dict(O01_inventory_positive=1,O01_actions_admitted=6,O01_fields_bound=78,native_type_checks=6,native_whole_model_admission='NOT_ESTABLISHED',positive_role_bindings=len(bound),negative_definition_cases=negatives,negative_role_cases=role_negatives,canonical_definition_inventory_sha256=identity,selection_execution_invariant='PASS',whole_E2_case_execution=False,experiment_actions_executed=0)
if __name__=='__main__':
    print(json.dumps(qualify(),sort_keys=True))
