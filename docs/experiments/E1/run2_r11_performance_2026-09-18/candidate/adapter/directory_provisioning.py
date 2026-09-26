"""Exact controller-only pre-activation directory provisioning, no mkdir -p."""
import hashlib
import json
import os
from pathlib import Path

SOURCE = 'Architect PD-06 explicit-directory blocker-closure instruction, 2026-09-16'
SHAPES = [('src', 'package ancestor'), ('src/kge_forge', 'package initializer parent'),
          ('src/kge_forge/context', 'utility directory write grant'),
          ('tests', 'acceptance-test ancestor'), ('tests/context', 'test directory write grant'),
          ('docs', 'existing documentation ancestor'),
          ('docs/implementation', 'implementation report parent')]


def plan(root, context_sha256):
    root = Path(root)
    if not root.is_absolute() or str(root) != str(root.resolve()):
        raise ValueError('canonical root required')
    return {'schema': 1, 'root': str(root), 'context_sha256': context_sha256,
            'authority_source': SOURCE, 'state_required': 'INACTIVE',
            'directories': [{'path': str(root / rel), 'reason': reason,
                'authority_source': SOURCE + '; E1-WP-001 writable paths; committed context ' + context_sha256,
                'authorized_parent': str((root / rel).parent),
                'expected': 'existing' if rel == 'docs' else 'absent',
                'controller_provisioning_required': rel != 'docs'} for rel, reason in SHAPES]}


def open_directory(path):
    """Walk from / with O_NOFOLLOW at every component, never resolve a symlink."""
    path = Path(path)
    if not path.is_absolute() or '..' in path.parts or str(path) != os.path.normpath(str(path)):
        raise ValueError('noncanonical directory')
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for name in path.parts[1:]:
            child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd); fd = child
        return fd
    except BaseException:
        os.close(fd); raise


def provision(record, audit_path, state='INACTIVE'):
    root = Path(record['root']); audit = Path(audit_path)
    if not audit.is_absolute() or root == audit or root in audit.parents:
        raise ValueError('provisioning audit must be outside Programmer root')
    digest = hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()
    audit_fd = os.open(audit, os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    def log(event, **fields):
        data = (json.dumps({'event': event, 'plan_sha256': digest, **fields}) + '\n').encode()
        with os.fdopen(os.dup(audit_fd), 'ab', buffering=0) as stream:
            stream.write(data); os.fsync(stream.fileno())
    opened = {}
    created = []
    try:
        log('provisioning_preflight')
        if state != 'INACTIVE' or record != plan(record['root'], record['context_sha256']):
            raise ValueError('exact inactive provisioning plan required')
        opened[str(root)] = open_directory(root)
        known = {str(root)}
        for row in record['directories']:
            p = Path(row['path']); parent = row['authorized_parent']
            if parent not in known or p.parent != Path(parent) or root not in p.parents:
                raise ValueError('unlisted or unauthorized ancestor')
            known.add(str(p))
            # Full lexical preflight, including absent entries under absent parents.
            if row['expected'] == 'existing':
                opened[str(p)] = open_directory(p)
            elif os.path.lexists(str(p)):
                raise ValueError('expected absent directory exists or is wrong type')
        for row in record['directories']:
            if not row['controller_provisioning_required']:
                continue
            p = Path(row['path']); parent = row['authorized_parent']
            # Reject replaced ancestor names even though retained directory fds are safe.
            current = open_directory(parent)
            try:
                if os.fstat(current) != os.fstat(opened[parent]):
                    raise ValueError('ancestor state changed')
            finally:
                os.close(current)
            log('directory_create_intent', path=str(p), parent=parent)
            os.mkdir(p.name, mode=0o755, dir_fd=opened[parent])
            os.fsync(opened[parent])
            opened[str(p)] = os.open(p.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                    dir_fd=opened[parent])
            created.append(str(p))
            log('directory_created', path=str(p))
        for path, fd in opened.items():
            current = open_directory(path)
            try:
                a, b = os.fstat(current), os.fstat(fd)
                if (a.st_dev, a.st_ino) != (b.st_dev, b.st_ino):
                    raise ValueError('directory identity changed')
            finally: os.close(current)
        log('provisioning_complete', created=created)
        return {'result': 'PASS', 'plan_sha256': digest, 'created': created,
                'state': state, 'profile_activated': False}
    except BaseException:
        log('provisioning_failed', created=created)
        raise
    finally:
        for fd in opened.values(): os.close(fd)
        os.close(audit_fd)
