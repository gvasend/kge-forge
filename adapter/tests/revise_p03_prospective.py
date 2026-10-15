"""Immutable pre-execution revision for native resolution-contract encoding.

Preserves failed original fixtures/results. New revision adopts exact existing
native ExternalResolutionContract source grammar; no oracle/control expectation,
authority permission, policy, historical artifact or runtime code is changed.
"""
from dataclasses import replace
from pathlib import Path
import hashlib,json,os,sys
from adapter.tests import qualify_p03_prospective as q
from adapter.planner import codec as c, core
BASE_VERIFY=q.verify_seal
REV=q.A/'revision-2-seal.json'

def prepare():
 manifest=BASE_VERIFY();info=manifest['fixtures']['unknown'];b=q.load_bundle(q.ROOT/info['file']);gate=b.current.external_gates[0];route=gate.resolution_contracts[0]
 body=c._wire(route);body.pop('$type');body.pop('provenance');raw=q.jbytes({'schema':'EXTERNAL-RESOLUTION-CONTRACT-1','contract':body})
 p=q.A/'sources/unknown-native-resolution-contract.json';q.write(p,raw)
 pin=q.m.ArtifactPin(str(p.relative_to(q.ROOT)),q.identity(raw));prov=q.m.Provenance(pin.path,pin.identity,'/',raw.decode(),'NATIVE_PROSPECTIVE_RESOLUTION_CONTRACT',q.SCOPE)
 r=replace(route,provenance=prov);state=replace(b.current,external_gates=(replace(gate,resolution_contracts=(r,)),));b=replace(b,initial=state,current=state,sources=b.sources+(pin,))
 # All values follow the preexisting native contract grammar. Expected control
 # remains EXTERNAL_WAIT, authored before any run of this revision.
 oracle=json.loads((q.ROOT/info['oracle']).read_text());oracle.update(start=c._wire(state),checkpoint=c._wire(state),pins=c._wire(b.sources),authority=c._wire(state.entities))
 sf=q.A/'revision-2-unknown-start.json';of=q.A/'revision-2-unknown-oracle.json';q.write(sf,c.bundle_bytes(b));q.write(of,q.jbytes(oracle))
 assert core.recompute(state).control.value=='EXTERNAL_WAIT'
 updated=dict(manifest);updated['fixtures']=dict(manifest['fixtures']);updated['fixtures']['unknown']={'file':str(sf.relative_to(q.ROOT)),'oracle':str(of.relative_to(q.ROOT)),'start_id':c._wire(c.snapshot_id(state)),'source_pins':c._wire(b.sources),'policy':c._wire(b.policy),'bundle_id':c._wire(c.bundle_id(b))}
 record={'schema':'P03-PREEXECUTION-FIXTURE-REVISION-2','base_seal_sha256':hashlib.sha256((q.A/'seal-final.json').read_bytes()).hexdigest(),'revision':2,'reason':'Replace invalid generic metadata wrapper with exact native ExternalResolutionContract canonical source body','prior_attempts_preserved':['writer-a','writer-b','corrected-a','corrected-b'],'failed_native_oracle':'UNQUALIFIED_EXTERNAL_CONTRACT:E2-GATE; PLAN_DEFECT','runtime_defect':False,'historical_reconstruction':False,'expectations_changed':False,'permissions_changed':False,'sources_and_policy_unchanged_except_native_resolution_contract_encoding':True,'fixture_files':[c._wire(q.m.ArtifactPin(str(x.relative_to(q.ROOT)),q.identity(x.read_bytes())))for x in (sf,of)],'new_source':c._wire(pin),'manifest':updated,'revision_driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'ordered_driver_sha256':hashlib.sha256((q.ROOT/'adapter/tests/run_p03_prospective.py').read_bytes()).hexdigest(),'all_revision_inputs_sealed_before_revision_execution':True,'execution_started':False}
 q.write(REV,q.jbytes(record));print(json.dumps({'revision_seal':str(REV),'fixture_id':c._wire(q.identity(REV.read_bytes(),'planner-prospective-fixture-v1'))}))

def verify_revision():
 BASE_VERIFY();r=json.loads(REV.read_text());assert r['execution_started']is False and r['all_revision_inputs_sealed_before_revision_execution']
 assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest()==r['revision_driver_sha256']
 assert hashlib.sha256((q.ROOT/'adapter/tests/run_p03_prospective.py').read_bytes()).hexdigest()==r['ordered_driver_sha256']
 for w in r['fixture_files']+[r['new_source']]:c.load_pinned(q.ROOT,c._unwire(w))
 for info in r['manifest']['fixtures'].values():
  b=q.load_bundle(q.ROOT/info['file']);assert c.bundle_id(b)==c._unwire(info['bundle_id']);c._verify_sources(b,q.ROOT)
 return r['manifest']

def writer(label):
 from adapter.tests.run_p03_prospective import dependency_ordered_load
 q.load_bundle=dependency_ordered_load;q.verify_seal=verify_revision
 record={'schema':'P03-REVISION-2-PRE-RUN-SEAL','revision_seal_sha256':hashlib.sha256(REV.read_bytes()).hexdigest(),'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'execution_started':False,'sources_and_oracle_fixed_before_execution':True}
 q.write(q.A/'runs'/label/'driver-seal.json',q.jbytes(record));q.writer(label)

if __name__=='__main__':
 os.chdir(q.ROOT)
 if sys.argv[1]=='prepare':prepare()
 else:writer(sys.argv[1])
