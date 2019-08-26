import unittest
from pathlib import Path
from typing import List

from hypothesis import given
from hypothesis.strategies import from_type, lists

from bankroll.broker import AccountAggregator, AccountData
from bankroll.broker.configuration import Settings
from bankroll.model import AccountBalance, Activity, Position

from tests import helpers


class TestAccountAggregator(unittest.TestCase):
    @given(lists(from_type(AccountData)))
    def testDataAddsUp(self, accounts: List[AccountData]) -> None:
        aggregator = AccountAggregator(accounts, lenient=False)
        instruments = set((p.instrument for p in aggregator.positions()))

        balance = AccountBalance(cash={})
        for account in accounts:
            balance += account.balance()

            for p in account.positions():
                self.assertIn(
                    p.instrument,
                    instruments,
                    msg=f"Expected {p} from {account} to show up in aggregated data",
                )

            for a in account.activity():
                self.assertIn(
                    a,
                    aggregator.activity(),
                    msg=f"Expected {a} from {account} to show up in aggregated data",
                )

        self.assertEqual(aggregator.balance(), balance)
