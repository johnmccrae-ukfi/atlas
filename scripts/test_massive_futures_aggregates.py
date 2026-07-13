from __future__ import annotations

import os
import sys
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv


API_URL = "https://api.massive.com/futures/v1/aggs/MESU6"


def format_timestamp_ns(timestamp_ns: int | None) -> str:
    if timestamp_ns is None:
        return "None"

    timestamp_seconds = timestamp_ns / 1_000_000_000
    return datetime.fromtimestamp(
        timestamp_seconds,
        tz=timezone.utc,
    ).isoformat()


def main() -> int:
    load_dotenv()

    api_key = os.getenv("MASSIVE_API_KEY")

    if not api_key or api_key == "your_massive_api_key_here":
        print("Error: MASSIVE_API_KEY is missing or still contains the placeholder value.")
        return 1

    params = {
        "resolution": "1min",
        "limit": 10,
        "sort": "window_start.desc",
        "apiKey": api_key,
    }

    print("Requesting recent 1-minute aggregates for MESU6...")

    try:
        response = requests.get(API_URL, params=params, timeout=30)

        if not response.ok:
            print(f"Massive API request failed with status {response.status_code}.")
            print(f"Response body: {response.text}")
            return 1

    except requests.RequestException as exc:
        print(f"Massive API request failed: {exc}")
        return 1

    try:
        payload = response.json()
    except requests.JSONDecodeError:
        print("Massive returned a response that was not valid JSON.")
        print(response.text)
        return 1

    results = payload.get("results", [])

    print(f"Aggregate bars returned: {len(results)}")

    if not results:
        print("No aggregate bars were returned.")
        print(payload)
        return 1

    # Display the bars in chronological order for easier reading.
    results = sorted(
        results,
        key=lambda bar: bar.get("window_start", 0),
    )

    for bar in results:
        print("-" * 78)
        print(f"Ticker:            {bar.get('ticker')}")
        print(f"Window start UTC:  {format_timestamp_ns(bar.get('window_start'))}")
        print(f"Session end date:  {bar.get('session_end_date')}")
        print(f"Open:              {bar.get('open')}")
        print(f"High:              {bar.get('high')}")
        print(f"Low:               {bar.get('low')}")
        print(f"Close:             {bar.get('close')}")
        print(f"Volume:            {bar.get('volume')}")
        print(f"Transactions:      {bar.get('transactions')}")
        print(f"Dollar volume:     {bar.get('dollar_volume')}")

    return 0


if __name__ == "__main__":
    sys.exit(main())