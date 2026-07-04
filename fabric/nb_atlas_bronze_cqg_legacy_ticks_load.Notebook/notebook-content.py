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
# ## Bronze Layer
# 
# Notebook:
# nb_atlas_bronze_cqg_legacy_ticks_load
# 
# Purpose:
# Load CQG legacy tick data from OneLake Files (Parquet) into the managed Bronze Delta table.
# 
# Input:
# Files/bronze/cqg/*.parquet
# 
# Output:
# bronze_cqg_legacy_ticks (Delta)
# 
# Expected rows:
# 17,317,408

# CELL ********************

# Atlas Market Data Platform
# Notebook: nb_atlas_bronze_cqg_legacy_ticks_load
# Purpose: Load CQG legacy Bronze Parquet files from OneLake Files into a Bronze Delta table

from pyspark.sql import functions as F

# Source path in Lakehouse Files
source_path = "Files/bronze/cqg"

# Target Bronze Delta table
target_table = "bronze_cqg_legacy_ticks"

print(f"Source path: {source_path}")
print(f"Target table: {target_table}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Read all Bronze CQG Parquet files from OneLake Files

bronze_df = (
    spark.read
         .parquet(source_path)
)

print(f"Rows read: {bronze_df.count():,}")

display(bronze_df.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Inspect the schema

bronze_df.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Cell 2 - Read Bronze CQG Parquet files and validate row count

expected_row_count = 17_317_408

bronze_df = (
    spark.read
         .parquet(source_path)
)

actual_row_count = bronze_df.count()

print(f"Source path:        {source_path}")
print(f"Rows read:          {actual_row_count:,}")
print(f"Expected rows:      {expected_row_count:,}")

if actual_row_count != expected_row_count:
    raise ValueError(
        f"Row count mismatch. Expected {expected_row_count:,}, got {actual_row_count:,}"
    )

print("Bronze Parquet read validation passed.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Cell 3 - Inspect Bronze schema and sample rows

print("Bronze DataFrame schema:")
bronze_df.printSchema()

display(bronze_df.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Cell 4 - Write Bronze DataFrame to managed Delta table

(
    bronze_df.write
             .format("delta")
             .mode("overwrite")
             .option("overwriteSchema", "true")
             .saveAsTable(target_table)
)

print(f"Bronze Delta table written successfully: {target_table}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Cell 5 - Validate Bronze Delta table

bronze_delta_df = spark.table(target_table)

delta_row_count = bronze_delta_df.count()

print(f"Bronze Delta table : {target_table}")
print(f"Rows in Delta table: {delta_row_count:,}")

if delta_row_count != expected_row_count:
    raise ValueError(
        f"Delta validation failed. Expected {expected_row_count:,}, found {delta_row_count:,}"
    )

print("✅ Bronze Delta validation passed.")

display(bronze_delta_df.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Cell 6 - Bronze Load Summary

print("=" * 60)
print("ATLAS BRONZE LOAD SUMMARY")
print("=" * 60)

print(f"Source Path         : {source_path}")
print(f"Target Table        : {target_table}")
print(f"Rows Loaded         : {delta_row_count:,}")
print(f"Validation          : PASSED")
print(f"Storage Format      : Delta")
print("=" * 60)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
