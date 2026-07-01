from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable

from src.common.models.MarketBar import MarketBar


class IMarketDataProvider(ABC):
    """
    Abstract interface for Atlas market data providers.

    Provider implementations convert vendor-specific market data
    into Atlas canonical MarketBar objects.
    """

    @abstractmethod
    def get_bars(
        self,
        instrument: str,
        start_time: datetime,
        end_time: datetime,
        timeframe: str,
    ) -> Iterable[MarketBar]:
        """
        Retrieve OHLCV market bars for an instrument.

        Args:
            instrument: Provider or Atlas instrument symbol.
            start_time: Start of requested period. Must be timezone-aware.
            end_time: End of requested period. Must be timezone-aware.
            timeframe: Bar interval, for example '1m' or '5m'.

        Returns:
            Iterable of provider-normalised MarketBar objects.
        """
        raise NotImplementedError