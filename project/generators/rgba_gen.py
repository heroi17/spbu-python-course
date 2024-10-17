from typing import Generator

def get_rgba_generator() -> Generator[tuple[int, int, int, int], None, None]:
    """
    -------
    Explonation
    -------
    #
    #
    # TODO: add here some explonation + order how it returns values
    #
    #
    
    The output is in the format (R, G, B, A), where:
    - R: Red component (0-255)
    - G: Green component (0-255)
    - B: Blue component (0-255)
    - A: Alpha transparency component (0, 2, 4, ..., 100)

    -------
    Yields:
    -------
    tuple[int, int, int, int]
        A tuple representing an RGBA color (R, G, B, A).
    
    -------
    Example:
    -------
    >>> gen = get_rgba_gen()
    >>> next(gen)
    (0, 0, 0, 0)
    >>> next(gen)
    (0, 0, 0, 2)
    >>> next(gen)
    (0, 0, 0, 4)
    ...
    >>> next(gen)
    (0, 0, 255, 100)
    >>> next(gen)
    (0, 1, 0, 0)
    """
    return (
        (r, g, b, a)
        for r in range(256)
        for g in range(256)
        for b in range(256)
        for a in range(0, 101, 2)
        )


def get_rgba_vec(index: int) -> tuple[int, int, int, int]:
    """
    
    """
    if index < 0:
        raise IndexError(f"Index of Rgba_vec can not be negative: {index}")
    
    if index >= 256**3 * 51:
        raise IndexError(f"Sorry, but there no rgba_vec with too big index such as yurs: {index}")
    i = 0
    for vec in get_rgba_generator():
        if i == index:
            return vec
        i+=1