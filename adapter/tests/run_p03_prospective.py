"""Dependency-ordered execution of the immutable prospective fixture.

The original runner traversed a native UNORDERED proof definition collection.
This harness permutes that collection SLOT-first as required by the sealed
contract's support dependencies. No source, contract, oracle or pin changes.
"""
from dataclasses import replace
import hashlib,json,os,sys
from pathlib import Path
from adapter.tests import qualify_p03_prospective as q
from adapter.planner import codec as c, model as m
original_load=q.load_bundle

def dependency_ordered_load(path):
 b=original_load(path)
 def ordered(s):return replace(s,proof_contracts=tuple(sorted(s.proof_contracts,key=lambda p:(0 if p.proof_type is m.TypedProofKind.SLOT_PROOF else 1,p.id.sha256))))
 ordered_bundle=replace(b,initial=ordered(b.initial),current=ordered(b.current))
 assert c.bundle_id(ordered_bundle)==c.bundle_id(b)
 return ordered_bundle

if __name__=='__main__':
 os.chdir(q.ROOT);q.verify_seal()
 driver={'schema':'P03-PRE-RUN-DRIVER-SEAL-1','driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'fixture_seal_sha256':hashlib.sha256((q.A/'seal-final.json').read_bytes()).hexdigest(),'purpose':'Correct qualification driver ordering for an explicitly unordered collection; all fixture/policy/source/oracle pins unchanged','planned_event_order':['native seal-witness reevaluation','native RecordedDecision at mainline','SLOT_PROOF then ROOT_PROOF in isolated support variant'],'no_runtime_change':True,'sequence':1,'execution_started':False}
 q.write(q.A/'runs'/sys.argv[1]/'driver-seal.json',q.jbytes(driver))
 q.load_bundle=dependency_ordered_load
 q.writer(sys.argv[1])
