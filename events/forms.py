from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    """Создание и редактирование события, включая изображение."""

    class Meta:
        model = Event
        fields = ("person", "title", "date", "image")
        widgets = {
            "person": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Название события",
            }),
            "date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def clean_title(self):
        title = (self.cleaned_data.get("title") or "").strip()
        if len(title) < 3:
            raise forms.ValidationError(
                "Название должно содержать хотя бы 3 символа."
            )
        return title
