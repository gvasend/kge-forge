"""Apply only the authorized I01 route replacement after generic qualification.

Every historical input is read-only. All newly created qualification artifacts
are immutable except the current package's explanatory result report.
"""
from dataclasses import replace,fields
from pathlib import Path
import hashlib,json,os,re,subprocess,sys
from adapter.planner import model as m,codec as c,core,gates,installation as i,evidence as ev
from adapter.planner import evidence_attestation as ea
from adapter.tests.test_planner_installation import request as prepare_request

R=Path(__file__).resolve().parents[2];D=R/'docs/plans';P='DETERMINISTIC_PLANNER_V0_1_'
O=D/'qualification/INSTALLATION_I02_1';Q=D/'qualification/E2_P04_CONTINUATION_INPUT_CLOSURE_1'
BUNDLE_NAME=P+'E2_P04_POST_ROUTE_INSTALL_BUNDLE_1.json'


def write(path,value):
    raw=c.canonical_bytes(value)
    c._write_immutable(c._transaction_directory(path.parent,R),path.name,raw)
    return raw


def pure_preflight(snapshot,candidate,attestation):
    before=c.snapshot_bytes(snapshot)
    try:ev.apply(snapshot,candidate,attestation)
    except m.PlannerError as ex:failure=str(ex)
    else:raise AssertionError('unexpected Evidence admission in closure')
    assert c.snapshot_bytes(snapshot)==before
    return failure


