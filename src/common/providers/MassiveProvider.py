from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable

import requests

from src.common.models.MarketBar import MarketBar
from src.common.providers.IMarketDataProvider import IMarketDataProvider


class MassiveProvider(IMarketDataProvider):
    """Sprint 1 adapter for the Massive REST API."""

    def __init__(self, api_key: str) -> None:
        if not api_key.strip():
            raise ValueError("api_key must be a non-empty string.")

        self._api_key = api_key
        self._base_url = "https://api.massive.com"
        self._provider_name = "Massive"

    def get_bars(
        self,
        instrument: str,
        start_time: datetime,
        end_time: datetime,
        timeframe: str,
    ) -> Iterable[MarketBar]:

        multiplier, timespan = self._parse_timeframe(timeframe)

        url = (
            f"{self._base_url}/v2/aggs/ticker/{instrument}"
            f"/range/{multiplier}/{timespan}"
            f"/{start_time.date()}/{end_time.date()}"
        )

        params = {
            "adjusted": "true",
            "sort": "asc",
            "limit": 50000,
            "apiKey": self._api_key,
        }

        response = requests.get(url, params=params, timeout=30)

        if response.status_code >= 400:
            raise RuntimeError(
                f"Massive API request failed with status "
                f"{response.status_code}: {response.text}"
            )

        payload = response.json()

        bars_payload = payload.get("results", [])

        return [self._build_market_bar(item, instrument) for item in bars_payload]

    def _parse_timeframe(self, timeframe: str) -> tuple[int, str]:
        mapping = {
            "1m": (1, "minute"),
            "5m": (5, "minute"),
            "15m": (15, "minute"),
            "1h": (1, "hour"),
            "1d": (1, "day"),
        }

        if timeframe not in mapping:
            raise ValueError(f"Unsupported timeframe: {timeframe}")

        return mapping[timeframe]

    def _build_market_bar(self, payload: Any, instrument: str) -> MarketBar:
        if not isinstance(payload, dict):
            raise ValueError("Massive API returned an invalid bar payload.")

        from datetime import datetime, timezone
        timestamp = datetime.fromtimestamp(payload["t"] / 1000, tz=timezone.utc)

        return MarketBar(
            instrument=instrument,
            timestamp=timestamp,
            open=float(payload["o"]),
            high=float(payload["h"]),
            low=float(payload["l"]),
            close=float(payload["c"]),
            volume=float(payload["v"]),
            provider=self._provider_name,
        )