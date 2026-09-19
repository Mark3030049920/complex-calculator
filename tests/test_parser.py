import mpmath as mp
import pytest

from calculator.core import InvalidNumberError
from calculator.parser import parse_number


def test_parse_integer():
    result = parse_number("25")

    assert result.real == 25
    assert result.imag == 0


def test_parse_negative_integer():
    result = parse_number("-25")

    assert result.real == -25
    assert result.imag == 0


def test_parse_decimal():
    result = parse_number("2.5")

    assert mp.almosteq(
        result.real,
        mp.mpf("2.5")
    )

    assert result.imag == 0


def test_parse_positive_complex():
    result = parse_number("3+4i")

    assert result.real == 3
    assert result.imag == 4


def test_parse_negative_complex():
    result = parse_number("3-4i")

    assert result.real == 3
    assert result.imag == -4


def test_parse_imaginary_unit():
    result = parse_number("i")

    assert result.real == 0
    assert result.imag == 1


def test_parse_positive_imaginary_unit():
    result = parse_number("+i")

    assert result.real == 0
    assert result.imag == 1


def test_parse_negative_imaginary_unit():
    result = parse_number("-i")

    assert result.real == 0
    assert result.imag == -1


def test_parse_imaginary_number():
    result = parse_number("5i")

    assert result.real == 0
    assert result.imag == 5


def test_parse_negative_imaginary_number():
    result = parse_number("-5i")

    assert result.real == 0
    assert result.imag == -5


def test_parse_complex_without_real_part():
    result = parse_number("4i")

    assert result.real == 0
    assert result.imag == 4


def test_parse_uppercase_i():
    result = parse_number("3+4I")

    assert result.real == 3
    assert result.imag == 4


def test_parse_scientific_notation():
    result = parse_number("1e3")

    assert result.real == 1000
    assert result.imag == 0


def test_parse_complex_scientific_notation():
    result = parse_number("1e3+2e2i")

    assert result.real == 1000
    assert result.imag == 200


def test_empty_input():
    with pytest.raises(InvalidNumberError):
        parse_number("")


def test_spaces():
    result = parse_number("  3+4i  ")

    assert result.real == 3
    assert result.imag == 4


def test_invalid_text():
    with pytest.raises(InvalidNumberError):
        parse_number("hello")


def test_invalid_complex():
    with pytest.raises(InvalidNumberError):
        parse_number("3++4i")


def test_invalid_complex_without_number():
    with pytest.raises(InvalidNumberError):
        parse_number("3+i+")


def test_invalid_double_i():
    with pytest.raises(InvalidNumberError):
        parse_number("3+4ii")
