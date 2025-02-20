import datetime
import json
import logging
import os
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

import pandas as pd

from config import DATA_DIR, JSON_DIR, LOGS_DIR
from src.services import get_cashback_categories_dict
from src.utils import (get_cards, get_currency_rates, get_data_frame_from_excel_file, get_greeting, get_stock_prices,
                       get_top_transactions)

P = ParamSpec('P')
T = TypeVar('T')

logger = logging.getLogger(__name__)
path_to_log = os.path.join(LOGS_DIR, "views.log")
file_handler = logging.FileHandler(path_to_log, "w", encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

DATE = '2021-11-13 10:00:00'
PATH_TO_EXCEL = os.path.join(DATA_DIR, "operations.xlsx")
PATH_TO_USER_SETTINGS = os.path.join(DATA_DIR, "user_settings.json")
TRANSACTIONS = get_data_frame_from_excel_file(PATH_TO_EXCEL)
TRANSACTIONS_DICT = TRANSACTIONS.to_dict(orient='records')


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


def get_cashback_categories(transactions: list[dict], year: int, month: int) -> str:
    """
    На вход поступают транзакции в виде списка словарей,
    год и месяц в формате целых чисел, на выходе словарь с категориями и кэшбэком по ним
    """

    logger.info('Начало работы функции get_cashback_categories')

    cashback_categories = get_cashback_categories_dict(transactions, year, month)
    cashback_categories_json = json.dumps(cashback_categories, ensure_ascii=False)

    with open('../json/cashback_categories.json', 'w', encoding='utf-8') as file:
        json.dump(cashback_categories, file, ensure_ascii=False)

    logger.info('JSON-ответ записан в файл "../json/cashback_categories.json"')
    logger.info("Программа завершена успешно")

    return cashback_categories_json


def get_report_func_result(report_name: str = 'func_result_report.json') -> (
        Callable)[[Callable[P, pd.DataFrame]], Callable[P, pd.DataFrame]]:
    """
    Декоратор вывода результата функции
    """

    logger.info('Декоратор get_report_func_result')

    path_to_report = os.path.join(JSON_DIR, report_name)

    def decorator(func: Callable[P, pd.DataFrame]) -> Callable[P, pd.DataFrame]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> pd.DataFrame:
            result = func(*args, **kwargs)

            logger.debug(f"result = {result}")

            result.to_json(path_to_report, orient="records", force_ascii=False)

            logger.info('return func result')
            return result
        return wrapper
    return decorator
