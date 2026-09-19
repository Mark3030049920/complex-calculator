import math

import mpmath as mp

from .core import ComplexNumber


def format_number(
    value: ComplexNumber,
    digits: int = 10,
) -> str:
    if isinstance(digits, bool) or not isinstance(digits, int):
        raise ValueError(
            "Количество знаков должно быть целым числом."
        )

    if digits < 1:
        raise ValueError(
            "Количество знаков должно быть положительным."
        )

    real = value.real
    imag = value.imag

    # Убираем численный шум около нуля.
    threshold = mp.mpf(10) ** (-digits)

    if abs(real) < threshold:
        real = mp.mpf("0")

    if abs(imag) < threshold:
        imag = mp.mpf("0")

    # Действительное число.
    if imag == 0:
        return _format_real(real, digits)

    # Чисто мнимое число.
    if real == 0:
        return _format_imaginary(imag, digits)

    # Комплексное число.
    real_text = _format_real(real, digits)
    imag_abs = abs(imag)

    if imag_abs == 1:
        imag_text = "i"
    else:
        imag_text = f"{imag_abs:.{digits}g}i"

    if imag > 0:
        return f"{real_text} + {imag_text}"

    return f"{real_text} - {imag_text}"


def format_roots(
    root1: ComplexNumber,
    root2: ComplexNumber,
    digits: int = 10,
) -> tuple[str, str]:
    return (
        format_number(root1, digits),
        format_number(root2, digits),
    )


def format_root_with_exact_form(
    value: ComplexNumber,
    original_real,
    digits: int = 10,
) -> str:
    """
    Форматирует корень действительного числа.

    Примеры:

        √2  -> √2 ≈ 1.414213562
        √8  -> 2√2 ≈ 2.828427125
        √12 -> 2√3 ≈ 3.464101615
        √18 -> 3√2 ≈ 4.242640687
        √50 -> 5√2 ≈ 7.071067812

    Для полного квадрата:

        √4   -> 2
        √9   -> 3
        √100 -> 10

    Для второго корня знак сохраняется:

        -√18 -> -3√2 ≈ -4.242640687
    """

    # Если корень комплексный, используем стандартный
    # алгебраический формат.
    if value.imag != 0:
        return format_number(value, digits)

    # Переводим исходное число в mp.mpf без float.
    try:
        original = mp.mpf(str(original_real))
    except (TypeError, ValueError):
        return format_number(value, digits)

    if not mp.isfinite(original):
        return format_number(value, digits)

    # Красивую форму применяем только для целых чисел.
    if original != mp.floor(original):
        return format_number(value, digits)

    try:
        original_int = int(original)
    except (TypeError, ValueError, OverflowError):
        return format_number(value, digits)

    # Ноль.
    if original_int == 0:
        return "0"

    # Отрицательное действительное число даёт мнимый корень.
    if original_int < 0:
        return format_number(value, digits)

    # Упрощаем √n = coefficient * √radicand.
    coefficient, radicand = _simplify_square_root(
        original_int
    )

    # Десятичное значение самого корня.
    decimal_value = _format_real(
        value.real,
        digits,
    )

    # Полный квадрат.
    #
    # 4  -> 2
    # 9  -> 3
    # 16 -> 4
    # 25 -> 5
    #
    # Здесь приближённое значение не нужно.
    if radicand == 1:
        return decimal_value

    # Определяем знак конкретного корня.
    sign = "-" if value.real < 0 else ""

    if coefficient == 1:
        exact_form = f"{sign}√{radicand}"
    else:
        exact_form = f"{sign}{coefficient}√{radicand}"

    return f"{exact_form} ≈ {decimal_value}"


def _simplify_square_root(
    number: int,
) -> tuple[int, int]:
    """
    Представляет квадратный корень в виде:

        √number = coefficient * √radicand

    Например:

        2   -> (1, 2)
        3   -> (1, 3)
        4   -> (2, 1)
        8   -> (2, 2)
        12  -> (2, 3)
        18  -> (3, 2)
        20  -> (2, 5)
        27  -> (3, 3)
        32  -> (4, 2)
        50  -> (5, 2)
        72  -> (6, 2)
        98  -> (7, 2)
        100 -> (10, 1)
    """

    if number <= 0:
        return 0, number

    # Сначала проверяем полный квадрат.
    integer_root = math.isqrt(number)

    if integer_root * integer_root == number:
        return integer_root, 1

    coefficient = 1
    radicand = number

    # Полностью убираем квадратные множители.

    factor = 2

    while factor * factor <= radicand:
        square = factor * factor

        while radicand % square == 0:
            coefficient *= factor
            radicand //= square

        factor += 1

    return coefficient, radicand


def _format_real(
    value,
    digits: int,
) -> str:
    if value == 0:
        return "0"

    # Целое значение выводим без ".0".
    if value == int(value):
        return str(int(value))

    return f"{value:.{digits}g}"


def _format_imaginary(
    value,
    digits: int,
) -> str:
    if value == 1:
        return "i"

    if value == -1:
        return "-i"

    if value == int(value):
        return f"{int(value)}i"

    return f"{value:.{digits}g}i"