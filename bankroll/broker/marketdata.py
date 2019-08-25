from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from itertools import permutations
from typing import Any, Iterable, Optional, Tuple, TypeVar

from bankroll.model import Cash, Instrument, Quote


class MarketDataProvider(ABC):
    # Fetches up-to-date quotes for the provided instruments.
    # May return the results in any order.
    @abstractmethod
    def fetchQuotes(
        self, instruments: Iterable[Instrument]
    ) -> Iterable[Tuple[Instrument, Quote]]:
        pass

    def fetchHistoricalData(self, instrument: Instrument) -> Any:  # pd.DataFrame
        pass
