import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,'/home/gvasend/app/kge-forge')
from adapter.context_binding import CommittedContext
from adapter.directory_provisioning import plan,provision,SOURCE
from adapter.committed_objects import object_bytes
root=Path('/home/gvasend/app/kge-forge')
b=CommittedContext(root/'docs/experiments/E1/pre_dispatch/CONTEXT_MANIFEST.json','5871bdce4f5b6539c84f69f4f2b2f94ee31be5cd')
assert b.verify()
# Verified committed root tree metadata, no hooks or repository-controlled processes.
revision='411cb5a9fabc71e482a414ed58387de0ff557e93'
kind,commit,_=object_bytes(root,revision)
assert kind=='commit'
oid=commit.split(b'\n',1)[0][5:].decode()
kind,tree,_=object_bytes(root,oid);assert kind=='tree'
entries={}
while tree:
 head,_,tail=tree.partition(b'\0');mode,name=head.split(b' ',1)
 entries[name.decode()]={'mode':mode.decode(),'oid':tail[:20].hex()};tree=tail[20:]
assert 'src' not in entries and 'tests' not in entries and entries['docs']['mode']=='40000'
record=plan(root,b.digest)
out=Path('/tmp/pd06-production-provision-20260916');out.mkdir(mode=0o700,exist_ok=False)
(out/'PLAN.json').write_text(json.dumps(record,indent=2)+'\n')
(out/'BASELINE_DERIVATION.json').write_text(json.dumps({'revision':revision,'tree':oid,'entries':entries,
 'work_package_sha256':hashlib.sha256((root/'docs/experiments/E1/pre_dispatch/E1-WP-001.md').read_bytes()).hexdigest(),
 'scope':b.manifest['scope'],'context_sha256':b.digest},indent=2)+'\n')
receipt=provision(record,out/'provisioning.jsonl')
receipt['architect_authority_reference']=SOURCE
assert b.verify()
(out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
