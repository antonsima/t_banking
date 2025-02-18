import os

from config import DATA_DIR
from src.services import filter_by_date, get_cashback_categories_dict
from src.utils import get_data_frame_from_excel_file

PATH_TO_EXCEL = os.path.join(DATA_DIR, "operations.xlsx")
TRANSACTIONS = get_data_frame_from_excel_file(PATH_TO_EXCEL)
TRANSACTIONS_DICT = TRANSACTIONS.to_dict(orient='records')


def test_get_cashback_categories_dict():
    assert get_cashback_categories_dict(TRANSACTIONS_DICT, 2021, 12) == {'Ж/д билеты': 181.0}