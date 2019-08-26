from abc import ABC, abstractmethod
from typing import Iterable, Mapping, Optional

from bankroll.model import AccountBalance, Activity, Position

from .configuration import Settings
from .marketdata import MarketDataProvider


# Offers data about one or more brokerage accounts, initialized with data
# (e.g., exported files) or a mechanism to get the data (e.g., a live
# connection).
class AccountData(ABC):
    # Instantiates the receiving type using the information in the given
    # settings map.
    #
    # TODO: Refactor/simplify Configuration class so it can be used in cases
    # like this, instead of an unintuitive mapping.
    #
    # TODO: Hoist `lenient` into a Setting to make this less awkward.
    @classmethod
    @abstractmethod
    def fromSettings(
        cls, settings: Mapping[Settings, str], lenient: bool
    ) -> "AccountData":
        pass

    # Returns the positions currently held, fetching the data on-demand if
    # necessary.
    #
    # Subclasses are encouraged to memoize this result.
    @abstractmethod
    def positions(self) -> Iterable[Position]:
        pass

    # Returns historical account activity, loading it if necessary.
    #
    # Subclasses are encouraged to memoize this result.
    @abstractmethod
    def activity(self) -> Iterable[Activity]:
        pass

    # Returns the cash balances in the account, fetching them if necessary.
    #
    # Subclasses are encouraged to memoize this result.
    @abstractmethod
    def balance(self) -> AccountBalance:
        pass

    # Offers access to market data, if provided through this brokerage account.
    @property
    def marketDataProvider(self) -> Optional[MarketDataProvider]:
        return None
