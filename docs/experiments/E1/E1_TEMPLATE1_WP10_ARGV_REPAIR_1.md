# WP-10 argv representation repair — justification and qualification 1

## Decision and scope

The user's bounded repair instruction authorizes the local constructor change and regression tests. It does not issue domain authority, authorize the WP-14 shared validator, publish a new runtime, or grant production execution.

The authoritative source-resolution report §1 says there is no separate T1 JSON Schema: `invocation_constructor.py` implements the effective contract. The consumer reconciliation specifies JSON canonical serialization and typed reconstruction. The production contract explicitly leaves broader field-source/type/provenance qualification incomplete. Consequently this repair does not claim an existing complete formal schema or complete WP-13.

The canonical representation of this field is a JSON array of argv arrays containing strings, as in the current released-profile content and ProgrammerProfile. JSON has no tuple type. The runtime tuple representation is intentional: `WorkAuthorization.exec_argv_allowlist` is annotated `tuple`, `authority_profile.programmer_authorization()` explicitly constructs a tuple of tuples, and the host compares `tuple(argv)` against its entries. Those independent producer and consumer facts justify preserving the comparison and decoding at the T1 canonical-to-runtime constructor boundary.

## Explicit representation rule

`_argv_allowlist_from_json()` accepts only a built-in list containing built-in, nonempty lists of built-in, nonempty strings without NULs. It rejects tuples, strings masquerading as containers, dictionaries, nulls, numeric/boolean atoms, and nested non-string atoms with `ConstructionDenied`; it does not coerce arbitrary iterables or stringify values. NUL/empty-string rejection agrees with the host's existing argv checks. Host command-size limits and other gates remain unchanged.

After validation it constructs `tuple(tuple(command) for command in value)`. Every string, command, duplicate, and order is preserved. There is no path normalization, basename substitution, shell splitting, wildcard expansion, sorting, deduplication, default insertion, or caller-selected policy. Source lists are not mutated or aliased by the immutable result. Re-serializing either representation yields identical canonical JSON bytes.

An explicitly supplied empty JSON array maps to the existing empty runtime tuple. In the unchanged host this means no exact-argv restriction from this field; it does NOT mean deny all. The decoder preserves that pre-existing sentinel rather than creating a new permission policy. Missing/malformed/nonempty input never falls back to empty. The current E1 policy is nonempty and cannot be replaced by this sentinel. Source authentication remains an independent mandatory gate.

The only adapter change is at `construct_work_authorization()` after its exact field-key check and before typed construction. The host comparison, serialization, authority sources, allowlist values, and issuance path are unchanged. Canonical template bytes are not rewritten. Direct in-memory tuple input to this JSON boundary is intentionally rejected; runtime-native producers retain their separate interfaces.

## Qualification before WP-10 re-evaluation

Command: `python3 -B -m unittest adapter.tests.test_invocation_constructor -v`

Result: **5 tests PASS**. Synthetic test fixtures use only `test-only-*` identities, not current E1 source inputs. They are not Template-1/Candidate-3 production artifacts or authority.

- Canonical JSON round trip reproduces the original list-versus-tuple rejection, then verifies deterministic tuple reconstruction, unchanged source bytes, and INACTIVE construction.
- The actual unchanged `GovernedHost.issue_exec_permit` guard is exercised with an in-memory stub and mocked lifecycle check. The matching command reaches an intentional rejection at the caller-supplied-scope-ID check before locks, snapshots, ownership, audit, or permit creation. No real host is initialized or lifecycle activated.
- Ten non-equivalent argv variants reject in both directions: added/removed/reordered/duplicated arguments, alternate executable spelling/path, literal wildcard versus filename, whitespace, case, and joined argument strings. Snapshot/audit calls remain absent.
- Fifteen malformed representation cases reject explicitly instead of coercing.
- Ordering, duplicate commands, Unicode/literal strings, input mutation isolation, empty-sentinel representation, and missing-field rejection are covered.

The repair is independently justified by the source/producer/consumer contract analysis above and qualified by these focused tests before WP-10 is re-evaluated. This is local checkout qualification only, not release qualification for the unchanged frozen R4 identity. The full shared validator remains outside scope.

## Exact provenance

| File | SHA-256 |
|---|---|
| `adapter/invocation_constructor.py` | `5908b257fdc7325d94d7524fbacbe3a7ec26d18d98507d6232c9ba1d41e8f9f7` |
| `adapter/tests/test_invocation_constructor.py` | `413f4623650ebbd78d3dedbfa57cd6589eb8f0cc765e43194cce38c9aaf8268e` |
| `adapter/governed_host.py` | `cb1d56d5787f69848ac67a8eee11755bd524cfbce17f5c0d797245357c0cdc16` |
| `adapter/authority_profile.py` | `a6f371fe1b6a4204631195976fbb938238a45ae1445243945aee68ad32c7c0a7` |
| `docs/experiments/E1/E1_WORKAUTHORIZATION_TEMPLATE1_SOURCE_RESOLUTION_1.md` | `b17cd033f64aa37ac92d5a7b7e6008d7b3a495cc7cd613b28482b743ced3e03e` |
| `docs/experiments/E1/E1_WORKAUTHORIZATION_CONSUMER_CONTRACT_RECONCILIATION_1.md` | `2ecc817901f9b7b7b3eb0ea635ff8fbc4ce817d472d3082a6a0f058eaca6e9ee` |
| `docs/experiments/E1/E1_WORKAUTHORIZATION_TEMPLATE1_PRODUCTION_CONTRACT_1.md` | `1af1f3aac2acc34aefb8c0b2a9a6fb775de152f2f8db6eaf6dd0673458ea6b6a` |

Constructor before repair SHA-256: `0799ca15ab055ddd13117cd67e4e47a924f02eacc78620d5ecee567f5d694ce2`.

`PRODUCTION_EFFECT = NO`. No domain authority was altered, consumed, or issued.
