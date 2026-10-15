"""File/canonical qualification helpers. No native operation execution."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent
D=ROOT/'docs/plans';Q=D/'qualification';P='DETERMINISTIC_PLANNER_V0_1_'
PRIOR=Q/'E2_P05_D01_PROSPECTIVE_MATRIX_CONTRACT_1'
TYPE='PROSPECTIVE_D01_RUNNER_MATRIX'
def read(p):return json.loads(Path(p).read_bytes())
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def filehash(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def qid(kind,x):return 'qualification-prospective-D01-'+kind+'-v1:'+digest(x)
def ref(p,pointer=''):
 p=Path(p);return dict(path=str(p.relative_to(ROOT)),pointer=pointer,raw_sha256=filehash(p))
def at(x,pointer):
 for t in pointer.split('/')[1:]:x=x[int(t)] if isinstance(x,list) else x[t.replace('~1','/').replace('~0','~')]
 return x
class Reject(ValueError):pass
def demand(x,message):
 if not x:raise Reject(message)
def save(name,x):
 p=OUT/name;p.parent.mkdir(exist_ok=True,parents=True);p.write_bytes(canonical(x)+b'\n')
# Closed native registry: every semantic operation remains a native implementation.
OPERATIONS={
 'MODEL_VALIDATE':('adapter.planner.model','validate_model','Snapshot','None','NONE','NONE'),
 'RECOMPUTE':('adapter.planner.core','recompute','Snapshot','Computation','NONE','NONE'),
 'APPLY_RESULT':('adapter.planner.core','apply_result','Snapshot,SuppliedResult','TransitionReport','IN_MEMORY_NATIVE_RESULT','NONE'),
 'DOSSIER_RESULT':('adapter.planner.core','admit_dossier_materialization','Snapshot,SuppliedResult,ValidationInstanceTuple','TransitionReport','IN_MEMORY_NATIVE_T02_RESULT','HISTORICAL_NATIVE_OUTCOMES_ONLY'),
 'RECORD_RESULT':('adapter.planner.codec','record_result','PersistenceBundle,TypedResult','PersistenceBundle','IN_MEMORY_NATIVE_EVENT_APPEND','NATIVE_LEDGER_VALIDATION'),
 'RECORDED_DECISION':('adapter.planner.core','apply_recorded_decision','Snapshot,RecordedDecision','TransitionReport','IN_MEMORY_NATIVE_DECISION','NONE'),
 'APPLY_EVENT':('adapter.planner.core','apply_event','Snapshot,TypedEvent','TransitionReport','IN_MEMORY_NATIVE_EVENT','NONE'),
 'RECEIPT_PHASE':('adapter.planner.core','apply_receipt','Snapshot,ExternalEvent','TransitionReport','IN_MEMORY_NATIVE_LIFECYCLE','NONE'),
 'SAVE_BUNDLE':('adapter.planner.codec','save_bundle','PersistenceBundle,Store,SourceRoot','Path,ArtifactIdentity','IMMUTABLE_NATIVE_PERSISTENCE','NATIVE_LEDGER_VALIDATION'),
 'RESTORE':('adapter.planner.codec','restore','Path,TrustedArtifactIdentity,SourceRoot','PersistenceBundle','NONE','NATIVE_HISTORICAL_REPLAY'),
 'EVIDENCE_ADMISSION':('adapter.planner.codec','admit_external_evidence','PersistenceBundle,EvidenceSourceAdmission,SourceBytes,Store,SourceRoot','PersistenceBundle,ArtifactIdentity,Bool','NATIVE_ATOMIC_RECEIPT_TRANSACTION','NATIVE_HISTORICAL_REPLAY'),
 'EVIDENCE_APPLY':('adapter.planner.evidence','apply','Snapshot,EvidenceSourceAdmission','TransitionReport','IN_MEMORY_NATIVE_ADMISSION','NONE'),
 'VALIDATION_APPLY':('adapter.planner.validation_transaction','apply','Snapshot,ValidationSupportAdmission','TransitionReport','IN_MEMORY_NATIVE_VALIDATION','NONE'),
 'VALIDATION_COMMIT':('adapter.planner.validation_transaction','commit','PersistenceBundle,ValidationSupportAdmission,Store,SourceRoot','PersistenceBundle,ArtifactIdentity,Bool','NATIVE_VALIDATION_TRANSACTION','NATIVE_HISTORICAL_REPLAY'),
 'RESUME':('adapter.planner.core','resume_eligibility','PersistenceBundle,SourceRoot','ResumeEligibility','NONE','NATIVE_CURRENT_ELIGIBILITY_CHECK'),
 'SATISFACTION':('adapter.planner.core','evaluate_satisfaction','Snapshot','Snapshot','PURE_NATIVE_PROOF_PROJECTION','NONE'),
 'INVALIDATE_EVENT':('adapter.planner.core','apply_event','Snapshot,SourceInvalidation','TransitionReport','IN_MEMORY_NATIVE_INVALIDATION','NONE'),
 'PREDICATE':('adapter.planner.gates','evaluate_predicate','Snapshot,PredicateId','Proof','NONE','NONE'),
 'LOAD_PIN':('adapter.planner.codec','load_pinned','SourceRoot,ArtifactPin','BytesOrJSON','NONE','NONE'),
 'VALIDATE_PIN':('adapter.planner.codec','validate_pin','ArtifactPin','None','NONE','NONE'),
 'VALIDATE_POLICY':('adapter.planner.selector','validate_policy','ArtifactPin,PolicyVersion','PolicyBinding','NONE','NONE'),
 'BUNDLE_VALIDATE':('adapter.planner.codec','bundle_bytes','PersistenceBundle,SnapshotResolver','Bytes','NONE','NATIVE_HISTORICAL_REPLAY'),
 'SNAPSHOT_ID':('adapter.planner.codec','snapshot_id','Snapshot','ArtifactIdentity','NONE','NONE'),
 'BUNDLE_ID':('adapter.planner.codec','bundle_id','PersistenceBundle,SnapshotResolver','ArtifactIdentity','NONE','NATIVE_HISTORICAL_REPLAY'),
 'COMMIT_EVENT':('adapter.planner.codec','commit_event','PersistenceBundle,TypedEvent,Store,SourceRoot','PersistenceBundle,ArtifactIdentity,Bool','NATIVE_DURABLE_EVENT_TRANSACTION','NATIVE_HISTORICAL_REPLAY'),
 'QUALIFICATION_METADATA':(None,None,'PinnedQualificationMetadata','ValidatedQualificationMetadata','NONE','NONE')}
POSITIVE={'E2-A01':['MODEL_VALIDATE'],'E2-A02':['RECOMPUTE'],'E2-A03':['COMMIT_EVENT'],'E2-A04':['DOSSIER_RESULT'],'E2-A05':['COMMIT_EVENT'],'E2-A06':['COMMIT_EVENT','COMMIT_EVENT'],'E2-A07':['SAVE_BUNDLE'],'E2-A08':['RESTORE'],'E2-A09':['EVIDENCE_ADMISSION'],'E2-A10':['VALIDATION_COMMIT'],'E2-A11':['COMMIT_EVENT','COMMIT_EVENT','RESUME'],'E2-A12':['COMMIT_EVENT'],'E2-A13':['COMMIT_EVENT','COMMIT_EVENT'],'E2-A14':['RECOMPUTE','SAVE_BUNDLE','RESTORE'],'E2-A15':['INVALIDATE_EVENT'],'E2-A16':['INVALIDATE_EVENT']}
NEGATIVE={'E2-N01':['RECOMPUTE'],'E2-N02':['EVIDENCE_APPLY'],'E2-N03':['EVIDENCE_APPLY'],'E2-N04':['INVALIDATE_EVENT','RESUME'],'E2-N05':['LOAD_PIN','VALIDATE_PIN'],'E2-N06':['PREDICATE','RECOMPUTE'],'E2-N07':['SATISFACTION'],'E2-N08':['MODEL_VALIDATE'],'E2-N09':['INVALIDATE_EVENT','RECOMPUTE'],'E2-N10':['VALIDATE_POLICY'],'E2-N11':['RESTORE'],'E2-N12':['APPLY_EVENT'],'E2-N13':['APPLY_EVENT'],'E2-N14':['APPLY_EVENT'],'E2-N15':['RESUME'],'E2-N16':['RECOMPUTE']}
def operation_path(name):
 if name.startswith('E2-'):
  return dict(POSITIVE,**NEGATIVE)[name.split('_')[0]]
 if name.startswith('PHASE_'):return ['RESTORE','RECOMPUTE'] if name=='PHASE_COLD_RESTORED' else ['RECOMPUTE']
 if name.startswith(('INVALIDATE_','MUTATION_')):return ['INVALIDATE_EVENT','RECOMPUTE'] if name.startswith('INVALIDATE_') else ['MODEL_VALIDATE','RECOMPUTE']
 if name.startswith('CONTROL_'):return ['MODEL_VALIDATE','RECOMPUTE']
 if name in ['TRUSTED_NATIVE_BUNDLES','ORDERED_EVENT_ANCESTRY']:return ['BUNDLE_VALIDATE']
 if name=='POST_SNAPSHOT_ARCHIVES':return ['MODEL_VALIDATE']
 if name=='SOURCE_BYTES':return ['LOAD_PIN']
 if name=='POLICY':return ['VALIDATE_POLICY']
 if name=='CONTEXT_AND_DEFINITIONS':return ['MODEL_VALIDATE']
 if name=='COLD_READER_PROCESS':return ['RESTORE','RECOMPUTE']
 if name=='WRITER_PROCESS':return ['SAVE_BUNDLE']
 if name.startswith(('PERMUTE_','EXPECTED_')):return ['RECOMPUTE']
 return ['QUALIFICATION_METADATA']
