from models import Person
from models.persons import add_person, find_person_by_id


def test_person_creation():
    person = Person(1, "Иван")
    assert person.id == 1
    assert person.name == "Иван"


def test_person_str():
    person = Person(1, "Иван")
    assert str(person) == "#1 Иван"


def test_add_person():
    persons = []
    add_person(persons, "Иван")
    assert len(persons) == 1
    assert persons[0].name == "Иван"


def test_find_person_by_id():
    persons = [Person(1, "Иван"), Person(2, "Мария")]
    found = find_person_by_id(persons, 2)
    assert found is not None
    assert found.name == "Мария"


def test_find_person_by_id_not_found():
    persons = [Person(1, "Иван")]
    assert find_person_by_id(persons, 99) is None
