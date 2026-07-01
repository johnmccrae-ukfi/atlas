import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from src.common.models.MarketBar import MarketBar
from src.common.providers.MassiveProvider import MassiveProvider


class MassiveProviderTests(unittest.TestCase):
    def test_get_bars_returns_canonical_market_bars(self) -> None:
        provider = MassiveProvider(api_key="test-key")

        class DummyResponse:
            status_code = 200

            def json(self) -> dict:
                return {
                    "bars": [
                        {
                            "timestamp": "2024-01-02T12:00:00Z",
                            "open": 100.0,
                            "high": 102.0,
                            "low": 99.0,
                            "close": 101.5,
                            "volume": 100000.0,
                        }
                    ]
                }

        with patch("src.common.providers.MassiveProvider.requests.get", return_value=DummyResponse()):
            bars = list(provider.get_bars("AAPL", datetime(2024, 1, 2, tzinfo=timezone.utc), datetime(2024, 1, 3, tzinfo=timezone.utc), "1m"))

        self.assertEqual(len(bars), 1)
        self.assertIsInstance(bars[0], MarketBar)
        self.assertEqual(bars[0].instrument, "AAPL")
        self.assertEqual(bars[0].provider, "Massive")
        self.assertEqual(bars[0].volume, 100000.0)

    def test_get_bars_raises_for_invalid_response(self) -> None:
        provider = MassiveProvider(api_key="test-key")

        class DummyResponse:
            status_code = 200

            def json(self) -> dict:
                return {"unexpected": []}

        with patch("src.common.providers.MassiveProvider.requests.get", return_value=DummyResponse()):
            with self.assertRaises(ValueError):
                list(provider.get_bars("AAPL", datetime(2024, 1, 2, tzinfo=timezone.utc), datetime(2024, 1, 3, tzinfo=timezone.utc), "1m"))

    def test_get_bars_raises_for_http_failure(self) -> None:
        provider = MassiveProvider(api_key="test-key")

        class DummyResponse:
            status_code = 500
            text = "internal error"

        with patch("src.common.providers.MassiveProvider.requests.get", return_value=DummyResponse()):
            with self.assertRaises(RuntimeError):
                list(provider.get_bars("AAPL", datetime(2024, 1, 2, tzinfo=timezone.utc), datetime(2024, 1, 3, tzinfo=timezone.utc), "1m"))


if __name__ == "__main__":
    unittest.main()
