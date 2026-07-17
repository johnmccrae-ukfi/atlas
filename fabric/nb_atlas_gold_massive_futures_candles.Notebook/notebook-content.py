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
# ## Massive Futures Historical Gold Processing
# 
# **Notebook:** `nb_atlas_gold_massive_futures_candles`
# 
# **Purpose:**  
# Create governed Massive Futures historical minute and daily Gold candle tables from trusted Silver minute aggregates.
# 
# **Input:**
# 
# ```text
# Tables/silver_massive_futures_minute_aggregates
# ```
# 
# **Outputs:**
# 
# ```text
# Tables/gold_massive_futures_minute_candles
# Tables/gold_massive_futures_daily_candles
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
# TradingDate: 2026-07-14
# 1,380 minute bars per contract
# 2,760 total trusted Silver rows
# ```
# 
# **Contract:**
# 
# ```text
# docs/01_Architecture/Massive_Futures_Gold_Contract.md
# ```
# 
# ---
# 
# ## Engineering Rules
# 
# - Gold consumes only trusted Silver rows.
# - Massive minute bars are provider-generated and are projected rather than reconstructed.
# - `TradingDate` comes from the provider session date.
# - `MinuteTimestamp` remains UTC.
# - OHLC values retain `Decimal(18,5)` precision.
# - Daily Open and Close are derived chronologically.
# - Daily High and Low are derived from minute extrema.
# - Activity values retain Massive-specific semantics.
# - CQG-style event sequencing is not fabricated.
# - Automatic futures-contract rollover is outside scope.


# CELL ********************

# Configure the Massive Futures Gold transformation

from datetime import datetime, timezone

from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import DecimalType

silver_table = "silver_massive_futures_minute_aggregates"

gold_minute_table = "gold_massive_futures_minute_candles"
gold_daily_table = "gold_massive_futures_daily_candles"

selected_provider_tickers = [
    "MESU6",
    "MNQU6",
]

expected_silver_row_count = 2760
expected_rows_per_ticker = 1380
expected_daily_row_count = 2

gold_loaded_at_utc = datetime.now(timezone.utc).replace(tzinfo=None)

# Ensure timestamps are interpreted and displayed consistently in UTC.
spark.conf.set("spark.sql.session.timeZone", "UTC")

price_type = DecimalType(18, 5)
minute_dollar_volume_type = DecimalType(28, 5)
daily_dollar_volume_type = DecimalType(38, 5)

print("Massive Futures Gold configuration")
print("----------------------------------")
print(f"Silver input table: {silver_table}")
print(f"Gold minute target table: {gold_minute_table}")
print(f"Gold daily target table: {gold_daily_table}")
print(f"Selected tickers: {selected_provider_tickers}")
print(f"Expected Silver rows: {expected_silver_row_count:,}")
print(f"Expected rows per ticker: {expected_rows_per_ticker:,}")
print(f"Expected daily rows: {expected_daily_row_count:,}")
print(f"Gold load timestamp: {gold_loaded_at_utc} UTC")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Read and validate the trusted Massive Futures Silver input

silver_df = spark.table(silver_table)

silver_row_count = silver_df.count()

print(f"Silver row count: {silver_row_count:,}")

if silver_row_count != expected_silver_row_count:
    raise ValueError(
        f"Expected {expected_silver_row_count:,} Silver rows, "
        f"found {silver_row_count:,}."
    )

required_silver_columns = [
    "source_provider",
    "provider_ticker",
    "AtlasContractKey",
    "AtlasContractBusinessKey",
    "AtlasProductKey",
    "AtlasProductBusinessKey",
    "session_end_date",
    "minute_timestamp",
    "open_price",
    "high_price",
    "low_price",
    "close_price",
    "volume",
    "dollar_volume",
    "transactions",
    "silver_quality_status",
]

missing_silver_columns = [
    column_name
    for column_name in required_silver_columns
    if column_name not in silver_df.columns
]

if missing_silver_columns:
    raise ValueError(
        "Silver input is missing required columns: "
        + ", ".join(missing_silver_columns)
    )

unexpected_ticker_count = (
    silver_df
        .filter(
            ~F.col("provider_ticker").isin(
                selected_provider_tickers
            )
        )
        .count()
)

