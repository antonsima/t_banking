import datetime
import logging
import os
from functools import wraps
from typing import Callable, Optional, ParamSpec, TypeVar

import pandas as pd
from dateutil.relativedelta import relativedelta

from config import JSON_DIR, LOGS_DIR

P = ParamSpec('P')
T = TypeVar('T')

logger = logging.getLogger(__name__)
path_to_log = os.path.join(LOGS_DIR, "reports.log")
file_handler = logging.FileHandler(path_to_log, "w", encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


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


@get_report_func_result()
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """
    Принимает транзакции в виде DataFrame, категорию в виде строки и дату
    в виде строки в формате YYYY-MM-DD HH:MM:SS
    Возвращает DataFrame транзакций по категории за последние три месяца от переданной даты
    """

    logger.info('Начало работы функции spending_by_category')

    if date is None:
        end_period = datetime.datetime.now()
    else:
        end_period = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    logger.debug(f"end_period = {end_period}")

    start_period = end_period - relativedelta(months=3)

    logger.debug(f"start_period = {start_period}")

    filtered_transactions = transactions.loc[
        (pd.to_datetime(transactions['Дата операции'], dayfirst=True).between(start_period, end_period))]
    transactions_by_category = filtered_transactions.loc[
        (filtered_transactions['Категория'] == category) & (filtered_transactions['Сумма операции'] < 0)]

    logger.info("Программа завершена успешно")

    return transactions_by_category
