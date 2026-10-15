"""Independent direct-source reconstruction. Does not import the binding producer."""
import json,hashlib,sys
from pathlib import Path
R=Path('/home/gvasend/app/kge-forge');E=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification';P=Q/'E2_P05_D01_A15_APPLICABILITY_GAP_DECOMPOSITION_44'
def encode(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def read(p):return json.loads(Path(p).read_bytes())
def digest(b):return hashlib.sha256(b).hexdigest()
gaps=read(P/'typed-gap-inventory.json');graph=read(Q/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json');context=graph['CONTEXT'];values=[]
for gap in gaps:
 if gap['CLASSIFICATION']!='RECOVERABLE_EXISTING_DATA':continue
 source=gap['KNOWN_EVIDENCE'];raw=(R/source['path']).read_bytes();assert digest(raw)==source['raw_sha256'];doc=json.loads(raw);id=gap['GAP_ID']
 # This branch independently implements the declared D04 subset, not producer output.
 value=[node for node in doc['NODES'] if node['TYPE']=='SOURCE_CONTENT'] if id=='D04' else doc
 if '--identity' not in sys.argv:
  actual=read(E/('binding-'+id+'.json'));assert actual['VALUE']==value and actual['SOURCE_PATH']==source['path'] and actual['SOURCE_HASH']==source['raw_sha256'];assert actual['CONTENT_IDENTITY']=={'kind':'CONTENT_IDENTITY','namespace':'raw-file-sha256','sha256':source['raw_sha256']};assert actual['VALUE_COMPARISON_IDENTITY']=='qualification-retained-data-value-v1:'+digest(encode(value));body=dict(actual);identity=body.pop('BINDING_IDENTITY');assert identity=='qualification-A15-retained-binding-v1:'+digest(encode(body));assert actual['SCOPE']==context['scope'] and actual['LINEAGE']==context['lineage'] and actual['VALIDATION_RESULT']=='BOUND_PASS'
 values.append({'GAP_ID':id,'SOURCE':source,'SOURCE_POINTER':'/NODES' if id=='D04' else '', 'VALUE':value,'CONTEXT':context,'VALUE_HASH':digest(encode(value))})
assert len(values)==5
print(digest(encode(values)) if '--identity' in sys.argv else json.dumps({'RESULT':'PASS','DIRECT_SOURCE_BINDINGS_VERIFIED':5,'SOURCE_RECONSTRUCTION_IDENTITY':digest(encode(values)),'PRODUCER_OUTPUT_USED_AS_ORACLE':False},sort_keys=True))
