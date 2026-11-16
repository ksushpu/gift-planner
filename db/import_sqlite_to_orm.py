import os
import sys
import sqlite3
from datetime import date
from pathlib import Path

import django
from django.db import transaction

# Определяем корневой каталог проекта Gift Planner.
BASE_DIR = Path(__file__).resolve().parent.parent

# Добавляем корень проекта в пути поиска модулей Python.
sys.path.insert(0, str(BASE_DIR))

# Указываем путь к исходной базе данных.
SOURCE_DB = BASE_DIR / "data" / "gift_planner.sqlite"

# Указываем модуль настроек Django.
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "giftplanner.settings",
)

# Инициализируем Django после настройки пути и переменной окружения.
django.setup()

# Импортируем модели только после инициализации Django.
from events.models import Event  # noqa: E402
from gifts.models import Gift  # noqa: E402
from people.models import Person  # noqa: E402


def main():
    # Проверяем, что исходная база существует.
    if not SOURCE_DB.exists():
        raise FileNotFoundError(
            f"Исходная база не найдена: {SOURCE_DB}"
        )

    # Открываем исходную базу для чтения.
    with sqlite3.connect(SOURCE_DB) as connection:
        connection.row_factory = sqlite3.Row

        # Считываем всех людей, сохраняя их идентификаторы.
        people = connection.execute(
            """
            SELECT id, name
            FROM people
            ORDER BY id
            """
        ).fetchall()

        # Считываем события и их идентификаторы.
        events = connection.execute(
            """
            SELECT id, person_id, title, date
            FROM events
            ORDER BY id
            """
        ).fetchall()

        # Считываем подарки вместе с внешними ключами.
        gifts = connection.execute(
            """
            SELECT
                id,
                person_id,
                event_id,
                idea,
                is_done
            FROM gifts
            ORDER BY id
            """
        ).fetchall()

        # Выполняем запись в целевую базу одной транзакцией.
        with transaction.atomic():

            # Сначала переносим людей: на них ссылаются события и подарки.
            for row in people:
                Person.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "name": row["name"],
                    },
                )

            # Затем переносим события.
            for row in events:
                event_date = date.fromisoformat(row["date"])
                Event.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "person_id": row["person_id"],
                        "title": row["title"],
                        "date": event_date,
                    },
                )

            # После людей и событий переносим подарки.
            for row in gifts:
                Gift.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "person_id": row["person_id"],
                        "event_id": row["event_id"],
                        "idea": row["idea"],
                        "is_done": bool(row["is_done"]),
                    },
                )

    print("Перенос данных завершён.")
    print(f"Людей: {Person.objects.count()}")
    print(f"Событий: {Event.objects.count()}")
    print(f"Подарков: {Gift.objects.count()}")


if __name__ == "__main__":
    main()
