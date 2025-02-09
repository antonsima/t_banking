import datetime
import re

import pandas as pd


def get_greeting(date: str) -> str:
    """ Принимает строку формата YYYY-MM-DD HH:MM:SS, возвращает строку с приветствием """

    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    if 0 <= date_obj.hour <= 5:
        greeting = 'Доброй ночи'
    elif 6 <= date_obj.hour <= 11:
        greeting = 'Доброе утро'
    elif 12 <= date_obj.hour <= 17:
        greeting = 'Добрый день'
    else:
        greeting = 'Добрый вечер'

    return greeting


def get_cards(path_to_excel_file: str) -> list[dict]:
    """
    Принимает путь до xlsx-файла, возвращает список словарей
    last_digits, total_spent и cashback
    """

    try:
        transactions_df = pd.read_excel(path_to_excel_file)
    except FileNotFoundError as ex:
        print(f'{ex}: Файл не найден')
        return []

    if transactions_df.empty:
        print('[]: Пустой XLSX файл')
        return []

    grouped_transactions_df = transactions_df.groupby(['Номер карты', 'Сумма операции'])
    last_digits_pattern = re.compile(r'\d+')
    amount_dict = {}

    for card in grouped_transactions_df:
        last_card_digits = last_digits_pattern.search(card[0][0]).group(0)
        amount = card[0][1]

        if amount_dict.get(last_card_digits) is None:
            amount_dict[last_card_digits] = 0

        if amount < 0:
            amount_dict[last_card_digits] += amount

    grouped_transactions_df = transactions_df.groupby(['Номер карты', 'Кэшбэк'])
    cashback_dict = {}

    for card in grouped_transactions_df:
        last_card_digits = last_digits_pattern.search(card[0][0]).group(0)
        cashback = card[0][1]

        if cashback_dict.get(last_card_digits) is None:
            cashback_dict[last_card_digits] = 0

        cashback_dict[last_card_digits] += cashback

    cards = []

    for card_num in amount_dict.keys():
        # if card_num
        card_info = {'last_digits': card_num,
                     "total_spent": float(amount_dict.get(card_num)),
                     "cashback": float(cashback_dict.get(card_num, 0))}
        cards.append(card_info)

    return cards

print(get_cards('../data/operations.xlsx'))
print(get_greeting('2025-05-11 00:00:00'))