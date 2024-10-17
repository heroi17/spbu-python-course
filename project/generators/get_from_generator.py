from typing import Generator, Any, Callable


def get_elem_from_gen(
    gen_func: Callable[[], Generator[Any, None, None]]
) -> Callable[[int], Any]:
    """
    ------
    Explonations:
    ------
    return inner wich returns the elem in Generator under index given to inner.
    Indexing starts with 1.


    ------
    Args:
    ------
    gen_func: Generator[Any, None, None]

    ------
    Returns:
    ------
    Callable[[int], Any]
        Function-wich give us the elem under position n in gen_func()
        position starts withs 1.
    """
    gen = gen_func()
    index = 0

    def inner(n: int) -> Any:
        nonlocal index

        if n < index + 1:
            raise IndexError(f"Index can not be negative: {index}")

        result = None
        while index != n:
            result = next(gen, None)

            if result is None:
                raise IndexError(f"There no elem with too big index: {index}")

            index += 1

        return result

    return inner
