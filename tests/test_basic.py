import pytest
import project  # on import will print something from __init__ file


def setup_module(module) -> None:
    print("basic setup module")


def teardown_module(module) -> None:
    print("basic teardown module")


def test_1() -> None:
    assert 1 + 1 == 2


def test_2() -> None:
    assert "1" + "1" == "11"
