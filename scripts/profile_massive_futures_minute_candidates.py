from __future__ import annotations

import csv
import gzip
import io
import os
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv


S3_ENDPOINT_URL = "https://files.massive.com"
S3_BUCKET_NAME = "flatfiles"

OBJECT_KEY = (
    "us_futures_cme/minute_aggs_v1/"
    "2026/07/2026-07-14.csv.gz"
)

CURRENT_ATLAS_TICKER = "MESU6"

PRICE_COLUMNS = ("open", "high", "low", "close")

MIN_CANDIDATE_ROWS = 1_300
MAX_CANDIDATES = 20
MAX_DUPLICATE_SAMPLES = 10
MAX_HIGH_PRECISION_SAMPLES = 10


@dataclass
class TickerProfile:
    """Aggregated profile for one Massive provider ticker."""

    row_count: int = 0
    total_volume: int = 0
    total_transactions: int = 0
    earliest_window_start: int | None = None
    latest_window_start: int | None = None
    maximum_meaningful_price_scale: int = 0


def create_s3_client(access_key: str, secret_key: str) -> Any:
    """Create an S3 client for Massive Flat Files."""

    return boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(
            signature_version="s3v4",
            retries={
                "max_attempts": 3,
                "mode": "standard",
            },
        ),
    )


def meaningful_decimal_scale(raw_value: str | None) -> int | None:
    """
    Return the meaningful decimal scale after removing trailing zeroes.

    Examples:
        7558.250000000 -> 2
        0.186000000    -> 3
        42.000000000   -> 0
    """

    if raw_value is None or raw_value == "":
        return None

    try:
        value = Decimal(raw_value)
    except InvalidOperation:
        return None

    normalised_value = value.normalize()

    if normalised_value == normalised_value.to_integral():
        return 0

    return max(-normalised_value.as_tuple().exponent, 0)


def parse_non_negative_int(
    raw_value: str | None,
    column_name: str,
    row_number: int,
) -> int:
    """Parse a required non-negative integer field."""

    if raw_value is None or raw_value == "":
        raise ValueError(
            f"Row {row_number}: {column_name} is missing."
        )

    try:
        value = int(raw_value)
    except ValueError as exc:
        raise ValueError(
            f"Row {row_number}: {column_name} is not an integer: "
            f"{raw_value}"
        ) from exc

    if value < 0:
        raise ValueError(
            f"Row {row_number}: {column_name} is negative: {value}"
        )

    return value


