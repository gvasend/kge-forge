"""Construct a narrow effective Programmer authorization from captured context."""
from pathlib import Path
from .context_binding import ContextDenied
from .governed_host import WorkAuthorization

def _relative(raw):
    if not isinstance(raw,str) or not raw or raw=='.' or not Path(raw).parts or \
            Path(raw).is_absolute() or \
            '..' in Path(raw).parts:
        raise ContextDenied('scope path invalid')
    return raw

def programmer_authorization(binding, authorization_id, revision, session_id,
                             turn_id, exec_argv_allowlist=(),diagnostic=False):
    binding.verify()
    scope=binding.manifest.get('scope')
    if not isinstance(scope,dict) or scope.get('task_tool_network')!='DENIED' or \
            scope.get('unrelated_connectors')!='DENIED':
        raise ContextDenied('external authority profile not closed')
    forge=binding.repos['forge']
    read=tuple(Path(raw).resolve() for raw in scope.get('read_roots',[]))
    if set(read)!=set(binding.repos.values()):
        raise ContextDenied('context read roots and repository identities mismatch')
    writes=tuple(str(forge/_relative(raw)) for raw in scope.get('writable_paths',[]))
    protected=tuple(str(forge/_relative(raw)) for raw in scope.get('protected_paths',[]))
    if not writes or not protected: raise ContextDenied('scope grants missing')
    # The prepared E1 protected list is a write boundary. The hidden host
    # directories have no model-readable engineering purpose.
    read_denies=tuple(str(forge/name) for name in ('.git','.codex','.agents'))
    commands=tuple(tuple(command) for command in exec_argv_allowlist)
    if any(not command or any(not isinstance(part,str) or not part for part in command)
           for command in commands): raise ContextDenied('execution command grant invalid')
    bins=tuple(sorted({Path(command[0]).name for command in commands}))
    if diagnostic:
        if binding.manifest.get('status')!='DIAGNOSTIC_AUTHORIZED' or \
                binding.manifest.get('work_id')=='E1-WP-001' or \
                any(Path('/tmp') not in root.parents for root in binding.repos.values()):
            raise ContextDenied('diagnostic activation outside scratch authority')
    state='ACTIVE' if diagnostic else 'INACTIVE'
    return WorkAuthorization(authorization_id,revision,binding.manifest['work_id'],
        session_id,turn_id,tuple(str(root) for root in read),writes,(),bins,
        shell=False,network=False,state=state,context_binding=binding,
        exec_argv_allowlist=commands,read_deny_roots=read_denies,
        write_deny_roots=protected,
        ownership_ledger='' if diagnostic else '/tmp/kge-forge-e1-invocations.jsonl')
