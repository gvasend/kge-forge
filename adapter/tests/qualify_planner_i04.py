"""Apply the exact authorized I03 sequence after generic qualification only."""
from dataclasses import replace,fields
from pathlib import Path
import hashlib,json,os,re,subprocess,sys
from adapter.planner import codec as c,model as m,core,installation as i,authentication_installation as a,evidence as ev,evidence_attestation as ea,gates
from adapter.tests.test_planner_authentication_installation import operating,request
R=Path(__file__).resolve().parents[2];D=R/'docs/plans';P='DETERMINISTIC_PLANNER_V0_1_';O=D/'qualification/INSTALLATION_I04_1';Q=D/'qualification/E2_P04_CONTINUATION_INPUT_CLOSURE_1'


def write(path,value):
    raw=c.canonical_bytes(value);c._write_immutable(c._transaction_directory(path.parent,R),path.name,raw);return raw


def defn(value):
    d=value['descriptor'];raw=(R/d['provenance']['path']).read_bytes();p=m.Provenance(d['provenance']['path'],i.identity(d['content_id']),'/',raw.decode(),d['provenance']['method'],d['scope'])
    obj=m.InstallableDefinition(c._unwire(value['definition_id']),c.canonical_bytes(d).decode(),p);i.descriptor(obj);return obj


def preflight(b,x,t):
    before=c.bundle_bytes(b);c._replay(b);c._verify_sources(b,R)
    assert x.expected_bundle==c.bundle_id(b) and x.expected_parent_event==b.events[-1].identity
    contract=ev.ingress(x);assert m.ArtifactPin(contract.provenance.path,contract.provenance.identity) in b.sources
    try:ev.apply(b.current,x,t)
    except m.PlannerError as ex:result=str(ex)
    else:result='PASS'
    assert c.bundle_bytes(b)==before
    return result


