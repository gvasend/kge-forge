from contextlib import contextmanager
from contextvars import ContextVar
from functools import wraps
from .controller_authority_store import ControllerAuthorityStore, AuthorityDenied, encoded

def canonical(value):return encoded(value)

# Parsed catalog reuse, never an authorization verdict. Every borrow checks the
# pinned catalog and current placement. Every historical witness is reread below.
_history_stores = ContextVar('attempt_history_catalogs', default=None)

@contextmanager
def historical_store(configuration):
 pool = _history_stores.get()
 if pool is None:
  store = ControllerAuthorityStore(**configuration)
  try:yield store
  finally:store.close()
 else:
  key = canonical(configuration)
  if key not in pool:pool[key] = ControllerAuthorityStore(**configuration)
  store = pool[key]
  store._verify_catalog()
  yield store

@contextmanager
def history_scope():
 if _history_stores.get() is not None:
  yield
  return
 pool={};token=_history_stores.set(pool)
 try:yield
 finally:
  _history_stores.reset(token)
  for store in pool.values():store.close()

def reuse_history_catalogs(fn):
 @wraps(fn)
 def wrapped(*args, **kwargs):
  with history_scope():return fn(*args, **kwargs)
 return wrapped
