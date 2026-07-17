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
# ## Massive Futures Historical Silver Processing
# 
# **Notebook:** `nb_atlas_silver_massive_futures_minute_aggregates`
# 
# **Purpose:**  
# Transform source-aligned Massive Futures Bronze minute aggregates into a strongly typed, validated and contract-enriched Silver dataset.
# 
# **Input:**
# 
# ```text
# Tables/bronze_massive_futures_minute_aggregates
# ```
# 
# **Instrument mapping:**
# 
# ```text
# Tables/gold_dim_instrument
# ```
# 
# **Output:**
# 
# ```text
# Tables/silver_massive_futures_minute_aggregates
# ```
# 
# **Initial contracts:**
# 
# ```text
# MESU6
# MNQU6
# ```
# 
# **Initial data coverage:**
# 
# ```text
# One Massive Futures trading session
# Session end date: 2026-07-14
# 1,380 minute bars per contract
# 2,760 total Bronze rows
# ```
# 
# **Contract:**
# 
# ```text
# docs/01_Architecture/Massive_Futures_Silver_Contract.md
# ```
# 
# ---
# 
# ## Engineering Rules
# 
# - Silver remains at provider-generated minute-bar grain.
# - Massive nanosecond timestamps are converted to UTC minute timestamps.
# - Provider `session_end_date` becomes the governed session date.
# - Prices use `Decimal(18,5)` for the selected contracts.
# - Provider tickers map to stable Atlas contract and product keys.
# - Physical Bronze lineage is preserved.
# - Duplicate business keys are detected and classified.
# - Duplicate rows are not removed arbitrarily.
# - CQG-style event sequences are not fabricated.
# - Automatic futures-contract rollover is outside scope.


# CELL ********************

# Configure the Massive Futures Silver transformation

from datetime import datetime, timezone

from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import DecimalType

bronze_table = "bronze_massive_futures_minute_aggregates"
instrument_table = "gold_dim_instrument"
silver_table = "silver_massive_futures_minute_aggregates"

selected_provider_tickers = [
    "MESU6",
    "MNQU6",
]

expected_bronze_row_count = 2760
expected_rows_per_ticker = 1380

silver_loaded_at_utc = datetime.now(timezone.utc).replace(tzinfo=None)

print("Massive Futures Silver configuration")
print("------------------------------------")
print(f"Bronze input table: {bronze_table}")
print(f"Instrument mapping table: {instrument_table}")
print(f"Silver target table: {silver_table}")
print(f"Selected tickers: {selected_provider_tickers}")
print(f"Expected Bronze rows: {expected_bronze_row_count:,}")
print(f"Expected rows per ticker: {expected_rows_per_ticker:,}")
print(f"Silver load timestamp: {silver_loaded_at_utc} UTC")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Read and inspect the Bronze and instrument-dimension inputs

bronze_df = spark.table(bronze_table)
instrument_df = spark.table(instrument_table)

bronze_row_count = bronze_df.count()
instrument_row_count = instrument_df.count()

print(f"Bronze row count: {bronze_row_count:,}")
print(f"Instrument dimension row count: {instrument_row_count:,}")

if bronze_row_count != expected_bronze_row_count:
    raise ValueError(
        f"Expected {expected_bronze_row_count:,} Bronze rows, "
        f"found {bronze_row_count:,}."
    )

if instrument_row_count != 2:
    raise ValueError(
        f"Expected 2 instrument dimension rows, found {instrument_row_count:,}."
    )

bronze_ticker_counts_df = (
    bronze_df
        .groupBy("provider_ticker")
        .count()
        .orderBy("provider_ticker")
)

display(bronze_ticker_counts_df)

unexpected_bronze_tickers = (
    bronze_df
        .filter(
            ~F.col("provider_ticker").isin(
                selected_provider_tickers
            )
        )
        .count()
)

if unexpected_bronze_tickers > 0:
    raise ValueError(
        "Bronze contains provider tickers outside the approved Silver scope."
    )

for ticker in selected_provider_tickers:
    ticker_count = (
        bronze_df
            .filter(F.col("provider_ticker") == ticker)
            .count()
    )

    if ticker_count != expected_rows_per_ticker:
        raise ValueError(
            f"Expected {expected_rows_per_ticker:,} rows for {ticker}, "
            f"found {ticker_count:,}."
        )

required_instrument_columns = [
    "AtlasContractKey",
    "AtlasContractBusinessKey",
    "AtlasProductKey",
    "AtlasProductBusinessKey",
    "TradingVenue",
    "SourceProvider",
    "ProviderTicker",
]

