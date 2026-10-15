"""Reproducible E06 application; never supplies a FINISH execution result."""
from dataclasses import replace
import json
import os
from pathlib import Path
import subprocess
import sys
from adapter.planner import codec as c, model as m, typed_proofs as t
from adapter.planner.core import apply_event, recompute, evaluate_satisfaction
from adapter.tests.test_planner_typed_proofs import ZERO, candidate

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / 'docs/plans'
PREFIX = 'DETERMINISTIC_PLANNER_V0_1_EVIDENCE_E06'


def write(name, raw):
    # Reuse native immutable publication; output cannot replace earlier evidence.
    return c._write_immutable(D, name, raw)


def cold(path, expected):
    script = """import json,os,sys
from dataclasses import fields,is_dataclass
from enum import Enum
from pathlib import Path
from adapter.planner import codec as c,model as m
from adapter.planner.core import recompute
s=c.decode_snapshot(Path(sys.argv[1]).read_bytes());r=recompute(s)
for contract in s.proof_contracts:
 c.load_pinned(Path.cwd(),m.ArtifactPin(contract.provenance.path,contract.provenance.identity,m.HashProfile.RAW))
def wire(x):
 if isinstance(x,Enum):return {'type':type(x).__name__,'value':x.value}
 if is_dataclass(x):return {'type':type(x).__name__,**{f.name:wire(getattr(x,f.name)) for f in fields(x)}}
 if isinstance(x,tuple):return [wire(y) for y in x]
 return x
print(json.dumps({'pid':os.getpid(),'snapshot':c.snapshot_id(s).sha256,'computation':wire(r)}))
"""
    results = []
    for seed in (0, 1, 7, 101):
        for _ in range(3):
            env = dict(os.environ, PYTHONHASHSEED=str(seed), PYTHONDONTWRITEBYTECODE='1')
            output = subprocess.check_output([sys.executable, '-c', script, str(path)], cwd=ROOT, env=env, text=True)
            result = json.loads(output)
            assert result['snapshot'] == expected.sha256
            results.append(dict(result, seed=seed, exit_status=0, inputs=[str(path), 'native runtime modules', 'proof contract provenance pins (where present)']))
    assert all(x['computation'] == results[0]['computation'] for x in results)
    return results