def main() -> int:
    """Profile Massive CME minute aggregates for v1.3.0 discovery."""

    load_dotenv()

    access_key = os.getenv("MASSIVE_S3_ACCESS_KEY", "").strip()
    secret_key = os.getenv("MASSIVE_S3_SECRET_KEY", "").strip()

    if (
        not access_key
        or access_key == "your_massive_s3_access_key_here"
    ):
        print(
            "Error: MASSIVE_S3_ACCESS_KEY is missing or still contains "
            "the placeholder value."
        )
        return 1

    if (
        not secret_key
        or secret_key == "your_massive_s3_secret_key_here"
    ):
        print(
            "Error: MASSIVE_S3_SECRET_KEY is missing or still contains "
            "the placeholder value."
        )
        return 1

    s3_client = create_s3_client(
        access_key=access_key,
        secret_key=secret_key,
    )

    print("Massive Futures minute-aggregate candidate profiling")
    print(f"Object: {OBJECT_KEY}")
    print("The file will be processed in memory.")
    print("No market-data file will be written to disk.")

    try:
        response = s3_client.get_object(
            Bucket=S3_BUCKET_NAME,
            Key=OBJECT_KEY,
        )
        compressed_bytes = response["Body"].read()

    except ClientError as exc:
        error = exc.response.get("Error", {})
        print(
            "Massive Flat File retrieval failed: "
            f"{error.get('Code', 'Unknown')}: "
            f"{error.get('Message', str(exc))}"
        )
        return 1

    except BotoCoreError as exc:
        print(f"Massive Flat File retrieval failed: {exc}")
        return 1

    try:
        csv_bytes = gzip.decompress(compressed_bytes)
        csv_text = csv_bytes.decode("utf-8-sig")
    except (gzip.BadGzipFile, UnicodeDecodeError) as exc:
        print(f"Unable to decompress or decode the Flat File: {exc}")
        return 1

    reader = csv.DictReader(io.StringIO(csv_text))

    required_columns = {
        "ticker",
        "exchange",
        "session_end_date",
        "window_start",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "transactions",
    }

    actual_columns = set(reader.fieldnames or [])
    missing_columns = sorted(required_columns - actual_columns)

    if missing_columns:
        print(
            "The Flat File is missing required columns: "
            + ", ".join(missing_columns)
        )
        return 1

    profiles: dict[str, TickerProfile] = defaultdict(TickerProfile)
    grain_counts: Counter[tuple[str, int]] = Counter()
    exchange_counts: Counter[str] = Counter()
    session_end_date_counts: Counter[str] = Counter()
    meaningful_scale_counts: Counter[int] = Counter()

    duplicate_samples: list[tuple[str, int]] = []
    high_precision_samples: list[
        tuple[str, str, str, int]
    ] = []

    total_rows = 0
    invalid_ohlc_rows = 0

    for row_number, row in enumerate(reader, start=2):
        total_rows += 1

        ticker = (row.get("ticker") or "").strip()
        exchange = (row.get("exchange") or "").strip()
        session_end_date = (
            row.get("session_end_date") or ""
        ).strip()

        if not ticker:
            print(f"Row {row_number}: ticker is missing.")
            return 1

        window_start = parse_non_negative_int(
            row.get("window_start"),
            "window_start",
            row_number,
        )

        volume = parse_non_negative_int(
            row.get("volume"),
            "volume",
            row_number,
        )

        transactions = parse_non_negative_int(
            row.get("transactions"),
            "transactions",
            row_number,
        )

        grain_key = (ticker, window_start)
        grain_counts[grain_key] += 1

        if (
            grain_counts[grain_key] == 2
            and len(duplicate_samples) < MAX_DUPLICATE_SAMPLES
        ):
            duplicate_samples.append(grain_key)

        exchange_counts[exchange] += 1
        session_end_date_counts[session_end_date] += 1

        profile = profiles[ticker]
        profile.row_count += 1
        profile.total_volume += volume
        profile.total_transactions += transactions

        if (
            profile.earliest_window_start is None
            or window_start < profile.earliest_window_start
        ):
            profile.earliest_window_start = window_start

        if (
            profile.latest_window_start is None
            or window_start > profile.latest_window_start
        ):
            profile.latest_window_start = window_start

        decimal_prices: dict[str, Decimal] = {}

        for price_column in PRICE_COLUMNS:
            raw_price = row.get(price_column)

            try:
                decimal_price = Decimal(raw_price or "")
            except InvalidOperation:
                print(
                    f"Row {row_number}: invalid {price_column} "
                    f"value: {raw_price}"
                )
                return 1

            decimal_prices[price_column] = decimal_price

            scale = meaningful_decimal_scale(raw_price)

            if scale is not None:
                meaningful_scale_counts[scale] += 1

                profile.maximum_meaningful_price_scale = max(
                    profile.maximum_meaningful_price_scale,
                    scale,
                )

                if (
                    scale > 5
                    and len(high_precision_samples)
                    < MAX_HIGH_PRECISION_SAMPLES
                ):
                    high_precision_samples.append(
                        (
                            ticker,
                            price_column,
                            raw_price or "",
                            scale,
                        )
                    )

        open_price = decimal_prices["open"]
        high_price = decimal_prices["high"]
        low_price = decimal_prices["low"]
        close_price = decimal_prices["close"]

        if not (
            high_price >= open_price
            and high_price >= close_price
            and high_price >= low_price
            and low_price <= open_price
            and low_price <= close_price
        ):
            invalid_ohlc_rows += 1

    duplicate_keys = sum(
        1
        for occurrence_count in grain_counts.values()
        if occurrence_count > 1
    )

    duplicate_extra_rows = sum(
        occurrence_count - 1
        for occurrence_count in grain_counts.values()
        if occurrence_count > 1
    )

    candidates = [
        (ticker, profile)
        for ticker, profile in profiles.items()
        if ticker != CURRENT_ATLAS_TICKER
        and profile.row_count >= MIN_CANDIDATE_ROWS
    ]

    candidates.sort(
        key=lambda item: (
            item[1].row_count,
            item[1].total_transactions,
            item[1].total_volume,
        ),
        reverse=True,
    )

    tickers_over_five_decimal_places = sorted(
        ticker
        for ticker, profile in profiles.items()
        if profile.maximum_meaningful_price_scale > 5
    )

    print()
    print("=" * 96)
    print("Dataset grain validation")
    print(f"Rows processed:              {total_rows:,}")
    print(f"Unique tickers:              {len(profiles):,}")
    print(f"Unique grain keys:           {len(grain_counts):,}")
    print(f"Duplicate grain keys:        {duplicate_keys:,}")
    print(f"Duplicate additional rows:   {duplicate_extra_rows:,}")
    print(f"Invalid OHLC rows:           {invalid_ohlc_rows:,}")

    if duplicate_samples:
        print()
        print("Duplicate grain-key samples:")

        for ticker, window_start in duplicate_samples:
            print(
                f"  ticker={ticker}, "
                f"window_start={window_start}, "
                f"occurrences={grain_counts[(ticker, window_start)]}"
            )

    print()
    print("=" * 96)
    print("Provider session and venue values")

    print("Exchange values:")
    for exchange, count in exchange_counts.most_common():
        print(f"  {exchange or '<blank>':<16} {count:>12,}")

    print("Session end dates:")
    for session_end_date, count in session_end_date_counts.most_common():
        print(
            f"  {session_end_date or '<blank>':<16} "
            f"{count:>12,}"
        )

    print()
    print("=" * 96)
    print("Meaningful OHLC decimal scale")

    for scale, count in sorted(meaningful_scale_counts.items()):
        print(f"  Scale {scale}: {count:>12,} values")

    print(
        "Tickers requiring more than five meaningful decimal places: "
        f"{len(tickers_over_five_decimal_places):,}"
    )

    if tickers_over_five_decimal_places:
        preview = ", ".join(tickers_over_five_decimal_places[:30])
        print(f"Ticker preview: {preview}")

    if high_precision_samples:
        print()
        print("Values exceeding five meaningful decimal places:")

        for ticker, column_name, value, scale in high_precision_samples:
            print(
                f"  {ticker:<12} "
                f"{column_name:<6} "
                f"value={value:<20} "
                f"scale={scale}"
            )

    print()
    print("=" * 96)
    print(
        "Candidate contracts with at least "
        f"{MIN_CANDIDATE_ROWS:,} minute rows"
    )

    print(
        f"{'Ticker':<12}"
        f"{'Rows':>10}"
        f"{'Volume':>18}"
        f"{'Transactions':>18}"
        f"{'Max scale':>12}"
    )
    print("-" * 96)

    for ticker, profile in candidates[:MAX_CANDIDATES]:
        print(
            f"{ticker:<12}"
            f"{profile.row_count:>10,}"
            f"{profile.total_volume:>18,}"
            f"{profile.total_transactions:>18,}"
            f"{profile.maximum_meaningful_price_scale:>12}"
        )

    print()
    print(f"Current Atlas ticker: {CURRENT_ATLAS_TICKER}")

    current_profile = profiles.get(CURRENT_ATLAS_TICKER)

    if current_profile is None:
        print("Current Atlas ticker was not found.")
    else:
        print(
            f"Rows={current_profile.row_count:,}, "
            f"Volume={current_profile.total_volume:,}, "
            f"Transactions={current_profile.total_transactions:,}, "
            "Maximum meaningful price scale="
            f"{current_profile.maximum_meaningful_price_scale}"
        )

    print()
    print("Profiling complete.")
    print("No Flat File was persisted locally.")

    return 0


if __name__ == "__main__":
    sys.exit(main())