"""Build a separate prospective V3 candidate; never execute native cases."""
import json,hashlib
from pathlib import Path
R=Path('/home/gvasend/app/kge-forge');E=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification';B=Q/'E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2';P=Q/'E2_P05_D01_SOURCE_BYTES_PIN_RECONCILIATION_32'
def load(p):return json.loads(Path(p).read_bytes())
def write(n,x):(E/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def pin(p):return {'path':str(p.relative_to(R)),'raw_sha256':sha(p.read_bytes())}
domain=load(P/'source-collection.json');assert domain['COUNT']==51
instances=[]
for source in domain['MEMBERS']:
 subject={'obligation_id':'D01-OBL:SOURCE_BYTES','case_id':'E2-D01','dispatch_id':'D01-DISPATCH:SOURCE_BYTES','operation_id':'LOAD_PIN','native_entrypoint':'adapter.planner.codec.load_pinned','source_id':source['SOURCE_ID'],'source_pin':source['PIN'],'source_role':source['SEMANTIC_ROLE'],'provenance_role':source['PROVENANCE_ROLE'],'capsule_id':'D01-FIXTURE:SOURCE_BYTES:REQUIRED_ROLE','state_variant_id':'D01-VARIANT:SOURCE_BYTES:REQUIRED_ROLE','capsule_source':domain['OWNING_CAPSULE'],'scope':source['SCOPE'],'lineage':source['LINEAGE'],'generation':source['GENERATION'],'first_available_event_prefix':source['FIRST_AVAILABLE_EVENT_PREFIX'],'operands':{'source_root':str(R),'pin':source['PIN']},'mutation_descriptor':None,'comparison_reference':'FUTURE_INDEPENDENT_ORACLE_KEYED_BY_THIS_INSTANCE; no expected values constructed'}
 subject['instance_identity']='qualification-D01-source-instance-v1:'+sha(canon(subject));instances.append(subject)
instances.sort(key=lambda x:x['instance_identity'])
aggregate={'obligation_id':'D01-OBL:SOURCE_BYTES','case_id':'E2-D01','acceptance':'ALL','required_instance_identities':sorted(x['instance_identity'] for x in instances),'source_count':51,'source_collection_semantics':'UNORDERED; prefix chronology retained','frozen_obligations':128}
aggregate['aggregate_identity']='qualification-D01-source-aggregate-v1:'+sha(canon(aggregate))
write('source-instances.json',instances);write('aggregate-contract.json',aggregate)
paths=load(B/'dispatch-table-v2.json');old=paths['D01-DISPATCH:SOURCE_BYTES'];new=dict(old);new['per_source_expansion']={'schema':'D01-SOURCE-EXHAUSTIVE-EXPANSION-1','domain':pin(P/'source-collection.json'),'instances':pin(E/'source-instances.json'),'aggregate':pin(E/'aggregate-contract.json'),'expected_count':51,'acceptance':'ALL','original_fixture':domain['OWNING_CAPSULE'],'source_collection_pointer':'/canonical_content/arguments/bundle/sources','runtime_source_selection':False}
paths['D01-DISPATCH:SOURCE_BYTES']=new;write('dispatch-table-v3.json',paths)
# Preserve every V2 function except addition of the exhaustive branch and static dispatch path.
text=(B/'runner_v2.py').read_text();text=text.replace('from common_v2 import ROOT,OUT,TYPE,OPERATIONS,read,ref,demand,filehash,canonical,qid','sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2"))\nfrom common_v2 import ROOT,OUT,TYPE,OPERATIONS,read,ref,demand,filehash,canonical,qid\nfrom source_dispatch_v3 import expand_instances, aggregate_outputs\nV3_OUT = Path(__file__).resolve().parent')
needle="    demand(row['RUNNER_DISPATCH_ID']==path['dispatch_id'],'WRONG_DISPATCH')"
replacement="""    if 'per_source_expansion' in path:
        jobs = expand_instances(row, path, fixture, context)
        observed = []
        for instance, packet, single_path in jobs:
            output = execute_job(row, single_path, packet, dict(context))
            demand(output['rejections'] is None, 'SOURCE_INSTANCE_NATIVE_FAILURE')
            observed.append({'instance_identity':instance['instance_identity'],'output':output})
        return aggregate_outputs(path, observed)
"""+needle
assert text.count(needle)==1;text=text.replace(needle,replacement).replace("paths=read(OUT/'dispatch-table-v2.json')","paths=read(V3_OUT/'dispatch-table-v3.json')")
(E/'runner_v3.py').write_text(text)
write('candidate-source-pins.json',{'V2_RUNNER':pin(B/'runner_v2.py'),'V2_DISPATCH':pin(B/'dispatch-table-v2.json'),'V2_HELPERS':pin(B/'common_v2.py'),'V3_RUNNER':pin(E/'runner_v3.py'),'V3_DISPATCH':pin(E/'dispatch-table-v3.json'),'DOMAIN':pin(P/'source-collection.json'),'PROPOSAL':pin(P/'dispatch-correction-proposal.json')})
print('Candidate built: 128 obligations; SOURCE_BYTES 51 instances; non-source dispatches unchanged')
