import os

import pandas as pd
from freezegun import freeze_time

from config import DATA_DIR
from src.reports import spending_by_category
from src.utils import get_data_frame_from_excel_file

DATE_TO_TEST = '2022-03-30 22:22:03'
PATH_TO_EXCEL = os.path.join(DATA_DIR, "operations.xlsx")
TRANSACTIONS = get_data_frame_from_excel_file(PATH_TO_EXCEL)


def test_spending_by_category(spending_by_category_df):
    df1 = spending_by_category(TRANSACTIONS, 'Переводы', DATE_TO_TEST)
    df2 = spending_by_category_df

    df2['Номер карты'] = df2['Номер карты'].astype(df1['Номер карты'].dtype)

    pd.testing.assert_frame_equal(df1.reset_index(drop=True), df2.reset_index(drop=True))


@freeze_time(DATE_TO_TEST)
def test_spending_by_category_wo_date(spending_by_category_df):
    df1 = spending_by_category(TRANSACTIONS, 'Переводы')
    df2 = spending_by_category_df

    df2['Номер карты'] = df2['Номер карты'].astype(df1['Номер карты'].dtype)

    pd.testing.assert_frame_equal(df1.reset_index(drop=True), df2.reset_index(drop=True))
