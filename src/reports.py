import datetime
import logging
import os
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from config import LOGS_DIR
from src.views import get_report_func_result

logger = logging.getLogger(__name__)
path_to_log = os.path.join(LOGS_DIR, "reports.log")
file_handler = logging.FileHandler(path_to_log, "w", encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


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
