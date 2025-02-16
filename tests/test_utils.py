import os
from unittest.mock import patch

from freezegun import freeze_time

from src.utils import (get_cards, get_currency_rates, get_data_frame_from_excel_file, get_greeting, get_stock_prices,
                       get_top_transactions)

PATH_TO_EXCEL_FILE = os.path.join(os.path.dirname(__file__), "..", "tests", "reduced_operations.xlsx")
PATH_TO_EMPTY_EXCEL_FILE = os.path.join(os.path.dirname(__file__), "..", "tests", "empty_operations.xlsx")
PATH_TO_USER_SETTINGS = os.path.join(os.path.dirname(__file__), "..", "data", "user_settings.json")

test_cards_result = [{'last_digits': '4556', 'total_spent': 228633.33, 'cashback': 2286.0},
                     {'last_digits': '5091', 'total_spent': 14918.16, 'cashback': 150.0},
                     {'last_digits': '7197', 'total_spent': 48605.68, 'cashback': 487.0}]

test_top_transactions = [{'date': '22.11.2021 22:05:41', 'amount': 126105.03, 'category': 'Переводы',
                          'description': 'Перевод Кредитная карта. ТП 10.2 RUR'},
                         {'date': '17.11.2021 16:38:23', 'amount': 50000.0, 'category': 'Переводы',
                          'description': 'Пополнение вклада'},
                         {'date': '22.12.2021 23:30:44', 'amount': 28001.94, 'category': 'Переводы',
                          'description': 'Перевод Кредитная карта. ТП 10.2 RUR'},
                         {'date': '30.12.2021 22:22:03', 'amount': 20000.0, 'category': 'Переводы',
                          'description': 'Константин Л.'},
                         {'date': '16.12.2021 16:40:47', 'amount': 14216.42, 'category': 'ЖКХ',
                          'description': 'ЖКУ Квартира'}]

test_stock_prices = [{'stock': 'AAPL', 'price': 100}, {'stock': 'AMZN', 'price': 100},
                     {'stock': 'GOOGL', 'price': 100}, {'stock': 'MSFT', 'price': 100},
                     {'stock': 'TSLA', 'price': 100}]

test_currency_rates = [{"currency": "USD",
                        "rate": 100},
                       {"currency": "EUR",
                        "rate": 100}]


@freeze_time('2025-02-16 00:00:00')
def test_get_greeting_night():
    assert get_greeting() == 'Доброй ночи'


@freeze_time('2025-02-16 06:00:00')
def test_get_greeting_morning():
    assert get_greeting() == 'Доброе утро'


@freeze_time('2025-02-16 12:00:00')
def test_get_greeting_afternoon():
    assert get_greeting() == 'Добрый день'


@freeze_time('2025-02-16 18:00:00')
def test_get_greeting_evening():
    assert get_greeting() == 'Добрый вечер'


def test_get_data_frame_from_excel_file(reduced_operations_df, empty_df):
    assert get_data_frame_from_excel_file(PATH_TO_EXCEL_FILE).equals(reduced_operations_df)
    assert get_data_frame_from_excel_file(PATH_TO_EMPTY_EXCEL_FILE).equals(empty_df)
    assert get_data_frame_from_excel_file('wrong_path.xlsx').equals(empty_df)


def test_get_cards(reduced_operations_df, empty_df):
    assert get_cards(empty_df) == []
    assert get_cards(reduced_operations_df) == test_cards_result


def test_get_top_transactions(reduced_operations_df, empty_df):
    assert get_top_transactions(empty_df) == []
    assert get_top_transactions(reduced_operations_df) == test_top_transactions


@patch('src.utils.get_stock_price')
def test_get_stock_prices(mock_api):
    mock_api.return_value = 100
    assert get_stock_prices(PATH_TO_USER_SETTINGS) == test_stock_prices
    mock_api.assert_called()


def test_get_stock_prices_wrong_path():
    assert get_stock_prices('wrong.xlsx') == []


@patch('src.utils.get_currency_rate')
def test_get_currency_rates(mock_api):
    mock_api.return_value = 100
    assert get_currency_rates(PATH_TO_USER_SETTINGS) == test_currency_rates
    mock_api.assert_called()


def test_get_currency_rates_wrong_path():
    assert get_currency_rates('wrong.xlsx') == []
