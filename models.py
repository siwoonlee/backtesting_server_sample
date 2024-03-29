from pydantic import BaseModel


class BackTestPerTicker(BaseModel):
    ticker: str
    start: str
    end: str
    sharpe_ratio: float
    overall_return_percent: float
    buy_and_hold_return_percent: float
    maximum_draw_down_percent: float


class BackTestResponse(BaseModel):
    result: list[BackTestPerTicker]


class InsertRowResponse(BaseModel):
    message: str


class Row(BaseModel):
    transacted_date: str
    ticker: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    trade_volume: float


class InsertRowRequest(BaseModel):
    rows: list[Row]


class BackTestRequest(BaseModel):
    tickers_list: list[str] = None
