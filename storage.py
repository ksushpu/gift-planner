import datetime
import json
import os
from typing import List

from models import Event, Gift, Person
from models.persons import find_person_by_id

DATA_DIR = "data"


def ensure_data_dir() -> None:
    """Создать папку data, если её нет."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def _load_raw(filename: str) -> list:
    """Прочитать сырые данные из JSON-файла."""
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print(f"Ошибка чтения {filename}.")
        return []


def _save_raw(filename: str, data: list) -> None:
    """Записать данные в JSON-файл."""
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except IOError:
        print(f"Ошибка записи в {filename}.")


# --- Люди ---

def load_persons(filename: str = "people.json") -> List[Person]:
    """Загрузить людей из JSON и создать объекты Person."""
    raw = _load_raw(filename)
    return [Person(item["id"], item["name"]) for item in raw]


def save_persons(persons: List[Person],
                 filename: str = "people.json") -> None:
    """Сохранить объекты Person в JSON."""
    data = [{"id": p.id, "name": p.name} for p in persons]
    _save_raw(filename, data)


# --- События ---

def load_events(
    persons: List[Person],
    filename: str = "events.json",
) -> List[Event]:
    """Загрузить события и связать их с объектами Person."""
    raw = _load_raw(filename)
    events: List[Event] = []
    for item in raw:
        person = find_person_by_id(persons, item["person_id"])
        if person is None:
            continue
        event_date = datetime.date.fromisoformat(item["date"])
        events.append(Event(item["id"], person, event_date))
    return events


def save_events(events: List[Event],
                filename: str = "events.json") -> None:
    """Сохранить объекты Event в JSON."""
    data = [
        {
            "id": e.id,
            "person_id": e.person.id,
            "date": e.date.isoformat(),
        }
        for e in events
    ]
    _save_raw(filename, data)


# --- Подарки ---

def load_gifts(
    persons: List[Person],
    filename: str = "gifts.json",
) -> List[Gift]:
    """Загрузить подарки и связать их с объектами Person."""
    raw = _load_raw(filename)
    gifts: List[Gift] = []
    for item in raw:
        person = find_person_by_id(persons, item["person_id"])
        if person is None:
            continue
        gift = Gift(item["id"], person, item["idea"])
        gift.is_done = item.get("is_done", False)
        gifts.append(gift)
    return gifts


def save_gifts(gifts: List[Gift],
               filename: str = "gifts.json") -> None:
    """Сохранить объекты Gift в JSON."""
    data = [
        {
            "id": g.id,
            "person_id": g.person.id,
            "idea": g.idea,
            "is_done": g.is_done,
        }
        for g in gifts
    ]
    _save_raw(filename, data)
