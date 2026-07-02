from collections.abc import Iterable

import pandas as pd

from src.common.models.MarketBar import MarketBar


def market_bars_to_dataframe(bars: Iterable[MarketBar]) -> pd.DataFrame:
    rows = [
        {
            "instrument": bar.instrument,
            "timestamp": bar.timestamp,
            "open": bar.open,
            "high": bar.high,
            "low": bar.low,
            "close": bar.close,
            "volume": bar.volume,
            "provider": bar.provider,
        }
        for bar in bars
    ]

    return pd.DataFrame(rows)