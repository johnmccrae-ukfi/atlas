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
# ## Gold Instrument Dimension
# 
# **Notebook:** `nb_atlas_gold_dim_instrument`
# 
# **Purpose:**  
# Create the governed `gold_dim_instrument` Delta table for the first Atlas multi-instrument historical scope.
# 
# **Initial contracts:**
# 
# ```text
# MESU6
# MNQU6
# ```
# 
# **Output:**
# 
# ```text
# Tables/gold_dim_instrument
# ```
# 
# **Design reference:**
# 
# ```text
# docs/01_Architecture/Atlas_Multi_Instrument_Identity_and_Grain_Design.md
# ```
# 
# ---
# 
# ## Engineering Rules
# 
# - One row represents one governed dated Futures contract.
# - Atlas surrogate keys are explicitly allocated and must remain stable.
# - Provider tickers are source identifiers, not canonical relationship keys.
# - Keys must not be generated from row order or runtime-generated identifiers.
# - No automatic rollover or continuous-contract logic is included.
# - Unsupported metadata must not be invented.

# CELL ********************

# Atlas Market Data Platform
# Notebook: nb_atlas_gold_dim_instrument
# Purpose: Create the governed Gold instrument dimension

from datetime import datetime, timezone
from decimal import Decimal

from pyspark.sql import functions as F
from pyspark.sql.types import (
    BooleanType,
    DateType,
    DecimalType,
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

gold_instrument_table = "gold_dim_instrument"

instrument_schema = StructType(
    [
        StructField("AtlasContractKey", LongType(), False),
        StructField("AtlasContractBusinessKey", StringType(), False),
        StructField("AtlasProductKey", LongType(), False),
        StructField("AtlasProductBusinessKey", StringType(), False),
        StructField("AssetClass", StringType(), False),
        StructField("ProductCode", StringType(), False),
        StructField("ProductName", StringType(), False),
        StructField("ContractCode", StringType(), False),
        StructField("ContractMonthCode", StringType(), False),
        StructField("ContractMonthNumber", IntegerType(), False),
        StructField("ContractMonthName", StringType(), False),
        StructField("ContractYear", IntegerType(), False),
        StructField("ContractDisplayName", StringType(), False),
        StructField("TradingVenue", StringType(), False),
        StructField("TradeTickSize", DecimalType(18, 5), False),
        StructField("SettlementTickSize", DecimalType(18, 5), False),
        StructField("SpreadTickSize", DecimalType(18, 5), False),
        StructField("FirstTradeDate", DateType(), False),
        StructField("LastTradeDate", DateType(), False),
        StructField("SettlementDate", DateType(), False),
        StructField("IsActive", BooleanType(), False),
        StructField("SourceProvider", StringType(), False),
        StructField("ProviderTicker", StringType(), False),
        StructField("ProviderGroupCode", StringType(), False),
        StructField("ProviderContractType", StringType(), False),
        StructField("InstrumentSortOrder", IntegerType(), False),
        StructField("GoldLoadedUTC", TimestampType(), False),
    ]
)

gold_loaded_utc = datetime.now(timezone.utc).replace(tzinfo=None)

instrument_rows = [
    (
        2001,
        "FUT-XCME-MES-2026-09",
        1001,
        "FUT-XCME-MES",
        "Futures",
        "MES",
        "Micro E-mini S&P 500",
        "MES-2026-09",
        "U",
        9,
        "September",
        2026,
        "Micro E-mini S&P 500 Sep 2026",
        "XCME",
        Decimal("0.25000"),
        Decimal("0.25000"),
        Decimal("0.01000"),
        datetime.strptime("2025-06-20", "%Y-%m-%d").date(),
        datetime.strptime("2026-09-18", "%Y-%m-%d").date(),
        datetime.strptime("2026-09-18", "%Y-%m-%d").date(),
        True,
        "Massive",
        "MESU6",
        "MS",
        "single",
        1,
        gold_loaded_utc,
    ),
    (
        2002,
        "FUT-XCME-MNQ-2026-09",
        1002,
        "FUT-XCME-MNQ",
        "Futures",
        "MNQ",
        "Micro E-mini Nasdaq-100",
        "MNQ-2026-09",
        "U",
        9,
        "September",
        2026,
        "Micro E-mini Nasdaq-100 Sep 2026",
        "XCME",
        Decimal("0.25000"),
        Decimal("0.25000"),
        Decimal("0.01000"),
        datetime.strptime("2025-06-20", "%Y-%m-%d").date(),
        datetime.strptime("2026-09-18", "%Y-%m-%d").date(),
        datetime.strptime("2026-09-18", "%Y-%m-%d").date(),
        True,
        "Massive",
        "MNQU6",
        "NQ",
        "single",
        2,
        gold_loaded_utc,
    ),
]

gold_dim_instrument_df = spark.createDataFrame(
    instrument_rows,
    schema=instrument_schema,
)

print(f"Target table: {gold_instrument_table}")
print(f"Seed row count: {gold_dim_instrument_df.count():,}")

gold_dim_instrument_df.printSchema()
display(
    gold_dim_instrument_df.orderBy("InstrumentSortOrder")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Validate the proposed Gold instrument dimension before persistence

expected_row_count = 2

validation_checks = {
    "Expected row count": (
        gold_dim_instrument_df.count() == expected_row_count
    ),
    "AtlasContractKey is unique": (
        gold_dim_instrument_df
            .groupBy("AtlasContractKey")
            .count()
            .filter(F.col("count") > 1)
            .count() == 0
    ),
    "AtlasContractBusinessKey is unique": (
        gold_dim_instrument_df
            .groupBy("AtlasContractBusinessKey")
            .count()
            .filter(F.col("count") > 1)
            .count() == 0
    ),
    "Provider mapping is unique": (
        gold_dim_instrument_df
            .groupBy("SourceProvider", "ProviderTicker")
            .count()
            .filter(F.col("count") > 1)
            .count() == 0
    ),
    "InstrumentSortOrder is unique": (
        gold_dim_instrument_df
            .groupBy("InstrumentSortOrder")
            .count()
            .filter(F.col("count") > 1)
            .count() == 0
    ),
    "Required fields are non-null": (
        gold_dim_instrument_df
            .filter(
                F.col("AtlasContractKey").isNull()
                | F.col("AtlasContractBusinessKey").isNull()
                | F.col("AtlasProductKey").isNull()
                | F.col("AtlasProductBusinessKey").isNull()
                | F.col("SourceProvider").isNull()
                | F.col("ProviderTicker").isNull()
            )
            .count() == 0
    ),
    "Tick sizes are positive": (
        gold_dim_instrument_df
            .filter(
                (F.col("TradeTickSize") <= 0)
                | (F.col("SettlementTickSize") <= 0)
                | (F.col("SpreadTickSize") <= 0)
            )
            .count() == 0
    ),
    "FirstTradeDate is valid": (
        gold_dim_instrument_df
            .filter(F.col("FirstTradeDate") > F.col("LastTradeDate"))
            .count() == 0
    ),
    "LastTradeDate equals SettlementDate": (
        gold_dim_instrument_df
            .filter(F.col("LastTradeDate") != F.col("SettlementDate"))
            .count() == 0
    ),
    "Contract month mapping is correct": (
        gold_dim_instrument_df
            .filter(
                (F.col("ContractMonthCode") != "U")
                | (F.col("ContractMonthNumber") != 9)
                | (F.col("ContractMonthName") != "September")
                | (F.col("ContractYear") != 2026)
            )
            .count() == 0
    ),
    "MESU6 mapping is correct": (
        gold_dim_instrument_df
            .filter(
                (F.col("ProviderTicker") == "MESU6")
                & (F.col("AtlasContractKey") == 2001)
                & (F.col("AtlasProductKey") == 1001)
            )
            .count() == 1
    ),
    "MNQU6 mapping is correct": (
        gold_dim_instrument_df
            .filter(
                (F.col("ProviderTicker") == "MNQU6")
                & (F.col("AtlasContractKey") == 2002)
                & (F.col("AtlasProductKey") == 1002)
            )
            .count() == 1
    ),
}

validation_results = [
    (check_name, passed)
    for check_name, passed in validation_checks.items()
]

validation_results_df = spark.createDataFrame(
    validation_results,
    ["ValidationCheck", "ValidationPassed"],
)

display(
    validation_results_df.orderBy("ValidationCheck")
)

failed_checks = [
    check_name
    for check_name, passed in validation_checks.items()
    if not passed
]

if failed_checks:
    raise ValueError(
        "Gold instrument dimension validation failed: "
        + ", ".join(failed_checks)
    )

print(
    f"Gold instrument dimension validation passed: "
    f"{len(validation_checks)} checks completed successfully."
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Persist the governed Gold instrument dimension

(
    gold_dim_instrument_df
        .write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(gold_instrument_table)
)

print(f"Gold instrument dimension written: {gold_instrument_table}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Validate the persisted Gold instrument dimension

gold_dim_instrument_saved_df = spark.table(gold_instrument_table)

persisted_row_count = gold_dim_instrument_saved_df.count()

print(f"Persisted row count: {persisted_row_count:,}")

if persisted_row_count != 2:
    raise ValueError(
        f"Expected 2 persisted instrument rows, found {persisted_row_count}."
    )

persisted_duplicate_contract_keys = (
    gold_dim_instrument_saved_df
        .groupBy("AtlasContractKey")
        .count()
        .filter(F.col("count") > 1)
        .count()
)

if persisted_duplicate_contract_keys > 0:
    raise ValueError(
        "Persisted gold_dim_instrument contains duplicate AtlasContractKey values."
    )

persisted_duplicate_provider_mappings = (
    gold_dim_instrument_saved_df
        .groupBy("SourceProvider", "ProviderTicker")
        .count()
        .filter(F.col("count") > 1)
        .count()
)

if persisted_duplicate_provider_mappings > 0:
    raise ValueError(
        "Persisted gold_dim_instrument contains duplicate provider mappings."
    )

gold_dim_instrument_saved_df.printSchema()

display(
    gold_dim_instrument_saved_df
        .orderBy("InstrumentSortOrder")
)

print("Persisted Gold instrument dimension validation passed.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Validate persisted Gold instrument dimension against governed rules

persisted_validation_checks = {
    "Expected persisted row count": (
        gold_dim_instrument_saved_df.count() == 2
    ),
    "Persisted AtlasContractKey is unique": (
        gold_dim_instrument_saved_df
            .groupBy("AtlasContractKey")
            .count()
            .filter(F.col("count") > 1)
            .count() == 0
    ),
    "Persisted AtlasContractBusinessKey is unique": (
        gold_dim_instrument_saved_df
            .groupBy("AtlasContractBusinessKey")
            .count()
            .filter(F.col("count") > 1)
            .count() == 0
    ),
    "Persisted provider mapping is unique": (
        gold_dim_instrument_saved_df
            .groupBy("SourceProvider", "ProviderTicker")
            .count()
            .filter(F.col("count") > 1)
            .count() == 0
    ),
    "Persisted required fields are non-null": (
        gold_dim_instrument_saved_df
            .filter(
                F.col("AtlasContractKey").isNull()
                | F.col("AtlasContractBusinessKey").isNull()
                | F.col("AtlasProductKey").isNull()
                | F.col("AtlasProductBusinessKey").isNull()
                | F.col("SourceProvider").isNull()
                | F.col("ProviderTicker").isNull()
                | F.col("ContractDisplayName").isNull()
            )
            .count() == 0
    ),
    "Persisted tick sizes are positive": (
        gold_dim_instrument_saved_df
            .filter(
                (F.col("TradeTickSize") <= 0)
                | (F.col("SettlementTickSize") <= 0)
                | (F.col("SpreadTickSize") <= 0)
            )
            .count() == 0
    ),
    "Persisted contract dates are valid": (
        gold_dim_instrument_saved_df
            .filter(
                (F.col("FirstTradeDate") > F.col("LastTradeDate"))
                | (F.col("LastTradeDate") != F.col("SettlementDate"))
            )
            .count() == 0
    ),
    "Persisted MESU6 mapping is correct": (
        gold_dim_instrument_saved_df
            .filter(
                (F.col("ProviderTicker") == "MESU6")
                & (F.col("AtlasContractKey") == 2001)
                & (F.col("AtlasProductKey") == 1001)
            )
            .count() == 1
    ),
    "Persisted MNQU6 mapping is correct": (
        gold_dim_instrument_saved_df
            .filter(
                (F.col("ProviderTicker") == "MNQU6")
                & (F.col("AtlasContractKey") == 2002)
                & (F.col("AtlasProductKey") == 1002)
            )
            .count() == 1
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
        "Persisted gold_dim_instrument validation failed: "
        + ", ".join(failed_persisted_checks)
    )

print(
    "Persisted gold_dim_instrument validation passed: "
    f"{len(persisted_validation_checks)} checks completed successfully."
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
