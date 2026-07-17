from __future__ import annotations

import csv
import gzip
import io
import os
import sys
from collections import Counter
from datetime import datetime, timezone
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

TARGET_TICKER = "MESU6"
MAX_SAMPLE_ROWS = 5


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


def format_timestamp_ns(raw_value: str | None) -> str:
    """Convert a nanosecond Unix timestamp to an ISO-8601 UTC value."""

    if not raw_value:
        return "None"

    try:
        timestamp_ns = int(raw_value)
    except ValueError:
        return f"Unrecognised timestamp: {raw_value}"

    timestamp_seconds = timestamp_ns / 1_000_000_000

    return datetime.fromtimestamp(
        timestamp_seconds,
        tz=timezone.utc,
    ).isoformat()


def infer_decimal_scale(raw_value: str | None) -> int | None:
    """Return the number of decimal places represented by a numeric value."""

    if raw_value is None or raw_value == "":
        return None

    try:
        decimal_value = Decimal(raw_value)
    except InvalidOperation:
        return None

    exponent = decimal_value.as_tuple().exponent
    return max(-exponent, 0)


def main() -> int:
    """Retrieve and inspect one Massive CME minute-aggregate Flat File."""

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

    print("Massive Futures minute-aggregate Flat File inspection")
    print(f"Endpoint:      {S3_ENDPOINT_URL}")
    print(f"Bucket:        {S3_BUCKET_NAME}")
    print(f"Object:        {OBJECT_KEY}")
    print(f"Target ticker: {TARGET_TICKER}")
    print("The compressed object will be processed in memory.")
    print("No market-data file will be written to disk.")

    try:
        response = s3_client.get_object(
            Bucket=S3_BUCKET_NAME,
            Key=OBJECT_KEY,
        )

        compressed_bytes = response["Body"].read()

    except ClientError as exc:
        error = exc.response.get("Error", {})
        error_code = error.get("Code", "Unknown")
        error_message = error.get("Message", str(exc))

        print(
            f"Massive Flat File retrieval failed: "
            f"{error_code}: {error_message}"
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

    if not reader.fieldnames:
        print("The Flat File did not contain a CSV header.")
        return 1

    ticker_counts: Counter[str] = Counter()
    target_rows: list[dict[str, str]] = []

    row_count = 0
    null_counts = Counter()
    observed_decimal_scales = {
        "open": set(),
        "high": set(),
        "low": set(),
        "close": set(),
    }

    first_row: dict[str, str] | None = None
    last_row: dict[str, str] | None = None

    for row in reader:
        row_count += 1

        if first_row is None:
            first_row = dict(row)

        last_row = dict(row)

        ticker = (
            row.get("ticker")
            or row.get("symbol")
            or ""
        ).strip()

        if ticker:
            ticker_counts[ticker] += 1

        if ticker == TARGET_TICKER and len(target_rows) < MAX_SAMPLE_ROWS:
            target_rows.append(dict(row))

        for column_name, value in row.items():
            if value is None or value == "":
                null_counts[column_name] += 1

        for price_column in observed_decimal_scales:
            scale = infer_decimal_scale(row.get(price_column))

            if scale is not None:
                observed_decimal_scales[price_column].add(scale)

    print()
    print("=" * 88)
    print("CSV schema")
    print(f"Columns returned: {len(reader.fieldnames)}")

    for index, column_name in enumerate(reader.fieldnames, start=1):
        print(f"{index:>2}. {column_name}")

    print()
    print("=" * 88)
    print("File profile")
    print(f"Compressed size:       {len(compressed_bytes):,} bytes")
    print(f"Decompressed size:     {len(csv_bytes):,} bytes")
    print(f"Data rows:             {row_count:,}")
    print(f"Unique tickers:        {len(ticker_counts):,}")
    print(
        f"{TARGET_TICKER} rows:          "
        f"{ticker_counts.get(TARGET_TICKER, 0):,}"
    )

    print()
    print("Most frequent tickers:")

    for ticker, count in ticker_counts.most_common(10):
        print(f"  {ticker:<16} {count:>10,}")

    print()
    print("=" * 88)
    print("Null or blank values")

    nulls_found = False

    for column_name in reader.fieldnames:
        null_count = null_counts.get(column_name, 0)

        if null_count:
            nulls_found = True
            print(f"  {column_name:<24} {null_count:>10,}")

    if not nulls_found:
        print("  None detected.")

    print()
    print("=" * 88)
    print("Observed price scales")

    for column_name, scales in observed_decimal_scales.items():
        formatted_scales = (
            ", ".join(str(scale) for scale in sorted(scales))
            if scales
            else "No numeric values detected"
        )

        print(f"  {column_name:<8}: {formatted_scales}")

    print()
    print("=" * 88)
    print(f"Sample {TARGET_TICKER} rows")

    if not target_rows:
        print(f"No rows were found for {TARGET_TICKER}.")
    else:
        for sample_number, row in enumerate(target_rows, start=1):
            print("-" * 88)
            print(f"Sample row: {sample_number}")

            for column_name in reader.fieldnames:
                print(f"{column_name:<24}: {row.get(column_name)}")

            timestamp_value = (
                row.get("window_start")
                or row.get("timestamp")
            )

            if timestamp_value:
                print(
                    f"{'window_start_utc':<24}: "
                    f"{format_timestamp_ns(timestamp_value)}"
                )

    print()
    print("=" * 88)
    print("Boundary rows")

    if first_row:
        print("First row:")
        print(first_row)

    if last_row:
        print()
        print("Last row:")
        print(last_row)

    print()
    print("Inspection complete.")
    print("No Flat File was persisted locally.")

    return 0


if __name__ == "__main__":
    sys.exit(main())