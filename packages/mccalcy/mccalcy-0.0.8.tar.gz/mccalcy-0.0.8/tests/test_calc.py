import pytest
from mccalcy import mccalcy


def test_add() -> None:
    """
    Test the add() method.
    """
    calc = mccalcy.Calculator()
    calc.add(10)
    assert calc.memory == 10


def test_subtract() -> None:
    """
    Test the subtract() method.
    """
    calc = mccalcy.Calculator()
    calc.add(10)
    calc.subtract(5)
    assert calc.memory == 5


def test_multiply() -> None:
    """
    Test the multiply() method.
    """
    calc = mccalcy.Calculator()
    calc.add(10)
    calc.multiply(2)
    assert calc.memory == 20


def test_divide() -> None:
    """
    Test the divide() method.
    """
    calc = mccalcy.Calculator()
    calc.add(10)
    calc.divide(2)
    assert calc.memory == 5


def test_nth_root() -> None:
    """
    Test the root() method.
    """
    calc = mccalcy.Calculator()
    calc.add(16)
    calc.nth_root(2)
    assert calc.memory == 4


def test_reset_memory() -> None:
    """
    Test the reset_memory() method.
    """
    calc = mccalcy.Calculator()
    calc.add(10)
    calc.reset_memory()
    assert calc.memory == 0


def test_add_str() -> None:
    """
    Test the add() method with a string argument.
    """
    calc = mccalcy.Calculator()
    with pytest.raises(TypeError):
        calc.add("hello")


def test_subtract_str() -> None:
    """
    Test the subtract() method with a string argument.
    """
    calc = mccalcy.Calculator()
    with pytest.raises(TypeError):
        calc.subtract("hello")


def test_multiply_str() -> None:
    """
    Test the multiply() method with a string argument.
    """
    calc = mccalcy.Calculator()
    with pytest.raises(TypeError):
        calc.multiply("hello")


def test_divide_str() -> None:
    """
    Test the divide() method with a string argument.
    """
    calc = mccalcy.Calculator()
    with pytest.raises(TypeError):
        calc.divide("hello")


def test_nth_root_str() -> None:
    """
    Test the root() method with a string argument.
    """
    calc = mccalcy.Calculator()
    with pytest.raises(TypeError):
        calc.nth_root("hello")


if __name__ == "__main__":
    pytest.main()
