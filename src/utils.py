import json


def format_date():
    """
    Форматирование даты перевода в формате ДД.ММ.ГГГГ
    """
    # date = datetime()
    pass


def get_executed(all_operations):
    result = []
    for op in all_operations:
        if op.get("state") == "EXECUTED":
            result.append(op)
    return result


def load_operations_file(param):
    with open(param, 'r', encoding='utf-8') as f:
        return json.load(f)
