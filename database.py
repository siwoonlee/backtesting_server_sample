import aiomysql
import pandas as pd

from constants import (
    MYSQL_USERNAME,
    MYSQL_PASSWORD,
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_DATABASE_NAME,
)


class MySQLDatabase:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await aiomysql.create_pool(
            host=MYSQL_HOST,
            user=MYSQL_USERNAME,
            password=MYSQL_PASSWORD,
            db=MYSQL_DATABASE_NAME,
            port=MYSQL_PORT,
            autocommit=True,
            minsize=5,
            maxsize=20,
        )

    async def execute_query_to_pandas_df(self, query) -> pd.DataFrame:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                result = await cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(result, columns=column_names)
        return df
