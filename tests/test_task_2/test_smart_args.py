from project.task_2.smart_args import smart_args, Evaluated, Isolated
import pytest
from typing import Callable, Any, Union, Type
from random import randint


def get_random_number() -> int:
    return randint(0, 100)


def help_func_1(
    a1: Any,
    a2: Any = 2,
    a3: Any = 3,
    *args: tuple[Any],
    n1: Any,
    n2: Any = 12,
    n3: Any = 13,
    **kwargs: dict[str, Any]
) -> list[Any]:
    return [a1, a2, a3, args, n1, n2, n3, kwargs]


def test_invalid_using() -> None:

    # Have no test for invalid using Isolated: (Isolated(Evaluated()),
    # becouse Isolated cannot get any arguments.

    # Using Evaluated in call.
    with pytest.raises(TypeError):

        @smart_args
        def func1(*, a: Union[Evaluated, int] = Evaluated(get_random_number)) -> None:
            pass

        func1(a=Evaluated(get_random_number))

    # Using Isolated in call.
    with pytest.raises(TypeError):

        @smart_args
        def func1(*, a: Union[Evaluated, int] = Evaluated(get_random_number)) -> None:
            pass

        func1(a=Isolated())

    # Using Isolated in call.
    with pytest.raises(TypeError):

        @smart_args
        def func1(*, a: Union[Evaluated, int] = Evaluated(get_random_number)) -> None:
            pass

        func1(a=Isolated())

    # Do not give value for Isolated param.
    with pytest.raises(ValueError):

        @smart_args
        def func1(*, a: Union[Isolated, Any] = Isolated()) -> None:
            pass

        func1()

    # Evaluated connot get as param func with param.
    with pytest.raises(TypeError):

        #It is test so we ignore type checker(we give func wich have param - it's error)
        @smart_args
        def func1(*, a: Union[Evaluated, Any] = Evaluated(lambda x: x)) -> None:  # type: ignore
            pass

        func1()

    # Using positional when flag enable_positional is False
    with pytest.raises(TypeError):

        @smart_args(enable_positional=False)
        def func1(a: Union[Evaluated, int] = Evaluated(get_random_number)) -> None:
            pass

        func1()


@pytest.mark.parametrize(
    "func, args, kwargs, expected_data, enable_positional",
    [
        (
            help_func_1,
            (1,),
            {"n1": 11},
            [
                1,
                2,
                3,
                (),
                11,
                12,
                13,
                {},
            ],
            True,
        ),
        (
            help_func_1,
            (
                1,
                22,
            ),
            {"n1": 11, "HELLO": None},
            [1, 22, 3, (), 11, 12, 13, {"HELLO": None}],
            True,
        ),
        (
            help_func_1,
            (
                11,
                22,
                33,
                44,
                55,
            ),
            {"n1": 11},
            [11, 22, 33, (44, 55), 11, 12, 13, {}],
            True,
        ),
    ],
)
def test_correct_argument_providing(
    func: Callable[..., Any],
    args: tuple[Any],
    kwargs: dict[str, Any],
    expected_data: list[Any],
    enable_positional: bool,
) -> None:
    new_func = smart_args(func, enable_positional=enable_positional)
    assert new_func(*args, **kwargs) == expected_data


def test_Isolated_argument() -> None:
    # test with positional
    # test with dict
    @smart_args
    def check_isolation_1(d: Union[dict[Any, Any], Isolated] = Isolated()) -> dict[Any, Any]:
        assert type(d) is dict
        if type(d) is dict:
            d["a"] = 0
            return d
        return {"a": 1000}

    no_mutable_1: dict[Any, Any] = {"a": 10}
    assert check_isolation_1(no_mutable_1)["a"] == 0 and no_mutable_1["a"] == 10

    # tset with list
    @smart_args
    def check_isolation_2(d: Union[list[Any], Isolated] = Isolated()) -> list[Any]:
        assert type(d) is list
        if type(d) is list:
            d.append(0)
            return d
        return []

    list_for_test_1: list[Any] = [10]
    assert check_isolation_2(list_for_test_1) == [10, 0] and list_for_test_1 == [10]

    # test with named
    # test with dict
    @smart_args
    def check_isolation_3(*, d: Union[dict[Any, Any], Isolated] = Isolated()) -> dict[Any, Any]:
        assert type(d) is dict
        if type(d) is dict:
            d["a"] = 0
            return d
        return {"a": 1000}

    no_mutable_2: dict[Any, Any] = {"a": 10}
    assert check_isolation_3(d=no_mutable_2)["a"] == 0 and no_mutable_2["a"] == 10

    # tset with list
    @smart_args
    def check_isolation_4(*, d: Union[list[Any], Isolated] = Isolated()) -> list[Any]:
        assert type(d) is list
        if type(d) is list:
            d.append(0)
            return d
        return []

    list_for_test_2: list[Any] = [10]
    assert check_isolation_4(d=list_for_test_2) == [10, 0] and list_for_test_2 == [10]


def test_Evaluated_argument() -> None:

    # test with function wich returns different values.
    # test with positional
    id_counter: int = 0

    def get_new_id() -> int:
        nonlocal id_counter
        id_counter += 1
        return id_counter

    @smart_args
    def check_Evaluated_1(d: Union[int, Evaluated] = Evaluated(get_new_id)) -> int:
        assert type(d) is int
        if type(d) is int:
            return d
        return 10000

    # if call check_Evaluated_1 will generate arg d then answers will be different.
    assert check_Evaluated_1() != check_Evaluated_1()

    # test with named
    @smart_args
    def check_Evaluated_2(*, d: Union[int, Evaluated] = Evaluated(get_new_id)) -> int:
        assert type(d) is int
        if type(d) is int:
            return d
        return 10000

    # if call check_Evaluated_1 will generate arg d then answers will be different.
    assert check_Evaluated_2() != check_Evaluated_2()
