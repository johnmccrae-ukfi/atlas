from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv


S3_ENDPOINT_URL = "https://files.massive.com"
S3_BUCKET_NAME = "flatfiles"

EXCHANGES = ("cbot", "cme", "comex", "nymex")
DATASETS = (
    "session_aggs_v1",
    "minute_aggs_v1",
    "trades_v1",
    "quotes_v1",
)

MAX_RECENT_OBJECTS = 5
MAX_DESCENT_LEVELS = 6


@dataclass(frozen=True)
class DatasetProbeResult:
    """Result of probing one documented Massive Futures Flat Files prefix."""

    prefix: str
    accessible: bool
    recent_objects: tuple[dict[str, Any], ...]
    message: str


def create_s3_client(access_key: str, secret_key: str) -> Any:
    """Create a read-only-use S3 client for Massive Flat Files."""

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


def format_size(size_bytes: int) -> str:
    """Format an object size using readable binary units."""

    size = float(size_bytes)

    for unit in ("B", "KiB", "MiB", "GiB"):
        if size < 1024 or unit == "GiB":
            return f"{size:,.2f} {unit}"

        size /= 1024

    return f"{size_bytes:,} B"


def format_timestamp(value: Any) -> str:
    """Format an S3 LastModified value consistently in UTC."""

    if not isinstance(value, datetime):
        return "Unknown"

    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)

    return value.astimezone(timezone.utc).isoformat()


def list_prefix_level(
    s3_client: Any,
    prefix: str,
) -> tuple[list[str], list[dict[str, Any]]]:
    """
    List one logical S3 hierarchy level.

    Delimiter prevents the probe from recursively retrieving every object
    beneath a potentially large historical dataset.
    """

    response = s3_client.list_objects_v2(
        Bucket=S3_BUCKET_NAME,
        Prefix=prefix,
        Delimiter="/",
        MaxKeys=1000,
    )

    child_prefixes = [
        item["Prefix"]
        for item in response.get("CommonPrefixes", [])
        if item.get("Prefix")
    ]

    objects = [
        item
        for item in response.get("Contents", [])
        if item.get("Key") and item["Key"] != prefix
    ]

    return child_prefixes, objects


def find_recent_objects(
    s3_client: Any,
    dataset_prefix: str,
) -> list[dict[str, Any]]:
    """
    Descend through the newest lexicographical folders until files are found.

    Massive Futures keys are date-organised, so choosing the greatest folder
    name at each level should lead to the most recent available partition.
    No object body is requested or downloaded.
    """

    current_prefix = dataset_prefix.rstrip("/") + "/"

    for _ in range(MAX_DESCENT_LEVELS):
        child_prefixes, objects = list_prefix_level(
            s3_client=s3_client,
            prefix=current_prefix,
        )

        if objects:
            return sorted(
                objects,
                key=lambda item: (
                    item.get("LastModified")
                    or datetime.min.replace(tzinfo=timezone.utc),
                    item.get("Key", ""),
                ),
                reverse=True,
            )[:MAX_RECENT_OBJECTS]

        if not child_prefixes:
            return []

        current_prefix = max(child_prefixes)

    return []


def probe_dataset(
    s3_client: Any,
    dataset_prefix: str,
) -> DatasetProbeResult:
    """Probe one known Futures dataset without downloading data."""

    try:
        recent_objects = find_recent_objects(
            s3_client=s3_client,
            dataset_prefix=dataset_prefix,
        )

        if not recent_objects:
            return DatasetProbeResult(
                prefix=dataset_prefix,
                accessible=True,
                recent_objects=(),
                message="Prefix was accessible, but no objects were found.",
            )

        return DatasetProbeResult(
            prefix=dataset_prefix,
            accessible=True,
            recent_objects=tuple(recent_objects),
            message="Accessible.",
        )

    except ClientError as exc:
        error = exc.response.get("Error", {})
        error_code = str(error.get("Code", "Unknown"))
        error_message = str(error.get("Message", str(exc)))

        return DatasetProbeResult(
            prefix=dataset_prefix,
            accessible=False,
            recent_objects=(),
            message=f"{error_code}: {error_message}",
        )

    except BotoCoreError as exc:
        return DatasetProbeResult(
            prefix=dataset_prefix,
            accessible=False,
            recent_objects=(),
            message=f"Boto3 error: {exc}",
        )


def main() -> int:
    """Probe documented Massive Futures Flat Files dataset prefixes."""

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

    dataset_prefixes = [
        f"us_futures_{exchange}/{dataset}"
        for exchange in EXCHANGES
        for dataset in DATASETS
    ]

    print("Massive Futures Flat Files read-only catalogue probe")
    print(f"Endpoint: {S3_ENDPOINT_URL}")
    print(f"Bucket:   {S3_BUCKET_NAME}")
    print(f"Documented dataset prefixes tested: {len(dataset_prefixes)}")
    print("No files will be downloaded.")

    probe_results: list[DatasetProbeResult] = []

    for dataset_prefix in dataset_prefixes:
        result = probe_dataset(
            s3_client=s3_client,
            dataset_prefix=dataset_prefix,
        )
        probe_results.append(result)

        print()
        print("=" * 88)
        print(f"Dataset:    {result.prefix}")
        print(f"Accessible: {'Yes' if result.accessible else 'No'}")
        print(f"Result:     {result.message}")

        for item in result.recent_objects:
            print("-" * 88)
            print(f"Object key:    {item.get('Key')}")
            print(f"Size:          {format_size(int(item.get('Size', 0)))}")
            print(
                "Last modified: "
                f"{format_timestamp(item.get('LastModified'))}"
            )

    accessible_results = [
        result for result in probe_results if result.accessible
    ]

    accessible_with_files = [
        result
        for result in accessible_results
        if result.recent_objects
    ]

    inaccessible_results = [
        result for result in probe_results if not result.accessible
    ]

    print()
    print("=" * 88)
    print("Probe summary")
    print(f"Prefixes tested:                {len(probe_results)}")
    print(f"Accessible prefixes:            {len(accessible_results)}")
    print(f"Accessible prefixes with files: {len(accessible_with_files)}")
    print(f"Inaccessible prefixes:          {len(inaccessible_results)}")

    print()
    print("Accessible datasets containing files:")

    if accessible_with_files:
        for result in accessible_with_files:
            print(f"  - {result.prefix}")
    else:
        print("  None")

    print()
    print("Important: this probe listed metadata only.")
    print("No Flat Files were downloaded.")

    return 0


if __name__ == "__main__":
    sys.exit(main())