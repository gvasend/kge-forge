"""Private controller resolution. Repository paths are provenance, never selectors.

The controller pins a catalog hash at bootstrap. Import is a controller operation,
not a Programmer tool or an authority-issuance operation. Existing content and
ancestry verifiers still decide whether the imported material grants authority.
Mutable state stays behind existing typed lifecycle/ownership/audit operations.
"""
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path
import hashlib
import json
import os
import re
import stat
from types import MappingProxyType

_current = ContextVar('controller_authority_store', default=None)
_capture = ContextVar('controller_authority_evidence_capture', default=None)
_resolution_witness = ContextVar('controller_immutable_resolution_witness', default=None)
HEX = re.compile(r'^[0-9a-f]{64}$')

def _freeze(value):
    if isinstance(value,dict):return MappingProxyType({k:_freeze(v) for k,v in value.items()})
    if isinstance(value,list):return tuple(_freeze(v) for v in value)
    return value


class AuthorityDenied(ValueError):
    pass


def encoded(value):
    def proxy(obj):
        if isinstance(obj,MappingProxyType):return dict(obj)
        raise TypeError('not an authority JSON value')
    return json.dumps(value, sort_keys=True, separators=(',', ':'),default=proxy).encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def current():
    return _current.get()


def roots_for(auth):
    runtime = json.loads(auth.execution_profile or '{}')
    policy = json.loads(auth.model_transmission or '{}')
    roots = set((*auth.read_roots, *auth.write_roots, *auth.write_directory_roots))
    if runtime.get('cwd'):
        roots.add(runtime['cwd'])
        roots.update(str(Path(runtime['cwd']) / p) for p in runtime.get('inputs', []))
    roots.update(policy.get('transmission_roots', []))
    roots.update(row['path'] for row in policy.get('file_clearances', []))
    return sorted(roots)


def outside_many(paths, roots):
    """Fresh placement observation; share grant resolution only inside this call.

    No filesystem observation survives the predicate. Each private path is still
    resolved, including absent audit paths. No immutable-byte or state cache.
    """
    resolved = tuple(Path(raw).resolve().parts for raw in roots)
    for path in paths:
        p = Path(path)
        if not p.is_absolute() or p.resolve() != p:
            raise AuthorityDenied('noncanonical private authority path')
        parts = p.parts
        for root in resolved:
            if parts[:len(root)] == root or root[:len(parts)] == parts:
                raise AuthorityDenied('controller authority inside Programmer authority')


def outside(path, roots):
    outside_many((path,), roots)


def _directory(path):
    """Open every component without following symlinks, including ancestors."""
    path = Path(path)
    if not path.is_absolute() or '..' in path.parts:
        raise AuthorityDenied('absolute canonical store directory required')
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parts[1:]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        st = os.fstat(fd)
        if st.st_uid != os.getuid() or stat.S_IMODE(st.st_mode) & 0o077:
            raise AuthorityDenied('authority directory is not controller private')
        return fd
    except BaseException:
        os.close(fd)
        raise


def _read(fd, name):
    if '/' in name or name in ('', '.', '..'):
        raise AuthorityDenied('invalid authority object name')
    obj = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=fd)
    try:
        st = os.fstat(obj)
        if (not stat.S_ISREG(st.st_mode) or st.st_uid != os.getuid() or
                stat.S_IMODE(st.st_mode) & 0o077 or st.st_nlink != 1 or st.st_size > 64*1024*1024):
            raise AuthorityDenied('authority object ownership/type/mode invalid')
        with os.fdopen(os.dup(obj), 'rb') as stream:
            return stream.read(64*1024*1024 + 1)
    finally:
        os.close(obj)


