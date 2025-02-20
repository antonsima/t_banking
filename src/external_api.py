import logging
import os
from typing import Any, Union

import requests
from dotenv import load_dotenv

from config import LOGS_DIR

logger = logging.getLogger(__name__)
path_to_log = os.path.join(LOGS_DIR, "services.log")
file_handler = logging.FileHandler(path_to_log, "w", encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

load_dotenv()
api_key_currency = os.getenv('API_KEY_CURRENCY')
api_key_stock = os.getenv('API_KEY_STOCK')


def get_currency_rate(currency: str) -> Union[float, str]:
    """ Принимает валюту в виде строки и возвращает курс в рублях """

    logger.info('Начало работы функции get_currency_rate')

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
        logger.debug(f"Статус код запроса = {status_code}")

        if status_code == 200:
            logger.info("Программа завершена успешно")
            return round(float(response.json()['result']), 2)
        else:
            logger.error("Статус код запроса != 200")
            return 'Something went wrong'


def get_stock_price(stock: str) -> Union[float, str]:
    """ Принимает тикер акции в виде строки, возвращает ее стоимость в USD """

    logger.info('Начало работы функции get_stock_price')

    web_page = 'https://www.alphavantage.co'
    url = f'{web_page}/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=5min&apikey={api_key_stock}'
    response = requests.get(url)
    data = response.json()
    status_code = response.status_code
    logger.debug(f"Статус код запроса = {status_code}")

    if status_code == 200:
        last_refreshed = data['Meta Data']['3. Last Refreshed']
        stock_price = data['Time Series (5min)'][last_refreshed]['4. close']

        logger.info("Программа завершена успешно")

        return round(float(stock_price), 2)
    else:
        logger.error("Статус код запроса != 200")
        return 'Something went wrong'
