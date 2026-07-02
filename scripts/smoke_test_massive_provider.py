from datetime import datetime, timezone
import os

from dotenv import load_dotenv

from src.common.providers.MassiveProvider import MassiveProvider


load_dotenv(override=True)

api_key = os.environ["MASSIVE_API_KEY"]

provider = MassiveProvider(api_key=api_key)

bars = provider.get_bars(
    instrument="AAPL",
    start_time=datetime(2025, 1, 2, tzinfo=timezone.utc),
    end_time=datetime(2025, 1, 3, tzinfo=timezone.utc),
    timeframe="1d",
)

print(f"Received {len(bars)} bars")

for bar in bars:
    print(bar)