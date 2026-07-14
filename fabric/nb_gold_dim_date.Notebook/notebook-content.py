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

# # Atlas Enterprise AI Intelligence Platform
# 
# ## Gold Date Dimension
# 
# **Notebook:** `nb_gold_dim_date`
# 
# **Purpose:** Generate a governed Gold date dimension for historical reporting, semantic-model relationships, time intelligence, and report navigation.
# 
# **Inputs:**
# 
# - `Tables/gold_cqg_daily_candles`
# - `Tables/gold_cqg_minute_candles`
# 
# **Output:**
# 
# - `Tables/gold_dim_date`
# 
# **Grain:**
# 
# One row per calendar date.
# 
# **Date range:**
# 
# The minimum `TradingDate` found across the current Gold candle tables through the maximum `TradingDate` found across those tables.
# 
# **Release:**
# 
# `v1.2.0 — Reporting Navigation and Time Intelligence`
# 
# ---
# 
# ## Design principles
# 
# - The date range is derived dynamically from governed Gold data.
# - Every calendar date in the range is represented, including weekends.
# - Trading-day status is not inferred from the presence or absence of candle data.
# - The dimension contains deterministic reporting attributes only.
# - The table is intended for Direct Lake semantic-model relationships and reusable time intelligence.


# CELL ********************

# Atlas Enterprise AI Intelligence Platform
# Notebook: nb_gold_dim_date
# Purpose: Generate the governed Gold date dimension

from pyspark.sql import functions as F
from pyspark.sql.types import DateType

gold_daily_table = "gold_cqg_daily_candles"
gold_minute_table = "gold_cqg_minute_candles"
gold_date_table = "gold_dim_date"

