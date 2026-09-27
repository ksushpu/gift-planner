import datetime
from typing import List

from .persons import Person


class Event:
    """Событие, связанное с человеком."""

    def __init__(
        self,
        event_id: int,
        person: Person,
        date: datetime.date,
    ) -> None:
        """Создать объект события."""
        self.id = event_id
        self.person = person
        self.date = date

    def days_until(self) -> int:
        """Сколько дней осталось до события."""
        today = datetime.date.today()
        return (self.date - today).days

    def __str__(self) -> str:
        """Строковое представление события."""
        return f"#{self.id} {self.date} — {self.person.name}"


def add_event(
    events: List[Event],
    person: Person,
    date: datetime.date,
) -> Event:
    """Создать объект Event и добавить его в коллекцию."""
    new_id = max((e.id for e in events), default=0) + 1
    event = Event(new_id, person, date)
    events.append(event)
    return event


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
