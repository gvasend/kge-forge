"""Controller-owned, byte-attributed input copy for one governed execution."""
from pathlib import Path
import hashlib, json, os, stat, tempfile

class SnapshotDenied(RuntimeError): pass

MAX_FILES=2000
MAX_BYTES=64*1024*1024
MAX_FILE_BYTES=8*1024*1024

def _digest(data): return hashlib.sha256(data).hexdigest()

def construct(source_root, requested, authorize, evidence_dir, scope_id,
              provenance=None, context_identity=None):
    source_root=Path(source_root).resolve()
    if not isinstance(requested,list) or len(requested)>100 or not all(
            isinstance(item,str) and item for item in requested):
        raise SnapshotDenied('invalid execution inputs')
    workspace=Path(tempfile.mkdtemp(prefix='a2-exec-',dir='/tmp')).resolve()
    files={}; omitted=[]; total=0
    for raw in requested:
        relative=Path(raw)
        if relative.is_absolute() or '..' in relative.parts:
            raise SnapshotDenied('execution input escape')
        entry=source_root/relative
        if entry.is_symlink(): raise SnapshotDenied('execution input symlink')
        if not entry.exists(): raise SnapshotDenied('execution input unavailable')
        explicit_file=not entry.is_dir()
        if not explicit_file:
            candidates=[]
            for directory,subdirs,names in os.walk(entry,followlinks=False):
                subdirs[:]=sorted(name for name in subdirs
                                  if not (Path(directory)/name).is_symlink())
                candidates.extend(Path(directory)/name for name in sorted(names))
        else: candidates=[entry]
        for candidate in candidates:
            rel=candidate.relative_to(source_root).as_posix()
            if candidate.is_symlink(): omitted.append(rel); continue
            try: authorized=authorize(rel)
            except Exception as exc:
                if explicit_file:
                    raise SnapshotDenied('execution input denied: '+rel) from exc
                omitted.append(rel); continue
            if authorized!=candidate.resolve() or not candidate.is_file():
                omitted.append(rel); continue
            if rel in files: continue
            fd=os.open(candidate,os.O_RDONLY|os.O_NOFOLLOW)
            try:
                meta=os.fstat(fd)
                if not stat.S_ISREG(meta.st_mode) or meta.st_size>MAX_FILE_BYTES:
                    raise SnapshotDenied('execution input type or size denied')
                data=b''
                while len(data)<=MAX_FILE_BYTES:
                    chunk=os.read(fd,65536)
                    if not chunk: break
                    data+=chunk
                if len(data)>MAX_FILE_BYTES: raise SnapshotDenied('execution input too large')
            finally: os.close(fd)
            total+=len(data)
            if len(files)>=MAX_FILES or total>MAX_BYTES:
                raise SnapshotDenied('execution snapshot limit')
            target=workspace/rel
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(data)
            target.chmod(stat.S_IMODE(meta.st_mode)&0o777)
            files[rel]={'sha256':_digest(data),'size':len(data),
                        'source_dev':meta.st_dev,'source_ino':meta.st_ino}
            if provenance is not None:
                identity=provenance(candidate,files[rel]['sha256'])
                if not isinstance(identity,dict):
                    raise SnapshotDenied('execution input lacks authoritative provenance')
                files[rel]['authority_provenance']=identity
    # Verify all copied source bytes still match the recorded capture. This is
    # a fail-closed check against a concurrent source change during copying.
    for rel,record in files.items():
        candidate=source_root/rel
        if candidate.is_symlink() or _digest(candidate.read_bytes())!=record['sha256']:
            raise SnapshotDenied('authoritative source changed during capture')
    manifest={'scope_id':scope_id,'source_root':str(source_root),
              'workspace_root':str(workspace),'requested':requested,
              'files':files,'omitted':sorted(set(omitted))}
    if context_identity is not None: manifest['context_identity']=context_identity
    canonical=json.dumps(manifest,sort_keys=True,separators=(',',':')).encode()
    manifest['manifest_sha256']=_digest(canonical)
    path=Path(evidence_dir).resolve()/'snapshots'/f'{scope_id}.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,'wb') as stream:
        stream.write(json.dumps(manifest,sort_keys=True,indent=2).encode())
        stream.flush(); os.fsync(stream.fileno())
    return workspace,manifest,path

def observe(workspace, manifest):
    """Verify authoritative capture stayed fixed and summarize scratch effects."""
    source_root=Path(manifest['source_root'])
    for rel,record in manifest['files'].items():
        source=source_root/rel
        if source.is_symlink() or not source.is_file() or \
                _digest(source.read_bytes())!=record['sha256']:
            raise SnapshotDenied('authoritative source changed during execution')
    current={}; total=0
    for directory,subdirs,names in os.walk(workspace,followlinks=False):
        subdirs[:]=sorted(name for name in subdirs
                          if not (Path(directory)/name).is_symlink())
        for name in sorted(names):
            candidate=Path(directory)/name
            rel=candidate.relative_to(workspace).as_posix()
            if candidate.is_symlink(): current[rel]={'type':'symlink'}; continue
            if not candidate.is_file(): current[rel]={'type':'other'}; continue
            size=candidate.stat().st_size
            if size>MAX_FILE_BYTES: raise SnapshotDenied('workspace output too large')
            total+=size
            if len(current)>=MAX_FILES or total>MAX_BYTES:
                raise SnapshotDenied('workspace observation limit')
            current[rel]={'type':'file','sha256':_digest(candidate.read_bytes()),
                          'size':size}
    changed={rel:state for rel,state in current.items()
             if rel not in manifest['files'] or
                state.get('sha256')!=manifest['files'][rel]['sha256']}
    deleted=sorted(set(manifest['files'])-set(current))
    return {'changed':changed,'deleted':deleted,
            'authoritative_source_unchanged':True}
