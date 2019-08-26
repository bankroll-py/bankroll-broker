import os
import unittest
from typing import Any, Iterable, no_type_check

from bankroll.broker.parsetools import lenientParse
from hypothesis import given, reproduce_failure
from hypothesis.strategies import (
    booleans,
    decimals,
    integers,
    iterables,
    none,
    nothing,
    one_of,
    text,
)


def failingTransform(_: Any) -> Any:
    raise ValueError("Transform failed!")


class TestParsetools(unittest.TestCase):
    @no_type_check
    @given(iterables(one_of(decimals(), integers(), none(), text()), min_size=1))
    def test_lenientParseNonLenient(self, i: Iterable[Any]) -> None:
        with self.assertRaises(ValueError):
            list(lenientParse(i, transform=failingTransform, lenient=False))

    @no_type_check
    @given(iterables(nothing(), max_size=0), booleans())
    def test_lenientParseEmpty(self, i: Iterable[Any], lenient: bool) -> None:
        result = list(lenientParse(i, transform=failingTransform, lenient=lenient))
        self.assertEqual(result, [])

    @no_type_check
    @given(iterables(one_of(decimals(), integers(), none(), text()), min_size=1))
    def test_lenientParseLenient(self, i: Iterable[Any]) -> None:
        with self.assertWarns(RuntimeWarning) as cm:
            result = list(lenientParse(i, transform=failingTransform, lenient=True))

        self.assertEqual(result, [])
        self.assertIn(os.path.basename(__file__), cm.filename)
