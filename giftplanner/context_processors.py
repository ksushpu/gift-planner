from gifts.models import Gift


def planner_stats(request):
    """Общие числа для шаблонов: сколько подарков ещё не вручено."""
    return {
        "planned_gifts_count": Gift.objects.planned().count(),
    }
