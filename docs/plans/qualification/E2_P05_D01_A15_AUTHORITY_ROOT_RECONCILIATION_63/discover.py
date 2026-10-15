"""Bounded read-only authority-root discovery; no native modules/operations."""
import pathlib,json,hashlib
P=pathlib.Path('docs/plans');Q=P/'qualification';E=pathlib.Path(__file__).parent;B=Q/'E2_P05_D01_A15_BOUNDED_AUTHORITY_QUALIFICATION_62';A=Q/'E2_P05_D01_A15_CAPTURE_PERSISTENCE_RESUME_CLOSURE_61'
def read(p):return json.loads(pathlib.Path(p).read_text())
def digest(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def pin(p):return {'PATH':str(p),'RAW_SHA256':digest(p)}
def save(n,x):(E/n).write_text(json.dumps(x,sort_keys=True,indent=2,ensure_ascii=False)+'\n')
sealed=read(B/'evidence-index.json')['FILES'];assert all(digest(p)==h for p,h in sealed.items())
assert all(digest(p)==h for p,h in read(A/'evidence-index.json')['FILES'].items())
subject=read(B/'authority-subject-manifest.json')['TECHNICAL_PREPARATION_IDENTITY'];cp=read(B/'checkpoint-ledger-verification.json');checkpoint=read(cp['NATIVE_CHECKPOINT_ARTIFACT']['PATH'])['bundle'];ctx=checkpoint['current']['context']
# Root candidates are scope-bearing instruments/records, not every occurrence
# duplicated inside historical bundle snapshots or negative-control fixtures.
files=[
 ('E2_DECISION_PROTOCOL',P/'DETERMINISTIC_PLANNER_V0_1_E2_P02_SYNTHETIC_HUMAN_DECISION_PROTOCOL_1.json'),
 ('E2_PROOF_AUTHORITY_INVENTORY',P/'DETERMINISTIC_PLANNER_V0_1_E2_P01_PROOF_AUTHORITY.json'),
 ('ROOT_SLOT_DESIGN_DOSSIER',P/'DETERMINISTIC_PLANNER_V0_1_E2_PC02_ROOT_SLOT_FIXTURE_AUTHORITY_1.json'),
 ('ROOT_SLOT_SEMANTIC_REQUEST',Q/'FINISH_F02_1/semantic-authority-request.json'),
 ('ROOT_SLOT_HUMAN_DECISIONS',Q/'FINISH_F03_1/authenticated-decisions.json'),
 ('ATTEST_HUMAN_DECISION',Q/'INSTALLATION_I04_1/authenticated-human-decision.json'),
 ('OPERATING_ATTEST_GRANT',Q/'INSTALLATION_I04_1/issued-operating-attest-grant.json'),
 ('OPERATING_ATTEST_ADMISSION',Q/'INSTALLATION_I04_1/operating-authority-admission.json'),
 ('INSTALL_GRANT',Q/'INSTALLATION_I02_1/issued-install-grant.json'),
 ('INSTALL_ADMISSION',Q/'INSTALLATION_I02_1/install-authority-admission.json'),
 ('A04_SCOPE_DECISION',Q/'E2_P05_A04_PROSPECTIVE_ANCESTRY_CONTRACT_1/authenticated-scope-decision.json'),
 ('A04_AUTHORITY_ASSESSMENT',Q/'E2_P05_A04_PROSPECTIVE_ANCESTRY_CONTRACT_1/authority.json'),
 ('END_SCOPE_DECISION',Q/'E2_P05_COMPOSITE_END_QUALIFICATION_1/scope-authentication.json'),
 ('P05_AUTHORITY_READINESS',Q/'E2_P05_READINESS_1/authority-inventory.json'),
 ('END_INTERFACE_AUTHORITY_REQUIREMENT',Q/'E2_P05_END_INTERFACE_CLOSURE_1/PC01-authority-requirement.json'),
 ('A14_RUNTIME_SCOPE',Q/'E2_P05_D01_A14_RUNTIME_PERSISTENCE_QUALIFICATION_31/scope-authentication.json'),
 ('A14_RUNTIME_DOSSIER',Q/'E2_P05_D01_A14_RUNTIME_PERSISTENCE_CONTRACT_30/bounded-execution-decision-dossier.json'),
 ('A15_NORMATIVE_SCHEMA',Q/'E2_P05_D01_A15_NORMATIVE_KNOWLEDGE_CONTRACT_42/normative-knowledge-schema.json'),
 ('A15_AUTHORITY_PREPARATION',A/'authority-preparation-eligibility.json'),
 ('E1_CONTINUATION_DELEGATION',pathlib.Path('docs/experiments/E1/a2_1i_enrollment_qualification_2026-09-19/ARCHITECT_DELEGATION_SOURCE.md'))]
# A missing catalog file is recorded, never replaced by a semantically nearby one.
# Actual admission filename is discovered by exact grant-declared native family.
files=[(kind,p) for kind,p in files if kind!='OPERATING_ATTEST_ADMISSION']
for p in sorted((Q/'INSTALLATION_I04_1').glob('*admission*.json')):
 schema=read(p).get('schema');assert schema in ('PLANNER-ATTEST-DEFINITION-ADMISSION-1','PLANNER-INSTALL-AUTHORITY-ADMISSION-1')
 files.append(('OPERATING_ATTEST_ADMISSION' if schema=='PLANNER-ATTEST-DEFINITION-ADMISSION-1' else 'INSTALL_ADMISSION',p))
for p in sorted(Q.glob('E2_P05_D01_A14_*/scope-authentication.json')):
 if p not in [f for _,f in files]:files.append(('A14_SCOPE_DECISION',p))
for p in sorted((Q/'FINISH_F03_1').glob('install-authority-*.json')):files.append(('P04_INSTALL_ADMISSION',p))
assert all(p.is_file() for _,p in files)
records=[]
for kind,p in files:
 raw=p.read_text();value=read(p) if p.suffix=='.json' else {'EXACT_TEXT':raw}
 records.append({'KIND':kind,'SOURCE':pin(p),'SOURCE_POINTER':'/','RECORD':value})
# Exact current native entities are evidence of narrower accepted grants, not
# evidence of the rights of their historical issuer over new A15 subjects.
for i,entity in enumerate(checkpoint['current']['entities']):
 if entity['kind']['value']=='AUTHORITY':records.append({'KIND':'NATIVE_CHECKPOINT_AUTHORITY','SOURCE':pin(cp['NATIVE_CHECKPOINT_ARTIFACT']['PATH']),'SOURCE_POINTER':'/bundle/current/entities/'+str(i),'RECORD':entity})
# Follow grant/decision provenance explicitly; do not infer or issue delegation.
support=[]
for p in [Q/'FINISH_F02_1/root-semantic-policy.json',Q/'FINISH_F02_1/slot-semantic-policy.json',Q/'FINISH_F02_1/sealed-manifest.json',Q/'FINISH_F02_1/install-authority-request.json',P/'DETERMINISTIC_PLANNER_V0_1_E2_P03_T01_TRUST_ANCESTRY_CLOSURE_1.json',P/'DETERMINISTIC_PLANNER_V0_1_E2_P02_DECISION_AUTHORITY_MATERIALIZATION_CLOSURE_1.json',Q/'E2_P05_D01_SOURCE_BYTES_DISPATCH_CORRECTION_33/authority-analysis.json',pathlib.Path('adapter/planner/authentication_installation.py'),pathlib.Path('adapter/planner/installation.py'),pathlib.Path('adapter/temporal_authority.py'),pathlib.Path('adapter/authority_bootstrap.py'),pathlib.Path('adapter/authority_profile.py')]:support.append(pin(p))
for r in records:
 if r['KIND']=='NATIVE_CHECKPOINT_AUTHORITY':support.append(pin(r['RECORD']['provenance']['path']))
input_hashes=dict(sealed);input_hashes.update(read(B/'authentication.json')['FILES']);input_hashes.update({x['SOURCE']['PATH']:x['SOURCE']['RAW_SHA256'] for x in records});input_hashes.update({x['PATH']:x['RAW_SHA256'] for x in support});input_hashes[str(B/'evidence-index.json')]=digest(B/'evidence-index.json');input_hashes[str(A/'evidence-index.json')]=digest(A/'evidence-index.json')
assert all(digest(p)==h for p,h in input_hashes.items())
save('authentication.json',{'PACKAGE_62_AUTHENTICATED':True,'PACKAGE_62_SEALED_FILES':len(sealed),'PACKAGE_61_SEALED_FILES':40,'FILES':input_hashes,'MISMATCHES':[],'TARGET_SUBJECT':subject})
save('retained-authority-source-catalog.json',{'TARGET_SUBJECT':subject,'TARGET_CHECKPOINT':cp['SNAPSHOT_IDENTITY'],'NATIVE_CONTEXT':ctx,'RECORDS':records,'SUPPORTING_RULE_SOURCES':support,'SEARCH_SCOPE':'Named E2 human protocols, native checkpoint authority entities, P04 install/ATTEST/root-slot instruments, P05/END/A04 decisions, all retained A14 scope-authentication records, Contract42/Package61 requirements and one explicit E1 delegation. No assertion that external or unretained authority sources do not exist.','SEARCH_METHOD':'rg --files for authority/grant/issuer/trust/delegation/decision paths; source-referenced scoped records; exclude duplicate snapshot embeddings and test-negative fixtures','SCHEMA_AND_AUTHORITY_VERSION_DISTINCT':True})
print(json.dumps({'AUTHORITY_CANDIDATE_RECORDS':len(records),'FAMILIES':sorted({r['KIND'] for r in records}),'SUPPORT_RULE_SOURCES':len(support)}))
