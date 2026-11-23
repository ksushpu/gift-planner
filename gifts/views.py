from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Max, Min, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render

from events.models import Event
from people.models import Person

from .forms import GiftFilterForm, GiftForm
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
    filter_form = GiftFilterForm(request.GET or None)
    gifts_data = Gift.objects.all()
    sort = "id"

    if filter_form.is_bound and filter_form.is_valid():
        query = filter_form.cleaned_data["q"]
        person = filter_form.cleaned_data["person"]
        event = filter_form.cleaned_data["event"]
        status = filter_form.cleaned_data["status"]
        sort = filter_form.cleaned_data["sort"] or "id"

        if query:
            gifts_data = gifts_data.filter(
                Q(idea__icontains=query) | Q(person__name__icontains=query)
            )
        if person:
            gifts_data = gifts_data.filter(person=person)
        if event:
            gifts_data = gifts_data.filter(event=event)
        if status == "done":
            gifts_data = gifts_data.given()
        elif status == "pending":
            gifts_data = gifts_data.planned()
        elif status == "cancelled":
            gifts_data = gifts_data.cancelled()

    gifts_data = gifts_data.annotate(
        person_name=F("person__name"),
        event_title=F("event__title"),
    )

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
        "status",
        "person_name",
        "event_title",
    )

    # Постраничный вывод: по 5 записей на страницу.
    paginator = Paginator(gifts_data, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "gifts": page_obj,
        "page_obj": page_obj,
        "filter_form": filter_form,
        "sort": sort,
        "total_count": paginator.count,
    }
    return render(request, "gifts/gift_list.html", context)


def gift_create(request):
    """Создание подарка через ModelForm."""
    if request.method == "POST":
        form = GiftForm(request.POST)
        if form.is_valid():
            gift = form.save()
            messages.success(request, "Подарок сохранён.")
            return redirect("gifts:detail", gift_id=gift.pk)
    else:
        form = GiftForm(initial={"status": Gift.Status.PLANNED})
    return render(request, "gifts/gift_form.html", {
        "form": form,
        "title": "Новый подарок",
    })


def gift_edit(request, gift_id):
    """Редактирование существующего подарка."""
    gift = get_object_or_404(Gift, pk=gift_id)
    if request.method == "POST":
        form = GiftForm(request.POST, instance=gift)
        if form.is_valid():
            form.save()
            messages.success(request, "Изменения сохранены.")
            return redirect("gifts:detail", gift_id=gift.pk)
    else:
        form = GiftForm(instance=gift)
    return render(request, "gifts/gift_form.html", {
        "form": form,
        "title": f"Редактирование подарка №{gift.pk}",
        "gift": gift,
    })


def gift_cancel(request, gift_id):
    """Отмена подарка. Запись остаётся в базе со статусом «отменён»."""
    gift = get_object_or_404(
        Gift.objects.select_related("person", "event"),
        pk=gift_id,
    )
    if request.method == "POST":
        gift.status = Gift.Status.CANCELLED
        gift.save(update_fields=["status"])
        messages.success(request, "Подарок отменён.")
        return redirect("gifts:detail", gift_id=gift.pk)
    return render(request, "gifts/gift_cancel.html", {"gift": gift})


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
        done=Count("id", filter=Q(status=Gift.Status.GIVEN)),
        pending=Count("id", filter=Q(status=Gift.Status.PLANNED)),
        cancelled=Count("id", filter=Q(status=Gift.Status.CANCELLED)),
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
