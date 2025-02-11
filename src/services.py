import os
from typing import Any, Union

import requests
from dotenv import load_dotenv

load_dotenv()
api_key_currency = os.getenv('API_KEY_CURRENCY')
api_key_stock = os.getenv('API_KEY_STOCK')


def get_currency_rate(currency: str) -> Union[float, str]:
    """ Принимает валюту в виде строки и возвращает курс в рублях """

    if currency == 'RUB':
        return 1
    else:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount=1"
        payload: dict[str, Any] = {}
        headers = {
            "apikey": api_key_currency
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        status_code = response.status_code

        if status_code == 200:
            return round(float(response.json()['result']), 2)
        else:
            return 'Something went wrong'


def get_stock_price(stock: str) -> Union[float, str]:
    web_page = 'https://www.alphavantage.co'
    url = f'{web_page}/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=5min&apikey={api_key_stock}'
    response = requests.get(url)
    data = response.json()
    status_code = response.status_code

    if status_code == 200:
        last_refreshed = data['Meta Data']['3. Last Refreshed']
        stock_price = data['Time Series (5min)'][last_refreshed]['4. close']
        return round(float(stock_price), 2)
    else:
        return 'Something went wrong'