missing_instrument_columns = [
    column_name
    for column_name in required_instrument_columns
    if column_name not in instrument_df.columns
]

if missing_instrument_columns:
    raise ValueError(
        "Instrument dimension is missing required columns: "
        + ", ".join(missing_instrument_columns)
    )

selected_instrument_df = (
    instrument_df
        .filter(F.col("SourceProvider") == "Massive")
        .filter(
            F.col("ProviderTicker").isin(
                selected_provider_tickers
            )
        )
        .select(
            "AtlasContractKey",
            "AtlasContractBusinessKey",
            "AtlasProductKey",
            "AtlasProductBusinessKey",
            "TradingVenue",
            "SourceProvider",
            "ProviderTicker",
        )
)

selected_instrument_count = selected_instrument_df.count()

if selected_instrument_count != 2:
    raise ValueError(
        "Expected exactly two governed Massive instrument mappings, "
        f"found {selected_instrument_count}."
    )

duplicate_instrument_mappings = (
    selected_instrument_df
        .groupBy("SourceProvider", "ProviderTicker")
        .count()
        .filter(F.col("count") > 1)
        .count()
)

if duplicate_instrument_mappings > 0:
    raise ValueError(
        "Instrument dimension contains duplicate provider mappings."
    )

print("Bronze and instrument-dimension input validation passed.")

bronze_df.printSchema()

display(
    bronze_df
        .orderBy("source_row_number")
        .limit(10)
)

