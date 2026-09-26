"""Real supervisor/live transaction regression through canonical ancestry."""
from pathlib import Path
from unittest.mock import patch
import json,sys,subprocess
from adapter.tests import qualify_activation_transaction as integrated
from adapter.tests.test_versioned_ancestry import qualify
from adapter.tests.test_governance_continuation import write
from adapter.context_projection import canonical,sha,read_exact
from adapter.context_binding import CommittedContext
from adapter.governed_host import WorkAuthorization
from adapter.activation_transaction import ActivationTransaction


def load_auth(path,fingerprint):
    raw=json.loads(read_exact(path,fingerprint));saved=raw['context_binding']
    raw['context_binding']=CommittedContext(saved['path'],saved['capture_commit'],json.loads(raw['operational_binding'])['governance'])
    for key in ('read_roots','write_roots','deny_roots','exec_bins','read_deny_roots','write_deny_roots','write_directory_roots'):
        raw[key]=tuple(raw[key])
    raw['exec_argv_allowlist']=tuple(tuple(x) for x in raw['exec_argv_allowlist'])
    return WorkAuthorization(**raw)


def fixture(out):
    auth,audit,ref,projection,report=qualify(out/'ancestry')
    raw=dict(auth.__dict__);raw['context_binding']={'path':str(auth.context_binding.path),'capture_commit':auth.context_binding.capture_commit}
    write(audit.parent/'SELECTED_SYNTHETIC_AUTH.json',raw)
    return auth.context_binding.repos['forge'],auth,audit,ref,projection


def recovery(audit,ref,compete=False):
    config=audit.parent/'SELECTED_SYNTHETIC_AUTH.json'
    args=[sys.executable,'-m','adapter.tests.qualify_versioned_ancestry','--recover',str(config),sha(config.read_bytes()),str(audit),ref['path'],ref['sha256'],'compete' if compete else 'recover']
    result=subprocess.run(args,capture_output=True,text=True,timeout=40)
    if result.returncode:raise AssertionError(result.stderr)
    return json.loads(result.stdout)


if __name__=='__main__':
    if sys.argv[1]=='--recover':
        try:
            auth=load_auth(sys.argv[2],sys.argv[3]);audit=Path(sys.argv[4]);ref={'path':sys.argv[5],'sha256':sys.argv[6]}
            fn=ActivationTransaction.activate if sys.argv[7]=='compete' else ActivationTransaction.recover
            tx=fn(auth,audit,ref);result={'denied':False,'recovery':getattr(tx,'recovery',{})};tx.close()
        except Exception as exc:result={'denied':True,'reason':str(exc),'handoff_eligible':False}
        print(canonical(result));sys.exit(0)
    out=Path(sys.argv[1]).resolve();out.mkdir(parents=True,exist_ok=True)
    with patch.object(integrated,'fixture',fixture),patch.object(integrated,'independent_recovery',recovery):
        report=integrated.live(out)
    print(canonical({'result':report['result'],'activation_event':report['activation_event']['event_id'],
        'reservation':report['ownership_reservation']['reservation_id'],'API_calls':report['actual_API_calls'],
        'terminal_recovery':report['terminal_recovery']}))
