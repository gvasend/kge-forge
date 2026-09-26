"""Process-free, SHA-1-verified loose Git object reader for pinned captures.

No Git executable, refs, config, hooks, filters, alternates, replacement refs or
network are consulted. Packed/worktree/alternate stores fail closed.
"""
from pathlib import Path
import hashlib, re, zlib

class ObjectDenied(ValueError): pass
OID=re.compile(r'^[0-9a-f]{40}$')
LIMIT=8*1024*1024

def object_bytes(root, oid):
    if not isinstance(oid,str) or not OID.fullmatch(oid):
        raise ObjectDenied('full immutable object identity required')
    base=Path(root).resolve(); path=base/'.git'/'objects'/oid[:2]/oid[2:]
    from .controller_authority_store import authority_bytes, current
    if current() is None:
        for p in (base/'.git',base/'.git/objects',path.parent,path):
            if p.is_symlink(): raise ObjectDenied('object-store symlink denied')
        if not path.is_file() or path.stat().st_size>LIMIT:
            raise ObjectDenied('loose object unavailable or oversized; no fallback')
    compressed=authority_bytes('git-sha1:'+oid, evidence_path=str(path),
                               git_loader=path.read_bytes)
    if len(compressed)>LIMIT: raise ObjectDenied('compressed object oversized')
    decoder=zlib.decompressobj()
    try: raw=decoder.decompress(compressed,LIMIT+1)
    except zlib.error as exc: raise ObjectDenied('invalid compressed object') from exc
    if len(raw)>LIMIT or not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
        raise ObjectDenied('object expansion invalid or oversized')
    if hashlib.sha1(raw).hexdigest()!=oid: raise ObjectDenied('object identity mismatch')
    header,sep,data=raw.partition(b'\0')
    try: kind,size=header.decode('ascii').split(' ')
    except ValueError as exc: raise ObjectDenied('invalid object header') from exc
    if not sep or size!=str(len(data)) or kind not in ('commit','tree','blob'):
        raise ObjectDenied('invalid object type/size')
    return kind,data,compressed

def read_blob(root, revision, relative, collected=None):
    path=Path(relative)
    if not isinstance(relative,str) or not relative or path.is_absolute() or \
            '..' in path.parts or '.' in relative.split('/') or '\x00' in relative:
        raise ObjectDenied('invalid committed relative path')
    def get(oid,expected):
        kind,data,compressed=object_bytes(root,oid)
        if kind!=expected: raise ObjectDenied('unexpected object type')
        if collected is not None: collected[oid]=compressed
        return data
    commit=get(revision,'commit'); first=commit.split(b'\n',1)[0]
    if not first.startswith(b'tree '): raise ObjectDenied('commit tree absent')
    try: tree_oid=first[5:].decode('ascii')
    except UnicodeError as exc: raise ObjectDenied('tree identity invalid') from exc
    for i,part in enumerate(path.parts):
        tree=get(tree_oid,'tree'); entries={}
        while tree:
            head,sep,tail=tree.partition(b'\0')
            if not sep or len(tail)<20: raise ObjectDenied('tree truncated')
            try: mode,name=head.split(b' ',1); name=name.decode('utf-8')
            except (ValueError,UnicodeError) as exc: raise ObjectDenied('invalid tree entry') from exc
            if name in entries or '/' in name or name in ('.','..'):
                raise ObjectDenied('invalid tree name')
            entries[name]=(mode,tail[:20].hex()); tree=tail[20:]
        if part not in entries: raise ObjectDenied('committed file absent')
        mode,tree_oid=entries[part]
        if i==len(path.parts)-1:
            if mode not in (b'100644',b'100755'): raise ObjectDenied('not a committed regular file')
            return get(tree_oid,'blob')
        if mode!=b'40000': raise ObjectDenied('not a committed directory')
    raise ObjectDenied('committed file absent')
