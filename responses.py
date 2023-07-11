from pydantic import BaseModel


class BackTest(BaseModel):
    ticker: str
    return_rate: float
    maximum_draw_down: float
    sharpe_ratio: float


class BackTestResponse(BaseModel):
    result: list[BackTest]
    total_return_rate: float
    total_maximum_draw_down: float
    total_sharpe_ratio: float
