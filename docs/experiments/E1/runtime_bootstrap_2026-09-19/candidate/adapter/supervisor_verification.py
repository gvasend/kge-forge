"""Shared production supervisor verification reuse; never a cached READY.

The reference is consumed only from an authenticated implementation-continuation
 evidence object. Original dependencies and current kernel facts remain required.
"""
import json
from pathlib import Path
from .context_projection import sha,read_exact
from .attempt_context import require,read,ident
from .history_catalogs import historical_store
from .supervisor_observation import observe as observe_instance
from .supervisor_succession import legacy_tuple
from .validation_spans import span

def verified_readiness(reference,parent_publication,expected,check_scopes,legacy):
 with span('supervisor_authority_dependencies'):
  capture=read(reference)
  require(capture['schema']=='SUPERVISOR-IMMUTABLE-VERIFICATION-1' and capture['id']==ident('SUPERVISOR-IMMUTABLE-VERIFICATION',{k:v for k,v in capture.items() if k!='id'}),'supervisor verification changed')
  require(capture['reuse_scope']=='PURE_AUTHORITY_VERIFICATION_ONLY_FRESH_KERNEL_AND_HEAD_REQUIRED','invalid supervisor reuse scope')
  inventory=capture['producer']['implementation'];roots={str(Path(p).parent) for p in inventory}
  require(len(roots)==1 and {str(p):sha(p.read_bytes()) for p in Path(next(iter(roots))).glob('*.py')}==inventory,'supervisor verification implementation changed')
  for key in ('path','python'):read_exact(capture['producer'][key],capture['producer']['sha256' if key=='path' else 'python_sha256'])
  for path,h in capture['mutable'].items():read_exact(path,h)
  pin=capture['parent_publication'];require(pin==parent_publication,'unrelated supervisor verification origin')
  publication=json.loads(read_exact(pin['path'],pin['sha256']))
  require(publication['selected_store']==capture['selected_store'],'supervisor authority store substituted')
  with historical_store(capture['selected_store']) as predecessor_store:
   predecessor_store.verify_immutable_witness(capture['immutable_witness'])
   ledger=predecessor_store.state_path(capture['succession_ledger']['logical_identity'])
   require(str(ledger)==capture['succession_ledger']['path'],'supervisor ledger relocated')
   data=read_exact(str(ledger),capture['succession_ledger']['sha256'])
   instance=capture['instance']
   require(instance['id']==expected['current_supervisor'] and capture['head']==expected['succession_head'],'supervisor authority head stale')
   with span('supervisor_live_identity_readiness'):
    require(observe_instance(instance)==instance,'supervisor birth/configuration changed')
    result=legacy(legacy_tuple(instance),check_scopes=check_scopes)
    require(observe_instance(instance)==instance and ledger.read_bytes()==data,'supervisor identity/authority changed during readiness')
   predecessor_store._verify_catalog()
 return dict(result,SupervisorInstanceId=instance['id'],SupervisorSuccessionHead=capture['head'])
