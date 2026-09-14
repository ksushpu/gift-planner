import datetime

def show_menu():
    print("\nСистема планирования подарков")
    print("1 — Добавить человека")
    print("2 — Добавить событие")
    print("3 — Добавить идею подарка")
    print("4 — Планировать подарок")
    print("0 — Выход")

people = []
events = []
gifts = []

def add_person():
    name = input("Введите имя человека: ")
    people.append(name)
    print(f"Человек '{name}' добавлен.")

def add_event():
    # СПЕЦИАЛЬНАЯ ОШИБКА: неверный формат даты.
    person = input("Для кого событие: ")
    date_str = input("Введите дату события (ГГГГ-ММ-ДД): ")
    broken = 1 / 0
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        events.append((person, date))
        print(f"Событие для '{person}' на дату {date} добавлено.")
    except ValueError:
        print("Ошибка: неверный формат даты.")

def add_gift():
    person = input("Кому подарок: ")
    idea = input("Идея подарка: ")
    gifts.append((person, idea))
    print(f"Идея подарка '{idea}' для '{person}' добавлена.")

def plan_gift():
    person = input("Кому планируем подарок: ")
    idea = input("Какой подарок планируем: ")
    print(f"Планирование подарка: '{idea}' для '{person}'.")
    print("Пока без сохранения — будет реализовано в ПР2.")

def main():
    while True:
        show_menu()
        choice = input("Ваш выбор: ")

        if choice == "1":
            add_person()
        elif choice == "2":
            add_event()
        elif choice == "3":
            add_gift()
        elif choice == "4":
            plan_gift()
        elif choice == "0":
            print("Выход.")
            break
        else:
            print("Неизвестная команда.")

if __name__ == "__main__":
    main()
