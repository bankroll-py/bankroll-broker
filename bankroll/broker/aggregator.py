import operator
from functools import reduce
from itertools import chain, groupby
from typing import Dict, Iterable, Mapping, Optional, Sequence

from bankroll.model import AccountBalance, Activity, Position

from .account import AccountData
from .configuration import Configuration, Settings


class AccountAggregator(AccountData):
    @classmethod
    def allSettings(cls, config: Configuration) -> Dict[Settings, str]:
        return dict(
            chain.from_iterable(
                (
                    config.section(settingsCls).items()
                    for settingsCls in Settings.__subclasses__()
                )
            )
        )

    @classmethod
    def fromSettings(
        cls, settings: Mapping[Settings, str], lenient: bool
    ) -> "AccountAggregator":
        return AccountAggregator(
            accounts=(
                accountCls.fromSettings(settings, lenient=lenient)
                for accountCls in AccountData.__subclasses__()
                if not issubclass(accountCls, AccountAggregator)
            ),
            lenient=lenient,
        )

    def __init__(self, accounts: Iterable[AccountData], lenient: bool):
        self._accounts = list(accounts)
        self._lenient = lenient
        super().__init__()

    def _deduplicatePositions(
        self, positions: Iterable[Position]
    ) -> Iterable[Position]:
        return (
            reduce(operator.add, ps)
            for i, ps in groupby(
                sorted(positions, key=lambda p: p.instrument),
                key=lambda p: p.instrument,
            )
        )

    def positions(self) -> Iterable[Position]:
        # TODO: Memoize the result of deduplication?
        return self._deduplicatePositions(
            chain.from_iterable((account.positions() for account in self._accounts))
        )

    def activity(self) -> Iterable[Activity]:
        return chain.from_iterable((account.activity() for account in self._accounts))

    def balance(self) -> AccountBalance:
        return reduce(
            operator.add,
            (account.balance() for account in self._accounts),
            AccountBalance(cash={}),
        )

    @property
    def accounts(self) -> Sequence[AccountData]:
        return self._accounts
