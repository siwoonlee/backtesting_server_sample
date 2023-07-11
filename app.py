from typing import Any
from fastapi import FastAPI, HTTPException
import pandas as pd
import uvicorn
import asyncio
from backtesting import Backtest

from database import MySQLDatabase
from queries import SELECT_DATA_BY_TICKER, SELECT_ALL_TICKERS
from responses import BackTestPerTicker, BackTestResponse
from strategies import SimpleCrossStrategy

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


@app.get("/backtest", response_model=BackTestResponse)
async def backtest() -> Any:
    try:
        df = await db.execute_query_to_pandas_df(SELECT_ALL_TICKERS)
        tasks = [
            asyncio.ensure_future(
                cross_strategy_backtest(ticker)
            ) for ticker in df['ticker']
        ]
        result_list = await asyncio.gather(*tasks)
        return BackTestResponse(result=result_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)