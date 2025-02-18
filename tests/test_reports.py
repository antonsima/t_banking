import os

from freezegun import freeze_time

from config import DATA_DIR
from src.reports import get_report_func_result, spending_by_category
from src.utils import get_data_frame_from_excel_file

DATE_TO_TEST = '2021-11-13 10:00:00'
PATH_TO_EXCEL = os.path.join(DATA_DIR, "operations.xlsx")
TRANSACTIONS = get_data_frame_from_excel_file(PATH_TO_EXCEL)

test_result = '''Результат функции:            Дата операции  ... Сумма операции с округлением
302  12.11.2021 12:44:32  ...                       100.36
304  12.11.2021 12:34:17  ...                       292.93
305  11.11.2021 21:09:32  ...                       162.67
308  11.11.2021 15:25:03  ...                        99.32
309  10.11.2021 22:04:41  ...                        89.80
..                   ...  ...                          ...
819  16.08.2021 13:11:19  ...                        74.50
822  15.08.2021 12:10:21  ...                       180.97
823  15.08.2021 12:05:51  ...                       319.99
824  14.08.2021 18:32:30  ...                       136.97
825  13.08.2021 17:37:23  ...                        34.00

[181 rows x 15 columns]'''


def test_get_report_func_result():
    @get_report_func_result()
    def my_function(x: int, y: int) -> int:
        """
        Сложение двух чисел
        """
        return x + y

    result = my_function(1, 6)
    assert result == 'Результат функции: 7'


def test_spending_by_category():
    assert spending_by_category(TRANSACTIONS, 'Супермаркеты', DATE_TO_TEST) == test_result


@freeze_time(DATE_TO_TEST)
def test_spending_by_category_wo_date():
    assert spending_by_category(TRANSACTIONS, 'Супермаркеты') == test_result
