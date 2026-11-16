import datetime

from django.db import models

from people.models import Person


class Event(models.Model):
    """Событие, связанное с человеком."""

    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name="events",
        verbose_name="Человек",
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    date = models.DateField(
        verbose_name="Дата",
    )

    def days_until(self) -> int:
        """Сколько дней осталось до события."""
        return (self.date - datetime.date.today()).days

    def __str__(self) -> str:
        return f"{self.title} ({self.date}) — {self.person.name}"

    class Meta:
        ordering = ["date", "pk"]
        verbose_name = "Событие"
        verbose_name_plural = "События"
