from flask import (
    Flask,
    jsonify,
    render_template,
    request,
)

from calculator.i18n import (
    get_default_language,
    get_languages,
    get_translation,
)

from calculator.core import (
    CalculatorError,
    InvalidNumberError,
    InvalidPrecisionError,
)

from calculator.service import (
    calculate_from_parts,
    calculate_trigonometric,
)


app = Flask(__name__)

@app.route("/support")
def support():
    return render_template("support.html")


DEFAULT_MESSAGES = {
    "empty_number": (
        "Введите действительную или мнимую часть числа."
    ),
    "invalid_number": (
        "Введите корректное число."
    ),
    "invalid_precision": (
        "Точность должна быть целым числом."
    ),
    "invalid_display_digits": (
        "Количество отображаемых знаков должно быть целым числом."
    ),
    "calculation_error": (
        "Во время вычисления произошла ошибка."
    ),
}


VALID_TABS = {
    "root",
    "trig",
}


def translate(
    translations: dict,
    key: str,
    default: str = "",
) -> str:
    """
    Получает перевод по ключу.
    Если перевода нет — используется fallback.
    """

    value = translations.get(key)

    if isinstance(value, str) and value.strip():
        return value

    return (
        default
        or DEFAULT_MESSAGES.get(
            key,
            key,
        )
    )


def normalize_tab(
    value: str | None,
) -> str:
    """
    Разрешённые вкладки приложения.
    """

    if value in VALID_TABS:
        return value

    return "root"


def get_language() -> str:
    """
    Определяет текущий язык.

    GET:
        /?lang=en

    POST:
        hidden input name="lang"

    Новый язык определяется динамически
    из папки locales.
    """

    requested = (
        request.args.get(
            "lang",
            "",
        )
        or request.form.get(
            "lang",
            "",
        )
    )

    requested = (
        requested
        .strip()
        .lower()
    )

    languages = get_languages()

    if requested in languages:
        return requested

    return get_default_language()


def build_language_info(
    languages: list[str],
) -> list[dict]:
    """
    Формирует информацию для переключателя языка.
    """

    result = []

    for code in languages:

        translation = get_translation(
            code
        )

        native_name = translation.get(
            "native_name",
            code,
        )

        if (
            not isinstance(
                native_name,
                str,
            )
            or not native_name.strip()
        ):
            native_name = code

        result.append(
            {
                "code": code,
                "native_name": native_name,
            }
        )

    return result


# ==========================================================
# API: LANGUAGES
# ==========================================================

@app.get("/api/languages")
def api_languages():
    """
    Возвращает актуальный список языков.

    Новый JSON-файл будет найден без перезапуска.
    """

    languages = get_languages()

    return jsonify(
        build_language_info(
            languages
        )
    )


# ==========================================================
# API: TRANSLATION
# ==========================================================

@app.get(
    "/api/translations/<language>"
)
def api_translation(
    language: str,
):
    """
    Возвращает перевод выбранного языка.
    """

    language = (
        language
        .strip()
        .lower()
    )

    if language not in get_languages():

        return jsonify(
            {
                "error": "Language not found."
            }
        ), 404

    return jsonify(
        get_translation(
            language
        )
    )


# ==========================================================
# MAIN PAGE
# ==========================================================

