"""Offline R06 definition qualification. No installation or Action execution."""
import hashlib, json
from pathlib import Path
from dataclasses import replace, fields
from adapter.planner import codec as c, model as m, gates
from adapter.planner.action_materializer import materialize_action

R = Path(__file__).resolve().parents[2]
D = R / 'docs/plans'
O = D / 'qualification/REENTRY_R06_1'
P = 'DETERMINISTIC_PLANNER_V0_1_'

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write(name, value):
    O.mkdir(parents=True, exist_ok=True)
    (O / name).write_bytes(c.canonical_bytes(value))

def main():
    protected = {str(p.relative_to(R)): digest(p) for root in (R/'adapter/planner', D)
                 for p in root.rglob('*') if p.is_file() and O not in p.parents
                 and 'REENTRY_R06' not in p.name and '__pycache__' not in p.parts}
    path = D / (P+'E2_P04_POST_A10_INSTALL_BUNDLE_1.json')
    bid = m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, 'planner-bundle-v1',
        '1b69d962865c23fa43b3ec362af096e39d72bbfc4dee2252d1e0d4914d487054')
    b = c.restore(path, bid, R)
    old = next(a for a in b.current.actions if a.id.value == 'E2-REENTER')
    assert old.accepted_inventory == ()
    source = D/(P+'E2_PC01_SOURCES.json')
    declaration = next(x for x in json.loads(source.read_text())['declarations'] if x['id']=='E2-REENTER')
    assert declaration['output'] == {'id':'E2-K-REENTER', 'type':'KnowledgeRecord',
        'statement':'Bounded reentry mapping produced', 'producer':'E2-REENTER', 'outcome':'PASS'}
    new = materialize_action(old, declaration)
    changed = [f.name for f in fields(old) if getattr(old,f.name)!=getattr(new,f.name)]
    assert changed == ['accepted_inventory', 'pass_model_complete']
    candidate_model = replace(b.current, actions=tuple(new if a.id==old.id else a for a in b.current.actions))
    m.validate_model(candidate_model)
    # These are result-gate test operands, never executor results or admitted instances.
    operand = m.SuppliedResult(new.id, m.ActionResult.PASS, new.accepted_inventory,
                               c.snapshot_id(candidate_model))
    gates.validate_result(new, operand)
    negative = []
    def reject(name, operation):
        try: operation()
        except (m.PlannerError, ValueError) as e:
            negative.append({'name':name,'result':'PASS','native_reason':str(e)})
        else: raise AssertionError(name)
    k = new.accepted_inventory[0]
    reject('wrong outcome',lambda:gates.validate_result(new,replace(operand,result=m.ActionResult.FAIL)))
    reject('missing output',lambda:gates.validate_result(new,replace(operand,knowledge=())))
    reject('extra output',lambda:gates.validate_result(new,replace(operand,knowledge=(k,replace(k,id=m.KnowledgeId('EXTRA'))))))
    reject('wrong knowledge',lambda:gates.validate_result(new,replace(operand,knowledge=(replace(k,id=m.KnowledgeId('WRONG')),))))
    reject('wrong Action',lambda:gates.validate_result(new,replace(operand,action=m.ActionId('E2-FINISH'))))
    reject('wrong output scope',lambda:gates.validate_result(new,replace(operand,knowledge=(replace(k,provenance=replace(k.provenance,scope='FOREIGN')),))))
    reject('wrong output provenance/lineage source',lambda:gates.validate_result(new,replace(operand,knowledge=(replace(k,provenance=replace(k.provenance,excerpt='foreign lineage')),))))
    reject('prospective Action definition substituted for result',lambda:gates.validate_result(new,new))
    reject('wrong declaration producer',lambda:materialize_action(old,dict(declaration,output=dict(declaration['output'],producer='E2-FINISH'))))
    reject('wrong declaration outcome',lambda:materialize_action(old,dict(declaration,output=dict(declaration['output'],outcome='FAIL'))))
    write('canonical-action-before.json',c._wire(old))
    write('prospective-action-definition.json',c._wire(new))
    write('authoritative-source-declaration.json',declaration)
    decision = {'selected_option':'NONE','options':['AUTHORIZE_P04_A12_REENTER_RESULT_INSTALLATION','DECLINE_P04_A12_REENTER_RESULT_INSTALLATION'],
        'subject':'Replace only E2-REENTER accepted-result definition; implement and qualify required generic Action definition adapter before application',
        'authority_class':'INSTALL','operation':'REPLACE','issuer_required':'authenticated human qualification/configuration authority',
        'context':c._wire(b.current.context),'consumer':'O01/model.Action/gates.validate_result/core.apply_result',
        'expected_bundle':c._wire(bid),'expected_state':c._wire(c.snapshot_id(b.current)),
        'expected_parent':c._wire(b.events[-1].identity),'source_declaration_sha256':digest(source),
        'old_body':{'domain':'canonical native Action wire bytes/raw-file-sha256','sha256':digest(O/'canonical-action-before.json')},
        'replacement_body':{'domain':'canonical native Action wire bytes/raw-file-sha256','sha256':digest(O/'prospective-action-definition.json')},
        'allowed_frame_change':['accepted_inventory','pass_model_complete'],'generation':b.current.context.generation,
        'validity':'exact pinned prefix; context tick within 0..100; one semantic replacement; invalidated source/authority fails closed',
        'authorize_consequence':'Permit only this prospective definition replacement after generic adapter qualification. Advance canonical installation event/head, preserve history, rematerialize candidates. Does not permit A09-A12 execution.',
        'decline_consequence':'No change; A12_READY and P04_EXECUTION_READY remain NO.',
        'exclusions':['Action execution','ActionResult creation','Action completion','new operating authority','route/authentication/A10 changes','other Actions','N-REAL','P03 scope changes']}
    write('bounded-installation-decision.json',decision)
    preserved = all(digest(R/p)==h for p,h in protected.items())
    assert preserved
    evidence = {'bundle_trust':'PASS','canonical_bundle':c._wire(bid),'canonical_state':c._wire(c.snapshot_id(b.current)),
        'canonical_append_head':c._wire(b.events[-1].identity),'Action_before':c._wire(old),
        'Action_prospective':c._wire(new),'source_declaration':declaration,'source_path':str(source.relative_to(R)),
        'source_sha256':digest(source),'frame_changed':changed,'model_admission':'PASS',
        'result_gate_positive':'PASS: non-live typed operand; no execution/result admission',
        'negatives':negative,'native_scope_lineage_limitation':'SuppliedResult has no standalone scope/lineage fields. Output provenance is compared exactly; execution additionally pins expected snapshot. No invented fields or direct lineage rejection claim.',
        'protected_artifacts_unchanged':preserved,'protected_file_count':len(protected),
        'execution':'NOT_RUN: missing bounded installation grant and Action installation adapter; stop decision-ready',
        'canonical_action_inventory_after':[],'decision':decision}
    write('qualification-evidence.json',evidence)
    print(json.dumps({'model':'PASS','result_gate':'PASS','negatives':len(negative),'preservation':preserved,'execution':'NOT_RUN'}))

if __name__ == '__main__': main()