def run():
    testlog=(O/'qualified-tests.log').read_text();assert re.search(r'\nOK\s*$',testlog),'Qualify generic installation before P04 application'
    contractpath=D/(P+'INSTALLATION_I03_ATTEST_INGRESS_CONTRACT.json');raw=contractpath.read_bytes();contract=json.loads(raw);prior=json.loads((O/'pre-work-hashes.json').read_text())
    assert hashlib.sha256(raw).hexdigest()==prior[str(contractpath.relative_to(R))]
    for path,sha in prior.items():
        if '/INSTALLATION_I03_1/' in path:assert hashlib.sha256((R/path).read_bytes()).hexdigest()==sha
    cid=c._identity(raw,'raw-file-sha256');auth=defn(contract['P04_mapping']['authentication_set']);ing=defn(contract['P04_mapping']['ingress'])
    spec=contract['INSTALLATION_AUTHORITY']['ordered_install_grants'][0]
    b=c.restore(D/(P+'E2_P04_POST_ROUTE_INSTALL_BUNDLE_1.json'),c._unwire(spec['pre_bundle']),R)
    assert c.snapshot_id(b.current)==c._unwire(spec['pre_state']) and b.events[-1].identity==c._unwire(spec['parent'])
    assert core.recompute(b.current).control is m.ControlState.EXTERNAL_WAIT and len(b.events)==3
    assert all(i.current(b,r) for r in b.current.installed_definitions)
    decision_body={'schema':'PLANNER-I04-AUTHENTICATED-HUMAN-DECISION-1','selected_option':'AUTHORIZE_P04_ATTEST_INGRESS_INSTALLATION','issuer':'AUTHENTICATED_HUMAN_USER','issuer_role':'QUALIFICATION_AUTHORITY','authentication':'EXPLICIT_USER_ROLE_SESSION_MESSAGE','date':'2026-10-04','capture_sequence':1,'I03_contract_id':i.simple(cid),'definition_set_id':c._wire(auth.id),'ingress_id':c._wire(ing.id),'member_subjects':contract['human_decision']['bounded_subjects']['members'],'pre_bundle':c._wire(c.bundle_id(b)),'pre_state':c._wire(c.snapshot_id(b.current)),'parent_event':c._wire(b.events[-1].identity),'context':c._wire(b.current.context),'provenance':'Current explicit INSTALLATION-I04 user instruction; trusted transport, no cryptographic signature','operating_authority_permission':'Separately issue/admit exact scoped ATTEST declaration under I03; INSTALL does not issue it','exclusions':['route replacement','A09-A13 execution','Evidence admission','proof/Action/result/validation/root-slot installations','P03/historical/N-REAL/release changes']}
    decision=c._identity(write(O/'authenticated-human-decision.json',decision_body),'raw-file-sha256')
    binding=operating(auth,decision,cid,str((O/'operating-attest-admission.json').relative_to(R)))
    write(O/'issued-operating-attest-grant.json',c.parse_json(binding.issued_authorization_json.encode()))
    # Future authority already issued/admitted; no native state or event yet changed.
    r=request(b,auth,decision,cid,str((O/'authentication-install-admission.json').relative_to(R)),binding)
    a.validate_binding(r,i.descriptor(auth)[0],i.descriptor(auth)[1],b.current.context);i.validate_authority(r,b.current.context)
    native=i.descriptor(auth)[1];record=m.InstalledDefinition(i.installed_id(r),r,None)
    oracle=replace(b.current,entities=b.current.entities+(native['authority'],native['attestor']),predicates=b.current.predicates+(native['authority_predicate'],native['source_predicate']),installed_definitions=b.current.installed_definitions+(record,))
    write(O/'authentication-pre-execution-oracle.json',{'expected_snapshot':c._wire(c.snapshot_id(oracle)),'allowed_fields':['entities','predicates','installed_definitions'],'expected_members':{k:c._wire(v) for k,v in native.items()},'expected_parent':c._wire(b.events[-1].identity),'expected_sequence':4})
    write(O/'authentication-install-command.json',c._wire(r))
    first,firstid,noop=i.commit(b,r,O/'canonical-authentication-head',R,expected_authority=r.authority.id,expected_decision=decision,expected_operating_authority=binding.operating_authorization_id)
    assert not noop and c.snapshot_id(first.current)==c.snapshot_id(oracle)
    firstpath,_=c.save_bundle(first,O/'first-boundary',R);cold=c.restore(firstpath,firstid,R)
    assert c.snapshot_id(cold.current)==c.snapshot_id(oracle) and i.current(cold,cold.current.installed_definitions[-1])
    # Second bounded grant names the actual committed descendant, never a guessed head.
    r2=request(cold,ing,decision,cid,str((O/'ingress-install-admission.json').relative_to(R)))
    native_ing=i.descriptor(ing)[1];record2=m.InstalledDefinition(i.installed_id(r2),r2,None)
    oracle2=replace(cold.current,ingress_contracts=(native_ing,),installed_definitions=cold.current.installed_definitions+(record2,))
    write(O/'ingress-pre-execution-oracle.json',{'expected_snapshot':c._wire(c.snapshot_id(oracle2)),'expected_ingress':c._wire(native_ing),'expected_parent':c._wire(cold.events[-1].identity),'expected_sequence':5,'allowed_fields':['ingress_contracts','installed_definitions']})
    write(O/'ingress-install-command.json',c._wire(r2))
    final,bid,noop=i.commit(cold,r2,O/'canonical-authentication-head',R,expected_authority=r2.authority.id,expected_decision=decision)
    assert not noop and c.snapshot_id(final.current)==c.snapshot_id(oracle2)
    assert all(i.current(final,x) for x in final.current.installed_definitions)
    assert c.bundle_bytes(c._prefix_bundle(final,3))==c.bundle_bytes(b)
    path=D/(P+'E2_P04_POST_ATTEST_INSTALL_BUNDLE_1.json');c.save_bundle(final,D,R);c._write_immutable(D,path.name,c.bundle_bytes(final))
    restored=c.restore(path,bid,R);assert c.snapshot_id(c._replay(restored))==c.snapshot_id(oracle2)
    # Exact retry at an advanced head is historical idempotence, no new issuance/use.
    retry,original,noop=i.commit(b,r,O/'canonical-authentication-head',R,expected_authority=r.authority.id,expected_decision=decision,expected_operating_authority=binding.operating_authorization_id)
    assert noop and original==firstid and c.bundle_id(retry)==bid
    # Independent second store reproduces both exact events/identities from same inputs.
    independent,_,_=i.commit(b,r,O/'independent-head',R,expected_authority=r.authority.id,expected_decision=decision,expected_operating_authority=binding.operating_authorization_id)
    independent,indid,_=i.commit(independent,r2,O/'independent-head',R,expected_authority=r2.authority.id,expected_decision=decision)
    assert indid==bid and c.bundle_bytes(independent)==c.bundle_bytes(final)
    old=c._unwire(c.parse_json((D/'qualification/INSTALLATION_I02_1/a09-post-install-candidate.json').read_bytes()))
    try:ev.apply(final.current,old)
    except m.PlannerError as ex:old_failure=str(ex)
    else:raise AssertionError('old candidate unexpectedly usable')
    assert old_failure=='PARENT_MISMATCH'
    deps=tuple(c._unwire(x) for x in contract['P04_DEPENDENCY_PROVENANCE_SET'])
    assert len(deps)==len(set(deps))==4
    for p in deps:assert m.ArtifactPin(p.path,p.identity) in final.sources and c.load_pinned(R,m.ArtifactPin(p.path,p.identity)).decode()==p.excerpt
    admission=replace(old.admission,dependencies=deps)
    fresh=replace(old,expected_bundle=bid,expected_snapshot=c.snapshot_id(final.current),expected_parent_event=final.events[-1].identity,admission=admission,contract_pin=native_ing.provenance.identity,field_provenance=ev.field_bindings(old.entity,admission,native_ing))
    fresh=replace(fresh,command_key=ev.command_key(fresh));assert ev.ingress(fresh)==native_ing
    binding_info=json.loads((Q/'evidence-binding.json').read_text())['attestation']['fields']
    # Transient E02 instance only: do NOT emit/serialize its body or put it in bundle.
    fields2={k:c._unwire(v) for k,v in binding_info.items() if k!='attestation_id'};attest=ea.materialize(**fields2)
    outcome=preflight(restored,fresh,attest)
    write(O/'a09-post-authentication-candidate.json',c._wire(fresh))
    # Fresh process readers verify all relevant native identities/currentness without a transient instance.
    program='from pathlib import Path;from adapter.planner import codec as c,model as m,installation as i;import json,sys;b=c.restore(Path(sys.argv[1]),m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,"planner-bundle-v1",sys.argv[2]),Path(sys.argv[3]));assert all(i.current(b,x) for x in b.current.installed_definitions);print(json.dumps({"bundle":c.bundle_id(b).sha256,"snapshot":c.snapshot_id(c._replay(b)).sha256,"head":b.events[-1].identity.sha256,"entities":len(b.current.entities),"predicates":len(b.current.predicates),"ingress":len(b.current.ingress_contracts)}))'
    readers=[]
    for seed in ('0','1','7','101'):
        for n in range(3):
            out=subprocess.check_output([sys.executable,'-c',program,str(path),bid.sha256,str(R)],text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(R),PYTHONHASHSEED=seed))
            value=json.loads(out);assert value['bundle']==bid.sha256 and value['snapshot']==c.snapshot_id(final.current).sha256 and value['head']==final.events[-1].identity.sha256 and value['ingress']==1
            readers.append({'seed':seed,'reader':n,'domains':value,'result':'PASS'})
    for f in fields(m.Snapshot):
        if f.name not in ('entities','predicates','installed_definitions','ingress_contracts'):assert getattr(final.current,f.name)==getattr(b.current,f.name),f.name
    assert not final.current.receipt_admissions and not final.current.receipt_observations and not final.current.typed_proofs
    assert not any(e.kind is m.EntityKind.EVIDENCE for e in final.current.entities)
    changes=[p for p,sha in prior.items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=sha]
    assert all(p.startswith('adapter/planner/') for p in changes),changes
    diff=subprocess.run(['git','diff','--check'],cwd=R,text=True,capture_output=True);assert diff.returncode==0,diff.stdout+diff.stderr
    trace=[{'operation':'INSTALL','type':'AUTHENTICATION_DEFINITION_SET','authority':c._wire(r.authority.id),'event':c._wire(first.events[-1].identity),'pre_state':c._wire(c.snapshot_id(b.current)),'post_state':c._wire(c.snapshot_id(first.current)),'parent':c._wire(b.events[-1].identity),'sequence':4},
      {'operation':'INSTALL','type':'EVIDENCE_INGRESS_CONTRACT','authority':c._wire(r2.authority.id),'event':c._wire(final.events[-1].identity),'pre_state':c._wire(c.snapshot_id(first.current)),'post_state':c._wire(c.snapshot_id(final.current)),'parent':c._wire(first.events[-1].identity),'sequence':5}]
    dag={k:{'status':'RUNTIME_BLOCKED','authority':'AUTHORITY_REQUIRED','reason':'Prepared offline definitions are not installed; no authority from I04 applies; generic closed adapter for this type not enabled'} for k in ('A10_VALIDATION','A11_TYPED_EVIDENCE_PROOF','A12_REENTER_ACTION_RESULTS','ROOT_SLOT','A13_FINISH_RESULT')}
    dag['INSTANCES']={'status':'LIFECYCLE_INSTANCE_NOT_YET_EXPECTED','objects':['ValidationResult','Evidence proof','REENTER ActionResult','SLOT_PROOF','ROOT_PROOF','FINISH ActionResult']}
    result={'schema':'INSTALLATION-I04-RESULT-1','WORK_PACKAGE':'INSTALLATION-I04','RESULT':'PASS','SELECTED_OPTION':'AUTHORIZE_P04_ATTEST_INGRESS_INSTALLATION','AUTHORIZATION_AUTHENTICATION':'PASS','authenticated_authorization':decision_body,'decision_id':c._wire(decision),'I03_contract_content_id':c._wire(cid),'ATTEST_INGRESS_INSTALLATION_CAPABILITY':'PASS','INSTALL_AUTHORITY_ID':c._wire(r.authority.id),'P04_ATTEST_INSTALL_AUTHORITY_ID':c._wire(r.authority.id),'INGRESS_INSTALL_AUTHORITY_ID':c._wire(r2.authority.id),'OPERATING_ATTEST_AUTHORIZATION_ID':c._wire(binding.operating_authorization_id),'INSTALL_AUTHORITY_ADMISSION':'PASS','INSTALL_AUTHORITY_APPLICABILITY':'PASS','P04_ATTESTOR_ID':c._wire(native['attestor'].id),'P04_PREDICATE_ID':c._wire(native['source_predicate'].id),'P04_INGRESS_DEFINITION_ID':c._wire(ing.id),'DEPENDENCY_PROVENANCE_CARDINALITY':4,'DEPENDENCY_PROVENANCE':'PASS','dependency_provenance_set':c._wire(deps),'POST_ATTEST_INSTALL_STATE_ID':c._wire(c.snapshot_id(final.current)),'POST_ATTEST_INSTALL_APPEND_HEAD':c._wire(final.events[-1].identity),'P04_FINAL_INSTALL_EVENT_ID':c._wire(final.events[-1].identity),'POST_INSTALL_BUNDLE_ID':c._wire(bid),'POST_INSTALL_BUNDLE_PATH':str(path.relative_to(R)),'installation_trace':trace,'CURRENTNESS':'PASS','PERSISTENCE':'PASS','COLD_RESTORE':'PASS','REPLAY':'PASS','DETERMINISM':'PASS','HISTORICAL_IMMUTABILITY':'PASS','ATOMICITY':'PASS','IDEMPOTENCE':'PASS','SECURITY_NEGATIVES':'PASS','generic_qualification':{'log':str((O/'qualified-tests.log').relative_to(R)),'test_count':int(re.search(r'Ran (\d+) tests',testlog).group(1)),'result':'PASS','operating_authority_separation':'PASS','Evidence_bound_attestation_installed':False},'fresh_reader_results':readers,'OLD_A09_CANDIDATE':'STALE','old_candidate_failure':old_failure,'A09_CANDIDATE_REMATERIALIZED':'YES','A09_PREFLIGHT':outcome,'NEXT_FAILURE':None if outcome=='PASS' else outcome,'REMAINING_CONTINUATION_DAG':dag,'NEXT_PACKAGE':'P04-A10-PROSPECTIVE-VALIDATION-CONTRACT-INSTALLATION-CONTRACT','P04_EXECUTION_READY':'NO','E2_P04_READY':'NO','A09_A13_EXECUTED':'NO','E2_FINISH_EXECUTED':'NO','P03_RESULT':'PASS','P03_HISTORICAL_CORRESPONDENCE':'UNPROVEN','N_REAL_SATISFIED':'NO','E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO','git_diff_check':'PASS','runtime_files_changed':changes+['adapter/planner/authentication_installation.py'],'historical_record_files_changed':[],'transient_attestation':'Constructed in memory for preflight, not serialized or admitted','broad_regression_status':'OTHER: 20 legacy Evidence-admission tests: 4 pass, 4 failures, 12 errors; same failures with exact pre-I04 Evidence module; frozen-E1 duplicate-import collection blocker separately preserved','legacy_regression_counterexamples':'docs/plans/qualification/INSTALLATION_I04_1/legacy-baseline-counterexamples.json','legacy_regression_log':'docs/plans/qualification/INSTALLATION_I04_1/legacy-baseline-tests.log'}
    write(O/'execution-evidence.json',result)
    (D/(P+'INSTALLATION_I04_RESULT.json')).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    lines=['# INSTALLATION-I04 — native ATTEST / ingress installation','', 'Generic installation qualification passed before the exact authorized P04 application. Two ordinary INSTALL_DEFINITION events install the atomic authority-reference/attestor/predicate set and its ingress definition. Operating ATTEST was issued/admitted separately; installation did not issue ATTEST rights or create an attestation instance.','', 'The I03 sealed identities and source bytes remain unchanged. The original route checkpoint and every historical report are preserved. Both boundary oracles were recorded before the respective transition; the second grant binds the actual first-event descendant.','', '## Results','', '```text']
    for k,v in result.items():
        if isinstance(v,(str,int)) and k not in ('schema','transient_attestation','broad_regression_status'):lines.append(k+' = '+str(v))
    lines+=['```','', '## Canonical installation trace','', '```json',json.dumps(trace,indent=2),'```','', '## Qualification','',f"{result['generic_qualification']['test_count']} targeted tests passed. They cover generic non-E2 positive projection, closed definitions, wrong references/context/authority, exact provenance cardinality, transient attestation chain guards, atomic publication failures, retry/conflict semantics, independent reproduction, source invalidation and four fresh-process hash-seed readers. P04 adds 12 fresh readers, each comparing six identity/state domains, plus cold restore at both installation boundaries, exact prefix replay and independent two-event reproduction.",'', 'A09 preflight evaluates an isolated immutable candidate through ordinary native admission checks; its proposed Snapshot is discarded and no Evidence/receipt event is committed. The transient E02 attestation body is held only in memory. The old candidate remains unmodified and fails PARENT_MISMATCH.','', 'The expected dependency set has four complete Provenance records: installed ingress body, shared gate/requirement source, installed route body and common installed authentication-set body. Member bodies and authority admission receipts are pinned installation support, not extra A09 dependencies. Extra, missing and duplicate records fail closed.','', '## Continuation boundary','',f'A09 preflight: **{outcome}**. P04 execution readiness remains **NO**: A10-A13 prospective definitions remain offline and their authority/adapters are not installed. No later lifecycle instance is expected yet. I04 authority does not cover them.','', '```json',json.dumps(dag,indent=2),'```','', '## Preservation','', 'P03 PASS and historical correspondence UNPROVEN remain unchanged. N-REAL remains NO; no release conclusion follows. A09-A13 and E2-FINISH were not executed. E1 hash comparison reports zero changes. git diff --check passed. The expanded legacy Evidence-admission suite has 4 passes, 4 failures and 12 errors. The same 16 failures reproduce using the exact pre-I04 Evidence module (hash verified), so they remain separately recorded rather than reported as passing. Representative native failures are RECEIPT_CHANGED_CONTROL and FIELD_PROVENANCE. The pre-existing frozen-E1 broad collection blocker is also preserved; neither failure class was repaired by this bounded package.','', '[Machine evidence](DETERMINISTIC_PLANNER_V0_1_INSTALLATION_I04_RESULT.json) and [native bundle](DETERMINISTIC_PLANNER_V0_1_E2_P04_POST_ATTEST_INSTALL_BUNDLE_1.json).','']
    (D/(P+'INSTALLATION_I04_RESULT.md')).write_text('\n'.join(lines))
    print(json.dumps({k:result[k] for k in ('RESULT','A09_PREFLIGHT','NEXT_FAILURE','P04_EXECUTION_READY','POST_INSTALL_BUNDLE_ID')}))

if __name__=='__main__':run()
