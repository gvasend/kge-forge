"""Explicit same-thread append capability for an already locked audit.

Only the lifecycle transaction installs this capability after acquiring flock.
It does not acquire locks or grant lifecycle authority. No cross-thread reuse,
recursive transactions, lock substitution, or broadly reentrant lock exists.
"""
from contextvars import ContextVar
import os
import threading

_held = ContextVar('held_lifecycle_audit', default=None)

def enter(path, fd):
    if _held.get() is not None:
        raise RuntimeError('nested lifecycle audit transaction forbidden')
    st = os.fstat(fd)
    observed = os.stat(path, follow_symlinks=False)
    if (st.st_dev, st.st_ino) != (observed.st_dev, observed.st_ino):
        raise RuntimeError('audit descriptor identity mismatch')
    return _held.set((str(path), fd, st.st_dev, st.st_ino, os.getpid(), threading.get_ident()))

def leave(token):
    _held.reset(token)

def descriptor(path):
    held = _held.get()
    if held is None or held[0] != str(path):
        return None
    name, fd, dev, ino, pid, thread = held
    st = os.fstat(fd)
    actual = os.stat(path, follow_symlinks=False)
    if (pid, thread) != (os.getpid(), threading.get_ident()) or \
            (st.st_dev, st.st_ino) != (dev, ino) or \
            (actual.st_dev, actual.st_ino) != (dev, ino):
        raise RuntimeError('audit append capability invalid')
    return fd
