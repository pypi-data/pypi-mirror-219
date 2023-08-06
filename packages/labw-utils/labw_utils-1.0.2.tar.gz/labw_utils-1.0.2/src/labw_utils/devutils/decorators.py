"""
labw_utils.devutils.decorators -- Decorators for miscellaneous features.
"""

__all__ = (
    "copy_doc",
    "chronolog",
    "create_class_init_doc_from_property",
    "supress_inherited_doc"
)

import inspect
import logging
import os
import types
import uuid

from labw_utils.stdlib.cpy310.pkgutil import resolve_name
from labw_utils.typing_importer import Any, TypeVar, Callable

_InType = TypeVar("_InType")


def copy_doc(source: Any) -> Callable:
    """
    The following piece of code is from
    https://stackoverflow.com/questions/68901049/copying-the-docstring-of-function-onto-another-function-by-name
    by Iced Chai at Aug 24, 2021 at 2:56

    This wrapper copies docstring from one function to another.

    Use Example: copy_doc(self.copy_func)(self.func) or used as deco

    >>> class Test:
    ...     def foo(self) -> None:
    ...         \"\"\"Woa\"\"\"
    ...         ...
    ...
    ...     @copy_doc(foo)
    ...     def this(self) -> None:
    ...         pass
    >>> Test.this.__doc__
    'Woa'

    This function should be used on so-called "proxy" classes. For example,

    >>> class A:
    ...     def foo(self) -> None:
    ...         \"\"\"Woa\"\"\"
    ...         ...
    ...
    >>> class AProxy:
    ...     _A: A
    ...     @copy_doc(A.foo)
    ...     def foo(self) -> None:
    ...         self._A.foo()
    >>> AProxy.foo.__doc__
    'Woa'
    """
    if isinstance(source, str):
        source = resolve_name(source)

    def wrapper(func: Any) -> Callable:
        func.__doc__ = source.__doc__
        return func

    return wrapper


def supress_inherited_doc(obj):
    if os.getenv("SPHINX_BUILD") is not None:
        mro_defined = {"__init__"}
        for mro in obj.__mro__:
            for mro_attr in dir(mro):
                if not mro_attr.startswith("_"):
                    mro_defined.add(mro_attr)
        for inside_obj_name in dir(obj):
            if inside_obj_name in mro_defined:
                try:
                    delattr(obj, inside_obj_name)
                except (AttributeError, TypeError):
                    pass
    return obj


def chronolog(display_time: bool = False, log_error: bool = False):
    """
    The logging decorator, will inject a logger variable named _lh to the code.
    From <https://stackoverflow.com/questions/17862185/how-to-inject-variable-into-scope-with-a-decorator>

    .. note::
        The :py:func:`error` (or :py:func:`exception`, :py:func:`critical`, :py:func:`fatal`
        functions DO NOT exit the program! You have to exit the program by yourself!

    .. warning::
        Call this function, do NOT call functions inside this function!

    :param display_time: Whether to display calling time, arguments and return value in log level.
    :param log_error: Whether add error captured
    """

    def msg_decorator(f: types.FunctionType) -> Callable:
        if os.environ.get('SPHINX_BUILD') is not None:
            return f  # To make Sphinx get the right result.

        def inner_dec(*args, **kwargs):
            """
            Decorator which performs the logging and do the work.

            :param args: Unnamed arguments of the decorated function call.
            :param kwargs: Named arguments of the decorated function call.
            :return: The return value of the decorated function call.
            :raise: The return value of the decorated function call.
            """
            call_id = f"CHRONOLOG CID={uuid.uuid4()}"
            try:
                _ = f.__globals__
            except AttributeError:
                return f(*args, **kwargs)
            lh = logging.getLogger(f.__module__)
            if display_time:
                args_repr = [repr(a) for a in args]
                kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
                signature = ", ".join(args_repr + kwargs_repr)
                lh.debug("%s %s(%s)", call_id, f.__name__, signature)
            res = None
            try:
                res = f(*args, **kwargs)
            except Exception as e:
                if log_error:
                    lh.exception("%s exception inside func: %s", call_id, str(e), stack_info=True, exc_info=True)
                raise e
            finally:
                lh.debug("%s returns %s", f.__name__, repr(res))
            return res

        return inner_dec

    return msg_decorator


def create_class_init_doc_from_property(
        text_before: str = "",
        text_after: str = "",
):
    """
    Place documentations at attributes to ``__init__`` function of a class.

    :param text_before: Text placed before parameters.
    :param text_after: Text placed after parameters.

    Example:

    >>> @create_class_init_doc_from_property()
    ... class TestInitDoc:
    ...     _a: int
    ...     _b: int
    ...     def __init__(self, a: int, b: int):
    ...         ...
    ...
    ...     @property
    ...     def a(self) -> int:
    ...         \"\"\"Some A value\"\"\"
    ...         return self._a
    ...
    ...     @property
    ...     def b(self) -> int:
    ...         \"\"\"Some B value\"\"\"
    ...         return self._b
    >>> print(TestInitDoc.__init__.__doc__)
    :param a: Some A value
    :param b: Some B value
    <BLANKLINE>

    Note that this example would NOT work:

    >>> @create_class_init_doc_from_property()
    ... class TestInitDoc:
    ...     a: int
    ...     \"\"\"Some A value\"\"\"
    ...
    ...     b: int
    ...     \"\"\"Some B value\"\"\"
    ...
    ...     def __init__(self, a: int, b: int):
    ...         ...
    >>> print(TestInitDoc.__init__.__doc__)
    <BLANKLINE>
    """

    def inner_dec(cls: _InType) -> _InType:
        init_func = cls.__init__
        mro = list(cls.__mro__)
        sig = inspect.signature(init_func)
        result_doc = ""
        for argname in sig.parameters.keys():
            curr_mro = list(mro)
            while curr_mro:
                curr_class = curr_mro.pop(0)
                try:
                    doc = getattr(curr_class, argname).__doc__
                except AttributeError:
                    continue
                if doc is None:
                    continue
                result_doc += f":param {argname}: {doc}\n"
                break

        init_func.__doc__ = text_before + result_doc + text_after
        return cls

    return inner_dec
