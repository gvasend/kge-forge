"""Seal exact native receipt payload for accepted-support invalidation variant.

Prior fixture revisions are retained. Original metadata-wrapped receipt bytes
were not a current native receipt; no PASS is credited to that premise.
"""
from dataclasses import replace
from pathlib import Path
import hashlib,json,os,sys
from adapter.tests import qualify_p03_prospective as q
from adapter.tests import revise_p03_prospective as r2
from adapter.planner import codec as c,model as m,gates,evidence_attestation as att
REV=q.A/'revision-3-seal.json'

def prepare():
 manifest=r2.verify_revision();info=manifest['fixtures']['accepted-support'];b=q.load_bundle(q.ROOT/info['file']);a=b.current.receipt_admissions[0];e=next(e for e in b.current.entities if e.id==a.artifact)
 body={'producer':c._wire(a.producer),'target':c._wire(a.target),'claims':sorted([c._wire(x)for x in a.claims],key=c.canonical_bytes)};raw=q.jbytes(body);p=q.A/'sources/accepted-native-receipt-payload.json';q.write(p,raw)
 pin=m.ArtifactPin(str(p.relative_to(q.ROOT)),q.identity(raw));pv=m.Provenance(pin.path,pin.identity,'/',raw.decode(),'NATIVE_PROSPECTIVE_RECEIPT_INITIAL_PREMISE',q.SCOPE);old=e.identity
 def rewrite(x):
  if isinstance(x,list):return [rewrite(v)for v in x]
  if isinstance(x,dict):
   if x.get('$type')=='Provenance'and x['identity']==c._wire(old):return c._wire(pv)
   if x.get('$type')=='ArtifactIdentity'and x==c._wire(old):return c._wire(pin.identity)
   return {k:rewrite(v)for k,v in x.items()}
  return x
 s=c._unwire(rewrite(c._wire(b.current)));a=s.receipt_admissions[0];e=next(e for e in s.entities if e.id==a.artifact);pred=next(p for p in s.predicates if p.id==a.authentication);owner=next(x for x in s.entities if x.id==pred.entity)
 req=s.evidence_requirements[0];semantic=q.identity(b'prospective accepted-support semantic evidence','prospective-semantic-evidence-v1');content=q.identity(raw,'prospective-evidence-content-v1')
 bound=att.materialize(attestor_authority=owner.identity,attestor=owner.identity,source_predicate=pred.id,source_pin=e.identity,native_entity=e.id,semantic_evidence=semantic,content=content,proposition=req.proposition,gate=s.external_gates[0].id,scope=q.SCOPE,lineage=q.LINEAGE,provenance=e.provenance.identity)
 s=replace(s,receipt_admissions=(replace(a,attestation=bound.attestation_id),))
 assert gates._check_receipt(s,s.external_gates[0],e.id).state is m.ProofState.PROVED
 b=replace(b,initial=s,current=s,sources=b.sources+(pin,))
 sf=q.A/'revision-3-accepted-support-start.json';of=q.A/'revision-3-accepted-support-oracle.json';q.write(sf,c.bundle_bytes(b))
 oracle=json.loads((q.ROOT/info['oracle']).read_text());oracle.update(start=c._wire(s),checkpoint=c._wire(s),pins=c._wire(b.sources),authority=c._wire(s.entities),receipt_proof_expectation='PROVED',receipt_proof_source='Independent native producer/target/claims contract, actual raw payload pin and newly materialized evidence-bound prospective attestation')
 q.write(of,q.jbytes(oracle))
 updated=dict(manifest);updated['fixtures']=dict(manifest['fixtures']);updated['fixtures']['accepted-support']={'file':str(sf.relative_to(q.ROOT)),'oracle':str(of.relative_to(q.ROOT)),'start_id':c._wire(c.snapshot_id(s)),'source_pins':c._wire(b.sources),'policy':c._wire(b.policy),'bundle_id':c._wire(c.bundle_id(b))}
 record={'schema':'P03-PREEXECUTION-FIXTURE-REVISION-3','previous_revision_seal_sha256':hashlib.sha256(r2.REV.read_bytes()).hexdigest(),'revision':3,'reason':'Native accepted receipt source must be canonical producer/target/claims payload, not metadata wrapper; initial native support explicitly proved before execution','prior_failed_support_comparisons_not_credited':True,'runtime_defect':False,'historical_reconstruction':False,'boundary_and_authority_permissions_changed':False,'fixture_files':[c._wire(m.ArtifactPin(str(x.relative_to(q.ROOT)),q.identity(x.read_bytes())))for x in (sf,of)],'new_source':c._wire(pin),'attestation':c._wire(bound.attestation_id),'manifest':updated,'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'execution_started':False,'all_inputs_sealed_before_revision_execution':True}
 q.write(REV,q.jbytes(record));print(json.dumps({'revision_seal':str(REV),'fixture_id':c._wire(q.identity(REV.read_bytes(),'planner-prospective-fixture-v1'))}))

def verify_revision():
 r2.verify_revision();r=json.loads(REV.read_text());assert r['execution_started']is False and r['all_inputs_sealed_before_revision_execution']
 assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest()==r['driver_sha256']
 for w in r['fixture_files']+[r['new_source']]:c.load_pinned(q.ROOT,c._unwire(w))
 for info in r['manifest']['fixtures'].values():
  b=q.load_bundle(q.ROOT/info['file']);assert c.bundle_id(b)==c._unwire(info['bundle_id']);c._verify_sources(b,q.ROOT)
 return r['manifest']

def writer(label):
 from adapter.tests.run_p03_prospective import dependency_ordered_load
 q.load_bundle=dependency_ordered_load;q.verify_seal=verify_revision
 manifest=verify_revision();b=q.load_bundle(q.ROOT/manifest['fixtures']['accepted-support']['file']);e=next(e for e in b.current.entities if e.kind is m.EntityKind.EVIDENCE)
 assert gates._check_receipt(b.current,b.current.external_gates[0],e.id).state is m.ProofState.PROVED
 q.write(q.A/'runs'/label/'driver-seal.json',q.jbytes({'schema':'P03-REVISION-3-PRE-RUN-SEAL','revision_seal_sha256':hashlib.sha256(REV.read_bytes()).hexdigest(),'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'execution_started':False,'sources_and_oracle_fixed_before_execution':True,'initial_native_receipt_support':'PROVED'}));q.writer(label)

if __name__=='__main__':
 os.chdir(q.ROOT)
 if sys.argv[1]=='prepare':prepare()
 else:writer(sys.argv[1])
