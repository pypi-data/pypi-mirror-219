import asyncio
import time
from typing import Type, TypeVar
from abc import ABC, abstractmethod

import pandas_ta as ta

from .core.meta_trader import MetaTrader
from .core.constants import TimeFrame
from .candle import Candles, Candle
from .symbol import Symbol as _Symbol
from .account import Account
from .core.config import Config

Symbol = TypeVar('Symbol', bound=_Symbol)


class Strategy(ABC):
    """The base class for creating strategies.

    Keyword Args:
        symbol (Symbol): The Financial Instrument as a Symbol Object
        params (dict): Configurable parameters for running the strategy

    Attributes:
        candle_class (Type[Candle]): Can be a subclass of the Candle class specific to the strategy and analysis carried out on it.
        candles_class (Type[Candles]): Candles class for the strategy can be the same or a subclass of the "candle.Candles" class.
        name (str): A name for the strategy.
        symbol (Symbol): The Financial Instrument as a Symbol Object
        mt5 (MetaTrader): MetaTrader instance.
        config (Config): Config instance.
        account (Account): Account instance.

    Notes:
        If you want to use a subclass of the Candle class, you must set the candle_class attribute to the subclass.
        The same applies to the Candles class.
    """
    candle_class: Type[Candle] = Candle
    candles_class: Type[Candles] = Candles
    name:  str = ""
    account = Account()
    mt5: MetaTrader()
    config = Config()

    def __init__(self, *, symbol: Symbol, params: dict = None):
        self.symbol = symbol
        self.parameters = params or {}
        self.parameters['symbol'] = symbol.name

    def __repr__(self):
        return f"{self.name}({self.symbol!r})"

    async def get_ema(self, *, time_frame: TimeFrame, period: int, count: int = 500) -> type(Candles):
        """Helper method that gets the ema of the bars.

        Keyword Args:
            time_frame (TimeFrame): Timeframe of the bars returned
            period (int): Period of the ema
            count (int): Number of objects to be returned

        Returns:
            Candles: A Candles Object
        """
        data = await self.symbol.copy_rates_from_pos(timeframe=time_frame, count=count)
        await asyncio.to_thread(data.ta.ema, length=period, append=True)
        data.rename(columns={f"EMA_{period}": 'ema'}, inplace=True)
        return self.candles_class(data=data)

    @staticmethod
    async def sleep(secs: float):
        """Sleep for the needed amount of seconds in between requests to the terminal.
        computes the accurate amount of time needed to sleep ensuring that the next request is made at the start of
        a new bar and making cooperative multitasking possible.

        Args:
            secs (float): The time in seconds. Usually the timeframe of the chart you trading with.
        """
        mod = time.time() % secs
        secs = secs - mod if mod != 0 else mod
        await asyncio.sleep(secs + 0.1)

    @abstractmethod
    async def trade(self):
        """Place trades using this method. This is the main method of the strategy.
        It will be called by the strategy runner.
        """
