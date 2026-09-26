"""Optional durable timing sink; observations never select authority."""
from contextvars import ContextVar
from contextlib import contextmanager
from functools import wraps
_sink=ContextVar('validation_span_sink',default=None)

@contextmanager
def recording(control):
    token=_sink.set(control)
    try:yield
    finally:_sink.reset(token)

@contextmanager
def span(name):
    control=_sink.get()
    if control is None:
        yield
    else:
        with control.span(name):yield

def measured(name):
    def decorate(fn):
        @wraps(fn)
        def wrapped(*args,**kwargs):
            with span(name):return fn(*args,**kwargs)
        return wrapped
    return decorate


def reconciliation_only(fn):
    """Remove admission-gating observers only inside typed recovery/cancellation.

    This does not change admission, budgets, authority, or transaction checks.
    The function's own authoritative durable lifecycle evidence remains required.
    """
    @wraps(fn)
    def wrapped(*args, **kwargs):
        with recording(None):
            return fn(*args, **kwargs)
    return wrapped
