from logging import getLogger
from typing import Type

from .core.models import AccountInfo, SymbolInfo


logger = getLogger()


class Account(AccountInfo):
    """A Subclass of AccountInfo and the Base class
    Properties and methods for working with the current trading account are defined here.
    This is a singleton class as you can only use one account at a time.

    Attributes:
        risk (float): Percentage of account to risk
        risk_to_reward (float): ratio of risk to reward
        connected (bool): Status of connection to MetaTrader 5 Terminal
        symbols (set[SymbolInfo]): A set of available symbols for the financial market.

    Notes:
        Other Account properties are defined in the AccountInfo class.
    """
    risk: float = 0.05
    risk_to_reward: float = 2
    connected: bool
    symbols = set()
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    async def refresh(self):
        """
        Update the account info instance with the latest values from the terminal
        """
        account_info = await self.mt5.account_info()
        acc = account_info._asdict()
        self.set_attributes(**acc)

    @property
    def account_info(self) -> dict:
        """Creates a dictionary of login details.
        Looks for login details in both the instance and the global config instance.
        login details defined in the account instance takes precedence over those in the config instance

        Returns (dict): A dict of login, server and password details

        Note:
            This method will only look for config details in the config instance if the login attribute of the
            account Instance returns a falsy value
        """
        acc_info = self.get_dict(include={'login', 'server', 'password'})
        return acc_info if acc_info['login'] else self.config.account_info()

    async def sign_in(self) -> bool:
        """Connect to a trading account.

        Returns:
            bool: True if login was successful else False
        """
        await self.mt5.initialize(**self.account_info)
        self.connected = await self.mt5.login(**self.account_info)
        if self.connected:
            await self.refresh()
            self.symbols = await self.symbols_get()
            return self.connected
        await self.mt5.shutdown()
        return False

    def has_symbol(self, symbol: str | Type[SymbolInfo]):
        """Checks to see if a symbol is available for a trading account

        Args:
            symbol (str | SymbolInfo):

        Returns:
            bool: True if symbol is present otherwise False
        """
        try:
            symbol = SymbolInfo(name=symbol) if isinstance(symbol, str) else symbol
            return symbol in self.symbols
        except Exception as err:
            logger.warning(f'Error: {err}; {symbol} not available in this market')
            return False

    async def symbols_get(self) -> set[SymbolInfo]:
        """Get all financial instruments from the MetaTrader 5 terminal available for the current account.

        Returns:
            set[Symbol]: A set of available symbols.
        """
        syms = await self.mt5.symbols_get()
        return {SymbolInfo(name=sym.name) for sym in syms}
