from typing import Generator, Any, Callable

def get_elem_from_gen(gen: Generator[Any, None, None]) -> Callable[[int], Any]:
    def inner(index: int):
        nonlocal gen
        i = 0
        if index < 0:
            raise IndexError(f"Index can not be negative: {index}")
        for vec in gen():
            if i == index:
                return vec
            i+=1
        raise IndexError(f"There no elem with too big index: {index}")
    
    return inner