from __future__ import annotations

import csv
import gzip
import io
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone
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

TARGET_DUPLICATE_KEYS = {
    ("NIYU6", 1783987140000000000),
    ("NKDU6", 1783987140000000000),
}


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


def format_timestamp_ns(timestamp_ns: int) -> str:
    """Convert a Unix nanosecond timestamp into ISO-8601 UTC."""

    timestamp_seconds = timestamp_ns / 1_000_000_000

    return datetime.fromtimestamp(
        timestamp_seconds,
        tz=timezone.utc,
    ).isoformat()


def compare_rows(
    rows: list[dict[str, str]],
    fieldnames: list[str],
) -> dict[str, set[str]]:
    """
    Return fields whose values differ across duplicate source rows.

    Each result contains the distinct source values observed for the field.
    """

    differences: dict[str, set[str]] = {}

    for field_name in fieldnames:
        values = {
            row.get(field_name, "")
            for row in rows
        }

        if len(values) > 1:
            differences[field_name] = values

    return differences


def main() -> int:
    """Inspect known duplicate Massive Futures minute aggregate keys."""

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

    print("Massive Futures minute-aggregate duplicate inspection")
    print(f"Object: {OBJECT_KEY}")
    print(f"Target duplicate keys: {len(TARGET_DUPLICATE_KEYS)}")
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

    if not reader.fieldnames:
        print("The Flat File did not contain a CSV header.")
        return 1

    required_columns = {
        "ticker",
        "window_start",
    }

    missing_columns = sorted(
        required_columns - set(reader.fieldnames)
    )

    if missing_columns:
        print(
            "The Flat File is missing required columns: "
            + ", ".join(missing_columns)
        )
        return 1

    matched_rows: dict[
        tuple[str, int],
        list[dict[str, str]],
    ] = defaultdict(list)

    total_rows = 0

    for row_number, row in enumerate(reader, start=2):
        total_rows += 1

        ticker = (row.get("ticker") or "").strip()
        raw_window_start = (row.get("window_start") or "").strip()

        if not raw_window_start:
            print(
                f"Row {row_number}: window_start is missing."
            )
            return 1

        try:
            window_start = int(raw_window_start)
        except ValueError:
            print(
                f"Row {row_number}: invalid window_start value: "
                f"{raw_window_start}"
            )
            return 1

        grain_key = (ticker, window_start)

        if grain_key in TARGET_DUPLICATE_KEYS:
            source_row = dict(row)
            source_row["_source_csv_row_number"] = str(row_number)
            matched_rows[grain_key].append(source_row)

    print()
    print("=" * 96)
    print("Inspection summary")
    print(f"Rows processed:       {total_rows:,}")
    print(f"Target keys:          {len(TARGET_DUPLICATE_KEYS):,}")
    print(f"Target keys located:  {len(matched_rows):,}")

    unresolved_keys = sorted(
        TARGET_DUPLICATE_KEYS - set(matched_rows)
    )

    if unresolved_keys:
        print()
        print("Target keys not found:")

        for ticker, window_start in unresolved_keys:
            print(
                f"  ticker={ticker}, "
                f"window_start={window_start}"
            )

    identical_duplicate_keys = 0
    conflicting_duplicate_keys = 0
    unexpected_occurrence_keys = 0

    for ticker, window_start in sorted(TARGET_DUPLICATE_KEYS):
        rows = matched_rows.get((ticker, window_start), [])

        print()
        print("=" * 96)
        print(f"Ticker:            {ticker}")
        print(f"Window start:      {window_start}")
        print(
            "Window start UTC:  "
            f"{format_timestamp_ns(window_start)}"
        )
        print(f"Occurrences found: {len(rows)}")

        if not rows:
            print("Result: target key was not found.")
            continue

        for occurrence_number, row in enumerate(rows, start=1):
            print()
            print("-" * 96)
            print(f"Occurrence {occurrence_number}")

            print(
                f"{'_source_csv_row_number':<28}: "
                f"{row.get('_source_csv_row_number')}"
            )

            for field_name in reader.fieldnames:
                print(
                    f"{field_name:<28}: "
                    f"{row.get(field_name)}"
                )

        if len(rows) != 2:
            unexpected_occurrence_keys += 1

        differences = compare_rows(
            rows=rows,
            fieldnames=reader.fieldnames,
        )

        print()
        print("Comparison result")

        if not differences:
            identical_duplicate_keys += 1
            print(
                "The source rows are identical across all "
                "11 provider columns."
            )
        else:
            conflicting_duplicate_keys += 1
            print(
                "The source rows conflict in the following fields:"
            )

            for field_name, values in differences.items():
                print(f"  {field_name}:")

                for value in sorted(values):
                    print(f"    - {value}")

    print()
    print("=" * 96)
    print("Duplicate classification summary")
    print(
        "Identical duplicate keys:       "
        f"{identical_duplicate_keys:,}"
    )
    print(
        "Conflicting duplicate keys:     "
        f"{conflicting_duplicate_keys:,}"
    )
    print(
        "Unexpected occurrence counts:   "
        f"{unexpected_occurrence_keys:,}"
    )

    if (
        identical_duplicate_keys == len(TARGET_DUPLICATE_KEYS)
        and conflicting_duplicate_keys == 0
        and unexpected_occurrence_keys == 0
    ):
        print()
        print(
            "Conclusion: all inspected duplicate keys contain exactly "
            "two byte-equivalent logical source records across the "
            "provider columns."
        )
        print(
            "This supports exact-row deduplication for these samples, "
            "but does not yet establish a general provider correction "
            "or revision rule."
        )

    elif conflicting_duplicate_keys > 0:
        print()
        print(
            "Conclusion: at least one duplicate business-grain key "
            "contains conflicting provider values."
        )
        print(
            "Do not apply arbitrary deduplication until an explicit "
            "correction or precedence rule has been designed."
        )

    else:
        print()
        print(
            "Conclusion: the observed duplicate pattern requires "
            "further investigation before a general rule is defined."
        )

    print()
    print("Inspection complete.")
    print("No Flat File was persisted locally.")

    return 0


if __name__ == "__main__":
    sys.exit(main())