"""Independent effective-pointer reader. Documentary processes only."""
import hashlib,json,os,pathlib,subprocess
R=pathlib.Path(__file__).resolve().parents[5];O=pathlib.Path(__file__).parent

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
ref=read(O/'effective-launch-actor-interpretation-reference.json');assert ref['GOVERNANCE_INTERPRETATION_EFFECTIVE'] and not ref['PROBE_EXECUTION_AUTHORIZED'] and not ref['CONSTRUCTION_AUTHORITY_ISSUED'] and not ref['TECHNICAL_ENFORCEMENT_VERIFIED'] and not ref['HOST_WIDE_TECHNICAL_EXCLUSIVITY_CLAIM'] and ref['QUALIFIED_CONTROLLER_IDENTITY'] is None
for p in ref['VERIFICATION_PINS']:assert sha(R/p['path'])==p['raw_sha256']
p=ref['ADOPTION_RECORD_PIN'];assert sha(R/p['path'])==p['raw_sha256'];record=read(R/p['path']);assert hashlib.sha256(enc(record['CONTENT'])).hexdigest()==ref['ADOPTION_RECORD_IDENTITY']['sha256'];assert record['CONTENT']['STATUS']=='ADOPTION_RECORDED_PENDING_INDEPENDENT_EFFECTIVENESS_VERIFICATION'
# Reconstruct the immutable qualified prefix from pinned bytes, not construction-era
# source-absence predicates. Future authorized construction does not revoke this policy.
old=read(O/'independent-static-verification.json');core=old['RECONSTRUCTION']
for name,expected_sha in core['CONTRACT_PINS'].items():assert sha(O/name)==expected_sha
assert hashlib.sha256(enc(core)).hexdigest()==old['SEMANTIC_SHA256']
decl=read(O/'owner-declaration-content.json');iw=read(O/'interpretation-content.json');approval=read(O/'owner-approval-record.json')
for document in (decl,iw,approval):assert hashlib.sha256(enc(document['CONTENT'])).hexdigest()==document['IDENTITY']['sha256']
assert decl['IDENTITY']==ref['OWNER_DECLARATION_IDENTITY'] and iw['IDENTITY']==ref['INTERPRETATION_IDENTITY'] and approval['IDENTITY']==ref['OWNER_APPROVAL_IDENTITY']
assert decl['CONTENT']['OTHER_ACTORS_MAY_EXERCISE_GRANT']=='NO' and decl['CONTENT']['PROBE_EXECUTION_AUTHORIZED']=='NO' and decl['CONTENT']['HOST_WIDE_TECHNICAL_EXCLUSIVITY_CLAIM']=='NO'
assert iw['CONTENT']['DECLARATION']==decl['CONTENT'] and iw['CONTENT']['CHARTER_BINDING']==ref['CHARTER_BINDING']
conflict=read(O/'interpretation-conflict-audit.json');assert conflict['RESULT']=='PASS' and not conflict['OTHER_SAME_TYPE_SCOPE_DECLARATIONS']
lifecycle=read(O/'governance-lifecycle-finalization.json');assert lifecycle['GOVERNANCE_INTERPRETATION_EFFECTIVE'] and lifecycle['CHARTER_LIFECYCLE_UNCHANGED'];assert sha(R/lifecycle['EFFECTIVE_REFERENCE_PIN']['path'])==lifecycle['EFFECTIVE_REFERENCE_PIN']['raw_sha256']
semantic={'EFFECTIVE_REFERENCE_RAW_SHA256':sha(O/'effective-launch-actor-interpretation-reference.json'),'INTERPRETATION_IDENTITY':ref['INTERPRETATION_IDENTITY'],'ADOPTION_RECORD_IDENTITY':ref['ADOPTION_RECORD_IDENTITY'],'OWNER_DECLARATION_IDENTITY':ref['OWNER_DECLARATION_IDENTITY'],'QUALIFIED_CORE_PREFIX_SHA256':old['SEMANTIC_SHA256'],'GOVERNANCE_INTERPRETATION_EFFECTIVE':True,'PROBE_EXECUTION_AUTHORIZED':False,'CONSTRUCTION_AUTHORITY_ISSUED':False,'TECHNICAL_ENFORCEMENT_VERIFIED':False,'CONSTRUCTION_DECISION_READY':False,'NUMERIC_BUDGET_COMPLETE':False}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':semantic,'SEMANTIC_SHA256':hashlib.sha256(enc(semantic)).hexdigest()},sort_keys=True))
