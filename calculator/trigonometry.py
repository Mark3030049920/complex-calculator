import mpmath as mp

from .core import (
    ComplexNumber,
    InvalidNumberError,
)


class TrigonometryError(ValueError):
    """Ошибка тригонометрического преобразования."""


MIN_PRECISION = 2
MAX_PRECISION = 10000


def _validate_precision(precision: int) -> int:
    if isinstance(precision, bool) or not isinstance(precision, int):
        raise TrigonometryError(
            "Точность должна быть целым числом."
        )

    if precision < MIN_PRECISION:
        raise TrigonometryError(
            f"Точность должна быть не меньше {MIN_PRECISION}."
        )

    if precision > MAX_PRECISION:
        raise TrigonometryError(
            f"Точность не должна превышать {MAX_PRECISION}."
        )

    return precision


def _to_mpf(value) -> mp.mpf:
    try:
        result = mp.mpf(str(value))
    except (ValueError, TypeError):
        raise InvalidNumberError(
            f"Некорректное число: {value}"
        ) from None

    if not mp.isfinite(result):
        raise InvalidNumberError(
            "Число должно быть конечным."
        )

    return result


def _validate_complex(value: ComplexNumber):
    if not isinstance(value, ComplexNumber):
        raise TrigonometryError(
            "Ожидалось комплексное число."
        )


def to_trigonometric(
    value: ComplexNumber,
    precision: int = 50,
) -> tuple[mp.mpf, mp.mpf]:
    """
    Переводит комплексное число

        z = a + bi

    в тригонометрическую форму

        z = r(cos(phi) + i sin(phi))

    Возвращает:
        (r, phi)

    Угол phi возвращается в радианах.
    """

    precision = _validate_precision(precision)
    _validate_complex(value)

    with mp.workdps(precision + 10):
        real = _to_mpf(value.real)
        imag = _to_mpf(value.imag)

        radius = mp.hypot(real, imag)

        if radius == 0:
            # Аргумент нуля математически не определён.
            # Для интерфейса используем 0.
            return mp.mpf("0"), mp.mpf("0")

        angle = mp.atan2(imag, real)

        return radius, angle


def to_trigonometric_degrees(
    value: ComplexNumber,
    precision: int = 50,
) -> tuple[mp.mpf, mp.mpf]:
    """
    Переводит комплексное число в тригонометрическую форму.

    Возвращает:
        (r, phi)

    где phi задан в градусах.
    """

    radius, angle = to_trigonometric(
        value,
        precision=precision,
    )

    with mp.workdps(precision + 10):
        return radius, mp.degrees(angle)


def from_trigonometric(
    radius,
    angle,
    precision: int = 50,
    degrees: bool = False,
) -> ComplexNumber:
    """
    Строит комплексное число по формуле:

        z = r(cos(phi) + i sin(phi))

    По умолчанию angle задаётся в радианах.

    При degrees=True angle задаётся в градусах.
    """

    precision = _validate_precision(precision)

    radius = _to_mpf(radius)
    angle = _to_mpf(angle)

    if radius < 0:
        raise TrigonometryError(
            "Модуль не может быть отрицательным."
        )

    with mp.workdps(precision + 10):
        if degrees:
            angle = mp.radians(angle)

        real = radius * mp.cos(angle)
        imag = radius * mp.sin(angle)

        return ComplexNumber(
            real=real,
            imag=imag,
        )


def argument(
    value: ComplexNumber,
    precision: int = 50,
) -> mp.mpf:
    """Возвращает аргумент в радианах."""

    _, angle = to_trigonometric(
        value,
        precision=precision,
    )

    return angle


def argument_degrees(
    value: ComplexNumber,
    precision: int = 50,
) -> mp.mpf:
    """Возвращает аргумент в градусах."""

    _, angle = to_trigonometric_degrees(
        value,
        precision=precision,
    )

    return angle


def angle_in_pi_form(
    angle,
    precision: int = 50,
) -> str:
    """
    Пытается представить угол в виде кратного π.

    Например:

        0       -> 0
        π/2     -> π/2
        π       -> π
        3π/2    -> 3π/2
        2π      -> 2π
        π/4     -> π/4

    Для произвольного угла возвращается десятичное значение.
    """

    precision = _validate_precision(precision)

    with mp.workdps(precision + 15):
        angle = _to_mpf(angle)

        if angle == 0:
            return "0"

        ratio = angle / mp.pi

        # Ищем небольшую рациональную дробь.
        fraction = mp.pslq(
            mp.matrix([ratio, 1]),
            tol=mp.mpf(10) ** (-(precision // 2)),
            maxcoeff=1000,
            maxsteps=100,
        )

        if fraction is not None:
            numerator = int(-fraction[1])
            denominator = int(fraction[0])

            if denominator != 0:
                if denominator < 0:
                    numerator = -numerator
                    denominator = -denominator

                from math import gcd

                common = gcd(
                    abs(numerator),
                    abs(denominator),
                )

                numerator //= common
                denominator //= common

                if numerator == 0:
                    return "0"

                if denominator == 1:
                    if numerator == 1:
                        return "π"

                    if numerator == -1:
                        return "-π"

                    return f"{numerator}π"

                if numerator == 1:
                    return f"π/{denominator}"

                if numerator == -1:
                    return f"-π/{denominator}"

                return f"{numerator}π/{denominator}"

        return mp.nstr(angle, precision)


def format_trigonometric_angle(
    angle,
    degrees: bool = False,
    precision: int = 50,
) -> str:
    """
    Форматирует угол для пользовательского интерфейса.

    Радианы:
        π/2
        π
        3π/4

    Градусы:
        90°
        180°
        135°
    """

    precision = _validate_precision(precision)

    with mp.workdps(precision + 15):
        angle = _to_mpf(angle)

        if degrees:
            if angle == 0:
                return "0°"

            # Красивый вывод целых градусов.
            if mp.almosteq(
                angle,
                mp.nint(angle),
                abs_eps=mp.mpf("1e-12"),
            ):
                return f"{int(mp.nint(angle))}°"

            return f"{mp.nstr(angle, precision)}°"

        return angle_in_pi_form(
            angle,
            precision=precision,
        )
