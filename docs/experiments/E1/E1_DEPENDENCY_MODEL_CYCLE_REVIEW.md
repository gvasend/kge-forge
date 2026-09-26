# E1 Dependency Model — Cycle Semantics Review

Review date: 2026-09-21  
Scope: the two reciprocal pairs in the reconciled model.  
Constraint: read-only semantic review; no graph, authority, implementation, or production changes.

## Assessment

Neither pair is established as a genuine circular prerequisite. Both pairs combine an ordering/derivation relation with a currentness, binding, or correspondence relation. Treating every relation as a prerequisite edge creates artificial cycles and can make satisfaction semantics circular. The model should retain the semantic information, but the non-prerequisite relation should be represented in a separate typed relation layer or as a constraint/consistency edge excluded from prerequisite traversal.

## Pair 1: `R4_CURRENT ↔ G4_CURRENT`

### Edge `G4_CURRENT → R4_CURRENT`

**Proposition represented:** the live R4 controller can reconstruct and treat R4 as current using the selected live authority-store generation G4.

**Is the source’s satisfaction prior to the target required?** Partly. A live R4 currentness assertion must be checked against the authority store actually consumed by the R4 controller. That is a currentness/authority binding, not proof that G4 was created before R4 existed.

**Evidence:** the accepted G3→G4 selection required R4-final to remain current, and post-selection reconstruction required the live R4 consumer to authenticate the dispatch and invocation from G4. The G4 artifact and live reconstruction evidence establish this relationship as a live-store correspondence.

**Relationship classification:** `correspondence` + `synchronization`/`freshness`, not a pure prerequisite.

**Removing from prerequisite traversal:** does not lose legitimate knowledge if retained as an explicit currentness constraint: `R4_CURRENT.runtime_store == G4_CURRENT.consumed_store`.

**Circularity if retained as prerequisite:** yes. Treating G4 as a prerequisite for R4 while also deriving G4 from R4 makes “R4 is current” depend on a store selected from R4. That is a temporal/authority loop, not a sound construction order.

### Edge `R4_CURRENT → G4_CURRENT`

**Proposition represented:** G4 was derived and selected from the already-current R4 production authority state, adding the authorized reconciliation record while preserving G3.

**Is the source’s satisfaction prior to the target required?** Yes for the G4 operation: the G4 pre-selection gate required exact R4-final currentness, G3 currentness, and the one-record delta. This is a real temporal/derivation prerequisite for the G3→G4 selection.

**Evidence:** the Architect G4 authorization and `LIVE_R4_G4_GENERATION.json` selection qualification explicitly required live R4-final current, exact G3, deterministic G4 derivation, and post-selection reconstruction.

**Relationship classification:** `derivation` + `temporal prerequisite` for the G4 selection operation.

**Removing from prerequisite traversal:** would lose the legitimate ordering that G4 selection follows the established R4 state. It should remain in the construction DAG for the G4-selection operation.

**Circularity if retained with the reverse edge:** the pair becomes circular only when the currentness correspondence above is represented as another prerequisite. The derivation edge itself is not circular.

### Pair conclusion

Classification: **B/C — two semantic relationships incorrectly represented as reciprocal prerequisites**. The recommended boundary is:

- retain `R4_CURRENT → G4_CURRENT` as a derivation/temporal edge for generation selection;
- represent `G4_CURRENT` ↔ `R4_CURRENT` as a typed live-consumer currentness constraint or correspondence, excluded from prerequisite traversal;
- do not use the reverse correspondence as a prerequisite for constructing R4.

This does not authorize a new generation or change the accepted live state.

## Pair 2: `INVOCATION_CANDIDATE ↔ OPERATIONAL_BINDING_CURRENT`

### Edge `OPERATIONAL_BINDING_CURRENT → INVOCATION_CANDIDATE`

**Proposition represented:** the candidate invocation must be checked against the exact operational binding that governs its runtime, context, dispatch, profile, and policy envelope.

