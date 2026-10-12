from typing import List, Optional

from .events import Event
from .persons import Person


class Gift:
    """Подарок, связывающий человека и событие."""

    def __init__(
        self,
        gift_id: int,
        person: Person,
        event: Event,
        idea: str,
    ) -> None:
        """Создать объект подарка."""
        self.id = gift_id
        self.person = person
        self.event = event
        self.idea = idea
        self.is_done = False

    def mark_done(self) -> None:
        """Отметить подарок как вручённый."""
        self.is_done = True

    def __str__(self) -> str:
        """Строковое представление подарка."""
        status = "вручён" if self.is_done else "не вручён"
        return (
            f"#{self.id} {self.idea} для {self.person.name} "
            f"к {self.event.title} ({status})"
        )


def add_gift(
    gifts: List[Gift],
    person: Person,
    event: Event,
    idea: str,
) -> Gift:
    """Создать объект Gift и добавить его в коллекцию."""
    new_id = max((g.id for g in gifts), default=0) + 1
    gift = Gift(new_id, person, event, idea)
    gifts.append(gift)
    return gift


def find_gift_by_id(
    gifts: List[Gift],
    gift_id: int,
) -> Optional[Gift]:
    """Найти подарок по идентификатору."""
    for gift in gifts:
        if gift.id == gift_id:
            return gift
    return None


def show_gifts(gifts: List[Gift]) -> None:
    """Вывести список подарков."""
    if not gifts:
        print("Список подарков пуст.")
        return
    for gift in gifts:
        print(gift)
