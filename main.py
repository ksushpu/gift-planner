from models.persons import (
    add_person,
    find_persons_by_name,
    show_persons,
)
from models.events import add_event, show_events
from models.gifts import add_gift, show_gifts
from storage import (
    load_events,
    load_gifts,
    load_persons,
    save_events,
    save_gifts,
    save_persons,
)
from utils import input_date


def show_menu() -> None:
    """Показать главное меню."""
    print("\n--- Система планирования подарков ---")
    print("1 — Добавить человека")
    print("2 — Добавить событие")
    print("3 — Добавить идею подарка")
    print("4 — Показать все события")
    print("5 — Показать все подарки")
    print("6 — Показать всех людей")
    print("7 — Найти человека по имени")
    print("0 — Выход")


def choose_person(persons):
    """Запросить имя и вернуть найденного человека."""
    name = input("Введите имя человека: ")
    found = find_persons_by_name(persons, name)
    if not found:
        print("Человек не найден. Сначала добавьте его.")
        return None
    return found[0]


def main() -> None:
    """Точка запуска приложения."""
    persons = load_persons()
    events = load_events(persons)
    gifts = load_gifts(persons)

    while True:
        show_menu()
        choice = input("Ваш выбор: ")

        if choice == "1":
            name = input("Введите имя: ")
            add_person(persons, name)
            save_persons(persons)
            print(f"Человек '{name}' добавлен.")

        elif choice == "2":
            person = choose_person(persons)
            if person is None:
                continue
            date = input_date("Дата события (ГГГГ-ММ-ДД): ")
            add_event(events, person, date)
            save_events(events)
            print(f"Событие для '{person.name}' добавлено.")

        elif choice == "3":
            person = choose_person(persons)
            if person is None:
                continue
            idea = input("Идея подарка: ")
            add_gift(gifts, person, idea)
            save_gifts(gifts)
            print(f"Идея '{idea}' добавлена для '{person.name}'.")

        elif choice == "4":
            show_events(events)

        elif choice == "5":
            show_gifts(gifts)

        elif choice == "6":
            show_persons(persons)

        elif choice == "7":
            query = input("Имя для поиска: ")
            results = find_persons_by_name(persons, query)
            if not results:
                print("Ничего не найдено.")
            else:
                for p in results:
                    print(p)

        elif choice == "0":
            print("Выход.")
            break

        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()
