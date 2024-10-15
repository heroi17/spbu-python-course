import inspect
import copy
from typing import Any, Callable, Union
from logging import raiseExceptions
from functools import wraps


class Isolated:
    """
    ----------
    Discription
    ----------
    Special Argument type for smart_args.

    Cannot be used as argument in call.
    Every args wich by default = to Isolated()
    shuld be given in call.

    When user call func.
    Making deepcopy of all Isolated arguments in call.
    And enstead of getted walues we use it's copyes.

    ----------
    Example:
    ----------
    @smart_args
    test_func(d=Isolated())
        d["a"] = 1
        return d

    dict={"a":10}
    print(test_func(dict))
    print(dict)
    >>>
    {"a":1}
    {"a":10}
    """

    pass


class Evaluated:
    """
    ----------
    Discription
    ----------
    Special Argument type for smart_args.

    When user call user_func,
    All args that by defoults is Evaluated and not given in call,
    will be replaced to eval_func(),
    where eval_func is argument in Evaluated.
    Eval_func calls hepens exactly at call user_func, not when user_func was initialised.

    ----------
    Example:
    ----------
    import random

    def get_random_number():
       return random.randint(0,100)

    @smart_args
    def test_func(*, x=get_random_number(), y=Evaluated(get_random_number)):
       print(x, y)


    test_func()
    test_func()
    test_func(y=150)
    >>>
    15 36
    15 66
    15 150
    """

    def __init__(self, func: Callable[[], Any]) -> None:
        self._func = func
        if type(func) is Isolated:
            raise TypeError("You cannot use as argument Isolated into Evaluated.")
        if type(func) is Evaluated:
            raise TypeError("You cannot use as argument Evaluated into Evaluated.")
        if not callable(func):
            raise TypeError("You cannot use funk as param to Evaluated.")
        if len(inspect.getfullargspec(func).args) != 0:
            raise TypeError("You shuld use function without params.")

    def __call__(self) -> Any:
        return self._func()


def CheckForCorrectArgs(args: tuple[Any], kwargs: dict[str, Any]) -> None:
    """
    Special function for smart_args.
    Calls by smart_args when we should to check eather call user func with agrument like:
    type(arg) is Evaluated or type(arg) is Isolated
    """

    for el in args:
        if type(el) is Evaluated:
            raise TypeError(f"You cannot use Evaluated() when call the function.")
        if type(el) is Isolated:
            raise TypeError(f"You cannot use Isolated() when call the function.")
    for el in kwargs:
        if type(kwargs[el]) is Evaluated:
            raise TypeError(f"You cannot use Evaluated() when call the function.")
        if type(kwargs[el]) is Isolated:
            raise TypeError(f"You cannot use Isolated() when call the function.")


def fillDictByDefaults(
    dict_to_fill: dict[str, Any], dict_defoults: dict[str, Any]
) -> None:
    """
    Special function for smart_args.

    For el in dict_defoults
    put el into dict_to_fill if it is not there.


    Here heppend copying Esolated args
    And calculating defoult values for Evaluated arguments.
    """

    for i in dict_defoults:
        if type(dict_defoults[i]) is Isolated:
            if not i in dict_to_fill:
                raise ValueError(f"Have no expected value for Isolated parameter {i}.")
            else:
                dict_to_fill[i] = copy.deepcopy(dict_to_fill[i])
        else:
            if i not in dict_to_fill:  # then set there new walue
                if type(dict_defoults[i]) is Evaluated:
                    dict_to_fill[i] = dict_defoults[i]()
                else:
                    dict_to_fill[i] = dict_defoults[i]


def smart_args(
    func: Union[Callable[..., Any], None] = None, enable_positional: bool = True
) -> Callable[..., Any]:
    """
    Provide two new type of argument:
    Isolated - kopy value in call.
    Evaluated - calculate function and use it resoult as defoult argument every call.

    ----------
    Args
    ----------
    func: Callable
        Function that decorated by smart_args

    enable_positional: bool
        If True, positional arguments are supported. If False, only
        keyword arguments are allowed. Default is True

    ----------
    Returns
    ----------
    Callable
        Wrapped func.
        Should get Isolated args
        Every call when do not get Evaluated args. they generated uniqe for call.
    """

    if func is None:
        return lambda func: smart_args(func=func, enable_positional=enable_positional)

    data: inspect.FullArgSpec = inspect.getfullargspec(func)

    if not enable_positional and not data.defaults is None:
        for el in data.defaults:
            if type(el) is Isolated:
                raise TypeError(
                    "You use positional Isolated when enable_positional is False"
                )
            if type(el) is Evaluated:
                raise TypeError(
                    "You use positional Evaluated when enable_positional is False"
                )

    @wraps(func)
    def inner(*args, **kwargs) -> Union[Callable[..., Any], Any]:
        # Check for invalid using smart args functions
        CheckForCorrectArgs(args, kwargs)

        # Args for func to call.
        return_vargs: list[Any] = []
        return_varkw: dict[str, Any] = {}
        return_args: list[Any] = []
        return_kwonlyargs: dict[str, Any] = {}

        # Defoult args.
        default_args: dict[str, Any] = {}
        if not data.defaults is None:
            for i in range(len(data.defaults)):
                default_args[
                    data.args[i + len(data.args) - len(data.defaults)]
                ] = data.defaults[i]

        default_kwonlyargs: dict[str, Any] = {}
        if not data.kwonlydefaults is None:
            default_kwonlyargs = copy.copy(data.kwonlydefaults)

        return_args_dict: dict[str, Any] = {}

        # all args is used
        for i in range(len(args)):
            if i < len(data.args):
                return_args_dict[data.args[i]] = args[i]
            else:
                if data.varargs is None:
                    raise ValueError(
                        f"Too many args, {func.__name__}, cannot get {i} as unnamed becouse it's no space for it"
                    )
                return_vargs.append(args[i])

        # all kwargs is used
        for el in kwargs:
            if el in return_args_dict:
                raise ValueError(f"Arg {el} getted twice or more")
            if el in return_kwonlyargs:
                raise ValueError(f"Arg {el} getted twice or more")
            if el in data.args:
                return_args_dict[el] = kwargs[el]
            elif el in data.kwonlyargs:
                return_kwonlyargs[el] = kwargs[el]
            else:  # use it as named
                if data.varkw is None:
                    raise ValueError(
                        f"Too many args, {func.__name__}, cannot get {el} as named becouse it's no space for it"
                    )
                return_varkw[el] = kwargs[el]

        # use defoult values if it's need for args
        fillDictByDefaults(return_args_dict, default_args)

        # use defoult values if it's need for kwargs
        fillDictByDefaults(return_kwonlyargs, default_kwonlyargs)

        # check for existing values and fill return_args by return_args_dict
        for el in data.args:
            if not el in return_args_dict:
                raise ValueError(f"Do not get the unnamed arg: {el}.")
            return_args.append(return_args_dict[el])
        for el in data.kwonlyargs:
            if not el in return_kwonlyargs:
                raise ValueError(f"Do not get the named arg: {el}.")

        # Call function with expected arguments.
        return func(
            *(*return_args, *return_vargs), **{**return_kwonlyargs, **return_varkw}
        )

    return inner
