import json,hashlib
from pathlib import Path
OUT=Path(__file__).resolve().parent
load=lambda n:json.loads((OUT/n).read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
proof=load('POST_PUBLICATION_RECONSTRUCTION.json');assert proof['result']=='PASS'
pub=load('PUBLICATION_RECORD.json');pin=load('PRIVATE_PUBLICATION_PIN.json');q=load('CONSUMPTION_QUALIFICATION.json')
host=load('HOST_INSTALLATION_MANIFEST.json');app=load('MATERIAL_RELEASE_APPLICATION.json');dispatch=load('ARCHITECT_DISPATCH_AMENDMENT.json')
assert not host['target_directory_exists'] and not Path('/var/lib/kge-forge-supervisor-succession').exists()
assert proof['state']=='INACTIVE' and proof['ownership']=='NONE' and proof['handoff_eligible'] is False
for name in ('AMENDMENT_PROBES.log','CURRENT_REGRESSION.log','ISOLATION_RETRY.log'):assert (OUT/name).read_text().rstrip().endswith('OK')
for p,h in load('PRESERVED_STATE.json').items():assert sha(Path(p))==h
for p,h in q['implementation']['current'].items():assert sha(Path(p))==h
rows='\n'.join('| '+k+' | `'+v+'` |' for k,v in {**proof['identities'],**proof['context_identities']}.items())
text=f'''# PD-06 Supervisor Authority Amendment — publication and production consumption

**PUBLISHED; production decision-consumption qualification PASS; independent private restart reconstruction PASS. E1 remains INACTIVE with NO OWNERSHIP. E1-WP-001 remains INELIGIBLE and UNDISPATCHED. S2 is unlaunched.**

## Applied authority

- Applied amendment: `{pub['amendment_identity']}`.
- Exact authorized candidate-file SHA-256: `5a73a14859ddf63a733fcc1941a0a744f9c399863ef7eaf8f6889c4e769d0eae`.
- Resulting release authority: `{pub['resulting_release_authority']}`.
- Separate append-only release decision: `{pub['release_amendment_decision']}`.
- Dispatch amendment: `{dispatch['id']}`.
- Dispatch amendment file SHA-256: `{pub['dispatch_amendment_file_sha256']}`.
- Accepted frozen succession implementation: `{q['accepted_succession_implementation']}`.
- Qualified production-consumption implementation: `{q['implementation_identity']}`.

The release rule is: **The Execution Supervisor authority holder is historical S1, or exactly one explicitly Architect-authorized, qualified successor selected through authenticated SupervisorSuccession. Missing evidence establishes no ready holder.** The exact fourteen conditions remain in the authorized immutable candidate. Configuration equality is insufficient. Historical S1 remains `SupervisorHistoricalInstance-sha256:8ffe7a419d3953ed54fb1a73a9bd1d793cbe2c540c181cee9c0ca4e30987d572`; missing historical boot/start observations were not manufactured.

The original PD-06 decision, E1-B01 PASS, ReleaseBasisId, ReleaseDecisionId, original dispatch authorization `auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39`, task, profile, payload and grants remain unchanged. All 716 historical reference fingerprints were rechecked without rewriting them. Profile bytes remain `a0547c7c33b95628d9419a62972f15062bd6fa8ab9236496ceb7d6ab21fbab75`; canonical profile fingerprint remains `b9e7f72d97525f39fbddfe92f276ab6aedd057ef6c5b7284dc163f1db9c9c328`.

No Programmer tool, read/write grant, execution or QUIESCENT rule, sequential execution, ownership mechanism, transmission/destination policy, snapshot/evidence isolation or host authority boundary was expanded. The exact production delta is in `IMPLEMENTATION_DELTA.json`. Material implementation is bound directly through a material release application, not mislabeled as OPERATIONAL-CONTINUATION-1.

## Current operational ancestry

| Identity | Value |
| --- | --- |
{rows}

The adopted authority-store context `2f51cf476c9b77eda1dbbb38407e68c8b698137b5732ab20416e9189522882c3` precedes the first material application `439bfbea3b1b75ba832f80e690ccdf7cd3e0414ae88eb063d0d8ecc430735ce0`, which precedes the current corrected application above. After initial publication, final review added exact host-receipt plan/launcher hash comparison against the independent host grant. The first publication is retained; this append-only correction binds its exact private publication and ancestry. Release and dispatch amendment bytes and identities are identical across both applications. No successor, launch, activation or ownership occurred between them. The final external bootstrap pin selects this qualified version.

Private store: `{proof['private_store']['root']}`. Catalog SHA-256: `{proof['private_store']['catalog_sha256']}`. All {proof['objects']} logical objects / {proof['distinct_objects']} distinct content objects were verified privately. Store placement remains outside all Programmer grants and execution/transmission roots. Repository files are documentary provenance, not operational authority.

Private publication pin: `{pin['path']}`, SHA-256 `{pin['sha256']}`. Restart verification read the private pin with an explicit expected hash, opened the pinned store, checked every object, reconstructed full operational ancestry, authenticated the original dispatch plus the explicit amendment, and reconstructed the original authorization lifecycle without acquiring an ownership fence. See `POST_PUBLICATION_RECONSTRUCTION.json`.

## Qualification

All twelve requested cases are mapped in `QUALIFICATION_COVERAGE.json`. Seventeen targeted synthetic amendment tests pass. Twenty-seven current regression tests pass; the unchanged payload namespace isolation probe also passed its explicitly permitted retry outside the sandbox after the sandbox rejected NETLINK_ROUTE. Original failed sandbox output remains evidence; no validator exception was introduced.

Tests cover original-release S1 behavior, private release/dispatch decision authentication, missing/invalid amendments, wrong composite authority, absent/wrong dispatch inheritance, inability to self-authorize S2, separate specific succession authority, separately attributable Jerry host consent, exact receipt-to-grant hashes, private substitution, replay/reordering, correction ancestry and fresh-process reconstruction. Regressions cover private authority isolation, production activation/ownership/handoff/recovery synthetically, transmission filtering, governed execution and authoritative QUIESCENT, lifecycle and context/payload preservation. No synthetic fixture uses real E1 ownership.

Production readiness remains **BLOCKED**: no private specifically authorized successor policy or genuinely observed S2 exists. This is the expected stop point, not a failed amendment qualification. The original dispatch inherits only through the authenticated explicit dispatch amendment; neither amendment supplies a successor identity.

## Frozen host package and exact proposed installation

Frozen launcher SHA-256: `{host['frozen_package']['launcher_sha256']}`.
Frozen launch-proposal SHA-256: `{host['frozen_package']['frozen_launch_proposal_sha256']}`.
The accepted full succession inventory and qualification closure remain exact. The installation target `/var/lib/kge-forge-supervisor-succession/` remains absent.

`HOST_INSTALLATION_MANIFEST.json` contains source/destination/owner/mode and exact hashes. `PROPOSED_LAUNCH_SPEC.json` contains every proposed field with the current operational binding and qualified consumption inventory: interpreter `/usr/bin/python3.11`, argv `[/usr/bin/python, -m, adapter.supervisor_server, /tmp/a21m.sock]`, UID/GID 1000:1000, supplementary groups [], workspace `/home/gvasend/app/kge-forge`, delegated cgroup `/sys/fs/cgroup/unified/kge-forge/executor`, socket `/tmp/a21m.sock`, exact environment and unchanged protocol constants. It retains `PROPOSED_NOT_AUTHORIZED` and a null prelaunch audit hash.

`HOST_INSTALLATION_PROCEDURE.md` gives exact human installation commands and post-launch capture requirements. The frozen wrapper places the root child in the delegated cgroup before credential drop. It does not rely on unprivileged startup in user.slice followed by migration. No command in that document was executed.

Architect pre-launch fields that can be proposed now are `authority`, decision type, predecessor S1, current `runtime_binding`, frozen `launcher_sha256`, implementation/qualification identities and proposed plan fields. Actual `authorization_id`, `qualification_acceptance_id`, executable plan status and final `launch_spec_sha256` require the separate Architect launch decision and fresh host observations. Specific succession acceptance remains post-launch and must bind genuine S2 identity and the exact event body; all current S2/event/approval fields are null.

Jerry must explicitly provide a separately attributable HOST_OPERATOR launch authorization: operator, decision, authorization ID/source, exact launch-spec/launcher hashes, predecessor, runtime binding and command/scope. Its ID becomes `host_operator_authorization_id` in the wrapper input. Root staging/installation, cgroup placement before credential drop and launch must be covered. `remove_verified_stale_socket` remains false unless Jerry separately authorizes deletion after a genuine no-listener check. See `HOST_AUTHORIZATION_BOUNDARIES.json` for exact schemas. The root wrapper authenticates file ownership and exact bytes but does not itself verify signatures; the root operator must authenticate both actual decisions before staging, and the production controller additionally requires the private attributed host grant and matching receipt.

Final approved plan and authorization file hashes are intentionally unset: those files and consents do not yet exist. Proposal hashes are exact and are not represented as executable authority. The unchanged final launch command, for the separately authorized human operator only, is:

```sh
sudo /usr/bin/python3.11 /var/lib/kge-forge-supervisor-succession/host_launch.py /var/lib/kge-forge-supervisor-succession/LAUNCH_SPEC.json /var/lib/kge-forge-supervisor-succession/HOST_LAUNCH_AUTHORIZATION.json
```

## Stop confirmation

S2 unlaunched; no host package installed; no SupervisorSuccession event; no real E1 activation event or ownership; zero E1 model requests and zero E1 implementation effects. Model-handoff eligibility is false. E1-WP-001 remains INELIGIBLE and UNDISPATCHED. No human/host consent was fabricated.
'''
(OUT/'REPORT.md').write_text(text)
closure={'result':'PASS','publication_pin':pin,'amendment_identity':pub['amendment_identity'],
 'release_authority':pub['resulting_release_authority'],'dispatch_amendment':dispatch['id'],
 'identities':proof['identities'],'state':'INACTIVE','ownership':'NONE','S2_launched':False,
 'evidence':[{'path':str(p),'sha256':sha(p)} for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='CLOSURE.json' and '__pycache__' not in p.parts]}
(OUT/'CLOSURE.json').write_text(json.dumps(closure,sort_keys=True,separators=(',',':')))
for p in OUT.rglob('*'):
 if p.is_file() and '__pycache__' not in p.parts:p.chmod(0o444)
print(json.dumps({'result':'PASS','report':str(OUT/'REPORT.md'),'OperationalContextId':proof['identities']['OperationalContextId']}))
