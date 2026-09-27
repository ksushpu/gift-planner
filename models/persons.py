from typing import List, Optional


class Person:
    """Человек, для которого планируются подарки."""

    def __init__(self, person_id: int, name: str) -> None:
        """Создать объект человека."""
        self.id = person_id
        self.name = name

    def __str__(self) -> str:
        """Строковое представление человека."""
        return f"#{self.id} {self.name}"


def add_person(persons: List[Person], name: str) -> Person:
    """Создать объект Person и добавить его в коллекцию."""
    new_id = max((p.id for p in persons), default=0) + 1
    person = Person(new_id, name)
    persons.append(person)
    return person


def find_person_by_id(
    persons: List[Person],
    person_id: int,
) -> Optional[Person]:
    """Найти человека по идентификатору."""
    for person in persons:
        if person.id == person_id:
            return person
    return None


def find_persons_by_name(
    persons: List[Person],
    query: str,
) -> List[Person]:
    """Найти людей по подстроке имени."""
    return [p for p in persons if query.lower() in p.name.lower()]


def show_persons(persons: List[Person]) -> None:
    """Вывести список людей."""
    if not persons:
        print("Список людей пуст.")
        return
    for person in persons:
        print(person)
