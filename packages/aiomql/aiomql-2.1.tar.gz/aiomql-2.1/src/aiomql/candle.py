import asyncio
from typing import Type, TypeVar, Generic
from pandas import DataFrame, Series

from .core.constants import TimeFrame

_Candles = TypeVar('_Candles', bound='Candles')
_Candle = TypeVar('_Candle', bound='Candle')


class Candle:
    """A class representing bars from the MetaTrader 5 terminals as customized class analogous to Japanese Candlesticks.
    You can subclass this class for added customization.

    Keyword Args:
        All keyword arguments are set as object attributes.

    Attributes:
        time (int): Period start time.
        open (int): Open price
        high (float): The highest price of the period
        low (float): The lowest price of the period
        close (float): Close price
        tick_volume (float): Tick volume
        real_volume (float): Trade volume
        spread (float): Spread
        ema (float, optional): ema
        Index (int): Custom attribute representing the position of the candle in a sequence.
    """
    def __init__(self, *, time: int, open: float, high: float, low: float, close: float, tick_volume: float = 0,
                 real_volume: float = 0, spread: float = 0, Index: int = 0, ema: float = 0):
        self.time = time
        self.high = high
        self.low = low
        self.close = close
        self.real_volume = real_volume
        self.spread = spread
        self.open = open
        self.tick_volume = tick_volume
        self.Index = Index
        self.ema = ema

    def __eq__(self, other):
        return (self.open, self.close, self.low, self.high, self.time) == (other.open, other.close, other.low, other.high, other.time)

    def __lt__(self, other):
        return self.time < other.time

    def __gt__(self, other):
        return self.time > other.time

    def __hash__(self):
        return int(self.open*self.close*self.high*self.low*self.time)

    @property
    def mid(self) -> float:
        """The median of open and close

        Returns:
            float: The median of open and close
        """
        return (self.open + self.close) / 2

    def is_bullish(self) -> bool:
        """ A simple check to see if the candle is bullish.

        Returns:
            bool: True or False
        """
        return self.close > self.open

    def is_bearish(self) -> bool:
        """A simple check to see if the candle is bearish.

        Returns:
            bool: True or False
        """
        return self.open > self.close


class Candles(Generic[_Candle]):
    """An iterable container class of Candle objects in chronological order.

    Args:
        data (DataFrame, tuple[tuple]): A pandas dataframe or a tuple of tuple as returned from the terminal

    Keyword Args:
        flip (bool): If flip is True reverse the chronological order of the candles.
        candle (Type[Candle]): A subclass of Candle to use as the candle class.

    Attributes:
        data: A pandas dataframe of the rates.
        Index (Series['int']): A pandas Series of the indexes of all candles in the object.
        time (Series['int']): A pandas Series of the time of all candles in the object.
        open (Series[float]): A pandas Series of the opening price of all candles in the object.
        high (Series[float]): A pandas Series of the high price of all candles in the object.
        low (Series[float]):  A pandas Series of the low price of all candles in the object.
        close (Series[float]):  A pandas Series of the closing price of all candles in the object.
        tick_volume (Series[float]):  A pandas Series of the tick volume of all candles in the object.
        real_volume (Series[float]): A pandas Series of the real volume of all candles in the object.
        spread (Series[float]): A pandas Series of the spread of all candles in the object.
        ema (Series[float], Optional): A pandas Series of the ema of all candles in the object if available.
        timeframe (TimeFrame): The timeframe of the candles in the object.
        candle_class (Type[Candle]): The Candle class to use for the candles in the object.

    Notes:
        The candle class can be customized by subclassing the Candle class and passing the subclass as the candle keyword argument.
        Or defining it on the class body as a class attribute.
    """
    Index: Series
    time: Series
    open: Series
    high: Series
    low: Series
    close: Series
    tick_volume: Series
    real_volume: Series
    spread: Series
    ema: Series
    candle_class: Type[Candle] = Candle
    timeframe: TimeFrame
    
    def __init__(self, *, data: DataFrame | tuple[tuple], flip=False, candle_class: Type[Candle] = None):
        data = DataFrame(data) if not isinstance(data, DataFrame) else data
        self._data = data.iloc[::-1] if flip else data
        tf = self.time[1] - self.time[0]
        self.timeframe = TimeFrame.get(abs(tf))
        self.candle_class = candle_class or self.candle_class

    def __len__(self):
        return self._data.shape[0]

    def __contains__(self, item: _Candle):
        return item.time == self[item.Index].time

    def __getitem__(self, index) -> _Candle | _Candles:
        if isinstance(index, slice):
            cls = self.__class__
            data = self._data.iloc[index]
            data.reset_index(drop=True, inplace=True)
            return cls(data=data)

        item = self._data.iloc[index]
        return self.candle_class(Index=index, **item)

    def __getattr__(self, item):
        if item in {'Index', 'time', 'open', 'high', 'low', 'close', 'tick_volume', 'real_volume', 'spread', 'ema'}:
            return self._data[item]
        raise AttributeError(f'Attribute {item} not defined on class {self.__class__.__name__}')

    def __iter__(self):
        return (self.candle_class(**row._asdict()) for row in self._data.itertuples())

    async def compute_ema(self, *, period: int):
        """Compute the ema of the rates in the object and append it inplace to the dataframe object
         under the column name 'ema'.

        Args:
            period (int): The period of the ema.
        """
        await asyncio.to_thread(self._data.ta.ema, length=period, append=True)
        self._data.rename(columns={f"EMA_{period}": 'ema'}, inplace=True)

    @property
    def data(self) -> DataFrame:
        return self._data
