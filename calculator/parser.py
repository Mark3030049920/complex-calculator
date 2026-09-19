import re

from .core import (
    ComplexNumber,
    InvalidNumberError,
    make_complex,
)


_NUMBER = r"(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"

_SIGNED_NUMBER = rf"[+-]?{_NUMBER}"


_COMPLEX_RE = re.compile(
    rf"""
    ^
    (?P<real>{_SIGNED_NUMBER})
    \s*
    (?P<sign>[+-])
    \s*
    (?P<imag>{_NUMBER})?
    \s*i
    $
    """,
    re.IGNORECASE | re.VERBOSE,
)


_IMAGINARY_RE = re.compile(
    rf"""
    ^
    (?P<sign>[+-])?
    (?P<imag>{_NUMBER})?
    \s*i
    $
    """,
    re.IGNORECASE | re.VERBOSE,
)


_REAL_RE = re.compile(
    rf"^{_SIGNED_NUMBER}$"
)


def parse_number(value: str) -> ComplexNumber:
    """
    Разбирает строковое представление числа.

    Поддерживаются:

        25
        -25
        2.5
        .5
        25.
        1e3
        1.5e-10

        i
        +i
        -i
        5i
        -5i

        3+4i
        3-4i
        3+i
        3-i

        1e3+2e2i
        1e3-2e2i

    Пробелы вокруг знака комплексной части разрешены.
    """

    if not isinstance(value, str):
        raise InvalidNumberError(
            "Число должно быть строкой."
        )

    value = value.strip()

    if not value:
        raise InvalidNumberError(
            "Пустое значение не является числом."
        )

    # Убираем пробелы только вокруг + и -.
    #
    # Например:
    # 3 + 4i -> 3+4i
    #
    # Но:
    # 1 2 -> 1 2
    #
    # и такое значение будет отклонено.
    normalized = re.sub(
        r"\s*([+-])\s*",
        r"\1",
        value,
    )

    # Обычное действительное число.
    if _REAL_RE.fullmatch(normalized):
        return make_complex(
            real=normalized,
            imag=0,
        )

    # Комплексное число с действительной частью:
    #
    # 3+4i
    # 3-4i
    # 3+i
    # 3-i
    complex_match = _COMPLEX_RE.fullmatch(normalized)

    if complex_match:
        real = complex_match.group("real")
        sign = complex_match.group("sign")
        imag = complex_match.group("imag") or "1"

        if sign == "-":
            imag = f"-{imag}"

        return make_complex(
            real=real,
            imag=imag,
        )

    # Чисто мнимое:
    #
    # i
    # +i
    # -i
    # 5i
    # -5i
    imaginary_match = _IMAGINARY_RE.fullmatch(normalized)

    if imaginary_match:
        sign = imaginary_match.group("sign") or "+"
        imag = imaginary_match.group("imag") or "1"

        if sign == "-":
            imag = f"-{imag}"

        return make_complex(
            real=0,
            imag=imag,
        )

    raise InvalidNumberError(
        f"Некорректное число: {value}"
    )
