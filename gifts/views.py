import sqlite3
from django.shortcuts import render

DB_PATH = "data/gift_planner.sqlite"


def gifts(request):
    """Страница со списком подарков."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Запрос с JOIN (получаем идею, имя человека и название события)
    gifts_list = conn.execute("""
        SELECT gifts.id, gifts.idea, gifts.is_done,
               people.name AS person_name,
               events.title AS event_title
        FROM gifts
        JOIN people ON gifts.person_id = people.id
        JOIN events ON gifts.event_id = events.id
        ORDER BY gifts.id;
    """).fetchall()
    conn.close()

    return render(request, "gifts/gift_list.html", {"gifts": gifts_list})


def gift_detail(request, gift_id):
    """Страница отдельного подарка."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    gift = conn.execute("""
        SELECT
        gifts.id,
        gifts.idea,
        gifts.is_done,
        people.name AS person_name,
        events.title AS event_title,
        events.date AS event_date
        FROM gifts
        JOIN people ON gifts.person_id = people.id
        JOIN events ON gifts.event_id = events.id
        WHERE gifts.id = ?;
    """, (gift_id,)).fetchone()
    conn.close()

    return render(request, "gifts/gift_detail.html",
                  {"gift": gift}, status=404 if gift is None else 200)


def statistics(request):
    """Страница статистики."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    stats = conn.execute("""
        SELECT
            people.name AS person_name,
            COUNT(gifts.id) AS gifts_count,
            CASE
                WHEN COUNT(gifts.id) % 10 = 1
                    AND COUNT(gifts.id) % 100 != 11
                THEN 'подарок'
                WHEN COUNT(gifts.id) % 10 IN (2, 3, 4)
                    AND COUNT(gifts.id) % 100 NOT IN (12, 13, 14)
                THEN 'подарка'
                ELSE 'подарков'
            END AS word
        FROM people
        LEFT JOIN gifts ON people.id = gifts.person_id
        GROUP BY people.id, people.name
        ORDER BY gifts_count DESC;
    """).fetchall()
    conn.close()

    return render(request, "gifts/statistics.html", {"statistics": stats})
