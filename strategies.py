from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA
import pandas as pd


class SimpleCrossStrategy(Strategy):
    def init(
        self,
        short_ma_unit: int = 30,
        long_ma_unit: int = 100,
    ):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, short_ma_unit)
        self.sma2 = self.I(SMA, close, long_ma_unit)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()


if __name__ == "__main__":
    df = pd.read_csv("./crypto_ohlcv.csv", date_parser=['Date'])
    df.set_index("Date", inplace=True)
    df.index = pd.to_datetime(df.index)
    df = df[df['Ticker'] == 'IOSTUSDT']
    bt = Backtest(
        df,
        SimpleCrossStrategy,
        cash=10000,
        commission=.002,
        exclusive_orders=True,
    )
    output = bt.run()
