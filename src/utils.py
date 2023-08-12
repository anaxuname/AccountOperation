import json
from datetime import datetime


def load_operations_file(param):
    """
    Функция загрузки файла json
    """
    with open(param, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_executed(all_operations):
    """
    Функция формирования списка только выполненных (EXECUTED) операций
    """
    result = []
    for op in all_operations:
        if op.get("state") == "EXECUTED":
            result.append(op)
    return result


def format_date(operation_date: str):
    """
    Форматирование даты перевода в формате ДД.ММ.ГГГГ
    """
    op_date = datetime.fromisoformat(operation_date)
    return op_date.strftime("%d.%m.%Y")
