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

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.read.parquet(
    "Files/bronze/cqg"
)

print(f"Rows: {df.count():,}")

display(df.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(
    df.select(
        "instrument",
        "trade_date",
        "time_hhmm",
        "event_type",
        "price_decimal",
        "size"
    ).limit(20)
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.write.mode("overwrite").format("delta").saveAsTable("bronze_cqg_legacy_ticks")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

bronze_df = spark.table("bronze_cqg_legacy_ticks")

print(f"Rows: {bronze_df.count():,}")

display(
    bronze_df.select(
        "source_file",
        "source_row_number",
        "instrument",
        "trade_date",
        "time_hhmm",
        "event_type",
        "price_decimal",
        "size"
    ).limit(20)
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.table("bronze_cqg_legacy_ticks")
df.count()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
