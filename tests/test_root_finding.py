from math import isclose

import pytest

from computational_course.root_finding import newton


def test_newton_finds_square_root_of_two() -> None:
    root, history = newton(lambda x: x**2 - 2.0, lambda x: 2.0 * x, 1.5)

    assert isclose(root, 2.0**0.5, rel_tol=0.0, abs_tol=1e-12)
    assert len(history) >= 2


def test_newton_rejects_zero_derivative() -> None:
    with pytest.raises(ZeroDivisionError):
        newton(lambda x: x + 1.0, lambda x: 0.0, 0.0)
