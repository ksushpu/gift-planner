import datetime
from logic import add_person, add_event, sort_events_by_date


def test_add_person():
    people = []
    add_person(people, "Иван")
    assert len(people) == 1
    assert people[0]["name"] == "Иван"


def test_add_event():
    events = []
    date = datetime.date(2026, 9, 15)
    add_event(events, "Иван", date)
    assert len(events) == 1
    assert events[0]["person"] == "Иван"
    assert events[0]["date"] == "2026-09-15"


def test_sort_events_by_date():
    events = [
        {"person": "А", "date": "2026-12-01"},
        {"person": "Б", "date": "2026-01-01"}
    ]
    sorted_events = sort_events_by_date(events)
    assert sorted_events[0]["person"] == "Б"
    assert sorted_events[1]["person"] == "А"