if unexpected_ticker_count > 0:
    raise ValueError(
        "Silver contains provider tickers outside the approved Gold scope."
    )

invalid_silver_row_count = (
    silver_df
        .filter(F.col("silver_quality_status") != "Valid")
        .count()
)

if invalid_silver_row_count > 0:
    raise ValueError(
        "Gold processing requires all selected Silver rows to be Valid. "
        f"Invalid Silver rows found: {invalid_silver_row_count:,}."
    )

for ticker in selected_provider_tickers:
    ticker_count = (
        silver_df
            .filter(F.col("provider_ticker") == ticker)
            .count()
    )

    if ticker_count != expected_rows_per_ticker:
        raise ValueError(
            f"Expected {expected_rows_per_ticker:,} Silver rows for {ticker}, "
            f"found {ticker_count:,}."
        )

duplicate_silver_business_keys = (
    silver_df
        .groupBy(
            "source_provider",
            "provider_ticker",
            "minute_timestamp",
        )
        .count()
        .filter(F.col("count") > 1)
        .count()
)

if duplicate_silver_business_keys > 0:
    raise ValueError(
        "Trusted Silver contains duplicate minute business keys."
    )

null_identity_count = (
    silver_df
        .filter(
            F.col("AtlasContractKey").isNull()
            | F.col("AtlasContractBusinessKey").isNull()
            | F.col("AtlasProductKey").isNull()
            | F.col("AtlasProductBusinessKey").isNull()
        )
        .count()
)

if null_identity_count > 0:
    raise ValueError(
        "Trusted Silver contains null governed instrument identity values."
    )

display(
    silver_df
        .groupBy(
            "provider_ticker",
            "silver_quality_status",
        )
        .count()
        .orderBy("provider_ticker")
)

silver_df.printSchema()

display(
    silver_df
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
            "dollar_volume",
            "silver_quality_status",
        )
        .orderBy(
            "provider_ticker",
            "minute_timestamp",
        )
        .limit(20)
)

