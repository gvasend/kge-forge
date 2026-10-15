"""Report PC01's qualified documentary binding and the next interface frontier."""
import hashlib
import json
import subprocess
from binding import ROOT, OUT, DOCS, P, CLOSURE, BASE_ID, ACCEPTANCE_ID, read, ref, save


def main():
    projection=read(OUT/'END-projection.json');manifest=read(OUT/'invocation-input-manifest.json')
    pre=read(OUT/'preflight.json');negative=read(OUT/'negative-results.json');det=read(OUT/'determinism.json')
    support=read(OUT/'currentness-provenance-policy.json');frontier=read(OUT/'six-interface-frontier.json')
    assert pre['PC01_END_INTERFACE']==support['RESULT']==negative['RESULT']==det['RESULT']=='PASS'
    baseline=read(OUT/'baseline.json')['files']
    changed=[p for p,h in baseline.items() if not (ROOT/p).is_file() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
    assert not changed,changed
    check=subprocess.run(['git','diff','--check'],cwd=str(ROOT),capture_output=True,text=True)
    assert check.returncode==0,check.stdout+check.stderr
    save('preservation.json',{'RESULT':'PASS','baseline_files_unchanged':len(baseline),'changed_prior_files':[],
        'native_Snapshot_bundle_event_source_policy_authority_bytes_unchanged':True,
        'closed_13_stage_bindings_four_bridges_N12_N13_unchanged':True,
        'NATIVE_STATE_CHANGED':'NO','INSTALL_EVENTS':0,'NEW_AUTHORITIES':0,'RUNTIME_MODIFIED':'NO',
        'P05_EXECUTED':'NO','P06_EXECUTED':'NO','N_REAL_SATISFIED':'NO','E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO',
        'runtime_files_unchanged':sum(p.startswith('adapter/planner/') for p in baseline),
        'frozen_E1_files_unchanged':sum(p.startswith('docs/experiments/E1/') for p in baseline),'git_diff_check':'PASS'})
    evidence={k:ref(OUT/v) for k,v in {
        'sources':'source-pins.json','inventory':'six-Action-inventory.json','projection':'END-projection.json',
        'manifest':'invocation-input-manifest.json','process_binding':'process-binding.json','independent_oracle':'expected-oracle.json',
        'manifest_oracle':'expected-manifest-oracle.json','preflight':'preflight.json','currentness':'currentness-provenance-policy.json',
        'negative_plan':'negative-plan.json','negatives':'negative-results.json','determinism':'determinism.json',
        'frontier':'six-interface-frontier.json','preservation':'preservation.json'}.items()}
    result={'WORK_PACKAGE':'E2-P05-PC01-END-BINDING','RESULT':'PASS','PC01_RESULT':'PASS',
        'PC01_SOURCE':projection['projection']['PC01_definition'],'PC01_QUALIFICATION':projection['projection']['PC01_qualification'],
        'SIX_ACTION_SNAPSHOT':[{k:v for k,v in model.items() if k!='actions'} for model in projection['projection']['models']],
        'SIX_ACTIONS':projection['projection']['action_ids'],'END_CONSUMER':projection['projection']['consumer'],
        'END_PROCESS':projection['projection']['process_identity'],'END_PROJECTION':evidence['projection'],
        'PROJECTION_IDENTITY':projection['identity'],'INVOCATION_INPUT_MANIFEST':evidence['manifest'],
        'MANIFEST_IDENTITY':manifest['identity'],'CURRENTNESS':'PASS; historical model roles retained, current native definition support and policy/source pins verified',
        'SCOPE':'PASS; exact E2-QUALIFICATION-ONLY acceptance scope','LINEAGE':'PASS; original baseline and canonical P04 contexts remain separate',
        'PROVENANCE':'PASS; exact native model/Action selectors, provenance content and current physical pins; old temporary paths not used as current sources',
        'NATIVE_MODEL_PREFLIGHT':'PASS for both retained native source models','END_INTERFACE_PREFLIGHT':pre['terms'],
        'NEGATIVE_SUITE':'PASS; 18/18 fixed isolated controls','DETERMINISM':'PASS; 36 fresh readers, seeds 0,1,7,101 and original/reversed/rotated Action presentations',
        'PC01_END_INTERFACE':'PASS','END_INTERFACES_BOUND':1,'END_INTERFACE_COUNT':6,
        'NEXT_UNRESOLVED_INTERFACE':frontier['NEXT_UNRESOLVED_INTERFACE'],
        'remaining_five_interfaces_unchanged':True,'P05_STAGE_BINDINGS':'13/13','FOUR_SEMANTIC_BRIDGES':'PASS',
        'AGGREGATE_N12':'PASS','AGGREGATE_N13':'PASS','COMPOSITE_P05_END_QUALIFICATION':'FAIL','P05_EXECUTION_READY':'NO',
        'NATIVE_STATE_CHANGED':'NO','INSTALL_EVENTS':0,'NEW_AUTHORITIES':0,'P05_EXECUTED':'NO','P06_EXECUTED':'NO',
        'N_REAL_SATISFIED':'NO','ORIGINAL_A03_HISTORICAL_OCCURRENCE':'UNPROVEN','ORIGINAL_A04_HISTORICAL_ANCESTRY':'UNPROVEN',
        'ORIGINAL_A05_HISTORICAL_ANCESTRY':'UNPROVEN','ORIGINAL_A06_HISTORICAL_REQUEST_WAIT_TRACE':'UNPROVEN',
        'P03_HISTORICAL_CORRESPONDENCE':'UNPROVEN','CONTINUOUS_ORIGINAL_A01_A13_LINEAGE_PROVEN':'NO',
        'RUNTIME_MODIFIED':'NO','E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO','GIT_DIFF_CHECK':'PASS',
        'NEXT_PACKAGE':'E2-P05 PC02 -> END CURRENT INTERFACE / PROCESS BINDING CLOSURE',
        'evidence':evidence,'verification':{'path':str((OUT/'verification.json').relative_to(ROOT))}}
    output=DOCS/(P+'E2_P05_PC01_END_BINDING_1.json')
    raw=(json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode()
    if output.exists():assert output.read_bytes()==raw
    else:output.write_bytes(raw)
    text=f'''# E2-P05 PC01 → END qualification binding materialization 1

**RESULT = PASS. PC01_END_INTERFACE = PASS.** The exact retained PC01 source/qualified models are bound to END dependency 0 by a documentary six-Action projection and concrete invocation/input manifest. All independent interface terms, native structural models, definition currentness, source/policy/provenance checks, eighteen negative controls and thirty-six fresh reader comparisons pass. **END_INTERFACES_BOUND = 1/6**; the next unresolved interface is **E2-PC02 → E2-END**. P05 remains not ready and unexecuted.

The [machine companion](DETERMINISTIC_PLANNER_V0_1_E2_P05_PC01_END_BINDING_1.json) links the [source pins](qualification/E2_P05_PC01_END_BINDING_1/source-pins.json), [full six-Action inventory](qualification/E2_P05_PC01_END_BINDING_1/six-Action-inventory.json), [projection](qualification/E2_P05_PC01_END_BINDING_1/END-projection.json), [input manifest](qualification/E2_P05_PC01_END_BINDING_1/invocation-input-manifest.json), [process binding](qualification/E2_P05_PC01_END_BINDING_1/process-binding.json), independent oracles and all verification evidence.

## Exact source and consumer roles

PC01 original preparation-scope PASS is pinned through its [exit reconciliation](DETERMINISTIC_PLANNER_V0_1_E2_PC01_EXIT_RECONCILIATION_1.json), complete six-Action [definition source](DETERMINISTIC_PLANNER_V0_1_E2_PC01_SOURCES.json) and the two native source views already identified by [interface closure](DETERMINISTIC_PLANNER_V0_1_E2_P05_END_INTERFACE_CLOSURE_1.md). PC01's producer and historical temporary-fixture constructor were not rerun.

| Model role | Exact retained native Snapshot | Context / observed Action states |
|---|---|---|
| Original qualified definition/model view | planner-snapshot-v1:545ad19184d8dd7dfb5b2737e081b043d13982f05d05326939ac2cbb89bf54e2 | E2-CANONICAL-BASELINE-1 / E2-GENERATION-1; six ACTION_ELIGIBLE statuses |
| Current canonical P04 definition/model view | planner-snapshot-v1:046fdc270a0060503729151368a68672f76af122830b86e65d372e6bc5d7dea4 | E2-P03-PROSPECTIVE-QUALIFICATION-1 / E2-P03-PROSPECTIVE-GENERATION-1; six existing COMPLETED statuses |

Both use E2-QUALIFICATION-ONLY. The inventory preserves every native Action field, exact prerequisite/result/output/accepted-inventory declaration, source and context for **E2-CHECK, E2-COLLECT, E2-DECIDE, E2-FINISH, E2-PREPARE and E2-REENTER**. Both native models have exactly that set and the declaration's operation/effect classes. Source/context/definition version differences remain explicit; no Action is added, removed, rewritten or retagged.

Accepted inventory objects remain prospective result declarations, not new actual Knowledge/results. Existing P04 completion states are observed source facts, not newly manufactured execution evidence. The projection introduces no native Snapshot, Action definition, event, permission or proof.

The exact consumer is **E2-END#/dependencies/0**, edge `qualification-END-edge-v1:c6367fb06db561c4c881ff2d0209b6ee02f26017ea9d05aee3f7d3b3fdfb75e4`, under the unchanged composite graph `{BASE_ID}` and qualified scope mapping `{ACCEPTANCE_ID}`. Its [recovered contract](qualification/E2_P05_END_INTERFACE_CLOSURE_1/END-PC01-consumer-contract.json) requires a current source/model projection and concrete process/input binding; historical READY or source presence alone is insufficient.

## Projection and concrete invocation manifest

```text
PROJECTION_IDENTITY = {projection['identity']}
MANIFEST_IDENTITY = {manifest['identity']}
PROCESS_IDENTITY = {projection['projection']['process_identity']}
```

These are deterministic **qualification comparison identities**, not native Snapshot/Event/Action/Authority identities. They bind exact definition/qualification/source Snapshot and six Action views, consumer/edge, process code/contracts, scope/context and provenance. Action collections normalize under native codec SET_FIELDS semantics and stable ActionId order; causal event history is not permuted.

The manifest contains twelve exact input terms: PC01 definition and qualification, original and current native models, END consumer, process contract, existing scope capture, composite graph, qualified acceptance mapping, governed definition history, supported policy and the independent comparison oracle. Every term records its expected type, source selector/hash/semantics, projection and consumer/process identity, scope/lineage/provenance/currentness role. The oracle is marked **COMPARISON_ONLY**, never a Planner operand.

Process edges are explicit: **PC01 sources → exact model projection → invocation/input manifest → END dependency 0**. The read-only program/interpreter/native primitive content pins, materialization/preflight invocations, bounded environment and all thirty-six seed/reader/presentation invocations are concrete. No process argument or input is selected after observing results. The manifest is retained qualification evidence; no native PersistenceBundle is created for this mapping.

## Independent preflight and currentness

The [binding oracle](qualification/E2_P05_PC01_END_BINDING_1/expected-oracle.json) and [manifest oracle](qualification/E2_P05_PC01_END_BINDING_1/expected-manifest-oracle.json) were sealed **before** projection materialization/preflight. Expected values came from authoritative retained JSON, PC01 declarations and the END consumer/process contract, not materializer output. The independent oracle never called the materializer, inventory extractor or native state transition.

[Preflight](qualification/E2_P05_PC01_END_BINDING_1/preflight.json) compares the complete projection and manifest to those fixed expected inputs, then uses unchanged native `validate_model`/type/identity and definition-currentness primitives on the retained models. Both full native structural models pass. SOURCE, CONSUMER, PROJECTION, PROCESS, INPUT_MANIFEST, CURRENTNESS, SCOPE, LINEAGE and PROVENANCE each pass independently. Native model bytes remain exact after inspection.

[Support checks](qualification/E2_P05_PC01_END_BINDING_1/currentness-provenance-policy.json) verify the twelve retained Action provenance bodies by content hash, the current P04 physical source/policy pins and supported policy version. Old original-fixture temporary paths are not promoted to current filesystem sources; their historical provenance is retained inside the pinned original Snapshot. The original model is consumed at its qualified historical definition role, while current P04 native source support is verified physically.

Existing governed Action replacements are traced without applying them: **E2-REENTER at native sequence 7** and **E2-FINISH at 9**. Exact installed definition/content/authority/event references and new Action bytes match the current canonical model. Currentness uses native `action_current`, independent of the fact that those Actions are completed. There is no new installation, grant, lifecycle result, manual completion or source reactivation.

## Negatives, fresh readers and frontier

All **18/18** [fixed negatives](qualification/E2_P05_PC01_END_BINDING_1/negative-results.json) reject: wrong Snapshot/qualification, five/seven Actions, wrong/foreign Action, wrong consumer/process, missing/extra input, wrong source/projection identity, wrong scope/lineage/provenance, stale pin, an order-sensitive forged identity and report-only source substitution. Mutated candidates can be rehashed; they still fail the independently trusted oracle. Negative fixtures never edit retained native data.

Valid reversed/rotated native Action presentations remain equivalent. [Determinism](qualification/E2_P05_PC01_END_BINDING_1/determinism.json) reconstructs the same complete projection/manifest identities in **36 fresh processes**: seeds 0,1,7,101; three readers per seed and original/reversed/rotated presentation. Readers have no writer memory and use pinned sources/contracts and comparison-only oracles. No replay, result application or event/commit path is available.

[Six-interface frontier](qualification/E2_P05_PC01_END_BINDING_1/six-interface-frontier.json) records **PC01 PASS, 1/6 interfaces bound**, followed by **E2-PC02 proof/authority/external-lifecycle contracts → E2-END**. All five remaining records/dimensions are identical to the prior inventory. They were not repaired or reinterpreted. Composite END remains FAIL while five interfaces are open; P05_EXECUTION_READY remains NO. Thirteen stage bindings, four bridges and aggregate N12/N13 remain closed and unchanged.

Next package: **E2-P05 PC02 → END CURRENT INTERFACE / PROCESS BINDING CLOSURE**.

## Preservation

[Preservation](qualification/E2_P05_PC01_END_BINDING_1/preservation.json) and [final verification](qualification/E2_P05_PC01_END_BINDING_1/verification.json) audit every prior workspace file, source/code/contract/policy hash and report link. Only documentary PC01 binding/qualification artifacts and read-only harnesses were added. No earlier binding, native state/history, runtime or E1 file changed.

```text
WORK_PACKAGE = E2-P05-PC01-END-BINDING
RESULT = PASS
PC01_RESULT = PASS
PC01_END_INTERFACE = PASS
NEGATIVE_SUITE = PASS (18/18)
DETERMINISM = PASS (36 FRESH READERS)
END_INTERFACES_BOUND = 1
END_INTERFACE_COUNT = 6
NEXT_UNRESOLVED_INTERFACE = E2-PC02 -> E2-END
P05_STAGE_BINDINGS = 13/13
FOUR_SEMANTIC_BRIDGES = PASS
AGGREGATE_N12 = PASS
AGGREGATE_N13 = PASS
COMPOSITE_P05_END_QUALIFICATION = FAIL
P05_EXECUTION_READY = NO
NATIVE_STATE_CHANGED = NO
INSTALL_EVENTS = 0
NEW_AUTHORITIES = 0
P05_EXECUTED = NO
P06_EXECUTED = NO
ORIGINAL_A03_HISTORICAL_OCCURRENCE = UNPROVEN
ORIGINAL_A04_HISTORICAL_ANCESTRY = UNPROVEN
ORIGINAL_A05_HISTORICAL_ANCESTRY = UNPROVEN
ORIGINAL_A06_HISTORICAL_REQUEST_WAIT_TRACE = UNPROVEN
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
CONTINUOUS_ORIGINAL_A01_A13_LINEAGE_PROVEN = NO
N_REAL_SATISFIED = NO
RUNTIME_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```
'''
    md=output.with_suffix('.md')
    if md.exists():assert md.read_text()==text
    else:md.write_text(text)
    print(json.dumps({'RESULT':'PASS','PC01_END_INTERFACE':'PASS','interfaces_bound':'1/6',
        'next_interface':'E2-PC02 -> E2-END','P05_EXECUTION_READY':'NO','preserved_files':len(baseline)}))


if __name__=='__main__':main()
