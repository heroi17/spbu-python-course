import pytest
from project.task_2.decorators import curry_explicit, uncurry_explicit
from typing import Any


def test_curry_errors() -> None:
    def help_func(*args: Any) -> int:
        return sum(args)

    with pytest.raises(TypeError):
        curry_explicit(help_func, 3)(1)(2)(3)(4)

    with pytest.raises(ValueError):
        curry_explicit(help_func, -1)


def test_none_return() -> None:
    def help_func(*args: Any) -> int:
        return sum(args)

    assert curry_explicit(help_func, 3)(1)(2)(3) is None


def test_curry_correct_argument_providing() -> None:
    curryed_func = curry_explicit(
        (
            lambda a, b, c, d: (
                a,
                b,
                c,
                d,
            )
        ),
        4,
    )
    assert (1, 2, 3, 4,) == curryed_func(1)(2)(
        3
    )(4)

    uncurryed_func = uncurry_explicit(curryed_func, 4)
    assert uncurryed_func(5, 6, 7, 8) == (5, 6, 7, 8)


def test_correct_uncurry_working() -> None:
    def func(a: int, b: int, c: int) -> int:
        return a + b + c

    with pytest.raises(ValueError):
        uncurry_explicit(curry_explicit(func, 3), 4)  # dif arity

    with pytest.raises(ValueError):
        uncurry_explicit(
            lambda x: x, 1
        )  # given function wich is no wrapped by curry_explicit


def test_curry_for_build_in_functions() -> None:
    # We got the same function as we put in.
    assert uncurry_explicit(curry_explicit(len, 3), 3) is len
    assert uncurry_explicit(curry_explicit(sum, 2), 2) is sum
    assert uncurry_explicit(curry_explicit(print, 3), 3) is print

    # ttest with zero curry
    assert curry_explicit(max, 0) is max

    assert curry_explicit(len, 1)([1, 2, 3]) == 3
    assert curry_explicit(sum, 1)([1, 2, 3]) == 6

    # actually it's enough None becouse print returns NoneType
    # but we test it becouse we can find errors
    assert curry_explicit(print, 2)(1)(2) is None