print("Trusted Massive Futures Silver input validation passed.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create the governed Massive Futures Gold minute candles

gold_minute_df = (
    silver_df
        .filter(F.col("silver_quality_status") == "Valid")
        .select(
            "AtlasContractKey",
            "AtlasContractBusinessKey",
            "AtlasProductKey",
            "AtlasProductBusinessKey",
            F.col("provider_ticker").alias("Instrument"),
            F.col("session_end_date").alias("TradingDate"),
            F.col("minute_timestamp").alias("MinuteTimestamp"),
            F.date_format(
                F.col("minute_timestamp"),
                "HH:mm",
            ).alias("TradingTime"),
            F.hour(
                F.col("minute_timestamp")
            ).alias("TradingHour"),
            (
                F.hour(F.col("minute_timestamp")) * 60
                + F.minute(F.col("minute_timestamp"))
            ).alias("MinuteOfDay"),
            F.col("open_price").cast(price_type).alias("Open"),
            F.col("high_price").cast(price_type).alias("High"),
            F.col("low_price").cast(price_type).alias("Low"),
            F.col("close_price").cast(price_type).alias("Close"),
            F.col("volume").cast("long").alias("Volume"),
            F.col("transactions").cast("long").alias(
                "TransactionCount"
            ),
            F.col("dollar_volume")
                .cast(minute_dollar_volume_type)
                .alias("DollarVolume"),
            F.lit(gold_loaded_at_utc)
                .cast("timestamp")
                .alias("GoldLoadedUTC"),
        )
        .orderBy(
            "AtlasContractKey",
            "MinuteTimestamp",
        )
)

gold_minute_row_count = gold_minute_df.count()

print(f"Gold minute candle rows: {gold_minute_row_count:,}")

gold_minute_df.printSchema()

display(
    gold_minute_df
        .select(
            "AtlasContractKey",
            "AtlasContractBusinessKey",
            "Instrument",
            "TradingDate",
            "MinuteTimestamp",
            "TradingTime",
            "TradingHour",
            "MinuteOfDay",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "TransactionCount",
            "DollarVolume",
            "GoldLoadedUTC",
        )
        .orderBy(
            "AtlasContractKey",
            "MinuteTimestamp",
        )
        .limit(20)
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Validate the prepared Massive Futures Gold minute candles

gold_minute_validation_checks = {
    "Expected Gold minute row count": (
        gold_minute_df.count() == expected_silver_row_count
    ),
    "MESU6 expected Gold minute row count": (
        gold_minute_df
            .filter(F.col("Instrument") == "MESU6")
            .count() == expected_rows_per_ticker
    ),
    "MNQU6 expected Gold minute row count": (
        gold_minute_df
            .filter(F.col("Instrument") == "MNQU6")
            .count() == expected_rows_per_ticker
    ),
    "Only approved instruments are present": (
        gold_minute_df
            .filter(
                ~F.col("Instrument").isin(
                    selected_provider_tickers
                )
            )
            .count() == 0
    ),
    "Governed identity fields are populated": (
        gold_minute_df
            .filter(
                F.col("AtlasContractKey").isNull()
                | F.col("AtlasContractBusinessKey").isNull()
                | F.col("AtlasProductKey").isNull()
                | F.col("AtlasProductBusinessKey").isNull()
            )
            .count() == 0
    ),
    "TradingDate is populated": (
        gold_minute_df
            .filter(F.col("TradingDate").isNull())
            .count() == 0
    ),
    "MinuteTimestamp is populated": (
        gold_minute_df
            .filter(F.col("MinuteTimestamp").isNull())
            .count() == 0
    ),
    "Minute grain is unique": (
        gold_minute_df
            .groupBy(
                "AtlasContractKey",
                "MinuteTimestamp",
            )
            .count()
            .filter(F.col("count") > 1)
            .count() == 0
    ),
    "All OHLC values are positive": (
        gold_minute_df
            .filter(
                (F.col("Open") <= 0)
                | (F.col("High") <= 0)
                | (F.col("Low") <= 0)
                | (F.col("Close") <= 0)
            )
            .count() == 0
    ),
    "All OHLC relationships are valid": (
        gold_minute_df
            .filter(
                (F.col("High") < F.col("Open"))
                | (F.col("High") < F.col("Close"))
                | (F.col("High") < F.col("Low"))
                | (F.col("Low") > F.col("Open"))
                | (F.col("Low") > F.col("Close"))
            )
            .count() == 0
    ),
    "All activity values are non-negative": (
        gold_minute_df
            .filter(
                (F.col("Volume") < 0)
                | (F.col("TransactionCount") < 0)
                | (F.col("DollarVolume") < 0)
            )
            .count() == 0
    ),
    "TradingDate remains 2026-07-14": (
        gold_minute_df
            .filter(
                F.col("TradingDate")
                != F.to_date(F.lit("2026-07-14"))
            )
            .count() == 0
    ),
    "Minute timestamps remain minute-aligned": (
        gold_minute_df
            .filter(
                (F.second("MinuteTimestamp") != 0)
                | (
                    F.date_format(
                        F.col("MinuteTimestamp"),
                        "SSSSSS",
                    ) != "000000"
                )
            )
            .count() == 0
    ),
    "TradingTime matches MinuteTimestamp": (
        gold_minute_df
            .filter(
                F.col("TradingTime")
                != F.date_format(
                    F.col("MinuteTimestamp"),
                    "HH:mm",
                )
            )
            .count() == 0
    ),
    "TradingHour is valid": (
        gold_minute_df
            .filter(
                (F.col("TradingHour") < 0)
                | (F.col("TradingHour") > 23)
            )
            .count() == 0
    ),
    "MinuteOfDay is valid": (
        gold_minute_df
            .filter(
                (F.col("MinuteOfDay") < 0)
                | (F.col("MinuteOfDay") > 1439)
            )
            .count() == 0
    ),
    "Minute values reconcile with Silver": (
        gold_minute_df.alias("gold")
            .join(
                silver_df.alias("silver"),
                (
                    F.col("gold.AtlasContractKey")
                    == F.col("silver.AtlasContractKey")
                )
                & (
                    F.col("gold.MinuteTimestamp")
                    == F.col("silver.minute_timestamp")
                ),
                "inner",
            )
            .filter(
                (F.col("gold.TradingDate")
                 != F.col("silver.session_end_date"))
                | (F.col("gold.Open")
                   != F.col("silver.open_price"))
                | (F.col("gold.High")
                   != F.col("silver.high_price"))
                | (F.col("gold.Low")
                   != F.col("silver.low_price"))
                | (F.col("gold.Close")
                   != F.col("silver.close_price"))
                | (F.col("gold.Volume")
                   != F.col("silver.volume"))
                | (
                    F.col("gold.TransactionCount")
                    != F.col("silver.transactions")
                )
                | (
                    F.col("gold.DollarVolume")
                    != F.col("silver.dollar_volume")
                )
            )
            .count() == 0
    ),
    "One Gold load timestamp": (
        gold_minute_df
            .select("GoldLoadedUTC")
            .distinct()
            .count() == 1
    ),
}

gold_minute_validation_results_df = spark.createDataFrame(
    [
        (check_name, passed)
        for check_name, passed in gold_minute_validation_checks.items()
    ],
    ["ValidationCheck", "ValidationPassed"],
)

display(
    gold_minute_validation_results_df.orderBy("ValidationCheck")
)

failed_gold_minute_checks = [
    check_name
    for check_name, passed in gold_minute_validation_checks.items()
    if not passed
]

if failed_gold_minute_checks:
    raise ValueError(
        "Massive Futures Gold minute validation failed: "
        + ", ".join(failed_gold_minute_checks)
    )

print(
    "Massive Futures Gold minute validation passed: "
    f"{len(gold_minute_validation_checks)} checks completed successfully."
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Persist the Massive Futures Gold minute Delta table

(
    gold_minute_df
        .write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(gold_minute_table)
)

print(f"Massive Futures Gold minute table written: {gold_minute_table}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Validate the persisted Massive Futures Gold minute Delta table

gold_minute_saved_df = spark.table(gold_minute_table)

persisted_gold_minute_row_count = gold_minute_saved_df.count()

persisted_gold_minute_checks = {
    "Persisted row count matches prepared row count": (
        persisted_gold_minute_row_count == gold_minute_row_count
    ),
    "Persisted MESU6 row count": (
        gold_minute_saved_df
            .filter(F.col("Instrument") == "MESU6")
            .count() == expected_rows_per_ticker
    ),
    "Persisted MNQU6 row count": (
        gold_minute_saved_df
            .filter(F.col("Instrument") == "MNQU6")
            .count() == expected_rows_per_ticker
    ),
    "Persisted minute grain is unique": (
        gold_minute_saved_df
            .groupBy(
                "AtlasContractKey",
                "MinuteTimestamp",
            )
            .count()
            .filter(F.col("count") > 1)
            .count() == 0
    ),
    "Persisted governed identity is populated": (
        gold_minute_saved_df
            .filter(
                F.col("AtlasContractKey").isNull()
                | F.col("AtlasContractBusinessKey").isNull()
                | F.col("AtlasProductKey").isNull()
                | F.col("AtlasProductBusinessKey").isNull()
            )
            .count() == 0
    ),
    "Persisted OHLC values are valid": (
        gold_minute_saved_df
            .filter(
                (F.col("Open") <= 0)
                | (F.col("High") <= 0)
                | (F.col("Low") <= 0)
                | (F.col("Close") <= 0)
                | (F.col("High") < F.col("Open"))
                | (F.col("High") < F.col("Close"))
                | (F.col("High") < F.col("Low"))
                | (F.col("Low") > F.col("Open"))
                | (F.col("Low") > F.col("Close"))
            )
            .count() == 0
    ),
    "Persisted activity values are non-negative": (
        gold_minute_saved_df
            .filter(
                (F.col("Volume") < 0)
                | (F.col("TransactionCount") < 0)
                | (F.col("DollarVolume") < 0)
            )
            .count() == 0
    ),
    "Persisted TradingDate is correct": (
        gold_minute_saved_df
            .filter(
                F.col("TradingDate")
                != F.to_date(F.lit("2026-07-14"))
            )
            .count() == 0
    ),
    "Persisted minute timestamps are aligned": (
        gold_minute_saved_df
            .filter(
                (F.second("MinuteTimestamp") != 0)
                | (
                    F.date_format(
                        F.col("MinuteTimestamp"),
                        "SSSSSS",
                    ) != "000000"
                )
            )
            .count() == 0
    ),
    "Persisted Gold load timestamp is consistent": (
        gold_minute_saved_df
            .select("GoldLoadedUTC")
            .distinct()
            .count() == 1
    ),
}

persisted_gold_minute_results_df = spark.createDataFrame(
    [
        (check_name, passed)
        for check_name, passed in persisted_gold_minute_checks.items()
    ],
    ["ValidationCheck", "ValidationPassed"],
)

display(
    persisted_gold_minute_results_df.orderBy("ValidationCheck")
)

failed_persisted_gold_minute_checks = [
    check_name
    for check_name, passed in persisted_gold_minute_checks.items()
    if not passed
]

if failed_persisted_gold_minute_checks:
    raise ValueError(
        "Persisted Massive Futures Gold minute validation failed: "
        + ", ".join(failed_persisted_gold_minute_checks)
    )

print(
    f"Persisted Gold minute row count: "
    f"{persisted_gold_minute_row_count:,}"
)

gold_minute_saved_df.printSchema()

display(
    gold_minute_saved_df
        .orderBy(
            "AtlasContractKey",
            "MinuteTimestamp",
        )
        .limit(20)
)

print(
    "Persisted Massive Futures Gold minute validation passed: "
    f"{len(persisted_gold_minute_checks)} checks completed successfully."
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Create the governed Massive Futures Gold daily candles

daily_partition_window = Window.partitionBy(
    "AtlasContractKey",
    "TradingDate",
)

daily_ascending_window = (
    Window
        .partitionBy(
            "AtlasContractKey",
            "TradingDate",
        )
        .orderBy(F.col("MinuteTimestamp").asc())
)

daily_descending_window = (
    Window
        .partitionBy(
            "AtlasContractKey",
            "TradingDate",
        )
        .orderBy(F.col("MinuteTimestamp").desc())
)

gold_daily_base_df = (
    gold_minute_saved_df
        .withColumn(
            "DailyOpenCandidate",
            F.first("Open").over(daily_ascending_window),
        )
        .withColumn(
            "DailyCloseCandidate",
            F.first("Close").over(daily_descending_window),
        )
)

gold_daily_df = (
    gold_daily_base_df
        .groupBy(
            "AtlasContractKey",
            "AtlasContractBusinessKey",
            "AtlasProductKey",
            "AtlasProductBusinessKey",
            "Instrument",
            "TradingDate",
        )
        .agg(
            F.first("DailyOpenCandidate").cast(price_type).alias("Open"),
            F.max("High").cast(price_type).alias("High"),
            F.min("Low").cast(price_type).alias("Low"),
            F.first("DailyCloseCandidate").cast(price_type).alias("Close"),
            F.sum("Volume").cast("long").alias("TotalVolume"),
            F.sum("TransactionCount").cast("long").alias(
                "TotalTransactions"
            ),
            F.sum("DollarVolume")
                .cast(daily_dollar_volume_type)
                .alias("TotalDollarVolume"),
            F.count("*").cast("long").alias("MinuteBarCount"),
            F.min("MinuteTimestamp").alias("SessionStartTimestamp"),
            F.max("MinuteTimestamp").alias("SessionEndTimestamp"),
        )
        .withColumn(
            "GoldLoadedUTC",
            F.lit(gold_loaded_at_utc).cast("timestamp"),
        )
        .orderBy("AtlasContractKey", "TradingDate")
)

gold_daily_row_count = gold_daily_df.count()

print(f"Gold daily candle rows: {gold_daily_row_count:,}")

gold_daily_df.printSchema()

display(
    gold_daily_df.orderBy(
        "AtlasContractKey",
        "TradingDate",
    )
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Validate the prepared Massive Futures Gold daily candles

gold_daily_validation_checks = {
    "Expected Gold daily row count": (
        gold_daily_df.count() == expected_daily_row_count
    ),
    "MESU6 has one daily row": (
        gold_daily_df
            .filter(F.col("Instrument") == "MESU6")
            .count() == 1
    ),
    "MNQU6 has one daily row": (
        gold_daily_df
            .filter(F.col("Instrument") == "MNQU6")
            .count() == 1
    ),
    "Daily grain is unique": (
        gold_daily_df
            .groupBy(
                "AtlasContractKey",
                "TradingDate",
            )
            .count()
            .filter(F.col("count") > 1)
            .count() == 0
    ),
    "Governed identity fields are populated": (
        gold_daily_df
            .filter(
                F.col("AtlasContractKey").isNull()
                | F.col("AtlasContractBusinessKey").isNull()
                | F.col("AtlasProductKey").isNull()
                | F.col("AtlasProductBusinessKey").isNull()
            )
            .count() == 0
    ),
    "TradingDate remains 2026-07-14": (
        gold_daily_df
            .filter(
                F.col("TradingDate")
                != F.to_date(F.lit("2026-07-14"))
            )
            .count() == 0
    ),
    "MinuteBarCount is 1,380": (
        gold_daily_df
            .filter(F.col("MinuteBarCount") != expected_rows_per_ticker)
            .count() == 0
    ),
    "Session timestamps are correct": (
        gold_daily_df
            .filter(
                (
                    F.col("SessionStartTimestamp")
                    != F.to_timestamp(
                        F.lit("2026-07-13 22:00:00")
                    )
                )
                | (
                    F.col("SessionEndTimestamp")
                    != F.to_timestamp(
                        F.lit("2026-07-14 20:59:00")
                    )
                )
            )
            .count() == 0
    ),
    "Daily OHLC values are positive": (
        gold_daily_df
            .filter(
                (F.col("Open") <= 0)
                | (F.col("High") <= 0)
                | (F.col("Low") <= 0)
                | (F.col("Close") <= 0)
            )
            .count() == 0
    ),
    "Daily OHLC relationships are valid": (
        gold_daily_df
            .filter(
                (F.col("High") < F.col("Open"))
                | (F.col("High") < F.col("Close"))
                | (F.col("High") < F.col("Low"))
                | (F.col("Low") > F.col("Open"))
                | (F.col("Low") > F.col("Close"))
            )
            .count() == 0
    ),
    "Daily activity values are non-negative": (
        gold_daily_df
            .filter(
                (F.col("TotalVolume") < 0)
                | (F.col("TotalTransactions") < 0)
                | (F.col("TotalDollarVolume") < 0)
            )
            .count() == 0
    ),
    "Daily values reconcile with minute table": (
        gold_daily_df.alias("daily")
            .join(
                (
                    gold_minute_saved_df
                        .groupBy(
                            "AtlasContractKey",
                            "TradingDate",
                        )
                        .agg(
                            F.max("High").alias("ExpectedHigh"),
                            F.min("Low").alias("ExpectedLow"),
                            F.sum("Volume").alias("ExpectedVolume"),
                            F.sum("TransactionCount").alias(
                                "ExpectedTransactions"
                            ),
                            F.sum("DollarVolume").alias(
                                "ExpectedDollarVolume"
                            ),
                            F.count("*").alias("ExpectedMinuteBarCount"),
                            F.min("MinuteTimestamp").alias(
                                "ExpectedSessionStart"
                            ),
                            F.max("MinuteTimestamp").alias(
                                "ExpectedSessionEnd"
                            ),
                        )
                ).alias("minute"),
                on=[
                    "AtlasContractKey",
                    "TradingDate",
                ],
                how="inner",
            )
            .filter(
                (F.col("daily.High") != F.col("minute.ExpectedHigh"))
                | (F.col("daily.Low") != F.col("minute.ExpectedLow"))
                | (
                    F.col("daily.TotalVolume")
                    != F.col("minute.ExpectedVolume")
                )
                | (
                    F.col("daily.TotalTransactions")
                    != F.col("minute.ExpectedTransactions")
                )
                | (
                    F.col("daily.TotalDollarVolume")
                    != F.col("minute.ExpectedDollarVolume")
                )
                | (
                    F.col("daily.MinuteBarCount")
                    != F.col("minute.ExpectedMinuteBarCount")
                )
                | (
                    F.col("daily.SessionStartTimestamp")
                    != F.col("minute.ExpectedSessionStart")
                )
                | (
                    F.col("daily.SessionEndTimestamp")
                    != F.col("minute.ExpectedSessionEnd")
                )
            )
            .count() == 0
    ),
    "Daily Open reconciles with first minute Open": (
        gold_daily_df.alias("daily")
            .join(
                (
                    gold_minute_saved_df
                        .withColumn(
                            "row_number_ascending",
                            F.row_number().over(
                                Window
                                    .partitionBy(
                                        "AtlasContractKey",
                                        "TradingDate",
                                    )
                                    .orderBy(
                                        F.col("MinuteTimestamp").asc()
                                    )
                            ),
                        )
                        .filter(F.col("row_number_ascending") == 1)
                        .select(
                            "AtlasContractKey",
                            "TradingDate",
                            F.col("Open").alias("ExpectedOpen"),
                        )
                ).alias("first_minute"),
                on=[
                    "AtlasContractKey",
                    "TradingDate",
                ],
                how="inner",
            )
            .filter(
                F.col("daily.Open")
                != F.col("first_minute.ExpectedOpen")
            )
            .count() == 0
    ),
    "Daily Close reconciles with last minute Close": (
        gold_daily_df.alias("daily")
            .join(
                (
                    gold_minute_saved_df
                        .withColumn(
                            "row_number_descending",
                            F.row_number().over(
                                Window
                                    .partitionBy(
                                        "AtlasContractKey",
                                        "TradingDate",
                                    )
                                    .orderBy(
                                        F.col("MinuteTimestamp").desc()
                                    )
                            ),
                        )
                        .filter(F.col("row_number_descending") == 1)
                        .select(
                            "AtlasContractKey",
                            "TradingDate",
                            F.col("Close").alias("ExpectedClose"),
                        )
                ).alias("last_minute"),
                on=[
                    "AtlasContractKey",
                    "TradingDate",
                ],
                how="inner",
            )
            .filter(
                F.col("daily.Close")
                != F.col("last_minute.ExpectedClose")
            )
            .count() == 0
    ),
    "One Gold load timestamp": (
        gold_daily_df
            .select("GoldLoadedUTC")
            .distinct()
            .count() == 1
    ),
}

gold_daily_validation_results_df = spark.createDataFrame(
    [
        (check_name, passed)
        for check_name, passed in gold_daily_validation_checks.items()
    ],
    ["ValidationCheck", "ValidationPassed"],
)

display(
    gold_daily_validation_results_df.orderBy("ValidationCheck")
)

failed_gold_daily_checks = [
    check_name
    for check_name, passed in gold_daily_validation_checks.items()
    if not passed
]

if failed_gold_daily_checks:
    raise ValueError(
        "Massive Futures Gold daily validation failed: "
        + ", ".join(failed_gold_daily_checks)
    )

print(
    "Massive Futures Gold daily validation passed: "
    f"{len(gold_daily_validation_checks)} checks completed successfully."
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Persist the Massive Futures Gold daily Delta table

(
    gold_daily_df
        .write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(gold_daily_table)
)

print(f"Massive Futures Gold daily table written: {gold_daily_table}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Validate the persisted Massive Futures Gold daily Delta table

gold_daily_saved_df = spark.table(gold_daily_table)

persisted_gold_daily_row_count = gold_daily_saved_df.count()

persisted_gold_daily_checks = {
    "Persisted daily row count matches prepared row count": (
        persisted_gold_daily_row_count == gold_daily_row_count
    ),
    "Persisted MESU6 daily row count": (
        gold_daily_saved_df
            .filter(F.col("Instrument") == "MESU6")
            .count() == 1
    ),
    "Persisted MNQU6 daily row count": (
        gold_daily_saved_df
            .filter(F.col("Instrument") == "MNQU6")
            .count() == 1
    ),
    "Persisted daily grain is unique": (
        gold_daily_saved_df
            .groupBy(
                "AtlasContractKey",
                "TradingDate",
            )
            .count()
            .filter(F.col("count") > 1)
            .count() == 0
    ),
    "Persisted governed identity is populated": (
        gold_daily_saved_df
            .filter(
                F.col("AtlasContractKey").isNull()
                | F.col("AtlasContractBusinessKey").isNull()
                | F.col("AtlasProductKey").isNull()
                | F.col("AtlasProductBusinessKey").isNull()
            )
            .count() == 0
    ),
    "Persisted TradingDate is correct": (
        gold_daily_saved_df
            .filter(
                F.col("TradingDate")
                != F.to_date(F.lit("2026-07-14"))
            )
            .count() == 0
    ),
    "Persisted MinuteBarCount is correct": (
        gold_daily_saved_df
            .filter(F.col("MinuteBarCount") != expected_rows_per_ticker)
            .count() == 0
    ),
    "Persisted session timestamps are correct": (
        gold_daily_saved_df
            .filter(
                (
                    F.col("SessionStartTimestamp")
                    != F.to_timestamp(
                        F.lit("2026-07-13 22:00:00")
                    )
                )
                | (
                    F.col("SessionEndTimestamp")
                    != F.to_timestamp(
                        F.lit("2026-07-14 20:59:00")
                    )
                )
            )
            .count() == 0
    ),
    "Persisted daily OHLC values are valid": (
        gold_daily_saved_df
            .filter(
                (F.col("Open") <= 0)
                | (F.col("High") <= 0)
                | (F.col("Low") <= 0)
                | (F.col("Close") <= 0)
                | (F.col("High") < F.col("Open"))
                | (F.col("High") < F.col("Close"))
                | (F.col("High") < F.col("Low"))
                | (F.col("Low") > F.col("Open"))
                | (F.col("Low") > F.col("Close"))
            )
            .count() == 0
    ),
    "Persisted daily activity values are non-negative": (
        gold_daily_saved_df
            .filter(
                (F.col("TotalVolume") < 0)
                | (F.col("TotalTransactions") < 0)
                | (F.col("TotalDollarVolume") < 0)
            )
            .count() == 0
    ),
    "Persisted daily values reconcile with persisted minute table": (
        gold_daily_saved_df.alias("daily")
            .join(
                (
                    gold_minute_saved_df
                        .groupBy(
                            "AtlasContractKey",
                            "TradingDate",
                        )
                        .agg(
                            F.max("High").alias("ExpectedHigh"),
                            F.min("Low").alias("ExpectedLow"),
                            F.sum("Volume").alias("ExpectedVolume"),
                            F.sum("TransactionCount").alias(
                                "ExpectedTransactions"
                            ),
                            F.sum("DollarVolume").alias(
                                "ExpectedDollarVolume"
                            ),
                            F.count("*").alias("ExpectedMinuteBarCount"),
                            F.min("MinuteTimestamp").alias(
                                "ExpectedSessionStart"
                            ),
                            F.max("MinuteTimestamp").alias(
                                "ExpectedSessionEnd"
                            ),
                        )
                ).alias("minute"),
                on=[
                    "AtlasContractKey",
                    "TradingDate",
                ],
                how="inner",
            )
            .filter(
                (F.col("daily.High") != F.col("minute.ExpectedHigh"))
                | (F.col("daily.Low") != F.col("minute.ExpectedLow"))
                | (
                    F.col("daily.TotalVolume")
                    != F.col("minute.ExpectedVolume")
                )
                | (
                    F.col("daily.TotalTransactions")
                    != F.col("minute.ExpectedTransactions")
                )
                | (
                    F.col("daily.TotalDollarVolume")
                    != F.col("minute.ExpectedDollarVolume")
                )
                | (
                    F.col("daily.MinuteBarCount")
                    != F.col("minute.ExpectedMinuteBarCount")
                )
                | (
                    F.col("daily.SessionStartTimestamp")
                    != F.col("minute.ExpectedSessionStart")
                )
                | (
                    F.col("daily.SessionEndTimestamp")
                    != F.col("minute.ExpectedSessionEnd")
                )
            )
            .count() == 0
    ),
    "Persisted Gold load timestamp is consistent": (
        gold_daily_saved_df
            .select("GoldLoadedUTC")
            .distinct()
            .count() == 1
    ),
}

persisted_gold_daily_results_df = spark.createDataFrame(
    [
        (check_name, passed)
        for check_name, passed in persisted_gold_daily_checks.items()
    ],
    ["ValidationCheck", "ValidationPassed"],
)

display(
    persisted_gold_daily_results_df.orderBy("ValidationCheck")
)

failed_persisted_gold_daily_checks = [
    check_name
    for check_name, passed in persisted_gold_daily_checks.items()
    if not passed
]

if failed_persisted_gold_daily_checks:
    raise ValueError(
        "Persisted Massive Futures Gold daily validation failed: "
        + ", ".join(failed_persisted_gold_daily_checks)
    )

print(
    f"Persisted Gold daily row count: "
    f"{persisted_gold_daily_row_count:,}"
)

gold_daily_saved_df.printSchema()

display(
    gold_daily_saved_df.orderBy(
        "AtlasContractKey",
        "TradingDate",
    )
)

print(
    "Persisted Massive Futures Gold daily validation passed: "
    f"{len(persisted_gold_daily_checks)} checks completed successfully."
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
