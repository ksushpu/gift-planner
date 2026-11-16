from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Max, Min, Q, Sum
from django.shortcuts import get_object_or_404, render

from events.models import Event
from people.models import Person

from .models import Gift


def _gift_word(count: int) -> str:
    """Вернуть корректную форму слова «подарок» для числа."""
    n = abs(count) % 100
    n1 = n % 10
    if 10 < n < 20:
        return "подарков"
    if n1 == 1:
        return "подарок"
    if 2 <= n1 <= 4:
        return "подарка"
    return "подарков"


def gifts(request):
    """Страница со списком подарков с фильтрами, поиском и пагинацией."""
    query = request.GET.get("q", "").strip()
    person_id = request.GET.get("person", "").strip()
    event_id = request.GET.get("event", "").strip()
    status = request.GET.get("status", "").strip()
    sort = request.GET.get("sort", "id")

    # Базовая выборка подарков.
    gifts_data = Gift.objects.all()

    # Поиск по идее подарка и имени человека.
    if query:
        gifts_data = gifts_data.filter(
            Q(idea__icontains=query) | Q(person__name__icontains=query)
        )

    # Фильтрация по человеку и событию (поля связанных моделей).
    if person_id.isdigit():
        gifts_data = gifts_data.filter(person_id=int(person_id))
    if event_id.isdigit():
        gifts_data = gifts_data.filter(event_id=int(event_id))

    # Фильтрация по статусу вручения.
    if status == "done":
        gifts_data = gifts_data.filter(is_done=True)
    elif status == "pending":
        # Исключаем уже вручённые подарки.
        gifts_data = gifts_data.exclude(is_done=True)

    # Добавляем сведения о связанных объектах для шаблона.
    gifts_data = gifts_data.annotate(
        person_name=F("person__name"),
        event_title=F("event__title"),
    )

    # Выбор поля сортировки из заранее заданного соответствия.
    sort_fields = {
        "id": "id",
        "idea": "idea",
        "person": "person__name",
        "event": "event__title",
    }
    sort_field = sort_fields.get(sort, "id")
    gifts_data = gifts_data.order_by(sort_field, "id")

    # Формируем набор полей для шаблона.
    gifts_data = gifts_data.values(
        "id",
        "idea",
        "is_done",
        "person_name",
        "event_title",
    )

    # Постраничный вывод: по 5 записей на страницу.
    paginator = Paginator(gifts_data, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "gifts": page_obj,
        "page_obj": page_obj,
        "query": query,
        "selected_person": person_id,
        "selected_event": event_id,
        "status": status,
        "sort": sort,
        "persons": Person.objects.order_by("name"),
        "events": Event.objects.order_by("title"),
        "total_count": paginator.count,
    }
    return render(request, "gifts/gift_list.html", context)


def gift_detail(request, gift_id):
    """Страница отдельного подарка."""
    gift = get_object_or_404(
        Gift.objects.select_related("person", "event"),
        pk=gift_id,
    )

    context = {
        "gift": gift,
    }
    return render(request, "gifts/gift_detail.html", context)


def statistics(request):
    """Страница статистики подарков."""
    # Сводные показатели по всем подаркам.
    summary = Gift.objects.aggregate(
        total=Count("id"),
        done=Count("id", filter=Q(is_done=True)),
        pending=Count("id", filter=Q(is_done=False)),
        avg_id=Avg("id"),
        min_id=Min("id"),
        max_id=Max("id"),
        sum_id=Sum("id"),
    )

    # Статистика по людям, включая тех, у кого нет подарков (LEFT JOIN).
    statistics_data = (
        Person.objects
        .annotate(
            gifts_count=Count("gifts"),
            person_name=F("name"),
        )
        .values(
            "person_name",
            "gifts_count",
        )
        .order_by("-gifts_count", "person_name")
    )

    statistics_list = [
        {
            "person_name": item["person_name"],
            "gifts_count": item["gifts_count"],
            "word": _gift_word(item["gifts_count"]),
        }
        for item in statistics_data
    ]

    context = {
        "statistics": statistics_list,
        "summary": summary,
    }
    return render(request, "gifts/statistics.html", context)
