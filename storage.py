import json
import os

DATA_DIR = "data"


def ensure_data_dir():
    """Создает папку data, если её нет."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_data(filename: str) -> list:
    """Загружает данные из JSON-файла."""
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print(f"Ошибка чтения файла {filename}.")
        print("Данные не загружены, используется пустой список.")
        return []


def save_data(filename: str, data: list) -> None:
    """Сохраняет данные в JSON-файл."""
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except IOError:
        print(f"Ошибка записи в файл {filename}.")