display(
    selected_instrument_df
        .orderBy("AtlasContractKey")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Strongly type Bronze values and enrich them with governed instrument identity

# Ensure epoch conversion and displayed timestamps use UTC consistently.
spark.conf.set("spark.sql.session.timeZone", "UTC")

price_type = DecimalType(18, 5)
dollar_volume_type = DecimalType(28, 5)

instrument_mapping_df = (
    selected_instrument_df
        .select(
            F.col("SourceProvider").alias("mapping_source_provider"),
            F.col("ProviderTicker").alias("mapping_provider_ticker"),
            "AtlasContractKey",
            "AtlasContractBusinessKey",
            "AtlasProductKey",
            "AtlasProductBusinessKey",
            F.col("TradingVenue").alias("trading_venue"),
        )
)

silver_typed_df = (
    bronze_df.alias("bronze")
        .join(
            instrument_mapping_df.alias("mapping"),
            (
                F.col("bronze.source_provider")
                == F.col("mapping.mapping_source_provider")
            )
            & (
                F.col("bronze.provider_ticker")
                == F.col("mapping.mapping_provider_ticker")
            ),
            "left",
        )
        .withColumn(
            "session_end_date",
            F.to_date(
                F.col("bronze.session_end_date_raw"),
                "yyyy-MM-dd",
            ),
        )
        .withColumn(
            "minute_timestamp",
            F.timestamp_seconds(
                F.col("bronze.window_start_ns")
                / F.lit(1_000_000_000)
            ),
        )
        .withColumn(
            "open_price",
            F.col("bronze.open_raw").cast(price_type),
        )
        .withColumn(
            "high_price",
            F.col("bronze.high_raw").cast(price_type),
        )
        .withColumn(
            "low_price",
            F.col("bronze.low_raw").cast(price_type),
        )
        .withColumn(
            "close_price",
            F.col("bronze.close_raw").cast(price_type),
        )
        .withColumn(
            "volume",
            F.col("bronze.volume_raw").cast("long"),
        )
        .withColumn(
            "dollar_volume",
            F.col("bronze.dollar_volume_raw").cast(
                dollar_volume_type
            ),
        )
        .withColumn(
            "transactions",
            F.col("bronze.transactions_raw").cast("long"),
        )
        .withColumn(
            "is_valid_ticker",
            F.col("AtlasContractKey").isNotNull()
            & F.col("AtlasContractBusinessKey").isNotNull()
            & F.col("AtlasProductKey").isNotNull()
            & F.col("AtlasProductBusinessKey").isNotNull(),
        )
        .withColumn(
            "is_valid_session_date",
            F.col("session_end_date").isNotNull(),
        )
        .withColumn(
            "is_valid_timestamp",
            F.col("minute_timestamp").isNotNull(),
        )
        .withColumn(
            "is_valid_minute_boundary",
            F.col("bronze.window_start_ns").isNotNull()
            & (
                F.col("bronze.window_start_ns")
                % F.lit(60_000_000_000)
                == 0
            ),
        )
        .withColumn(
            "is_valid_price",
            F.col("open_price").isNotNull()
            & F.col("high_price").isNotNull()
            & F.col("low_price").isNotNull()
            & F.col("close_price").isNotNull()
            & (F.col("open_price") > 0)
            & (F.col("high_price") > 0)
            & (F.col("low_price") > 0)
            & (F.col("close_price") > 0),
        )
        .withColumn(
            "is_valid_ohlc",
            F.col("is_valid_price")
            & (F.col("high_price") >= F.col("open_price"))
            & (F.col("high_price") >= F.col("close_price"))
            & (F.col("high_price") >= F.col("low_price"))
            & (F.col("low_price") <= F.col("open_price"))
            & (F.col("low_price") <= F.col("close_price")),
        )
        .withColumn(
            "is_valid_activity",
            F.col("volume").isNotNull()
            & F.col("dollar_volume").isNotNull()
            & F.col("transactions").isNotNull()
            & (F.col("volume") >= 0)
            & (F.col("dollar_volume") >= 0)
            & (F.col("transactions") >= 0),
        )
        .withColumn(
            "silver_loaded_at_utc",
            F.lit(silver_loaded_at_utc).cast("timestamp"),
        )
        .select(
            F.col("bronze.source_provider").alias(
                "source_provider"
            ),
            F.col("bronze.provider_ticker").alias(
                "provider_ticker"
            ),
            "AtlasContractKey",
            "AtlasContractBusinessKey",
            "AtlasProductKey",
            "AtlasProductBusinessKey",
            F.col("bronze.provider_exchange_code").alias(
                "provider_exchange_code"
            ),
            "trading_venue",
            "session_end_date",
            "minute_timestamp",
            "open_price",
            "high_price",
            "low_price",
            "close_price",
            "volume",
            "dollar_volume",
            "transactions",
            F.col("bronze.source_dataset").alias(
                "source_dataset"
            ),
            F.col("bronze.source_object_key").alias(
                "source_object_key"
            ),
            F.col("bronze.source_row_number").alias(
                "source_row_number"
            ),
            "is_valid_ticker",
            "is_valid_session_date",
            "is_valid_timestamp",
            "is_valid_minute_boundary",
            "is_valid_price",
            "is_valid_ohlc",
            "is_valid_activity",
            F.col("bronze.bronze_loaded_at_utc").alias(
                "bronze_loaded_at_utc"
            ),
            "silver_loaded_at_utc",
        )
)

silver_typed_row_count = silver_typed_df.count()

print(f"Strongly typed Silver candidate rows: {silver_typed_row_count:,}")

silver_typed_df.printSchema()

display(
    silver_typed_df
        .select(
            "provider_ticker",
            "AtlasContractKey",
            "AtlasContractBusinessKey",
            "session_end_date",
            "minute_timestamp",
            "open_price",
            "high_price",
            "low_price",
            "close_price",
            "volume",
            "transactions",
            "is_valid_ticker",
            "is_valid_session_date",
            "is_valid_timestamp",
            "is_valid_minute_boundary",
            "is_valid_price",
            "is_valid_ohlc",
            "is_valid_activity",
            "source_row_number",
        )
        .orderBy(
            "provider_ticker",
            "minute_timestamp",
        )
        .limit(20)
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Detect duplicate business keys and assign Silver quality status

business_key_window = Window.partitionBy(
    "source_provider",
    "provider_ticker",
    "minute_timestamp",
)

business_value_columns = [
    "session_end_date",
    "provider_exchange_code",
    "open_price",
    "high_price",
    "low_price",
    "close_price",
    "volume",
    "dollar_volume",
    "transactions",
]

business_value_signature = F.sha2(
    F.concat_ws(
        "||",
        *[
            F.coalesce(
                F.col(column_name).cast("string"),
                F.lit("<NULL>"),
            )
            for column_name in business_value_columns
        ],
    ),
    256,
)

silver_duplicate_classified_df = (
    silver_typed_df
        .withColumn(
            "business_key_row_count",
            F.count("*").over(business_key_window),
        )
        .withColumn(
            "business_value_signature",
            business_value_signature,
        )
)

duplicate_signature_counts_df = (
    silver_duplicate_classified_df
        .groupBy(
            "source_provider",
            "provider_ticker",
            "minute_timestamp",
        )
        .agg(
            F.count("*").alias("business_key_row_count_check"),
            F.countDistinct("business_value_signature").alias(
                "distinct_business_value_count"
            ),
        )
)

silver_duplicate_classified_df = (
    silver_duplicate_classified_df.alias("silver")
        .join(
            duplicate_signature_counts_df.alias("duplicates"),
            on=[
                "source_provider",
                "provider_ticker",
                "minute_timestamp",
            ],
            how="left",
        )
        .withColumn(
            "is_duplicate_business_key",
            F.col("business_key_row_count_check") > 1,
        )
        .withColumn(
            "is_exact_duplicate",
            (F.col("business_key_row_count_check") > 1)
            & (F.col("distinct_business_value_count") == 1),
        )
        .withColumn(
            "has_conflicting_duplicate",
            (F.col("business_key_row_count_check") > 1)
            & (F.col("distinct_business_value_count") > 1),
        )
        .withColumn(
            "silver_quality_status",
            F.when(
                ~F.col("is_valid_ticker"),
                F.lit("InvalidTicker"),
            )
            .when(
                ~F.col("is_valid_session_date"),
                F.lit("InvalidSessionDate"),
            )
            .when(
                ~F.col("is_valid_timestamp"),
                F.lit("InvalidTimestamp"),
            )
            .when(
                ~F.col("is_valid_minute_boundary"),
                F.lit("InvalidMinuteBoundary"),
            )
            .when(
                ~F.col("is_valid_price"),
                F.lit("InvalidPrice"),
            )
            .when(
                ~F.col("is_valid_ohlc"),
                F.lit("InvalidOHLC"),
            )
            .when(
                ~F.col("is_valid_activity"),
                F.lit("InvalidActivity"),
            )
            .when(
                F.col("has_conflicting_duplicate"),
                F.lit("ConflictingDuplicate"),
            )
            .when(
                F.col("is_exact_duplicate"),
                F.lit("ExactDuplicate"),
            )
            .otherwise(F.lit("Valid")),
        )
)

silver_df = (
    silver_duplicate_classified_df
        .select(
            "source_provider",
            "provider_ticker",
            "AtlasContractKey",
            "AtlasContractBusinessKey",
            "AtlasProductKey",
            "AtlasProductBusinessKey",
            "provider_exchange_code",
            "trading_venue",
            "session_end_date",
            "minute_timestamp",
            "open_price",
            "high_price",
            "low_price",
            "close_price",
            "volume",
            "dollar_volume",
            "transactions",
            "source_dataset",
            "source_object_key",
            "source_row_number",
            "is_valid_ticker",
            "is_valid_session_date",
            "is_valid_timestamp",
            "is_valid_minute_boundary",
            "is_valid_price",
            "is_valid_ohlc",
            "is_valid_activity",
            "is_duplicate_business_key",
            "is_exact_duplicate",
            "has_conflicting_duplicate",
            "silver_quality_status",
            "bronze_loaded_at_utc",
            "silver_loaded_at_utc",
        )
)

duplicate_summary_df = (
    silver_df
        .agg(
            F.sum(
                F.col("is_duplicate_business_key").cast("int")
            ).alias("duplicate_business_key_rows"),
            F.sum(
                F.col("is_exact_duplicate").cast("int")
            ).alias("exact_duplicate_rows"),
            F.sum(
                F.col("has_conflicting_duplicate").cast("int")
            ).alias("conflicting_duplicate_rows"),
        )
)

display(duplicate_summary_df)

display(
    silver_df
        .groupBy("silver_quality_status")
        .count()
        .orderBy("silver_quality_status")
)

display(
    silver_df
        .select(
            "provider_ticker",
            "minute_timestamp",
            "source_row_number",
            "is_duplicate_business_key",
            "is_exact_duplicate",
            "has_conflicting_duplicate",
            "silver_quality_status",
        )
        .orderBy(
            "provider_ticker",
            "minute_timestamp",
        )
        .limit(20)
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Run full pre-persistence validation for the Massive Futures Silver dataset

silver_row_count = silver_df.count()

pre_persistence_checks = {
    "Expected Silver row count": (
        silver_row_count == expected_bronze_row_count
    ),
    "All Silver rows are Valid": (
        silver_df
            .filter(F.col("silver_quality_status") != "Valid")
            .count() == 0
    ),
    "MESU6 expected Silver row count": (
        silver_df
            .filter(F.col("provider_ticker") == "MESU6")
            .count() == expected_rows_per_ticker
    ),
    "MNQU6 expected Silver row count": (
        silver_df
            .filter(F.col("provider_ticker") == "MNQU6")
            .count() == expected_rows_per_ticker
    ),
    "Only approved tickers are present": (
        silver_df
            .filter(
                ~F.col("provider_ticker").isin(
                    selected_provider_tickers
                )
            )
            .count() == 0
    ),
    "All instrument mappings are populated": (
        silver_df
            .filter(
                F.col("AtlasContractKey").isNull()
                | F.col("AtlasContractBusinessKey").isNull()
                | F.col("AtlasProductKey").isNull()
                | F.col("AtlasProductBusinessKey").isNull()
                | F.col("trading_venue").isNull()
            )
            .count() == 0
    ),
    "All session dates are valid": (
        silver_df
            .filter(~F.col("is_valid_session_date"))
            .count() == 0
    ),
    "All timestamps are valid": (
        silver_df
            .filter(~F.col("is_valid_timestamp"))
            .count() == 0
    ),
    "All timestamps are minute-aligned": (
        silver_df
            .filter(~F.col("is_valid_minute_boundary"))
            .count() == 0
    ),
    "All prices are valid": (
        silver_df
            .filter(~F.col("is_valid_price"))
            .count() == 0
    ),
    "All OHLC relationships are valid": (
        silver_df
            .filter(~F.col("is_valid_ohlc"))
            .count() == 0
    ),
    "All activity values are valid": (
        silver_df
            .filter(~F.col("is_valid_activity"))
            .count() == 0
    ),
    "No duplicate business-key rows": (
        silver_df
            .filter(F.col("is_duplicate_business_key"))
            .count() == 0
    ),
    "No exact duplicates": (
        silver_df
            .filter(F.col("is_exact_duplicate"))
            .count() == 0
    ),
    "No conflicting duplicates": (
        silver_df
            .filter(F.col("has_conflicting_duplicate"))
            .count() == 0
    ),
    "Physical source identity is unique": (
        silver_df
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
    "Trusted Silver business grain is unique": (
        silver_df
            .filter(F.col("silver_quality_status") == "Valid")
            .groupBy(
                "source_provider",
                "provider_ticker",
                "minute_timestamp",
            )
            .count()
            .filter(F.col("count") > 1)
            .count() == 0
    ),
    "Required lineage fields are non-null": (
        silver_df
            .filter(
                F.col("source_provider").isNull()
                | F.col("source_dataset").isNull()
                | F.col("source_object_key").isNull()
                | F.col("source_row_number").isNull()
                | F.col("bronze_loaded_at_utc").isNull()
                | F.col("silver_loaded_at_utc").isNull()
            )
            .count() == 0
    ),
    "One Silver load timestamp": (
        silver_df
            .select("silver_loaded_at_utc")
            .distinct()
            .count() == 1
    ),
    "Session date remains 2026-07-14": (
        silver_df
            .filter(
                F.col("session_end_date")
                != F.to_date(F.lit("2026-07-14"))
            )
            .count() == 0
    ),
    "MESU6 mapping is correct": (
        silver_df
            .filter(
                (F.col("provider_ticker") == "MESU6")
                & (F.col("AtlasContractKey") == 2001)
                & (
                    F.col("AtlasContractBusinessKey")
                    == "FUT-XCME-MES-2026-09"
                )
                & (F.col("AtlasProductKey") == 1001)
                & (
                    F.col("AtlasProductBusinessKey")
                    == "FUT-XCME-MES"
                )
            )
            .count() == expected_rows_per_ticker
    ),
    "MNQU6 mapping is correct": (
        silver_df
            .filter(
                (F.col("provider_ticker") == "MNQU6")
                & (F.col("AtlasContractKey") == 2002)
                & (
                    F.col("AtlasContractBusinessKey")
                    == "FUT-XCME-MNQ-2026-09"
                )
                & (F.col("AtlasProductKey") == 1002)
                & (
                    F.col("AtlasProductBusinessKey")
                    == "FUT-XCME-MNQ"
                )
            )
            .count() == expected_rows_per_ticker
    ),
}

pre_persistence_results_df = spark.createDataFrame(
    [
        (check_name, passed)
        for check_name, passed in pre_persistence_checks.items()
    ],
    ["ValidationCheck", "ValidationPassed"],
)

display(
    pre_persistence_results_df.orderBy("ValidationCheck")
)

failed_pre_persistence_checks = [
    check_name
    for check_name, passed in pre_persistence_checks.items()
    if not passed
]

if failed_pre_persistence_checks:
    raise ValueError(
        "Massive Futures Silver pre-persistence validation failed: "
        + ", ".join(failed_pre_persistence_checks)
    )

print(
    "Massive Futures Silver pre-persistence validation passed: "
    f"{len(pre_persistence_checks)} checks completed successfully."
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Persist the Massive Futures Silver Delta table

(
    silver_df
        .write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(silver_table)
)

print(f"Massive Futures Silver table written: {silver_table}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Validate the persisted Massive Futures Silver Delta table

silver_saved_df = spark.table(silver_table)

persisted_silver_row_count = silver_saved_df.count()

persisted_checks = {
    "Persisted row count matches prepared row count": (
        persisted_silver_row_count == silver_row_count
    ),
    "Persisted MESU6 row count": (
        silver_saved_df
            .filter(F.col("provider_ticker") == "MESU6")
            .count() == expected_rows_per_ticker
    ),
    "Persisted MNQU6 row count": (
        silver_saved_df
            .filter(F.col("provider_ticker") == "MNQU6")
            .count() == expected_rows_per_ticker
    ),
    "Persisted rows are all Valid": (
        silver_saved_df
            .filter(F.col("silver_quality_status") != "Valid")
            .count() == 0
    ),
    "Persisted business grain is unique": (
        silver_saved_df
            .groupBy(
                "source_provider",
                "provider_ticker",
                "minute_timestamp",
            )
            .count()
            .filter(F.col("count") > 1)
            .count() == 0
    ),
    "Persisted physical source identity is unique": (
        silver_saved_df
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
    "Persisted contract mappings are populated": (
        silver_saved_df
            .filter(
                F.col("AtlasContractKey").isNull()
                | F.col("AtlasContractBusinessKey").isNull()
                | F.col("AtlasProductKey").isNull()
                | F.col("AtlasProductBusinessKey").isNull()
                | F.col("trading_venue").isNull()
            )
            .count() == 0
    ),
    "Persisted validation flags remain true": (
        silver_saved_df
            .filter(
                ~F.col("is_valid_ticker")
                | ~F.col("is_valid_session_date")
                | ~F.col("is_valid_timestamp")
                | ~F.col("is_valid_minute_boundary")
                | ~F.col("is_valid_price")
                | ~F.col("is_valid_ohlc")
                | ~F.col("is_valid_activity")
            )
            .count() == 0
    ),
    "Persisted duplicate flags remain false": (
        silver_saved_df
            .filter(
                F.col("is_duplicate_business_key")
                | F.col("is_exact_duplicate")
                | F.col("has_conflicting_duplicate")
            )
            .count() == 0
    ),
    "Persisted session date is correct": (
        silver_saved_df
            .filter(
                F.col("session_end_date")
                != F.to_date(F.lit("2026-07-14"))
            )
            .count() == 0
    ),
    "Persisted minute timestamps are aligned": (
        silver_saved_df
            .filter(
                (F.second("minute_timestamp") != 0)
                | (
                    F.date_format(
                        F.col("minute_timestamp"),
                        "SSSSSS",
                    ) != "000000"
                )
            )
            .count() == 0
    ),
    "Persisted Silver load timestamp is consistent": (
        silver_saved_df
            .select("silver_loaded_at_utc")
            .distinct()
            .count() == 1
    ),
}

persisted_results_df = spark.createDataFrame(
    [
        (check_name, passed)
        for check_name, passed in persisted_checks.items()
    ],
    ["ValidationCheck", "ValidationPassed"],
)

display(
    persisted_results_df.orderBy("ValidationCheck")
)

failed_persisted_checks = [
    check_name
    for check_name, passed in persisted_checks.items()
    if not passed
]

if failed_persisted_checks:
    raise ValueError(
        "Persisted Massive Futures Silver validation failed: "
        + ", ".join(failed_persisted_checks)
    )

print(f"Persisted Silver row count: {persisted_silver_row_count:,}")

silver_saved_df.printSchema()

display(
    silver_saved_df
        .select(
            "provider_ticker",
            "AtlasContractKey",
            "AtlasContractBusinessKey",
            "session_end_date",
            "minute_timestamp",
            "open_price",
            "high_price",
            "low_price",
            "close_price",
            "volume",
            "transactions",
            "silver_quality_status",
            "source_row_number",
        )
        .orderBy(
            "provider_ticker",
            "minute_timestamp",
        )
        .limit(20)
)

print(
    "Persisted Massive Futures Silver validation passed: "
    f"{len(persisted_checks)} checks completed successfully."
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
