from src.utils import get_executed, load_operations_file, sorted_operations, print_top_operations


def main():
    """
    Основная логика программы
    """
    all_operations = load_operations_file('operations.json')
    executed_operations = get_executed(all_operations)
    sorted_operations(executed_operations)
    print_top_operations(executed_operations)


if __name__ == "__main__":
    main()
