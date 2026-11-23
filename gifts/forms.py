from django import forms
from django.utils import timezone

from events.models import Event
from people.models import Person

from .models import Gift


class GiftFilterForm(forms.Form):
    """Фильтры списка подарков. Данные приходят через GET."""

    q = forms.CharField(
        required=False,
        label="Поиск",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Идея или имя",
        }),
    )
    person = forms.ModelChoiceField(
        queryset=Person.objects.order_by("name"),
        required=False,
        label="Человек",
        empty_label="Все люди",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    event = forms.ModelChoiceField(
        queryset=Event.objects.order_by("title"),
        required=False,
        label="Событие",
        empty_label="Все события",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    status = forms.ChoiceField(
        required=False,
        label="Статус",
        choices=(
            ("", "Все"),
            ("pending", "Запланирован"),
            ("done", "Вручён"),
            ("cancelled", "Отменён"),
        ),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    sort = forms.ChoiceField(
        required=False,
        label="Сортировать по",
        choices=(
            ("id", "ID"),
            ("idea", "Идее"),
            ("person", "Человеку"),
            ("event", "Событию"),
        ),
        initial="id",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def clean(self):
        cleaned = super().clean()
        person = cleaned.get("person")
        event = cleaned.get("event")
        if person and event and event.person_id != person.pk:
            self.add_error(
                "event",
                "Это событие относится к другому человеку.",
            )
        return cleaned


class GiftForm(forms.ModelForm):
    """Создание и редактирование подарка."""

    class Meta:
        model = Gift
        fields = ("person", "event", "idea", "status")
        widgets = {
            "person": forms.Select(attrs={"class": "form-select"}),
            "event": forms.Select(attrs={"class": "form-select"}),
            "idea": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Что подарить",
            }),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_idea(self):
        idea = (self.cleaned_data.get("idea") or "").strip()
        if len(idea) < 3:
            raise forms.ValidationError(
                "Опишите идею хотя бы тремя символами."
            )
        return idea

    def clean_event(self):
        event = self.cleaned_data.get("event")
        if event and not self.instance.pk and event.date < timezone.localdate():
            raise forms.ValidationError(
                "Нельзя планировать подарок к прошедшему событию."
            )
        return event

    def clean(self):
        cleaned = super().clean()
        person = cleaned.get("person")
        event = cleaned.get("event")
        status = cleaned.get("status")
        if person and event and event.person_id != person.pk:
            self.add_error(
                "person",
                "Выберите человека, к которому относится событие.",
            )
        if (
            status == Gift.Status.PLANNED
            and person
            and event
            and not self.errors
        ):
            existing = Gift.objects.planned().filter(person=person, event=event)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                self.add_error(
                    None,
                    "Для этого события уже есть запланированный подарок. "
                    "Отменённый подарок новую запись не блокирует.",
                )
        return cleaned
