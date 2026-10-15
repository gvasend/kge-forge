from pathlib import Path
import hashlib,json,re,importlib.abc,importlib.util,sys,unittest
R=Path(__file__).resolve().parents[2];O=R/'docs/plans/qualification/EVIDENCE_E07_1';hashes=json.loads((O/'pre-work-hashes.json').read_text());codes={}
for name in ('model','codec','evidence','evidence_attestation','evidence_materializer','authentication_installation'):
 codes[name]=(R/('adapter/planner/'+name+'.py')).read_text()
m=codes['model'];a=m[m.index('@dataclass(frozen=True)\nclass EvidenceBoundAttestation:'):m.index('\n\n@dataclass(frozen=True)\nclass SemanticNativeBinding:')];b=m[m.index('@dataclass(frozen=True)\nclass SemanticNativeBinding:'):m.index('\n\n@dataclass(frozen=True)\nclass EvidenceAttestationOperand:')]
for ref in ('ArtifactIdentity','EntityId','PredicateId','GateId'):
 a=re.sub(r'(?<=: )'+ref+r'\b','m.'+ref,a);b=re.sub(r'(?<=: )'+ref+r'\b','m.'+ref,b)
codes['model']=m[:m.index('@dataclass(frozen=True)\nclass EvidenceBoundAttestation:')]+m[m.index('@dataclass(frozen=True)\nclass EvidenceSourceAdmission:'):]
codes['model']=codes['model'].replace('    attestation_operand: Optional[EvidenceAttestationOperand] = None\n','').replace('    # E07 preserves the full typed witness in the committed ingress event.\n','')
codes['evidence']=codes['evidence'].replace('    from .evidence_transaction import validate as validate_operand\n    evidence_attestation = validate_operand(snapshot,event,contract,evidence_attestation)\n','')
codes['authentication_installation']=codes['authentication_installation'].replace('ea.identity(**fields)==attestation.attestation_id','ea.materialize(**fields)==attestation')
codes['evidence_materializer']=codes['evidence_materializer'].replace('SemanticNativeBinding = m.SemanticNativeBinding',b)
s=codes['evidence_attestation'];s=s.replace('import hashlib\n','from dataclasses import dataclass\nimport hashlib\n').replace('EvidenceBoundAttestation = m.EvidenceBoundAttestation',a).replace('def identity(*,','def materialize(*,')
s=s[:s.index('\n\ndef materialize(**fields):')]+s[s.index('\ndef validate('):]
s=s.replace('    return aid','    return EvidenceBoundAttestation(aid,attestor_authority,attestor,source_predicate,source_pin,native_entity,semantic_evidence,content,proposition,gate,scope,lineage,provenance)')
codes['evidence_attestation']=s
s=codes['codec'];hs=s.index('def preflight_external_evidence(');he=s.index('def admit_external_evidence(',hs);helper=s[hs:he];body=helper[helper.index('    if request.expected_parent_event'):helper.index('    return updated')];body='\n'.join('    '+line if line else '' for line in body.splitlines())+'\n'
s=s[:hs]+s[he:];s=s.replace('def admit_external_evidence(bundle, request, source_bytes, output_dir, repo_root, *, expected_binding=None):','def admit_external_evidence(bundle, request, source_bytes, output_dir, repo_root):')
s=s.replace('    from .evidence_transaction import trusted_binding\n    trusted_binding(request,expected_binding)\n','').replace("P03_FIELDS[m.EvidenceSourceAdmission] = {'attestation_operand'}\n",'')
start=s.index('        if bundle_id(current) != bundle_id(bundle):',s.index('def admit_external_evidence'));end=s.index('        # Validate everything before creating source files.',start)
s=s[:start]+"        if bundle_id(current) != bundle_id(bundle) or request.expected_bundle != bundle_id(current):\n            raise m.PlannerError('PARENT_MISMATCH')\n"+body+s[end:]
# Only retry filtering changed; existing prefix helper already included installs.
s=s.replace('later = {p for e in current.events[index+2:] if type(e.result) in (m.EvidenceSourceAdmission,m.InstallDefinition) for p in e.result.source_additions}', 'later = {p for e in current.events[index+2:] if type(e.result) is m.EvidenceSourceAdmission for p in e.result.source_additions}')
codes['codec']=s
check={}
for name,s in codes.items():
 path='adapter/planner/'+name+'.py';wanted=hashes[path]
 if hashlib.sha256(s.encode()).hexdigest()!=wanted:
  # Dataclass extraction may carry a single boundary newline from its module.
  for marker in ('\n\ndef materialize','\n\n\ndef materialize','\n\n\n@dataclass','\n\n@dataclass'):
   for n in range(1,5):
    candidate=s.replace(marker,'\n'*n+marker.lstrip('\n'))
    if hashlib.sha256(candidate.encode()).hexdigest()==wanted:s=candidate;break
  codes[name]=s
 check[path]=hashlib.sha256(s.encode()).hexdigest()==wanted
