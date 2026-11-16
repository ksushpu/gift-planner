from django.db import models

from events.models import Event
from people.models import Person


class Gift(models.Model):
    """Подарок, связывающий человека и событие."""

    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name="gifts",
        verbose_name="Человек",
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.PROTECT,
        related_name="gifts",
        verbose_name="Событие",
    )
    idea = models.CharField(
        max_length=300,
        verbose_name="Идея подарка",
    )
    is_done = models.BooleanField(
        default=False,
        verbose_name="Вручён",
    )

    def mark_done(self) -> None:
        """Отметить подарок как вручённый."""
        self.is_done = True
        self.save(update_fields=["is_done"])

    def __str__(self) -> str:
        status = "вручён" if self.is_done else "не вручён"
        return (
            f"{self.idea} для {self.person.name} "
            f"к {self.event.title} ({status})"
        )

    class Meta:
        ordering = ["pk"]
        verbose_name = "Подарок"
        verbose_name_plural = "Подарки"
