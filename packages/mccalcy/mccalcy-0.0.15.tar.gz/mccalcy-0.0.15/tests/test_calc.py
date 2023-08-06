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


def test_root() -> None:
    """
    Test the nth_root() method.
    """
    calc = mccalcy.Calculator()
    calc.add(16)
    calc.root(2)
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
    with pytest.raises(TypeError) as exc_info:
        calc.add("hello")
    assert str(exc_info.value) == "hello is not a number"


def test_subtract_str() -> None:
    """
    Test the subtract() method with a string argument.
    """
    calc = mccalcy.Calculator()
    with pytest.raises(TypeError) as exc_info:
        calc.subtract("hello")
    assert str(exc_info.value) == "hello is not a number"


def test_multiply_str() -> None:
    """
    Test the multiply() method with a string argument.
    """
    calc = mccalcy.Calculator()
    with pytest.raises(TypeError) as exc_info:
        calc.multiply("hello")
    assert str(exc_info.value) == "hello is not a number"


def test_divide_str() -> None:
    """
    Test the divide() method with a string argument.
    """
    calc = mccalcy.Calculator()
    with pytest.raises(TypeError) as exc_info:
        calc.divide("hello")
    assert str(exc_info.value) == "Can't divide by hello"


def test_root_str() -> None:
    """
    Test the root() method with a string argument.
    """
    calc = mccalcy.Calculator()
    with pytest.raises(TypeError) as exc_info:
        calc.root("hello")
    assert str(exc_info.value) == "'hello' is not a number"


def test_root_valid_value() -> None:
    """
    Test the root() method with a valid value.
    """
    calc = mccalcy.Calculator()
    calc.add(16)
    calc.root(2)
    assert calc.memory == 4


def test_root_invalid_value() -> None:
    """
    Test the root() method with an invalid value.
    """
    calc = mccalcy.Calculator()
    calc.add(16)
    with pytest.raises(ValueError) as exc_info:
        calc.root(0)
    assert (
        str(exc_info.value)
        == "Root value must be greater than or equal to 1"
    )


def test_root_non_numeric_value() -> None:
    """
    Test the root() method with a non-numeric value.
    """
    calc = mccalcy.Calculator()
    with pytest.raises(TypeError) as exc_info:
        calc.root("hello")
    assert str(exc_info.value) == "'hello' is not a number"


if __name__ == "__main__":
    pytest.main()
