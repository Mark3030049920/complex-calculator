Комплексный Калькулятор

Данный проект представляет собой веб-приложение на базе **Flask**, предназначенное для высокоточных вычислений с комплексными числами (извлечение квадратного корня, представление чисел в точной алгебраической и тригонометрической формах, динамическая локализация).

---

## Структура продукта

Проект имеет слоистую архитектуру с чётким разделением ответственности между модулями:

* **`app.py`** — **Слой представления и HTTP API.** Выполняет роль контроллера Flask[cite: 16]. Обрабатывает веб-маршруты, управление сессией/языком и API-эндпоинты[cite: 16].
* **`service.py`** — **Сервисный слой (оркестрация).** Принимает и валидирует пользовательские параметры, координирует работу парсера, вычислительного ядра и форматирования[cite: 14].
* **`core.py`** — **Вычислительное ядро.** Содержит основные структуры данных (`ComplexNumber`, `SquareRootResult`), алгоритмы извлечения корней и пользовательские исключения[cite: 10].
* **`trigonometry.py`** — **Модуль тригонометрии.** Ответственен за конвертацию чисел в тригонометрическую форму, работу с углами и представлением через коэффициенты $\pi$[cite: 15].
* **`parser.py`** — **Парсер ввода.** Преобразует строковые представления чисел в внутренние объекты `ComplexNumber`[cite: 13].
* **`formatter.py`** — **Модуль форматирования.** Отвечает за представление результатов вычислений в понятном человеку виде (включая упрощение радикалов)[cite: 11].
* **`i18n.py`** — **Модуль интернационализации.** Обеспечивает считывание и валидацию файлов локализации[cite: 12].
* **`__init__.py`** — **Инициализация пакета.** Экспортирует ключевые функции тригонометрического модуля для использования снаружи[cite: 9].

---

## Основные технические решения

1. **Библиотека `mpmath` для длинной арифметики**
   * Вместо стандартных типов `float` или `complex` (ограниченных 64-битным плавающим точечным стандартом IEEE 754), вычисления проводятся с использованием `mpmath`[cite: 10]. Это позволяет рассчитывать значения с произвольной точностью (до 10 000 знаков)[cite: 10].
2. **Аналитический метод вычисления квадратного корня**
   * Для нахождения корня из комплексного числа $z = a + bi$ используется аналитическая формула с учётом знака действительной части $a$, что предотвращает потерю точности при делении на близкие к нулю величины[cite: 10]:
     $$\text{Re}(\sqrt{z}) = \sqrt{\frac{\vert{}z\vert{} + a}{2}}, \quad \text{Im}(\sqrt{z}) = \text{sign}(b) \sqrt{\frac{\vert{}z\vert{} - a}{2}}$$
3. **Динамическая загрузка локализаций (Hot-Reloading)**
   * Переводы считываются напрямую из `.json` файлов в директории `locales/` при каждом запросе без необходимости перезапуска приложения[cite: 12]. Некорректные или повреждённые имена файлов отсеиваются регулярными выражениями[cite: 12].
4. **Упрощение радикалов (Exact Algebraic Form)**
   * Для целых чисел реализован алгоритм вынесения полного квадрата из-под знака корня (например, $\sqrt{18} \to 3\sqrt{2}$) с помощью функции `_simplify_square_root`[cite: 11].

---

## Особенности реализации

* **Защита от сбоев и переполнения (Input Validation):**
  * Введён жесткий лимит на длину входных строк (`MAX_INPUT_DIGITS = 100 000`), предотвращающий ReDoS и сбои при обработке гигантских чисел[cite: 10].
  * Автоматический расчёт рабочей точности: внутреннее число знаков `working_precision` динамически увеличивается относительно запрошенного пользователем `precision`, чтобы избежать накопительной погрешности `mpmath` при промежуточных операциях[cite: 10].
* **Парсинг чисел с высокой гибкостью:**
  * Поддерживаются различные текстовые представления: обычные числа, числа с плавающей точкой, экспоненциальная запись (`1e3`), чисто мнимая форма (`-5i`) и комплексная (`3+4i`, `3-i`)[cite: 13].
