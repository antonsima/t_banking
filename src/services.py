import os
from collections import defaultdict
import datetime as dt

import pandas as pd

from src.utils import get_data_frame_from_excel_file


def get_cashback_categories_dict(transactions: list[dict], year: int, month: int) -> dict:
    """
    На вход поступают транзакции в виде списка словарей,
    год и месяц в формате целых чисел, на выходе словарь с категориями и кэшбэком по ним
    """

    transactions_dataframe = pd.DataFrame(transactions)
    transactions_dataframe['Дата операции'] = pd.to_datetime(transactions_dataframe['Дата операции'], dayfirst=True)
    filtered_transactions_df = transactions_dataframe[
        (transactions_dataframe['Дата операции'].dt.month == month) & (transactions_dataframe[
                                                                           'Дата операции'].dt.year == year)]

    cashback_categories_defdict = defaultdict(int)

    for index, row in filtered_transactions_df.iterrows():
        if row['Кэшбэк'] > 0:
            category = row['Категория']
            cashback = row['Кэшбэк']

            cashback_categories_defdict[category] += cashback

    cashback_categories = dict(cashback_categories_defdict)

    return cashback_categories

