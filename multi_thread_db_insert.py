"""
    This script needs to be executed once before running the app for sample data insertion.
"""

import tqdm
import threading
import pymysqlpool
import pandas as pd

from constants import (
    MYSQL_USERNAME,
    MYSQL_PASSWORD,
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_DATABASE_NAME,
)
from queries import SAMPLE_DATA_QUERY
from create_mysql_db_table import create_db_and_tables

pymysqlpool.logger.setLevel('DEBUG')
config = {
    'host': MYSQL_HOST,
    'user': MYSQL_USERNAME,
    'port': MYSQL_PORT,
    'password': MYSQL_PASSWORD,
    'database': MYSQL_DATABASE_NAME,
    'autocommit': False
}


def main(pool, df, is_main_thread):
    conn = pool.get_connection()
    cursor = conn.cursor()
    for row in (tqdm.tqdm(df.itertuples(), total=len(df)) if is_main_thread else df.itertuples()):
        cursor.execute(
            SAMPLE_DATA_QUERY.format(
                transacted_date=getattr(row, "Date"),
                ticker=getattr(row, "Ticker"),
                open_price=getattr(row, "Open"),
                high_price=getattr(row, "High"),
                low_price=getattr(row, "Low"),
                close_price=getattr(row, "Close"),
                trade_volume=getattr(row, "Volume"),
            )
        )
        if getattr(row, "Index") % 1000 == 0:
            conn.commit()

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_db_and_tables()
    pool1 = pymysqlpool.ConnectionPool(size=1, maxsize=4, pre_create_num=4, name='pool1', **config)
    df = pd.read_csv("./crypto_ohlcv.csv")
    threads = []
    for i, df_part_start_idx in enumerate(range(0, len(df), len(df)//4)):
        df_partition = df.iloc[df_part_start_idx : df_part_start_idx + len(df)//4]
        threads.append(threading.Thread(target=main, args=(pool1, df_partition, i == 0)))
    # start threads
    for _thread in threads:
        _thread.start()
    for _thread in threads:
        _thread.join()