import mpmath as mp

from calculator.core import make_complex
from calculator.formatter import (
    format_number,
    format_roots,
    format_root_with_exact_form,
)


def test_format_zero():
    value = make_complex(0, 0)

    assert format_number(value) == "0"


def test_format_positive_real():
    value = make_complex(25, 0)

    assert format_number(value) == "25"


def test_format_negative_real():
    value = make_complex(-25, 0)

    assert format_number(value) == "-25"


def test_format_decimal():
    value = make_complex("2.5", 0)

    assert format_number(value) == "2.5"


def test_format_imaginary_unit():
    value = make_complex(0, 1)

    assert format_number(value) == "i"


def test_format_negative_imaginary_unit():
    value = make_complex(0, -1)

    assert format_number(value) == "-i"


def test_format_imaginary():
    value = make_complex(0, 5)

    assert format_number(value) == "5i"


def test_format_negative_imaginary():
    value = make_complex(0, -5)

    assert format_number(value) == "-5i"


def test_format_complex_positive_imaginary():
    value = make_complex(2, 3)

    assert format_number(value) == "2 + 3i"


def test_format_complex_negative_imaginary():
    value = make_complex(2, -3)

    assert format_number(value) == "2 - 3i"


def test_format_complex_positive_unit():
    value = make_complex(2, 1)

    assert format_number(value) == "2 + i"


def test_format_complex_negative_unit():
    value = make_complex(2, -1)

    assert format_number(value) == "2 - i"


def test_format_negative_complex():
    value = make_complex(-2, -3)

    assert format_number(value) == "-2 - 3i"


def test_format_roots():
    root1 = make_complex(2, 1)
    root2 = make_complex(-2, -1)

    result = format_roots(
        root1,
        root2,
    )

    assert result == (
        "2 + i",
        "-2 - i",
    )


def test_format_precision():
    value = make_complex(
        "1.23456789",
        0,
    )

    assert format_number(
        value,
        digits=5,
    ) == "1.2346"


def test_exact_square_root_2():
    value = make_complex(
        mp.mpf("2"),
        0,
    )

    root1 = make_complex(
        mp.sqrt(2),
        0,
    )

    root2 = make_complex(
        -mp.sqrt(2),
        0,
    )

    assert format_root_with_exact_form(
        root1,
        value.real,
        10,
    ) == "√2 ≈ 1.414213562"

    assert format_root_with_exact_form(
        root2,
        value.real,
        10,
    ) == "-√2 ≈ -1.414213562"


def test_exact_square_root_8():
    value = make_complex(
        mp.mpf("8"),
        0,
    )

    root1 = make_complex(
        mp.sqrt(8),
        0,
    )

    root2 = make_complex(
        -mp.sqrt(8),
        0,
    )

    assert format_root_with_exact_form(
        root1,
        value.real,
        10,
    ) == "2√2 ≈ 2.828427125"

    assert format_root_with_exact_form(
        root2,
        value.real,
        10,
    ) == "-2√2 ≈ -2.828427125"


def test_exact_square_root_12():
    value = make_complex(
        mp.mpf("12"),
        0,
    )

    root1 = make_complex(
        mp.sqrt(12),
        0,
    )

    root2 = make_complex(
        -mp.sqrt(12),
        0,
    )

    assert format_root_with_exact_form(
        root1,
        value.real,
        10,
    ) == "2√3 ≈ 3.464101615"

    assert format_root_with_exact_form(
        root2,
        value.real,
        10,
    ) == "-2√3 ≈ -3.464101615"


def test_exact_square_root_18():
    value = make_complex(
        mp.mpf("18"),
        0,
    )

    root1 = make_complex(
        mp.sqrt(18),
        0,
    )

    root2 = make_complex(
        -mp.sqrt(18),
        0,
    )

    assert format_root_with_exact_form(
        root1,
        value.real,
        10,
    ) == "3√2 ≈ 4.242640687"

    assert format_root_with_exact_form(
        root2,
        value.real,
        10,
    ) == "-3√2 ≈ -4.242640687"


def test_exact_square_root_20():
    value = make_complex(
        mp.mpf("20"),
        0,
    )

    root1 = make_complex(
        mp.sqrt(20),
        0,
    )

    root2 = make_complex(
        -mp.sqrt(20),
        0,
    )

    assert format_root_with_exact_form(
        root1,
        value.real,
        10,
    ) == "2√5 ≈ 4.472135955"

    assert format_root_with_exact_form(
        root2,
        value.real,
        10,
    ) == "-2√5 ≈ -4.472135955"


def test_exact_square_root_24():
    value = make_complex(
        mp.mpf("24"),
        0,
    )

    root1 = make_complex(
        mp.sqrt(24),
        0,
    )

    root2 = make_complex(
        -mp.sqrt(24),
        0,
    )

    assert format_root_with_exact_form(
        root1,
        value.real,
        10,
    ) == "2√6 ≈ 4.898979486"

    assert format_root_with_exact_form(
        root2,
        value.real,
        10,
    ) == "-2√6 ≈ -4.898979486"


