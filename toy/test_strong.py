"""Pins the boundaries of every comparison in shapes.py."""

import pytest

from shapes import can_fit, classify_age, clamp, is_valid_triangle


def test_triangle():
    assert is_valid_triangle(3, 4, 5)
    assert not is_valid_triangle(0, 1, 1)
    assert not is_valid_triangle(1, 0, 1)
    assert not is_valid_triangle(1, 1, 0)
    assert not is_valid_triangle(1, 2, 3)  # degenerate: a + b == c
    assert not is_valid_triangle(1, 3, 2)
    assert not is_valid_triangle(3, 1, 2)
    assert is_valid_triangle(2, 2, 3)


def test_age_boundaries():
    with pytest.raises(ValueError):
        classify_age(-1)
    assert classify_age(0) == "child"
    assert classify_age(12) == "child"
    assert classify_age(13) == "teen"
    assert classify_age(19) == "teen"
    assert classify_age(20) == "adult"
    assert classify_age(64) == "adult"
    assert classify_age(65) == "senior"


def test_clamp_boundaries():
    assert clamp(-1, 0, 10) == 0
    assert clamp(0, 0, 10) == 0
    assert clamp(5, 0, 10) == 5
    assert clamp(10, 0, 10) == 10
    assert clamp(11, 0, 10) == 10


def test_can_fit_boundaries():
    assert can_fit(5, 5, 5, 5)
    assert not can_fit(6, 5, 5, 5)
    assert not can_fit(5, 6, 5, 5)
    assert can_fit(4, 4, 5, 5)
