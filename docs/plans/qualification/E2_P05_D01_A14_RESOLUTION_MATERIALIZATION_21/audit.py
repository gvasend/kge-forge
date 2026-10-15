"""Sealed static handoff reentry and all 111 references; no case invocation."""
import hashlib,json,ast,runpy
from pathlib import Path
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;Q=O.parent;C4=Q/'E2_P05_D01_OPERAND_RECONCILIATION_4';C5=Q/'E2_P05_D01_A14_HANDOFF_CLOSURE_5';C20=Q/'E2_P05_D01_A14_RESOLUTION_SOURCE_RECOVERY_20';C2=Q/'E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2'
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):return {'path':str(p.relative_to(R)),'raw_sha256':sha(p.read_bytes())}
def save(n,v):(O/n).write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
runpy.run_path(str(C4/'verify.py'),run_name='__frozen_52_metadata_verify__')
closure=read(O/'complete-source-validation.json');assert closure['STATUS']=='PASS' and closure['SOURCE_PINS_PRESENT']==10
plan=read(C20/'a14-handoff-reentry-oracle.json');assert [x['STEP'] for x in plan['ORDERED_STEPS']]==list(range(1,9))
for row in plan['ORDERED_STEPS']:
 if 'CONTRACT' in row:assert sha((R/row['CONTRACT']['path']).read_bytes())==row['CONTRACT']['raw_sha256']
bundle=read(C5/'bundle-contract.json');savecontract=read(C5/'save-contract.json');reader=read(C5/'cold-reader-contract.json');inventory=read(C5/'bundle-source-inventory.json')
assert inventory['SOURCE_SELECTION']=='NO_NATIVE_BUNDLE_SELECTED' and not inventory['UNIQUE_ELIGIBLE_RETAINED_BUNDLE']
for candidate in inventory['CANDIDATES']:
 p=candidate.get('SOURCE') or candidate.get('source')
 if p:assert sha((R/p['path']).read_bytes())==p['raw_sha256']
