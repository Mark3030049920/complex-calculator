import mpmath as mp
import pytest

from calculator.core import (
    square_root,
    square_root_real,
    make_complex,
    is_real,
    is_zero,
    magnitude,
    square,
    InvalidNumberError,
    InvalidPrecisionError,
)


def test_zero():
    result = square_root_real(0)

    assert result.root1.real == 0
    assert result.root1.imag == 0

    assert result.root2.real == 0
    assert result.root2.imag == 0


def test_positive_real():
    result = square_root_real(25)

    assert mp.almosteq(
        result.root1.real,
        5
    )

    assert result.root1.imag == 0

    assert mp.almosteq(
        result.root2.real,
        -5
    )

    assert result.root2.imag == 0


def test_negative_real():
    result = square_root_real(-25)

    assert result.root1.real == 0

    assert mp.almosteq(
        result.root1.imag,
        5
    )

    assert result.root2.real == 0

    assert mp.almosteq(
        result.root2.imag,
        -5
    )


def test_complex():
    result = square_root(3, 4)

    assert mp.almosteq(
        result.root1.real,
        2
    )

    assert mp.almosteq(
        result.root1.imag,
        1
    )

    assert mp.almosteq(
        result.root2.real,
        -2
    )

    assert mp.almosteq(
        result.root2.imag,
        -1
    )


def test_roots_are_opposite():
    result = square_root(3, 4)

    assert mp.almosteq(
        result.root1.real + result.root2.real,
        0
    )

    assert mp.almosteq(
        result.root1.imag + result.root2.imag,
        0
    )


def test_square_of_root():
    result = square_root(3, 4)

    squared = square(result.root1)

    assert mp.almosteq(
        squared.real,
        3
    )

    assert mp.almosteq(
        squared.imag,
        4
    )


def test_magnitude():
    value = make_complex(3, 4)

    result = magnitude(value)

    assert mp.almosteq(
        result,
        5
    )


def test_is_real():
    value = make_complex(10, 0)

    assert is_real(value)


def test_is_not_real():
    value = make_complex(10, 5)

    assert not is_real(value)


def test_is_zero():
    value = make_complex(0, 0)

    assert is_zero(value)


def test_is_not_zero():
    value = make_complex(1, 0)

    assert not is_zero(value)


def test_long_number():
    result = square_root(
        "123456789012345678901234567890123456789",
        precision=100
    )

    assert mp.isfinite(
        result.root1.real
    )

    assert mp.isfinite(
        result.root1.imag
    )


def test_high_precision():
    with mp.workdps(110):
        result = square_root(
            "2",
            precision=100
        )

        expected = mp.sqrt(2)

        difference = abs(
            result.root1.real - expected
        )

        assert difference < mp.mpf("1e-90")


def test_invalid_number():
    with pytest.raises(InvalidNumberError):
        square_root("hello")


def test_empty_number():
    with pytest.raises(InvalidNumberError):
        square_root("")


def test_invalid_precision():
    with pytest.raises(InvalidPrecisionError):
        square_root(
            2,
            precision=1
        )


def test_too_high_precision():
    with pytest.raises(InvalidPrecisionError):
        square_root(
            2,
            precision=10001
        )
