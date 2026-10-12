import datetime

from models import Event, Person
from models.events import add_event, sort_events_by_date


def test_event_creation():
    person = Person(1, "Иван")
    event_date = datetime.date(2026, 9, 15)
    event = Event(1, person, "День рождения", event_date)
    assert event.id == 1
    assert event.person is person
    assert event.title == "День рождения"
    assert event.date == event_date


def test_add_event():
    persons = [Person(1, "Иван")]
    events = []
    add_event(
        events,
        persons[0],
        "День рождения",
        datetime.date(2026, 9, 15),
    )
    assert len(events) == 1
    assert events[0].title == "День рождения"


def test_sort_events_by_date():
    person = Person(1, "Иван")
    events = [
        Event(1, person, "Новый год",
              datetime.date(2026, 12, 31)),
        Event(2, person, "День рождения",
              datetime.date(2026, 1, 1)),
    ]
    sorted_events = sort_events_by_date(events)
    assert sorted_events[0].id == 2
    assert sorted_events[1].id == 1
