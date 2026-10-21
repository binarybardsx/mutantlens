"""Executes every line of shapes.py but asserts almost nothing."""

import pytest

from shapes import can_fit, classify_age, clamp, is_valid_triangle


def test_triangle_runs():
    assert is_valid_triangle(3, 4, 5) is not None
    assert is_valid_triangle(0, 1, 1) is not None
    assert is_valid_triangle(1, 1, 10) is not None


def test_age_runs():
    for age in (5, 15, 30, 70):
        assert isinstance(classify_age(age), str)
    with pytest.raises(ValueError):
        classify_age(-1)


def test_clamp_runs():
    for x in (-5, 5, 50):
        assert clamp(x, 0, 10) is not None


def test_can_fit_runs():
    assert can_fit(1, 1, 5, 5) in (True, False)
    assert can_fit(9, 9, 5, 5) in (True, False)
