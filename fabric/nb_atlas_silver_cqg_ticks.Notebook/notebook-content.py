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
# ## Silver Layer
# 
# **Notebook:** nb_atlas_silver_cqg_ticks
# 
# **Purpose:**
# Transform Bronze CQG legacy tick data into the curated Silver Delta table while preserving event ordering, provenance and data quality.
# 
# **Input:**
# Tables/bronze_cqg_legacy_ticks (Delta)
# 
# **Output:**
# Tables/silver_cqg_ticks (Delta)
# 
# **Expected rows:**
# 17,317,408
# 
# **Silver Contract:**
# docs/01_Architecture/Silver_Contract.md

# CELL ********************

# Atlas Market Data Platform
# Notebook: nb_atlas_silver_cqg_ticks
# Purpose: Transform Bronze CQG legacy tick data into the Silver CQG ticks table

from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import DecimalType

bronze_table = "bronze_cqg_legacy_ticks"
silver_table = "silver_cqg_ticks"

print(f"Bronze source table: {bronze_table}")
print(f"Silver target table: {silver_table}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

bronze_df = spark.table(bronze_table)

print(f"Bronze row count: {bronze_df.count():,}")

bronze_df.printSchema()
display(bronze_df.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

minute_window = (
    Window
    .partitionBy(
        "source_provider",
        "source_file_name",
        "trade_date",
        "time_hhmm"
    )
    .orderBy("event_sequence_in_file")
)

silver_df = (
    bronze_df
    .withColumn(
        "event_minute_ts",
        F.to_timestamp(
            F.concat_ws(
                " ",
                F.col("trade_date").cast("string"),
                F.concat(
                    F.substring("time_hhmm", 1, 2),
                    F.lit(":"),
                    F.substring("time_hhmm", 3, 2),
                    F.lit(":00")
                )
            )
        )
    )
    .withColumn(
        "event_sequence_in_minute",
        F.row_number().over(minute_window)
    )
    .withColumn(
        "is_valid_time",
        F.col("time_hhmm").rlike("^[0-2][0-9][0-5][0-9]") &
        (F.substring("time_hhmm", 1, 2).cast("int") <= 23)
    )
    .withColumn(
        "is_valid_price",
        F.col("price_decimal").isNotNull() & (F.col("price_decimal") > 0)
    )
    .withColumn(
        "is_duplicate_source_event",
        F.lit(False)
    )
    .withColumn(
        "silver_quality_status",
        F.when(
            F.col("is_valid_time") & F.col("is_valid_price"),
            F.lit("Valid")
        ).otherwise(F.lit("Invalid"))
    )
    .withColumn(
        "silver_loaded_at_utc",
        F.current_timestamp()
    )
    .select(
        "source_provider",
        "trade_date",
        "time_hhmm",
        "event_minute_ts",
        "price_decimal",
        "event_sequence_in_file",
        "event_sequence_in_minute",
        "source_file_row_number",
        "source_file_name",
        "source_file_path",
        "is_valid_time",
        "is_valid_price",
        "is_duplicate_source_event",
        "silver_quality_status",
        "bronze_loaded_at_utc",
        "silver_loaded_at_utc"
    )
)

display(silver_df.limit(20))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

(
    silver_df
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(silver_table)
)

print(f"Silver table written: {silver_table}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

silver_validated_df = spark.table(silver_table)

bronze_count = bronze_df.count()
silver_count = silver_validated_df.count()

print(f"Bronze row count: {bronze_count:,}")
print(f"Silver row count: {silver_count:,}")

if bronze_count != silver_count:
    raise ValueError("Bronze and Silver row counts do not match.")

display(
    silver_validated_df
    .groupBy("silver_quality_status")
    .count()
    .orderBy("silver_quality_status")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(
    silver_validated_df
    .select(
        "trade_date",
        "time_hhmm",
        "event_sequence_in_file",
        "event_sequence_in_minute",
        "price_decimal",
        "source_file_name"
    )
    .orderBy(
        "trade_date",
        "source_file_name",
        "event_sequence_in_file"
    )
    .limit(50)
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(
    silver_validated_df
    .groupBy("trade_date", "time_hhmm")
    .agg(
        F.count("*").alias("events_in_minute"),
        F.min("event_sequence_in_minute").alias("min_sequence_in_minute"),
        F.max("event_sequence_in_minute").alias("max_sequence_in_minute")
    )
    .orderBy("trade_date", "time_hhmm")
    .limit(20)
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
