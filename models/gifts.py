from typing import List

from .persons import Person


class Gift:
    """Идея подарка для человека."""

    def __init__(
        self,
        gift_id: int,
        person: Person,
        idea: str,
    ) -> None:
        """Создать объект подарка."""
        self.id = gift_id
        self.person = person
        self.idea = idea
        self.is_done = False

    def mark_done(self) -> None:
        """Отметить подарок как вручённый."""
        self.is_done = True

    def __str__(self) -> str:
        """Строковое представление подарка."""
        status = "вручён" if self.is_done else "не вручён"
        return f"#{self.id} {self.idea} для {self.person.name} ({status})"


def add_gift(
    gifts: List[Gift],
    person: Person,
    idea: str,
) -> Gift:
    """Создать объект Gift и добавить его в коллекцию."""
    new_id = max((g.id for g in gifts), default=0) + 1
    gift = Gift(new_id, person, idea)
    gifts.append(gift)
    return gift


def show_gifts(gifts: List[Gift]) -> None:
    """Вывести список подарков."""
    if not gifts:
        print("Список подарков пуст.")
        return
    for gift in gifts:
        print(gift)