**Is the source’s satisfaction prior to the target required?** It is required for applicability/validation of an invocation candidate, but it is not necessarily required to construct the invocation’s binding if the binding is derived from the invocation and other authenticated inputs.

**Evidence:** the operational-context/binding model and the R4 invocation qualification require shared InvocationAttemptId, runtime/context, dispatch, profile, and policy bindings. The R4 applicability negative tests reject invocation/binding mismatches.

**Relationship classification:** `binding` + `consistency constraint` + `applicability`, not an unconditional construction prerequisite.

**Removing from prerequisite traversal:** legitimate knowledge is preserved if the edge becomes a validation constraint: `binding.invocation_id == candidate.id` and all shared authority identities agree. Removing it as a prerequisite avoids falsely requiring a binding to pre-exist its own invocation input.

**Circularity if retained as prerequisite:** yes when the reverse derivation edge is also present. The binding cannot both authenticate the invocation and require that invocation as a prior authority without a separate source/dependency boundary.

### Edge `INVOCATION_CANDIDATE → OPERATIONAL_BINDING_CURRENT`

**Proposition represented:** the canonical operational binding is constructed from the exact invocation together with dispatch, context, profile, runtime, release, and policy inputs.

**Is the source’s satisfaction prior to the target required?** Yes if the qualified binding schema defines invocation as an input to binding derivation. The binding identity cannot be computed from an invocation-independent placeholder.

**Evidence:** `DEEP_AUTHORITY_ROOT_RECONSTRUCTION.json` and `OPERATIONAL_CONTEXT_BINDING_MODEL_QUALIFICATION.json` describe OperationalBinding as a derived object with Invocation and Dispatch inputs, while prohibiting circular WorkAuthorization/OperationalBinding authority.

**Relationship classification:** `derivation prerequisite`.

**Removing from prerequisite traversal:** would lose the binding constructor’s actual input ordering and could permit a binding not bound to the exact invocation. It should remain in the derivation DAG.

**Circularity if retained with the reverse edge:** the reverse relation must be a post-derivation validation/correspondence check, not a prerequisite. Otherwise satisfaction is circular.

### Pair conclusion

Classification: **C — one prerequisite plus one non-prerequisite relationship**:

- retain `INVOCATION_CANDIDATE → OPERATIONAL_BINDING_CURRENT` as derivation;
- represent `OPERATIONAL_BINDING_CURRENT` ↔ `INVOCATION_CANDIDATE` as an applicability/binding consistency constraint after both records are independently available;
- exclude the reverse consistency relation from prerequisite traversal.

This preserves the no-self-authorization rule. OperationalBinding must still have independently authoritative inputs; an invocation copy alone cannot create authority.

## Cycle and DAG implications

The two cycles are semantic cycles only because the graph currently places derivation, correspondence, synchronization, and applicability in one prerequisite edge set. They are not evidence that E1 requires a genuinely circular authority model. A sound traversal would maintain at least two relations:

1. a directed prerequisite/derivation DAG used for construction and execution ordering;
2. typed non-ordering constraints for correspondence, currentness, binding, applicability, and TOCTOU freshness.

The current review does not apply that correction. Until it is applied and validated, the reconciled model should remain assessed as `PARTIAL / FAIL as a DAG`.

## Recommended corrections (not applied)

- Reclassify the R4/G4 reverse relation as `CURRENTNESS_CORRESPONDENCE` or `LIVE_CONSUMER_SYNCHRONIZATION`, not a prerequisite.
- Retain R4→G4 as the generation-selection derivation/temporal edge.
- Reclassify OperationalBinding→Invocation as a post-construction binding/applicability constraint.
- Retain Invocation→OperationalBinding as the derivation edge only if the canonical constructor confirms Invocation is an input.
- Add machine-checkable relation classes so non-ordering constraints cannot create prerequisite cycles.
- Preserve both relations in audit evidence; do not delete the knowledge merely because one relation leaves the construction DAG.

## Conclusion

The evidence supports **B/C** rather than a genuine circular prerequisite for both reciprocal pairs. The cycles expose a node/relation modeling problem, not a reason to invent authority or to execute production actions.
