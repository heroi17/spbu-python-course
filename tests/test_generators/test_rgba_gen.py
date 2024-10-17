import pytest
from project.generators.rgba_gen import get_rgba_generator


def make_index_from_rgba(r: int, g: int, b: int, a: int):
    return int(a/2) + 51 * (b + 256 * (g + 256 * r))
@pytest.mark.parametrize(
    "rgba_vec",
    [
        (22, 33, 1, 0),
        (0, 255, 3, 100),
        (70, 0, 255, 50)
        (0, 0, 0, 0),
    ],
)
def test_get_nth_rgba_vec(
    rgba_vec: tuple[int, int, int, int]
) -> None:
    index: int = make_index_from_rgba(rgba_vec)
    assert get_rgba_generator(index) == rgba_vec



@pytest.mark.parametrize(
    "index", [-1, 256**3 * 51]
)
def test_invalid_index(index: int) -> None:
    with pytest.raises(IndexError):
        get_rgba_generator(index)