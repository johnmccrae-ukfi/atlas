from datetime import datetime, timezone
import unittest

from src.common.models.MarketBar import MarketBar


def make_bar(**overrides):
    fields = {
        "instrument": "AAPL",
        "timestamp": datetime(2024, 1, 2, 12, 0, tzinfo=timezone.utc),
        "open": 100.0,
        "high": 102.0,
        "low": 99.0,
        "close": 101.5,
        "provider": "ExampleProvider",
        "volume": 100000.0,
    }
    fields.update(overrides)
    return MarketBar(**fields)


class MarketBarTests(unittest.TestCase):
    def test_valid_bar_is_created(self) -> None:
        bar = make_bar()

        self.assertEqual(bar.instrument, "AAPL")
        self.assertEqual(bar.provider, "ExampleProvider")
        self.assertEqual(bar.volume, 100000.0)

    def test_valid_bar_without_volume_is_created(self) -> None:
        bar = make_bar(volume=None)

        self.assertIsNone(bar.volume)

    def test_bar_is_immutable(self) -> None:
        bar = make_bar()

        with self.assertRaises(AttributeError):
            bar.close = 999.0

    def test_empty_instrument_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            make_bar(instrument="  ")

    def test_empty_provider_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            make_bar(provider="  ")

    def test_non_datetime_timestamp_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            make_bar(timestamp="2024-01-02T12:00:00Z")

    def test_naive_timestamp_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            make_bar(timestamp=datetime(2024, 1, 2, 12, 0))

    def test_negative_open_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            make_bar(open=-1.0, high=102.0, low=99.0, close=101.0)

    def test_negative_volume_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            make_bar(volume=-1.0)

    def test_high_below_low_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            make_bar(high=90.0, low=95.0, open=92.0, close=93.0)

    def test_open_outside_low_high_range_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            make_bar(open=105.0, high=102.0, low=99.0, close=101.0)

    def test_close_outside_low_high_range_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            make_bar(close=105.0, high=102.0, low=99.0, open=101.0)


if __name__ == "__main__":
    unittest.main()
