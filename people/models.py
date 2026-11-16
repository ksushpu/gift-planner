from django.db import models


class Person(models.Model):
    """Человек, для которого планируются подарки."""

    name = models.CharField(
        max_length=200,
        verbose_name="Имя",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Человек"
        verbose_name_plural = "Люди"
