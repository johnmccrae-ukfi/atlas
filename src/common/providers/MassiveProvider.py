from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable

import requests

from src.common.models.MarketBar import MarketBar
from src.common.providers.IMarketDataProvider import IMarketDataProvider


class MassiveProvider(IMarketDataProvider):
    """Sprint 1 adapter for the Massive REST API.

    The implementation stays provider-specific internally and translates
    provider responses into Atlas canonical MarketBar objects.
    """

    def __init__(self, api_key: str) -> None:
        if not api_key.strip():
            raise ValueError("api_key must be a non-empty string.")

        self._api_key = api_key
        self._base_url = "https://api.massive.example/v1/bars"
        self._provider_name = "Massive"

    def get_bars(
        self,
        instrument: str,
        start_time: datetime,
        end_time: datetime,
        timeframe: str,
    ) -> Iterable[MarketBar]:
        """Fetch OHLCV bars for an instrument and return canonical MarketBar objects."""
        if not isinstance(instrument, str) or not instrument.strip():
            raise ValueError("instrument must be a non-empty string.")

        if start_time.tzinfo is None or end_time.tzinfo is None:
            raise ValueError("start_time and end_time must be timezone-aware datetimes.")

        params = {
            "symbol": instrument,
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
            "timeframe": timeframe,
        }

        response = requests.get(
            self._base_url,
            params=params,
            headers={"Authorization": f"Bearer {self._api_key}"},
            timeout=10,
        )

        if response.status_code >= 400:
            raise RuntimeError(f"Massive API request failed with status {response.status_code}: {getattr(response, 'text', '')}")

        try:
            payload = response.json()
        except ValueError as exc:
            raise ValueError("Massive API returned an invalid JSON response.") from exc

        if not isinstance(payload, dict):
            raise ValueError("Massive API returned an invalid response payload.")

        bars_payload = payload.get("bars")
        if not isinstance(bars_payload, list):
            raise ValueError("Massive API response did not contain a bars list.")

        return [self._build_market_bar(item, instrument) for item in bars_payload]

    def _build_market_bar(self, payload: Any, instrument: str) -> MarketBar:
        if not isinstance(payload, dict):
            raise ValueError("Massive API returned an invalid bar payload.")

        try:
            timestamp = datetime.fromisoformat(str(payload["timestamp"]).replace("Z", "+00:00"))
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("Massive API returned a bar with an invalid timestamp.") from exc

        try:
            return MarketBar(
                instrument=instrument,
                timestamp=timestamp,
                open=float(payload["open"]),
                high=float(payload["high"]),
                low=float(payload["low"]),
                close=float(payload["close"]),
                volume=float(payload["volume"]),
                provider=self._provider_name,
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("Massive API returned a bar with invalid OHLCV values.") from exc
