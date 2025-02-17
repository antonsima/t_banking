import os

from src.utils import get_data_frame_from_excel_file
from src.views import get_main_page, get_cashback_categories

DATE_TO_TEST = '2021-11-13 10:00:00'
PATH_TO_EXCEL = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")
TRANSACTIONS = get_data_frame_from_excel_file(PATH_TO_EXCEL)
TRANSACTIONS_DICT = TRANSACTIONS.to_dict(orient='records')


# Веб-страница
print(get_main_page(DATE_TO_TEST, TRANSACTIONS))

# Сервис
print(get_cashback_categories(TRANSACTIONS_DICT, 2021, 11))

# Отчет
print(get_report(TRANSACTIONS))
