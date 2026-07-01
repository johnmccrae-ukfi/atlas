from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class MarketBar:
    """Canonical Silver-layer OHLCV model for a single market bar."""

    instrument: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    provider: str
    volume: float | None = None

    def __post_init__(self) -> None:
        self._validate_required_fields()
        self._validate_numeric_values()

    def _validate_required_fields(self) -> None:
        if not isinstance(self.instrument, str) or not self.instrument.strip():
            raise ValueError("instrument must be a non-empty string.")

        if not isinstance(self.timestamp, datetime):
            raise ValueError("timestamp must be a datetime value.")

        if self.timestamp.tzinfo is None:
            raise ValueError("timestamp should include timezone information.")

        if not isinstance(self.provider, str) or not self.provider.strip():
            raise ValueError("provider must be a non-empty string.")

    def _validate_numeric_values(self) -> None:
        # TODO: NaN prices/volume currently pass validation (NaN comparisons are always False).
        for field_name, value in (
            ("open", self.open),
            ("high", self.high),
            ("low", self.low),
            ("close", self.close),
        ):
            if value < 0:
                raise ValueError(f"{field_name} must be greater than or equal to zero.")

        if self.volume is not None and self.volume < 0:
            raise ValueError("volume must be greater than or equal to zero when supplied.")

        if self.high < self.low:
            raise ValueError("high must be greater than or equal to low.")

        if not (self.low <= self.open <= self.high):
            raise ValueError("open must be between low and high.")

        if not (self.low <= self.close <= self.high):
            raise ValueError("close must be between low and high.")