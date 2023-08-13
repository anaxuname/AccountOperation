from datetime import datetime

from src.utils import get_executed, load_operations_file, format_operation_date, get_date_from_operation, \
    sorted_operations, mask_acc_number
import pytest
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent

def test_get_executed():
    assert get_executed([{"id": 863064926, "state": "EXECUTED", "date": "2019-12-08T22:46:21.935582",
                          "operationAmount": {"amount": "41096.24", "currency": {"name": "USD", "code": "USD"}},
                          "description": "Открытие вклада", "to": "Счет 90424923579946435907"},
                         {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689",
                          "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
                          "description": "Перевод организации", "from": "Visa Platinum 1246377376343588",
                          "to": "Счет 14211924144426031657"},
                         {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441",
                          "operationAmount": {"amount": "77751.04", "currency": {"name": "руб.", "code": "RUB"}},
                          "description": "Перевод с карты на счет", "from": "Maestro 3928549031574026",
                          "to": "Счет 84163357546688983493"}, ]) == [
               {"id": 863064926, "state": "EXECUTED", "date": "2019-12-08T22:46:21.935582",
                "operationAmount": {"amount": "41096.24", "currency": {"name": "USD", "code": "USD"}},
                "description": "Открытие вклада", "to": "Счет 90424923579946435907"}]
    assert get_executed([]) == []
    assert get_executed([{"id": 863064926, "state": "EXECUTED", "date": "2019-12-08T22:46:21.935582",
                          "operationAmount": {"amount": "41096.24", "currency": {"name": "USD", "code": "USD"}},
                          "description": "Открытие вклада", "to": "Счет 90424923579946435907"}]) == [
               {"id": 863064926, "state": "EXECUTED", "date": "2019-12-08T22:46:21.935582",
                "operationAmount": {"amount": "41096.24", "currency": {"name": "USD", "code": "USD"}},
                "description": "Открытие вклада", "to": "Счет 90424923579946435907"}]
    assert get_executed([{"a": 1}, {"state": "EXECUTED"}]) == [{"state": "EXECUTED"}]
    assert get_executed([{}]) == []


def test_load_operations_file():
    print('ALLO BLYAD', BASE_DIR)

    assert load_operations_file(BASE_DIR / 'test_operations.json') == [
        {"id": 863064926, "state": "EXECUTED", "date": "2019-12-08T22:46:21.935582",
         "operationAmount": {"amount": "41096.24", "currency": {"name": "USD", "code": "USD"}},
         "description": "Открытие вклада", "to": "Счет 90424923579946435907"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689",
         "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
         "description": "Перевод организации", "from": "Visa Platinum 1246377376343588",
         "to": "Счет 14211924144426031657"}]


def test_format_date():
    assert format_operation_date({"id": 863064926, "state": "EXECUTED", "date": "2019-12-08T22:46:21.935582",
                                  "operationAmount": {"amount": "41096.24", "currency": {"name": "USD", "code": "USD"}},
                                  "description": "Открытие вклада", "to": "Счет 90424923579946435907"}) == "08.12.2019"
    with pytest.raises(ValueError):
        format_operation_date({"id": 863064926, "state": "EXECUTED", "date": "20198T22:46:21.935582",
                               "operationAmount": {"amount": "41096.24", "currency": {"name": "USD", "code": "USD"}},
                               "description": "Открытие вклада", "to": "Счет 90424923579946435907"})
    with pytest.raises(AttributeError):
        format_operation_date(None)


def test_get_date_from_operation():
    assert get_date_from_operation({"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689",
                                    "operationAmount": {"amount": "67314.70",
                                                        "currency": {"name": "руб.", "code": "RUB"}},
                                    "description": "Перевод организации", "from": "Visa Platinum 1246377376343588",
                                    "to": "Счет 14211924144426031657"}) == datetime(2018, 9, 12, 21, 27, 25, 241689)


def test_sorted_operations():
    op_list = [{"id": 416017997, "state": "EXECUTED", "date": "2019-05-07T01:32:37.142797",
                "operationAmount": {"amount": "29033.65", "currency": {"name": "USD", "code": "USD"}},
                "description": "Перевод с карты на карту", "from": "МИР 4878656375033856",
                "to": "Maestro 6890749237669619"},
               {"id": 556488059, "state": "CANCELED", "date": "2019-05-17T01:50:00.166954",
                "operationAmount": {"amount": "74604.56", "currency": {"name": "USD", "code": "USD"}},
                "description": "Перевод с карты на карту", "from": "МИР 8021883699486544",
                "to": "Visa Gold 8702717057933248"},
               {"id": 74897425, "state": "EXECUTED", "date": "2019-02-08T09:09:35.038506",
                "operationAmount": {"amount": "62654.30", "currency": {"name": "USD", "code": "USD"}},
                "description": "Перевод организации", "from": "Счет 28429442875257789335",
                "to": "Счет 95473010446151855633"}, ]
    sorted_operations(op_list)
    assert op_list == [{"id": 556488059, "state": "CANCELED", "date": "2019-05-17T01:50:00.166954",
                        "operationAmount": {"amount": "74604.56", "currency": {"name": "USD", "code": "USD"}},
                        "description": "Перевод с карты на карту", "from": "МИР 8021883699486544",
                        "to": "Visa Gold 8702717057933248"},
        {"id": 416017997, "state": "EXECUTED", "date": "2019-05-07T01:32:37.142797",
         "operationAmount": {"amount": "29033.65", "currency": {"name": "USD", "code": "USD"}},
         "description": "Перевод с карты на карту", "from": "МИР 4878656375033856", "to": "Maestro 6890749237669619"},
        {"id": 74897425, "state": "EXECUTED", "date": "2019-02-08T09:09:35.038506",
         "operationAmount": {"amount": "62654.30", "currency": {"name": "USD", "code": "USD"}},
         "description": "Перевод организации", "from": "Счет 28429442875257789335", "to": "Счет 95473010446151855633"}]


def test_mask_acc_number():
    assert mask_acc_number("МИР 4878656375033856") == "МИР 4878 65** **** 3856"
    assert mask_acc_number("Счет 95473010446151855633") == "Счет **5633"
    assert mask_acc_number("Visa Gold 8702717057933248") == "Visa Gold 8702 71** **** 3248"
    with pytest.raises(ValueError):
        mask_acc_number("VisaGold8702717057933248")
    with pytest.raises(ValueError):
        mask_acc_number("")
