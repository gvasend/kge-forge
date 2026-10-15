"""Issue documentary normative adoption only, with fail-closed ordered verification."""
import copy, importlib.util, json, os, pathlib, subprocess, sys, tempfile, hashlib
D=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('independent',D/'verify.py'); v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
ROOT=v.ROOT
WP='E2-P05-D01-A15-NORMATIVE-ADOPTION-ISSUANCE-68'
def publish(name,value):
 p=D/name; assert not p.exists() and not p.is_symlink(),str(p)
 data=value.encode() if isinstance(value,str) else (json.dumps(value,indent=2,sort_keys=True,ensure_ascii=True)+'\n').encode()
 fd,tmp=tempfile.mkstemp(prefix='.publication-',dir=str(D))
 try:
  with os.fdopen(fd,'wb') as f: f.write(data);f.flush();os.fsync(f.fileno())
  os.link(tmp,str(p));os.unlink(tmp)
  fd=os.open(str(D),os.O_RDONLY|os.O_DIRECTORY)
  try: os.fsync(fd)
  finally: os.close(fd)
  assert p.read_bytes()==data
 finally:
  if os.path.exists(tmp): os.unlink(tmp)
 return p
# Snapshot all prior evidence and runtime sources before any issuance record.
prior={}
for area in ['docs/plans','adapter']:
 for p in (ROOT/area).rglob('*'):
  if p.is_file() and D not in p.parents and '__pycache__' not in p.parts:
   prior[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
if (D/'preservation-before.json').exists():
 assert v.read(D/'preservation-before.json')==prior, 'preissuance preservation snapshot differs'
else: publish('preservation-before.json',prior)
charter,dossier,subject=v.inputs(); audit=v.conflicts()
publish('pre-adoption-conflict-audit.json',audit)
publish('effective-charter-verification.json',{'RESULT':'PASS','METADATA_READER':'Package66 reader.py; documentary verification only','ORDERED_LIFECYCLE':charter['ORDERED_LIFECYCLE'],'GOVERNING_CHARTER':charter['CHARTER_CONTENT_IDENTITY'],'SCOPE':charter['SCOPE'],'EXCLUSIONS':charter['EXCLUSIONS']})
source='''# KGE-Forge — A15 Normative Adoption Issuance 68
WORK_PACKAGE: E2-P05-D01-A15-NORMATIVE-ADOPTION-ISSUANCE-68
Source: current conversation user-role instruction. No platform message ID, personal credential, signature, or timestamp is asserted.

The project owner explicitly selected:
AUTHORIZE_BOUNDED_PROSPECTIVE_A15_NORMATIVE_SCOPE

Exact normative subject:
CONTENT_IDENTITY/qualification-A15-normative-adoption-subject-v1:b83a133c612f690f433e64b4e4f2788369851466d850cfdb7a6fb135d6f8e30d
Effective governing charter:
CONTENT_IDENTITY/kge-forge-qualification-governance-charter-v1:d26962c58f17281173e965433dae63a941e078115f3dcc30e2a3512fa21812b8
Effective charter lifecycle identity:
CONTENT_IDENTITY/kge-forge-charter-lifecycle-record-v1:a27516baa0ab7f34a36a1130490b6cfa38c508975ca337e0824c8eac33715cbb
Exact technical preparation subject:
CONTENT_IDENTITY/qualification-A15-technical-preparation-subject-v1:befe07aacc6b4c4e203488bce731f265a0520cf145174dca33dbfb4e68b43e9b

Authorized scope (verbatim user excerpt):
Record and independently qualify the project owner's adoption of the exact prospective A15 normative semantics:
- Owner/source relationships.
- Requiredness and coverage rules.
- Two independent singleton variants.
- Protection policy.
- Qualification assurance limitations.
- Historical exclusions.
This is a normative qualification decision only.

Explicit prohibitions (verbatim user excerpt):
This decision does not authorize:
- Native invalidation.
- Execution of either A15 variant.
- apply_event or record_result.
- Capture, save, restore, or replay.
- Writer or cold-reader operations.
- Baseline modification.
- V3 or Planner runtime modification.
- E1 modification.
- Production or external-system effects.
No execution or capture grant may be inferred from normative adoption.

Effectiveness condition: mark the normative mandate effective only after successful persistence and independent verification, four-seed reconstruction and fail-closed negative controls.
'''
sourcepath=publish('project-owner-decision-source.txt',source)
dc={'SCHEMA_ID':'A15-OWNER-NORMATIVE-DECISION-1','SOURCE_KIND':'CURRENT_CONVERSATION_USER_MESSAGE','SOURCE_PIN':v.pin(sourcepath),'ISSUER_ROLE':dossier['ISSUER_ROLE'],'OPTION_ID':dossier['OPTIONS'][0]['OPTION_ID'],'MANDATE':'NORMATIVE_SCOPE_ONLY','NORMATIVE_SUBJECT':subject['IDENTITY'],'GOVERNING_CHARTER':dossier['CHARTER_CONTENT_IDENTITY'],'EFFECTIVE_LIFECYCLE':dossier['EFFECTIVE_CHARTER_RECORD_IDENTITY'],'TECHNICAL_SUBJECT':dossier['EXACT_A15_TECHNICAL_SUBJECT'],'OFFERED_DOSSIER_PIN':v.pin(v.P/'unselected-normative-scope-decision-dossier.json'),'PERSONAL_IDENTITY_OR_SIGNATURE_ASSERTED':False,'AUTHENTICATION_BOUNDARY':'Explicit current user project-owner declaration and selection under independently verified effective charter; no external credential authentication claimed'}
decision={'IDENTITY':v.identity('qualification-A15-owner-normative-decision-v1',dc),'CONTENT':dc}
publish('project-owner-decision.json',decision)
r={'SCHEMA_ID':'A15-NORMATIVE-ADOPTION-RECORD-1','WORK_PACKAGE':WP,'NORMATIVE_SUBJECT':subject['IDENTITY'],'NORMATIVE_SUBJECT_PIN':v.pin(v.P/'normative-adoption-subject.json'),'GOVERNING_CHARTER':dc['GOVERNING_CHARTER'],'EFFECTIVE_LIFECYCLE':dc['EFFECTIVE_LIFECYCLE'],'TECHNICAL_SUBJECT':dc['TECHNICAL_SUBJECT'],'OWNER_DECISION':decision['IDENTITY'],'OWNER_DECISION_PIN':v.pin(D/'project-owner-decision.json'),'ISSUER_ROLE':dc['ISSUER_ROLE'],'OPTION_ID':dc['OPTION_ID'],'MANDATE':'NORMATIVE_SCOPE_ONLY','ADOPTED_CONTENT':subject['CONTENT'],'STATUS':'ADOPTION_RECORDED_PENDING_INDEPENDENT_EFFECTIVENESS_VERIFICATION','EXECUTION_GRANT':None,'CAPTURE_GRANT':None,'PREDECESSOR_ADOPTION':None,'EFFECTIVENESS_RULE':'Only after immutable persistence, independent reread, four-seed agreement and all negative controls pass; no backdating','PROHIBITED_OPERATIONS':['native invalidation','apply_event','record_result','capture/save/restore/replay','writer/cold-reader operations','baseline amendment','V3/Planner runtime modification','E1 modification','production/external-system effects']}
record={'IDENTITY':v.identity('qualification-A15-normative-adoption-record-v1',r),'RECORD':r}
pre=v.verify(record,decision,sourcepath)
publish('prepublication-validation.json',pre)
recordpath=publish('normative-adoption-record-'+record['IDENTITY']['sha256']+'.json',record)
post=json.loads(subprocess.check_output([sys.executable,str(D/'verify.py')],cwd=str(ROOT)))
publish('independent-persisted-record-verification.json',post)
seeds=[]
for seed in [0,1,7,101]:
 env=dict(os.environ,PYTHONHASHSEED=str(seed)); out=json.loads(subprocess.check_output([sys.executable,str(D/'verify.py')],cwd=str(ROOT),env=env))
 assert out==post
 seeds.append({'PYTHONHASHSEED':seed,'RESULT':'PASS','SEMANTIC_SHA256':v.digest(out),'RECONSTRUCTION':out})
publish('four-seed-determinism.json',{'RESULT':'PASS','FRESH_DOCUMENTARY_VERIFIER_PROCESSES':4,'SEEDS':seeds,'NATIVE_OPERATIONS_INVOKED':False})
neg=[]
def reject(name,mutate=None,dm=None,duplicates=1):
 e=copy.deepcopy(record); d=copy.deepcopy(decision)
 if mutate: mutate(e['RECORD']);e['IDENTITY']=v.identity('qualification-A15-normative-adoption-record-v1',e['RECORD'])
 if dm: dm(d['CONTENT']);d['IDENTITY']=v.identity('qualification-A15-owner-normative-decision-v1',d['CONTENT'])
 try: v.verify(e,d,sourcepath,duplicates)
 except (AssertionError,KeyError,ValueError): neg.append({'CONTROL':name,'RESULT':'REJECTED'});return
 raise RuntimeError('negative accepted: '+name)
reject('wrong normative subject',lambda r:r['NORMATIVE_SUBJECT'].update(sha256='0'*64))
reject('wrong charter',lambda r:r['GOVERNING_CHARTER'].update(sha256='0'*64))
reject('wrong lifecycle',lambda r:r['EFFECTIVE_LIFECYCLE'].update(sha256='0'*64))
reject('wrong technical subject',lambda r:r['TECHNICAL_SUBJECT'].update(sha256='0'*64))
reject('wrong offered option',dm=lambda d:d.update(OPTION_ID='AUTHORIZE_EXECUTION'))
reject('wrong issuer role',dm=lambda d:d.update(ISSUER_ROLE='UNDELEGATED'))
reject('wrong owner provenance pin',dm=lambda d:d['SOURCE_PIN'].update(RAW_SHA256='0'*64))
reject('wrong offered dossier pin',dm=lambda d:d['OFFERED_DOSSIER_PIN'].update(RAW_SHA256='0'*64))
reject('wrong normative source pin',lambda r:r['NORMATIVE_SUBJECT_PIN'].update(RAW_SHA256='0'*64))
reject('execution mandate inferred',lambda r:r.update(EXECUTION_GRANT={'ISSUED':True}))
reject('capture mandate inferred',lambda r:r.update(CAPTURE_GRANT={'ISSUED':True}))
reject('expanded mandate',lambda r:r.update(MANDATE='COMBINED'))
reject('protection policy removed',lambda r:r['ADOPTED_CONTENT'].update(PROTECTION_POLICY={}))
reject('historical exclusions removed',lambda r:r['ADOPTED_CONTENT'].update(HISTORICAL_EXCLUSIONS={}))
reject('scope changed',lambda r:r['ADOPTED_CONTENT'].update(SCENARIO_BOUNDARY='ALL_E2'))
reject('duplicate adoption',duplicates=2)
reject('self authorizing predecessor',lambda r:r.update(PREDECESSOR_ADOPTION=record['IDENTITY']))
reject('premature effectiveness',lambda r:r.update(STATUS='EFFECTIVE'))
reject('native operations permitted',lambda r:r.update(PROHIBITED_OPERATIONS=[]))
publish('negative-controls.json',{'RESULT':'PASS','PASSED':len(neg),'TOTAL':len(neg),'CONTROLS':neg,'METHOD':'In-memory independently reidentified corrupt records; no issued evidence mutated'})
# Fail closed on previous evidence changes BEFORE effectiveness.
changed=[p for p,h in prior.items() if not (ROOT/p).exists() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
assert not changed,changed
pres={'RESULT':'PASS','PREEXISTING_FILES_VERIFIED':len(prior),'CHANGED_PREEXISTING_FILES':changed,'APPEND_ONLY_PUBLICATION':'exclusive hard-link publication, file and directory fsync, independent persisted reread','NATIVE_OPERATIONS_INVOKED':False,'E1_ARTIFACTS_MODIFIED':0,'PLANNER_RUNTIME_MODIFIED':False,'LESSONS_REGISTER_PRESERVED':True,'A14_PERSISTENCE_RERUN':False}
publish('preservation-audit.json',pres)
# Effective reference comes strictly after persisted, independent and four-seed validation.
effective={'SCHEMA_ID':'A15-EFFECTIVE-NORMATIVE-MANDATE-REFERENCE-1','NORMATIVE_MANDATE_EFFECTIVE':True,'ADOPTION_RECORD_IDENTITY':record['IDENTITY'],'ADOPTION_RECORD_PIN':v.pin(recordpath),'GOVERNING_CHARTER':dc['GOVERNING_CHARTER'],'EFFECTIVE_LIFECYCLE':dc['EFFECTIVE_LIFECYCLE'],'NORMATIVE_SUBJECT':subject['IDENTITY'],'OWNER_DECISION':decision['IDENTITY'],'MANDATE':'NORMATIVE_SCOPE_ONLY','EFFECTIVE_BOUNDARY':'Package68 exclusive publication of this reference after persisted adoption reread, four fresh deterministic reconstructions, 19 rejected corruptions and preservation verification; no prior or backdated effect','VERIFICATION_PINS':[v.pin(D/n) for n in ['independent-persisted-record-verification.json','four-seed-determinism.json','negative-controls.json','preservation-audit.json']],'A15_EXECUTION_AUTHORITY_ISSUED':False,'A15_CAPTURE_AUTHORITY_ISSUED':False,'A15_EXECUTED':False}
efpath=publish('effective-normative-mandate-reference.json',effective)
assert v.read(efpath)==effective
for p in effective['VERIFICATION_PINS']: assert hashlib.sha256((ROOT/p['PATH']).read_bytes()).hexdigest()==p['RAW_SHA256']
assert v.verify(v.read(recordpath),v.read(D/'project-owner-decision.json'),sourcepath)==post
publish('effective-reference-independent-verification.json',{'RESULT':'PASS','EFFECTIVE_REFERENCE_PIN':v.pin(efpath),'ADOPTION_VERIFIED_AGAIN':post,'ALL_PREREQUISITE_PINS_VALIDATED':True,'NO_EXECUTION_OR_CAPTURE_GRANT':True})
gaps=v.read(v.P/'remaining-gap-dossier.json')
publish('updated-authority-readiness.json',{'NORMATIVE_MANDATE_EFFECTIVE':True,'NORMATIVE_ADOPTION_PENDING':False,'EXECUTION_DECISION_READY':False,'CAPTURE_DECISION_READY':False,'COMBINED_EXECUTION_CAPTURE_READY':False,'RETAINED_RUNTIME_GAPS':gaps['GAPS'],'NEXT_BOUNDARY':'A15_EXECUTOR_AND_ENVIRONMENT_QUALIFICATION','OPERANDS':{'TOTAL':161,'RESOLVED':109,'UNRESOLVED':52},'END_INTERFACES_BOUND':'4/6','P05_EXECUTION_READY':False})
report={'WORK_PACKAGE':WP,'RESULT':'PASS','OWNER_DECISION':dc['OPTION_ID'],'CHARTER_EFFECTIVE':'YES','NORMATIVE_SUBJECT_VERIFIED':'YES','OWNER_DECISION_VERIFIED':'YES','ADOPTION_RECORD_PERSISTED':'YES','ADOPTION_RECORD_INDEPENDENTLY_VERIFIED':'YES','NORMATIVE_MANDATE_EFFECTIVE':'YES','ADOPTION_RECORD_IDENTITY':record['IDENTITY'],'A15_NORMATIVE_AUTHORITY_ISSUED':'YES','A15_EXECUTION_AUTHORITY_ISSUED':'NO','A15_CAPTURE_AUTHORITY_ISSUED':'NO','A15_EXECUTED':'NO','A16_EXECUTED':'NO','A14_PERSISTENCE_RERUN':'NO','BASELINE_AMENDED':'NO','FOUR_SEED_DETERMINISM':'PASS (0,1,7,101)','NEGATIVE_SUITE':str(len(neg))+'/'+str(len(neg))+' PASS','TOTAL_REFERENCES':161,'TOTAL_RESOLVED':109,'TOTAL_UNRESOLVED':52,'NEXT_BOUNDARY':'A15_EXECUTOR_AND_ENVIRONMENT_QUALIFICATION','V3_SELECTED':'YES','FROZEN_OBLIGATIONS':128,'CONCRETE_DISPATCH_JOBS':220,'A14_RUNTIME_PERSISTENCE_QUALIFICATION':'PASS','E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO','END_INTERFACES_BOUND':'4/6','P05_EXECUTION_READY':'NO'}
base=ROOT/'docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_P05_D01_A15_NORMATIVE_ADOPTION_ISSUANCE_68'
assert not base.with_suffix('.json').exists() and not base.with_suffix('.md').exists()
base.with_suffix('.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
md='''# A15 Normative Adoption Issuance 68

The project owner's exact normative-only selection has been recorded, persisted and independently verified under effective Charter v1.0. The normative mandate is effective. Execution and capture grants remain withheld.

The adoption binds the immutable Package67 normative subject `b83a133c612f690f433e64b4e4f2788369851466d850cfdb7a6fb135d6f8e30d`, technical subject `befe07aacc6b4c4e203488bce731f265a0520cf145174dca33dbfb4e68b43e9b`, charter `d26962c58f17281173e965433dae63a941e078115f3dcc30e2a3512fa21812b8` and effective lifecycle `a27516baa0ab7f34a36a1130490b6cfa38c508975ca337e0824c8eac33715cbb`.

The record preserves the complete adopted content: owner/source relationships, requiredness and coverage, two independent singleton variants, nonempty protection policy, assurance limitations and historical exclusions. It does not change native proof declarations, frozen acceptance, historical admissions, the baseline, or the unresolved historical owner classifications. Package67 remains an unchanged historical preparation report.

Owner evidence is the explicit current user-role declaration and selection under the charter's project-owner role. No personal identifier, signature, platform message identifier or external credential is invented. The provenance excerpt and its raw pin are separate from the decision content identity. The adoption's canonical record identity excludes its own identity and future verification evidence. The effective reference depends on the adoption and completed checks, avoiding circular approval identities.

Documentary evidence was published exclusively with file and directory fsync and independently reread. This is issuance-record persistence, not native qualification capture, save or restore. The Package66 metadata reader verified the ordered DRAFT → REVIEWED → APPROVED → EFFECTIVE chain. A separate Package68 reader reconstructed the subject and owner decision from retained sources. Four fresh hash-seeded documentary verifier processes agreed. Nineteen in-memory corruptions were rejected. No native Planner entrypoint, invalidation, writer, cold reader, persistence transaction or A14 rerun was invoked.

The immutable adoption record retains a pending-verification status describing its publication phase; the separately persisted effective reference records completion of every prerequisite. Effectiveness starts at that verified publication boundary, with no backdating. Prior artifacts and the lessons register were checked byte-for-byte and left unchanged.

Execution and capture decision readiness remain NO. The next work is exact executor/invocation qualification and verified environment/resource permissions, followed by separately approved execution and capture mandates. No operand is promoted; accounting remains 161 total, 109 resolved, 52 unresolved.

Evidence is in [the Package68 qualification directory](qualification/E2_P05_D01_A15_NORMATIVE_ADOPTION_ISSUANCE_68/). `verify.py` is read-only; `issue.py` refuses existing publication targets and must not be rerun to duplicate issuance.

```text
'''+ '\n'.join(k+' = '+str(x) for k,x in report.items())+'\n```\n'
base.with_suffix('.md').write_text(md)
print(json.dumps(report,sort_keys=True))
