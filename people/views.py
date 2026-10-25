from django.shortcuts import render
from storage import load_persons


def people(request):
    """Страница со списком людей."""
    persons_list = load_persons("people.json")
    context = {
        "persons": persons_list,
    }
    return render(request, "people/person_list.html", context)
