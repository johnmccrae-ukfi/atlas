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
# ## Gold Layer
# 
# **Notebook:** `nb_gold_cqg_ohlc_candles`
# 
# **Purpose:** Generate business-ready OHLC candle tables from validated Silver CQG tick data.
# 
# **Input:** `Tables/silver_cqg_ticks` (Delta)
# 
# **Outputs:**
# 
# - `Tables/gold_cqg_minute_candles` (Delta)
# - `Tables/gold_cqg_daily_candles` (Delta)
# 
# **Gold Contract:** `docs/01_Architecture/Gold_Contract.md`
# 
# **Release:** `v0.4.0 — Gold Foundation`
# 
# ---
# 
# ## Engineering Rule
# 
# Open and Close prices must be calculated using preserved event ordering.
# 
# They must **never** be calculated using `MIN()` or `MAX()`.
# 
# - **Open** = first valid event in the candle window
# - **Close** = last valid event in the candle window
# - **High** = maximum price in the candle window
# - **Low** = minimum price in the candle window
# 
# ---
# 
# ## Scope
# 
# This notebook creates the first Gold analytical layer for reporting and Power BI visualization.
# 
# It does not create trading signals, indicators, forecasts, backtests, or AI commentary.

# CELL ********************

# Atlas Market Data Platform
# Notebook: nb_gold_cqg_ohlc_candles
# Purpose: Generate Gold OHLC candle tables from Silver CQG ticks

from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import DecimalType

silver_table = "silver_cqg_ticks"

gold_minute_table = "gold_cqg_minute_candles"
gold_daily_table = "gold_cqg_daily_candles"

