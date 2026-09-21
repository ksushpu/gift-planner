import datetime


def input_int(prompt: str) -> int:
    """Запрашивает целое число, обрабатывая ошибки ввода."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def input_date(prompt: str) -> datetime.date:
    """Запрашивает дату в формате ГГГГ-ММ-ДД."""
    while True:
        date_str = input(prompt)
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Ошибка: неверный формат даты.")
            print("Попробуйте снова (ГГГГ-ММ-ДД).")