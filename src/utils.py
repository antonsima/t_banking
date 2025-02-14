import datetime
import json
import logging
import os
import re
from typing import Union

import pandas as pd

from src.services import get_currency_rate, get_stock_price

logger = logging.getLogger(__name__)
path_to_log = os.path.join(os.path.dirname(__file__), "..", "logs", "utils.log")
file_handler = logging.FileHandler(path_to_log, "w", encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_greeting(date: str) -> str:
    """ Принимает строку формата YYYY-MM-DD HH:MM:SS, возвращает строку с приветствием """

    logger.info('Начало работы функции get_greeting')

    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

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


def get_data_frame_from_excel_file(path_to_excel_file: str) -> dict:
    """ Принимает путь до xlsx-файла, возвращает DataFrame """

    logger.info('Начало работы функции get_greeting')

    try:
        transactions = pd.read_excel(path_to_excel_file).to_dict(orient='list')
    except FileNotFoundError as ex:
        logger.error(f'Произошла ошибка, Файл не найден: {ex}')
        return {}

    if not transactions:
        logger.error('Произошла ошибка: pd.DataFrame(): Пустой XLSX файл')
        return {}

    logger.info("Программа завершена успешно")

    return transactions


def get_cards(transactions: dict) -> list[dict]:
    """
    Принимает DataFrame с транзакциями, возвращает список словарей
    last_digits, total_spent и cashback
    """

    logger.info('Начало работы функции get_cards')

    if not transactions:
        logger.info("Пустой словарь транзакций. Программа завершена успешно")
        return []
    else:
        transactions_df = pd.DataFrame(transactions)

        grouped_transactions_df = transactions_df.groupby(['Номер карты', 'Сумма операции'])
        last_digits_pattern = re.compile(r'\d+')
        amount_dict: dict[str, Union[str, float]] = {}

        for card in grouped_transactions_df:
            last_card_digits = last_digits_pattern.search(card[0][0]).group(0)

            amount = card[0][1]

            if amount_dict.get(last_card_digits) is None:
                amount_dict[last_card_digits] = 0

            if amount < 0:
                amount_dict[last_card_digits] += amount

        grouped_transactions_df = transactions_df.groupby(['Номер карты', 'Кэшбэк'])
        cashback_dict: dict[str, Union[str, float]] = {}

        for card in grouped_transactions_df:
            last_card_digits = last_digits_pattern.search(card[0][0]).group(0)

            cashback = card[0][1]

            if cashback_dict.get(last_card_digits) is None:
                cashback_dict[last_card_digits] = 0

            cashback_dict[last_card_digits] += cashback

        cards = []

        for card_num in amount_dict.keys():
            total_spent = round(float(str(amount_dict.get(card_num))) * (-1), 2)

            card_info = {'last_digits': card_num,
                         "total_spent": total_spent,
                         "cashback": round(float(cashback_dict.get(card_num, 0)), 2)}
            cards.append(card_info)

        logger.info("Программа завершена успешно")

        return cards


def get_top_transactions(transactions: dict) -> list[dict]:
    """
    Принимает DataFrame с транзакциями, возвращает список словарей
    date, amount, category и description
    """

    logger.info('Начало работы функции get_top_transactions')

    if not transactions:
        logger.info("Пустой словарь транзакций. Программа завершена успешно")
        return []
    else:
        transactions_df = pd.DataFrame(transactions)

        sorted_transactions = transactions_df.sort_values(by='Сумма операции')

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

    with open(path_to_user_settings_json, 'r') as file:
        currencies = json.load(file)

    currency_rates = []

    for currency in currencies['user_currencies']:
        rate = get_currency_rate(currency)

        tmp_dict = {"currency": currency,
                    "rate": rate}

        currency_rates.append(tmp_dict)

    logger.info("Программа завершена успешно")

    return currency_rates


def get_stock_prices(path_to_user_settings_json: str) -> list[dict]:
    logger.info('Начало работы функции get_stock_prices')

    with open(path_to_user_settings_json, 'r') as file:
        stocks = json.load(file)

    stock_prices = []

    for stock in stocks['user_stocks']:
        price = get_stock_price(stock)

        tmp_dict = {"stock": stock,
                    "price": price}

        stock_prices.append(tmp_dict)

    logger.info("Программа завершена успешно")

    return stock_prices


# print(get_stock_prices('../data/user_settings.json'))
# print(get_currency_rates('../data/user_settings.json'))
# transactions_dataframe = get_data_frame_from_excel_file('../data/operations.xlsx')
# print(get_cards(transactions_dataframe))
# print(get_greeting('2025-05-11 00:00:00'))
# print(get_top_transactions(transactions_dataframe))
