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


if __name__ == "__main__":
    # for testing purposes
    from queries import SELECT_DATA_BY_TICKER, SELECT_ALL_TICKERS
    import asyncio

    db = MySQLDatabase()

    async def startup_event():
        await db.connect()


    async def cross_strategy_backtest(ticker: str):
        df = await db.execute_query_to_pandas_df(
            SELECT_DATA_BY_TICKER.format(ticker=ticker)
        )
        print(df)
        return df


    async def main():
        await startup_event()
        df = await db.execute_query_to_pandas_df(SELECT_ALL_TICKERS)
        tasks = [
            asyncio.ensure_future(
                cross_strategy_backtest(ticker)
            ) for ticker in df['ticker'][:10]
        ]
        result_list = await asyncio.gather(*tasks)
        print(result_list)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()