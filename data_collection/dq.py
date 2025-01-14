import re

def validate_dataframe(df, rules):
    report = []

    for column, checks in rules.items():
        if column not in df.columns:
            report.append(f"Колонка {column} отсутствует в данных")
            continue

        # Проверка на уникальность
        if checks.get("unique") and not df[column].is_unique:
            report.append(f"Колонка {column} содержит дубликаты")

        # Проверка на заполненность
        if checks.get("not_null") and df[column].isnull().any():
            report.append(f"Колонка {column} содержит пустые значения")

        # Проверка диапазона значений
        if "range" in checks:
            min_val, max_val = checks["range"]
            if not df[column].dropna().between(min_val, max_val).all():
                report.append(f"Колонка {column} содержит значения вне диапазона {min_val}-{max_val}")

        # Проверка типа данных
        if "type" in checks:
            expected_type = checks["type"]
            if not df[column].dropna().apply(lambda x: isinstance(x, expected_type)).all():
                report.append(f"Колонка {column} содержит значения, которые не соответствуют типу {expected_type}")

        # Проверка длины строки
        if "max_length" in checks:
            max_length = checks["max_length"]
            if df[column].dropna().apply(lambda x: len(str(x)) > max_length).any():
                report.append(f"Колонка {column} содержит строки длиной больше {max_length} символов")

        # Проверка формата URL
        if checks.get("is_url"):
            url_pattern = re.compile(r'^(http|https)://')
            if not df[column].dropna().apply(lambda x: bool(url_pattern.match(str(x)))).all():
                report.append(f"Колонка {column} содержит некорректные URL")

    return report

# Применение проверок
report = validate_dataframe(df, rules)

# Вывод отчёта
if report:
    print("Обнаружены проблемы:")
    for issue in report:
        print(f" - {issue}")
else:
    print("Все данные корректны!")
