import datetime

from django.db import models
from django.db.models.functions import ExtractYear
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode

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
        help_text="Название повода, например день рождения.",
    )
    slug = models.SlugField(
        max_length=180,
        unique=True,
        blank=True,
        verbose_name="URL-идентификатор",
        help_text="Заполняется автоматически из названия.",
    )
    date = models.DateField(
        verbose_name="Дата",
        help_text="Дата события в формате ГГГГ-ММ-ДД.",
    )
    event_year = models.GeneratedField(
        expression=ExtractYear("date"),
        output_field=models.IntegerField(),
        db_persist=True,
        verbose_name="Год события",
    )

    def save(self, *args, **kwargs):
        """Сохранить событие и при необходимости заполнить slug."""
        if not self.slug and self.pk:
            self.slug = self._build_slug()
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = self._build_slug()
            super().save(update_fields=["slug"])

    def _build_slug(self) -> str:
        base = slugify(unidecode(self.title)) or "event"
        return f"{base}-{self.pk}"

    def get_absolute_url(self):
        """Адрес страницы события."""
        return reverse("events:detail", kwargs={"event_slug": self.slug})

    def days_until(self) -> int:
        """Сколько дней осталось до события."""
        return (self.date - datetime.date.today()).days

    def __str__(self) -> str:
        return f"{self.title} ({self.date}) — {self.person.name}"

    class Meta:
        ordering = ["date", "pk"]
        verbose_name = "Событие"
        verbose_name_plural = "События"
