import datetime
from typing import List, Optional

from .persons import Person


class Event:
    """Событие, связанное с человеком."""

    def __init__(
        self,
        event_id: int,
        person: Person,
        title: str,
        date: datetime.date,
    ) -> None:
        """Создать объект события."""
        self.id = event_id
        self.person = person
        self.title = title
        self.date = date

    def days_until(self) -> int:
        """Сколько дней осталось до события."""
        today = datetime.date.today()
        return (self.date - today).days

    def __str__(self) -> str:
        """Строковое представление события."""
        return f"#{self.id} {self.title} ({self.date}) — {self.person.name}"


def add_event(
    events: List[Event],
    person: Person,
    title: str,
    date: datetime.date,
) -> Event:
    """Создать объект Event и добавить его в коллекцию."""
    new_id = max((e.id for e in events), default=0) + 1
    event = Event(new_id, person, title, date)
    events.append(event)
    return event


def find_event_by_id(
    events: List[Event],
    event_id: int,
) -> Optional[Event]:
    """Найти событие по идентификатору."""
    for event in events:
        if event.id == event_id:
            return event
    return None


def sort_events_by_date(events: List[Event]) -> List[Event]:
    """Отсортировать события по дате."""
    return sorted(events, key=lambda e: e.date)


def show_events(events: List[Event]) -> None:
    """Вывести список событий, отсортированных по дате."""
    if not events:
        print("Список событий пуст.")
        return
    for event in sort_events_by_date(events):
        print(event)