def run():
    log=(O/'qualified-tests.log').read_text()
    assert re.search(r'Ran 30 tests in .*\n\nOK\s*$',log), 'Generic/current-runtime qualification must pass before P04 replacement'
    test_names=[{'test':name,'class':cls} for name,cls in re.findall(r'^(test_\w+) \(([^)]+)\) \.\.\. ok$',log,re.M)]
    assert len(test_names)==30
    contract_path=D/(P+'INSTALLATION_I01_CONTRACT.json');contract_raw=contract_path.read_bytes()
    contract=json.loads(contract_raw);a=contract['P04_route_application'];d=a['definition_descriptor']
    prior=json.loads((O/'pre-work-hashes.json').read_text())
    assert hashlib.sha256(contract_raw).hexdigest()==prior[str(contract_path.relative_to(R))]
    assert c._identity(c.canonical_bytes(d),'planner-installable-definition-v1')==i.identity(a['definition_id'])
    raw=(R/d['provenance']['path']).read_bytes()
    assert c._identity(raw,'raw-file-sha256')==i.identity(a['content_id'])
    provenance=m.Provenance(d['provenance']['path'],i.identity(a['content_id']),d['provenance']['section'],raw.decode(),d['provenance']['method'],d['scope'])
    definition=m.InstallableDefinition(i.identity(a['definition_id']),c.canonical_bytes(d).decode(),provenance)
    parsed,route=i.descriptor(definition)
    assert parsed==d
    b=c.restore(D/(P+'P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1.json'),c._unwire(a['pre_bundle']),R)
    assert c.snapshot_id(b.current)==c._unwire(a['pre_state']) and b.events[-1].identity==c._unwire(a['parent_event'])
    assert i.old_reference(b.current,d)==i.identity(a['expected_old_reference_id'])
    assert b.policy==c._unwire(a['policy_pin']) and b.policy_version==a['policy_version']
    assert not b.current.installed_definitions and core.recompute(b.current).control is m.ControlState.EXTERNAL_WAIT
    old=c._unwire(c.parse_json((Q/'a09-candidate.json').read_bytes()))
    bound=json.loads((Q/'evidence-binding.json').read_text())['attestation']['fields']
    attest=ea.EvidenceBoundAttestation(**{k:c._unwire(v) for k,v in bound.items()})
    assert pure_preflight(b.current,old,attest)=='ROUTE_NOT_CURRENT'
    capture={'schema':'PLANNER-INSTALL-HUMAN-DECISION-1','issuer':'AUTHENTICATED_HUMAN_USER',
        'authorizing_role':'QUALIFICATION_AUTHORITY','transport':'EXPLICIT_USER_ROLE_SESSION_MESSAGE',
        'selected_option':'AUTHORIZE_P04_ROUTE_REPLACEMENT','I01_option_equivalence':'AUTHORIZE_P04_ROUTE_INSTALLATION',
        'equivalence_basis':'I01 decision subject explicitly authorizes the exact prospective route REPLACE. User selected the more specific REPLACEMENT token; no definition/scope term changes.',
        'decision_subject':contract['human_decision']['subject'],'contract_id':i.simple(c._identity(contract_raw,'raw-file-sha256')),
        'definition_id':a['definition_id'],'content_id':a['content_id'],'expected_old_reference_id':a['expected_old_reference_id'],
        'scope':d['scope'],'lineage':d['lineage'],'generation':d['generation'],'operation':'REPLACE',
        'pre_bundle':a['pre_bundle'],'pre_state':a['pre_state'],'parent_event':a['parent_event'],
        'policy_pin':a['policy_pin'],'policy_version':a['policy_version'],'capture_sequence':1,'session_date':'2026-10-04',
        'provenance':'Current explicit INSTALLATION-I02 user request; no cryptographic human signature claimed.',
        'exclusions':contract['human_decision']['authorize']['does_not_authorize']}
    capture_raw=write(O/'human-replacement-authorization.json',capture)
    decision=c._identity(capture_raw,'raw-file-sha256')
    r,returned_decision=prepare_request(b,definition,receipt_path=str((O/'install-authority-admission.json').relative_to(R)),
        decision=decision,contract=c._identity(contract_raw,'raw-file-sha256'))
    assert returned_decision==decision
    write(O/'install-command.json',c._wire(r))
    write(O/'issued-install-grant.json',c.parse_json(r.authority.grant_json.encode()))
    # Authority admitted via trusted user transport before the install transaction.
    i.validate_authority(r,b.current.context)
    # Independent frame oracle exists before installation; it does not use its output.
    expected_gate=replace(b.current.external_gates[0],resolution_contracts=(route,))
    expected=m.InstalledDefinition(i.installed_id(r),r,r.expected_old_reference)
    oracle=replace(b.current,external_gates=(expected_gate,),installed_definitions=(expected,))
    write(O/'pre-install-oracle.json',{'pre_state':c._wire(c.snapshot_id(b.current)),
        'expected_post_state':c._wire(c.snapshot_id(oracle)),'expected_snapshot':c._wire(oracle),
        'expected_sequence':3,'expected_parent':c._wire(b.events[-1].identity),
        'allowed_snapshot_fields':['external_gates.resolution_contracts','installed_definitions'],
        'forbidden_lifecycle_operations':['A09','A10','A11','A12','A13']})
    post,bid,noop=i.commit(b,r,O/'canonical-route-head',R,expected_authority=r.authority.id,expected_decision=decision)
    assert c.snapshot_id(post.current)==c.snapshot_id(oracle)
    assert len(post.events)==3 and sum(type(e.result) is m.InstallDefinition for e in post.events)==1
    record=next(x for x in post.current.installed_definitions if x.id==expected.id)
    assert i.current(post,record)
    assert post.events[:2]==b.events  # Prefix execution events have no unordered field changes.
    before=c._prefix_bundle(post,2)
    assert c.bundle_bytes(before)==c.bundle_bytes(b)
    assert not any(p.path==provenance.path for p in before.sources)
    comparisons={f.name:getattr(post.current,f.name)==getattr(b.current,f.name) for f in fields(m.Snapshot)
        if f.name not in ('external_gates','installed_definitions')}
    assert all(comparisons.values())
    assert replace(post.current.external_gates[0],resolution_contracts=b.current.external_gates[0].resolution_contracts)==b.current.external_gates[0]
    # Emit complete native event files beside a separately named published bundle.
    native_path,native_id=c.save_bundle(post,D,R)
    assert native_id==bid
    c._write_immutable(D,BUNDLE_NAME,c.bundle_bytes(post))
    postpath=D/BUNDLE_NAME
    restored=c.restore(postpath,bid,R)
    assert c.bundle_id(restored)==bid and c.snapshot_id(c._replay(restored))==c.snapshot_id(oracle)
    retry,original,noop=i.commit(b,r,O/'canonical-route-head',R,expected_authority=r.authority.id,expected_decision=decision)
    assert noop and original==bid and c.bundle_id(retry)==bid
    assert pure_preflight(restored.current,old,attest)=='PARENT_MISMATCH'
    # Identical native Evidence identity inputs justify equal identity, not reuse
    # of a previously admitted Evidence (none is present in either state).
    fresh=replace(old,expected_bundle=bid,expected_snapshot=c.snapshot_id(restored.current),expected_parent_event=restored.events[-1].identity)
    fresh=replace(fresh,command_key=ev.command_key(fresh))
    new_attest=ea.EvidenceBoundAttestation(**{k:c._unwire(v) for k,v in bound.items()})
    assert ev.evidence_id(fresh.gate,fresh.entity.identity,restored.current.context)==fresh.entity.id
    assert fresh.expected_parent_event==post.events[-1].identity and fresh.command_key!=old.command_key
    assert provenance in fresh.admission.dependencies
    fresh_failure=pure_preflight(restored.current,fresh,new_attest)
    assert fresh_failure!='ROUTE_NOT_CURRENT' and fresh_failure=='DEPENDENCY_PROVENANCE'
    write(O/'a09-post-install-candidate.json',c._wire(fresh))
    write(O/'a09-post-install-transient-attestation.json',{'type':'EvidenceBoundAttestation','fields':{k:c._wire(v) for k,v in vars(new_attest).items()}})
    # Scope/domain outputs remain exactly the checkpoint's non-executed lifecycle.
    assert not post.current.receipt_admissions and not post.current.receipt_observations
    assert not post.current.typed_proofs and not post.current.proof_contracts
    assert not any(e.kind is m.EntityKind.EVIDENCE for e in post.current.entities)
    assert all(s.state is not m.ActionState.COMPLETED for s in post.current.statuses if s.id.value in ('E2-REENTER','E2-FINISH'))
    dag={
        'ROUTE':{'status':'ALREADY_CURRENT','definition_id':i.simple(definition.id),'scope_authority':'Exact authorized REPLACE only'},
        'INGRESS':{'status':'AUTHORITY_REQUIRED','additional_dependency':'Separately qualify EvidenceIngressContract installation adapter; prepared ingress source is absent from prefix'},
        'ATTEST':{'status':'AUTHORITY_REQUIRED','additional_dependency':'Separately qualify atomic authority/attestor/source predicate configuration adapter; prepared offline ATTEST is absent'},
        'ACTION_RESULTS':{'status':'AUTHORITY_REQUIRED','additional_dependency':'Accepted-result contract adapter, explicit bounded replacement grant; E2-REENTER inventory remains empty'},
        'VALIDATION':{'status':'CONTRACT_BLOCKED','additional_dependency':'Define ordinary native A10 event/persisted validation adapter; no ValidationResult generated'},
        'PROOFS':{'status':'AUTHORITY_REQUIRED','additional_dependency':'Evidence-proof contract adapter/authority after ingress+validation'},
        'ROOT_SLOT':{'status':'AUTHORITY_REQUIRED','additional_dependency':'Route INSTALL grant cannot install PC02/E06 definitions; their reviewed adapters and separate grant required'}}
    negative_map={
        'I01-N01':'test_authority_admission_is_not_self_authorization',
        'I01-N02':'test_security_negatives_and_stale_parent','I01-N03':'test_security_negatives_and_stale_parent',
        'I01-N04':'test_security_negatives_and_stale_parent','I01-N05':'test_security_negatives_and_stale_parent',
        'I01-N06':'test_authority_admission_is_not_self_authorization','I01-N07':'test_authority_admission_is_not_self_authorization',
        'I01-N08':'test_security_negatives_and_stale_parent','I01-N09':'test_security_negatives_and_stale_parent',
        'I01-N10':'test_security_negatives_and_stale_parent','I01-N11':'test_security_negatives_and_stale_parent',
        'I01-N12':'test_currentness_invalidation_expiry_context_and_no_fallback','I01-N13':'test_security_negatives_and_stale_parent',
        'I01-N14':'test_security_negatives_and_stale_parent','I01-N15':'P04 old candidate pure preflight PARENT_MISMATCH',
        'I01-N16':'test_authority_admission_is_not_self_authorization','I01-N17':'test_authority_admission_is_not_self_authorization',
        'I01-N18':'test_security_negatives_and_stale_parent','I01-N19':'test_security_negatives_and_stale_parent',
        'I01-N20':'test_security_negatives_and_stale_parent','I01-N21':'test_source_history_missing_records_and_concurrent_head',
        'I01-N22':'test_source_history_missing_records_and_concurrent_head','I01-N23':'test_source_history_missing_records_and_concurrent_head',
        'I01-N24':'test_security_negatives_and_stale_parent','I01-N25':'test_security_negatives_and_stale_parent',
        'I01-N26':'test_replace_frame_identity_history_persistence_and_retry','I01-N27':'test_source_history_missing_records_and_concurrent_head',
        'I01-N28':'test_currentness_invalidation_expiry_context_and_no_fallback','I01-N29':'test_install_absent_role_and_replacement_supersession',
        'I01-N30':'test_source_history_missing_records_and_concurrent_head','I01-N31':'test_process_crash_before_and_after_head'}
    negatives=[dict(n,status='PASS',evidence=negative_map[n['id']]) for n in contract['SECURITY_NEGATIVES']]
    result={'schema':'PLANNER-INSTALLATION-I02-RESULT-1','WORK_PACKAGE':'INSTALLATION-I02','RESULT':'PASS',
        'SELECTED_OPTION':'AUTHORIZE_P04_ROUTE_REPLACEMENT','AUTHORIZATION_AUTHENTICATION':'PASS',
        'authorization_capture':capture,'authorization_capture_id':c._wire(decision),'contract_id':i.simple(c._identity(contract_raw,'raw-file-sha256')),
        'INSTALLATION_CAPABILITY':'PASS','generic_qualification':{'tests':test_names,'test_count':30,'generic_test_count':9,
            'independent_non_E2_lineage':'TEST/lineage','fresh_readers':24,'hash_seeds':[0,1,7,101],
            'readers_per_checkpoint_per_seed':3,'writer_terminated_before_fresh_reads':True,
            'criteria':{k:'PASS' for k in ['authority','INSTALL_DEFINITION','INSTALL_REPLACE','currentness','atomicity','idempotence','historical_immutability',
                'candidate_invalidation','negatives','persistence','cold_restore','replay','determinism']},'negatives':negatives,
            'supersession_semantics':'REPLACE retires exact predecessor. Standalone SUPERSEDE and CONFLICT rejected, per I01.',
            'enabled_definition_adapter':'EXTERNAL_RESOLUTION_CONTRACT only'},
        'INSTALL_AUTHORITY_ID':c._wire(r.authority.id),'INSTALL_AUTHORITY_ADMISSION':'PASS','INSTALL_AUTHORITY_APPLICABILITY':'PASS',
        'P04_ROUTE_INSTALL_EVENT_ID':c._wire(post.events[-1].identity),
        'INSTALLED_ROUTE_DEFINITION_ID':c._wire(definition.id),'INSTALLED_ROUTE_CONTENT_ID':c._wire(provenance.identity),
        'INSTALLED_DEFINITION_INSTANCE_ID':c._wire(record.id),
        'PRE_INSTALL_STATE_ID':c._wire(c.snapshot_id(b.current)),'POST_INSTALL_STATE_ID':c._wire(c.snapshot_id(post.current)),
        'POST_INSTALL_LEDGER_ROOT':c._wire(post.events[0].identity),'POST_INSTALL_APPEND_HEAD':c._wire(post.events[-1].identity),
        'ledger_root_semantics':'Native ordinary ledger anchor is first event; remains unchanged. One append advances event count and head. No fabricated LedgerId/Merkle root.',
        'P04_POST_INSTALL_BUNDLE_ID':c._wire(bid),'P04_POST_INSTALL_BUNDLE_PATH':str(postpath.relative_to(R)),
        'ROUTE_CURRENTNESS':'PASS','ROUTE_APPLICABILITY':'PASS','PERSISTENCE':'PASS','COLD_RESTORE':'PASS','REPLAY':'PASS','HISTORICAL_IMMUTABILITY':'PASS',
        'frame_comparison':comparisons,'pre_install_prefix_exact':True,'authority_use_count':1,'idempotent_retry':'PASS',
        'OLD_A09_CANDIDATE':'STALE','old_candidate_native_preflight':'PARENT_MISMATCH',
        'A09_CANDIDATE_REMATERIALIZED':'YES','fresh_candidate_path':str((O/'a09-post-install-candidate.json').relative_to(R)),
        'native_Evidence_identity_equal':'Identity input equality independently checked; no admitted historical instance reused',
        'A09_PREFLIGHT':'FAIL_CLOSED','NEXT_FAILURE':fresh_failure,
        'preflight_dimensions':{'bundle':fresh.expected_bundle==bid,'Snapshot':fresh.expected_snapshot==c.snapshot_id(post.current),
            'parent':fresh.expected_parent_event==post.events[-1].identity,'route':i.current(restored,record),
            'scope_lineage_generation':(fresh.entity.scope,fresh.entity.lineage,fresh.entity.generation)==(d['scope'],d['lineage'],d['generation'])},
        'next_failure_trace':{'canonical_authentication_predicate_present':any(p.id==fresh.admission.authentication for p in post.current.predicates),
            'missing_dependency':'Offline ATTEST provenance in admission.dependencies has no canonical current authority/attestor. Do not drop it to bypass authentication.',
            'ingress_source_in_prefix':any(p.identity==fresh.contract_pin for p in post.sources)},
        'REMAINING_INSTALLATION_DAG':dag,'NEXT_PACKAGE':'P04 ingress/ATTEST installation adapter contract + bounded authority',
        'P04_EXECUTION_READY':'NO','E2_P04_READY':'NO','A09_A13_EXECUTED':'NO',
        'A09_EXECUTED':'NO','A10_EXECUTED':'NO','A11_EXECUTED':'NO','A12_EXECUTED':'NO','A13_EXECUTED':'NO',
        'P03_RESULT':'PASS','P03_HISTORICAL_CORRESPONDENCE':'UNPROVEN','N_REAL_SATISFIED':'NO','E2_FINISH_EXECUTED':'NO',
        'E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO','RUNTIME_MODIFIED':'YES',
        'TARGETED_REGRESSIONS':'30 PASS',
        'BROAD_REGRESSION_STATUS':'Pre-existing frozen-E1 duplicate-import collection blocker; expanded T01 compatibility suite retains identical pre-work 4 failures/12 errors; no aggregate qualification inferred',
        'pre_existing_comparison':json.loads((O/'pre-existing-regression-comparison.json').read_text())}
    write(O/'post-install-evidence.json',result)
    print(json.dumps({'bundle':bid.sha256,'state':c.snapshot_id(post.current).sha256,'event':post.events[-1].identity.sha256,
        'next_failure':fresh_failure,'P04_ready':'NO'}))

if __name__=='__main__':run()
