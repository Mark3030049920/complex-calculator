from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


# ==========================================================
# CONFIGURATION
# ==========================================================

LOCALES_DIR = (
    Path(__file__).resolve().parent
    / "locales"
)

DEFAULT_LANGUAGE = "ru"


# ==========================================================
# VALID LANGUAGE CODE
# ==========================================================

LANGUAGE_CODE_PATTERN = re.compile(
    r"^[a-z]{2,3}(?:-[a-z0-9]{2,8})*$",
    re.IGNORECASE,
)


def _is_valid_language_code(
    language: str,
) -> bool:
    """
    Проверяет, является ли строка нормальным
    кодом языка.

    Разрешены, например:

        ru
        en
        zh
        pt
        pt-br
        zh-hant

    НЕ разрешены:

        ar (1)
        ru (1)
        test
        русский язык
        foo bar
    """

    return bool(
        LANGUAGE_CODE_PATTERN.fullmatch(
            language
        )
    )


# ==========================================================
# LOCALE PATH
# ==========================================================

def _locale_path(
    language: str,
) -> Path:
    """
    Возвращает путь к JSON языка.
    """

    return (
        LOCALES_DIR
        / f"{language}.json"
    )


# ==========================================================
# GET LANGUAGES
# ==========================================================

def get_languages() -> list[str]:
    """
    Возвращает список доступных языков.

    Очень важно:

    приложение НЕ считает файл:

        ar (1).json

    отдельным языком.

    Такие мусорные имена игнорируются.

    Новый нормальный файл:

        it.json

    будет обнаружен без перезапуска программы.
    """

    if not LOCALES_DIR.exists():
        return []


    languages: set[str] = set()


    for path in LOCALES_DIR.glob("*.json"):

        if not path.is_file():
            continue


        code = (
            path.stem
            .strip()
            .lower()
        )


        # ----------------------------------------------
        # Игнорируем неправильные имена файлов
        # ----------------------------------------------

        if not _is_valid_language_code(
            code
        ):
            continue


        languages.add(
            code
        )


    result = sorted(
        languages
    )


    # ==================================================
    # DEFAULT LANGUAGE FIRST
    # ==================================================

    if DEFAULT_LANGUAGE in result:

        result.remove(
            DEFAULT_LANGUAGE
        )

        result.insert(
            0,
            DEFAULT_LANGUAGE
        )


    return result


# ==========================================================
# DEFAULT LANGUAGE
# ==========================================================

def get_default_language() -> str:
    """
    Возвращает язык по умолчанию.

    Если ru.json существует —
    ВСЕГДА используется русский.

    Это важно для тестов и для первого открытия
    приложения.
    """

    languages = get_languages()


    if DEFAULT_LANGUAGE in languages:
        return DEFAULT_LANGUAGE


    # ------------------------------------------------------
    # Если ru пока отсутствует,
    # используем первый доступный язык.
    # ------------------------------------------------------

    if languages:
        return languages[0]


    # ------------------------------------------------------
    # Даже если locales временно пуст,
    # код языка остаётся предсказуемым.
    # ------------------------------------------------------

    return DEFAULT_LANGUAGE


# ==========================================================
# GET TRANSLATION
# ==========================================================

def get_translation(
    language: str,
) -> dict[str, Any]:
    """
    Загружает JSON перевода.

    Каждый запрос читает актуальный файл с диска.

    Поэтому:

        добавили it.json
            ↓
        программа уже работает
            ↓
        it обнаруживается автоматически

    Перезапуск не требуется.
    """

    language = (
        language
        or ""
    ).strip().lower()


    # ==================================================
    # НЕРАЗРЕШЁННЫЙ КОД
    # ==================================================

    if not _is_valid_language_code(
        language
    ):

        language = (
            get_default_language()
        )


    path = _locale_path(
        language
    )


    # ==================================================
    # LANGUAGE NOT FOUND
    # ==================================================

    if not path.is_file():

        path = _locale_path(
            get_default_language()
        )


    # ==================================================
    # EVEN DEFAULT FILE IS MISSING
    # ==================================================

    if not path.is_file():

        return {}


    # ==================================================
    # READ JSON
    # ==================================================

    try:

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(
                file
            )


    except (
        OSError,
        json.JSONDecodeError,
    ):

        return {}


    # ==================================================
    # VALIDATE DATA
    # ==================================================

    if isinstance(
        data,
        dict,
    ):

        return data


    return {}