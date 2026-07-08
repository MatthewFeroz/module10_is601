"""
Unit tests for app.operations.

These tests exercise each arithmetic function in isolation (no web server,
no HTTP) using pytest parametrization to cover positive, negative, float,
and zero inputs, plus the division-by-zero error path.
"""

from typing import Union

import pytest

from app.operations import add, subtract, multiply, divide

Number = Union[int, float]


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5),
        (-2, -3, -5),
        (2.5, 3.5, 6.0),
        (-2.5, 3.5, 1.0),
        (0, 0, 0),
        (1e10, 1e10, 2e10),
    ],
    ids=[
        "two_positive_ints",
        "two_negative_ints",
        "two_positive_floats",
        "negative_and_positive_float",
        "zeros",
        "large_numbers",
    ],
)
def test_add(a: Number, b: Number, expected: Number) -> None:
    """add() returns the correct sum for ints, floats, negatives, and zero."""
    assert add(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 3, 2),
        (-5, -3, -2),
        (5.5, 2.5, 3.0),
        (-5.5, -2.5, -3.0),
        (0, 0, 0),
        (3, 5, -2),
    ],
    ids=[
        "two_positive_ints",
        "two_negative_ints",
        "two_positive_floats",
        "two_negative_floats",
        "zeros",
        "result_negative",
    ],
)
def test_subtract(a: Number, b: Number, expected: Number) -> None:
    """subtract() returns the correct difference across sign combinations."""
    assert subtract(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 6),
        (-2, 3, -6),
        (-2, -3, 6),
        (2.5, 4.0, 10.0),
        (0, 5, 0),
        (1, 0.5, 0.5),
    ],
    ids=[
        "two_positive_ints",
        "negative_times_positive",
        "two_negatives",
        "two_floats",
        "zero_times_positive",
        "fractional_multiplier",
    ],
)
def test_multiply(a: Number, b: Number, expected: Number) -> None:
    """multiply() returns the correct product across sign combinations."""
    assert multiply(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (6, 3, 2.0),
        (-6, 3, -2.0),
        (6.0, 3.0, 2.0),
        (-6.0, 3.0, -2.0),
        (0, 5, 0.0),
        (1, 4, 0.25),
    ],
    ids=[
        "two_positive_ints",
        "negative_dividend",
        "two_positive_floats",
        "negative_float_dividend",
        "zero_dividend",
        "fractional_result",
    ],
)
def test_divide(a: Number, b: Number, expected: float) -> None:
    """divide() returns the correct quotient across sign combinations."""
    assert divide(a, b) == expected


def test_divide_by_zero() -> None:
    """divide() raises ValueError with a clear message when dividing by zero."""
    with pytest.raises(ValueError) as excinfo:
        divide(6, 0)
    assert "Cannot divide by zero!" in str(excinfo.value)


def test_divide_by_zero_float() -> None:
    """divide() also rejects a float zero divisor (0.0 == 0)."""
    with pytest.raises(ValueError):
        divide(6, 0.0)
