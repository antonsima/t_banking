import os
from unittest.mock import patch

from dotenv import load_dotenv

from src.external_api import get_currency_rate, get_stock_price

load_dotenv()
api_key_currency = os.getenv('API_KEY_CURRENCY')
api_key_stock = os.getenv('API_KEY_STOCK')

test_operation_result_from_usd = {"date": "2025-02-02",
                                  "info": {"rate": 98.568878,
                                           "timestamp": 1738438205},
                                  "query": {"amount": 1,
                                            "from": "USD",
                                            "to": "RUB"},
                                  "result": 98.568878,
                                  "success": True}

test_operation_result_from_rub = {"date": "2025-02-02",
                                  "info": {"rate": 1,
                                           "timestamp": 1738438205},
                                  "query": {"amount": 1,
                                            "from": "RUB",
                                            "to": "RUB"},
                                  "result": 1,
                                  "success": True}

test_url_from_usd = 'https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=1'
test_url_from_rub = 'https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=RUB&amount=1'

stock_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol'
test_url_from_aapl = f'{stock_url}=AAPL&interval=5min&apikey={api_key_stock}'

test_stock_price_answer = {'Meta Data': {'1. Information': 'Intraday (5min) open, high, low, close prices and volume',
                                         '2. Symbol': 'AAPL',
                                         '3. Last Refreshed': '2025-02-14 19:55:00',
                                         '4. Interval': '5min',
                                         '5. Output Size': 'Compact',
                                         '6. Time Zone': 'US/Eastern'},
                           'Time Series (5min)': {'2025-02-14 19:55:00': {'1. open': '244.7100',
                                                                          '2. high': '244.7500',
                                                                          '3. low': '244.5000',
                                                                          '4. close': '244.6400',
                                                                          '5. volume': '2096'}}}


@patch('requests.request')
def test_get_currency_rate_from_usd(mock_get):
    mock_get.return_value.json.return_value = test_operation_result_from_usd
    mock_get.return_value.status_code = 200
    assert get_currency_rate('USD') == 98.57
    mock_get.assert_called_once_with('GET',
                                     test_url_from_usd,
                                     headers={'apikey': api_key_currency},
                                     data={})


def test_get_currency_rate_from_rub():
    assert get_currency_rate('RUB') == 1


@patch('requests.request')
def test_get_currency_rate_error(mock_get):
    mock_get.return_value.json.return_value = test_operation_result_from_usd
    mock_get.return_value.status_code = 404
    assert get_currency_rate('USD') == 'Something went wrong'
    mock_get.assert_called_once_with('GET',
                                     test_url_from_usd,
                                     headers={'apikey': api_key_currency},
                                     data={})


@patch('requests.get')
def test_get_stock_price(mock_get):
    mock_get.return_value.json.return_value = test_stock_price_answer
    mock_get.return_value.status_code = 200
    assert get_stock_price('AAPL') == 244.64
    mock_get.assert_called_once_with(test_url_from_aapl)


@patch('requests.get')
def test_get_stock_price_error(mock_get):
    mock_get.return_value.json.return_value = test_stock_price_answer
    mock_get.return_value.status_code = 404
    assert get_stock_price('AAPL') == 'Something went wrong'
    mock_get.assert_called_once_with(test_url_from_aapl)