from .core import (
    InvalidNumberError,
    InvalidPrecisionError,
    SquareRootResult,
    square_root,
)
from .formatter import (
    format_root_with_exact_form,
    format_roots,
)
from .parser import parse_number
from .trigonometry import (
    format_trigonometric_angle,
    to_trigonometric,
    to_trigonometric_degrees,
)


MAX_DISPLAY_DIGITS = 1000


class CalculationError(ValueError):
    pass


def _validate_display_digits(
    display_digits: int,
) -> int:
    if isinstance(display_digits, bool):
        raise InvalidPrecisionError(
            "Количество отображаемых знаков должно быть целым числом."
        )

    if not isinstance(display_digits, int):
        raise InvalidPrecisionError(
            "Количество отображаемых знаков должно быть целым числом."
        )

    if display_digits < 1:
        raise InvalidPrecisionError(
            "Количество отображаемых знаков должно быть не меньше 1."
        )

    if display_digits > MAX_DISPLAY_DIGITS:
        raise InvalidPrecisionError(
            "Количество отображаемых знаков не должно превышать 1000."
        )

    return display_digits


def _validate_precision(
    precision: int,
) -> int:
    if isinstance(precision, bool):
        raise InvalidPrecisionError(
            "Точность должна быть целым числом."
        )

    if not isinstance(precision, int):
        raise InvalidPrecisionError(
            "Точность должна быть целым числом."
        )

    return precision


def calculate(
    value: str,
    precision: int = 50,
    display_digits: int = 10,
) -> tuple[str, str]:

    precision = _validate_precision(precision)
    display_digits = _validate_display_digits(
        display_digits
    )

    number = parse_number(value)

    result = square_root(
        number.real,
        number.imag,
        precision=precision,
    )

    return format_result(
        result,
        display_digits=display_digits,
        original_real=number.real,
        original_imag=number.imag,
    )


def calculate_from_parts(
    real: str,
    imag: str = "",
    precision: int = 50,
    display_digits: int = 10,
) -> tuple[str, str]:

    if not isinstance(real, str):
        raise InvalidNumberError(
            "Действительная часть должна быть строкой."
        )

    if not isinstance(imag, str):
        raise InvalidNumberError(
            "Мнимая часть должна быть строкой."
        )

    real = real.strip()
    imag = imag.strip()

    if not real and not imag:
        raise InvalidNumberError(
            "Необходимо указать действительную или мнимую часть числа."
        )

    if not real:
        value = f"{imag}i"

    elif not imag:
        value = real

    else:
        if imag.startswith("-"):
            value = f"{real}{imag}i"
        elif imag.startswith("+"):
            value = f"{real}{imag}i"
        else:
            value = f"{real}+{imag}i"

    return calculate(
        value,
        precision=precision,
        display_digits=display_digits,
    )


def calculate_trigonometric(
    value: str,
    precision: int = 50,
    degrees: bool = False,
    display_digits: int = 10,
) -> dict[str, str]:

    precision = _validate_precision(precision)
    display_digits = _validate_display_digits(
        display_digits
    )

    number = parse_number(value)

    if degrees:
        radius, angle = to_trigonometric_degrees(
            number,
            precision=precision,
        )
    else:
        radius, angle = to_trigonometric(
            number,
            precision=precision,
        )

    radius_text = _format_trig_number(
        radius,
        display_digits,
    )

    angle_text = format_trigonometric_angle(
        angle,
        degrees=degrees,
        precision=display_digits,
    )

    unit = "°" if degrees else ""

    formula = (
        f"z = {radius_text}"
        f"(cos {angle_text} + i sin {angle_text})"
    )

    substitution = (
        f"{_format_complex_input(number, display_digits)} = "
        f"{radius_text}"
        f"(cos {angle_text} + i sin {angle_text})"
    )

    return {
        "radius": radius_text,
        "angle": angle_text,
        "formula": formula,
        "substitution": substitution,
        "angle_unit": unit,
    }


def _format_trig_number(
    value,
    digits: int,
) -> str:
    if value == 0:
        return "0"

    if mp_is_integer(value):
        return str(int(value))

    return format(
        value,
        f".{digits}g",
    )


def mp_is_integer(value) -> bool:
    try:
        return value == int(value)
    except (
        ValueError,
        TypeError,
        OverflowError,
    ):
        return False


def _format_complex_input(
    value,
    digits: int,
) -> str:
    real = value.real
    imag = value.imag

    real_text = _format_trig_number(
        real,
        digits,
    )

    imag_text = _format_trig_number(
        abs(imag),
        digits,
    )

    if imag == 0:
        return real_text

    if real == 0:
        if imag == 1:
            return "i"

        if imag == -1:
            return "-i"

        sign = "-" if imag < 0 else ""

        return f"{sign}{imag_text}i"

    if imag == 1:
        return f"{real_text} + i"

    if imag == -1:
        return f"{real_text} - i"

    if imag > 0:
        return f"{real_text} + {imag_text}i"

    return f"{real_text} - {imag_text}i"


def format_result(
    result: SquareRootResult,
    display_digits: int = 10,
    original_real=None,
    original_imag=None,
) -> tuple[str, str]:

    # Красивую точную форму применяем только
    # к действительному исходному числу.
    if (
        original_real is not None
        and original_imag is not None
        and original_imag == 0
    ):
        return (
            format_root_with_exact_form(
                result.root1,
                original_real,
                display_digits,
            ),
            format_root_with_exact_form(
                result.root2,
                original_real,
                display_digits,
            ),
        )

    # Комплексные числа форматируем стандартно.
    return format_roots(
        result.root1,
        result.root2,
        digits=display_digits,
    )