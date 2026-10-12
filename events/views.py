from django.http import HttpResponse

from homepage.views import page
from models.events import find_event_by_id
from storage import load_events, load_persons


def events(request):
    """Страница со списком событий."""
    persons = load_persons("people.json")
    events_list = load_events(persons, "events.json")

    items = ""
    for event in events_list:
        text = (
            f"{event.title} — {event.date} "
            f"({event.person.name})"
        )
        items += (
            f'<li class="list-group-item">'
            f'<a href="/events/{event.id}/">{text}</a>'
            f'</li>'
        )

    if not items:
        items = '<li class="list-group-item">Список пуст.</li>'

    content = f"""
    <h1>События</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Gift Planner — события", content))


def event_detail(request, event_id):
    """Страница отдельного события."""
    persons = load_persons("people.json")
    events_list = load_events(persons, "events.json")
    event = find_event_by_id(events_list, event_id)

    if event is None:
        content = """
        <h1 class="text-danger">Событие не найдено</h1>
        <a href="/events/" class="btn btn-outline-secondary">
            ← к списку событий
        </a>
        """
        return HttpResponse(
            page("Событие не найдено", content),
            status=404,
        )

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{event.title}</h5>
            <p class="card-text">
                <strong>ID:</strong> {event.id}
            </p>
            <p class="card-text">
                <strong>Дата:</strong> {event.date}
            </p>
            <p class="card-text">
                <strong>Кому:</strong> {event.person.name}
            </p>
            <p class="card-text">
                <strong>Дней до события:</strong>
                {event.days_until()}
            </p>
            <a href="/events/" class="btn btn-outline-secondary">
                ← к списку событий
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(event.title, content))
