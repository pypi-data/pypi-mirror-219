"""
Code for dropping stack frames from stack traces.
"""
from contextlib import contextmanager
from typing import ContextManager, Iterator

_enabled = True


def set_enable_drop_stack_frame(enabled: bool) -> ContextManager[None]:
    """Sets whether `drop_stack_frame` is enabled or not.

    If `set_enable_drop_stack_frame(False)` then `drop_stack_frame()` has no effect.  This can be
    used for debugging. Write code with `drop_stack_frame()`, and if something goes wrong (or just
    in all unit tests...) call `set_enable_drop_stack_frame(False)` to get more information in your
    stack frames.

    This function can either be called alone::

        set_enable_drop_stack_frame(False)
        ...

    Or used as a context manager::

        with set_enable_drop_stack_frame(False):
            ...

    If used as a context manager then the previous state of enabledness is restored when the context
    is left.
    """

    global _enabled
    old_enabled = _enabled
    _enabled = enabled

    @contextmanager
    def _context_manager() -> Iterator[None]:
        global _enabled
        try:
            yield
        finally:
            _enabled = old_enabled

    return _context_manager()


def get_enable_drop_stack_frame() -> bool:
    """Gets whether `drop_stack_frame` is enabled or not.

    If `get_enable_drop_stack_frame()` returns `False` then `drop_stack_frame` has no effect.
    """
    return _enabled


DROP_STACK_FRAME_SUPPORTED = False
"""
Whether the current set-up supports dropping stack frames.

If this is `False` the function `drop_stack_frame()` has no effect.
"""


def drop_stack_frame() -> None:
    """
    Drop the top-most stack frame from the current exception.

    Useful for hiding functions from tracebacks.

    Example::
        def f() -> None:
            try:
                ...
            except Exception:
                drop_stack_frame()
                raise
    """


try:
    # pylint: disable=function-redefined

    import sys

    import _testcapi

    DROP_STACK_FRAME_SUPPORTED = True

    def drop_stack_frame() -> None:
        # https://stackoverflow.com/questions/72146438/remove-decorator-from-stack-trace

        if not get_enable_drop_stack_frame():
            return

        tp, exc, tb = sys.exc_info()

        if exc is None:
            return

        etb = exc.__traceback__
        if etb is not None:
            exc.__traceback__ = etb.tb_next

        if tb is not None:
            _testcapi.set_exc_info(tp, exc, tb.tb_next)

except ImportError:
    pass
