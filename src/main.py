import os

from src.utils import get_data_frame_from_excel_file
from src.views import get_main_page

date_to_test = '2021-11-13 10:00:00'
PATH_TO_EXCEL = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")
transactions = get_data_frame_from_excel_file(PATH_TO_EXCEL)


# Веб-страница
print(get_main_page(date_to_test, transactions))

# Сервис
transactions_dicts = transactions.to_dict(orient='records')
print(get_(transactions_dicts))

# Отчет

print(get_report(transactions))