def _put(fd, name, data):
    obj = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=fd)
    with os.fdopen(obj, 'wb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


@contextmanager
def capture_evidence():
    """Offline dependency inventory only. Never usable inside production resolution."""
    if current() is not None:
        raise AuthorityDenied('evidence capture cannot replace production authority')
    records = {}
    token = _capture.set(records)
    try:
        yield records
    finally:
        _capture.reset(token)


def authority_bytes(identity, *, evidence_path=None, git_loader=None):
    """Resolve stable existing content IDs; evidence fallback is offline-only.

Production entrypoints require an active store. A private session never falls
back, even when repository bytes match. Legacy serialized paths are only useful
to the offline engineering reader and provenance capture.
"""
    if current() is not None:
        return current().resolve(identity)
    if git_loader is not None:
        data = git_loader()
    else:
        from .context_projection import read_exact
        if not identity.startswith('sha256:'):
            raise AuthorityDenied('offline content identity unsupported')
        data = read_exact(evidence_path, identity[7:])
    if _capture.get() is not None:
        row = _capture.get().setdefault(identity, {'bytes': data, 'evidence': []})
        if row['bytes'] != data:
            raise AuthorityDenied('ambiguous evidence content')
        ref = {'path': str(evidence_path), 'sha256': sha(data)}
        if ref not in row['evidence']:
            row['evidence'].append(ref)
    return data


def read_authority_ref(ref):
    if 'authority_id' in ref:
        if current() is None or set(ref) != {'authority_id','sha256'}:
            raise AuthorityDenied('private logical authority reference required')
        data = current().resolve(ref['authority_id'])
        if sha(data) != ref['sha256']:
            raise AuthorityDenied('logical authority reference hash mismatch')
        return data
    return authority_bytes('sha256:' + ref['sha256'], evidence_path=ref.get('path'))


class ControllerAuthorityStore:
    def __init__(self, root, catalog_sha256, applicability):
        if not HEX.fullmatch(catalog_sha256):
            raise AuthorityDenied('controller-pinned catalog identity required')
        self.root = Path(root)
        self.catalog_sha256 = catalog_sha256
        self.applicability = json.loads(encoded(applicability))
        self.fd = _directory(self.root)
        try:
            self.catalog = json.loads(_read(self.fd, 'catalog.json'))
            self._issued_catalog=self.catalog
            self._issued_catalog_sha256=sha(encoded(self.catalog))
            self._verify_catalog()
            self.catalog=_freeze(self.catalog)
            self._issued_catalog=self.catalog
        except BaseException:
            self.close()
            raise

    @classmethod
    def materialize(cls, root, records, aliases, provenance, applicability, programmer_roots,
                    private_state=None):
        """Exclusive, batch materialization; no updates, grants, or adoption.

        Caller supplies exact selected content. The catalog must subsequently be
        pinned by a qualified controller bootstrap/continuation before production.
        """
        root = Path(root)
        outside(root, programmer_roots)
        root.mkdir(mode=0o700)  # parent must already be controller-selected
        fd = _directory(root)
        try:
            objects = {}
            written = set()
            for identity, item in sorted(records.items()):
                data = item['bytes']
                h = sha(data)
                if h not in written:
                    _put(fd, h, data)
                    written.add(h)
                objects[identity] = {'sha256': h, 'evidence': item['evidence'],
                    'authority_source': provenance['authority_source'],
                    'release_identities': provenance['release_identities'],
                    'temporal_applicability': applicability, 'mutation': 'IMMUTABLE'}
            for alias, identity in aliases.items():
                if alias in objects or identity not in objects or '/' in alias:
                    raise AuthorityDenied('invalid logical authority alias')
                objects[alias] = objects[identity]
            catalog = {'schema': 'CONTROLLER-AUTHORITY-STORE-1',
                'applicability': applicability, 'programmer_roots': sorted(programmer_roots),
                'objects': objects, 'private_state': private_state or {}}
            data = encoded(catalog)
            _put(fd, 'catalog.json', data)
            os.fsync(fd)
        finally:
            os.close(fd)
        return cls(root, sha(data), applicability)

    def _verify_catalog(self):
        if (sha(_read(self.fd, 'catalog.json')) != self.catalog_sha256 or
                self.catalog is not self._issued_catalog or
                self._issued_catalog_sha256 != self.catalog_sha256):
            raise AuthorityDenied('authority catalog hash mismatch')
        disk = self.root.lstat()
        held = os.fstat(self.fd)
        if (disk.st_dev, disk.st_ino) != (held.st_dev, held.st_ino):
            raise AuthorityDenied('authority store directory replaced')
        c = self.catalog
        if c.get('schema') != 'CONTROLLER-AUTHORITY-STORE-1' or c.get('applicability') != self.applicability:
            raise AuthorityDenied('stale authority applicability')
        outside_many((self.root, *(r['path'] for r in c['private_state'].values())), c['programmer_roots'])
        # Content equality is freshly established above against the external pin.
        # Only pure validation of those immutable bytes is reusable. Locations of
        # mutable state and grants are checked on EVERY call; objects are reread
        # and hashed in resolve. No lifecycle/head/readiness result is cached.
        if getattr(self, '_validated_catalog_sha256', None) == self.catalog_sha256:
            return
        for identity, row in c['objects'].items():
            if (not isinstance(identity, str) or '/' in identity or not identity or
                    not HEX.fullmatch(row.get('sha256', '')) or
                    not isinstance(row.get('authority_source'), dict) or
                    not HEX.fullmatch(row.get('authority_source', {}).get('sha256', '')) or
                    not {'ReleaseBasisId','ReleaseDecisionId'} <= set(row.get('release_identities', {})) or
                    row.get('temporal_applicability') != self.applicability or
                    row.get('mutation') != 'IMMUTABLE' or not isinstance(row.get('evidence'), list) or
                    any(set(e) != {'path', 'sha256'} or e['sha256'] != row['sha256'] for e in row['evidence'])):
                raise AuthorityDenied('incomplete authority provenance')
            if identity.startswith('sha256:') and identity[7:] != row['sha256']:
                raise AuthorityDenied('logical content identity mismatch')
        for record in c['private_state'].values():
            if record.get('mutation') not in ('APPEND_ONLY', 'TYPED_LIFECYCLE') or not record.get('mechanism'):
                raise AuthorityDenied('untyped private mutable authority')
            outside(record['path'], c['programmer_roots'])
        self._validated_catalog_sha256 = self.catalog_sha256

    def resolve(self, identity):
        self._verify_catalog()
        if not isinstance(identity, str) or '/' in identity or identity not in self.catalog['objects']:
            raise AuthorityDenied('unknown logical authority identity; paths are not selectors')
        row = self.catalog['objects'][identity]
        data = _read(self.fd, row['sha256'])
        if sha(data) != row['sha256']:
            raise AuthorityDenied('private authority artifact hash mismatch')
        witness = _resolution_witness.get()
        if witness is not None:
            if witness['store'] is not self:raise AuthorityDenied('cross-store resolution witness')
            witness['objects'][identity]=row['sha256']
        return data

    @contextmanager
    def witness(self):
        if _resolution_witness.get() is not None:raise AuthorityDenied('nested resolution witness')
        objects={};token=_resolution_witness.set({'store':self,'objects':objects})
        try:yield objects
        finally:_resolution_witness.reset(token)

    def verify_immutable_witness(self, objects):
        # Reuse pure parsing/ancestry evaluation only. Every object is reopened,
        # ownership/type checked and hashed against the externally pinned catalog.
        # No effect occurs in this batch. Mutable placement/catalog is checked
        # at both boundaries; fd-relative reads never follow a relocated path.
        self._verify_catalog()
        for identity,expected in objects.items():
            if identity not in self.catalog['objects'] or self.catalog['objects'][identity]['sha256']!=expected:
                raise AuthorityDenied('immutable resolution witness selection changed')
            if sha(_read(self.fd,expected))!=expected:
                raise AuthorityDenied('immutable resolution witness object changed')
        self._verify_catalog()

    def location(self, identity):
        self.resolve(identity)
        return self.root / self.catalog['objects'][identity]['sha256']

    def state_path(self, identity):
        self._verify_catalog()
        if identity not in self.catalog['private_state']:
            raise AuthorityDenied('unknown private state identity')
        row = self.catalog['private_state'][identity]
        outside(row['path'], self.catalog['programmer_roots'])
        st = Path(row['path']).lstat()
        if not stat.S_ISREG(st.st_mode) or st.st_uid != os.getuid() or st.st_mode & 0o077 or st.st_nlink != 1:
            raise AuthorityDenied('private state ownership/type/mode invalid')
        return Path(row['path'])

    def require(self, auth, audit=None):
        self._verify_catalog()
        op = json.loads(auth.operational_binding)
        expected = {'authorization_id': auth.authorization_id,
                    **op['governance']['identities']}
        if self.applicability != expected:
            raise AuthorityDenied('authority store is stale for operational ancestry')
        outside(self.root, roots_for(auth))
        if sorted(roots_for(auth)) != list(self.catalog['programmer_roots']):
            raise AuthorityDenied('Programmer authority changed after store binding')
        for role, path in [('ownership', auth.ownership_ledger), *([('audit', str(audit))] if audit else [])]:
            if self.state_path(auth.authorization_id + ':' + role) != Path(path):
                raise AuthorityDenied('private state binding mismatch')

    @contextmanager
    def session(self):
        if current() is not None:
            raise AuthorityDenied('nested authority selection forbidden')
        self._verify_catalog()
        token = _current.set(self)
        try:
            yield self
        finally:
            _current.reset(token)

    def close(self):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None


def require_store(auth, audit=None):
    store = current()
    if store is None:
        raise AuthorityDenied('production requires a pinned private authority store')
    store.require(auth, audit)
    return store
