from datetime import datetime, timezone
import os

from dotenv import load_dotenv

from src.common.providers.MassiveProvider import MassiveProvider
from common.transformers.market_bar_dataframe_transformer import (
    market_bars_to_dataframe,
)
from src.common.storage.parquet_writer import write_dataframe_to_parquet

load_dotenv(override=True)

api_key = os.environ["MASSIVE_API_KEY"]

provider = MassiveProvider(api_key=api_key)

bars = provider.get_bars(
    instrument="AAPL",
    start_time=datetime(2025, 1, 2, tzinfo=timezone.utc),
    end_time=datetime(2025, 1, 3, tzinfo=timezone.utc),
    timeframe="1d",
)

df = market_bars_to_dataframe(bars)

print(df)
print()
print(df.dtypes)

output_path = (
    "data/bronze/market_bars/"
    "aapl_2025_01_02_2025_01_03.parquet"
)

write_dataframe_to_parquet(df, output_path)

print(f"Written Parquet file to: {output_path}")