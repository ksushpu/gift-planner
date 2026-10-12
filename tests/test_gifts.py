import datetime

from models import Event, Gift, Person
from models.gifts import add_gift


def _make_event():
    person = Person(1, "Иван")
    event_date = datetime.date(2026, 9, 15)
    return person, Event(1, person, "День рождения", event_date)


def test_gift_creation():
    person, event = _make_event()
    gift = Gift(1, person, event, "Книга")
    assert gift.id == 1
    assert gift.person is person
    assert gift.event is event
    assert gift.idea == "Книга"
    assert gift.is_done is False


def test_gift_mark_done():
    person, event = _make_event()
    gift = Gift(1, person, event, "Книга")
    gift.mark_done()
    assert gift.is_done is True


def test_add_gift():
    person, event = _make_event()
    gifts = []
    add_gift(gifts, person, event, "Книга")
    assert len(gifts) == 1
    assert gifts[0].idea == "Книга"
    assert gifts[0].person.name == "Иван"
    assert gifts[0].event.title == "День рождения"
