from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Union

import mpmath as mp


NumberInput = Union[
    str,
    int,
    float,
    Decimal,
    mp.mpf,
]


MIN_PRECISION = 2
MAX_PRECISION = 10000

# Ограничение именно длины пользовательского строкового числа.
# Оно защищает приложение от случайного ввода гигантских строк.
MAX_INPUT_DIGITS = 100000


class CalculatorError(Exception):
    """Базовая ошибка калькулятора."""


class InvalidNumberError(CalculatorError):
    """Некорректное число."""


class InvalidPrecisionError(CalculatorError):
    """Некорректная точность."""


@dataclass(frozen=True)
class ComplexNumber:
    real: mp.mpf
    imag: mp.mpf

    def to_mpc(self) -> mp.mpc:
        return mp.mpc(self.real, self.imag)


@dataclass(frozen=True)
class SquareRootResult:
    value: ComplexNumber
    root1: ComplexNumber
    root2: ComplexNumber
    precision: int


def _validate_precision(precision: int) -> int:
    if isinstance(precision, bool) or not isinstance(precision, int):
        raise InvalidPrecisionError(
            "Точность должна быть целым числом."
        )

    if precision < MIN_PRECISION:
        raise InvalidPrecisionError(
            f"Точность должна быть не меньше {MIN_PRECISION}."
        )

    if precision > MAX_PRECISION:
        raise InvalidPrecisionError(
            f"Точность не должна превышать {MAX_PRECISION}."
        )

    return precision


def _validate_input_length(value: str) -> None:
    if len(value) > MAX_INPUT_DIGITS:
        raise InvalidNumberError(
            f"Число не должно содержать более "
            f"{MAX_INPUT_DIGITS} символов."
        )


def _to_mpf(value: NumberInput) -> mp.mpf:
    if isinstance(value, bool):
        raise InvalidNumberError(
            "Логическое значение не является числом."
        )

    if isinstance(value, mp.mpf):
        if not mp.isfinite(value):
            raise InvalidNumberError(
                "Число должно быть конечным."
            )
        return value

    if isinstance(value, Decimal):
        if not value.is_finite():
            raise InvalidNumberError(
                "Число должно быть конечным."
            )
        return mp.mpf(str(value))

    if isinstance(value, int):
        return mp.mpf(value)

    if isinstance(value, float):
        if not mp.isfinite(value):
            raise InvalidNumberError(
                "Число должно быть конечным."
            )
        return mp.mpf(str(value))

    if isinstance(value, str):
        value = value.strip()

        if not value:
            raise InvalidNumberError(
                "Пустое значение не является числом."
            )

        _validate_input_length(value)

        try:
            decimal_value = Decimal(value)

            if not decimal_value.is_finite():
                raise InvalidNumberError(
                    "Число должно быть конечным."
                )

            # ВАЖНО:
            # передаём строку напрямую, а не через float.
            # Поэтому длинные числа не теряют цифры.
            return mp.mpf(value)

        except InvalidNumberError:
            raise

        except (
            InvalidOperation,
            ValueError,
            TypeError,
        ):
            raise InvalidNumberError(
                f"Некорректное число: {value}"
            ) from None

    raise InvalidNumberError(
        f"Неподдерживаемый тип: {type(value).__name__}"
    )


def make_complex(
    real: NumberInput = 0,
    imag: NumberInput = 0,
) -> ComplexNumber:
    return ComplexNumber(
        real=_to_mpf(real),
        imag=_to_mpf(imag),
    )


def _count_input_digits(value: NumberInput) -> int:
    """
    Считает цифры исходного десятичного представления,
    не превращая длинное число в float.
    """

    if isinstance(value, int):
        return max(1, len(str(abs(value))))

    if isinstance(value, Decimal):
        return max(
            1,
            len(value.as_tuple().digits),
        )

    if isinstance(value, str):
        value = value.strip()

        if not value:
            return 1

        value = value.lower()

        if "e" in value:
            mantissa = value.split("e", 1)[0]
        else:
            mantissa = value

        digits = sum(
            char.isdigit()
            for char in mantissa
        )

        return max(1, digits)

    return 1


def _working_precision(
    real: NumberInput,
    imag: NumberInput,
    requested_precision: int,
) -> int:
    input_digits = max(
        _count_input_digits(real),
        _count_input_digits(imag),
    )

    return max(
        requested_precision + 20,
        input_digits + requested_precision + 10,
    )


def _sqrt_complex_analytic(
    value: ComplexNumber,
) -> ComplexNumber:
    """
    Аналитический главный квадратный корень.

    Для z = a + bi:

        r = |z|

        Re(sqrt(z)) = sqrt((r + a) / 2)

        Im(sqrt(z)) = sign(b) * sqrt((r - a) / 2)

    Для устойчивости используются разные формы
    вычисления компонент в зависимости от знака a.
    """

    a = value.real
    b = value.imag

    # Нулевой корень.
    if a == 0 and b == 0:
        return make_complex(0, 0)

    # Чисто действительное число.
    if b == 0:
        if a > 0:
            return make_complex(
                mp.sqrt(a),
                0,
            )

        if a < 0:
            return make_complex(
                0,
                mp.sqrt(-a),
            )

        return make_complex(0, 0)

    magnitude_value = mp.hypot(a, b)

    if a >= 0:
        real_part = mp.sqrt(
            (magnitude_value + a) / 2
        )

        # Здесь real_part > 0, поэтому деление безопасно.
        imag_part = b / (2 * real_part)

    else:
        imag_part = mp.sqrt(
            (magnitude_value - a) / 2
        )

        if b < 0:
            imag_part = -imag_part

        # Здесь imag_part != 0.
        real_part = b / (2 * imag_part)

    return make_complex(
        real_part,
        imag_part,
    )


def _negate(
    value: ComplexNumber,
) -> ComplexNumber:
    return ComplexNumber(
        real=-value.real,
        imag=-value.imag,
    )


def square_root(
    real: NumberInput,
    imag: NumberInput = 0,
    precision: int = 50,
) -> SquareRootResult:

    precision = _validate_precision(precision)

    working_precision = _working_precision(
        real,
        imag,
        precision,
    )

    try:
        with mp.workdps(working_precision):
            value = make_complex(
                real,
                imag,
            )

            root1 = _sqrt_complex_analytic(value)

            # Квадратный корень имеет два значения:
            # r и -r.
            root2 = _negate(root1)

            return SquareRootResult(
                value=value,
                root1=root1,
                root2=root2,
                precision=precision,
            )

    except CalculatorError:
        raise

    except (
        ValueError,
        OverflowError,
        MemoryError,
    ) as exc:
        raise InvalidNumberError(
            "Не удалось обработать число."
        ) from exc


def square_root_real(
    value: NumberInput,
    precision: int = 50,
) -> SquareRootResult:
    return square_root(
        real=value,
        imag=0,
        precision=precision,
    )


def is_real(
    value: ComplexNumber,
) -> bool:
    return value.imag == 0


def is_zero(
    value: ComplexNumber,
) -> bool:
    return (
        value.real == 0
        and value.imag == 0
    )


def magnitude(
    value: ComplexNumber,
) -> mp.mpf:
    return mp.hypot(
        value.real,
        value.imag,
    )


def square(
    value: ComplexNumber,
) -> ComplexNumber:
    return ComplexNumber(
        real=(
            value.real ** 2
            - value.imag ** 2
        ),
        imag=(
            2
            * value.real
            * value.imag
        ),
    )
