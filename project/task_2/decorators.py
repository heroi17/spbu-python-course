from inspect import unwrap
from functools import wraps
from optparse import BadOptionError
from inspect import getfullargspec
from typing import Callable, Any, Union


def curry_explicit(function: Callable[..., Any], arity: int) -> Callable[..., Any]:
    """
    Make from function sequence of them.
    To get result you can call func(arg1)(arg2)....(argn) where n = arity.

    ----------
    Params:
    ----------
    function: Callable
        Function wich should be separated.

    arity: int
        Count of function params.

    ----------
    Returns:
    ----------
    Callable[[Any], Callable[[Any], Any]]
        Secuence of function that returns next function, last one return result.
    """
    if arity < 0:
        raise ValueError("Arity can not be positive")

    if arity == 0:
        return function

    args: list[Any] = []

    @wraps(function)
    def inner(arg: Any) -> Union[Callable[..., Any], Any]:
        nonlocal arity
        nonlocal args
        args.append(arg)
        arity -= 1
        if arity == 0:
            if not getfullargspec(function).varargs is None:
                return None
            return function(*args)
        else:
            return inner

    setattr(inner, "__decorated_by_curry_explicit", function)
    setattr(inner, "__arity_glob", arity)

    return inner


def uncurry_explicit(function: Callable[..., Any], arity: int) -> Callable[..., Any]:
    """
    Decompose curried function, get function only getted by curry_explicit.
    You can call now function as normal on: funk(arg1, arg2, ..., argn) where n = arity.

    ----------
    Params:
    ----------
    function: Callable
        Chenged by curry_explicit Origin function.

    arity: int
        Count of function params.

    ----------
    Returns:
    ----------
    Callable[[Any], Callable[[Any], Any]]
        Origin function, wich given to curry_explicit.
    """
    if arity < 0:
        raise ValueError("Arity can not be positive")

    if arity == 0:
        return function

    if hasattr(function, "__decorated_by_curry_explicit"):
        if getattr(function, "__arity_glob") == arity:
            return getattr(function, "__decorated_by_curry_explicit")  # type: ignore
        else:
            raise ValueError(
                f'Expected arity is {getattr(function, "__arity_glob")}, but given arity is {arity}'
            )
    else:
        raise ValueError("This function doesn't wrapped by curry_explicit")
