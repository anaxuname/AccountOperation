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


def format_operation_date(operation_date: dict):
    """
    Форматирование даты перевода в формате ДД.ММ.ГГГГ
    """
    return get_date_from_operation(operation_date).strftime("%d.%m.%Y")


def get_date_from_operation(op: dict):
    """
    Функция достает строку с датой операции и конвертирует ее в объект datetime
    """
    return datetime.fromisoformat(op.get('date'))


def sorted_operations(operations: list):
    """
    Форматирование списка по дате(сверху списка находятся последние)
    """
    operations.sort(key=get_date_from_operation, reverse=True)


def mask_acc_number(acc_number: str):
    """
    Маскировка номера карты в формате XXXX XX** **** XXXX
    Маскировка номера счета в формате **XXXX
    """
    type_, num = acc_number.rsplit(maxsplit=1)
    if type_ == 'Счет':
        return f"{type_} **{num[-4:]}"
    return f"{type_} {num[:4]} {num[4:6]}** **** {num[-4:]}"


def print_top_operations(executed_operations, max_operations=5):
    """
    Выведение 5 последних выполненных (EXECUTED) операций
    """
    i = 0
    for operation in executed_operations:
        op_date = operation.get("date")
        op_description = operation.get("description")
        op_from = operation.get("from")
        op_to = operation.get("to")
        op_amount = operation.get("operationAmount", {}).get("amount")
        op_currency = operation.get("operationAmount", {}).get("currency", {}).get("name")
        if op_date and op_description and op_from and op_to and op_amount and op_currency:
            print(format_operation_date(operation), op_description)
            print(mask_acc_number(op_from), "->", mask_acc_number(op_to))
            print(op_amount, op_currency)
            print()
            i += 1
            if i == max_operations:
                break
