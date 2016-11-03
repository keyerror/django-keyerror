import sys
import contextlib

from .utils import WrappedException


@contextlib.contextmanager
def group_errors(ident):
    """
    with group_errors('some identifier'):
        if random.random > 0.5:
            1/0
        else:
            variable_does_not_exist
    """

    try:
        yield
    except Exception:
        raise WrappedException(ident, sys.exc_info())
