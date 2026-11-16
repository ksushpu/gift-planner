from django.shortcuts import render

from .models import Person


def people(request):
    """Страница со списком людей."""
    query = request.GET.get("q", "").strip()

    # Получаем всех людей; при поисковом запросе фильтруем по имени.
    persons_list = Person.objects.all()
    if query:
        persons_list = persons_list.filter(name__icontains=query)

    persons_list = persons_list.order_by("name")

    context = {
        "persons": persons_list,
        "query": query,
    }
    return render(request, "people/person_list.html", context)
