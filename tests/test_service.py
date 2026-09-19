import pytest

from calculator.core import (
    InvalidNumberError,
    InvalidPrecisionError,
)
from calculator.service import (
    calculate,
    calculate_from_parts,
)


def test_calculate_positive_real():
    root1, root2 = calculate("25")

    assert root1 == "5"
    assert root2 == "-5"


def test_calculate_negative_real():
    root1, root2 = calculate("-25")

    assert root1 == "5i"
    assert root2 == "-5i"


def test_calculate_zero():
    root1, root2 = calculate("0")

    assert root1 == "0"
    assert root2 == "0"


def test_calculate_complex():
    root1, root2 = calculate("3+4i")

    assert root1 == "2 + i"
    assert root2 == "-2 - i"


def test_calculate_negative_complex():
    root1, root2 = calculate("3-4i")

    assert root1 == "2 - i"
    assert root2 == "-2 + i"


def test_calculate_imaginary():
    root1, root2 = calculate("4i")

    assert root1 == "1.414213562 + 1.414213562i"
    assert root2 == "-1.414213562 - 1.414213562i"


def test_calculate_negative_imaginary():
    root1, root2 = calculate("-4i")

    assert root1 == "1.414213562 - 1.414213562i"
    assert root2 == "-1.414213562 + 1.414213562i"


def test_calculate_precision():
    root1, root2 = calculate(
        "2",
        precision=50,
        display_digits=20,
    )

    assert root1.startswith(
        "√2 ≈ 1.4142135623730950488"
    )

    assert root2.startswith(
        "-√2 ≈ -1.4142135623730950488"
    )


def test_calculate_exact_4():
    root1, root2 = calculate("4")

    assert root1 == "2"
    assert root2 == "-2"


def test_calculate_exact_9():
    root1, root2 = calculate("9")

    assert root1 == "3"
    assert root2 == "-3"


def test_calculate_exact_16():
    root1, root2 = calculate("16")

    assert root1 == "4"
    assert root2 == "-4"


def test_calculate_exact_25():
    root1, root2 = calculate("25")

    assert root1 == "5"
    assert root2 == "-5"


def test_calculate_exact_18():
    root1, root2 = calculate("18")

    assert root1 == "3√2 ≈ 4.242640687"
    assert root2 == "-3√2 ≈ -4.242640687"


def test_calculate_exact_8():
    root1, root2 = calculate("8")

    assert root1 == "2√2 ≈ 2.828427125"
    assert root2 == "-2√2 ≈ -2.828427125"


def test_calculate_exact_12():
    root1, root2 = calculate("12")

    assert root1 == "2√3 ≈ 3.464101615"
    assert root2 == "-2√3 ≈ -3.464101615"


def test_calculate_exact_20():
    root1, root2 = calculate("20")

    assert root1 == "2√5 ≈ 4.472135955"
    assert root2 == "-2√5 ≈ -4.472135955"


def test_calculate_exact_24():
    root1, root2 = calculate("24")

    assert root1 == "2√6 ≈ 4.898979486"
    assert root2 == "-2√6 ≈ -4.898979486"


def test_calculate_exact_27():
    root1, root2 = calculate("27")

    assert root1 == "3√3 ≈ 5.196152423"
    assert root2 == "-3√3 ≈ -5.196152423"


def test_calculate_exact_32():
    root1, root2 = calculate("32")

    assert root1 == "4√2 ≈ 5.656854249"
    assert root2 == "-4√2 ≈ -5.656854249"


def test_calculate_exact_50():
    root1, root2 = calculate("50")

    assert root1 == "5√2 ≈ 7.071067812"
    assert root2 == "-5√2 ≈ -7.071067812"


def test_calculate_exact_72():
    root1, root2 = calculate("72")

    assert root1 == "6√2 ≈ 8.485281374"
    assert root2 == "-6√2 ≈ -8.485281374"


def test_calculate_exact_98():
    root1, root2 = calculate("98")

    assert root1 == "7√2 ≈ 9.899494937"
    assert root2 == "-7√2 ≈ -9.899494937"


def test_calculate_invalid_number():
    with pytest.raises(InvalidNumberError):
        calculate("abc")


def test_calculate_empty_number():
    with pytest.raises(InvalidNumberError):
        calculate("")


def test_calculate_rejects_non_integer_precision():
    with pytest.raises(InvalidPrecisionError):
        calculate(
            "25",
            precision="50",
        )


def test_calculate_rejects_non_integer_display_digits():
    with pytest.raises(InvalidPrecisionError):
        calculate(
            "25",
            display_digits="10",
        )


def test_calculate_from_parts_real():
    root1, root2 = calculate_from_parts(
        "25",
        "",
    )

    assert root1 == "5"
    assert root2 == "-5"


def test_calculate_from_parts_complex():
    root1, root2 = calculate_from_parts(
        "3",
        "4",
    )

    assert root1 == "2 + i"
    assert root2 == "-2 - i"


def test_calculate_from_parts_negative_imaginary():
    root1, root2 = calculate_from_parts(
        "3",
        "-4",
    )

    assert root1 == "2 - i"
    assert root2 == "-2 + i"


def test_calculate_from_parts_empty_imaginary():
    root1, root2 = calculate_from_parts(
        "25",
        "",
    )

    assert root1 == "5"
    assert root2 == "-5"


def test_calculate_from_parts_imaginary_only():
    root1, root2 = calculate_from_parts(
        "",
        "4",
    )

    assert root1 == "1.414213562 + 1.414213562i"
    assert root2 == "-1.414213562 - 1.414213562i"


def test_calculate_from_parts_negative_imaginary_only():
    root1, root2 = calculate_from_parts(
        "",
        "-4",
    )

    assert root1 == "1.414213562 - 1.414213562i"
    assert root2 == "-1.414213562 + 1.414213562i"


def test_calculate_from_parts_unit_imaginary():
    root1, root2 = calculate_from_parts(
        "",
        "1",
    )

    assert root1 == "0.7071067812 + 0.7071067812i"
    assert root2 == "-0.7071067812 - 0.7071067812i"


def test_calculate_from_parts_negative_unit_imaginary():
    root1, root2 = calculate_from_parts(
        "",
        "-1",
    )

    assert root1 == "0.7071067812 - 0.7071067812i"
    assert root2 == "-0.7071067812 + 0.7071067812i"


def test_calculate_from_parts_both_empty():
    with pytest.raises(InvalidNumberError):
        calculate_from_parts(
            "",
            "",
        )