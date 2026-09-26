"""Resume uncommitted enrollment after private-file preparation validation."""
import json,sys,os,stat,importlib.util,time
from pathlib import Path
from structured_evidence import validate
O=Path(__file__).resolve().parent;pin=json.loads((O/'AUTHORIZED_ENROLLMENT_SELECTION.json').read_bytes());sys.path.insert(0,pin['consumer_root'])
from adapter import runtime_adoption as r,runtime_bootstrap as b
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha
root=Path(pin['enrollment_module']).parent
assert not (root/'ENROLLMENT_INTENT.json').exists() and not (O/'ENROLLMENT_RESULT.json').exists()
def write(path,obj):
 fd=os.open(str(path),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 try:
  data=encoded(obj);assert os.write(fd,data)==len(data);os.fsync(fd)
 finally:os.close(fd)
 fd=os.open(str(Path(path).parent),os.O_RDONLY|os.O_DIRECTORY);os.fsync(fd);os.close(fd)
assert sha(Path(pin['enrollment_module']).read_bytes())==pin['enrollment_module_sha256']
sp=importlib.util.spec_from_file_location('exact_enrollment',pin['enrollment_module']);en=importlib.util.module_from_spec(sp);sp.loader.exec_module(en)
s=ControllerAuthorityStore(**pin['selected_store']);base=ControllerAuthorityStore(**pin['base_store']);d=en.delegation(s)
journal=Path(s.catalog['private_state'][d['journal']]['path']);fd=os.open(journal,os.O_RDONLY|os.O_NOFOLLOW);before=os.fstat(fd)
assert stat.S_ISREG(before.st_mode) and before.st_uid==os.getuid() and before.st_nlink==1 and before.st_size==0
assert stat.S_IMODE(before.st_mode)==0o664
os.fchmod(fd,0o600);os.fsync(fd);after=os.fstat(fd);os.close(fd)
write(O/'PRIVATE_JOURNAL_MODE_REPAIR.json',{'path':str(journal),'before':oct(stat.S_IMODE(before.st_mode)),'after':oct(stat.S_IMODE(after.st_mode)),'inode_unchanged':before.st_ino==after.st_ino,'bytes_before_after_sha256':sha(b''),'authority_semantics_changed':False,'reason':'restore existing qualified private-state mode; empty journal only'})
for label in ('qualification_report','architect_instruction'):validate(label,(O/(label+'.json')).read_bytes())
for name,h in pin['baseline'].items():assert sha(Path(name).read_bytes())==h
state=r.reconstruct(base);assert state['current_runtime']==pin['R1'] and state['head_event']==pin['base_binding']['head_event'] and state['pending'] is None
assert b.reconstruct(base)['state']=='SUCCESSOR_CURRENT'
p=r.policy(base);lc=dict(p['release_context']);release=lc.pop('release_authority');rr,cc=r.production_identities(base,release,lc,pin['base_binding']);assert d['context']==dict(cc,release_authority=rr)
assert sha(s.resolve(pin['candidate']['authority_id']))=='94bb69262b6af4020fbd829d582f439c60bcfbc42c4df2fba2e266d444554172'
en.validate(s,d,pin['candidate'],pin['qualification'],pin['decision'])
r.descriptor(base,state['current_descriptor'],live=True)
_,record,_=b.verify_records(base);b.fresh_supervisor(base,record)
with en.current_head(base,d) as head,en.lock(s,d,False) as f:
 assert en.history(s,d,f)==[] and head['current_runtime']==pin['R1']
intent=r.seal('CONTINUATION-ENROLLMENT-INTENT',{'schema':'ENROLLMENT-INTENT-1','candidate':pin['candidate'],'qualification':pin['qualification'],'decision':pin['decision'],'delegation':d['id'],'runtime_head':state['head_event'],'current_runtime':pin['R1'],'selected_catalog_sha256':s.catalog_sha256,'wall_time':time.time(),'authority_scope':'ENROLL_ONLY'})
write(root/'ENROLLMENT_INTENT.json',intent)
row=en.enroll(s,base,pin['candidate'],pin['qualification'],pin['decision'],binding_kind='PRODUCTION_ENROLLMENT')
assert en.require_eligible(s,base,pin['candidate'],row['id'],binding_kind='PRODUCTION_ENROLLMENT')==row
assert r.reconstruct(base)==state
for name,h in pin['baseline'].items():assert sha(Path(name).read_bytes())==h
write(root/'ENROLLMENT_RESULT.json',row);write(O/'ENROLLMENT_RESULT.json',row);write(O/'ENROLLMENT_INTENT.json',intent)
write(O/'PRODUCTION_DELEGATION.json',d);write(O/'PRODUCTION_QUALIFICATION.json',r.read(s,pin['qualification']));write(O/'PRODUCTION_ENROLLMENT_DECISION.json',r.read(s,pin['decision']))
s.close();base.close();print(json.dumps({'enrollment':row['id'],'enrollment_sha256':sha(encoded(row)),'R1':'CURRENT','R3':'ENROLLED_ELIGIBLE_UNADOPTED'}))
