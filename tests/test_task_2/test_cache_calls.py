from project.task_2.cache_calls import cache_calls
import pytest
from time import time

from typing import Callable, Any, Union, Type


def fib(
    n: int, *, doublestep: bool = False, recurcsive_call: Union[None, Callable[..., int]] = None
) -> int:
    if recurcsive_call is None:
        return 0
    if n < 0:
        raise ValueError("Cannot calculete negtive number of fibanacci.")
    if n == 0:
        return 0
    if doublestep:
        if n == 1:
            return 2

        return 2 * (
            recurcsive_call(
                n - 2, doublestep=doublestep, recurcsive_call=recurcsive_call
            )
            + recurcsive_call(
                n - 1, doublestep=doublestep, recurcsive_call=recurcsive_call
            )
        )
    if n == 1:
        return 1
    return recurcsive_call(
        n - 2, doublestep=doublestep, recurcsive_call=recurcsive_call
    ) + recurcsive_call(n - 1, doublestep=doublestep, recurcsive_call=recurcsive_call)


def steps_to(
    stair: int, *, extrasteps: int = 0, recurcsive_call: Union[None, Callable[..., int]] = None
) -> int:
    if recurcsive_call is None:
        return 0
    if stair == 1:
        return 1
    elif stair == 2:
        return 2
    elif stair == 3:
        return 4
    else:
        return (  # use recurcsive_call argument becouse we should reset recursive function when wrapp it.
            recurcsive_call(
                stair - 3, extrasteps=extrasteps, recurcsive_call=recurcsive_call
            )
            + recurcsive_call(
                stair - 2, extrasteps=extrasteps, recurcsive_call=recurcsive_call
            )
            + recurcsive_call(
                stair - 1, extrasteps=extrasteps, recurcsive_call=recurcsive_call
            )
        ) + extrasteps  # if we will use @smart_args under the function declaration, we'll not need recurcsive_call(it's only for test)


@pytest.mark.parametrize(
    "func, capacity, args, kwds, faster_times",
    [
        (fib, 0, (4,), {}, None),  # test for correct working without cache
        (steps_to, 0, (14,), {}, None),
        (steps_to, 3, (6,), {}, None),  # test for little numbers
        (steps_to, 5, (10,), {"extrasteps": 4}, None),  # some tests with cache
        (steps_to, 5, (15,), {"extrasteps": 2}, None),
        (
            fib,
            100,
            (22,),
            {"doublestep": False},
            2,
        ),  # some tests with accelerating by caching
        (fib, 2, (25,), {}, 3),
        (steps_to, 5, (25,), {"extrasteps": 2}, 10),
    ],
)
def test_correct_cache_calls_and_speed_test_for_recursive(
    func: Callable[..., Any],
    capacity: int,
    args: tuple[Any],
    kwds: dict[str, Any],
    faster_times: Union[float, None],
) -> None:

    # do it becouse recurent func should call decorated function, not origin, so we need to create funk with that name  into local scope
    time_start_simple = time()
    answer = func(*args, recurcsive_call=func, **kwds)
    delta_time_simple = time() - time_start_simple

    cached_function = cache_calls(func, capacity=capacity)

    time_start_cached = time()
    answer_cached = cached_function(*args, recurcsive_call=cached_function, **kwds)
    delta_time_cached = time() - time_start_cached

    assert answer == answer_cached

    if not faster_times is None:
        assert delta_time_simple > delta_time_cached * faster_times


def test_correct_internal_caching() -> None:

    # we try to cache function wich cannot be cached in usuall aplication(becouse for the same calls it returns different answers)
    # But we will se that caching work good.
    counter: int = 0

    @cache_calls(capacity=3)
    def help_func(value: int) -> int:
        nonlocal counter
        counter += 1
        return counter * 1000 + value

    v1_1: int = help_func(1)
    v1_2: int = help_func(1)  # if it is cached then return the same result.

    assert v1_1 == v1_2

    v2_1: int = help_func(2)
    v3_1: int = help_func(3)  # cache is shuld be full now
    v1_3: int = help_func(
        1
    )  # it should be equal to v1_1 (becouse v1_1 in cache before this call)

    assert v1_3 == v1_1

    v4_1: int = help_func(4)  # cache is full so we need to remove oldest elem: v2_1

    v2_2: int = help_func(
        2
    )  # it should be not equal to v2_1 (becouse v2_1 not in cache after call help_func(4))

    assert v2_2 != v2_1

    # if it's all passed then it's work good:
    #    Make element newest if it already in cache.
    #    Delete oldest in use elements(when count == maxcount)


@pytest.mark.parametrize(
    "func, capacity, args, kwds",
    [  # cache do nothing special, we just see that these functions are working.
        (
            sum,
            3,
            (
                (
                    1,
                    2,
                    3,
                ),
            ),
            {},
        ),
        (
            len,
            3,
            (
                (
                    1,
                    2,
                    3,
                ),
            ),
            {},
        ),
        (
            any,
            3,
            (
                (
                    1,
                    0,
                ),
            ),
            {},
        ),
        (
            any,
            3,
            (
                (
                    0,
                    0,
                ),
            ),
            {},
        ),
    ],
)
def test_cache_for_Pythons_functions(
    func: Callable[..., Any], capacity: int, args: dict[Any], kwds: dict[str, Any]
) -> None:
    assert func(*args, **kwds) == cache_calls(func, capacity=capacity)(*args, **kwds)
