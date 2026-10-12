from django.http import HttpResponse

from homepage.views import page
from models.gifts import find_gift_by_id
from storage import load_events, load_gifts, load_persons


def gifts(request):
    """Страница со списком подарков."""
    persons = load_persons("people.json")
    events = load_events(persons, "events.json")
    gifts_list = load_gifts(persons, events, "gifts.json")

    items = ""
    for gift in gifts_list:
        status = "вручён" if gift.is_done else "не вручён"
        badge = "bg-success" if gift.is_done else "bg-warning"
        text = (
            f"{gift.idea} для {gift.person.name} "
            f"к {gift.event.title} ({gift.event.date})"
        )
        items += (
            f'<li class="list-group-item d-flex '
            f'justify-content-between align-items-center">'
            f'<a href="/gifts/{gift.id}/">{text}</a>'
            f'<span class="badge {badge}">{status}</span>'
            f'</li>'
        )

    if not items:
        items = '<li class="list-group-item">Список пуст.</li>'

    content = f"""
    <h1>Подарки</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Gift Planner — подарки", content))


def gift_detail(request, gift_id):
    """Страница отдельного подарка."""
    persons = load_persons("people.json")
    events = load_events(persons, "events.json")
    gifts_list = load_gifts(persons, events, "gifts.json")
    gift = find_gift_by_id(gifts_list, gift_id)

    if gift is None:
        content = """
        <h1 class="text-danger">Подарок не найден</h1>
        <a href="/gifts/" class="btn btn-outline-secondary">
            ← к списку подарков
        </a>
        """
        return HttpResponse(
            page("Подарок не найден", content),
            status=404,
        )

    status = "вручён" if gift.is_done else "не вручён"
    badge = "bg-success" if gift.is_done else "bg-warning"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Подарок №{gift.id}</h5>
            <p class="card-text">
                <strong>Идея:</strong> {gift.idea}
            </p>
            <p class="card-text">
                <strong>Кому:</strong> {gift.person.name}
            </p>
            <p class="card-text">
                <strong>Событие:</strong> {gift.event.title}
                ({gift.event.date})
            </p>
            <p class="card-text">
                <strong>Статус:</strong>
                <span class="badge {badge}">{status}</span>
            </p>
            <a href="/gifts/" class="btn btn-outline-secondary">
                ← к списку подарков
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Подарок №{gift.id}", content))
