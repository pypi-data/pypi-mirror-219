from logging import getLogger

from .core.models import TradeRequest, OrderSendResult, OrderCheckResult, TradeOrder
from .core.constants import TradeAction, OrderTime, OrderFilling

logger = getLogger()


class Order(TradeRequest):
    """Trade order related functions and properties. Subclass of TradeRequest.
    An order class must always be initialized with a symbol.

    Keyword Args:
        kwargs: Arguments for initializing the order object

    Attributes:
        action (TradeAction): Trading operation type from TradeAction Enum

        type_time (OrderTime):  Order type by expiration from OrderTime

        type_filling (OrderFilling): Order filling type from OrderFilling Enum
    """

    def __init__(self, **kwargs):
        if 'symbol' not in kwargs:
            raise ValueError('symbol is required')
        self.symbol = kwargs.pop('symbol')
        self.action = kwargs.get('action', None) or TradeAction.DEAL
        self.type_time = kwargs.get('type_time', None) or OrderTime.GTC
        self.type_filling = kwargs.get('type_filling', None) or OrderFilling.FOK
        super().__init__(**kwargs)

    @property
    async def orders_total(self):
        """Get the number of active orders.

        Returns:
            (int): total number of active orders
        """
        return await self.mt5.orders_total()

    @property
    async def orders(self) -> tuple[TradeOrder]:
        """Get active orders with the ability to filter by symbol or ticket.
        Keyword Args:
            ticket (int): Order ticket. Optional named parameter. If ticket=0, then all orders are returned using symbol as filter.

        Returns:
            list[TradeOrder]: A list of active trade orders as TradeOrder objects
        """
        orders = await self.mt5.orders_get(symbol=self.symbol)
        orders = (TradeOrder(**order._asdict()) for order in orders)
        return tuple(orders)

    async def check(self) -> OrderCheckResult:
        """Check funds sufficiency for performing a required trading operation

        Returns:
            (OrderCheckResult): Returns OrderCheckResult object
        """
        res = await self.mt5.order_check(self.dict)
        return OrderCheckResult(**res._asdict())

    async def send(self) -> OrderSendResult:
        """Send a request to perform a trading operation from the terminal to the trade server.

        Returns:
             OrderSendResult: Returns OrderSendResult object
        """
        res = await self.mt5.order_send(self.dict)
        return OrderSendResult(**res._asdict())

    async def calc_margin(self) -> float:
        """Return the required margin in the account currency to perform a specified trading operation.

        Returns:
            float: Returns float value if successful

        Raises:
            ValueError: If not successful
        """
        res = await self.mt5.order_calc_margin(self.type, self.symbol, self.volume, self.price)
        raise ValueError(f'Failed to calculate margin for {self.symbol} {self.type} {self.volume} {self.price} {res}')

    async def calc_profit(self) -> float:
        """Return profit in the account currency for a specified trading operation.

        Returns:
            float: Returns float value if successful

        Raises:
            ValueError: If not successful
        """
        res = await self.mt5.order_calc_profit(self.type, self.symbol, self.volume, self.price, self.tp)
        if res is not None:
            return res
        raise ValueError(f'Failed to calculate profit for {self.symbol} {self.type} {self.volume} {self.price} {self.tp}')
