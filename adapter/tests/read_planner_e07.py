"""Fresh E07 reader: only sealed manifests, native bundles and pinned sources."""
import json,os
from pathlib import Path
from adapter.planner import codec as c,model as m,evidence_attestation as ea
R=Path(__file__).resolve().parents[2];O=R/'docs/plans/qualification/EVIDENCE_E07_1'
def forbidden(**args):raise AssertionError('Replay attempted a new attestation decision')
ea.materialize=forbidden
spec=json.loads((O/'generic-qualification.json').read_text());bid=c._unwire(spec['bundle_id']);root=R/spec['repo_root']
b=c.restore(R/spec['bundle'],bid,root);start=c.restore(R/spec['start_bundle'],c._unwire(spec['start_bundle_id']),root)
r=b.events[-2].result;a=b.current.receipt_admissions[0];t=r.attestation_operand.attestation
checks={
 'bundle_identity':c.bundle_id(b)==bid,
 'state_identity':c.snapshot_id(b.current)==c._unwire(spec['state_id']),
 'replay':c.snapshot_id(c._replay(b))==c.snapshot_id(b.current),
 'precommit_prefix':c.bundle_bytes(c._prefix_bundle(b,len(start.events)))==c.bundle_bytes(start),
 'prefix_has_no_evidence_or_attestation':not start.current.receipt_admissions,
 'one_evidence':len([e for e in b.current.entities if e.kind is m.EntityKind.EVIDENCE])==1,
 'one_attestation':a.attestation==t.attestation_id,
 'exact_recorded_operand':r.attestation_operand.expected_parent_event==start.events[-1].identity,
 'one_receipt':len(b.current.receipt_admissions)==1,
 'no_validation':not b.current.receipt_observations,
 'received_stage':b.current.external_gates[0].stage is m.ExternalStage.EVIDENCE_RECEIVED,
 'event_parent':b.events[-2].parent_event==start.events[-1].identity,
 'source_provenance':a.provenance==r.entity.provenance,
 'scope_lineage':(t.scope,t.lineage)==(b.current.context.scope,b.current.context.lineage),
 'source_pin':t.source_pin==a.producer,
 'four_records':len(a.dependencies)==4,
 'semantic_binding':t.semantic_evidence==r.attestation_operand.binding.semantic_evidence_id,
 'content_binding':t.content==r.attestation_operand.binding.content_id,
}
assert all(checks.values()),checks
print(json.dumps({'reader_pid':os.getpid(),'writer_pid':spec['writer_pid'],'hash_seed':os.environ['PYTHONHASHSEED'],'checks':checks,'no_new_attestation_decision':True},sort_keys=True))
