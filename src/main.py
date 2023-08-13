from src.utils import get_executed, load_operations_file, sorted_operations, format_operation_date


def main():
    """
    Выведение 5 последних выполненных (EXECUTED) операций
    Маскировка номера карты в формате XXXX XX** **** XXXX
    Маскировка номер счета в формате **XXXX
    """

    all_operations = load_operations_file('operations.json')
    executed_operations = get_executed(all_operations)
    sorted_operations(executed_operations)
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
            print(op_from, "->", op_to)
            print(op_amount, op_currency)
            print()
            i += 1
            if i == 5:
                break



if __name__ == "__main__":
    main()
