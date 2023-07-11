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
