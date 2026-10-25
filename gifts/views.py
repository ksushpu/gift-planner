from django.shortcuts import render
from models.gifts import find_gift_by_id
from storage import load_events, load_gifts, load_persons


def gifts(request):
    """Страница со списком подарков."""
    persons = load_persons("people.json")
    events = load_events(persons, "events.json")
    gifts_list = load_gifts(persons, events, "gifts.json")

    context = {
        "gifts": gifts_list,
    }
    return render(request, "gifts/gift_list.html", context)


def gift_detail(request, gift_id):
    """Страница отдельного подарка."""
    persons = load_persons("people.json")
    events = load_events(persons, "events.json")
    gifts_list = load_gifts(persons, events, "gifts.json")
    gift = find_gift_by_id(gifts_list, gift_id)

    context = {
        "gift": gift,
    }
    return render(
        request,
        "gifts/gift_detail.html",
        context,
        status=404 if gift is None else 200
    )
