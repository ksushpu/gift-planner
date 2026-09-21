import datetime
from typing import Any, Dict, List


def add_person(people: List[Dict[str, Any]], name: str) -> None:
    """Добавляет человека в список."""
    people.append({"name": name})
    print(f"Человек '{name}' добавлен.")


def add_event(
    events: List[Dict[str, Any]],
    person_name: str,
    date: datetime.date,
) -> None:
    """Добавляет событие."""
    events.append({"person": person_name, "date": date.isoformat()})
    print(f"Событие для '{person_name}' на {date} добавлено.")


def add_gift_idea(
    gifts: List[Dict[str, Any]],
    person_name: str,
    idea: str,
) -> None:
    """Добавляет идею подарка."""
    gifts.append({"person": person_name, "idea": idea})
    print(f"Идея '{idea}' для '{person_name}' добавлена.")


def find_events_by_person(
    events: List[Dict[str, Any]],
    person_name: str,
) -> List[Dict[str, Any]]:
    """Поиск событий по имени человека."""
    return list(
        filter(
            lambda e: e["person"].lower() == person_name.lower(),
            events,
        )
    )


def sort_events_by_date(
    events: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Сортировка событий по дате."""
    return sorted(events, key=lambda e: e["date"])