missing=['Exact native PersistenceBundle or sealed deterministic construction rule for corrected prospective A14 boundary','Authoritative initial Snapshot and ordered event history; cannot assume empty history','Exact applicable policy ArtifactPin and policy_version','Explicit replay bundle scope distinct from Snapshot context scope','Ledger root/head from legitimate ordered history where required','Complete dossier materialization/archive requirements where historical event results require them']
boundary=read(O/'pre-materialization-snapshot-oracle.json');checks={'CURRENT_CORRECTED_SNAPSHOT':'PASS','CURRENT_SNAPSHOT_PHYSICAL_SOURCE_SET':'PASS_10_OF_10','INITIAL_SNAPSHOT':'UNSEALED','ORDERED_HISTORY':'UNSEALED','POLICY_PIN_AND_VERSION':'UNSEALED','REPLAY_SCOPE':'UNSEALED','LEDGER_ROOT_HEAD':'UNSEALED_HISTORY_NOT_SELECTED','CURRENT_SCOPE_LINEAGE_PROVENANCE':'PASS','BUNDLE_NATIVE_TYPE_AND_IDENTITY':'NO_EXACT_INPUT_AVAILABLE'}
block={'CLASSIFICATION':'BUNDLE_CONTRACT','REASON':'Current A14 input is a corrected source-complete Snapshot, not an authoritative native PersistenceBundle. No exact initial/history/policy/replay-scope binding or sealed pure construction rule is selected.','MISSING_TERMS':missing,'SOURCE_BYTES_BLOCKER_CLOSED':True,'REPAIRED':False}
save('a14-bundle-preflight.json',{'STATUS':'FAIL','BUNDLE_CONTRACT':pin(C5/'bundle-contract.json'),'PREVIOUS_SOURCE_INVENTORY':pin(C5/'bundle-source-inventory.json'),'SNAPSHOT_IDENTITY':boundary['PRE_MATERIALIZATION_SNAPSHOT_ID'],'CHECKS':checks,'FIRST_NON_SOURCE_BLOCKER':block,'NO_EMPTY_HISTORY_OR_POLICY_DEFAULT_ASSUMED':True,'NO_NATIVE_BUNDLE_CONSTRUCTED':True,'NOTE':'Old source contradiction is superseded only for current corrected Snapshot. Old candidate Snapshot/history claims and genesis-bundle identity remain unchanged and cannot substitute for a complete native bundle.'})
resolved=read(C4/'resolved-bindings.json');known=resolved['PRESERVED_39']+resolved['NEW_BINDINGS'];remaining=read(C4/'remaining-frontier.json')['ROWS'];deps=read(C5/'a14-dependency-inventory.json')['ROWS'];assert len(known)==52 and len(remaining)==59 and len(deps)==16
def key(r):return (r['OBLIGATION_ID'],r['DISPATCH_ID'],r['CAPSULE_ID'],r['OPERAND_NAME'])
assert len({key(r) for r in known+remaining})==111
depmap={key(r):r for r in deps};catalog=read(C2/'fixture-catalog.json');drafts=read(C4/'reconciled-invocation-drafts.json');assert drafts['ROW_COUNT']==128
rows=[]
for r in known:rows.append({'REFERENCE_KEY':list(key(r)),'STATUS':'RESOLVED_FROZEN','ORIGINAL_BINDING':r,'RECONSTRUCTION':'PASS_C4_INDEPENDENT_RECONSTRUCTION','PROMOTED_THIS_PACKAGE':False})
affected=[]
for r in remaining:
 cap=catalog[r['CAPSULE_ID']];p=cap['artifact'];assert sha((R/p['path']).read_bytes())==p['raw_sha256'];packet=read(R/p['path'])
 for p in r['PROVENANCE']:assert sha((R/p['path']).read_bytes())==p['raw_sha256']
 if key(r) in depmap:
  if r['OPERAND_NAME']=='bundle':status='STILL_BLOCKED_BY_BUNDLE';reason='Ten current sources present; exact native initial/policy/history/scope bundle inputs remain absent'
  elif r['OPERAND_NAME']=='bundle_path':status='STILL_BLOCKED_BY_READER';reason='No sealed native bundle/save-return artifact path; report path cannot substitute'
  elif r['OPERAND_NAME']=='expected_bundle_identity':status='STILL_BLOCKED_BY_SAVE';reason='No complete bundle bytes or trusted save/precommit identity; Snapshot identity is not bundle identity'
  else:status='OTHER';reason=r['EXACT_ROOT_CAUSE']+'; required A14 post-restore or unknown-rule base still unavailable'
  affected.append({'REFERENCE_KEY':list(key(r)),'ORIGINAL_REFERENCE':depmap[key(r)],'STATUS':status,'REASON':reason,'SOURCE_DEPENDENCY_SATISFIED':True,'FULL_BINDING_SATISFIED':False})
 else:status='OTHER';reason=r['EXACT_ROOT_CAUSE']+'; current A14 ten-pin closure does not uniquely seal this separate source/mutation/phase operand'
 # Recheck actual dispatch operand position against the sealed 128-row draft.
 drow=next(x for x in drafts['ROWS'] if x['OBLIGATION_ID']==r['OBLIGATION_ID']);variant=next(x for x in drow['VARIANTS'] if x['CAPSULE_ID']==r['CAPSULE_ID']);step=variant['INVOCATION_STEPS'][r['STEP']];contract=step['ENTRYPOINT_CONTRACT'];assert sha((R/contract['SOURCE']['path']).read_bytes())==contract['SOURCE']['raw_sha256']
 assert r['REQUIRED_BY_ENTRYPOINT']==contract['NATIVE_ENTRYPOINT']
 rows.append({'REFERENCE_KEY':list(key(r)),'STATUS':status,'ORIGINAL_REFERENCE':r,'CAPSULE_LOAD_AND_HASH':'PASS','ENTRYPOINT_CONTRACT_PIN':'PASS','REQUIRED_BY_ENTRYPOINT':contract['NATIVE_ENTRYPOINT'],'SOURCE_CLOSURE_APPLICABLE':key(r) in depmap,'REASON':reason,'PROMOTED_THIS_PACKAGE':False})
