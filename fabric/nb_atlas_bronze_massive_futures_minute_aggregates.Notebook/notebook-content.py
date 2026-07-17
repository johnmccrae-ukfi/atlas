# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "3691f7ef-8726-4cdd-a6df-ac92e8f2a972",
# META       "default_lakehouse_name": "lh_atlas_dev",
# META       "default_lakehouse_workspace_id": "7da777a8-e7db-4c0a-9423-3c91eaad9dda",
# META       "known_lakehouses": [
# META         {
# META           "id": "3691f7ef-8726-4cdd-a6df-ac92e8f2a972"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Atlas Market Data Platform
# 
# ## Massive Futures Historical Bronze Ingestion
# 
# **Notebook:** `nb_atlas_bronze_massive_futures_minute_aggregates`
# 
# **Purpose:**  
# Retrieve one explicitly configured Massive Futures minute-aggregate Flat File and create the source-aligned Bronze dataset for the first controlled multi-instrument scope.
# 
# **Source dataset:**
# 
# ```text
# us_futures_cme/minute_aggs_v1
# ```
# 
# **Initial source object:**
# 
# ```text
# us_futures_cme/minute_aggs_v1/2026/07/2026-07-14.csv.gz
# ```
# 
# **Initial selected contracts:**
# 
# ```text
# MESU6
# MNQU6
# ```
# 
# **Output:**
# 
# ```text
# Tables/bronze_massive_futures_minute_aggregates
# ```
# 
# **Contract:**
# 
# ```text
# docs/01_Architecture/Massive_Futures_Bronze_Contract.md
# ```
# 
# ---
# 
# ## Engineering Rules
# 
# - One Bronze row represents one accepted physical CSV source row.
# - Physical source row numbering is assigned before ticker filtering.
# - Raw provider values are preserved before Silver typing.
# - The provider nanosecond timestamp is not truncated in Bronze.
# - Provider exchange codes are preserved without translation.
# - Duplicate and conflicting source rows are not collapsed.
# - Atlas product and contract keys are not added in Bronze.
# - The configured source object is explicit; the notebook does not select the latest object.
# - Automatic futures-contract rollover is outside scope.
# - Credentials and proprietary source data must not be committed to GitHub.


# CELL ********************

# Runtime Dependency Setup
# The Massive Flat Files ingestion uses the AWS-compatible `boto3` client.
# This cell checks whether `boto3` is already available in the Fabric notebook runtime and installs it only when required.
# The Fabric Python session may restart after a new package installation. If that occurs, continue by rerunning the notebook from this section.

# Check whether boto3 is available in the current Fabric runtime

import importlib.util

boto3_available = importlib.util.find_spec("boto3") is not None

if boto3_available:
    print("boto3 is already installed in the current notebook runtime.")
else:
    print("boto3 is not installed. Installing boto3 now...")
    %pip install boto3

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Atlas Market Data Platform
# Notebook: nb_atlas_bronze_massive_futures_minute_aggregates
# Purpose: Configure the first controlled Massive Futures Bronze ingestion

