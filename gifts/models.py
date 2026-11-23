from django.db import models

from events.models import Event
from people.models import Person


class GiftQuerySet(models.QuerySet):
    """Выборки подарков по статусу."""

    def planned(self):
        return self.filter(status=Gift.Status.PLANNED)

    def given(self):
        return self.filter(status=Gift.Status.GIVEN)

    def cancelled(self):
        return self.filter(status=Gift.Status.CANCELLED)


class Gift(models.Model):
    """Подарок, связывающий человека и событие."""

    class Status(models.TextChoices):
        PLANNED = "planned", "Запланирован"
        GIVEN = "given", "Вручён"
        CANCELLED = "cancelled", "Отменён"

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
        help_text="Кратко опишите, что планируется подарить.",
    )
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.PLANNED,
        verbose_name="Статус",
        help_text="Запланированный подарок ещё не вручён.",
    )
    objects = GiftQuerySet.as_manager()

    def mark_done(self) -> None:
        """Отметить подарок как вручённый."""
        self.status = self.Status.GIVEN
        self.save(update_fields=["status"])

    def __str__(self) -> str:
        status = self.get_status_display()
        return (
            f"{self.idea} для {self.person.name} "
            f"к {self.event.title} ({status})"
        )

    class Meta:
        ordering = ["pk"]
        verbose_name = "Подарок"
        verbose_name_plural = "Подарки"
