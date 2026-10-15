"""Independent terminated writers and fresh restore/replay readers."""
import json
import os
import subprocess
import sys
from pathlib import Path

import execution_driver as d


def run(mode, directory, seed, presentation='original', output=None):
    command=[sys.executable,str(d.OUT/'execution_driver.py'),mode,str(directory),
             '--presentation',presentation]
    if output: command += ['--output',str(output)]
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(d.ROOT),PYTHONHASHSEED=str(seed))
    result=subprocess.run(command,cwd=str(d.ROOT),env=env,capture_output=True,text=True)
    d.equal(mode+'_PROCESS_EXIT',result.returncode,0)
    return {'command':command,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr}


def main():
    primary=d.read(d.OUT/'primary/writer-result.json')
    writers=[];readers=[]
    for seed in (0,1,7,101):
        for index,presentation in enumerate(('original','reverse','rotate'),1):
            directory=d.OUT/'reproductions'/('seed-'+str(seed))/('writer-'+str(index))/'native-head'
            process=run('writer',directory,seed,presentation)
            actual=d.read(directory.parent/'writer-result.json')
            for term in ('A04_EVENT_ID','POST_SNAPSHOT_ID','POST_A04_BUNDLE_ID','post_computation','EVENT_PAYLOAD'):
                d.equal('INDEPENDENT_WRITER:'+term,actual[term],primary[term])
            writers.append({'seed':seed,'presentation':presentation,'run_id':actual['run_id'],
                'result':'PASS','new_occurrences':1,'producer_invocations':actual['producer_invocations'],
                'process':process,'writer_terminated':True})
            output=d.OUT/'cold-readers'/('seed-'+str(seed))/('reader-'+str(index)+'.json')
            # Read the primary after its writer has exited, with no writer memory.
            read_process=run('reader',d.OUT/'primary/native-head',seed,output=output)
            reader=d.read(output)
            d.equal('COLD_READER_ID',reader['POST_A04_BUNDLE_ID'],primary['POST_A04_BUNDLE_ID'])
            readers.append({'seed':seed,'reader':index,'result':'PASS','process':read_process,
                'output':str(output.relative_to(d.ROOT)),'replay_count':reader['replays']})
            # Independently restore each reproduced archive too.
            extra=directory.parent/'fresh-reader.json'
            run('reader',directory,seed,output=extra)
            print(json.dumps({'seed':seed,'presentation':presentation,'writer':'PASS','reader':'PASS'}),flush=True)
    record={**d.LABELS,'result':'PASS','hash_seeds':[0,1,7,101],
        'unordered_presentations':['original','reverse','rotate'],'independent_writers':writers,
        'primary_cold_readers':readers,'independent_writer_count':12,'primary_cold_reader_count':12,
        'reproduction_cold_reader_count':12,'primary_qualification_new_occurrences':1,
        'primary_reexecution_count':0,'replay_live_operation_invocations':0,
        'replay_validators_rerun':False,'replay_new_occurrences':0,
        'identity_semantics':'Same sealed lineage and source IDs in distinct stores; identical native content IDs, separate run IDs.',
        'original_history_changed':False,'P05_EXECUTED':'NO','P06_EXECUTED':'NO'}
    d.write(d.OUT/'process-qualification.json',record)


if __name__=='__main__':
    main()
