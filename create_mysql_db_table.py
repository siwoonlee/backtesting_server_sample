import tqdm
import pandas as pd
import pymysql
from constants import (
    MYSQL_USERNAME,
    MYSQL_PASSWORD,
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_DATABASE_NAME,
)
from queries import SAMPLE_DATA_DDL_QUERY, SAMPLE_DATA_QUERY


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

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    create_db_and_tables()