print(check)
(O/'baseline-runtime-hash-verification.json').write_text(json.dumps(check,indent=2))
assert all(check.values()),check
class Finder(importlib.abc.MetaPathFinder,importlib.abc.Loader):
 def find_spec(self,fullname,path,target=None):
  name=fullname.removeprefix('adapter.planner.') if hasattr(str,'removeprefix') else fullname[len('adapter.planner.'):] if fullname.startswith('adapter.planner.') else ''
  if name in codes:return importlib.util.spec_from_loader(fullname,self)
 def create_module(self,spec):return None
 def exec_module(self,module):
  name=module.__name__.split('.')[-1];path=str(R/'adapter/planner'/str(name+'.py'));module.__file__=path;exec(compile(codes[name],path,'exec'),module.__dict__)
sys.meta_path.insert(0,Finder())
suite=unittest.defaultTestLoader.loadTestsFromName('adapter.tests.test_planner_e1_replay.P04ReplayTests.test_x05_all_nine_checks_required_not_majority_vote')
result=unittest.TextTestRunner(verbosity=2).run(suite)
assert len(result.failures)==1 and not result.errors

# Exact pre-E07 comparison also reproduces the post-receipt diagnostic mismatch.
from adapter.planner import codec as c, model as model, core, evidence as ev, evidence_attestation as ea
D=R/'docs/plans';Q=D/'qualification/E2_P04_CONTINUATION_INPUT_CLOSURE_1'
parent=c.restore(D/'DETERMINISTIC_PLANNER_V0_1_E2_P04_POST_ATTEST_INSTALL_BUNDLE_1.json',
 model.ArtifactIdentity(model.IdentityKind.CONTENT_IDENTITY,'planner-bundle-v1','fa86ce94d76651ce5eccfa76c2d862243548d6d8dcaae91e74dca4e9c571c7d1'),R)
x=c._unwire(c.parse_json((D/'qualification/INSTALLATION_I04_1/a09-post-authentication-candidate.json').read_bytes()))
spec=c.parse_json((Q/'evidence-binding.json').read_bytes())
t=ea.materialize(**{k:c._unwire(v) for k,v in spec['attestation']['fields'].items() if k!='attestation_id'})
private=ev.apply(parent.current,x,t).snapshot
receipt=core.apply_receipt(private,model.ExternalEvent(x.gate,model.ExternalStage.EVIDENCE_RECEIVED,c.snapshot_id(private),x.entity.id)).snapshot
before,after=core.recompute(parent.current),core.recompute(receipt)
differing={k:{'before':c._wire(v),'after':c._wire(vars(after)[k])} for k,v in vars(before).items() if v!=vars(after)[k]}
assert set(differing)=={'blocked'} and before.control==after.control and before.actionable==after.actionable
(O/'baseline-control-counterexample.json').write_bytes(c.canonical_bytes({'runtime_hashes_exact':True,'differing_fields':differing,'canonical_commit':False}))
