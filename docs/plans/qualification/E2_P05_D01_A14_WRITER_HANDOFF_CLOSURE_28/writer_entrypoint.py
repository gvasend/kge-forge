"""Future save-only writer callable; not executed by this package.

An external trusted qualification launcher must supply execution authorization.
The writer cannot launch the reader or prove its own subsequent process exit.
"""
import hashlib,json
from pathlib import Path
from adapter.planner import codec

def run_writer(spec, scope_verifier):
    if not callable(scope_verifier) or scope_verifier(spec) is not True:
        raise ValueError('TRUSTED_FUTURE_SAVE_EXECUTION_SCOPE_REQUIRED')
    root=Path(spec['SOURCE_ROOT']);source=root/spec['INPUT_SOURCE']['path'];raw=source.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=spec['EXPECTED_BUNDLE_ID']['sha256']:
        raise ValueError('WRONG_INPUT_BYTES')
    bundle=codec._unwire(json.loads(raw)['bundle'])
    if bundle.events or bundle.dossier_materializations:
        raise ValueError('ZERO_EVENT_FRAME_REQUIRED')
    if codec.bundle_bytes(bundle)!=raw:
        raise ValueError('INPUT_NOT_EXACT_NATIVE_BYTES')
    saved_path,saved_id=codec.save_bundle(bundle,Path(spec['OUTPUT_DIRECTORY']),root,
                                         snapshot_resolver=None,failure_hook=None)
    if str(saved_path)!=spec['EXPECTED_TARGET'] or codec._wire(saved_id)!=spec['EXPECTED_BUNDLE_ID']:
        raise ValueError('SAVE_RETURN_MISMATCH')
    if saved_path.is_symlink() or saved_path.read_bytes()!=raw:
        raise ValueError('PUBLISHED_SOURCE_MISMATCH')
    record=spec['EXPECTED_SUCCESS_HANDOFF_RECORD']
    if record['SAVED_PATH']!=str(saved_path) or record['SAVED_NATIVE_ID']!=codec._wire(saved_id):
        raise ValueError('HANDOFF_MISMATCH')
    # Qualification metadata publication only, after native save success.
    # This file also has no directory-fsync/general crash guarantee.
    codec._write_immutable(saved_path.parent,Path(spec['HANDOFF_PATH']).name,
                           codec.canonical_bytes(record))
    # No core.recompute, result/event application, HEAD operation or reader.
    return None

if __name__=='__main__':
    raise SystemExit('STATIC_ENTRYPOINT_ONLY: trusted future launcher must authorize run_writer')