from datetime import datetime, timezone
from io import BytesIO, TextIOWrapper
import csv
import gzip
import os

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from pyspark.sql import functions as F
from pyspark.sql.types import (
    LongType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

# -------------------------------------------------------------------
# Governed ingestion configuration
# -------------------------------------------------------------------

source_provider = "Massive"
source_dataset = "us_futures_cme/minute_aggs_v1"

source_object_key = (
    "us_futures_cme/minute_aggs_v1/"
    "2026/07/2026-07-14.csv.gz"
)

selected_provider_tickers = [
    "MESU6",
    "MNQU6",
]

expected_source_columns = [
    "ticker",
    "exchange",
    "session_end_date",
    "window_start",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "dollar_volume",
    "transactions",
]

bronze_table = "bronze_massive_futures_minute_aggregates"

massive_s3_endpoint = "https://files.massive.com"
massive_s3_bucket = "flatfiles"
massive_s3_region = "us-east-1"

# One consistent Atlas ingestion timestamp for every accepted row.
bronze_loaded_at_utc = datetime.now(timezone.utc).replace(tzinfo=None)

# -------------------------------------------------------------------
# Governed Bronze schema
# -------------------------------------------------------------------

bronze_schema = StructType(
    [
        StructField("source_provider", StringType(), False),
        StructField("source_dataset", StringType(), False),
        StructField("source_object_key", StringType(), False),
        StructField("source_row_number", LongType(), False),
        StructField("provider_ticker", StringType(), False),
        StructField("provider_exchange_code", StringType(), False),
        StructField("session_end_date_raw", StringType(), False),
        StructField("window_start_ns", LongType(), False),
        StructField("open_raw", StringType(), False),
        StructField("high_raw", StringType(), False),
        StructField("low_raw", StringType(), False),
        StructField("close_raw", StringType(), False),
        StructField("volume_raw", StringType(), False),
        StructField("dollar_volume_raw", StringType(), False),
        StructField("transactions_raw", StringType(), False),
        StructField("bronze_loaded_at_utc", TimestampType(), False),
    ]
)

print("Massive Futures Bronze configuration")
print("------------------------------------")
print(f"Source provider: {source_provider}")
print(f"Source dataset: {source_dataset}")
print(f"Source object: {source_object_key}")
print(f"Selected tickers: {selected_provider_tickers}")
print(f"Target table: {bronze_table}")
print(f"Expected source columns: {len(expected_source_columns)}")
print(f"Governed Bronze columns: {len(bronze_schema.fields)}")
print(f"Bronze load timestamp: {bronze_loaded_at_utc} UTC")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Retrieve Massive Flat Files credentials securely from Azure Key Vault

key_vault_url = "https://kv-atlas-dev-ukfi.vault.azure.net/"

massive_s3_access_key = notebookutils.credentials.getSecret(
    key_vault_url,
    "massive-s3-access-key",
)

massive_s3_secret_key = notebookutils.credentials.getSecret(
    key_vault_url,
    "massive-s3-secret-key",
)

if not massive_s3_access_key:
    raise ValueError(
        "The Massive S3 access key could not be retrieved from Azure Key Vault."
    )

if not massive_s3_secret_key:
    raise ValueError(
        "The Massive S3 secret key could not be retrieved from Azure Key Vault."
    )

print("Massive Flat Files credentials retrieved securely from Azure Key Vault.")
print("Credential values have not been displayed.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create the Massive S3-compatible client and verify source object access

massive_s3_client = boto3.client(
    "s3",
    endpoint_url=massive_s3_endpoint,
    aws_access_key_id=massive_s3_access_key,
    aws_secret_access_key=massive_s3_secret_key,
    region_name=massive_s3_region,
    config=Config(
        signature_version="s3v4",
        retries={
            "max_attempts": 3,
            "mode": "standard",
        },
    ),
)

try:
    source_object_metadata = massive_s3_client.head_object(
        Bucket=massive_s3_bucket,
        Key=source_object_key,
    )
except ClientError as exc:
    error_code = (
        exc.response
        .get("Error", {})
        .get("Code", "Unknown")
    )

    raise ValueError(
        "Massive source object could not be accessed. "
        f"Object key: {source_object_key}. "
        f"Provider error code: {error_code}."
    ) from exc
except BotoCoreError as exc:
    raise RuntimeError(
        "The Massive S3-compatible client failed while checking "
        "the configured source object."
    ) from exc

source_object_size_bytes = source_object_metadata.get("ContentLength")
source_object_etag = source_object_metadata.get("ETag", "").strip('"')
source_object_last_modified = source_object_metadata.get("LastModified")

print("Massive source object access confirmed.")
print(f"Object key: {source_object_key}")
print(f"Compressed size: {source_object_size_bytes:,} bytes")
print(f"Last modified: {source_object_last_modified}")
print(f"ETag available: {bool(source_object_etag)}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Retrieve the configured source object and validate the CSV header

try:
    source_object_response = massive_s3_client.get_object(
        Bucket=massive_s3_bucket,
        Key=source_object_key,
    )

    compressed_source_bytes = source_object_response["Body"].read()

except ClientError as exc:
    error_code = (
        exc.response
        .get("Error", {})
        .get("Code", "Unknown")
    )

    raise ValueError(
        "Massive source object could not be retrieved. "
        f"Object key: {source_object_key}. "
        f"Provider error code: {error_code}."
    ) from exc

except BotoCoreError as exc:
    raise RuntimeError(
        "The Massive S3-compatible client failed while retrieving "
        "the configured source object."
    ) from exc

if not compressed_source_bytes:
    raise ValueError(
        "The configured Massive source object was retrieved but contained no data."
    )

try:
    with gzip.GzipFile(
        fileobj=BytesIO(compressed_source_bytes),
        mode="rb",
    ) as gzip_stream:
        decompressed_source_bytes = gzip_stream.read()

except OSError as exc:
    raise ValueError(
        "The configured Massive source object could not be decompressed as gzip."
    ) from exc

if not decompressed_source_bytes:
    raise ValueError(
        "The configured Massive source object decompressed successfully "
        "but contained no CSV data."
    )

source_text_stream = TextIOWrapper(
    BytesIO(decompressed_source_bytes),
    encoding="utf-8",
    newline="",
)

csv_reader = csv.reader(source_text_stream)

try:
    actual_source_columns = next(csv_reader)
except StopIteration as exc:
    raise ValueError(
        "The decompressed Massive source object does not contain a CSV header."
    ) from exc

if actual_source_columns != expected_source_columns:
    raise ValueError(
        "Massive source header validation failed. "
        f"Expected: {expected_source_columns}. "
        f"Actual: {actual_source_columns}."
    )

print("Massive source header validation passed.")
print(f"Compressed bytes retrieved: {len(compressed_source_bytes):,}")
print(f"Decompressed bytes available: {len(decompressed_source_bytes):,}")
print(f"Validated source columns: {len(actual_source_columns)}")
print(f"Header: {actual_source_columns}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Parse physical source rows and create the selected Bronze DataFrame

source_text_stream = TextIOWrapper(
    BytesIO(decompressed_source_bytes),
    encoding="utf-8",
    newline="",
)

csv_reader = csv.reader(source_text_stream)

# Skip the already validated header.
parsed_header = next(csv_reader)

if parsed_header != expected_source_columns:
    raise ValueError(
        "The source header changed between validation and row parsing."
    )

selected_ticker_set = set(selected_provider_tickers)

bronze_rows = []
source_data_row_count = 0
malformed_row_count = 0

selected_ticker_counts = {
    ticker: 0
    for ticker in selected_provider_tickers
}

for source_row_number, source_row in enumerate(csv_reader, start=1):
    source_data_row_count += 1

    if len(source_row) != len(expected_source_columns):
        malformed_row_count += 1
        continue

    (
        ticker,
        exchange,
        session_end_date,
        window_start,
        open_value,
        high_value,
        low_value,
        close_value,
        volume,
        dollar_volume,
        transactions,
    ) = source_row

    # Physical source row numbering is assigned before ticker filtering.
    if ticker not in selected_ticker_set:
        continue

    try:
        window_start_ns = int(window_start)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "A selected Massive source row contains an invalid "
            f"window_start value. Source row: {source_row_number}."
        ) from exc

    bronze_rows.append(
        (
            source_provider,
            source_dataset,
            source_object_key,
            source_row_number,
            ticker,
            exchange,
            session_end_date,
            window_start_ns,
            open_value,
            high_value,
            low_value,
            close_value,
            volume,
            dollar_volume,
            transactions,
            bronze_loaded_at_utc,
        )
    )

    selected_ticker_counts[ticker] += 1

if source_data_row_count == 0:
    raise ValueError(
        "The configured Massive source object contains no CSV data rows."
    )

if malformed_row_count > 0:
    raise ValueError(
        "Malformed CSV rows were detected in the Massive source object. "
        f"Malformed row count: {malformed_row_count:,}."
    )

missing_selected_tickers = [
    ticker
    for ticker, row_count in selected_ticker_counts.items()
    if row_count == 0
]

if missing_selected_tickers:
    raise ValueError(
        "The configured source object does not contain all selected tickers: "
        + ", ".join(missing_selected_tickers)
    )

bronze_massive_df = spark.createDataFrame(
    bronze_rows,
    schema=bronze_schema,
)

prepared_bronze_row_count = bronze_massive_df.count()

print(f"Physical source data rows: {source_data_row_count:,}")
print(f"Malformed source rows: {malformed_row_count:,}")
print(f"Selected Bronze rows: {prepared_bronze_row_count:,}")

for ticker in selected_provider_tickers:
    print(
        f"{ticker} selected rows: "
        f"{selected_ticker_counts[ticker]:,}"
    )

bronze_massive_df.printSchema()

display(
    bronze_massive_df
        .orderBy("source_row_number")
        .limit(20)
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Validate the prepared Massive Futures Bronze DataFrame

prepared_validation_checks = {
    "Expected prepared row count": (
        bronze_massive_df.count() == 2760
    ),
    "Only approved tickers are present": (
        bronze_massive_df
            .filter(
                ~F.col("provider_ticker").isin(
                    selected_provider_tickers
                )
            )
            .count() == 0
    ),
    "MESU6 expected row count": (
        bronze_massive_df
            .filter(F.col("provider_ticker") == "MESU6")
            .count() == 1380
    ),
    "MNQU6 expected row count": (
        bronze_massive_df
            .filter(F.col("provider_ticker") == "MNQU6")
            .count() == 1380
    ),
    "Physical source identity is unique": (
        bronze_massive_df
            .groupBy(
                "source_provider",
                "source_dataset",
                "source_object_key",
                "source_row_number",
            )
            .count()
            .filter(F.col("count") > 1)
            .count() == 0
    ),
    "Source row numbers are positive": (
        bronze_massive_df
            .filter(F.col("source_row_number") <= 0)
            .count() == 0
    ),
    "Required lineage fields are non-null": (
        bronze_massive_df
            .filter(
                F.col("source_provider").isNull()
                | F.col("source_dataset").isNull()
                | F.col("source_object_key").isNull()
                | F.col("source_row_number").isNull()
            )
            .count() == 0
    ),
    "Required source fields are non-null": (
        bronze_massive_df
            .filter(
                F.col("provider_ticker").isNull()
                | F.col("provider_exchange_code").isNull()
                | F.col("session_end_date_raw").isNull()
                | F.col("window_start_ns").isNull()
                | F.col("open_raw").isNull()
                | F.col("high_raw").isNull()
                | F.col("low_raw").isNull()
                | F.col("close_raw").isNull()
                | F.col("volume_raw").isNull()
                | F.col("dollar_volume_raw").isNull()
                | F.col("transactions_raw").isNull()
            )
            .count() == 0
    ),
    "One source provider value": (
        bronze_massive_df
            .select("source_provider")
            .distinct()
            .count() == 1
    ),
    "One source dataset value": (
        bronze_massive_df
            .select("source_dataset")
            .distinct()
            .count() == 1
    ),
    "One source object value": (
        bronze_massive_df
            .select("source_object_key")
            .distinct()
            .count() == 1
    ),
    "One Bronze load timestamp": (
        bronze_massive_df
            .select("bronze_loaded_at_utc")
            .distinct()
            .count() == 1
    ),
}

prepared_validation_results_df = spark.createDataFrame(
    [
        (check_name, passed)
        for check_name, passed in prepared_validation_checks.items()
    ],
    ["ValidationCheck", "ValidationPassed"],
)

display(
    prepared_validation_results_df.orderBy("ValidationCheck")
)

failed_prepared_checks = [
    check_name
    for check_name, passed in prepared_validation_checks.items()
    if not passed
]

if failed_prepared_checks:
    raise ValueError(
        "Prepared Massive Futures Bronze validation failed: "
        + ", ".join(failed_prepared_checks)
    )

print(
    "Prepared Massive Futures Bronze validation passed: "
    f"{len(prepared_validation_checks)} checks completed successfully."
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Persist the Massive Futures Bronze Delta table

(
    bronze_massive_df
        .write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(bronze_table)
)

print(f"Massive Futures Bronze table written: {bronze_table}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Validate the persisted Massive Futures Bronze Delta table

bronze_massive_saved_df = spark.table(bronze_table)

persisted_bronze_row_count = bronze_massive_saved_df.count()

persisted_validation_checks = {
    "Persisted row count matches prepared row count": (
        persisted_bronze_row_count == prepared_bronze_row_count
    ),
    "Persisted MESU6 row count": (
        bronze_massive_saved_df
            .filter(F.col("provider_ticker") == "MESU6")
            .count() == 1380
    ),
    "Persisted MNQU6 row count": (
        bronze_massive_saved_df
            .filter(F.col("provider_ticker") == "MNQU6")
            .count() == 1380
    ),
    "Persisted scope contains only approved tickers": (
        bronze_massive_saved_df
            .filter(
                ~F.col("provider_ticker").isin(
                    selected_provider_tickers
                )
            )
            .count() == 0
    ),
    "Persisted physical source identity is unique": (
        bronze_massive_saved_df
            .groupBy(
                "source_provider",
                "source_dataset",
                "source_object_key",
                "source_row_number",
            )
            .count()
            .filter(F.col("count") > 1)
            .count() == 0
    ),
    "Persisted source row numbers are positive": (
        bronze_massive_saved_df
            .filter(F.col("source_row_number") <= 0)
            .count() == 0
    ),
    "Persisted source object is correct": (
        bronze_massive_saved_df
            .filter(
                F.col("source_object_key") != source_object_key
            )
            .count() == 0
    ),
    "Persisted source dataset is correct": (
        bronze_massive_saved_df
            .filter(
                F.col("source_dataset") != source_dataset
            )
            .count() == 0
    ),
    "Persisted source provider is correct": (
        bronze_massive_saved_df
            .filter(
                F.col("source_provider") != source_provider
            )
            .count() == 0
    ),
    "Persisted load timestamp is consistent": (
        bronze_massive_saved_df
            .select("bronze_loaded_at_utc")
            .distinct()
            .count() == 1
    ),
    "Persisted required fields are non-null": (
        bronze_massive_saved_df
            .filter(
                F.col("source_provider").isNull()
                | F.col("source_dataset").isNull()
                | F.col("source_object_key").isNull()
                | F.col("source_row_number").isNull()
                | F.col("provider_ticker").isNull()
                | F.col("provider_exchange_code").isNull()
                | F.col("session_end_date_raw").isNull()
                | F.col("window_start_ns").isNull()
                | F.col("open_raw").isNull()
                | F.col("high_raw").isNull()
                | F.col("low_raw").isNull()
                | F.col("close_raw").isNull()
                | F.col("volume_raw").isNull()
                | F.col("dollar_volume_raw").isNull()
                | F.col("transactions_raw").isNull()
                | F.col("bronze_loaded_at_utc").isNull()
            )
            .count() == 0
    ),
}

persisted_validation_results_df = spark.createDataFrame(
    [
        (check_name, passed)
        for check_name, passed in persisted_validation_checks.items()
    ],
    ["ValidationCheck", "ValidationPassed"],
)

display(
    persisted_validation_results_df.orderBy("ValidationCheck")
)

failed_persisted_checks = [
    check_name
    for check_name, passed in persisted_validation_checks.items()
    if not passed
]

if failed_persisted_checks:
    raise ValueError(
        "Persisted Massive Futures Bronze validation failed: "
        + ", ".join(failed_persisted_checks)
    )

print(f"Persisted row count: {persisted_bronze_row_count:,}")

bronze_massive_saved_df.printSchema()

display(
    bronze_massive_saved_df
        .orderBy("source_row_number")
        .limit(20)
)

print(
    "Persisted Massive Futures Bronze validation passed: "
    f"{len(persisted_validation_checks)} checks completed successfully."
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
