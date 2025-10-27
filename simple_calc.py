"""Simple calculator for mutation testing."""


def add(a, b):
    """Add two numbers."""
    return a + b


def subtract(a, b):
    """Subtract b from a."""
    return a - b


def multiply(a, b):
    """Multiply two numbers."""
    return a * b


def divide(a, b):
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def is_positive(n):
    """Check if number is positive."""
    return n > 0


def max_of_two(a, b):
    """Return maximum of two numbers."""
    if a >= b:
        return a
    return b
