import pymysql
from constants import (
    MYSQL_USERNAME,
    MYSQL_PASSWORD,
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_DATABASE_NAME,
)
from queries import SAMPLE_DATA_DDL_QUERY, SAMPLE_DATA_QUERY

import pandas as pd


def create_db_and_tables():
    connection = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USERNAME,
        password=MYSQL_PASSWORD,
    )

    cursor = connection.cursor()
    # Make database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE_NAME}")
    connection.commit()
    cursor.close()
    connection.close()

    connection = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USERNAME,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE_NAME,
    )
    cursor = connection.cursor()
    # Make sample table
    cursor.execute(SAMPLE_DATA_DDL_QUERY)

    # Insert sample data to table
    df = pd.read_csv("./crypto_ohlcv.csv")
    for row in df.itertuples():
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
            connection.commit()

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    create_db_and_tables()