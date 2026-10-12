from django.http import HttpResponse

from homepage.views import page
from storage import load_persons


def people(request):
    """Страница со списком людей."""
    items = ""
    for person in load_persons("people.json"):
        items += f'<li class="list-group-item">{person}</li>'

    if not items:
        items = '<li class="list-group-item">Список пуст.</li>'

    content = f"""
    <h1>Люди</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Gift Planner — люди", content))
