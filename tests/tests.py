from src.utils import get_executed, load_operations_file, format_date
import pytest


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
    assert load_operations_file('test_operations.json') == [
        {"id": 863064926, "state": "EXECUTED", "date": "2019-12-08T22:46:21.935582",
            "operationAmount": {"amount": "41096.24", "currency": {"name": "USD", "code": "USD"}},
            "description": "Открытие вклада", "to": "Счет 90424923579946435907"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации", "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"}]


def test_format_date():
    assert format_date("2019-12-08T22:46:21.935582") == "08.12.2019"
    with pytest.raises(ValueError):
        format_date("2019:46:21.935582")
    with pytest.raises(TypeError):
        format_date(None)