from datetime import datetime
import asyncio
from logging import getLogger

import MetaTrader5
from MetaTrader5 import BookInfo, SymbolInfo, AccountInfo, Tick, TerminalInfo, TradeOrder, TradeDeal,\
    TradePosition, OrderSendResult, OrderCheckResult

from .constants import TimeFrame, CopyTicks, OrderType

logger = getLogger()


class BaseMeta(type):
    def __new__(mcs, cls_name, bases, cls_dict):
        defaults = MetaTrader5.__dict__
        defaults = {f'_{key}': value for key, value in defaults.items() if not key.startswith('_')}
        cls_dict |= defaults
        return super().__new__(mcs, cls_name, bases, cls_dict)


class MetaTrader(metaclass=BaseMeta):

    async def __aenter__(self):
        """
        Async context manager entry point.
        Initializes the connection to the MetaTrader terminal.
        Returns: An instance of the MetaTrader class.
        """
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Async context manager exit point.
        Closes the connection to the MetaTrader terminal.
        """
        await self.shutdown()

    async def login(self, login: int, password: str, server: str, timeout: int = 60000) -> bool:
        """"""
        return await asyncio.to_thread(self._login, login, password=password, server=server, timeout=timeout)

    async def initialize(self, path: str = "", login: int = 0, password: str = "", server: str = "",
                         timeout: int | None = None, portable=False) -> bool:
        """"""
        args = (path,) if path else tuple()
        kwargs = {key: value for key, value in (('login', login), ('password', password), ('server', server),
                                                ('timeout', timeout), ('portable', portable)) if value}
        return await asyncio.to_thread(self._initialize, *args, **kwargs)

    async def shutdown(self) -> None:
        """"""
        return await asyncio.to_thread(self._shutdown)

    async def last_error(self) -> tuple[int, str]:
        return await asyncio.to_thread(self._last_error)

    async def version(self) -> tuple[int, int, str] | None:
        """"""
        res = await asyncio.to_thread(self._version)

        if res is None:
            err = await self.last_error()
            logger.warning(f'Error in obtaining version. Error Code: {err}')
            return res

        return res

    async def account_info(self) -> AccountInfo | None:
        """"""
        res = await asyncio.to_thread(self._account_info)

        if res is None:
            err = await self.last_error()
            logger.warning(f'Error in obtaining account information. Error Code: {err}')
            return res

        return res

    async def terminal_info(self) -> TerminalInfo | None:
        res = await asyncio.to_thread(self._terminal_info)

        if res is None:
            err = await self.last_error()
            logger.warning(f'Error in obtaining terminal information. Error Code: {err}')
            return res

        return res

    async def symbols_total(self) -> int:
        return await asyncio.to_thread(self._symbols_total)

    async def symbols_get(self, group: str = "") -> tuple[SymbolInfo] | None:
        kwargs = {'group': group} if group else {}
        res = await asyncio.to_thread(self._symbols_get, **kwargs)

        if res is None:
            err = await self.last_error()
            logger.warning(f'Error in obtaining symbols. Error Code: {err}')
            return res

        return res

    async def symbol_info(self, symbol: str) -> SymbolInfo | None:
        res = await asyncio.to_thread(self._symbol_info, symbol)

        if res is None:
            err = await self.last_error()
            logger.warning(f'Error in obtaining information for {symbol}. Error Code: {err}')
            return res

        return res

    async def symbol_info_tick(self, symbol: str) -> Tick | None:
        res = await asyncio.to_thread(self._symbol_info_tick, symbol)

        if res is None:
            err = await self.last_error()
            logger.warning(f'Error in obtaining tick for {symbol}. Error Code: {err}')
            return res

        return res

    async def symbol_select(self, symbol: str, enable: bool) -> bool:
        return await asyncio.to_thread(self._symbol_select, symbol, enable)

    async def market_book_add(self, symbol: str) -> bool:
        return await asyncio.to_thread(self._market_book_add, symbol)

    async def market_book_get(self, symbol: str) -> tuple[BookInfo] | None:
        res = await asyncio.to_thread(self._market_book_get, symbol)

        if res is None:
            err = await self.last_error()
            logger.warning(f'Error in obtaining market depth content for {symbol}. Error Code: {err}')
            return res

        return res

    async def market_book_release(self, symbol: str) -> bool:
        return await asyncio.to_thread(self._market_book_release, symbol)

    async def copy_rates_from(self, symbol: str, timeframe: TimeFrame, date_from: datetime | int, count: int):
        res = await asyncio.to_thread(self._copy_rates_from, symbol, timeframe, date_from, count)

        if res is None:
            err = await self.last_error()
            logger.warning(f'Error in obtaining rates for {symbol}. Error Code: {err}')
            return res

        return res

    async def copy_rates_from_pos(self, symbol: str, timeframe: TimeFrame, start_pos: int, count: int):
        res = await asyncio.to_thread(self._copy_rates_from_pos, symbol, timeframe, start_pos, count)

        if res is None:
            err = await self.last_error()
            logger.warning(f'Error in obtaining rates for {symbol}. Error Code: {err}')
            return res

        return res

    async def copy_rates_range(self, symbol: str, timeframe: TimeFrame, date_from: datetime | int,
                               date_to: datetime | int):
        res = await asyncio.to_thread(self._copy_rates_range, symbol, timeframe, date_from, date_to)

        if res is None:
            err = await self.last_error()
            logger.warning(f'Error in obtaining rates for {symbol}. Error Code: {err}')
            return res

        return res

    async def copy_ticks_from(self, symbol: str, date_from: datetime | int, count: int, flags: CopyTicks):
        res = await asyncio.to_thread(self._copy_ticks_from, symbol, date_from, count, flags)

        if res is None:
            err = await self.last_error()
            logger.warning(f'Error in obtaining ticks for {symbol}. Error Code: {err}')
            return res

        return res

    async def copy_ticks_range(self, symbol: str, date_from: datetime | int, date_to: datetime | int, flags: CopyTicks):
        res = await asyncio.to_thread(self._copy_ticks_range, symbol, date_from, date_to, flags)

        if res is None:
            err = await self.last_error()
            logger.warning(f'Error in obtaining ticks for {symbol}. Error Code: {err}')
            return res

        return res

    async def orders_total(self) -> int:
        return await asyncio.to_thread(self._orders_total)

    async def orders_get(self, group: str = "", ticket: int = 0, symbol: str = "") -> tuple[TradeOrder] | None:
        """Get active orders with the ability to filter by symbol or ticket. There are three call options.
           Call without parameters. Return active orders on all symbols

        Keyword Args:
            symbol (str): Symbol name. Optional named parameter. If a symbol is specified, the ticket parameter is ignored.

            group (str): The filter for arranging a group of necessary symbols. Optional named parameter. If the group is specified, the function
                returns only active orders meeting a specified criteria for a symbol name.

            ticket (int): Order ticket (ORDER_TICKET). Optional named parameter.

        Returns:
            list[TradeOrder]: A list of active trade orders as TradeOrder objects
        """
        kwargs = {key: value for key, value in (('group', group), ('ticket', ticket), ('symbol', symbol)) if value}
        res = await asyncio.to_thread(self._orders_get, **kwargs)

        if res is None:
            err = await self.last_error()
            logger.warning(f'Error in obtaining orders. Error Code: {err}')
            return res

        return res

    async def order_calc_margin(self, action: OrderType, symbol: str, volume: float, price: float) -> float | None:
        res = await asyncio.to_thread(self._order_calc_margin, action, symbol, volume, price)

        if res is None:
            err = await self.last_error()
            logger.warning(f'Error in calculating margin. Error Code: {err}')
            return res

        return res

    async def order_calc_profit(self, action: OrderType, symbol: str, volume: float, price_open: float,
                                price_close: float) -> float | None:
        res = await asyncio.to_thread(self._order_calc_profit, action, symbol, volume, price_open, price_close)

        if res is None:
            err = await self.last_error()
            logger.warning(f'Error in calculating profit. Error Code: {err}')
            return res

        return res

    async def order_check(self, request: dict) -> OrderCheckResult:
        return await asyncio.to_thread(self._order_check, request)

    async def order_send(self, request: dict) -> OrderSendResult:
        return await asyncio.to_thread(self._order_send, request)

    async def positions_total(self) -> int:
        return await asyncio.to_thread(self._positions_total)

    async def positions_get(self, group: str = "", ticket: int = 0, symbol: str = "") -> tuple[TradePosition] | None:
        kwargs = {key: value for key, value in (('group', group), ('ticket', ticket), ('symbol', symbol)) if value}
        res = await asyncio.to_thread(self._positions_get, **kwargs)

        if res is None:
            err = await self.last_error()
            logger.warning(f'Error in obtaining open positions. Error Code: {err}')
            return res

        return res

    async def history_orders_total(self, date_from: datetime | int, date_to: datetime | int) -> int:
        return await asyncio.to_thread(self._history_orders_total, date_from, date_to)

    async def history_orders_get(self, date_from: datetime | int, date_to: datetime | int, group: str = '',
                                 ticket: int = 0, position: int = 0) -> tuple[TradeOrder] | None:
        kwargs = {key: value for key, value in (('group', group), ('ticket', ticket), ('position', position)) if value}
        res = await asyncio.to_thread(self._history_orders_get, date_from, date_to, **kwargs)

        if res is None:
            err = await self.last_error()
            logger.warning(f'Error in getting orders. Error Code: {err}')
            return res

        return res

    async def history_deals_total(self, date_from: datetime | int, date_to: datetime | int) -> int:
        return await asyncio.to_thread(self._history_deals_total, date_from, date_to)

    async def history_deals_get(self, date_from: datetime | int, date_to: datetime | int, group: str = '',
                                ticket: int = 0, position: int = 0) -> tuple[TradeDeal] | None:
        kwargs = {key: value for key, value in (('group', group), ('ticket', ticket), ('position', position)) if value}
        res = await asyncio.to_thread(self._history_deals_get, date_from, date_to, **kwargs)

        if res is None:
            err = await self.last_error()
            logger.warning(f'Error in getting deals. Error Code: {err}')
            return res

        return res


# TODO:
#  Typing for the methods that return numpy arrays types