def main():
    authority = json.loads((D/'DETERMINISTIC_PLANNER_V0_1_E2_PC02_A_ROOT_SLOT_FIXTURE_RESULT.json').read_text())
    dossier = json.loads((D/'DETERMINISTIC_PLANNER_V0_1_E2_PC02_ROOT_SLOT_FIXTURE_AUTHORITY_1.json').read_text())
    assert authority['authority_issued'] and authority['authorization_authentication']['decision'] == 'PASS'
    assert authority['fixture_authority_applicability'] == 'PASS'
    original = c.decode_snapshot((D/'DETERMINISTIC_PLANNER_V0_1_E2_P03_E05_TARGET_SNAPSHOT.json').read_bytes())
    knowledge = next(k for k in original.knowledge if k.id == m.KnowledgeId('E2-K-REENTER'))
    assert knowledge.validation is m.ValidationState.ACCEPTED and knowledge.outcome is m.ActionResult.PASS
    assert any(s.id == m.ActionId('E2-REENTER') and s.state is m.ActionState.COMPLETED for s in original.statuses)
    assert m.ActionId('E2-FINISH') not in recompute(original).actionable
    ctx = original.context
    path = 'docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_PC02_A_ROOT_SLOT_FIXTURE_RESULT.json'
    pin = c._identity((ROOT/path).read_bytes(), 'raw-file-sha256')
    provenance = m.Provenance(path, pin, '/fixture_authority_id', authority['fixture_authority_id'], 'AUTHENTICATED_QUALIFICATION_FIXTURE', ctx.scope)
    entity = m.GraphEntity(m.EntityId(authority['fixture_authority_id']), m.EntityKind.AUTHORITY, pin, provenance, ctx.scope, ctx.lineage, ctx.generation, 100, permissions=(m.AuthorityClass.DECIDE,))
    # Authorized fixture definitions and Action prerequisites; statuses are retained.
    slot_id, root_id = m.SlotId(dossier['e2_slot_contract']['slot_id']), m.ConditionId(dossier['e2_root_contract']['root_id'])
    actions = tuple(replace(a, prerequisites=a.prerequisites + (m.Gate(m.GateKind.CONDITION_SATISFIED, root_id),), blocked_terminal=False) if a.id == m.ActionId('E2-FINISH') else a for a in original.actions)
    # Existing explicit ordering graphs must represent the additional authored gate.
    assertions = original.assertions
    if any(a.relation is m.Relation.REQUIRES for a in assertions):
        assertions += (m.GraphAssertion(m.AssertionId('E06-finish-root-binding'), provenance, relation=m.Relation.REQUIRES, subject=m.ActionId('E2-FINISH'), object=root_id, ordering_justification='Authorized independent root prerequisite'),)
    start = replace(original, actions=actions, assertions=assertions, slots=(m.ValueSlot(slot_id, m.SlotState.UNRESOLVED, m.ValueType.NON_IDENTITY_VALUE),), entities=original.entities + (entity,))
    sc = m.TypedProofContract(ZERO, m.TypedProofKind.SLOT_PROOF, dossier['slot_proof_contract']['proposition'], slot_id, (knowledge.id,), (t.support_identity(start, knowledge.id),), ctx.scope, ctx.lineage, ctx.generation, 100, entity.id, entity.identity, provenance)
    sc = replace(sc, id=t.identity(sc)); start = replace(start, proof_contracts=(sc,))
    sp = candidate(sc)
    preview = apply_event(start, m.TypedProofAdmission(sp, c.snapshot_id(start))).snapshot
    rc = replace(sc, proof_type=m.TypedProofKind.ROOT_PROOF, proposition=dossier['root_proof_contract']['proposition'], target=root_id, supports=(slot_id,), support_identities=(t.support_identity(preview, slot_id),))
    rc = replace(rc, id=t.identity(rc)); start = replace(start, proof_contracts=(sc, rc))
    assert start.statuses == original.statuses
    # Independent oracle binds to authoritative dossier, rather than derived labels.
    assert sp.proof_type is m.TypedProofKind.SLOT_PROOF and sp.target.value == dossier['slot_proof_contract']['target_slot']
    assert sp.supports == (m.KnowledgeId(dossier['slot_proof_contract']['knowledge_input']),)
    assert knowledge.statement == 'Bounded reentry mapping produced' and knowledge.producer == m.ActionId('E2-REENTER')
    assert (sp.scope, sp.lineage) == (dossier['authority_record']['scope'], dossier['authority_record']['lineage'])
    slot_event = m.TypedProofAdmission(sp, c.snapshot_id(start))
    slot = apply_event(start, slot_event).snapshot
    assert slot.slots[0].state is m.SlotState.RESOLVED
    assert slot.roots[0].state is not m.ConditionState.SATISFIED
    assert m.ActionId('E2-FINISH') not in recompute(slot).actionable
    slot_path = write(PREFIX+'_SLOT_BOUNDARY_SNAPSHOT.json', c.snapshot_bytes(slot)+b'\n')
    slot_cold = cold(slot_path, c.snapshot_id(slot))
    rp = candidate(rc)
    assert rp.proof_type is m.TypedProofKind.ROOT_PROOF and rp.target.value == dossier['root_proof_contract']['target_root']
    assert rp.proposition == dossier['root_proof_contract']['proposition'] and rp.id != sp.id
    assert rp.supports == (slot_id,) and rp.support_identities == (t.support_identity(slot, slot_id),)
    root_event = m.TypedProofAdmission(rp, c.snapshot_id(slot))
    target = apply_event(c.decode_snapshot(slot_path.read_bytes()), root_event).snapshot
    assert target.roots[0].state is m.ConditionState.SATISFIED
    assert m.ActionId('E2-FINISH') in recompute(target).actionable
    assert any(s.id == m.ActionId('E2-FINISH') and s.state is m.ActionState.ACTIONABLE for s in target.statuses)
    assert not any(k.producer == m.ActionId('E2-FINISH') for k in target.knowledge)
    target_path = write(PREFIX+'_P03_TARGET_SNAPSHOT.json', c.snapshot_bytes(target)+b'\n')
    target_cold = cold(target_path, c.snapshot_id(target))
    # Native causal event records; replay starts at the explicitly identified
    # reconstructed E06 boundary, preserving earlier history as E05 input.
    events = []; state = start; parent_event = None
    for index, command in enumerate((slot_event, root_event), 1):
        after = apply_event(state, command).snapshot
        parent, aid = c.snapshot_id(state), c.snapshot_id(after)
        event = m.ExecutionEvent(index, parent, parent_event, command, aid, c._event_identity(index, parent, parent_event, command, aid))
        events.append(event); state = after; parent_event = event.identity
    assert c.snapshot_id(state) == c.snapshot_id(target)
    journal = {'schema':'E06-NATIVE-EVENT-QUALIFICATION-1', 'historical_input':c._wire(c.snapshot_id(original)), 'initial':c._wire(start), 'events':[c._wire(x) for x in events], 'target':c._wire(c.snapshot_id(target)), 'history_boundary':'E05 historical lifecycle retained in its original artifacts; E06 journal starts at authorized definition materialization'}
    write(PREFIX+'_EVENT_REPLAY.json', c.canonical_bytes(journal)+b'\n')
    replay = c.decode_snapshot(c.snapshot_bytes(start))
    for event in events:
        assert event.parent_snapshot == c.snapshot_id(replay)
        replay = apply_event(replay, event.result).snapshot
        assert event.after_snapshot == c.snapshot_id(replay)
    assert c.snapshot_id(replay) == c.snapshot_id(target)
    replay_script = """import json,os,sys
from pathlib import Path
from adapter.planner import codec as c
from adapter.planner.core import apply_event,recompute
j=json.loads(Path(sys.argv[1]).read_text());state=c._unwire(j['initial']);parent=None
for raw in j['events']:
 e=c._unwire(raw)
 assert e.parent_snapshot==c.snapshot_id(state) and e.parent_event==parent
 assert e.identity==c._event_identity(e.sequence,e.parent_snapshot,parent,e.result,e.after_snapshot)
 state=apply_event(state,e.result).snapshot
 assert c.snapshot_id(state)==e.after_snapshot
 parent=e.identity
assert c.snapshot_id(state)==c._unwire(j['target'])
print(json.dumps({'pid':os.getpid(),'snapshot':c.snapshot_id(state).sha256,'actionable':[a.value for a in recompute(state).actionable]}))
"""
    journal_path = D/(PREFIX+'_EVENT_REPLAY.json')
    replay_cold = []
    for seed in (0,1,7,101):
        for _ in range(3):
            env = dict(os.environ, PYTHONHASHSEED=str(seed), PYTHONDONTWRITEBYTECODE='1')
            result = json.loads(subprocess.check_output([sys.executable,'-c',replay_script,str(journal_path)],cwd=ROOT,env=env,text=True))
            assert result['snapshot']==c.snapshot_id(target).sha256 and result['actionable']==['E2-FINISH']
            replay_cold.append(dict(result,seed=seed,exit_status=0))
    invalidation = apply_event(c.decode_snapshot(target_path.read_bytes()), m.ProofDependencyChange((knowledge.id,), c.snapshot_id(target), provenance)).snapshot
    assert invalidation.slots[0].state is m.SlotState.UNRESOLVED and invalidation.roots[0].state is m.ConditionState.UNRESOLVED
    assert m.ActionId('E2-FINISH') not in recompute(invalidation).actionable
    write(PREFIX+'_INVALIDATION_SNAPSHOT.json', c.snapshot_bytes(invalidation)+b'\n')
    # Original P03 includes a separately governed-unknown checkpoint, not just
    # the now-achieved post-reentry root/readiness target.
    governed = c.decode_snapshot((D/'DETERMINISTIC_PLANNER_V0_1_E2_P03_GATE_QUALIFIED_SNAPSHOT.json').read_bytes())
    gc = recompute(governed)
    assert all(not r.rule_known for r in governed.evidence_requirements)
    assert not gc.actionable and not governed.receipt_observations
    route_changed = governed.external_gates[0].resolution_contracts[0].provenance.identity
    route_invalid = apply_event(c.decode_snapshot(c.snapshot_bytes(governed)), m.SourceInvalidation((route_changed,), c.snapshot_id(governed))).snapshot
    assert recompute(route_invalid).control is m.ControlState.PLAN_DEFECT
    governed_path = write(PREFIX+'_GOVERNED_UNKNOWN_SNAPSHOT.json', c.snapshot_bytes(governed)+b'\n')
    governed_cold = cold(governed_path, c.snapshot_id(governed))
    terms = {'E2_K_REENTER_CURRENT':True, 'E2_REENTER_COMPLETED':True, 'SLOT_PROOF_ACCEPTED':True, 'SLOT_SATISFIED':True, 'INDEPENDENT_ROOT_PROOF_ACCEPTED':True, 'ROOT_SATISFIED':True, 'FINISH_ACTIONABLE_UNEXECUTED':True, 'TARGET_COLD_RESTORE_FULL_SNAPSHOT_EQUALITY':True, 'TARGET_REPLAY':True, 'TARGET_DETERMINISM':True, 'GOVERNED_UNKNOWN_EXTERNAL_WAIT':gc.control is m.ControlState.EXTERNAL_WAIT, 'POST_RELOAD_INVALIDATION':True, 'GOVERNED_UNKNOWN_ROUTE_INVALIDATION_PLAN_DEFECT':True, 'ORIGINAL_CHECKPOINT_PINNED_BUNDLE_FULL_EQUALITY':False}
    # E05 supplied a Snapshot, not a replayable, source-pinned full bundle.
    # Do not upgrade that historical evidence into a fabricated bundle claim.
    result = {'work_package':'EVIDENCE-E06', 'result':'PARTIAL', 'typed_slot_proof_capability':'PASS', 'typed_root_proof_capability':'PASS', 'proof_persistence':'PASS_NATIVE_SNAPSHOT_AND_GENERIC_BUNDLE_TEST', 'proof_replay':'PASS_NATIVE_TRANSITIONS', 'proof_invalidation':'PASS', 'blocked_action_semantics':'Legacy/default BLOCKED terminal hold; blocked_terminal=False permits prerequisite reevaluation; terminal_failure and WAITING/SELECTED/COMPLETED remain held', 'reevaluation_capability':'PASS', 'reevaluation_triggers':['proof admitted','proof invalidated','knowledge invalidated','slot changed','root changed','authority invalidated','source/contract/provenance invalidated'], 'generic_positive_lifecycle':'PASS', 'invalid_transitions':'PASS', 'atomicity':'PASS_PURE_VALIDATION_THEN_NATIVE_COMMIT', 'idempotence':'PASS', 'regressions':'PENDING', 'e2_slot_proof_id':sp.id.sha256, 'e2_slot_proof_admission':'PASS', 'e2_slot_state':'SATISFIED (native RESOLVED)', 'e2_root_proof_id':rp.id.sha256, 'e2_root_proof_admission':'PASS', 'e2_root_state':'SATISFIED', 'e2_reenter_completed':True, 'e2_finish_before_root':'NON_ACTIONABLE', 'e2_finish_after_root':'ACTIONABLE', 'e2_finish_executed':False, 'p03_exit_predicate':all(terms.values()), 'p03_exit_terms':terms, 'e2_p03_result':'PARTIAL', 'e2_p04_ready':False, 'next_package':'P03 original external checkpoint pinned-bundle cold-restore equality reconciliation', 'persistence':'PASS', 'cold_restore':'PASS_48_FRESH_INTERPRETERS', 'replay':'PASS_E06_BOUNDARY_NATIVE_EVENTS', 'determinism':'PASS_SEEDS_0_1_7_101', 'full_suite_status':'PENDING', 'e1_artifacts_modified':0, 'production_effect':False, 'fixture_definition_boundary':{'input':c.snapshot_id(original).sha256,'materialized':c.snapshot_id(start).sha256,'action_statuses_unchanged':True,'source':'PC02-A authenticated fixture admission'}, 'slot_oracle':'PASS', 'root_oracle':'PASS', 'slot_proof':c._wire(sp), 'root_proof':c._wire(rp), 'reevaluations':[c._wire(x) for x in target.reevaluations], 'invalidation':{'slot':invalidation.slots[0].state.value,'root':invalidation.roots[0].state.value,'actionable':[a.value for a in recompute(invalidation).actionable]}, 'cold_restore_runs':{'slot':slot_cold,'target':target_cold,'governed_unknown':governed_cold,'event_replay':replay_cold}}
    # This report is regenerated after regression evidence is attached.
    (D/(PREFIX+'_ROOT_SLOT_REEVALUATION_RESULT.json')).write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k in ('result','e2_finish_after_root','e2_p03_result','p03_exit_terms')}, indent=2))

if __name__ == '__main__': main()
