"""D01 isolated native writers/readers. This script never executes A04."""
import argparse
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

from adapter.planner import codec as c, dossier_transaction as dt, model as m
from adapter.tests import dossier_fixture as f

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2)+'\n')


def manifest(store):
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in store.iterdir() if p.is_file()}


def writer(root, mode, crash=None):
    before, artifacts = f.create(root)
    before_id = c.bundle_id(before)
    expected, expected_id = f.expected(before, artifacts)
    # All comparison values are sealed before registration/invocation/commit.
    save(root/'sealed-oracle.json', {'bundle':c._wire(expected_id), 'snapshot':c._wire(c.snapshot_id(expected.current)),
        'event':c._wire(expected.events[-1].identity), 'parent':c._wire(before.events[-1].identity),
        'pre_bundle':c._wire(before_id), 'pre_snapshot':c._wire(c.snapshot_id(before.current)),
        'sequence':2, 'index':1, 'typed_validation_count':6,
        'qualifying_action':f.BUILD.value, 'scope':f.SCOPE, 'lineage':f.LINEAGE,
        'authority':'NONE_REQUIRED_BY_NATIVE_ACTION', 'primary_prospective_execution':False})
    before_path, _ = c.save_bundle(before,root/'start',root)
    calls=[]
    producer = dt.register_producer(f.BUILD,lambda state, inputs: (calls.append('operation') or f.produce(state,inputs,mode)))
    def hook(stage):
        if stage == crash:
            os._exit(73)
    after,bid,noop = dt.execute(before,before_id,producer,artifacts,root/'store',root,
        postcondition=f.oracle,failure_hook=hook)
    assert not noop and calls==['operation']
    assert bid==expected_id and c.snapshot_id(after.current)==c.snapshot_id(expected.current)
    assert after.events[-1].identity==expected.events[-1].identity
    assert c.bundle_bytes(after,snapshot_resolver=c.snapshot_resolver(root/'store'))==c._bundle_bytes_admitted(expected)
    retry,same,noop = dt.execute(before,before_id,producer,artifacts,root/'store',root)
    assert noop and same==bid and calls==['operation']
    # Retain a separate descendant branch proving historical outcomes survive
    # later source invalidation without becoming current support/permission.
    resolver=c.snapshot_resolver(root/'store')
    invalidation=m.SourceInvalidation((artifacts[0][0].identity,),c.snapshot_id(after.current))
    later,lid=c.commit_event(after,invalidation,root/'descendant',root,snapshot_resolver=resolver)
    assert all(v.currentness is m.ValidationState.STALE for v in later.current.validation_instances)
    save(root/'writer.json', {'result':'PASS', 'seed':os.environ.get('PYTHONHASHSEED'), 'presentation':mode,
        'start_path':str(before_path.relative_to(root)), 'bundle':c._wire(bid),
        'snapshot':c._wire(c.snapshot_id(after.current)), 'event':c._wire(after.events[-1].identity),
        'parent':c._wire(after.events[-1].parent_event), 'sequence':2, 'index':1,
        'descendant_bundle':c._wire(lid), 'descendant_snapshot':c._wire(c.snapshot_id(later.current)),
        'producer_invocations':len(calls), 'retry':'EXACT_NOOP',
        'store_files':manifest(root/'store'), 'descendant_files':manifest(root/'descendant')})
    print(json.dumps({'role':'writer','result':'PASS','seed':os.environ.get('PYTHONHASHSEED'),'presentation':mode}))


def reader(root, mode):
    recorded=json.loads((root/'writer.json').read_text())
    oracle=json.loads((root/'sealed-oracle.json').read_text())
    bid=c._unwire(recorded['bundle']); expected=c._unwire(oracle['bundle'])
    assert bid==expected
    store=root/'store'; original=manifest(store)
    # Neither producer registration nor execution/publication is available in
    # this independent process. No expected Snapshot body supplies replay data.
    with patch.object(dt,'prepare',side_effect=AssertionError('live admission on replay')), \
         patch.object(dt,'execute',side_effect=AssertionError('live operation on replay')), \
         patch.object(dt,'register_producer',side_effect=AssertionError('registration on replay')), \
         patch.object(c,'_publish_head',side_effect=AssertionError('replay publication')):
        cold=c.restore(store/('bundle-'+bid.sha256+'.json'),bid,root)
        resolver=c.snapshot_resolver(store)
        assert c.snapshot_id(cold.current)==c._unwire(oracle['snapshot'])
        assert cold.events[-1].identity==c._unwire(oracle['event'])
        assert cold.events[-1].parent_event==c._unwire(oracle['parent'])
        assert cold.events[-1].sequence==2 and len(cold.events)==2
        assert len(cold.current.validation_instances)==6
        assert all(v.currentness is m.ValidationState.ACCEPTED and v.result is m.ValidationOutcome.PASS
                   for v in cold.current.validation_instances)
        f.oracle(c._prefix_bundle(cold,1,snapshot_resolver=resolver).current,cold.current,cold.events[-1])
        for _ in range(3):
            assert c.snapshot_id(c._replay(cold,snapshot_resolver=resolver))==c._unwire(oracle['snapshot'])
        prefix=c._prefix_bundle(cold,1,snapshot_resolver=resolver)
        assert c.bundle_id(prefix)==c._unwire(oracle['pre_bundle'])
        assert all(p.path!='dossier-input.json' for p in prefix.sources)
        assert c.bundle_id(c._read_head(store,prefix,root),snapshot_resolver=resolver)==bid
        # Declaration order may be changed only for explicitly unordered fields.
        permute=(lambda xs:xs[::-1]) if mode=='reverse' else (lambda xs:xs[1:]+xs[:1])
        reordered=replace(cold,sources=permute(cold.sources),
            current=replace(cold.current,actions=permute(cold.current.actions),
                statuses=permute(cold.current.statuses),validation_instances=permute(cold.current.validation_instances)))
        assert c.bundle_id(reordered,snapshot_resolver=resolver)==bid
        lid=c._unwire(recorded['descendant_bundle']); branch=root/'descendant'
        later=c.restore(branch/('bundle-'+lid.sha256+'.json'),lid,root)
        later_resolver=c.snapshot_resolver(branch)
        assert c.snapshot_id(later.current)==c._unwire(recorded['descendant_snapshot'])
        assert all(v.currentness is m.ValidationState.STALE for v in later.current.validation_instances)
        old=later_resolver(cold.events[-1].after_snapshot)
        assert all(v.currentness is m.ValidationState.ACCEPTED for v in old.validation_instances)
        assert c.bundle_id(c._prefix_bundle(later,2,snapshot_resolver=later_resolver),snapshot_resolver=later_resolver)==bid
        assert manifest(branch)==recorded['descendant_files']
    assert manifest(store)==original==recorded['store_files']
    result={'role':'fresh_reader','result':'PASS','seed':os.environ.get('PYTHONHASHSEED'), 'presentation':mode,
            'live_operation_calls':0,'new_appends':0,'replay_repetitions':3,
            'bundle':recorded['bundle'],'event':recorded['event'],'snapshot':recorded['snapshot'],
            'historical_source_boundary':'PASS','invalidation_history':'PASS','writer_terminated':True}
    print(json.dumps(result))
    return result