assert len(affected)==16 and len(rows)==111
save('a14-dependent-reference-audit.json',{'A14_DEPENDENT_REFERENCES':16,'A14_REFERENCES_RESOLVED':0,'ROWS':affected,'COUNTS':{s:sum(r['STATUS']==s for r in affected) for s in sorted({r['STATUS'] for r in affected})}})
save('full-111-reference-audit.json',{'AUDITED_REFERENCES':111,'ROWS':rows,'PREVIOUSLY_RESOLVED':52,'RESOLVED_BY_10_OF_10_SOURCE_CLOSURE':0,'RESOLVED_BY_HANDOFF_REENTRY':0,'TOTAL_RESOLVED':52,'TOTAL_UNRESOLVED':59,'FROZEN_52_BYTE_SEMANTIC_PRESERVATION':'PASS','128_ROW_DRAFT_LOADED':True,'INVOCATION_STATIC_PREFLIGHT':'NOT_RUN','FULL_OUTPUT_ORACLES':'0/128'})
save('static-handoff-reentry.json',{'SEALED_PLAN':pin(C20/'a14-handoff-reentry-oracle.json'),'ORDERED_RESULTS':[{'STEP':1,'TERM':'complete current physical source set','STATUS':'PASS'},{'STEP':2,'TERM':'native prospective A14 bundle','STATUS':'FAIL','BLOCKER':block},{'STEP':3,'TERM':'save contract preflight','STATUS':'NOT_RUN_UPSTREAM_BUNDLE_FAIL','CONTRACT_INSPECTED':pin(C5/'save-contract.json')},{'STEP':4,'TERM':'writer termination preflight','STATUS':'NOT_RUN_UPSTREAM_BUNDLE_FAIL','CONTRACT_INSPECTED':pin(C5/'cold-reader-contract.json')},{'STEP':5,'TERM':'cold-reader persisted source/operands','STATUS':'NOT_RUN_UPSTREAM_BUNDLE_FAIL'},{'STEP':6,'TERM':'16 dependent reference audit','STATUS':'PASS_AUDIT_ONLY_NONE_RESOLVED'},{'STEP':7,'TERM':'111 reference audit','STATUS':'PASS_AUDIT_ONLY_52_RESOLVED_59_UNRESOLVED'},{'STEP':8,'TERM':'first remaining non-source blocker','STATUS':'IDENTIFIED_BUNDLE_CONTRACT'}],'A14_BUNDLE_PREFLIGHT':'FAIL','SAVE_CONTRACT_PREFLIGHT':'NOT_RUN','WRITER_TERMINATION_PREFLIGHT':'NOT_RUN','COLD_READER_PREFLIGHT':'NOT_RUN','FIRST_NON_SOURCE_BLOCKER':block,'SAVE_NATIVE_ENTRYPOINT':savecontract['ENTRYPOINT'],'READER_NATIVE_ENTRYPOINT':reader['ENTRYPOINT'],'SAVE_EXECUTED':False,'WRITER_TERMINATED':False,'QUALIFICATION_READER_LAUNCHED':False})
print(json.dumps({'SOURCE_CLOSURE':'PASS_10/10','BUNDLE_PREFLIGHT':'FAIL','FIRST_NON_SOURCE_BLOCKER':'BUNDLE_CONTRACT','AUDIT':'111/111','COUNTS':'52/59','A14_REFERENCES':'16/16_AUDITED_0_RESOLVED'}))
