import unittest
from argparse import ArgumentParser
from enum import unique

from bankroll.broker.configuration import (
    Configuration,
    Settings,
    addSettingsToArgumentGroup,
)
from hypothesis import given
from hypothesis.strategies import from_type, sampled_from, text

from tests import helpers


@unique
class TestSettings(Settings):
    INT_KEY = "Some integer"
    STR_KEY = "String key"

    @classmethod
    def sectionName(cls) -> str:
        return "Test"

class TestConfiguration(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Configuration(["tests/bankroll.test.ini"])

    def testSettingsApplied(self) -> None:
        settings = self.config.section(TestSettings)
        self.assertEqual(settings[TestSettings.INT_KEY], "1234")
        self.assertEqual(settings[TestSettings.STR_KEY], "foobar")

    @given(sampled_from(TestSettings), text(min_size=1))
    def testOverrides(self, key: TestSettings, value: str) -> None:
        defaultSettings = self.config.section(TestSettings)

        settings = self.config.section(TestSettings, overrides={key: value})
        self.assertNotEqual(settings, defaultSettings)
        self.assertEqual(settings[key], value)

        for otherKey in list(TestSettings):
            if key == otherKey:
                continue

            self.assertEqual(settings[otherKey], defaultSettings[otherKey])

    def testAddSettingsToArgumentGroup(self) -> None:
        parser = ArgumentParser()
        readSettings = addSettingsToArgumentGroup(TestSettings, parser)

        values = self.config.section(TestSettings)

        self.assertEqual(readSettings(self.config, parser.parse_args([])), values)

        values[TestSettings.INT_KEY] = "5"
        self.assertEqual(
            readSettings(self.config, parser.parse_args(["--test-some-integer", "5"])),
            values,
        )

        values[TestSettings.STR_KEY] = "fuzzbuzz"
        self.assertEqual(
            readSettings(
                self.config,
                parser.parse_args(
                    ["--test-some-integer", "5", "--test-string-key", "fuzzbuzz"]
                ),
            ),
            values,
        )
