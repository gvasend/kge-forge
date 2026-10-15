# E1 graph resolution deterministic selection policy 1

Policy validation: **VALID**. Dry-run selection: **S-ANCESTRY**. **Criterion 5** first makes the result unique. No resolution action executed.

The normative machine-readable specification is `selection_policy` in [the resolution plan](E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json). This policy changes selection semantics only. The prior selection attempt remains historical evidence; its execution state, action definitions, completion states, graph, authorities and readiness values are unchanged.

## Ordered selection semantics

Start with the current eligible set after exact prerequisite, evidence, authority and effect checks. Ranking cannot confer eligibility or permission. Apply criteria only to the remaining tied set, in the user-specified order. Stop once unique; an initial singleton needs no tie-break.

1. Maximize the complete triple (directly resolved unresolved root conditions, distinct unresolved slots transitively dependent on those conditions, currently blocked actions newly eligible after this action alone passes), lexicographically. Require explicit graph-backed transitions and all gate predicates for every tied candidate. Missing or inconsistent values skip the entire criterion: `CRITERION_1_NOT_DECISIVE`. Do not substitute affected slots, eventual descendants, or hypothetical completion of other actions.
2. Maximize a comparable, formally represented information score derived from explicit outcome partitions or relationship eliminations. Without that model for every candidate, record `CRITERION_2_NOT_DECISIVE`. No expected usefulness or LLM inference is permitted.
3. Minimize static operation-class rank: DETERMINISTIC_VALIDATION, DETERMINISTIC_CONSTRUCTION, SOURCE_ACQUISITION, DETERMINISTIC_MAPPING, IMPLEMENTATION_PREPARATION, SEMANTIC_EVALUATION, ARCHITECT_PREPARATION, RUNTIME_EXPERIMENT, GOVERNED_OPERATION. Preserve action semantics. SEMANTIC_RESOLUTION maps to SEMANTIC_EVALUATION, except explicit DECISION_PREPARATION stages map to ARCHITECT_PREPARATION. Actual authority/contract decisions and implementation/validator repairs map to GOVERNED_OPERATION, not preparation or validation. Exact listed classes retain their names. Unmapped future classes skip this criterion for the tied set pending a policy revision; the selector never asks an LLM to assign priority at runtime.
4. Minimize effect rank: NON_EFFECTING, QUALIFICATION_EFFECT_ONLY, PRODUCTION_EFFECT. Then minimize cost only with complete comparable explicit deterministic cost metadata. Missing cost is not zero. Unknown effect labels skip this ranking, never bypass the upstream eligibility check.
5. Return the smallest canonical ActionId using exact case-sensitive Unicode code-point lexicographic comparison, with no locale or normalization. All current IDs are ASCII.

Every finite non-empty actionable set has unique canonical ActionIds. Each applicable criterion retains a non-empty subset; unavailable criteria retain the tied set. Criterion 5 gives its unique minimum. This proves totality over that domain independently of input order, JSON key order, time or conversation order. Conflicting duplicate IDs are malformed records, not a valid action set.

## Current graph evidence and replay

`CRITERION_1_NOT_DECISIVE`: the graph's 339 entities contain no resolution-action entities, and its assertions define no action-PASS transition system. All 15 plan actions explicitly have empty `closes_conditions_only_on_accepted_output`: zero direct roots and therefore zero unresolved slots through directly closed roots. The newly eligible count cannot be derived completely from this graph. Plan dependency-only simulations would rank preparation steps differently, but omit formal graph outcome/authority predicates and are not substituted for the requested metric. No missing count is estimated.

`CRITERION_2_NOT_DECISIVE`: there are no formal outcome partitions, alternative graph-state enumeration, or deterministic relationship-elimination scores. Different possible prose result labels do not establish information gain.

