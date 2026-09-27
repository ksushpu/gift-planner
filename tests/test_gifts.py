from models import Gift, Person
from models.gifts import add_gift


def test_gift_creation():
    person = Person(1, "Иван")
    gift = Gift(1, person, "Книга")
    assert gift.id == 1
    assert gift.person is person
    assert gift.idea == "Книга"
    assert gift.is_done is False


def test_gift_mark_done():
    person = Person(1, "Иван")
    gift = Gift(1, person, "Книга")
    gift.mark_done()
    assert gift.is_done is True


def test_add_gift():
    persons = [Person(1, "Иван")]
    gifts = []
    add_gift(gifts, persons[0], "Книга")
    assert len(gifts) == 1
    assert gifts[0].idea == "Книга"
    assert gifts[0].person.name == "Иван"
