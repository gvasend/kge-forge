"""Future independent reader callable; never invoked by Closure29.

Authority and supervisor-observed process facts must come from trusted launcher
callbacks, not self-declared writer/JSON flags. No save or Action call occurs.
"""
import hashlib,json,os
from pathlib import Path
from adapter.planner import codec,selector

def run_reader(spec, supervisor_evidence, scope_verifier, guard_verifier):
    if not callable(scope_verifier) or scope_verifier(spec) is not True:
        raise ValueError('FUTURE_READER_SCOPE_NOT_AUTHORIZED')
    if not callable(guard_verifier) or guard_verifier(spec,supervisor_evidence) is not True:
        raise ValueError('RUNTIME_GUARDS_NOT_ESTABLISHED_BY_TRUSTED_SUPERVISOR')
    if supervisor_evidence['writer_exit_code']!=0 or not supervisor_evidence['writer_exit_observed']:
        raise ValueError('WRITER_EXIT_NOT_OBSERVED')
    if os.getpid()==supervisor_evidence['writer_pid']:
        raise ValueError('WARM_READER')
    if not all(supervisor_evidence[g] for g in spec['REQUIRED_GUARDS']):
        raise ValueError('RUNTIME_GUARDS_UNMET')
    root=Path(spec['SOURCE_ROOT']);handoff=Path(spec['HANDOFF_PATH']);rawhandoff=handoff.read_bytes()
    if handoff.is_symlink() or hashlib.sha256(rawhandoff).hexdigest()!=spec['EXPECTED_HANDOFF_HASH']:
        raise ValueError('HANDOFF_IDENTITY_MISMATCH')
    record=json.loads(rawhandoff)
    if record!=spec['EXPECTED_HANDOFF_RECORD']:
        raise ValueError('HANDOFF_CONTENT_MISMATCH')
    target=Path(record['SAVED_PATH'])
    if str(target)!=spec['TARGET_PATH'] or target.is_symlink():
        raise ValueError('WRONG_PERSISTED_TARGET')
    raw=target.read_bytes()
    if len(raw)!=spec['EXPECTED_BYTE_LENGTH'] or hashlib.sha256(raw).hexdigest()!=spec['EXPECTED_HASH']:
        raise ValueError('PERSISTED_BYTES_MISMATCH')
    # Trusted identity comes from sealed independent spec, not from handoff alone.
    bundle=codec.restore(target,codec._unwire(spec['EXPECTED_BUNDLE_ID']),root)
    if bundle.events or bundle.policy_version!='E1-SELECTION-1-P06' or bundle.scope!='PARTIAL_HISTORICAL_REPLAY':
        raise ValueError('WRONG_FRAME_POLICY_OR_REPLAY_SCOPE')
    if codec._wire(codec.snapshot_id(bundle.current))!=spec['EXPECTED_SNAPSHOT_ID'] or codec.snapshot_id(bundle.initial)!=codec.snapshot_id(bundle.current):
        raise ValueError('RESTORED_CHECKPOINT_MISMATCH')
    expected_pins=sorted(spec['EXPECTED_SOURCE_PINS'],key=codec.canonical_bytes)
    if sorted(codec._wire(bundle.sources),key=codec.canonical_bytes)!=expected_pins:
        raise ValueError('RESTORED_SOURCE_SET_MISMATCH')
    selector.validate_policy(bundle.policy,bundle.policy_version)
    return {'schema':'A14-COLD-READER-IDENTITY-RESULT-1','restore_status':'PASS','bundle_identity':codec._wire(codec.bundle_id(bundle)),'snapshot_identity':codec._wire(codec.snapshot_id(bundle.current)),'policy_version':bundle.policy_version,'native_replay_scope':bundle.scope,'event_count':0,'source_policy_validation':'PASS','identity_comparison':'PASS','reader_pid':os.getpid(),'failure':None,'full_D01_output_comparison':'REQUIRES_SEPARATE_INDEPENDENT_OUTPUT_ORACLE'}

if __name__=='__main__':
    raise SystemExit('STATIC_ENTRYPOINT_ONLY: trusted future launcher must authorize independent run_reader')
