"""Tests for simple calculator."""

import pytest
from simple_calc import add, subtract, multiply, divide, is_positive, max_of_two


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5


def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6


def test_divide():
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3


def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(5, 0)


def test_is_positive():
    assert is_positive(5) is True
    assert is_positive(-5) is False
    assert is_positive(0) is False


def test_max_of_two():
    assert max_of_two(5, 3) == 5
    assert max_of_two(1, 10) == 10
    assert max_of_two(7, 7) == 7
