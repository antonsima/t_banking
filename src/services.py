import datetime as dt
from collections import defaultdict


def filter_by_date(transaction: dict, year: int, month: int) -> bool:
    transaction_month = dt.datetime.strptime(transaction['Дата операции'], '%d.%m.%Y %H:%M:%S').month
    transaction_year = dt.datetime.strptime(transaction['Дата операции'], '%d.%m.%Y %H:%M:%S').year

    return transaction_month == month and transaction_year == year


def get_cashback_categories_dict(transactions: list[dict], year: int, month: int) -> dict:
    """
    На вход поступают транзакции в виде списка словарей,
    год и месяц в формате целых чисел, на выходе словарь с категориями и кэшбэком по ним
    """

    filtered_transactions = list(filter(lambda transaction: filter_by_date(transaction, year, month), transactions))

    cashback_categories_def_dict: defaultdict = defaultdict(int)

    for transaction in filtered_transactions:
        if 0 < transaction['Кэшбэк'] > 0:
            category = transaction['Категория']
            cashback = transaction['Кэшбэк']

            cashback_categories_def_dict[category] += cashback

    cashback_categories = dict(cashback_categories_def_dict)
    sorted_cashback_categories = dict(sorted(cashback_categories.items(), key=lambda item: item[1], reverse=True))

    return sorted_cashback_categories
