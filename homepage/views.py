from django.http import HttpResponse


def page(title, content):
    """Единый каркас HTML-страницы."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
<nav class="nav bg-light px-3 py-2 mb-4">
    <a class="nav-link" href="/">Главная</a>
    <a class="nav-link" href="/people/">Люди</a>
    <a class="nav-link" href="/events/">События</a>
    <a class="nav-link" href="/gifts/">Подарки</a>
</nav>
<main class="container">{content}</main>
</body>
</html>"""


def index(request):
    """Главная страница."""
    content = """
    <h1 class="display-4">Gift Planner</h1>
    <p class="lead">Система планирования подарков.</p>
    <p>Основные разделы:</p>
    <a href="/people/" class="btn btn-primary me-2">Люди</a>
    <a href="/events/" class="btn btn-secondary me-2">События</a>
    <a href="/gifts/" class="btn btn-success">Подарки</a>
    """
    return HttpResponse(page("Gift Planner", content))


def page_not_found(request, exception):
    """Собственная страница ошибки 404."""
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )
