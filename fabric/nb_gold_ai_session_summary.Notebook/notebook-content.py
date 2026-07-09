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

# # Atlas Trading Intelligence Platform
# 
# ## AI Trading Intelligence Layer
# 
# **Notebook:** `nb_gold_ai_session_summary`
# 
# **Purpose:** Generate AI-ready market session summaries from validated Gold OHLC candle data for downstream analytics and future Large Language Model (LLM) integration.
# 
# **Inputs:**
# - `Tables/gold_cqg_daily_candles` (Delta)
# - `Tables/gold_cqg_minute_candles` (Delta)
# 
# **Outputs:**
# - `Tables/gold_ai_session_summary` (Delta)
# 
# **Gold Contract:** `docs/01_Architecture/Gold_Contract.md`
# 
# **Release:** `v0.8.0 – AI Trading Intelligence Foundation`
# 
# ---
# 
# # Engineering Rule
# 
# This notebook prepares deterministic market session intelligence.
# 
# It **does not** generate trading recommendations, price forecasts, or trading signals.
# 
# All AI-ready attributes are derived from validated Gold analytical data to ensure reproducible outputs suitable for reporting and future LLM enrichment.
# 
# The notebook establishes the foundation for future Azure AI and Microsoft Fabric AI capabilities without introducing non-deterministic processing into the core data pipeline.
# 
# ---
# 
# # Scope
# 
# This notebook creates an AI-ready summary of each trading session by combining daily and intraday market analytics.
# 
# The resulting Delta table forms the foundation for future capabilities including:
# 
# - Natural language market summaries
# - Azure AI integration
# - Microsoft Fabric AI functions
# - Prompt engineering
# - AI-assisted trading analytics
# 
# The output is intended for consumption by the Direct Lake Semantic Model and future AI services while maintaining a fully reproducible engineering workflow.


# CELL ********************

# ============================================================
# Atlas Trading Intelligence Platform
# Notebook: nb_gold_ai_session_summary
# Configuration
# ============================================================

from pyspark.sql import functions as F
from pyspark.sql.window import Window

# ------------------------------------------------------------
# Source Tables
# ------------------------------------------------------------

DAILY_TABLE = "Atlas.lh_atlas_dev.dbo.gold_cqg_daily_candles"
MINUTE_TABLE = "Atlas.lh_atlas_dev.dbo.gold_cqg_minute_candles"

# ------------------------------------------------------------
# Output Table
# ------------------------------------------------------------

OUTPUT_TABLE = "gold_ai_session_summary"

# ------------------------------------------------------------
# AI Configuration
# ------------------------------------------------------------

PROMPT_VERSION = "v1.0"

# Daily Range (%) thresholds
LOW_VOLATILITY_THRESHOLD = 0.25
HIGH_VOLATILITY_THRESHOLD = 0.75

# Session Trade Count thresholds
LOW_ACTIVITY_THRESHOLD = 1000
HIGH_ACTIVITY_THRESHOLD = 5000

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ============================================================
# Load Gold Analytics Tables
# ============================================================

daily = spark.table(DAILY_TABLE)
minute = spark.table(MINUTE_TABLE)

print(f"Daily candles : {daily.count():,}")
print(f"Minute candles: {minute.count():,}")

display(daily.limit(5))
display(minute.limit(5))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ============================================================
# Derive Intraday Session Statistics
# ============================================================

most_active_window = (
    Window
    .partitionBy("Instrument", "TradingDate")
    .orderBy(F.col("TradeCount").desc(), F.col("MinuteTimestamp").asc())
)

most_active_minute = (
    minute
    .withColumn("ActivityRank", F.row_number().over(most_active_window))
    .filter(F.col("ActivityRank") == 1)
    .select(
        "Instrument",
        "TradingDate",
        F.col("MinuteTimestamp").alias("MostActiveMinute"),
        F.col("TradeCount").alias("MostActiveMinuteTradeCount")
    )
)

session_stats = (
    minute
    .groupBy("Instrument", "TradingDate")
    .agg(
        F.max("High").alias("SessionHigh"),
        F.min("Low").alias("SessionLow"),
        F.sum("TradeCount").alias("SessionTradeCount")
    )
    .join(
        most_active_minute,
        on=["Instrument", "TradingDate"],
        how="left"
    )
)

display(session_stats.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ============================================================
# Build Gold AI Session Summary
# ============================================================

gold_ai_session_summary = (
    daily
    .join(
        session_stats,
        on=["Instrument", "TradingDate"],
        how="left"
    )
    .withColumn(
        "DailyRange",
        F.col("High") - F.col("Low")
    )
    .withColumn(
        "DailyMovement",
        F.col("Close") - F.col("Open")
    )
    .withColumn(
        "DailyRangePct",
        (F.col("DailyRange") / F.col("Open")) * 100
    )
    .withColumn(
        "DailyReturnPct",
        (F.col("DailyMovement") / F.col("Open")) * 100
    )
    .withColumn(
        "PriceDirection",
        F.when(F.col("Close") > F.col("Open"), "Higher Close")
         .when(F.col("Close") < F.col("Open"), "Lower Close")
         .otherwise("Unchanged")
    )
    .withColumn(
        "SessionDirection",
        F.when(F.col("DailyReturnPct") > 0, "Bullish")
         .when(F.col("DailyReturnPct") < 0, "Bearish")
         .otherwise("Flat")
    )
    .withColumn(
        "VolatilityBand",
        F.when(F.col("DailyRangePct") < LOW_VOLATILITY_THRESHOLD, "Low")
         .when(F.col("DailyRangePct") <= HIGH_VOLATILITY_THRESHOLD, "Moderate")
         .otherwise("High")
    )
    .withColumn(
        "ActivityBand",
        F.when(F.col("SessionTradeCount") < LOW_ACTIVITY_THRESHOLD, "Low")
         .when(F.col("SessionTradeCount") <= HIGH_ACTIVITY_THRESHOLD, "Moderate")
         .otherwise("High")
    )
    .withColumn(
        "SessionCharacter",
        F.concat_ws(
            " / ",
            F.col("SessionDirection"),
            F.concat(F.col("VolatilityBand"), F.lit(" Volatility")),
            F.concat(F.col("ActivityBand"), F.lit(" Activity"))
        )
    )
    .withColumn(
        "PromptVersion",
        F.lit(PROMPT_VERSION)
    )
)

display(gold_ai_session_summary.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ============================================================
# Generate AI Prompt Text
# ============================================================

gold_ai_session_summary = (
    gold_ai_session_summary
    .withColumn(
        "PromptTemplate",
        F.concat(
            F.lit("You are analysing a historical trading session for "),
            F.col("Instrument"),
            F.lit(" on "),
            F.col("TradingDate").cast("string"),
            F.lit(". The session opened at "),
            F.col("Open").cast("string"),
            F.lit(", reached a high of "),
            F.col("High").cast("string"),
            F.lit(", a low of "),
            F.col("Low").cast("string"),
            F.lit(", and closed at "),
            F.col("Close").cast("string"),
            F.lit(". The daily return was "),
            F.round(F.col("DailyReturnPct"), 3).cast("string"),
            F.lit("% and the daily range was "),
            F.round(F.col("DailyRangePct"), 3).cast("string"),
            F.lit("%. The session was classified as "),
            F.col("SessionCharacter"),
            F.lit(". Produce a concise market summary without giving trading advice.")
        )
    )
)

display(
    gold_ai_session_summary
    .select(
        "Instrument",
        "TradingDate",
        "SessionCharacter",
        "PromptVersion",
        "PromptTemplate"
    )
    .limit(5)
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ============================================================
# Select Final Output Columns
# ============================================================

gold_ai_session_summary = (
    gold_ai_session_summary
    .select(
        "Instrument",
        "TradingDate",
        "Open",
        "High",
        "Low",
        "Close",
        "TotalTrades",
        "SessionHigh",
        "SessionLow",
        "SessionTradeCount",
        "MostActiveMinute",
        "MostActiveMinuteTradeCount",
        "DailyRange",
        "DailyMovement",
        "DailyRangePct",
        "DailyReturnPct",
        "PriceDirection",
        "SessionDirection",
        "VolatilityBand",
        "ActivityBand",
        "SessionCharacter",
        "PromptVersion",
        "PromptTemplate"
    )
    .orderBy("Instrument", "TradingDate")
)

display(gold_ai_session_summary.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ============================================================
# Validation Checks
# ============================================================

source_daily_count = daily.count()
output_count = gold_ai_session_summary.count()

duplicate_count = (
    gold_ai_session_summary
    .groupBy("Instrument", "TradingDate")
    .count()
    .filter(F.col("count") > 1)
    .count()
)

missing_prompt_count = (
    gold_ai_session_summary
    .filter(F.col("PromptText").isNull())
    .count()
)

missing_classification_count = (
    gold_ai_session_summary
    .filter(
        F.col("SessionDirection").isNull()
        | F.col("VolatilityBand").isNull()
        | F.col("ActivityBand").isNull()
        | F.col("SessionCharacter").isNull()
    )
    .count()
)

print(f"Source daily rows              : {source_daily_count:,}")
print(f"AI session summary rows        : {output_count:,}")
print(f"Duplicate Instrument/Date rows : {duplicate_count:,}")
print(f"Missing prompt rows            : {missing_prompt_count:,}")
print(f"Missing classification rows    : {missing_classification_count:,}")

assert output_count == source_daily_count, "Output row count does not match daily candle row count"
assert duplicate_count == 0, "Duplicate Instrument/TradingDate rows found"
assert missing_prompt_count == 0, "PromptText contains null values"
assert missing_classification_count == 0, "Classification columns contain null values"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ============================================================
# Persist Gold AI Session Summary
# ============================================================

(
    gold_ai_session_summary
    .write
    .mode("overwrite")
    .format("delta")
    .saveAsTable(f"Atlas.lh_atlas_dev.dbo.{OUTPUT_TABLE}")
)

print(f"Successfully created Delta table: {OUTPUT_TABLE}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ============================================================
# Verify Persisted Delta Table
# ============================================================

verify_df = spark.table(f"Atlas.lh_atlas_dev.dbo.{OUTPUT_TABLE}")

print(f"Persisted rows : {verify_df.count():,}")

display(verify_df.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# ============================================================
# Notebook Complete
# ============================================================

print("nb_gold_ai_session_summary completed successfully")
print(f"Output table : {OUTPUT_TABLE}")
print(f"Rows written : {verify_df.count():,}")
print(f"Prompt version: {PROMPT_VERSION}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
