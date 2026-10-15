"""Fresh readers after the I02 writer exits; no configuration/lifecycle writes."""
import json,os,subprocess,sys
from pathlib import Path
from adapter.planner import codec as c
R=Path(__file__).resolve().parents[2];D=R/'docs/plans';P='DETERMINISTIC_PLANNER_V0_1_'
O=D/'qualification/INSTALLATION_I02_1'
PROGRAM='''import json,sys
from adapter.planner import model as m,codec as c,core,gates,installation as i
b=c.restore(sys.argv[1],c._unwire(json.loads(sys.argv[2])),sys.argv[3])
state=c._replay(b)
assert c.snapshot_id(state)==c._unwire(json.loads(sys.argv[4]))
assert core.recompute(state).control is m.ControlState.EXTERNAL_WAIT
assert not state.receipt_admissions and not state.receipt_observations and not state.typed_proofs
assert not any(e.kind is m.EntityKind.EVIDENCE for e in state.entities)
g=state.external_gates[0];q=state.evidence_requirements[0]
route_current=gates.governed_external_unknown(state,g,q,g.reentry[0])
assert route_current==(sys.argv[5]=='post')
if sys.argv[5]=='post':
 assert len(state.installed_definitions)==1 and i.current(b,state.installed_definitions[0])
 assert len(b.events)==3 and type(b.events[-1].result) is m.InstallDefinition
 assert sum(type(e.result) is m.InstallDefinition for e in b.events)==1
else:assert not state.installed_definitions and len(b.events)==2
print(json.dumps({'bundle':c._wire(c.bundle_id(b)),'state':c._wire(c.snapshot_id(state)),
 'append_head':c._wire(b.events[-1].identity),'ledger_root':c._wire(b.events[0].identity),
 'source_pins':c._wire(b.sources),'policy':c._wire(b.policy),'scope_lineage':c._wire(state.context),
 'installed_definitions':c._wire(state.installed_definitions),'route':c._wire(g.resolution_contracts),
 'control':core.recompute(state).control.value,'authority_use_count':len(state.installed_definitions),
 'route_current':route_current}))
'''

def run():
    report=json.loads((O/'post-install-evidence.json').read_text())
    oracle=json.loads((O/'pre-install-oracle.json').read_text())
    i01=json.loads((D/(P+'INSTALLATION_I01_CONTRACT.json')).read_text())['P04_route_application']
    rows=[]
    for stage,path,bid,sid in [('pre',D/(P+'P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1.json'),i01['pre_bundle'],i01['pre_state']),
            ('post',R/report['P04_POST_INSTALL_BUNDLE_PATH'],report['P04_POST_INSTALL_BUNDLE_ID'],oracle['expected_post_state'])]:
        expected=None
        for seed in ('0','1','7','101'):
            for reader in range(3):
                env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED=seed,PYTHONPATH=str(R))
                run=subprocess.run([sys.executable,'-c',PROGRAM,str(path),json.dumps(bid),str(R),json.dumps(sid),stage],
                    env=env,cwd=str(R),capture_output=True,text=True)
                assert run.returncode==0,run.stderr
                value=json.loads(run.stdout)
                if expected is None:expected=value
                assert value==expected,'Fresh reader semantic/pin/authority/ancestry mismatch'
                rows.append({'checkpoint':stage,'hash_seed':int(seed),'reader':reader,
                    'result':'PASS','equality_domains':['semantic_state','definition_identity','canonical_bytes_content_id',
                    'source_pins','policy','authority','scope_lineage_generation','provenance','event_ancestry','control','authority_use'],
                    'state':value['state'],'bundle':value['bundle'],'append_head':value['append_head']})
    out={'writer_exited_before_readers':True,'comparisons':rows,'count':len(rows),'result':'PASS',
        'cold_restore':'PASS','replay':'PASS','same_semantics_across_seeds_readers':'PASS'}
    (O/'fresh-readers.json').write_bytes(c.canonical_bytes(out))
    print(json.dumps({'fresh_reader_comparisons':len(rows),'result':'PASS'}))

if __name__=='__main__':run()
