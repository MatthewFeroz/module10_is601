"""
Module: app.operations

Basic arithmetic functions (add, subtract, multiply, divide) used by the
FastAPI calculator. Each function accepts ints or floats and is covered by
unit tests in tests/unit/test_operations.py.
"""

import logging
from typing import Union

logger = logging.getLogger(__name__)

# Type alias: any number the calculator accepts can be an int or a float.
Number = Union[int, float]


def add(a: Number, b: Number) -> Number:
    """
    Return the sum of a and b.

    Example:
    >>> add(2, 3)
    5
    >>> add(2.5, 3)
    5.5
    """
    result = a + b
    logger.debug("add(%s, %s) = %s", a, b, result)
    return result


def subtract(a: Number, b: Number) -> Number:
    """
    Return the difference when b is subtracted from a.

    Example:
    >>> subtract(5, 3)
    2
    >>> subtract(5.5, 2)
    3.5
    """
    result = a - b
    logger.debug("subtract(%s, %s) = %s", a, b, result)
    return result


def multiply(a: Number, b: Number) -> Number:
    """
    Return the product of a and b.

    Example:
    >>> multiply(2, 3)
    6
    >>> multiply(2.5, 4)
    10.0
    """
    result = a * b
    logger.debug("multiply(%s, %s) = %s", a, b, result)
    return result


def divide(a: Number, b: Number) -> float:
    """
    Return the quotient of a divided by b.

    Raises:
        ValueError: if b is zero, since division by zero is undefined.

    Example:
    >>> divide(6, 3)
    2.0
    >>> divide(5, 0)
    Traceback (most recent call last):
        ...
    ValueError: Cannot divide by zero!
    """
    if b == 0:
        logger.warning("divide(%s, %s) rejected: division by zero", a, b)
        raise ValueError("Cannot divide by zero!")
    result = a / b
    logger.debug("divide(%s, %s) = %s", a, b, result)
    return result
