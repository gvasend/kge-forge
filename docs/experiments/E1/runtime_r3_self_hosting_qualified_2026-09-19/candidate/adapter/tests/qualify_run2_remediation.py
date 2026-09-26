"""Non-live timing, integrated qualification and frozen evidence packaging."""
from pathlib import Path
import cProfile,io,json,pstats,sys,time,unittest
from unittest.mock import patch
from adapter.context_projection import canonical,sha
from adapter.run_control import RunControl,E1_POLICY,status

def write(path,value):
    data=canonical(value).encode();path.write_bytes(data)
    return {'path':str(path),'sha256':sha(data)}

def timing(out):
    from adapter.tests.qualify_activation_transaction import fixture
    from adapter.tests.test_controller_authority_store import private_fixture
    from adapter.controller_authority_store import ControllerAuthorityStore,encoded
    from adapter.authority_bootstrap import reconstruct_authorization
    from adapter.activation_transaction import ActivationTransaction
    root,auth,audit,ref,_=fixture(out/'fixture',supervisor_identity={'synthetic':'NON_LIVE'})
    store=private_fixture(auth,audit,ref,out/'private')
    # Match the released store's scale without importing E1 authority into this
    # synthetic invocation. Extra immutable evidence carries no extra grants.
    catalog=json.loads(encoded(store.catalog))
    records={key:{'bytes':store.resolve(key),'evidence':row['evidence']} for key,row in catalog['objects'].items()}
    while len(records)<477:
        data=('synthetic scale evidence '+str(len(records))).encode()
        records['sha256:'+sha(data)]={'bytes':data,'evidence':[]}
    provenance=next(iter(catalog['objects'].values()))
    store.close()
    store=ControllerAuthorityStore.materialize(out/'scaled-private',records,{},
        {'authority_source':provenance['authority_source'],'release_identities':provenance['release_identities']},
        catalog['applicability'],catalog['programmer_roots'],catalog['private_state'])
    selection={'root':str(store.root),
        'catalog_sha256':store.catalog_sha256,'applicability':store.applicability};store.close()
    control=RunControl(out/'timing.jsonl',{'authorization_id':'timing','session_id':'timing',
        'invocation_id':'timing','work_package_id':'synthetic'},E1_POLICY)
    elapsed={};prof=cProfile.Profile();prof.enable();tx=None
    try:
        begin=time.perf_counter()
        with control.span('private_bootstrap'):
            store=ControllerAuthorityStore(**selection)
            with store.session():restored=reconstruct_authorization(store,auth.authorization_id)
        elapsed['cold_private_bootstrap_seconds']=time.perf_counter()-begin
        with store.session(),patch('adapter.activation_transaction._host',return_value={'synthetic':'NON_LIVE'}):
            logical='E1-ARCHITECT-DISPATCH-sha256:'+ref['sha256']
            begin=time.perf_counter()
            with control.span('activation_recovery'):tx=ActivationTransaction.activate(restored,audit,logical)
            elapsed['cold_synthetic_activation_seconds']=time.perf_counter()-begin
            samples=[]
            for _ in range(3):
                begin=time.perf_counter()
                with control.span('validation'):tx.verify_handoff()
                samples.append(time.perf_counter()-begin)
            elapsed['warm_validation_seconds']=samples
            elapsed['warm_below_soft_threshold']=max(samples)<30
            # All mutable checks still execute: demonstrate a changed context fails warm.
            target=root/'task.txt';before=target.read_bytes();target.write_bytes(before+b'STALE')
            try:
                try:tx.verify_handoff()
                except (ValueError,RuntimeError):elapsed['changed_context_rejected']=True
                else:raise AssertionError('warm path cached away repository mutation')
            finally:target.write_bytes(before)
    finally:
        if tx:tx.close()
        store.close();prof.disable()
    stream=io.StringIO();pstats.Stats(prof,stream=stream).sort_stats('cumulative').print_stats(25)
    (out/'VALIDATION_PROFILE.txt').write_text(stream.getvalue())
    elapsed['scope']='Synthetic full activation/handoff, real private-store/context/ancestry checks; kernel supervisor observations mocked. No live E1 validation.'
    elapsed['logical_entries']=len(records)
    write(out/'TIMING_RESULTS.json',elapsed)
    return elapsed

def main():
    out=Path(sys.argv[1]).resolve();out.mkdir(parents=True,exist_ok=True)
    def inventory():return {str(p.resolve()):sha(p.read_bytes()) for base in ('adapter','adapter/tests') for p in sorted(Path(base).glob('*.py'))}
    frozen=inventory()
    write(out/'QUALIFIED_SOURCE_INVENTORY.json',frozen)
    modules=['adapter.tests.test_run_control','adapter.tests.test_orchestrator',
        'adapter.tests.test_production_exec','adapter.tests.test_recovery_ledger',
        'adapter.tests.test_programmer_substrate','adapter.tests.test_context_projection',
        'adapter.tests.test_authorization_lifecycle','adapter.tests.test_supervisor_amendment',
        'adapter.tests.test_controller_authority_store','adapter.tests.test_pd05_file_authority',
        'adapter.tests.test_pd06_release_boundaries','adapter.tests.test_versioned_ancestry']
    suite=unittest.defaultTestLoader.loadTestsFromNames(modules)
    with (out/'REGRESSION.log').open('w') as log:
        result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
    report={'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
        'skips':result.skipped,'verdict':'PASS' if result.wasSuccessful() else 'FAIL',
        'log_sha256':sha((out/'REGRESSION.log').read_bytes()),'non_live':True}
    write(out/'REGRESSION_RESULTS.json',report);print(canonical(report),flush=True)
    elapsed=timing(out);print(canonical(elapsed),flush=True)
    # Preserve an actual multi-cycle fixture status example and its source audit.
    from adapter.tests.test_run_control import InteractionTests
    case=InteractionTests('test_correction_multicycle_and_incomplete');case.setUp()
    try:
        case.test_correction_multicycle_and_incomplete()
        data=case.audit.read_bytes();(out/'MULTICYCLE_SYNTHETIC_AUDIT.jsonl').write_bytes(data)
        write(out/'OPERATOR_STATUS_EXAMPLE.json',status(case.audit))
    finally:case.tearDown()
    from adapter.tests.test_run_control import LifecycleTests
    lifecycle=LifecycleTests('test_cancel_releases_and_independent_reconstruction')
    lifecycle.test_cancel_releases_and_independent_reconstruction()
    write(out/'OPERATOR_LIFECYCLE_STATUS.json',lifecycle.terminal_status)
    assert inventory()==frozen,'implementation/test sources changed during qualification'
    write(out/'QUALIFICATION_CLOSURE.json',{'result':'PASS' if result.wasSuccessful() and elapsed['warm_below_soft_threshold'] else 'FAIL',
        'source_inventory_sha256':sha((out/'QUALIFIED_SOURCE_INVENTORY.json').read_bytes()),
        'regression_sha256':sha((out/'REGRESSION_RESULTS.json').read_bytes()),
        'timing_sha256':sha((out/'TIMING_RESULTS.json').read_bytes()),
        'python_executable':sys.executable,'python_version':sys.version,
        'source_unchanged_during_qualification':True,'non_live':True})
    if not result.wasSuccessful() or not elapsed['warm_below_soft_threshold']:raise SystemExit(1)

if __name__=='__main__':main()