print(f"Silver source table: {silver_table}")
print(f"Gold minute target table: {gold_minute_table}")
print(f"Gold daily target table: {gold_daily_table}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

silver_df = spark.table(silver_table)

print(f"Silver row count: {silver_df.count():,}")

silver_df.printSchema()

display(silver_df.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Retain only validated Silver events for Gold aggregation

gold_source_df = (
    silver_df
        .filter(F.col("silver_quality_status") == "Valid")
        .filter(F.col("is_valid_price"))
        .filter(F.col("is_valid_time"))
)

print(f"Gold source row count: {gold_source_df.count():,}")

display(gold_source_df.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Retain only validated Silver events for Gold aggregation

gold_source_df = (
    silver_df
        .filter(F.col("silver_quality_status") == "Valid")
        .filter(F.col("is_valid_price") == True)
        .filter(F.col("is_valid_time") == True)
)

print(f"Gold source row count: {gold_source_df.count():,}")

display(gold_source_df.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Build Gold minute OHLC candles using preserved Silver event ordering

minute_partition = Window.partitionBy(
    "instrument",
    "trade_date",
    "event_minute_ts"
)

minute_order_asc = minute_partition.orderBy(F.col("event_sequence_in_minute").asc())
minute_order_desc = minute_partition.orderBy(F.col("event_sequence_in_minute").desc())

minute_ranked_df = (
    gold_source_df
        .withColumn("open_price", F.first("price_decimal").over(minute_order_asc))
        .withColumn("close_price", F.first("price_decimal").over(minute_order_desc))
        .withColumn("first_event_sequence", F.min("event_sequence_in_minute").over(minute_partition))
        .withColumn("last_event_sequence", F.max("event_sequence_in_minute").over(minute_partition))
)

gold_minute_df = (
    minute_ranked_df
        .groupBy(
            "instrument",
            "trade_date",
            "event_minute_ts"
        )
        .agg(
            F.first("open_price").alias("Open"),
            F.max("price_decimal").alias("High"),
            F.min("price_decimal").alias("Low"),
            F.first("close_price").alias("Close"),
            F.lit(None).cast("double").alias("Volume"),
            F.count("*").alias("TradeCount"),
            F.first("first_event_sequence").alias("FirstEventSequence"),
            F.first("last_event_sequence").alias("LastEventSequence"),
            F.current_timestamp().alias("GoldLoadedUTC")
        )
        .select(
            F.col("instrument").alias("Instrument"),
            F.col("trade_date").alias("TradingDate"),
            F.col("event_minute_ts").alias("MinuteTimestamp"),
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "TradeCount",
            "FirstEventSequence",
            "LastEventSequence",
            "GoldLoadedUTC"
        )
        .withColumn("Open", F.col("Open").cast(DecimalType(18, 5)))
        .withColumn("High", F.col("High").cast(DecimalType(18, 5)))
        .withColumn("Low", F.col("Low").cast(DecimalType(18, 5)))
        .withColumn("Close", F.col("Close").cast(DecimalType(18, 5)))
        .orderBy("Instrument", "TradingDate", "MinuteTimestamp")
)

print(f"Gold minute candle count: {gold_minute_df.count():,}")

display(gold_minute_df.limit(20))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Validate first generated minute candle against underlying ordered Silver events

# Automatically select the first generated candle for validation
first_candle = (
    gold_minute_df
        .orderBy("Instrument", "TradingDate", "MinuteTimestamp")
        .first()
)

validation_instrument = first_candle["Instrument"]
validation_minute_ts = first_candle["MinuteTimestamp"]

print(f"Validation instrument: {validation_instrument}")
print(f"Validation minute timestamp: {validation_minute_ts}")

# Get the underlying ordered Silver events for the selected candle
validation_events_df = (
    gold_source_df
        .filter(F.col("instrument") == validation_instrument)
        .filter(F.col("event_minute_ts") == validation_minute_ts)
        .orderBy("event_sequence_in_minute")
)

# Get the generated Gold candle
validation_candle_df = (
    gold_minute_df
        .filter(F.col("Instrument") == validation_instrument)
        .filter(F.col("MinuteTimestamp") == validation_minute_ts)
)

print("Underlying ordered Silver events:")
display(
    validation_events_df.select(
        "instrument",
        "trade_date",
        "event_minute_ts",
        "event_sequence_in_minute",
        "price_decimal"
    )
)

print("Generated Gold minute candle:")
display(validation_candle_df)

# Calculate expected values directly from the ordered Silver events
validation_summary_df = (
    validation_events_df
        .agg(
            F.first("price_decimal").cast(DecimalType(18, 5)).alias("ExpectedOpen"),
            F.max("price_decimal").cast(DecimalType(18, 5)).alias("ExpectedHigh"),
            F.min("price_decimal").cast(DecimalType(18, 5)).alias("ExpectedLow"),
            F.last("price_decimal").cast(DecimalType(18, 5)).alias("ExpectedClose"),
            F.count("*").alias("ExpectedTradeCount"),
            F.min("event_sequence_in_minute").alias("ExpectedFirstEventSequence"),
            F.max("event_sequence_in_minute").alias("ExpectedLastEventSequence")
        )
)

print("Expected OHLC values from ordered Silver events:")
display(validation_summary_df)

# Compare expected values with generated Gold candle
validation_comparison_df = (
    validation_candle_df
        .crossJoin(validation_summary_df)
        .select(
            "Instrument",
            "TradingDate",
            "MinuteTimestamp",
            "Open",
            "ExpectedOpen",
            "High",
            "ExpectedHigh",
            "Low",
            "ExpectedLow",
            "Close",
            "ExpectedClose",
            "TradeCount",
            "ExpectedTradeCount",
            "FirstEventSequence",
            "ExpectedFirstEventSequence",
            "LastEventSequence",
            "ExpectedLastEventSequence",
            (
                (F.col("Open") == F.col("ExpectedOpen")) &
                (F.col("High") == F.col("ExpectedHigh")) &
                (F.col("Low") == F.col("ExpectedLow")) &
                (F.col("Close") == F.col("ExpectedClose")) &
                (F.col("TradeCount") == F.col("ExpectedTradeCount")) &
                (F.col("FirstEventSequence") == F.col("ExpectedFirstEventSequence")) &
                (F.col("LastEventSequence") == F.col("ExpectedLastEventSequence"))
            ).alias("ValidationPassed")
        )
)

print("Validation comparison:")
display(validation_comparison_df)

# Fail the notebook if the generated candle does not match the expected values
validation_failed_count = (
    validation_comparison_df
        .filter(F.col("ValidationPassed") == False)
        .count()
)

if validation_failed_count > 0:
    raise ValueError("Gold minute candle validation failed.")

print("Gold minute candle validation passed.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Persist Gold minute candles as Delta table

(
    gold_minute_df
        .write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(gold_minute_table)
)

print(f"Gold minute candle table written: {gold_minute_table}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Validate persisted Gold minute candle table

gold_minute_saved_df = spark.table(gold_minute_table)

print(f"Persisted Gold minute candle count: {gold_minute_saved_df.count():,}")

gold_minute_saved_df.printSchema()

display(
    gold_minute_saved_df
        .orderBy("Instrument", "TradingDate", "MinuteTimestamp")
        .limit(20)
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Build Gold daily OHLC candles from persisted minute candles

daily_partition = Window.partitionBy(
    "Instrument",
    "TradingDate"
)

daily_order_asc = daily_partition.orderBy(F.col("MinuteTimestamp").asc())
daily_order_desc = daily_partition.orderBy(F.col("MinuteTimestamp").desc())

daily_ranked_df = (
    gold_minute_saved_df
        .withColumn("daily_open", F.first("Open").over(daily_order_asc))
        .withColumn("daily_close", F.first("Close").over(daily_order_desc))
)

gold_daily_df = (
    daily_ranked_df
        .groupBy("Instrument", "TradingDate")
        .agg(
            F.first("daily_open").alias("Open"),
            F.max("High").alias("High"),
            F.min("Low").alias("Low"),
            F.first("daily_close").alias("Close"),
            F.sum("TradeCount").alias("TotalTrades"),
            F.current_timestamp().alias("GoldLoadedUTC")
        )
        .withColumn("Open", F.col("Open").cast(DecimalType(18, 5)))
        .withColumn("High", F.col("High").cast(DecimalType(18, 5)))
        .withColumn("Low", F.col("Low").cast(DecimalType(18, 5)))
        .withColumn("Close", F.col("Close").cast(DecimalType(18, 5)))
        .orderBy("Instrument", "TradingDate")
)

print(f"Gold daily candle count: {gold_daily_df.count():,}")

display(gold_daily_df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Persist Gold daily candles as Delta table

(
    gold_daily_df
        .write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(gold_daily_table)
)

print(f"Gold daily candle table written: {gold_daily_table}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Validate persisted Gold daily candle table

gold_daily_saved_df = spark.table(gold_daily_table)

print(f"Persisted Gold daily candle count: {gold_daily_saved_df.count():,}")

gold_daily_saved_df.printSchema()

display(
    gold_daily_saved_df
        .orderBy("Instrument", "TradingDate")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
