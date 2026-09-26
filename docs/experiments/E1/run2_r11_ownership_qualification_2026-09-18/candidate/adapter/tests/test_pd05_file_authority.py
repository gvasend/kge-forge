"""Synthetic committed two-repository qualification; never activates E1."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from adapter.authority_profile import programmer_authorization
from adapter.context_binding import CommittedContext
from adapter.governed_host import GovernedHost
from adapter.orchestrator import ReasoningOrchestrator
from adapter.responses_orchestrator import ResponsesReasoning


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory(root):
    """Complete synthetic worktree inventory; Git internals are not read."""
    result={}
    def walk(directory):
        for p in sorted(directory.iterdir()):
            rel=p.relative_to(root).as_posix()
            if p.name=='.git':
                result[rel]={'type':'git_directory_not_inspected'}
            elif p.is_symlink():
                result[rel]={'type':'symlink'}
            elif p.is_dir():
                result[rel]={'type':'directory'}; walk(p)
            else:
                data=p.read_bytes()
                result[rel]={'type':'file','sha256':digest(data),'bytes_hex':data.hex()}
    walk(root)
    return result


def qualify(evidence):
    evidence=Path(evidence); evidence.mkdir(parents=True,exist_ok=True)
    base=Path(tempfile.mkdtemp(prefix='pd05-qualified-scratch-'))
    report={'fixture_root':str(base),'model_calls':0,'execution_scopes':0,'cases':[]}
    for variant in ('normal','missing_directory_root','directory_root_is_file',
                    'leaf_is_directory','parent_is_file'):
        case=base/variant; forge=case/'forge'; service=case/'service'
        for repo in (forge,service):
            repo.mkdir(parents=True)
            subprocess.run(['/usr/bin/git','-C',str(repo),'init','-q'],check=True)
            (repo/'package.txt').write_text('DECIDED synthetic fixture, not E1 implementation\n')
            for hidden in ('.git','.codex','.agents'):
                (repo/hidden).mkdir(exist_ok=True)
                (repo/hidden/'pd05-marker.txt').write_text('SYNTHETIC_HIDDEN_NEEDLE\n')
            (repo/'visible.txt').write_text('VISIBLE_NEEDLE\n')
        (forge/'src/kge_forge/context').mkdir(parents=True)
        (forge/'src/kge_forge/context/protected.txt').write_text('PROTECTED\n')
        leaf=forge/'src/kge_forge/__init__.py'
        if variant=='leaf_is_directory': leaf.mkdir()
        else: leaf.write_text('# synthetic original\n')
        (forge/'tests').mkdir()
        if variant=='directory_root_is_file': (forge/'tests/context').write_text('WRONG TYPE\n')
        elif variant!='missing_directory_root': (forge/'tests/context').mkdir()
        if variant=='parent_is_file': (forge/'docs').write_text('WRONG TYPE\n')
        # The file grant docs/implementation/E1-WP-001.md has no parent directory.
        manifest={'schema_version':'E1-CONTEXT-1','baseline_id':'synthetic-pd05',
            'work_id':'scratch-pd05-'+variant,'status':'DIAGNOSTIC_AUTHORIZED',
            'repositories':{'forge':{'root':str(forge)},'service':{'root':str(service)}},
            'sources':[{'id':'package','repository':'forge','path':'package.txt',
                'sha256':digest((forge/'package.txt').read_bytes()),
                'revision_binding':'package_capture_commit','knowledge_status':'DECIDED',
                'dependencies':[]}], 'mandatory_roots':['package'],
            'scope':{'read_roots':[str(forge),str(service)],
                'writable_paths':['src/kge_forge/__init__.py','src/kge_forge/context/',
                                  'tests/context/','docs/implementation/E1-WP-001.md'],
                'protected_paths':['package.txt','src/kge_forge/context/protected.txt'],
                'task_tool_network':'DENIED','unrelated_connectors':'DENIED'},
            'prerequisites':[]}
        path=forge/'CONTEXT_MANIFEST.json'; path.write_text(json.dumps(manifest,indent=2))
        commits={}
        for alias,repo in (('service',service),('forge',forge)):
            subprocess.run(['/usr/bin/git','-C',str(repo),'add','.'],check=True)
            subprocess.run(['/usr/bin/git','-C',str(repo),'-c','core.hooksPath=/dev/null',
                '-c','user.name=PD05 Scratch','-c','user.email=scratch@example.invalid',
                'commit','-qm','Synthetic PD05 capture'],check=True)
            commits[alias]=subprocess.check_output(['/usr/bin/git','-C',str(repo),
                'rev-parse','HEAD'],text=True).strip()
        binding=CommittedContext(path,commits['forge'])
        auth=programmer_authorization(binding,'auth-pd05-'+variant,1,
            'session-pd05-'+variant,'turn-pd05-'+variant,diagnostic=True)
        host=GovernedHost(auth,evidence/(variant+'.jsonl'))
        runner=ResponsesReasoning(ReasoningOrchestrator(host))
        observations=[]
        def call(name,label,args,expected,changed=()):
            before=inventory(case)
            result=runner._dispatch({'name':name,'call_id':label,
                                      'arguments':json.dumps(args)})
            after=inventory(case)
            changes=sorted(k for k in set(before)|set(after) if before.get(k)!=after.get(k))
            assert result['result']==expected,(label,result)
            assert changes==sorted('forge/'+p for p in changed),(label,changes,changed)
            events=[json.loads(line) for line in host.audit.read_text().splitlines()]
            intent=next(i for i,e in enumerate(events) if e.get('event')=='action_request'
                        and e.get('action_request_id')==label)
            terminal=next(i for i,e in enumerate(events) if e.get('event')=='action_result'
                          and e.get('action_request_id')==label)
            assert intent<terminal
            observations.append({'label':label,'tool':name,'arguments':args,'result':result,
                'before':before,'after':after,'changed':changes,
                'audit_request_index':intent,'audit_result_index':terminal})
            return result
        if variant=='normal':
            for alias,repo in (('forge',forge),('service',service)):
                for hidden in ('.git','.codex','.agents'):
                    common={'repository':str(repo),'limit':100}
                    call('governed_read',alias+hidden+'-read',
                         {**common,'path':hidden+'/pd05-marker.txt'},'DENIED')
                    call('governed_list',alias+hidden+'-list',{**common,'path':hidden},'DENIED')
                    call('governed_search',alias+hidden+'-search',
                         {**common,'path':hidden,'query':'SYNTHETIC_HIDDEN_NEEDLE'},'DENIED')
                listed=call('governed_list',alias+'-root-list',
                    {'repository':str(repo),'path':'.','limit':100},'SUCCEEDED')
                assert not {'.git','.codex','.agents'} & {e['name'] for e in listed['data']['entries']}
                searched=call('governed_search',alias+'-root-search',
                    {'repository':str(repo),'path':'.','query':'SYNTHETIC_HIDDEN_NEEDLE','limit':100},'SUCCEEDED')
                assert searched['data']['matches']==[]
                visible=call('governed_search',alias+'-visible-search',
                    {'repository':str(repo),'path':'.','query':'VISIBLE_NEEDLE','limit':100},'SUCCEEDED')
                assert len(visible['data']['matches'])==1
            def write(label,rel,expected,changed=()):
                return call('governed_write',label,{'repository':str(forge),
                    'path':rel,'content':'# synthetic changed\n'},expected,changed)
            write('replace-leaf','src/kge_forge/__init__.py','SUCCEEDED',
                  ['src/kge_forge/__init__.py'])
            write('nested-context','src/kge_forge/context/a/b/module.py','SUCCEEDED',
                  ['src/kge_forge/context/a','src/kge_forge/context/a/b',
                   'src/kge_forge/context/a/b/module.py'])
            write('nested-tests','tests/context/a/test_sample.py','SUCCEEDED',
                  ['tests/context/a','tests/context/a/test_sample.py'])
            write('sibling','src/kge_forge/other.py','DENIED')
            write('protected','src/kge_forge/context/protected.txt','DENIED')
            write('missing-leaf-parent','docs/implementation/E1-WP-001.md','DENIED')
            write('write-directory-root','src/kge_forge/context','DENIED')
            write('write-existing-directory','src/kge_forge/context/a','DENIED')
            write('parent-is-regular-file','src/kge_forge/context/a/b/module.py/child','DENIED')
            call('governed_write','service-write',{'repository':str(service),
                 'path':'visible.txt','content':'DENIED'},'DENIED')
            patch_rel='src/kge_forge/context/a/b/module.py'; content='# positively patched\n'
            call('governed_patch','positive-patch',{'repository':str(forge),
                'changes':[{'op':'write','path':patch_rel,'content':content}]},
                'SUCCEEDED',[patch_rel])
            provenance=host._source_effects[str(forge/patch_rel)]
            assert provenance=={'kind':'governed_action','action_request_id':'positive-patch',
                                'sha256':digest(content.encode())}
            call('governed_patch','protected-patch',{'repository':str(forge),
                'changes':[{'op':'write','path':'src/kge_forge/context/protected.txt',
                            'content':'DENIED'}]},'DENIED')
            call('governed_patch','missing-parent-patch',{'repository':str(forge),
                'changes':[{'op':'write','path':'src/kge_forge/context/absent/file.py',
                            'content':'DENIED'}]},'DENIED')
        else:
            rel={'missing_directory_root':'tests/context/child/file.py',
                 'directory_root_is_file':'tests/context/child/file.py',
                 'leaf_is_directory':'src/kge_forge/__init__.py',
                 'parent_is_file':'docs/implementation/E1-WP-001.md'}[variant]
            call('governed_write',variant,{'repository':str(forge),'path':rel,
                                         'content':'DENIED'},'DENIED')
            if variant=='leaf_is_directory':
                call('governed_write','leaf-descendant',{'repository':str(forge),
                    'path':rel+'/child','content':'DENIED'},'DENIED')
        assert host.scope is None and not auth.exec_bins
        report['cases'].append({'variant':variant,'capture_commits':commits,
            'context_sha256':binding.digest,'observations':observations,
            'source_effects':host._source_effects,'binding_still_valid':binding.verify()})
    report['result']='PASS'
    (evidence/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


class PD05FileAuthorityTests(unittest.TestCase):
    def test_committed_two_root_dispatcher_qualification(self):
        with tempfile.TemporaryDirectory(prefix='pd05-test-evidence-') as out:
            result=qualify(out)
            self.assertEqual(result['result'],'PASS')


if __name__=='__main__':
    unittest.main()