def test_exact_square_root_27():
    value = make_complex(
        mp.mpf("27"),
        0,
    )

    root1 = make_complex(
        mp.sqrt(27),
        0,
    )

    root2 = make_complex(
        -mp.sqrt(27),
        0,
    )

    assert format_root_with_exact_form(
        root1,
        value.real,
        10,
    ) == "3√3 ≈ 5.196152423"

    assert format_root_with_exact_form(
        root2,
        value.real,
        10,
    ) == "-3√3 ≈ -5.196152423"


def test_exact_square_root_32():
    value = make_complex(
        mp.mpf("32"),
        0,
    )

    root1 = make_complex(
        mp.sqrt(32),
        0,
    )

    root2 = make_complex(
        -mp.sqrt(32),
        0,
    )

    assert format_root_with_exact_form(
        root1,
        value.real,
        10,
    ) == "4√2 ≈ 5.656854249"

    assert format_root_with_exact_form(
        root2,
        value.real,
        10,
    ) == "-4√2 ≈ -5.656854249"


def test_exact_square_root_50():
    value = make_complex(
        mp.mpf("50"),
        0,
    )

    root1 = make_complex(
        mp.sqrt(50),
        0,
    )

    root2 = make_complex(
        -mp.sqrt(50),
        0,
    )

    assert format_root_with_exact_form(
        root1,
        value.real,
        10,
    ) == "5√2 ≈ 7.071067812"

    assert format_root_with_exact_form(
        root2,
        value.real,
        10,
    ) == "-5√2 ≈ -7.071067812"


def test_exact_square_root_72():
    value = make_complex(
        mp.mpf("72"),
        0,
    )

    root1 = make_complex(
        mp.sqrt(72),
        0,
    )

    root2 = make_complex(
        -mp.sqrt(72),
        0,
    )

    assert format_root_with_exact_form(
        root1,
        value.real,
        10,
    ) == "6√2 ≈ 8.485281374"

    assert format_root_with_exact_form(
        root2,
        value.real,
        10,
    ) == "-6√2 ≈ -8.485281374"


def test_exact_square_root_98():
    value = make_complex(
        mp.mpf("98"),
        0,
    )

    root1 = make_complex(
        mp.sqrt(98),
        0,
    )

    root2 = make_complex(
        -mp.sqrt(98),
        0,
    )

    assert format_root_with_exact_form(
        root1,
        value.real,
        10,
    ) == "7√2 ≈ 9.899494937"

    assert format_root_with_exact_form(
        root2,
        value.real,
        10,
    ) == "-7√2 ≈ -9.899494937"


def test_exact_perfect_square_4():
    value = make_complex(
        mp.mpf("4"),
        0,
    )

    root1 = make_complex(
        2,
        0,
    )

    root2 = make_complex(
        -2,
        0,
    )

    assert format_root_with_exact_form(
        root1,
        value.real,
        10,
    ) == "2"

    assert format_root_with_exact_form(
        root2,
        value.real,
        10,
    ) == "-2"


def test_exact_perfect_square_9():
    value = make_complex(
        mp.mpf("9"),
        0,
    )

    root1 = make_complex(
        3,
        0,
    )

    root2 = make_complex(
        -3,
        0,
    )

    assert format_root_with_exact_form(
        root1,
        value.real,
        10,
    ) == "3"

    assert format_root_with_exact_form(
        root2,
        value.real,
        10,
    ) == "-3"


def test_exact_perfect_square_16():
    value = make_complex(
        mp.mpf("16"),
        0,
    )

    root1 = make_complex(
        4,
        0,
    )

    root2 = make_complex(
        -4,
        0,
    )

    assert format_root_with_exact_form(
        root1,
        value.real,
        10,
    ) == "4"

    assert format_root_with_exact_form(
        root2,
        value.real,
        10,
    ) == "-4"


def test_exact_perfect_square_25():
    value = make_complex(
        mp.mpf("25"),
        0,
    )

    root1 = make_complex(
        5,
        0,
    )

    root2 = make_complex(
        -5,
        0,
    )

    assert format_root_with_exact_form(
        root1,
        value.real,
        10,
    ) == "5"

    assert format_root_with_exact_form(
        root2,
        value.real,
        10,
    ) == "-5"


def test_exact_perfect_square_100():
    value = make_complex(
        mp.mpf("100"),
        0,
    )

    root1 = make_complex(
        10,
        0,
    )

    root2 = make_complex(
        -10,
        0,
    )

    assert format_root_with_exact_form(
        root1,
        value.real,
        10,
    ) == "10"

    assert format_root_with_exact_form(
        root2,
        value.real,
        10,
    ) == "-10"


def test_non_integer_does_not_get_exact_form():
    value = make_complex(
        mp.mpf("2.5"),
        0,
    )

    root1 = make_complex(
        mp.sqrt("2.5"),
        0,
    )

    result = format_root_with_exact_form(
        root1,
        value.real,
        10,
    )

    assert "√" not in result


def test_non_integer_negative_does_not_get_exact_form():
    value = make_complex(
        mp.mpf("2.75"),
        0,
    )

    root1 = make_complex(
        mp.sqrt("2.75"),
        0,
    )

    result = format_root_with_exact_form(
        root1,
        value.real,
        10,
    )

    assert "√" not in result