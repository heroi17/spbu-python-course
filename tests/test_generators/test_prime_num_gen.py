import pytest

from project.generators.get_from_generator import get_elem_from_gen
from project.generators.prime_num_gen import prime_number_generator


@pytest.mark.parametrize(
    "index, expected_prime",
    [(1, 2), (2, 3), (3, 5), (281, 1823), (921, 7211), (1000, 7919)],
)
def test_prime_gen_non_decorated(index: int, expected_prime: int) -> None:
    for i, prime in enumerate(prime_number_generator(), start=1):
        if i == index:
            assert prime == expected_prime
            break


@pytest.mark.parametrize(
    "index, expected_prime_sequence",
    [
        (1, [2, 3, 5, 7]),
        (3, [5]),
        (281, [1823, 1831, 1847, 1861, 1867, 1871, 1873]),
        (921, [7211]),
        (1000, [7919]),
    ],
)
def test_prime_gen_decorated(index: int, expected_prime_sequence: list[int]) -> None:
    decorated_gen = get_elem_from_gen(prime_number_generator)
    for el in expected_prime_sequence:
        assert el == decorated_gen(index)
        index += 1


@pytest.mark.parametrize("index", [-1, 0])
def test_invalid_index(index: int) -> None:
    with pytest.raises(IndexError):
        get_elem_from_gen(prime_number_generator)(index)
