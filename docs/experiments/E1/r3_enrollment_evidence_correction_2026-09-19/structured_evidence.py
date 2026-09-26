"""Lossless evidence packaging, not authority or a production-validator change."""
import json,hashlib,copy
from pathlib import Path
O=Path(__file__).resolve().parent;E=O.parent;Q=E/'runtime_r3_self_hosting_qualified_2026-09-19';P=E/'r3_enrollment_2026-09-19'
sha=lambda b:hashlib.sha256(b).hexdigest()
encode=lambda o:json.dumps(o,sort_keys=True,separators=(',',':')).encode()
q=json.loads((Q/'RUNTIME_QUALIFICATION_FINAL.json').read_bytes());closure=json.loads((Q/'QUALIFICATION_CLOSURE.json').read_bytes());old=json.loads((P/'AUTHORIZED_ENROLLMENT_SELECTION.json').read_bytes())
# Pins come from the frozen qualification manifest and preserved attributable intake.
manifest={name:h for h,name in (line.split('  ',1) for line in (Q/'SHA256SUMS').read_text().splitlines())}
SOURCES={'qualification_report':(Q/'REPORT.md',manifest['REPORT.md'],'QUALIFICATION_REPORT_MARKDOWN'), 'architect_instruction':(P/'ARCHITECT_ENROLLMENT_SOURCE.md',old['intake']['source']['sha256'],'ATTRIBUTABLE_ARCHITECT_ENROLLMENT_INSTRUCTION_MARKDOWN')}
def expected(name,loader=lambda p:p.read_bytes()):
 path,h,kind=SOURCES[name];raw=loader(path)
 if sha(raw)!=h:raise ValueError('source content hash differs')
 return {'schema':'LOSSLESS_SOURCE_EVIDENCE_REPRESENTATION-1','evidence_type':kind,'source_evidence_identity':'sha256:'+h,'source_content_sha256':h,'source_path':str(path.resolve()),'qualification_identity':closure['id'],'candidate_identity':q['continuation']['id'],'predecessor_runtime':q['R1']['identity'],'successor_runtime':q['R3']['identity'],'authority_context':q['continuation']['context'],'semantic_claim':{'mode':'EXACT_SOURCE_TEXT_NO_ADDITIONAL_ASSERTION','source_text':raw.decode('utf-8')},'provenance':{'source_role':name,'source_authority':'ARCHITECT_ACCEPTED_QUALIFICATION' if name=='qualification_report' else 'EXISTING_ATTRIBUTABLE_ARCHITECT_INSTRUCTION','authority_added':False},'packaging_only':True}
def build(name):
 obj=expected(name);obj['id']='STRUCTURED-EVIDENCE-sha256:'+sha(encode(obj));return obj
def validate(name,blob,loader=lambda p:p.read_bytes()):
 obj=json.loads(blob);body=dict(obj);identity=body.pop('id')
 if identity!='STRUCTURED-EVIDENCE-sha256:'+sha(encode(body)):raise ValueError('object fingerprint differs')
 if body!=expected(name,loader):raise ValueError('source identity/claim/schema substitution')
 return obj
def qualify():
 rows=[]
 for name in SOURCES:
  obj=build(name);data=encode(obj);validate(name,data);rows.append({'probe':name+':exact_lossless_equivalence','result':'PASS'})
  cases={'changed_source':(data,lambda p:p.read_bytes()+b'changed'),'malformed_json':(b'{',None),'markdown_only':(SOURCES[name][0].read_bytes(),None),'missing_required_field':(None,None),'substituted_source_identity':(None,None),'strengthened_claim':(None,None)}
  for test,(bad,loader) in cases.items():
   if bad is None:
    altered=copy.deepcopy(obj);altered.pop('id')
    if test=='missing_required_field':altered.pop('qualification_identity')
    elif test=='substituted_source_identity':altered['source_evidence_identity']='sha256:'+'0'*64
    else:altered['semantic_claim']['source_text']='PASS: R3 CURRENT AND ADOPTED'
    altered['id']='STRUCTURED-EVIDENCE-sha256:'+sha(encode(altered));bad=encode(altered)
   try:validate(name,bad,loader or (lambda p:p.read_bytes()))
   except (ValueError,KeyError,TypeError) as exc:rows.append({'probe':name+':'+test,'result':'REJECTED','reason':str(exc)})
   else:raise AssertionError(test+' accepted')
  (O/(name+'.json')).write_bytes(data)
 result={'schema':'EVIDENCE-REPRESENTATION-EQUIVALENCE-1','result':'PASS','authority_added':False,'production_validator_changed':False,'source_bytes_changed':False,'probes':rows,'mapping':{name:{'source':str(path),'source_sha256':h,'structured_identity':build(name)['id'],'structured_sha256':sha(encode(build(name)))} for name,(path,h,_) in SOURCES.items()}}
 (O/'EQUIVALENCE_QUALIFICATION.json').write_bytes(encode(result));return result
if __name__=='__main__':print(json.dumps(qualify(),indent=2))
