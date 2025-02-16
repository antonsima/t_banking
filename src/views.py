import datetime
import json
import logging
import os
import re

import pandas as pd

from src.utils import (get_cards, get_currency_rates, get_data_frame_from_excel_file, get_greeting, get_stock_prices,
                       get_top_transactions)

logger = logging.getLogger(__name__)
path_to_log = os.path.join(os.path.dirname(__file__), "..", "logs", "views.log")
file_handler = logging.FileHandler(path_to_log, "w", encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

date_to_test = '2021-11-13 10:00:00'
PATH_TO_EXCEL = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")
PATH_TO_USER_SETTINGS = os.path.join(os.path.dirname(__file__), "..", "data", "user_settings.json")
transactions_ = get_data_frame_from_excel_file(PATH_TO_EXCEL)


def get_main_page(date: str, transactions: pd.DataFrame) -> str:
    """
    Принимает дату в виде строки формата YYYY-MM-DD HH:MM:SS
    и транзакции в виде DataFrame, возвращает JSON-ответ с информацией
    greeting, cards, top_transactions, currency_rates и stock_prices
    """

    logger.info('Начало работы функции get_main_page')

    end_period = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    start_period = end_period.replace(day=1, hour=0, minute=0, second=0)

    filtered_transactions = transactions.loc[
        (pd.to_datetime(transactions['Дата операции'], dayfirst=True).between(start_period, end_period))]
    expenses_transactions = filtered_transactions.loc[filtered_transactions['Сумма операции'] < 0]

    greeting = get_greeting()
    logger.debug(f'Приветствие: {greeting}')

    cards = get_cards(expenses_transactions)
    logger.debug(f'Список карт: {cards}')

    top_transactions = get_top_transactions(expenses_transactions)
    logger.debug(f'5 топ транзакций: {top_transactions}')

    currency_rates = get_currency_rates(PATH_TO_USER_SETTINGS)
    logger.debug(f'Курс валют: {currency_rates}')

    stock_prices = get_stock_prices(PATH_TO_USER_SETTINGS)
    logger.debug(f'Стоимость акций: {stock_prices}')

    main_page = {'greeting': greeting,
                 'cards': cards,
                 'top_transactions': top_transactions,
                 'currency_rates': currency_rates,
                 'stock_prices': stock_prices}

    main_page_json = json.dumps(main_page, ensure_ascii=False)
    logger.info('Сгенерирован JSON-ответ')

    with open('../json/main_page.json', 'w', encoding='utf-8') as file:
        json.dump(main_page, file, ensure_ascii=False)

    logger.info('JSON-ответ записан в файл "../json/main_page.json"')
    logger.info("Программа завершена успешно")

    return main_page_json

get_main_page(date_to_test, transactions_)