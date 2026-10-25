import json
from db.database import get_connection

PEOPLE_FILE = "data/people.json"
EVENTS_FILE = "data/events.json"
GIFTS_FILE = "data/gifts.json"


def load_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_people(conn):
    people = load_json(PEOPLE_FILE)
    conn.executemany(
        "INSERT INTO people (id, name) VALUES (?, ?)",
        [(p["id"], p["name"]) for p in people]
    )


def import_events(conn):
    events = load_json(EVENTS_FILE)
    conn.executemany(
        "INSERT INTO events (id, person_id, title, date) VALUES (?, ?, ?, ?)",
        [(e["id"], e["person_id"], e["title"], e["date"]) for e in events]
    )


def import_gifts(conn):
    gifts = load_json(GIFTS_FILE)
    conn.executemany(
        "INSERT INTO gifts "
        "(id, person_id, event_id, idea, is_done)"
        "VALUES (?, ?, ?, ?, ?)",
        [
            (g["id"], g["person_id"], g["event_id"],
             g["idea"], int(g.get("is_done", False)))
            for g in gifts
        ]
    )


def main():
    conn = get_connection()
    try:
        # Очищаем таблицы перед импортом, чтобы не было ошибок при повторном
        # запуске
        conn.execute("DELETE FROM gifts")
        conn.execute("DELETE FROM events")
        conn.execute("DELETE FROM people")

        import_people(conn)
        import_events(conn)
        import_gifts(conn)
        conn.commit()
        print("Данные успешно импортированы!")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка импорта: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
