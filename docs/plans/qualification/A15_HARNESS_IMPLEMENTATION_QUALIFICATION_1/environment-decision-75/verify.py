"""Independent static environment-decision reconstruction. No test or migration."""
import copy,hashlib,json,pathlib,sys
D=pathlib.Path(__file__).resolve().parent;E=D.parent;R=D.parents[4];P70=R/'docs/plans/qualification/E2_P05_D01_A15_IMPLEMENTATION_TEST_AUTHORITY_70'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canon(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def verify(overrides=None):
 overrides=overrides or {}
 def read(n):return copy.deepcopy(overrides[n]) if n in overrides else load(D/n)
 auth=read('input-authentication.json')
 for x in auth['INDICES']:
  p=R/x['PIN']['PATH'];assert sha(p)==x['PIN']['RAW_SHA256'];a=load(p);assert len(a['FILES'])==x['FILES_VERIFIED']
  assert all(sha(R/n)==h for n,h in a['FILES'].items())
 p74=load(E/'outer-policy-74/assessment.json');assert p74['SAME_HOST_COMPATIBILITY']=='UNDETERMINED' and not p74['EXACT_REJECTING_POLICY_RULE_ESTABLISHED']
 request=read('codex-administrator-evidence-request.json');assert request['REQUEST_STATUS']=='PREPARED_NOT_SENT' and len(request['QUESTIONS'])==9
 approved=load(P70/'environment-resource-permission-contract.json');limits=approved['RESOURCE_LIMITS']
 assert request['CONTROL_LIMITS']==limits and request['NO_REPLY_STATUS'].startswith('Path A remains UNDETERMINED')
 profile=read('independent-qualification-host-specification.json')
 fields={'HOST_IDENTITY','OPERATING_SYSTEM','KERNEL_VERSION','INTERPRETER_IDENTITY','DEPENDENCY_IDENTITIES','CONFINEMENT_MECHANISM','NETWORK_POLICY','FILESYSTEM_BOUNDARY','PROCESS_ISOLATION','RESOURCE_LIMIT_ENFORCEMENT','INPUT_ALLOWLIST','OUTPUT_ALLOWLIST','AUDIT_BOUNDARY','RESOURCE_OWNERSHIP','ADMINISTRATIVE_AUTHORITY','ENVIRONMENT_FRESHNESS'}
 assert set(profile['REQUIREMENTS'])==fields and set(profile['ACTUAL_BINDINGS'])==fields and all(v is None for v in profile['ACTUAL_BINDINGS'].values())
 assert profile['RESOURCE_CEILINGS']==limits and profile['HOST_AVAILABLE']=='UNDETERMINED' and not profile['PERMISSIONS_VERIFIED'] and not profile['HOST_SELECTED'] and not profile['ENVIRONMENT_QUALIFIED'] and not profile['PROVISIONING_PERFORMED']
 assert profile['NO_VM_AUTOMATIC_COMPATIBILITY'] and profile['NO_ACTUAL_A15_EXECUTION_INCLUDED']
 for x in profile['SOURCE_FILES']:assert sha(R/x['PATH'])==x['RAW_SHA256'] and x['MODIFIABLE_IN_PACKAGE75'] is False
 matrix=read('resource-control-equivalence-matrix.json');assert len(matrix['ROWS'])==10 and not matrix['NETWORK_DISABLED_REQUIREMENT_WEAKENED'] and not matrix['UNKNOWN_RESOURCE_CONTROL_ACCEPTED']
 for x in matrix['ROWS']:assert x['CEILING']==limits[x['CONTROL']] and x['PATH_A_ENFORCEMENT']==x['PATH_B_ENFORCEMENT']=='UNVERIFIED' and x['INDEPENDENT_EVIDENCE_REQUIRED']
 transfer=read('artifact-transfer-contract.json');assert transfer['STATUS']=='PROPOSED_NOT_PERFORMED_NOT_AUTHORIZED' and transfer['TRANSFER_PERFORMED'] is False
 assert transfer['TARGET_HOST_IDENTITY'] is None and transfer['TARGET_WORKSPACE'] is None
 assert transfer['SOURCE_HASH_REQUIRED'] and transfer['DESTINATION_HASH_REQUIRED'] and transfer['AFTER_COPY_EQUALITY_REQUIRED'] and transfer['TARGET_OWNER_PERMISSION_REQUIRED'] and transfer['NO_ORIGINAL_RELOCATION_OR_DELETION'] and transfer['NO_RESET_STOPPED_JOURNAL']
 assert 'real A15 checkpoint and original19 ledger files' in transfer['FORBIDDEN_TRANSFER'] and 'real A15 full-output oracles' in transfer['FORBIDDEN_TRANSFER']
 for x in transfer['REQUIRED_SOURCE_ARTIFACTS']:
  assert sha(R/x['PATH'])==x['RAW_SHA256']
  assert '/checkpoints/' not in x['PATH'] and 'full-expected-output' not in x['PATH'] and not x['PATH'].endswith('campaign-budget.jsonl')
 assert len(transfer['DEFERRED_SYNTHETIC_ARTIFACTS'])==2 and transfer['DEFERRED_SYNTHETIC_ARTIFACTS'][0]['CURRENT_STATUS'].startswith('UNGENERATED')
 campaign=read('campaign-authority-prerequisites.json');assert campaign['ORIGINAL_CAMPAIGN_TERMINATED'] and not campaign['EXISTING_GRANT_IS_UNLIMITED_RETRY_PERMISSION'] and campaign['FRESH_EXPLICIT_APPROVAL_REQUIRED'] and not campaign['READY']
 assert not campaign['CAMPAIGN_AUTHORITY_ISSUED'] and campaign['SELECTABLE_EXECUTION_OPTIONS']==[] and campaign['NO_ACTUAL_A15_SCOPE']
 assert campaign['CURRENT_VALUES']['RESOURCE_LIMITS']==limits and campaign['CURRENT_VALUES']['RETRY_POLICY']['AUTOMATIC_RETRIES']==0
 assert campaign['CURRENT_VALUES']['QUALIFICATION_HOST'] is None and campaign['CURRENT_VALUES']['OUTPUT_BOUNDARY'] is None and campaign['CURRENT_VALUES']['EVIDENCE_BOUNDARY'] is None
 assert len(campaign['CODE_BINDING_BLOCKERS'])==2
 comparison=read('recovery-strategy-comparison.json');assert not comparison['PATH_A']['AUTHORITATIVE_POLICY_EVIDENCE_COMPLETE'] and comparison['PATH_A']['COMPATIBLE']=='UNDETERMINED' and not comparison['PATH_A']['IMPOSSIBILITY_PROVEN']
 assert comparison['PATH_A']['FURTHER_SPECULATIVE_SAME_HOST_RECOVERY']=='STOP'
 assert comparison['PATH_B']['PREFERRED_PROSPECTIVELY'] and not comparison['PATH_B']['QUALIFIED'] and not comparison['PATH_B']['PERMISSIONS_VERIFIED'] and not comparison['CURRENT_EXECUTABLE_DECISION_READY']
 gates=read('readiness-gates.json');assert gates=={'PATH_A_EVIDENCE_COMPLETE':'NO','PATH_A_COMPATIBLE':'UNDETERMINED','PATH_B_REQUIREMENTS_COMPLETE':'YES','PATH_B_PROFILE_COMPLETE':'NO (actual host/kernel/runtime/profile/permission bindings unsealed)','PATH_B_HOST_AVAILABLE':'UNDETERMINED','PATH_B_PERMISSIONS_VERIFIED':'NO','PREFERRED_PATH':'B_INDEPENDENT_QUALIFICATION_HOST_PROSPECTIVE','FRESH_CAMPAIGN_AUTHORITY_READY':'NO','FAKE_PROTOCOL_TEST_READY':'NO','NATIVE_SYNTHETIC_TEST_READY':'NO'}
 stopped=load(E/'grant-state-observation.json');assert not stopped['CURRENT_GRANT_ACTIVE_FOR_FURTHER_CAMPAIGN_OPERATIONS']
 return {'RESULT':'PASS_STATIC_PARTIAL_DECISION','PATH_A_FINDING':'UNDETERMINED; no authoritative compatible profile','PREFERRED_PATH':'B_INDEPENDENT_QUALIFICATION_HOST_PROSPECTIVE','PROFILE_REQUIREMENTS_HASH':canon(profile),'RESOURCE_MATRIX_HASH':canon(matrix),'TRANSFER_CONTRACT_HASH':canon(transfer),'CAMPAIGN_PREREQUISITES_HASH':canon(campaign),'STRATEGY_HASH':canon(comparison),'SOURCE_HASHES':{x['PATH']:x['RAW_SHA256'] for x in profile['SOURCE_FILES']},'READINESS':gates,'TRANSFER_OR_TESTS_EXECUTED':False}
if __name__=='__main__':print(json.dumps(verify(json.load(sys.stdin) if '--candidate' in sys.argv else None),sort_keys=True))