@app.route(
    "/",
    methods=[
        "GET",
        "POST",
    ],
)
def index():

    # ------------------------------------------------------
    # LANGUAGE
    # ------------------------------------------------------

    language = get_language()

    translations = get_translation(
        language
    )

    languages = get_languages()

    language_info = (
        build_language_info(
            languages
        )
    )


    # ------------------------------------------------------
    # DEFAULT FORM VALUES
    # ------------------------------------------------------

    real = ""
    imag = ""

    precision = "50"
    display_digits = "10"


    # ------------------------------------------------------
    # ROOT RESULTS
    # ------------------------------------------------------

    root1 = None
    root2 = None


    # ------------------------------------------------------
    # TRIG RESULTS
    # ------------------------------------------------------

    trig_value = ""

    trig_degrees = False

    trig_radius = None
    trig_angle = None

    trig_formula = None
    trig_substitution = None


    # ------------------------------------------------------
    # ERROR
    # ------------------------------------------------------

    error_key = None


    # ------------------------------------------------------
    # ACTIVE TAB
    # ------------------------------------------------------

    active_tab = normalize_tab(
        request.args.get(
            "active_tab"
        )
        or request.form.get(
            "active_tab"
        )
    )


    # ======================================================
    # POST
    # ======================================================

    if request.method == "POST":

        precision = request.form.get(
            "precision",
            "50",
        )

        display_digits = request.form.get(
            "display_digits",
            "10",
        )


        # ==================================================
        # ROOT
        # ==================================================

        if active_tab == "root":

            real = request.form.get(
                "real",
                "",
            )

            imag = request.form.get(
                "imag",
                "",
            )


            # ----------------------------------------------
            # EMPTY NUMBER
            # ----------------------------------------------

            if (
                not real.strip()
                and not imag.strip()
            ):

                error_key = (
                    "empty_number"
                )

            else:

                # ------------------------------------------
                # PRECISION
                # ------------------------------------------

                try:

                    precision_value = int(
                        precision
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    precision_value = None


                # ------------------------------------------
                # DISPLAY DIGITS
                # ------------------------------------------

                try:

                    display_digits_value = int(
                        display_digits
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    display_digits_value = None


                try:

                    # --------------------------------------
                    # INVALID PRECISION
                    # --------------------------------------

                    if precision_value is None:

                        raise InvalidPrecisionError()


                    # --------------------------------------
                    # INVALID DISPLAY DIGITS
                    # --------------------------------------

                    if display_digits_value is None:

                        error_key = (
                            "invalid_display_digits"
                        )

                    else:

                        # ----------------------------------
                        # CALCULATION
                        # ----------------------------------

                        (
                            root1,
                            root2,
                        ) = calculate_from_parts(

                            real.strip(),
                            imag.strip(),

                            precision=(
                                precision_value
                            ),

                            display_digits=(
                                display_digits_value
                            ),
                        )


                except InvalidNumberError:

                    error_key = (
                        "invalid_number"
                    )


                except InvalidPrecisionError:

                    error_key = (
                        "invalid_precision"
                    )


                except CalculatorError:

                    error_key = (
                        "calculation_error"
                    )


                except ValueError:

                    error_key = (
                        "invalid_number"
                    )


                except Exception:

                    error_key = (
                        "calculation_error"
                    )


        # ==================================================
        # TRIGONOMETRY
        # ==================================================

        elif active_tab == "trig":

            trig_value = request.form.get(
                "trig_value",
                "",
            ).strip()


            trig_degrees = (
                request.form.get(
                    "angle_unit",
                    "rad",
                )
                == "deg"
            )


            # ----------------------------------------------
            # EMPTY VALUE
            # ----------------------------------------------

            if not trig_value:

                error_key = (
                    "empty_number"
                )

            else:

                # ------------------------------------------
                # PRECISION
                # ------------------------------------------

                try:

                    precision_value = int(
                        precision
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    precision_value = None


                # ------------------------------------------
                # DISPLAY DIGITS
                # ------------------------------------------

                try:

                    display_digits_value = int(
                        display_digits
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    display_digits_value = None


                try:

                    # --------------------------------------
                    # INVALID PRECISION
                    # --------------------------------------

                    if precision_value is None:

                        raise InvalidPrecisionError()


                    # --------------------------------------
                    # INVALID DISPLAY DIGITS
                    # --------------------------------------

                    if display_digits_value is None:

                        error_key = (
                            "invalid_display_digits"
                        )

                    else:

                        # ----------------------------------
                        # CALCULATION
                        # ----------------------------------

                        trig_result = (
                            calculate_trigonometric(

                                trig_value,

                                precision=(
                                    precision_value
                                ),

                                degrees=(
                                    trig_degrees
                                ),

                                display_digits=(
                                    display_digits_value
                                ),
                            )
                        )


                        trig_radius = (
                            trig_result["radius"]
                        )

                        trig_angle = (
                            trig_result["angle"]
                        )

                        trig_formula = (
                            trig_result["formula"]
                        )

                        trig_substitution = (
                            trig_result.get(
                                "substitution"
                            )
                        )


                except InvalidNumberError:

                    error_key = (
                        "invalid_number"
                    )


                except InvalidPrecisionError:

                    error_key = (
                        "invalid_precision"
                    )


                except CalculatorError:

                    error_key = (
                        "calculation_error"
                    )


                except ValueError:

                    error_key = (
                        "invalid_number"
                    )


                except Exception:

                    error_key = (
                        "calculation_error"
                    )


    # ======================================================
    # TRANSLATE ERROR
    # ======================================================

    error = None

    if error_key:

        error = translate(
            translations,
            error_key,
        )


    # ======================================================
    # RENDER
    # ======================================================

    return render_template(

        "index.html",

        language=language,

        languages=languages,

        language_info=language_info,

        translations=translations,


        real=real,

        imag=imag,

        precision=precision,

        display_digits=display_digits,


        root1=root1,

        root2=root2,


        trig_value=trig_value,

        trig_degrees=trig_degrees,

        trig_radius=trig_radius,

        trig_angle=trig_angle,

        trig_formula=trig_formula,

        trig_substitution=(
            trig_substitution
        ),


        active_tab=active_tab,

        error=error,
    )


# ==========================================================
# START
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )