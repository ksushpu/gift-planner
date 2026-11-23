import datetime

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EventForm
from .models import Event


def events(request):
    """Страница со списком событий."""
    query = request.GET.get("q", "").strip()
    upcoming_only = request.GET.get("upcoming", "").strip() == "1"

    # Загружаем события вместе с людьми одним запросом.
    events_list = Event.objects.select_related("person")

    # Поиск по названию события или имени человека.
    if query:
        events_list = events_list.filter(
            Q(title__icontains=query) | Q(person__name__icontains=query)
        )

    # Исключаем прошедшие события, если запрошены только предстоящие.
    if upcoming_only:
        events_list = events_list.exclude(date__lt=datetime.date.today())

    events_list = events_list.order_by("date", "pk")

    context = {
        "events": events_list,
        "query": query,
        "upcoming_only": upcoming_only,
    }
    return render(request, "events/event_list.html", context)


def event_create(request):
    """Создание события."""
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            messages.success(request, "Событие сохранено.")
            return redirect(event.get_absolute_url())
    else:
        form = EventForm()
    return render(request, "events/event_form.html", {
        "form": form,
        "title": "Новое событие",
    })


def event_edit(request, event_slug):
    """Редактирование события и его изображения."""
    event = get_object_or_404(Event, slug=event_slug)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, "Изменения сохранены.")
            return redirect(event.get_absolute_url())
    else:
        form = EventForm(instance=event)
    return render(request, "events/event_form.html", {
        "form": form,
        "title": f"Редактирование: {event.title}",
        "event": event,
    })


def event_detail(request, event_slug):
    """Страница отдельного события."""
    event = get_object_or_404(
        Event.objects.select_related("person"),
        slug=event_slug,
    )

    context = {
        "event": event,
    }
    return render(request, "events/event_detail.html", context)
