import logging
from typing import Any
from fastapi import FastAPI, HTTPException
import pandas as pd
import uvicorn
import asyncio
from backtesting import Backtest

from database import MySQLDatabase
from queries import SELECT_DATA_BY_TICKER, SELECT_ALL_TICKERS, INSERT_SAMPLE_DATA_QUERY
from models import BackTestPerTicker, BackTestResponse, InsertRowResponse, InsertRowRequest, BackTestRequest
from strategies import SimpleCrossStrategy
from create_mysql_db_table import create_db_and_tables

logger = logging.getLogger("uvicorn")
create_db_and_tables()
db = MySQLDatabase()
app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await db.connect()


async def cross_strategy_backtest(ticker: str) -> BackTestPerTicker:
    df = await db.execute_query_to_pandas_df(
        SELECT_DATA_BY_TICKER.format(ticker=ticker)
    )
    df.rename(
        columns={
            "transacted_date": "Date",
            "open_price": "Open",
            "high_price": "High",
            "low_price": "Low",
            "close_price": "Close",
            "trade_volume": "Volume",
        },
        inplace=True
    )
    df.set_index("Date", inplace=True)
    df.index = pd.to_datetime(df.index)
    bt = Backtest(
        df,
        SimpleCrossStrategy,
        cash=10_000_000,
        commission=.002,
        exclusive_orders=True,
    )
    output = bt.run()
    return BackTestPerTicker(
        ticker=ticker,
        start=str(output['Start']),
        end=str(output['End']),
        sharpe_ratio=output['Sharpe Ratio'],
        overall_return_percent=output['Return [%]'],
        buy_and_hold_return_percent=output['Buy & Hold Return [%]'],
        maximum_draw_down_percent=output['Max. Drawdown [%]'],
    )


@app.post("/backtest", response_model=BackTestResponse)
async def backtest(req: BackTestRequest) -> Any:
    try:
        if req.tickers_list:
            tickers_list = req.tickers_list
        else:
            df = await db.execute_query_to_pandas_df(SELECT_ALL_TICKERS)
            tickers_list = df['ticker'].values
        tasks = [
            asyncio.ensure_future(
                cross_strategy_backtest(ticker)
            ) for ticker in tickers_list
        ]
        result_list = await asyncio.gather(*tasks)
        return BackTestResponse(result=result_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


@app.post("/insert_row", response_model=InsertRowResponse)
async def insert_row(req: InsertRowRequest) -> Any:
    try:
        async with db.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                for row in req.rows:
                    await cursor.execute(
                        INSERT_SAMPLE_DATA_QUERY.format(
                            transacted_date=row.transacted_date,
                            ticker=row.ticker,
                            open_price=row.open_price,
                            high_price=row.high_price,
                            low_price=row.low_price,
                            close_price=row.close_price,
                            trade_volume=row.trade_volume,
                        )
                    )
                await connection.commit()
        return {"message": "Insert Row Request Success!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)