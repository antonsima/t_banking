import datetime
import json
import logging
import os
import re

import pandas as pd

from src.utils import (get_currency_rates, get_data_frame_from_excel_file, get_greeting, get_stock_prices,
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


def get_main_page(date: str, transactions: dict) -> str:
    """
    Принимает дату в виде строки формата YYYY-MM-DD HH:MM:SS
    и транзакции в виде словаря, возвращает JSON-ответ с информацией
    greeting, cards, top_transactions, currency_rates и stock_prices
    """

    logger.info('Начало работы функции get_main_page')

    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    current_year = str(date_obj.year)

    if len(str(date_obj.month)) < 2:
        current_month = '0' + str(date_obj.month)
    else:
        current_month = str(date_obj.month)

    if len(str(date_obj.day)) < 2:
        current_day = '0' + str(date_obj.day)
    else:
        current_day = str(date_obj.day)

    transactions_df = pd.DataFrame(transactions)
    day_pattern = re.compile(fr'{current_day}[^-]{current_month}[^-]{current_year}\s\d+:\d+:\d+')
    month_pattern = re.compile(fr'\d+[^-]{current_month}[^-]{current_year}\s\d+:\d+:\d+')
    transactions_this_month_df = pd.DataFrame()

    logger.info('Начало работы цикла')

    for index_first_iter, row_first_iter in transactions_df.iterrows():
        operation_date = str(row_first_iter['Дата операции'])
        if day_pattern.search(operation_date) is not None:

            logger.info('Начало работы цикла в цикле')

            start_index = int(str(index_first_iter))

            for index_second_iter, row_second_iter in transactions_df.iloc[start_index:].iterrows():
                operation_date = str(row_second_iter['Дата операции'])

                if month_pattern.search(operation_date) is not None:
                    continue
                else:
                    end_index = int(str(index_second_iter))
                    transactions_this_month_df = transactions_df.iloc[start_index:end_index]

                    logger.info('Конец работы циклов')

                    break
            break

    transactions_this_month = transactions_this_month_df.to_dict(orient='list')

    greeting = get_greeting(date)
    logger.debug(f'Приветствие: {greeting}')

    top_transactions = get_top_transactions(transactions_this_month)
    logger.debug(f'5 топ транзакций: {top_transactions}')

    currency_rates = get_currency_rates(PATH_TO_USER_SETTINGS)
    logger.debug(f'Курс валют: {currency_rates}')

    stock_prices = get_stock_prices(PATH_TO_USER_SETTINGS)
    logger.debug(f'Стоимость акций: {stock_prices}')

    main_page = {'greeting': greeting,
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
