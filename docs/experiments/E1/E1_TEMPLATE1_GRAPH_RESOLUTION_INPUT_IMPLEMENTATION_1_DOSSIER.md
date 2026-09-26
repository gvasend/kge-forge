# INPUT-IMPLEMENTATION — incomplete DEC-IMPLEMENTATION dossier 1

**FACT_BLOCKED. Not presented for Architect approval. No identity domain is selected.**

The existing decision requires a domain choice with an authenticated owning source, canonical selector and byte-verification rule. Reducing it to a general preference would not satisfy that contract.

## Alternative A: conditional runtime content domain

Proposition: make the field denote the qualified current frozen runtime content identity. Recorded reference: `sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761`, from `/runtime` of `OperationalContext-sha256:ff57a2103cdcbfa578a4ce22d774ecea374a34267cdaf8d53385fca916dbc10c`. Proposed field shape is an exact `sha256:<64 lowercase hex>` JSON string, with no coercion. This is an unadopted contract proposal, not an accepted mapping.

The source context must be independently authenticated and applicable; the exact frozen runtime bytes must verify under their owning content-identity rule. Serializing the reference string is not hashing runtime content. Runtime byte qualification and current applicability are unestablished downstream obligations. Nothing here establishes the proposed equality.

## Alternative B: distinct implementation domain

A distinct implementation domain is a represented alternative, but the accepted corpus does not supply its owning record, exact identity semantics, source selector or canonical byte contract. All are explicitly NOT_ESTABLISHED. Importing a digest or another adapter path’s identity would invent a relationship.

These missing inputs determine the actual contract being chosen; a future-source placeholder cannot make this exact decision ready. No schema, identity prefix, producer or source member is fabricated. No broader source investigation was performed.

## Acceptance and readiness

The bounded action prepared and recorded what its allowed evidence establishes, but cannot meet the complete-dossier criterion. ACTION_RESULT = BLOCKED; DEC-IMPLEMENTATION = FACT_BLOCKED. Source/byte qualification is distinct from domain choice, but that distinction cannot fill the distinct-domain source/selector contract. Accepted knowledge does not complete the action or satisfy a root/slot.

Exact missing inputs:
- IMPLEMENTATION-OWNING-SOURCE: For a distinct domain, concrete owning source record/domain and its independently authenticated identity; no such member is established by accepted OperationalContext evidence.
- IMPLEMENTATION-SELECTOR: Exact source field or canonical body and byte-to-identity selector for that distinct domain, with scoped applicability and verification rule supported by its source contract.

The next allowed reentry requires new accepted evidence for these inputs and a separately authorized preparation attempt. No external facts were acquired.

## Provenance

- `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_SEM_IMPLEMENTATION_1_RESULT.md` — `sha256:7ed6761a1546dc659261691071c9e63b87a82a492a4a32513ff85fa730dfe999` — Accepted K1-K3 and Exact authority requirement
- `docs/experiments/E1/E1_OPERATIONAL_CONTEXT_1.json` — `sha256:3450887d8821a9bc53446499e4bbb2ef5fc1e94acdf830e5d03488a6fe25ef9b` — /runtime; /scope; /controller_store; /identity; absent implementation_identity
- `docs/experiments/E1/E1_WORKAUTHORIZATION_TEMPLATE1_PRODUCTION_CONTRACT_1.md` — `sha256:1af1f3aac2acc34aefb8c0b2a9a6fb775de152f2f8db6eaf6dd0673458ea6b6a` — implementation_identity row: conditional runtime identity equivalence
- `docs/experiments/E1/E1_WORKAUTHORIZATION_PRODUCTION_CONTRACT_DECISION_1.md` — `sha256:b916edc33d1534b516a187118146364c88aa360f0c8ff4f2dcc91a205aca1ad6` — implementation_identity row; authenticated source and per-field provenance requirements
- `adapter/invocation_constructor.py` — `sha256:5908b257fdc7325d94d7524fbacbe3a7ec26d18d98507d6232c9ba1d41e8f9f7` — _body required keys and return; artifact digest
- `docs/experiments/E1/E1_DECISION_INPUT_REENTRY_SEMANTICS_1.md` — `sha256:52827b823847a66266322c86818ae62826f761e30954f179e8282f96d79a5367` — Implementation-identity route; common dossier predicates

Source byte changes stale these observations. The JSON companion preserves the partial alternatives, exact omissions and reentry requirement.
