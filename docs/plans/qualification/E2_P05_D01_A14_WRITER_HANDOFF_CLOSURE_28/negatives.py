"""Future-contract metadata controls; no runtime fact asserted or operation run."""
import json
from copy import deepcopy
from pathlib import Path
O=Path(__file__).resolve().parent
targets=json.loads((O/'two-targets-and-guarded-handoff.json').read_bytes())['ROWS']
base={'path_exists_now':False,'static_bytes_are_persisted':False,'save_return_required':True,'target':targets[0]['TARGET_PATH'],'hash':targets[0]['EXPECTED_HASH'],'bundle_id':targets[0]['EXPECTED_BUNDLE_ID'],'transfer':'PERSISTED_REFERENCE_RECORD_AND_NATIVE_FILE','reader_before_exit':False,'open_fd_transfer':False,'head_updated':False,'head_required':False,'directory_fsync_claim':False,'crash_durability_claim':False,'post_save_native_transition':False,'post_save_state':'UNCHANGED','conflicting_target_accepted':False,'reader_target':targets[0]['TARGET_PATH'],'reader_mode':'INDEPENDENT_PROCESS','writer_self_proves_exit':False}
def validate(v):
 assert v==base
 assert not v['path_exists_now'] and not v['static_bytes_are_persisted'] and v['save_return_required'] and v['transfer']=='PERSISTED_REFERENCE_RECORD_AND_NATIVE_FILE'
rows=[]
def reject(name,fn):
 v=deepcopy(base);fn(v)
 try:validate(v)
 except AssertionError:rows.append({'CASE':name,'STATUS':'REJECTED'})
 else:raise AssertionError(name)
reject('path treated as existing before save',lambda v:v.update(path_exists_now=True))
reject('predicted bytes treated as persisted',lambda v:v.update(static_bytes_are_persisted=True))
reject('save return omitted',lambda v:v.update(save_return_required=False))
reject('wrong save target',lambda v:v.update(target='OTHER'))
reject('wrong persisted hash',lambda v:v.update(hash='0'*64))
reject('wrong bundle identity',lambda v:v['bundle_id'].update(namespace='planner-snapshot-v1'))
reject('writer memory passed to reader',lambda v:v.update(transfer='PYTHON_BUNDLE_OBJECT'))
reject('reader before writer termination',lambda v:v.update(reader_before_exit=True))
reject('open descriptor transfer',lambda v:v.update(open_fd_transfer=True))
reject('HEAD update claimed',lambda v:v.update(head_updated=True))
reject('HEAD dependency introduced',lambda v:v.update(head_required=True))
reject('directory fsync claimed',lambda v:v.update(directory_fsync_claim=True))
reject('general crash durability claimed',lambda v:v.update(crash_durability_claim=True))
reject('forbidden post-save lifecycle transition',lambda v:v.update(post_save_native_transition=True))
reject('wrong post-save state',lambda v:v.update(post_save_state='ADVANCED'))
reject('conflicting target accepted',lambda v:v.update(conflicting_target_accepted=True))
reject('reader different target',lambda v:v.update(reader_target='OTHER'))
reject('warm reader substituted',lambda v:v.update(reader_mode='WRITER_MEMORY'))
reject('writer record proves future exit',lambda v:v.update(writer_self_proves_exit=True))
(O/'negative-suite.json').write_text(json.dumps({'STATUS':'PASS_STATIC_WRITER_HANDOFF_GUARDS','COUNT':len(rows),'ROWS':rows,'MODE':'In-memory runtime contract proposals only; no save/exit/reader/failure injection'},sort_keys=True,indent=2)+'\n')
print(json.dumps({'NEGATIVES':'PASS_STATIC','COUNT':len(rows)}))
