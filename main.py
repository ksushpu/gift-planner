from utils import input_date
from storage import load_data, save_data
import logic

PEOPLE_FILE = "people.json"
EVENTS_FILE = "events.json"
GIFTS_FILE = "gifts.json"


def show_menu():
    print("\n--- Система планирования подарков ---")
    print("1 — Добавить человека")
    print("2 — Добавить событие")
    print("3 — Добавить идею подарка")
    print("4 — Показать все события (сортировка по дате)")
    print("5 — Планировать подарок")
    print("0 — Выход")


def main():
    people = load_data(PEOPLE_FILE)
    events = load_data(EVENTS_FILE)
    gifts = load_data(GIFTS_FILE)

    while True:
        show_menu()
        choice = input("Ваш выбор: ")

        if choice == "1":
            name = input("Введите имя человека: ")
            logic.add_person(people, name)
            save_data(PEOPLE_FILE, people)

        elif choice == "2":
            person = input("Для кого событие: ")
            date = input_date("Введите дату события (ГГГГ-ММ-ДД): ")
            logic.add_event(events, person, date)
            save_data(EVENTS_FILE, events)

        elif choice == "3":
            person = input("Кому подарок: ")
            idea = input("Идея подарка: ")
            logic.add_gift_idea(gifts, person, idea)
            save_data(GIFTS_FILE, gifts)

        elif choice == "4":
            if not events:
                print("Список событий пуст.")
            else:
                sorted_events = logic.sort_events_by_date(events)
                print("\n--- События (отсортированы по дате) ---")
                for e in sorted_events:
                    print(f"{e['date']} — {e['person']}")

        elif choice == "5":
            person = input("Кому планируем подарок: ")
            idea = input("Какой подарок планируем: ")
            print(f"Планирование подарка: '{idea}' для '{person}'.")

        elif choice == "0":
            print("Выход. Данные сохранены.")
            break
        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()