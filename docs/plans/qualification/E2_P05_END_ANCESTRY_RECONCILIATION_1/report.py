"""Seal the reconciliation report without changing prior evidence or authority."""
import hashlib
import json
import re
import subprocess

from reconcile import ROOT, OUT, DOCS, PREFIX, read, ref, save

STEM = PREFIX + 'E2_P05_END_ANCESTRY_RECONCILIATION_1'


def main():
    findings = read(OUT / 'reconciliation-findings.json')
    graph = read(OUT / 'qualified-evidence-graph.json')
    dossier = read(OUT / 'aggregate-END-decision-dossier.json')
    assert dossier['selected_option'] == 'NONE'
    baseline = read(OUT / 'baseline.json')['files']
    changed = [name for name, expected in baseline.items() if not (ROOT / name).is_file() or
               hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected]
    assert not changed, changed
    check = subprocess.run(['git', 'diff', '--check'], cwd=str(ROOT), capture_output=True, text=True)
    assert check.returncode == 0, check.stdout + check.stderr
    preservation = {'RESULT': 'PASS', 'baseline_files_unchanged': len(baseline), 'changed_prior_files': [],
        'frozen_E1_files_unchanged': sum(name.startswith('docs/experiments/E1/') for name in baseline),
        'runtime_files_unchanged': sum(name.startswith('adapter/planner/') for name in baseline),
        'all_13_existing_stage_bindings_unchanged': True, 'no_native_events_instances_or_authorities_created': True,
        'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO', 'RUNTIME_MODIFIED': 'NO',
        'E1_ARTIFACTS_MODIFIED': 0, 'PRODUCTION_EFFECT': 'NO', 'git_diff_check': 'PASS'}
    save(OUT / 'preservation.json', preservation)
    evidence = {key: ref(OUT / filename) for key, filename in {
        'END_contract': 'END-ancestry-contract.json', 'original_ideal': 'original-history-ideal.json',
        'qualified_graph': 'qualified-evidence-graph.json', 'edge_classifications': 'edge-classifications.json',
        'native_segments': 'native-segment-integrity.json', 'aggregate_N12_N13': 'aggregate-N12-N13-contract.json',
        'END_oracle': 'END-qualification-oracle.json', 'scope_dossier': 'aggregate-END-decision-dossier.json',
        'determinism': 'determinism.json', 'findings': 'reconciliation-findings.json', 'preservation': 'preservation.json',
    }.items()}
    report = dict(findings, WORK_PACKAGE='E2-P05-END-ANCESTRY-RECONCILIATION', RESULT='PASS',
        result_domain='Contract recovery and exact bounded decision preparation; no aggregate END acceptance or P05 execution',
        END_ANCESTRY_CONTRACT=evidence['END_contract'], ORIGINAL_HISTORICAL_IDEAL=evidence['original_ideal'],
        ORIGINAL_UNPROVEN_TERMS=read(OUT / 'original-history-ideal.json')['unproven'],
        QUALIFIED_EVIDENCE_GRAPH=evidence['qualified_graph'], EDGE_CLASSIFICATIONS=evidence['edge_classifications'],
        AGGREGATE_N12_MAPPING='Separation assurance contract complete, structurally supported by native evidence; aggregate policy unselected; global N12 test not run',
        AGGREGATE_N13_MAPPING='Independently complete separation/provenance contract; aggregate policy unselected; global N13 test not run; full single-mainline handoff assurance is excluded',
        P04_CANONICAL_TAIL=graph['graph']['P04_canonical_tail'],
        PASS_CLAIM=read(OUT / 'END-qualification-oracle.json')['PASS_CLAIM'],
        PASS_CLAIM_domain='Conditional future PASS_UNDER_COMPOSITE_END_SCOPE only after explicit policy authentication and qualification; not the unchanged native mainline END verdict',
        EXCLUDED_CLAIMS=read(OUT / 'END-qualification-oracle.json')['excluded_claims'] +
            ['A continuous new prospective native A01-A13 mainline has been executed'],
        AGGREGATE_END_OPTIONS=dossier['options'], AGGREGATE_END_DOSSIER=evidence['scope_dossier'],
        AGGREGATE_END_DOSSIER_RAW_SHA256=evidence['scope_dossier']['raw_sha256'],
        END_QUALIFICATION_ORACLE=evidence['END_oracle'],
        CURRENT_END_ACCEPTANCE='NOT_AUTHORIZED_NOT_EXECUTED',
        QUALIFICATION_GRAPH_RECONSTRUCTION='PASS', DETERMINISM='PASS; 12 fresh readers across seeds 0,1,7,101',
        PERSISTENCE='Documentary qualification manifest; cold reconstruction from unchanged authoritative native inputs. No new Planner object or ledger',
        P03_HISTORICAL_CORRESPONDENCE='UNPROVEN', ORIGINAL_A03_HISTORICAL_OCCURRENCE='UNPROVEN',
        ORIGINAL_A04_HISTORICAL_ANCESTRY='UNPROVEN', ORIGINAL_A05_HISTORICAL_ANCESTRY='UNPROVEN',
        ORIGINAL_A06_HISTORICAL_REQUEST_WAIT_TRACE='UNPROVEN',
        NEW_NATIVE_AUTHORITY_ISSUED='NO', EXISTING_STAGE_BINDINGS_ALTERED=0,
        evidence=evidence, verification={'path': str((OUT / 'verification.json').relative_to(ROOT))})
    save(DOCS / (STEM + '.json'), report)
    text = '''# E2-P05 full END ancestry and acceptance-mapping reconciliation 1

**RESULT = PASS — RECONCILIATION AND DECISION PREPARATION ONLY.** The thirteen scoped stage bindings remain complete and unchanged. The current authorizations do not establish aggregate END acceptance. A bounded, exact composite-method proposal and two unselected qualification-scope options are sealed. **P05_EXECUTION_READY = NO.** P05/P06, native operations, authority issuance and existing binding changes did not occur.

The [machine companion](DETERMINISTIC_PLANNER_V0_1_E2_P05_END_ANCESTRY_RECONCILIATION_1.json) links the recovered contract, ideal original model, complete actual graph, every edge, aggregate N12/N13 contract, native tail, acceptance oracle, decision dossier, fresh readers and preservation evidence.

## Earliest END requirement and continuity

The [canonical plan](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.md:30) specifies a mainline from construction and initial results through preparation/decision, external wait, persistence/termination/restore, receipt, validation/reentry, actual continuation and independent proof/control recomputation. The [matrix END case](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:467), also JSON `/cases/33`, starts from independently authored canonical E2 contracts/source bytes and operates A01–A13 across real writer termination and a fresh reader, repeated under D01. Every independent stage oracle, actual post-reentry event/state, source/authority/currentness, event trace and preservation term is required. END is an **EXPERIMENT_ACCEPTANCE_CASE**, not a native Action, root, terminal permission object or ledger event.

The original sources do not prescribe recovery of the original historical event IDs, literally use “full END ancestry”, or explicitly state a one-file/one-root ledger cardinality rule. The later P05 recovery uses that phrase for the causal lifecycle/state/ledger binding needed by this mainline. **The inference is explicit:** the unamended END execution method requires a continuous native causal mainline, including exact actual-state handoffs and native parent/pre/post bindings where events occur. An independently prepared new full native reproduction can satisfy that method; the missing original historical run is not a newly imposed prerequisite.

Thus `SINGLE_NATIVE_LINEAGE_REQUIRED = YES` describes the **unamended mainline method**, not a demand for the original historical ledger identity. `ORIGINAL_HISTORICAL_LINEAGE_REQUIRED = NO`. Physical checkpoint/bundle files can differ while their native history remains continuous. A conjunction of independently successful component histories does not demonstrate that native mainline.

The [recovered contract](qualification/E2_P05_END_ANCESTRY_RECONCILIATION_1/END-ancestry-contract.json) enumerates all thirteen predecessor cases, six PC04 interfaces, required occurrence/order/state/provenance/authority relationships and continuity. The [original-history ideal](qualification/E2_P05_END_ANCESTRY_RECONCILIATION_1/original-history-ideal.json) marks each native occurrence, original boundary fidelity and predecessor connection PROVEN, UNPROVEN or NOT_REQUIRED, with no replacements substituted into that ideal. A01 definitions/A02 read-only selection and the actual canonical P04 tail are supported; missing original A03–A06 occurrences/ancestry, original P03 fidelity and the full original prefix remain UNPROVEN. Snapshots can support state values without establishing their producers or occurrence/order.

## Actual scoped graph and native segments

The [graph](qualification/E2_P05_END_ANCESTRY_RECONCILIATION_1/qualified-evidence-graph.json) records every stage's exact source artifact/pointer, native identities, real source lineage, unchanged binding classification, historical status, local END mapping, N12/N13 status, currentness/provenance and authority. It retains all thirteen original row values exactly. Its identity is **GRAPH_ID**, a qualification comparison identity distinct from native event, Snapshot, bundle, authority and ledger/root identities.

| Stage roles | Actual evidence and lineage relationship |
|---|---|
| A01/A02 | Original canonical six-Action Snapshot and read-only selection evidence; selection creates no execution event |
| A03/A04 | New prospective A03 CHECK/COLLECT events followed by the actual A04 PREPARE event; A04 extends the identical two-event prefix in E2-P05-A03-PROSPECTIVE-QUALIFICATION-1 |
| A05 | Exact retained P03 RecordedDecision event under AUTHORIZED_ALTERNATE_NATIVE_EVIDENCE; not original A05 choice/history or grant issuance |
| A06 | Separate two-event new request-ready → waiting ledger in E2-P05-A06-PROSPECTIVE-QUALIFICATION-1 |
| A07/A08 | Authorized P03 prospective checkpoint persistence/cold-fidelity evidence; original correspondence UNPROVEN |
| A09–A13 | One actual canonical P04 tail in E2-P03-PROSPECTIVE-QUALIFICATION-1, with its retained P03 prefix and governed configuration |

A03 and A04 have separate qualification roles and bundle identities but **the same physical native lineage** and exact native prefix. P03/A05 and P04 also have separate roles but an identical two-event native prefix. Those overlaps were checked from complete native fields and are retained; distinct role names are not invented lineage names. A06 is a genuinely separate native history. The graph does not concatenate ledgers or substitute matching names for exact parent/state identities.

The [edge inventory](qualification/E2_P05_END_ANCESTRY_RECONCILIATION_1/edge-classifications.json) enumerates thirteen case-to-END coverage edges, twelve lifecycle-state dependencies, all actual within-segment native event links, six interface inputs, nine configuration memberships and five local qualification-scope relations. Each edge states its exact kind, assurance, evidence, current status and conditional proposal. Native ancestry, semantic acceptance, authorized replacement and unproven relations stay separate. Membership in a native tail is not fabricated as a parent event targeting the documentary graph.

Four native handoffs remain unproven:

- A02 original selection state → new A03 start;
- new A04 PREPARE state → retained P03/A05 decision start;
- P03/A05 decision → separate A06 request/wait start;
- separate A06 post-wait → P03 A07 checkpoint.

In a composite-method amendment, those exact four relations could be **semantic qualification acceptance edges**. They would remain unproven as native producer/state/parent connections. Equal Action/Knowledge/request names, matching control values and independent local PASS flags cannot supply the missing handoffs.

## P04 tail and governed history

The [native integrity record](qualification/E2_P05_END_ANCESTRY_RECONCILIATION_1/native-segment-integrity.json) verifies canonical bundle/event bytes, closed native types, source/policy pins, event hash operands, parent/pre/post continuity and ordered membership for all retained segments. Existing cold-restore/replay qualification remains attached to its own source. This reconciliation performs no new replay or operation.

Canonical P04 remains one complete tail: entry retains nine prefix/configuration events; A09–A13 occupies native sequences **10–20**. Evidence admission/receipt, ValidationResult/support, both reentry events, actual REENTER result, deferred SLOT install/proof, deferred ROOT install/proof and FINISH result remain actual native history. Root/head and the final target are unchanged; P04 is not recast as prospective replacements.

The graph includes all nine exact governed configuration occurrences at **3,4,5,6,7,8,9,16,18**: route REPLACE, ATTEST and ingress, A10 support/validation set, REENTER definition, A13 root/slot configuration/nonterminal FINISH relationship and the two deferred proof-contract installs. Every event keeps its native parent/pre/post, authority, definition/content, operation and source. Historical occurrence is separated from terminal currentness: acquisition-route applicability ceases after reentry without erasing its legitimate historical installation or source support.

A04 retains its native D01 event/result/post-Snapshot/typed-validation binding. The six validation members remain selected by the immutable Snapshot, PredicateId and dossier identity; they are not duplicated in the event or replaced by prose. A05 retains its exact authenticated P03 choice/issuer/context and **pre-existing-grant limitation**. A06 supplies actual phase occurrence/order while producing no Evidence, validation/proof, reentry or Action completion.

## Aggregate N12/N13 and proposed acceptance

The [aggregate assurance contract](qualification/E2_P05_END_ANCESTRY_RECONCILIATION_1/aggregate-N12-N13-contract.json) recovers [N12](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:383) independently from [N13](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:397). Composition is checked term by term, beyond local PASS flags.

N12 requires definitions/selections/persistence records to stay distinct from actual execution, actual native lifecycle results and enrolled events for occurrence claims, exact within-segment ordering, no invented aggregate event, no promotion of P03 authored initial premises into historical executions, and no aggregate acceptance without its own scope decision. N13 independently requires exact actual-result/output provenance, separate definition/oracle roles, independent P04 proof/authority predicates, no foreign-lineage native substitution, no historical aliasing or grant-issuance inference, and no local mapping verdict substituted for the global P05 negative cases.

Those **negative separation assurances can be preserved by an explicitly scoped composition**. Literal full-mainline state/producer handoff assurance cannot be recovered from independent histories and is not claimed preserved. Current aggregate N12/N13 status is a complete supported preservation contract with acceptance pending; global P05 N12/N13 remain unexecuted.

The [complete proposed END oracle](qualification/E2_P05_END_ANCESTRY_RECONCILIATION_1/END-qualification-oracle.json) specifies every stage, dependency, native identity, source, historical label, scope authority, N12/N13 term, native segment, currentness and persistence/determinism obligation. A possible future PASS would claim:

> Required Planner stage behaviors and local native occurrence/ancestry assurances are qualified through the exact explicitly authorized composite evidence mappings; cross-segment links are semantic acceptance edges.

It would **not** claim a continuous original or new A01–A13 native execution, original A03/A04/A05/A06 or P03 historical recovery, cross-lineage state equality, P03 grant issuance, real external transmission, P05/P06 completion, E1 migration, N-REAL or aggregate release qualification. It would be **PASS_UNDER_COMPOSITE_END_SCOPE**, an explicitly amended acceptance method; it is not evidence that the unchanged native-mainline END operation occurred. A Snapshot/report-only alternative is not proposed.

## Bounded aggregate scope decision

The individual P03/A03/A04/A05/A06 choices authorize their named checkpoint/case mappings. Their explicit exclusions leave aggregate END open. They collectively authorize neither the four missing causal bridges nor a new composite END verdict. The user authorizes construction of this read-only analysis/proposal now; **accepting it as END qualification needs a separate decision**.

`COMPOSITE_QUALIFICATION_PERMITTED = NO` records the **currently selected scope**. A composite proposal is available only as a new explicit qualification-scope amendment. No runtime interpretation, native authority class or previously qualified stage oracle is changed.

The [exact decision dossier](qualification/E2_P05_END_ANCESTRY_RECONCILIATION_1/aggregate-END-decision-dossier.json) is decision-ready. Subject **SUBJECT_ID** binds this graph identity/content, complete oracle and N12/N13 contract, all unchanged stage/source/canonical identities, four specific bridge edge IDs, conditional PASS claim and every exclusion. Dossier raw SHA-256: **DOSSIER_HASH**. Authentication requires the qualified owner, exact subject/dossier/graph/content hashes and one option, followed by separate mapping qualification. A material change invalidates applicability. No signature, grant or selection is manufactured.

| Unselected option | Exact effect |
|---|---|
| RETAIN_FULL_ORIGINAL_END_ANCESTRY_REQUIREMENT | Retains the original full-native-mainline END method. “Original” describes the original acceptance requirement, not a new requirement to recover irrecoverable original event IDs. The graph remains supplemental; a fully sealed new native reproduction may satisfy the method. |
| AUTHORIZE_COMPOSITE_P05_END_QUALIFICATION_MAPPING | Allows only this exact amended qualification graph and four semantic bridges, after authentication and independent mapping qualification. Native history/permissions remain unchanged and continuous-mainline claims stay excluded. |

**Neither option is selected.** Native Action, DECIDE/USE/ATTEST/INSTALL/event/grant/execution permissions are outside this decision. Declining the composite method retains 13/13 local coverage and the full native END preparation blocker. Authorizing it could close only the aggregate acceptance-method gap after qualification; it does not automatically resolve P05 process/checkpoint/authority subjects, N08/N12 initial negative operands, interfaces, D01/REG or review readiness.

## Determinism, persistence and readiness

The graph is computed documentary qualification evidence. JSON retention records its own comparison identity and exact native input references; it creates no Planner object, Snapshot, proof, authority, root or ledger. Twelve fresh processes, three per hash seed **0,1,7,101**, reconstructed identical graph bytes/identity from retained authoritative inputs. Writer memory and native operations were unavailable. Native set/key semantics use the unchanged codec, while causal ledger arrays are kept ordered.

The [determinism evidence](qualification/E2_P05_END_ANCESTRY_RECONCILIATION_1/determinism.json) and [final verification](qualification/E2_P05_END_ANCESTRY_RECONCILIATION_1/verification.json) distinguish graph reconstruction from P05's later full END/D01/REG execution. Stage coverage stays **13/13**. P05 readiness stays **NO** until an aggregate method is selected and qualified, and every other already sealed readiness term also passes. P05/P06 are unexecuted.

```text
WORK_PACKAGE = E2-P05-END-ANCESTRY-RECONCILIATION
RESULT = PASS (RECONCILIATION / DECISION PREPARATION ONLY)
SINGLE_NATIVE_LINEAGE_REQUIRED = YES (UNAMENDED MAINLINE METHOD; EXPLICIT INFERENCE)
ORIGINAL_HISTORICAL_LINEAGE_REQUIRED = NO
SINGLE_NATIVE_LINEAGE_PROVEN = NO
COMPOSITE_QUALIFICATION_PERMITTED = NO (CURRENT SCOPE)
COMPOSITE_GRAPH_IDENTITY = GRAPH_ID
AGGREGATE_END_AUTHORITY_REQUIRED = YES
AGGREGATE_END_DECISION_READY = YES
AGGREGATE_END_SELECTED_OPTION = NONE
P05_BOUND_STAGE_INPUTS = 13
P05_REQUIRED_STAGE_INPUTS = 13
P05_EXECUTION_READY = NO
NEXT_PACKAGE = E2-P05 AGGREGATE END QUALIFICATION-SCOPE DECISION
P05_EXECUTED = NO
P06_EXECUTED = NO
ORIGINAL_A03_HISTORICAL_OCCURRENCE = UNPROVEN
ORIGINAL_A04_HISTORICAL_ANCESTRY = UNPROVEN
ORIGINAL_A05_HISTORICAL_ANCESTRY = UNPROVEN
ORIGINAL_A06_HISTORICAL_REQUEST_WAIT_TRACE = UNPROVEN
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO
RUNTIME_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```

[Preservation](qualification/E2_P05_END_ANCESTRY_RECONCILIATION_1/preservation.json) verifies every pre-existing file, including all thirteen stage bindings, their native artifacts and scopes, the P04 target, runtime and frozen E1. No existing source artifact, native event or authority changed. Only this reconciliation's reports, comparison manifests and read-only reconstruction harness were added.
'''
    for token, replacement in {'GRAPH_ID': findings['COMPOSITE_GRAPH_IDENTITY'],
        'SUBJECT_ID': findings['AGGREGATE_SCOPE_SUBJECT_ID'],
        'DOSSIER_HASH': evidence['scope_dossier']['raw_sha256']}.items():
        text = re.sub(r'\b' + re.escape(token) + r'\b', lambda match: replacement, text)
    path = DOCS / (STEM + '.md')
    if path.exists():
        assert path.read_text() == text
    else:
        path.write_text(text)
    print(json.dumps({'RESULT': 'PASS_CONTRACT_ONLY', 'stage_count': 13,
                     'aggregate_decision_ready': True, 'selected_option': 'NONE',
                     'P05_EXECUTION_READY': 'NO', 'dossier': findings['AGGREGATE_SCOPE_SUBJECT_ID']}))


if __name__ == '__main__':
    main()
