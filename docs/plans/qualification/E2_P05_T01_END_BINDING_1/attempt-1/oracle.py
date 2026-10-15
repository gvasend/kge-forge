"""Independent expected values from sealed command and boundary specifications.

Never imports the projection builder or restores/executes the source transaction.
"""
from common import *

def expected():
    sel=selection();man=sel['restore_manifest'];path=ROOT/sel['native_bundle']['path']
    raw=read(path)['bundle'];command=read(ROOT/sel['command']['path'])
    # Read immutable native event artifacts independently of embedded event list.
    events=[read(path.parent/('event-'+e['identity']['sha256']+'.json')) for e in raw['events']]
    equal('command agrees with committed operand',events[-2]['result'],command)
    receipt=dict(command['admission']);receipt['attestation']=command['attestation_operand']['attestation']['attestation_id']
    entity=dict(command['entity']);entity.update(validated=False,validation={'$enum':'ValidationState','value':'NOT_EVALUATED'})
    fixed=read(ROOT/sel['independent_oracle']['path'])['semantic_oracle']
    checks=read(ROOT/sel['boundary_oracle']['path'])['A09']
    terms=dict(bundle=man['bundle_id'],snapshot=man['state_id'],evidence=entity,receipt=receipt,
        receipt_identity=c._wire(c._identity(c.canonical_bytes(dict(admission=receipt,ingress_event=events[-2]['identity'],received_event=events[-1]['identity'])),'planner-receipt-admission-reference-v1')),attestation_operand=command['attestation_operand'],
        ingress_operand=command,ingress_event=events[-2],receipt_event=events[-1],ancestry=events,
        ledger_root=fixed['ledger_root'],append_head=man['head'],sources=fixed['sources'],
        policy=fixed['policy'],policy_version=fixed['policy_version'],context=fixed['context'],bundle_scope=raw['scope'],
        post_restore=dict(bundle_trust=True,stage='EVIDENCE_RECEIVED',pending=entity['id']['value'],
            receipt_present=True,receipt_current=True,evidence_native_identity=entity['id']['value'],
            validation=checks['A09_EVIDENCE_NOT_EVALUATED']['expected'],evidence_validated=False,
            control=checks['A09_received_control']['expected'],resume=checks['A09_C03_ineligible']['expected'],
            observations=[],validation_results=[],validation_support=[],typed_proofs=checks['A09_no_Proof_instances']['expected']))
    p=envelope(terms)
    # Independent manifest construction: fixed complete ID/type/source/value inventory.
    ids=['RETAINED_BUNDLE','QUALIFIED_API','SEALED_END_CONTRACT','A09_COMMAND','A09_SNAPSHOT','EVIDENCE','ATTESTATION','RECEIPT','EVENT_ANCESTRY','LEDGER_ROOT_HEAD','SOURCE_POLICY_PINS','POST_RESTORE_ORACLE','CONTEXT','END_PROJECTION','PROCESS_BINDING']
    types=['PersistenceBundle','PinnedNativeAdmissionCapability','RecoveredENDInterfaceContract','EvidenceSourceAdmission','SnapshotIdentity','GraphEntity:EVIDENCE','EvidenceAttestationOperand','ReceiptAdmission','OrderedExecutionEvents','LedgerRootAndAppendHead','CanonicalUnorderedArtifactPins','T01ReceivedBoundaryOracle','EvaluationContext','QualificationProjection','ExplicitColdRestoreProcess']
    artifacts=[sel['native_bundle'],sel['capability'],ref(OUT/'recovered-contract.json'),sel['command'],sel['native_bundle'],sel['native_bundle'],sel['command'],sel['native_bundle'],sel['native_bundle'],sel['native_bundle'],sel['native_bundle'],sel['boundary_oracle'],sel['native_bundle'],ref(OUT/'source-selection.json'),ref(OUT/'process-binding.json')]
    values=[man['bundle_id'],sel['api'],contract(),command,man['state_id'],entity,command['attestation_operand'],receipt,events,[fixed['ledger_root'],man['head']],[fixed['sources'],fixed['policy']],terms['post_restore'],fixed['context'],p['identity'],process()]
    expected_rows=[]
    for i in range(len(ids)):
        expected_rows.append({'INPUT_ID':ids[i],'EXPECTED_TYPE':types[i],'SOURCE_ARTIFACT':artifacts[i],
            'SOURCE_IDENTITY':artifacts[i]['raw_sha256'],'EXPECTED_VALUE':values[i],
            'RESTORE_SOURCE':sel['native_bundle'],'PROJECTION_IDENTITY':p['identity'],
            'CONSUMER':INPUT,'PROCESS':process()['identity'],'SCOPE':contract()['SCOPE'],
            'LINEAGE':sel['context'],'PROVENANCE':sel['primary_sources'],'CURRENTNESS':p['body']['currentness']})
    body={'consumer':INPUT,'process':process()['identity'],'inputs':expected_rows}
    return p,{'body':body,'identity':qid('manifest',body)}

if __name__=='__main__':
    p,inv=expected();save('expected-projection.json',p);save('expected-manifest.json',inv)
    save('oracle-seal.json',dict(projection=ref(OUT/'expected-projection.json'),manifest=ref(OUT/'expected-manifest.json'),method='Fixed sealed expectations + pinned command + independent immutable event readers; no binding import or native transaction'))
    print('INDEPENDENT_ORACLE_SEALED')
