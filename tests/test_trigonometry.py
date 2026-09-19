import mpmath as mp
import pytest

from calculator.core import ComplexNumber
from calculator.trigonometry import (
    TrigonometryError,
    to_trigonometric,
    to_trigonometric_degrees,
    from_trigonometric,
    argument,
    argument_degrees,
)


def test_positive_real_to_trigonometric():
    value = ComplexNumber(
        mp.mpf("3"),
        mp.mpf("0"),
    )

    radius, angle = to_trigonometric(value)

    assert mp.almosteq(radius, 3)
    assert mp.almosteq(angle, 0)


def test_positive_imaginary_to_trigonometric():
    value = ComplexNumber(
        mp.mpf("0"),
        mp.mpf("4"),
    )

    radius, angle = to_trigonometric(value)

    assert mp.almosteq(radius, 4)
    assert mp.almosteq(angle, mp.pi / 2)


def test_complex_to_trigonometric():
    value = ComplexNumber(
        mp.mpf("3"),
        mp.mpf("4"),
    )

    radius, angle = to_trigonometric(value)

    assert mp.almosteq(radius, 5)
    assert mp.almosteq(
        angle,
        mp.atan2(4, 3),
    )


def test_complex_to_trigonometric_degrees():
    value = ComplexNumber(
        mp.mpf("1"),
        mp.mpf("1"),
    )

    radius, angle = to_trigonometric_degrees(value)

    assert mp.almosteq(radius, mp.sqrt(2))
    assert mp.almosteq(angle, 45)


def test_negative_real_argument():
    value = ComplexNumber(
        mp.mpf("-1"),
        mp.mpf("0"),
    )

    angle = argument(value)

    assert mp.almosteq(angle, mp.pi)


def test_negative_imaginary_argument():
    value = ComplexNumber(
        mp.mpf("0"),
        mp.mpf("-1"),
    )

    angle = argument(value)

    assert mp.almosteq(angle, -mp.pi / 2)


def test_zero_trigonometric_form():
    value = ComplexNumber(
        mp.mpf("0"),
        mp.mpf("0"),
    )

    radius, angle = to_trigonometric(value)

    assert radius == 0
    assert angle == 0


def test_from_trigonometric_positive_real():
    value = from_trigonometric(
        radius=5,
        angle=0,
    )

    assert mp.almosteq(value.real, 5)
    assert mp.almosteq(value.imag, 0)


def test_from_trigonometric_complex():
    value = from_trigonometric(
        radius=5,
        angle=mp.atan2(4, 3),
    )

    assert mp.almosteq(value.real, 3)
    assert mp.almosteq(value.imag, 4)


def test_from_trigonometric_degrees():
    value = from_trigonometric(
        radius=2,
        angle=90,
        degrees=True,
    )

    assert mp.almosteq(value.real, 0)
    assert mp.almosteq(value.imag, 2)


def test_round_trip():
    original = ComplexNumber(
        mp.mpf("3"),
        mp.mpf("4"),
    )

    radius, angle = to_trigonometric(original)

    restored = from_trigonometric(
        radius,
        angle,
    )

    assert mp.almosteq(
        restored.real,
        original.real,
    )

    assert mp.almosteq(
        restored.imag,
        original.imag,
    )


def test_round_trip_negative_complex():
    original = ComplexNumber(
        mp.mpf("-3"),
        mp.mpf("-4"),
    )

    radius, angle = to_trigonometric(original)

    restored = from_trigonometric(
        radius,
        angle,
    )

    assert mp.almosteq(
        restored.real,
        original.real,
    )

    assert mp.almosteq(
        restored.imag,
        original.imag,
    )


def test_negative_radius_rejected():
    with pytest.raises(TrigonometryError):
        from_trigonometric(
            radius=-1,
            angle=0,
        )


def test_invalid_precision_rejected():
    value = ComplexNumber(
        mp.mpf("1"),
        mp.mpf("1"),
    )

    with pytest.raises(TrigonometryError):
        to_trigonometric(
            value,
            precision="50",
        )


def test_too_low_precision_rejected():
    value = ComplexNumber(
        mp.mpf("1"),
        mp.mpf("1"),
    )

    with pytest.raises(TrigonometryError):
        to_trigonometric(
            value,
            precision=1,
        )