print(f"Gold daily source table: {gold_daily_table}")
print(f"Gold minute source table: {gold_minute_table}")
print(f"Gold date target table: {gold_date_table}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Load Gold candle dates and calculate the governed date range

gold_daily_dates_df = (
    spark.table(gold_daily_table)
        .select(F.col("TradingDate").cast(DateType()).alias("TradingDate"))
)

gold_minute_dates_df = (
    spark.table(gold_minute_table)
        .select(F.col("TradingDate").cast(DateType()).alias("TradingDate"))
)

gold_date_range_df = (
    gold_daily_dates_df
        .unionByName(gold_minute_dates_df)
        .filter(F.col("TradingDate").isNotNull())
        .agg(
            F.min("TradingDate").alias("MinimumTradingDate"),
            F.max("TradingDate").alias("MaximumTradingDate")
        )
)

gold_date_range = gold_date_range_df.first()

minimum_trading_date = gold_date_range["MinimumTradingDate"]
maximum_trading_date = gold_date_range["MaximumTradingDate"]

if minimum_trading_date is None or maximum_trading_date is None:
    raise ValueError(
        "Unable to generate gold_dim_date because no valid TradingDate values "
        "were found in the Gold candle tables."
    )

print(f"Minimum Gold trading date: {minimum_trading_date}")
print(f"Maximum Gold trading date: {maximum_trading_date}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Generate one row per calendar date across the governed Gold date range

gold_dim_date_df = (
    spark.sql(
        f"""
        SELECT EXPLODE(
            SEQUENCE(
                TO_DATE('{minimum_trading_date}'),
                TO_DATE('{maximum_trading_date}'),
                INTERVAL 1 DAY
            )
        ) AS Date
        """
    )
    .orderBy("Date")
)

expected_date_count = (
    maximum_trading_date - minimum_trading_date
).days + 1

actual_date_count = gold_dim_date_df.count()

if actual_date_count != expected_date_count:
    raise ValueError(
        "Gold date dimension continuity validation failed. "
        f"Expected {expected_date_count} dates but generated {actual_date_count}."
    )

print(f"Expected calendar date count: {expected_date_count}")
print(f"Generated calendar date count: {actual_date_count}")

display(gold_dim_date_df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Add deterministic reporting attributes to the Gold date dimension

gold_dim_date_enriched_df = (
    gold_dim_date_df
        .withColumn("Year", F.year("Date"))
        .withColumn("QuarterNumber", F.quarter("Date"))
        .withColumn(
            "Quarter",
            F.concat(
                F.lit("Q"),
                F.quarter("Date").cast("string")
            )
        )
        .withColumn("MonthNumber", F.month("Date"))
        .withColumn("Month", F.date_format("Date", "MMMM"))
        .withColumn("MonthShort", F.date_format("Date", "MMM"))
        .withColumn("YearMonth", F.date_format("Date", "yyyy-MM"))
        .withColumn(
            "YearMonthSort",
            F.year("Date") * 100 + F.month("Date")
        )
        .withColumn("DayOfMonth", F.dayofmonth("Date"))
        .withColumn(
            "DayOfWeekNumber",
            F.when(F.dayofweek("Date") == 1, 7)
             .otherwise(F.dayofweek("Date") - 1)
        )
        .withColumn("DayOfWeek", F.date_format("Date", "EEEE"))
        .withColumn(
            "IsWeekend",
            F.col("DayOfWeekNumber").isin(6, 7)
        )
        .select(
            "Date",
            "Year",
            "QuarterNumber",
            "Quarter",
            "MonthNumber",
            "Month",
            "MonthShort",
            "YearMonth",
            "YearMonthSort",
            "DayOfMonth",
            "DayOfWeekNumber",
            "DayOfWeek",
            "IsWeekend"
        )
        .orderBy("Date")
)

gold_dim_date_enriched_df.printSchema()

display(gold_dim_date_enriched_df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Validate the generated Gold date dimension

date_validation_df = (
    gold_dim_date_enriched_df
        .agg(
            F.count("*").alias("RowCount"),
            F.countDistinct("Date").alias("DistinctDateCount"),
            F.min("Date").alias("MinimumDate"),
            F.max("Date").alias("MaximumDate"),
            F.sum(
                F.when(F.col("Date").isNull(), 1).otherwise(0)
            ).alias("NullDateCount")
        )
)

date_validation = date_validation_df.first()

row_count = date_validation["RowCount"]
distinct_date_count = date_validation["DistinctDateCount"]
minimum_date = date_validation["MinimumDate"]
maximum_date = date_validation["MaximumDate"]
null_date_count = date_validation["NullDateCount"]

if row_count != expected_date_count:
    raise ValueError(
        f"Date dimension row-count validation failed. "
        f"Expected {expected_date_count}, found {row_count}."
    )

if distinct_date_count != row_count:
    raise ValueError(
        "Date dimension uniqueness validation failed. "
        f"Rows: {row_count}, distinct dates: {distinct_date_count}."
    )

if minimum_date != minimum_trading_date:
    raise ValueError(
        f"Minimum date validation failed. "
        f"Expected {minimum_trading_date}, found {minimum_date}."
    )

if maximum_date != maximum_trading_date:
    raise ValueError(
        f"Maximum date validation failed. "
        f"Expected {maximum_trading_date}, found {maximum_date}."
    )

if null_date_count != 0:
    raise ValueError(
        f"Date dimension contains {null_date_count} null Date values."
    )

print("Gold date dimension validation passed.")
print(f"Rows: {row_count}")
print(f"Distinct dates: {distinct_date_count}")
print(f"Minimum date: {minimum_date}")
print(f"Maximum date: {maximum_date}")
print(f"Null dates: {null_date_count}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Persist the governed Gold date dimension as a Delta table

(
    gold_dim_date_enriched_df
        .write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(gold_date_table)
)

print(f"Gold date dimension table written: {gold_date_table}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Reload and validate the persisted Gold date dimension

gold_dim_date_saved_df = spark.table(gold_date_table)

persisted_validation_df = (
    gold_dim_date_saved_df
        .agg(
            F.count("*").alias("RowCount"),
            F.countDistinct("Date").alias("DistinctDateCount"),
            F.min("Date").alias("MinimumDate"),
            F.max("Date").alias("MaximumDate")
        )
)

persisted_validation = persisted_validation_df.first()

if persisted_validation["RowCount"] != expected_date_count:
    raise ValueError(
        "Persisted date dimension row-count validation failed."
    )

if persisted_validation["DistinctDateCount"] != expected_date_count:
    raise ValueError(
        "Persisted date dimension uniqueness validation failed."
    )

if persisted_validation["MinimumDate"] != minimum_trading_date:
    raise ValueError(
        "Persisted date dimension minimum-date validation failed."
    )

if persisted_validation["MaximumDate"] != maximum_trading_date:
    raise ValueError(
        "Persisted date dimension maximum-date validation failed."
    )

print("Persisted Gold date dimension validation passed.")
print(f"Rows: {persisted_validation['RowCount']}")
print(f"Distinct dates: {persisted_validation['DistinctDateCount']}")
print(f"Minimum date: {persisted_validation['MinimumDate']}")
print(f"Maximum date: {persisted_validation['MaximumDate']}")

display(
    gold_dim_date_saved_df
        .orderBy("Date")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Validate that every Gold candle TradingDate exists in gold_dim_date

daily_unmatched_count = (
    spark.table(gold_daily_table)
        .select(F.col("TradingDate").cast("date").alias("TradingDate"))
        .distinct()
        .join(
            spark.table(gold_date_table).select(F.col("Date")),
            F.col("TradingDate") == F.col("Date"),
            "left_anti"
        )
        .count()
)

minute_unmatched_count = (
    spark.table(gold_minute_table)
        .select(F.col("TradingDate").cast("date").alias("TradingDate"))
        .distinct()
        .join(
            spark.table(gold_date_table).select(F.col("Date")),
            F.col("TradingDate") == F.col("Date"),
            "left_anti"
        )
        .count()
)

daily_null_count = (
    spark.table(gold_daily_table)
        .filter(F.col("TradingDate").isNull())
        .count()
)

minute_null_count = (
    spark.table(gold_minute_table)
        .filter(F.col("TradingDate").isNull())
        .count()
)

print(f"Daily unmatched trading dates: {daily_unmatched_count}")
print(f"Minute unmatched trading dates: {minute_unmatched_count}")
print(f"Daily null trading dates: {daily_null_count}")
print(f"Minute null trading dates: {minute_null_count}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
