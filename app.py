from typing import Any
from fastapi import FastAPI, HTTPException
import pandas as pd
import uvicorn
import asyncio

from database import MySQLDatabase
from queries import SELECT_DATA_BY_TICKER, SELECT_ALL_TICKERS
from responses import BackTest, BackTestResponse

db = MySQLDatabase()
app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await db.connect()


async def cross_strategy_backtest(ticker: str) -> BackTest:
    df = await db.execute_query_to_pandas_df(
        SELECT_DATA_BY_TICKER.format(ticker=ticker)
    )
    result = ...
    return result


@app.post("/backtest", response_model=BackTestResponse)
async def backtest() -> Any:
    try:
        df = await db.execute_query_to_pandas_df(SELECT_ALL_TICKERS)
        tasks = [
            asyncio.ensure_future(
                cross_strategy_backtest(ticker)
            ) for ticker in df['ticker']
        ]
        result_list = await asyncio.gather(*tasks)
        # do something with result_list
        return dict(
            result=result_list,
            total_return_rate=...,
            total_maximum_draw_down=...,
            total_sharpe_ratio=...,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)