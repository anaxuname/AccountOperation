from datetime import datetime

from src.utils import get_executed, load_operations_file, format_operation_date, get_date_from_operation, \
    sorted_operations, mask_acc_number, print_top_operations
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
                        "description": "Перевод с карты на карту", "from": "МИР 4878656375033856",
                        "to": "Maestro 6890749237669619"},
                       {"id": 74897425, "state": "EXECUTED", "date": "2019-02-08T09:09:35.038506",
                        "operationAmount": {"amount": "62654.30", "currency": {"name": "USD", "code": "USD"}},
                        "description": "Перевод организации", "from": "Счет 28429442875257789335",
                        "to": "Счет 95473010446151855633"}]


def test_mask_acc_number():
    assert mask_acc_number("МИР 4878656375033856") == "МИР 4878 65** **** 3856"
    assert mask_acc_number("Счет 95473010446151855633") == "Счет **5633"
    assert mask_acc_number("Visa Gold 8702717057933248") == "Visa Gold 8702 71** **** 3248"
    with pytest.raises(ValueError):
        mask_acc_number("VisaGold8702717057933248")
    with pytest.raises(ValueError):
        mask_acc_number("")


def test_print_operations(capfd):
    print_top_operations([{"id": 596914981, "state": "EXECUTED", "date": "2018-04-16T17:34:19.241289",
        "operationAmount": {"amount": "65169.27", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации", "from": "Visa Platinum 1813166339376336",
        "to": "Счет 97848259954268659635"}, {"id": 200634844, "state": "CANCELED", "date": "2018-02-13T04:43:11.374324",
        "operationAmount": {"amount": "42210.20", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации", "from": "Счет 33355011456314142963", "to": "Счет 45735917297559088682"},
        {"id": 879660146, "state": "EXECUTED", "date": "2018-07-22T07:42:32.953324",
            "operationAmount": {"amount": "92130.50", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации", "from": "Счет 19628854383215954147",
            "to": "Счет 90887717138446397473"},
        {"id": 893507143, "state": "EXECUTED", "date": "2018-02-03T07:16:28.366141",
            "operationAmount": {"amount": "90297.21", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Открытие вклада", "to": "Счет 37653295304860108767"},
        {"id": 710136990, "state": "CANCELED", "date": "2018-08-17T03:57:28.607101",
            "operationAmount": {"amount": "66906.45", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации", "from": "Maestro 1913883747791351",
            "to": "Счет 11492155674319392427"},
        {"id": 390558607, "state": "EXECUTED", "date": "2019-02-12T00:08:07.524972",
            "operationAmount": {"amount": "16796.95", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации", "from": "Счет 72645194281643232984",
            "to": "Счет 95782287258966264115"},
        {"id": 902831954, "state": "EXECUTED", "date": "2018-04-22T17:01:46.885252",
            "operationAmount": {"amount": "84732.61", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации", "from": "Visa Platinum 3530191547567121",
            "to": "Счет 46878338893256147528"}], max_operations=1)

    out, err = capfd.readouterr()
    assert out == "16.04.2018 Перевод организации\nVisa Platinum 1813 16** **** 6336 -> Счет **9635\n65169.27 USD\n\n"
