import json

from src.utils import get_executed


def main():
    """
    Считывание json file
    Выведение 5 последних выполненных (EXECUTED) операций
    Форматирование списка по дате(сверху списка находятся последние)
    Форматирование даты в формате ДД.ММ.ГГГГ
    Маскировка номера карты в формате XXXX XX** **** XXXX
    Маскировка номер счета в формате **XXXX
    """
    with open('operations.json', 'r', encoding='utf-8') as f:
        all_operations = json.load(f)

    executed_operations = get_executed(all_operations)

    for operation in executed_operations:
        try:
            print(operation["date"], operation["description"])
            print(operation["from"], "->", operation["to"])
            print(operation["operationAmount"]["amount"], operation["operationAmount"]["currency"]["name"])
        except KeyError:
            continue


if __name__ == "__main__":
    main()
