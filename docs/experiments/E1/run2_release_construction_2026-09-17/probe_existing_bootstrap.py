"""Read-only actual historical bootstrap under the approved phase deadline.
No activation, ledger lock, model request or ownership transaction is called.
"""
import json,tempfile,time
from pathlib import Path
from adapter.controller_authority_store import ControllerAuthorityStore,sha
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.run_control import RunControl,E1_POLICY
A='auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39'
p=Path('/tmp/kge-forge-controller-authority')/A/'supervisor-succession-adoption-2026-09-17/SUCCESSION_PUBLICATION.json'
b=p.read_bytes();assert sha(b)=='95a2454b094f2b6e4af044cbfa8a8efd98a225866e2b19fc286a2d63abdacd4e'
selection=json.loads(b)['selected_store'];results=[]
with tempfile.TemporaryDirectory(prefix='run2-readonly-preflight-') as d:
    control=RunControl(Path(d)/'probe.jsonl',{'authorization_id':'READ_ONLY_QUALIFICATION','session_id':'probe',
        'invocation_id':'probe','work_package_id':'NO_INVOCATION'},E1_POLICY)
    for temperature in ('cold','warm'):
        start=time.monotonic();s=None
        try:
            with control.span('private_bootstrap'):
                s=ControllerAuthorityStore(**selection)
                with s.session():reconstruct_authorization(s,A)
            result={'result':'PASS'}
        except Exception as exc:result={'result':'BLOCKED','exception':type(exc).__name__,'reason':str(exc)}
        finally:
            if s:s.close()
        results.append(dict(result,temperature=temperature,elapsed_seconds=time.monotonic()-start))
    report={'schema':'RUN2-ACTUAL-HISTORICAL-BOOTSTRAP-PROBE-1','selection':selection,'samples':results,
        'scope':'Existing Run-1 authority with current proposed implementation; not an issued amended Run-2 authority',
        'Run2_activation_validation':'NOT_RUN_NO_ISSUED_RUN2_AUTHORITY',
        'Run2_ownership_created':False,'model_requests':0,'telemetry':Path(d,'probe.jsonl').read_text().splitlines()}
Path(__file__).with_name('ACTUAL_BOOTSTRAP_TIMING.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
print(json.dumps(results))