* **Представление углов через $\pi$:**
  * Алгоритм на основе `mp.pslq` пытается найти рациональное отношение угла к $\pi$, приводя значения вида `1.57079...` к красивой математической форме $\pi/2$ или $3\pi/4$[cite: 15].

---



# Project Documentation: Complex Calculator

This project is a **Flask**-based web application designed for high-precision calculations with complex numbers (extracting square roots, representing numbers in exact algebraic and trigonometric forms, and dynamic localization).

---

## Product Structure

The project follows a layered architecture with a clear separation of concerns between modules:

* **`app.py`** — **Presentation Layer and HTTP API.** Acts as the Flask controller[cite: 16]. Handles web routes, session/language management, and API endpoints[cite: 16].
* **`service.py`** — **Service Layer (Orchestration).** Accepts and validates user parameters, coordinating the parser, computational core, and formatting modules[cite: 14].
* **`core.py`** — **Computational Core.** Contains the primary data structures (`ComplexNumber`, `SquareRootResult`), root-extraction algorithms, and custom exceptions[cite: 10].
* **`trigonometry.py`** — **Trigonometry Module.** Handles conversion of numbers into trigonometric form, angle manipulation, and representation using $\pi$ coefficients[cite: 15].
* **`parser.py`** — **Input Parser.** Converts string representations of numbers into internal `ComplexNumber` objects[cite: 13].
* **`formatter.py`** — **Formatting Module.** Formats calculation results into human-readable text (including radical simplification)[cite: 11].
* **`i18n.py`** — **Internationalization Module.** Manages reading and validating localization files[cite: 12].
* **`__init__.py`** — **Package Initialization.** Exports key functions from the trigonometry module for external use[cite: 9].

---

## Key Technical Decisions

1. **`mpmath` Library for Arbitrary-Precision Arithmetic**
   * Instead of standard `float` or `complex` types (which are limited by the 64-bit IEEE 754 floating-point standard), calculations are performed using `mpmath`[cite: 10]. This enables calculations with arbitrary precision (up to 10,000 digits)[cite: 10].
2. **Analytic Method for Square Root Calculation**
   * To find the square root of a complex number $z = a + bi$, an analytic formula accounting for the sign of the real part $a$ is used, preventing precision loss caused by division by near-zero values[cite: 10]:
     $$\text{Re}(\sqrt{z}) = \sqrt{\frac{\vert{}z\vert{} + a}{2}}, \quad \text{Im}(\sqrt{z}) = \text{sign}(b) \sqrt{\frac{\vert{}z\vert{} - a}{2}}$$
3. **Dynamic Localization Loading (Hot-Reloading)**
   * Translations are read directly from `.json` files in the `locales/` directory upon each request without requiring a server restart[cite: 12]. Invalid or corrupted filenames are filtered out using regular expressions[cite: 12].
4. **Radical Simplification (Exact Algebraic Form)**
   * For integer values, an algorithm extracts perfect squares from under the radical sign (e.g., $\sqrt{18} \to 3\sqrt{2}$) using the `_simplify_square_root` function[cite: 11].

---

## Implementation Details

* **Input Validation & Fault Tolerance:**
  * Enforces a strict limit on input string length (`MAX_INPUT_DIGITS = 100,000`), preventing ReDoS attacks and crashes when handling gigantic numbers[cite: 10].
  * Automatic working precision calculation: the internal precision `working_precision` dynamically scales relative to the user's requested `precision` to eliminate cumulative rounding errors in intermediate `mpmath` operations[cite: 10].
* **Flexible Number Parsing:**
  * Supports various text formats: standard integers, floating-point numbers, exponential notation (`1e3`), purely imaginary numbers (`-5i`), and complex forms (`3+4i`, `3-i`)[cite: 13].
* **Angle Representation via $\pi$:**
  * An algorithm based on `mp.pslq` attempts to find rational ratios between the angle and $\pi$, converting values like `1.57079...` into exact mathematical expressions such as $\pi/2$ or $3\pi/4$[cite: 15].






