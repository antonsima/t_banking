import datetime
import json
import logging
import os

import pandas as pd

from config import LOGS_DIR
from src.external_api import get_currency_rate, get_stock_price

logger = logging.getLogger(__name__)
path_to_log = os.path.join(LOGS_DIR, "utils.log")
file_handler = logging.FileHandler(path_to_log, "w", encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_greeting() -> str:
    """ Возвращает строку с приветствием """

    logger.info('Начало работы функции get_greeting')

    date_obj = datetime.datetime.now()

    if 0 <= date_obj.hour <= 5:
        greeting = 'Доброй ночи'
    elif 6 <= date_obj.hour <= 11:
        greeting = 'Доброе утро'
    elif 12 <= date_obj.hour <= 17:
        greeting = 'Добрый день'
    else:
        greeting = 'Добрый вечер'

    logger.info("Программа завершена успешно")

    return greeting


def get_data_frame_from_excel_file(path_to_excel_file: str) -> pd.DataFrame:
    """ Принимает путь до xlsx-файла, возвращает DataFrame """

    logger.info('Начало работы функции get_data_frame_from_excel_file')

    try:
        transactions = pd.read_excel(path_to_excel_file)
    except FileNotFoundError as ex:
        logger.error(f'Произошла ошибка, Файл не найден: {ex}')
        return pd.DataFrame()

    if transactions.empty:
        logger.error('Произошла ошибка: pd.DataFrame(): Пустой XLSX файл')
        return pd.DataFrame()

    logger.info("Программа завершена успешно")

    return transactions


def get_cards(transactions: pd.DataFrame) -> list[dict]:
    """
    Принимает DataFrame с транзакциями, возвращает список словарей
    last_digits, total_spent и cashback
    """

    logger.info('Начало работы функции get_cards')

    if transactions.empty:
        logger.info("Пустой DataFrame транзакций. Программа завершена успешно")
        return []
    else:

        grouped_transactions_df = transactions.groupby('Номер карты')
        total_info = grouped_transactions_df.agg(total_spent=('Сумма операции', 'sum'),
                                                 cashback=('Сумма операции', lambda x: sum(x) // 100)).abs().round(2)

        cards = []

        for index, row in total_info.iterrows():

            card_info = {'last_digits': str(index).replace('*', ''),
                         "total_spent": float(str(row['total_spent'])),
                         "cashback": float(str(row['cashback']))}

            cards.append(card_info)

        logger.info("Программа завершена успешно")

        return cards


def get_top_transactions(transactions: pd.DataFrame) -> list[dict]:
    """
    Принимает DataFrame с транзакциями, возвращает список словарей
    date, amount, category и description
    """

    logger.info('Начало работы функции get_top_transactions')

    if transactions.empty:
        logger.info("Пустой DataFrame транзакций. Программа завершена успешно")
        return []
    else:
        sorted_transactions = transactions.sort_values(by='Сумма операции')

        top_transactions = []

        count = 0

        for index, row in sorted_transactions.iterrows():
            amount = round(float(str(row['Сумма операции'])) * (-1), 2)

            tmp_dict = {'date': row['Дата операции'],
                        "amount": amount,
                        "category": row['Категория'],
                        "description": row['Описание']}

            top_transactions.append(tmp_dict)

            count += 1

            if count == 5:
                break

        logger.info("Программа завершена успешно")

        return top_transactions


def get_currency_rates(path_to_user_settings_json: str) -> list[dict]:
    """ Принимает путь до пользовательских настроек в формате json,
     возвращает список словарей currency и rate """

    logger.info('Начало работы функции get_currency_rates')

    try:
        with open(path_to_user_settings_json, 'r') as file:
            currencies = json.load(file)
    except FileNotFoundError as ex:
        logger.error(f'Произошла ошибка, Файл не найден: {ex}')
        return []

    currency_rates = []

    for currency in currencies['user_currencies']:
        rate = get_currency_rate(currency)

        tmp_dict = {"currency": currency,
                    "rate": rate}

        currency_rates.append(tmp_dict)

    logger.info("Программа завершена успешно")

    return currency_rates


def get_stock_prices(path_to_user_settings_json: str) -> list[dict]:
    """ Принимает путь до пользовательских настроек, возвращает стоимость акций в виде списка словарей """
    logger.info('Начало работы функции get_stock_prices')

    try:
        with open(path_to_user_settings_json, 'r') as file:
            stocks = json.load(file)
    except FileNotFoundError as ex:
        logger.error(f'Произошла ошибка, Файл не найден: {ex}')
        return []

    stock_prices = []

    for stock in stocks['user_stocks']:
        price = get_stock_price(stock)

        tmp_dict = {"stock": stock,
                    "price": price}

        stock_prices.append(tmp_dict)

    logger.info("Программа завершена успешно")

    return stock_prices