def recover_crash(root, stage):
    oracle=json.loads((root/'sealed-oracle.json').read_text())
    before_id=c._unwire(oracle['pre_bundle'])
    before=c.restore(root/'start'/('bundle-'+before_id.sha256+'.json'),before_id,root)
    current=c._read_head(root/'store',before,root)
    resolver=c.snapshot_resolver(root/'store')
    committed=stage=='after_head_replace'
    assert (len(current.events)==2)==committed
    if committed:
        assert c.bundle_id(current,snapshot_resolver=resolver)==c._unwire(oracle['bundle'])
    else:
        assert c.bundle_id(current)==before_id
    pin=m.ArtifactPin('dossier-input.json',c._identity(c.canonical_bytes(f.packet()),'raw-file-sha256'))
    artifacts=((pin,c.canonical_bytes(f.packet())),)
    calls=[]
    producer=dt.register_producer(f.BUILD,lambda state, inputs:(calls.append(1) or f.produce(state,inputs)))
    final,bid,noop=dt.execute(before,before_id,producer,artifacts,root/'store',root)
    assert noop==committed and len(calls)==(0 if committed else 1)
    assert bid==c._unwire(oracle['bundle']) and len(final.events)==2
    result={'stage':stage,'result':'PASS','killed_writer_exit':73,
            'observed':'COMPLETE_NEW' if committed else 'COMPLETE_OLD','retry':'EXACT_NOOP' if noop else 'CLEAN_COMMIT'}
    print(json.dumps(result));return result


def run(role, root, seed, mode='original', crash=None, expected_exit=0):
    command=[sys.executable,str(Path(__file__).resolve()),role,str(root),'--presentation',mode]
    if crash:command+=['--crash',crash]
    env=dict(os.environ,PYTHONHASHSEED=str(seed),PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(REPO))
    completed=subprocess.run(command,cwd=str(REPO),env=env,capture_output=True,text=True)
    if completed.returncode!=expected_exit:
        raise RuntimeError(completed.stdout+'\n'+completed.stderr)
    return json.loads(completed.stdout.strip().splitlines()[-1]) if completed.stdout.strip() else None


def orchestrate():
    writers=[];readers=[];crashes=[]
    # Separate processes and stores, identical fixed generic qualification context.
    for seed in (0,1,7,101):
        for mode in ('original','reverse','rotate'):
            root=HERE/'runs'/('seed-'+str(seed)+'-'+mode)
            writers.append(run('writer',root,seed,mode))
            readers.append(run('reader',root,seed,mode))
            print('PASS writer/reader seed='+str(seed)+' presentation='+mode,flush=True)
    anchors=[json.loads((HERE/'runs'/('seed-'+str(seed)+'-'+mode)/'writer.json').read_text())
             for seed in (0,1,7,101) for mode in ('original','reverse','rotate')]
    assert len({json.dumps({k:v[k] for k in ('bundle','snapshot','event','descendant_bundle')},sort_keys=True) for v in anchors})==1
    for stage in ('after_archive_stage','after_files_fsync','before_head_replace','after_head_replace'):
        root=HERE/'crashes'/stage
        run('writer',root,0,crash=stage,expected_exit=73)
        crashes.append(run('recover',root,1,crash=stage))
        print('PASS killed-writer recovery '+stage,flush=True)
    save(HERE/'process-qualification.json',{'result':'PASS','writers':writers,'fresh_readers':readers,
         'independent_writers':12,'cold_readers':12,'hash_seeds':[0,1,7,101],
         'unordered_presentations':['original','reverse','rotate'],'identity_semantics':'IDENTICAL',
         'killed_writer_recovery':crashes,'primary_prospective_executions':0})


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('role',choices=('writer','reader','recover','all'))
    parser.add_argument('root',nargs='?',type=Path)
    parser.add_argument('--presentation',default='original')
    parser.add_argument('--crash')
    args=parser.parse_args()
    if args.role=='all':orchestrate()
    elif args.role=='writer':writer(args.root,args.presentation,args.crash)
    elif args.role=='reader':reader(args.root,args.presentation)
    else:recover_crash(args.root,args.crash)
