"""Bind only fully determined native bundle inputs and trusted commitments."""
import json,hashlib,runpy
from pathlib import Path
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;Q=O.parent;C4=Q/'E2_P05_D01_OPERAND_RECONCILIATION_4';C5=Q/'E2_P05_D01_A14_HANDOFF_CLOSURE_5'
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p,ptr=''):return {'path':str(p.relative_to(R)),'pointer':ptr,'raw_sha256':sha(p.read_bytes())}
def save(n,v):(O/n).write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
runpy.run_path(str(C4/'verify.py'),run_name='__original_52_reconstruction__')
validation=read(O/'bundle-validation.json');candidate=R/validation['CANDIDATE']['path'];assert sha(candidate.read_bytes())==validation['BUNDLE_ID']['sha256']
old=read(C4/'resolved-bindings.json');resolved=old['PRESERVED_39']+old['NEW_BINDINGS'];remaining=read(C4/'remaining-frontier.json')['ROWS'];deps=read(C5/'a14-dependency-inventory.json')['ROWS'];assert len(resolved)==52 and len(remaining)==59
new=[];pending=[]
for row in remaining:
 for source in row['PROVENANCE']:assert sha((R/source['path']).read_bytes())==source['raw_sha256']
 if row['CASE_ID']=='E2-A14' and row['OPERAND_NAME'] in ['bundle','expected_bundle_identity']:
  value={'SOURCE':pin(candidate,'/bundle'),'NATIVE_TYPE':'PersistenceBundle','SOURCE_IDENTITY':validation['BUNDLE_ID'],'DERIVATION':'Exact pinned complete candidate -> native decode; no operation/save/restore'} if row['OPERAND_NAME']=='bundle' else {'SOURCE':pin(candidate),'NATIVE_TYPE':'TrustedArtifactIdentity','SOURCE_IDENTITY':validation['BUNDLE_ID'],'VALUE':validation['BUNDLE_ID'],'DERIVATION':'Externally sealed pre-execution commitment over complete native bundle bytes; C5 permits independent precommitment, not an invented save-return result'}
  new.append({**row,'STATUS':'RESOLVED','CURRENT_GAP':None,'RESOLUTION_PACKAGE':'CLOSURE26','VALUE_BINDING':value,'SCOPE':'E2-QUALIFICATION-ONLY','LINEAGE':'E2-CANONICAL-BASELINE-1','GENERATION':'E2-GENERATION-1','PROVENANCE':[pin(candidate),pin(O/'p06-policy-binding.json'),pin(O/'replay-scope-binding.json')],'CURRENTNESS':'Exact current source/model/policy and authorized frame pins','OPERATION_EXECUTED':False})
 else:pending.append(row)
assert len(new)==4 and len(pending)==55 and len(resolved)+len(new)+len(pending)==111
save('resolved-by-bundle.json',{'ROWS':new,'COUNT':4,'BUNDLE_OPERANDS':2,'EXPECTED_BUNDLE_IDENTITY_PRECOMMITMENTS':2,'NO_SAVE_OUTPUT_PRESUPPLIED':True})
snapshot_source=read(Q/'E2_P05_D01_A14_PROVENANCE_FIXTURE_CORRECTION_7/corrected-prospective-fixture.json')['SNAPSHOT_SOURCE']
save('a14-effective-invocation-overrides.json',{'ROWS':[{'OBLIGATION_ID':oid,'SNAPSHOT_OPERAND':{**snapshot_source,'pointer':'/snapshot'},'SNAPSHOT_IDENTITY':validation['INITIAL_CURRENT_SNAPSHOT'],'BUNDLE_OPERAND':pin(candidate,'/bundle'),'EXPECTED_BUNDLE_IDENTITY_PRECOMMITMENT':validation['BUNDLE_ID'],'BUNDLE_PATH':'UNRESOLVED_FUTURE_SAVE_RETURN_HANDOFF','SOURCE_ROOT':str(R),'SCOPE':'E2-QUALIFICATION-ONLY','LINEAGE':'E2-CANONICAL-BASELINE-1','GENERATION':'E2-GENERATION-1','RULE':'Use the already-authorized active corrected Snapshot for recompute and the same native frame Snapshot for save; original 117 capsules are immutable historical structural inputs, not silently edited.'} for oid in ['D01-OBL:E2-A14_OPERANDS','D01-OBL:E2-A14_ORACLE']],'ORIGINAL_117_CAPSULES_MODIFIED':False,'FROZEN_52_BINDINGS_MODIFIED':False,'CROSS_OPERAND_SNAPSHOT_BUNDLE_IDENTITY':'PASS','OPERATIONS_EXECUTED':0})
key=lambda r:(r['OBLIGATION_ID'],r['DISPATCH_ID'],r['CAPSULE_ID'],r['OPERAND_NAME']);keys={key(r) for r in new};a14=[]
for row in deps:
 if key(row) in keys:status='RESOLVED';reason='Exact complete native bundle input or independently sealed identity commitment now available'
 elif row['OPERAND_NAME']=='bundle_path':status='STILL_BLOCKED_BY_SAVE';reason='Future actual save artifact and persisted save-return handoff still unsealed. Candidate evidence file is not substituted for that writer/reader boundary.'
 else:status='OTHER';reason=row['CURRENT_GAP']+'; post-restore boundary/mutation realization is still not qualified'
 a14.append({'REFERENCE':row,'STATUS':status,'REASON':reason})
save('a14-dependent-audit.json',{'ROWS':a14,'COUNT':16,'RESOLVED_BY_BUNDLE':4,'STILL_UNRESOLVED':12})
save('full-111-reference-audit.json',{'FROZEN_52':resolved,'RESOLVED_NEW':new,'UNRESOLVED':pending,'PREVIOUSLY_RESOLVED':52,'RESOLVED_BY_POLICY':0,'RESOLVED_BY_REPLAY_SCOPE':0,'RESOLVED_BY_BUNDLE':4,'TOTAL_RESOLVED':56,'TOTAL_UNRESOLVED':55,'AUDITED_REFERENCES':111,'INVOCATION_STATIC_PREFLIGHT':'NOT_RUN','FULL_OUTPUT_ORACLES':'0/128'})
save('save-gate-and-next-blocker.json',{'SAVE_PREFLIGHT_ELIGIBLE':True,'SAVE_PERFORMED':False,'SAVE_PREFLIGHT':'NOT_RUN_NOT_REQUESTED_TO_REPAIR_NEXT_BLOCKER','FIRST_REMAINING_BLOCKER':{'CLASSIFICATION':'SAVE_CONTRACT','DETAIL':'Seal exact native bundle input-to-future save-return path/identity publication and persisted writer-termination/reader handoff. Existing candidate bytes/precommitment do not prove a performed save or the required cold-reader source.'},'KNOWN_STATIC_RULES':read(C5/'save-contract.json'),'SCOPE_NOTE':'No save invocation, no future store directory created, no native restore or qualification reader launched'})
print(json.dumps({'AUDIT':'111/111','NEW_BUNDLE_BINDINGS':4,'COUNTS':'56/55','SAVE_PREFLIGHT_ELIGIBLE':True,'FIRST_BLOCKER':'SAVE_CONTRACT'}))