| ActionId | Priority class | Direct roots | Slots through those roots | Graph-proven newly eligible |
|---|---|---:|---:|---|
| PREP-AUDIT | ARCHITECT_PREPARATION | 0 | 0 | Unknown |
| PREP-BINDING-GRANT | ARCHITECT_PREPARATION | 0 | 0 | Unknown |
| PREP-RUNTIME_HEAD | ARCHITECT_PREPARATION | 0 | 0 | Unknown |
| PREP-SUPERVISOR | ARCHITECT_PREPARATION | 0 | 0 | Unknown |
| PREP-VALIDATOR | ARCHITECT_PREPARATION | 0 | 0 | Unknown |
| S-ANCESTRY | SOURCE_ACQUISITION | 0 | 0 | Unknown |
| S-APPROVAL | SOURCE_ACQUISITION | 0 | 0 | Unknown |
| S-BINDING | SOURCE_ACQUISITION | 0 | 0 | Unknown |
| S-CONTEXT | SOURCE_ACQUISITION | 0 | 0 | Unknown |
| S-EXEC | SOURCE_ACQUISITION | 0 | 0 | Unknown |
| SEM-BUDGET | SEMANTIC_EVALUATION | 0 | 0 | Unknown |
| SEM-ELIGIBILITY | SEMANTIC_EVALUATION | 0 | 0 | Unknown |
| SEM-IGNORED | ARCHITECT_PREPARATION | 0 | 0 | Unknown |
| SEM-IMPLEMENTATION | SEMANTIC_EVALUATION | 0 | 0 | Unknown |
| SEM-INTERFACES | SEMANTIC_EVALUATION | 0 | 0 | Unknown |

Criterion 3 retains S-ANCESTRY, S-APPROVAL, S-BINDING, S-CONTEXT and S-EXEC. Criterion 4 retains all five: NON_EFFECTING, no explicit comparable cost metadata. Criterion 5 uniquely selects S-ANCESTRY. The graph and plan identities and exact source fields are retained in the JSON policy provenance.

## Validation

The reference selector below was run in an isolated temporary script, not installed in planner implementation. All checks passed:

- 49 deterministic input orders: ascending, descending, all 15 rotations, and 32 SHA-256-keyed orders.
- 100 identical-state replays and reversal of every action JSON object's key order.
- All six permutations of a synthetic equal-priority three-action set select TEST-A.
- Equal explicit coverage/information/cost scores still reach Criterion 5.
- Partial coverage metadata skips Criterion 1; separately unequal complete coverage, information and cost scores select at their respective criteria.
- No action definitions or historical execution-state fields changed; all other E1 artifact hashes remain unchanged.

## Validated reference selector

Optional metric maps below are accepted only after the completeness/provenance checks above; current graph replay passes none. `classes`, `effects`, and `mapped` use the fixed definitions above. The reference is a policy test, not a production implementation.

```python
def select(actions, coverage=None, information=None, costs=None):
 byid={a['id']:a for a in actions}; ids=sorted(byid); trace=[]
 assert ids and len(byid)==len(actions)  # canonical unique ActionIds
 def narrow(number, scores, greatest=False):
  nonlocal ids
  if scores is None or any(i not in scores or scores[i] is None for i in ids):
   trace.append((number,'NOT_DECISIVE',list(ids))); return False
  best=(max if greatest else min)(scores[i] for i in ids)
  ids=[i for i in ids if scores[i]==best]
  trace.append((number,'APPLIED',list(ids))); return len(ids)==1
 if len(ids)==1: return ids[0],0,trace
 if narrow(1,coverage,True): return ids[0],1,trace
 if narrow(2,information,True): return ids[0],2,trace
 ranks={i:classes.index(mapped(byid[i])) if mapped(byid[i]) in classes else None for i in ids}
 if narrow(3,ranks): return ids[0],3,trace
 ranks={i:effects.index(byid[i]['effect_boundary']) if byid[i]['effect_boundary'] in effects else None for i in ids}
 if narrow(4,ranks): return ids[0],4,trace
 if narrow(4,costs): return ids[0],4,trace
 ids.sort(); trace.append((5,'APPLIED',[ids[0]])); return ids[0],5,trace
```

```text
SELECTION_POLICY = VALID
SELECTED_ACTION = S-ANCESTRY
DECIDING_CRITERION = 5
PERMUTATION_INVARIANT = YES
REPLAY_INVARIANT = YES
TOTAL_SELECTOR = YES
LLM_PREFERENCE_REQUIRED = NO
PLAN_STATE_CHANGED = SELECTION_POLICY_ONLY
PRODUCTION_EFFECT = NO
```

## Decision-input reentry 1: static class extension

`DECISION_INPUT_ACQUISITION` maps to `ARCHITECT_PREPARATION` because it prepares bounded unadopted dossiers. The criterion order and priority list are unchanged. The current two-action replay selects INPUT-BUDGET at Criterion 5; both actions tie at Criteria 3 and 4, while Criteria 1/2 lack formal metrics. Original validation above remains historical. See [reentry semantics](E1_DECISION_INPUT_REENTRY_SEMANTICS_1.md). No action executed.
