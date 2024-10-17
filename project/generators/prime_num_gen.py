import math
from typing import Generator


def prime_number_generator() -> Generator[int, None, None]:
    """
    ------
    Explonations:
    ------
    Return Generator.

    ------
    Returns:
    ------
    Generator[int, None, None]:
        Generator wich give us prime numbers.


    """
    count = 2
    # maybe not the fastest solution, we can use memory to make it faster.
    while True:
        isprime = True

        for x in range(2, int(math.sqrt(count) + 1)):
            if count % x == 0:
                isprime = False
                break

        if isprime:
            yield count

        count += 1


for i in prime_number_generator():
    print(i)
    if i > 10:
        break
