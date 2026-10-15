"""Read-only pin/retained evidence authentication; writes qualification metadata only."""
import pathlib,json,hashlib
E=pathlib.Path(__file__).parent;Q=E.parent
read=lambda p:json.loads(pathlib.Path(p).read_text())
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
auth=read(E/'authentication.json')
for p,h in read(Q/'E2_P05_D01_A15_INDEPENDENT_AFTER_STATE_ORACLE_60/authentication.json')['AUTHORITATIVE_FILES'].items():
 assert sha(p)==h,(p,h,sha(p));auth['FILES'][p]=h
for p,h in read(Q/'E2_P05_D01_A14_RUNTIME_PERSISTENCE_QUALIFICATION_31/evidence-index.json')['FILES'].items():
 assert sha(p)==h,(p,h,sha(p));auth['FILES'][p]=h
bundle=read(Q/'E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2/fixtures/D01-VARIANT__E2-A15__CANONICAL_REQUIRED_BEHAVIOR.json')['canonical_content']['bundle']
rows=[]
for pin in bundle['sources']+[bundle['policy']]:
 p=pathlib.Path(pin['path']);assert pin['profile']['value']=='raw-file-sha256' and not pin.get('pointer')
 assert p.resolve()==p.absolute() and sha(p)==pin['identity']['sha256']
 auth['FILES'][str(p)]=sha(p);rows.append({'PATH':str(p),'CONTENT_IDENTITY':pin['identity'],'RESULT':'PASS'})
assert len(rows)==55
(E/'source-policy-pin-verification.json').write_text(json.dumps({'PIN_IDENTITIES':55,'BUNDLE_SOURCE_IDENTITIES':54,'POLICY_IDENTITIES':1,'ROWS':rows,'RESULT':'PASS','INVALIDATION_TARGET_MEMBERSHIP_INFERRED':False},sort_keys=True,indent=2)+'\n')
auth['A14_RETAINED_EVIDENCE_AUTHENTICATED']=True;auth['A14_EXECUTION_AUTHORITY_REUSED']=False
(E/'authentication.json').write_text(json.dumps(auth,sort_keys=True,indent=2)+'\n')
print(json.dumps({'AUTHENTICATED_FILES':len(auth['FILES']),'PIN_IDENTITIES':55}))
