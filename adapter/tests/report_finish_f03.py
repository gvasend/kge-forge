"""Publish F03 only after every required qualification and preservation gate."""
import hashlib,json,subprocess
from pathlib import Path
from adapter.tests import qualify_finish_f03 as q
from adapter.planner import codec as c,model as m,installation as i,proof_installation as pi,core
R,D,O,P=q.R,q.D,q.O,q.P
def read(name):return c.parse_json((O/name).read_bytes())
def ref(name):return str((O/name).relative_to(R))
def identity(x):return x['namespace']+':'+x['sha256']

def run():
 qual=read('generic-qualification.json');assert qual['result']=='PASS'
 assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in qual['hashes'].items())
 life=read('lifecycle-qualification.json');assert life['p04_exit'] and not life['canonical_lifecycle_executed']
 negatives=read('f02-negative-results.json');assert len(negatives)==30 and all(v['status']=='PASS' for v in negatives.values())
 bounds=read('boundary-comparisons.json');assert len(bounds)==8 and all(x['status']=='PASS' and all(x['checks'].values()) for x in bounds.values())
 perms=read('unordered-permutations.json');assert len(perms)==9 and all(all(v=='PASS' for v in row.values()) for rows in perms.values() for row in rows.values())
 cold=read('fresh-reader-results.json');generic=read('generic-fresh-reader-results.json')
 assert len(cold)==132 and len(generic)==12 and all(x['exit']==0 for x in cold+generic)
 assert len({(x['boundary'],x['seed'],x['reader']) for x in cold})==132
 reproductions={str(seed):read('reproduction-seed-'+str(seed)+'-final.json') for seed in (0,1,7,101)}
 assert all(x['positive_path']=='PASS' and all(all(v.values()) for v in x['boundaries'].values()) for x in reproductions.values())
 a09=read('a09-precommit-oracle.json');assert len(a09)==18 and all(a09.values())
 man=read('configuration-manifest.json');b=c.restore(Path(man['path']),c._unwire(man['bundle_id']),R)
 assert len(b.events)==9 and not b.current.receipt_admissions and not b.current.validation_results and not b.current.validation_support_records and not b.current.typed_proofs and not b.current.proof_contracts
 assert not any(s.state is m.ActionState.COMPLETED for s in b.current.statuses if s.id.value in ('E2-REENTER','E2-FINISH'))
 assert all(i.current(b,r) for r in b.current.installed_definitions)
 baseline=read('baseline.json')['files'];changed=[p for p,h in baseline.items() if not Path(p).exists() or hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h]
 assert set(changed)=={'adapter/planner/installation.py','adapter/planner/typed_proofs.py'},changed
 assert not any(p.startswith('docs/experiments/E1/') or p.startswith('docs/plans/') for p in changed)
 diff=subprocess.run(['git','diff','--check'],cwd=R,capture_output=True,text=True);assert diff.returncode==0,diff.stdout+diff.stderr
 logs={'generic':('generic-tests.log',6),'ingress_validation_authentication':('current-regressions.log',52),'installation_action_proofs':('install-proof-regressions.log',33),'E06':('e06-current-regressions.log',4)}
 assert all('Ran '+str(count)+' tests' in (O/file).read_text() and '\nOK\n' in (O/file).read_text() for file,count in logs.values())
 config=pi.records(b.current,'ROOT_SLOT_CONFIGURATION_SET')[0];df,body=i.descriptor(config.request.definition)
 proof_defs=[q.load_definition(R,item) for item in q.F['installable_definitions'][2:]]
 slots=[i.descriptor(x)[0] for x in proof_defs]
 identity_domains={
 'configuration':{'installable_definition_id':c._wire(config.request.definition.id),'installed_definition_id':c._wire(config.id),'body_content_id':df['content_id']},
 'root_source':{'native_entity_id':body['source_entity_definitions'][1]['id'],'canonical_body_content_id':body['sources'][1]['content_id']},
 'slot':{'native_slot_id':c._wire(b.current.slots[0].id),'definition_body_content_id':body['slot']['content_id']},
 'root':{'native_condition_id':c._wire(b.current.roots[0].id),'definition_body_content_id':body['existing_root_to_bind']['content_id']},
 'proof_definitions':{label:{'installable_definition_id':c._wire(definition.id),'canonical_body_content_id':descriptor['content_id'],'native_contract_id':i.descriptor(definition)[1]['contract']['id']} for label,definition,descriptor in zip(('slot','root'),proof_defs,slots)}}
 result={'WORK_PACKAGE':'FINISH-F03','RESULT':'PASS',
 'SELECTED_SEMANTIC_OPTION':'AUTHORIZE_P04_A13_SUPPORT_SEMANTICS','SELECTED_INSTALL_OPTION':'AUTHORIZE_P04_A13_CONFIGURATION_INSTALLATION',
 'SEMANTIC_AUTHORIZATION':'PASS','INSTALL_AUTHORIZATION':'PASS',
 'SEMANTIC_AUTHORITY_ADMISSION':'PASS','SEMANTIC_AUTHORITY_APPLICABILITY':'PASS',
 'INSTALL_AUTHORITY_ADMISSION':'PASS','INSTALL_AUTHORITY_APPLICABILITY':'PASS',
 'authenticated_authorization':read('authenticated-decisions.json'),
 'semantic_authority':c._wire(config.request.authority_bindings[0]),
 'install_authorities':{str(index):c._wire(c._unwire(read('install-request-'+str(index)+'.json')).authority) for index in range(4)},
 'A13_ADAPTERS':'PASS','A13_INSTALLATION':'PASS_PREEXECUTION_STEPS_1_2',
 'generic_qualification':qual,'adapter_inventory':{
 'ROOT_SLOT_CONFIGURATION_SET':'NEW: native source/semantic-reference/slot/root registry; no concrete proof or lifecycle instance',
 'SLOT_PROOF_CONTRACT_DEFINITION':'NEW: exact presealed contract activates only on actual/current completed REENTER knowledge',
 'ROOT_PROOF_CONTRACT_DEFINITION':'NEW: exact presealed contract activates only on sole usable accepted slot proof and independent source',
 'ACTION_DEFINITION':'EXISTING I05: FINISH REPLACE changes only prerequisites and blocked_terminal'},
 'POST_A13_CONFIG_STATE_ID':identity(man['state_id']),'POST_A13_CONFIG_APPEND_HEAD':identity(man['head']),
 'POST_A13_CONFIG_LEDGER_ROOT':i.simple(b.events[0].identity),
 'configuration_bundle':man,'configuration_trace':read('configuration-trace.json'),
 'P04_A13_SOURCE_ID':body['source_entity_definitions'][1]['id']['value'],
 'P04_SLOT_DEFINITION_ID':c._wire(b.current.slots[0].id),'P04_ROOT_DEFINITION_ID':c._wire(b.current.roots[0].id),
 'P04_SLOT_PROOF_DEFINITION_ID':c._wire(proof_defs[0].id),'P04_ROOT_PROOF_DEFINITION_ID':c._wire(proof_defs[1].id),
 'identity_domains':identity_domains,
 'SOURCE_CURRENTNESS':'PASS','ROOT_SOURCE_INDEPENDENCE':'PASS',
 'currentness':{'source_configuration':'CURRENT','semantic_policies':'CURRENT/APPLICABLE','FINISH_definition':'CURRENT','slot_root_prospective_declarations':'CANONICAL_IN_INSTALLED_CONFIGURATION',
 'concrete_slot_contract':'PRESEALED; DEFERRED_UNTIL_ACTUAL_POST_A12','concrete_root_contract':'PRESEALED; DEFERRED_UNTIL_ACTUAL_POST_SLOT_PROOF'},
 'A09_READY':'YES','A10_READY':'YES','A11_READY':'YES','A12_READY':'YES','A13_READY':'YES',
 'a09_precommit':a09,'isolated_lifecycle':life,'execution_trace':read('isolated-execution-trace.json'),
 'SLOT_PROOF_ADMISSION':'PASS','E2_SLOT_STATE':'RESOLVED (isolated qualification)',
 'ROOT_PROOF_ADMISSION':'PASS','E2_ROOT_STATE':'SATISFIED (isolated qualification)',
 'FINISH_REEVALUATION':'PASS','FINISH_EXECUTION':'PASS (isolated qualification only)',
 'FINISH_RESULT':'PASS + E2-K-FINISH','E2_K_FINISH':'ADMITTED/CURRENT (isolated qualification)',
 'P04_EXIT_PREDICATE':True,'p04_exit_role':'ISOLATED_TARGET_QUALIFIED; canonical P04 not executed',
 'NEGATIVE_SUITE':'PASS','f02_negatives':negatives,'additional_native_negatives':life['negative_cases'],
 'INVALIDATION':'PASS','invalidations':life['invalidations'],
 'PERSISTENCE':'PASS','COLD_RESTORE':'PASS','REPLAY':'PASS','DETERMINISM':'PASS',
 'readers':{'P04_checks':132,'generic_checks':12,'seeds':[0,1,7,101],'readers_per_boundary_per_seed':3,'P04_boundaries':11,'results':ref('fresh-reader-results.json'),'generic_results':ref('generic-fresh-reader-results.json')},
 'independent_reproductions':reproductions,'unordered_permutations':perms,'boundary_oracles':bounds,
 'A13_NATIVE_PATH_QUALIFIED':'PASS','P04_EXECUTION_READY':'YES','E2_P04_READY':'YES',
 'NEXT_PACKAGE':'CANONICAL E2-P04 A09-A13 EXECUTION',
 'CANONICAL_A09_A13_EXECUTED':'NO','E2_FINISH_EXECUTED':'NO','RESUME_ELIGIBILITY_PERSISTED':'NO_IN_CANONICAL_STATE',
 'P03_RESULT':'PASS','P03_HISTORICAL_CORRESPONDENCE':'UNPROVEN','N_REAL_SATISFIED':'NO','CANONICAL_E2_QUALIFIED':'NO',
 'E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO','git_diff_check':'PASS',
 'regressions':{'targeted_tests':95,'groups':{name:{'log':ref(file),'tests':count,'result':'PASS'} for name,(file,count) in logs.items()},
 'broad_suite':'NOT_RERUN; prior frozen-E1 duplicate-import collection blocker remains separate; no broad-suite PASS claimed',
 'legacy_admission':'Prior three legacy Evidence-admission fixture failures remain separate; not relabeled as current-path passes'},
 'preservation':{'preexisting_files_checked':len(baseline),'modified_preexisting_files':changed,'all_prior_plan_qualification_artifacts_unchanged':True,'E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO','git_diff_check':'PASS'},
 'qualification_report_repairs':{'compact_source_body':'Typed adapter fills only inert native SOURCE defaults; sealed bytes unchanged; requalified before canonical installation',
 'report_writes':'Qualification evidence writes atomic; native bundle/HEAD atomicity unchanged',
 'computed_proof_reporting':'Read-only native Proof encoded as comparison evidence; closed persistence codec unchanged; four full corrected reproductions required',
 'intermediate_control':'Explicit human clarification retains the sealed F02 PLAN_DEFECT oracle; no control/goal rewrite'}}
 output=D/(P+'FINISH_F03_RESULT.json');output.write_bytes(c.canonical_bytes(result));q.emit('preservation.json',result['preservation'])
 selected='\n'.join('A'+str(stage).zfill(2)+'_READY = YES' for stage in range(9,14))
 text=f'''# Deterministic Planner v0.1 — FINISH-F03

**RESULT = PASS. P04_EXECUTION_READY = YES.** The exact F02 configuration is installed in the canonical preexecution lineage. The full A09–A13 path reaches the qualified P04 target in isolated native execution. Canonical A09–A13 and FINISH remain unexecuted.

The [machine-readable result](./{P}FINISH_F03_RESULT.json) records the authenticated decisions, adapter qualification, installation events, all boundary comparisons, negative cases, process evidence and preservation. The [native final preexecution bundle](./{Path(man['path']).name}) is the canonical input for the next package, **CANONICAL E2-P04 A09-A13 EXECUTION**. This is readiness evidence; canonical P04, P05/P06 and aggregate release qualification are not claimed.

Both selected options bind the unchanged [F02 sealed manifest](./qualification/FINISH_F02_1/sealed-manifest.json), semantic/source request and INSTALL workflow. The authenticated semantic DECIDE witness is separate from four exact single-use INSTALL grants. Preexecution applies only workflow steps 1–2. Steps 3–4 are authorized conditional A13 preparation and were qualified in isolation after their actual support boundaries. INSTALL never admits a proof instance or executes an Action.

Your clarification, “retain that sealed oracle and qualify the remaining path,” resolves F03's conflicting no-PLAN_DEFECT clause. The original F02 oracle remains unchanged: PLAN_DEFECT after REENTER and slot proof; RUNNABLE after root proof; TERMINAL_SUCCESS after FINISH. Goals and control semantics were preserved.

| Canonical configuration identity | Value |
|---|---|
| Bundle | `{identity(man['bundle_id'])}` |
| State | `{identity(man['state_id'])}` |
| Append head | `{identity(man['head'])}` |
| Native ledger anchor | `{b.events[0].identity.namespace}:{b.events[0].identity.sha256}` |
| Events | 7 retained I05 events + 2 authorized configuration events |

The native bundle has no separate Merkle-root/LedgerId field; the recorded ledger anchor is its first native event, matching existing installation evidence. Its complete historical prefix, source/policy pins and scope/lineage remain intact.

The new generic adapters install source/slot/root configuration and deferred typed proof contracts. They validate canonical native bodies, independently authenticated semantic references, content pins, context and live support. The existing I05 Action adapter changes FINISH only by adding its root prerequisite and making the prerequisite hold nonterminal. Its PASS/E2-K-FINISH inventory is unchanged. Currentness and invalidation hooks connect canonical source entities to their owned concrete proof roles; unrelated legacy E06 targets retain their qualified path.

Prospective declarations are canonical in the installed configuration. Concrete SLOT_PROOF and ROOT_PROOF contracts remain deferred in canonical state until their sealed activation conditions hold. Actual current completed REENTER knowledge must equal the sealed permitted output and support fingerprint before slot-contract installation. The sole expected usable slot proof and independent current root source must match before root-contract installation. No contract bytes are discovered or changed after execution.

Root-source independence checks exact distinct role, identity, proposition, provenance origin and independently pinned source/policy bindings. A different hash alone is insufficient. PC02 supplies declaration precedent; its old-lineage issued authority is not reused. The sources are bounded qualification declarations, never assertions of current satisfaction or real-world facts.

| Isolated boundary | Result |
|---|---|
| A09 | All 18 received-only postconditions PASS; validation NOT_EVALUATED, no proof/resume/completion |
| A10 | Accepted ValidationResult and support; no A11 event or REENTER execution |
| A11 | Computed obligation Proof, both required native reentry events and fresh C03 eligibility PASS |
| A12 | Native selected permitted PASS/E2-K-REENTER result admitted; actual output current |
| Slot contract / proof | Exact deferred activation; proof accepted; slot RESOLVED; root unresolved; FINISH held |
| Root contract / proof | Independent source/support checks PASS; root SATISFIED; E06 reevaluation selects FINISH |
| FINISH / P04 target | Actual permitted PASS/E2-K-FINISH admitted/current; all six Actions completed; all declared goals proven; TERMINAL_SUCCESS |

[Eight sealed boundary comparisons](./qualification/FINISH_F03_1/boundary-comparisons.json), [30 F02 negative cases](./qualification/FINISH_F03_1/f02-negative-results.json), 24 additional native controls and support/source/authority invalidation pass. Historical proofs/results remain auditable after invalidation; live readiness is withdrawn and completed FINISH cannot execute again. No unrelated Action reopens. Computed A11 Proof/ResumeEligibility is comparison evidence, never a persisted permission or new lifecycle instance.

95 targeted tests pass: six new generic adapter tests, 52 affected ingress/validation/authentication tests, 33 INSTALL/Action/proof tests and four E06 regressions. [132 fresh P04 reader comparisons](./qualification/FINISH_F03_1/fresh-reader-results.json) cover 11 persisted boundaries, three readers each under seeds 0/1/7/101; 12 generic reader checks also pass. Writers terminate before readers restore. Native source/event verification, canonical identities, currentness, full Computation, obligation Proof and C03 outputs agree. Four corrected independent full reproductions and reversed/rotated native-declared unordered collections at nine lifecycle checkpoints pass. Causal event order is preserved.

Initial application exposed omitted inert native SOURCE defaults in the sealed prospective representation. The typed adapter supplies only empty permissions and null target/validator plus unconsumed state, leaving all sealed bytes unchanged; generic qualification was rerun before successful application. Qualification-only report repairs fixed concurrent evidence writes and read-only computed Proof reporting. Earlier attempt logs are retained; neither repair changes canonical identity or the persistence codec. Only completed corrected runs contribute PASS evidence.

The broad suite was not rerun. The previously recorded frozen-E1 duplicate-import collection blocker and three legacy Evidence-admission fixture failures remain separate; no broad-suite PASS is claimed. All {len(baseline)} baseline files were checked. Only the two expected existing runtime files changed; the new adapter and qualification utilities are additional files. All earlier plan/qualification artifacts, the P03 checkpoint/qualification and frozen E1 remain unchanged. `git diff --check = PASS`.

```text
WORK_PACKAGE = FINISH-F03
RESULT = PASS
SELECTED_SEMANTIC_OPTION = AUTHORIZE_P04_A13_SUPPORT_SEMANTICS
SELECTED_INSTALL_OPTION = AUTHORIZE_P04_A13_CONFIGURATION_INSTALLATION
SEMANTIC_AUTHORIZATION = PASS
INSTALL_AUTHORIZATION = PASS
A13_ADAPTERS = PASS
A13_INSTALLATION = PASS (PREEXECUTION STEPS 1–2)
SOURCE_CURRENTNESS = PASS
ROOT_SOURCE_INDEPENDENCE = PASS
{selected}
SLOT_PROOF_ADMISSION = PASS (ISOLATED)
E2_SLOT_STATE = RESOLVED (ISOLATED)
ROOT_PROOF_ADMISSION = PASS (ISOLATED)
E2_ROOT_STATE = SATISFIED (ISOLATED)
FINISH_REEVALUATION = PASS
FINISH_EXECUTION = PASS (ISOLATED)
FINISH_RESULT = PASS + E2-K-FINISH (ISOLATED)
E2_K_FINISH = ADMITTED/CURRENT (ISOLATED)
P04_EXIT_PREDICATE = TRUE (ISOLATED QUALIFICATION)
NEGATIVE_SUITE = PASS
INVALIDATION = PASS
PERSISTENCE = PASS
COLD_RESTORE = PASS
REPLAY = PASS
DETERMINISM = PASS
A13_NATIVE_PATH_QUALIFIED = PASS
P04_EXECUTION_READY = YES
E2_P04_READY = YES
NEXT_PACKAGE = CANONICAL E2-P04 A09-A13 EXECUTION
CANONICAL_A09_A13_EXECUTED = NO
E2_FINISH_EXECUTED = NO
P03_RESULT = PASS
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO
CANONICAL_E2_QUALIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
'''
 (D/(P+'FINISH_F03_RESULT.md')).write_text(text)
 print('F03_PASS P04_EXECUTION_READY=YES PRESERVATION=PASS')
if __name__=='__main__':run()
