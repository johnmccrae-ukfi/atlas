from pathlib import Path

import pandas as pd


BRONZE_FOLDER = Path(
    r"F:\ukfi\Development\Atlas\atlas\data\bronze\cqg"
)


def main():

    parquet_files = sorted(BRONZE_FOLDER.glob("*.parquet"))

    if not parquet_files:
        print("No Parquet files found.")
        return

    print("=" * 70)
    print("CQG Bronze Validation")
    print("=" * 70)
    print()

    total_rows = 0

    for file in parquet_files:

        df = pd.read_parquet(file)

        row_count = len(df)
        total_rows += row_count

        print(f"{file.name:<55} {row_count:>10,} rows")

    print()
    print("-" * 70)
    print(f"Files processed : {len(parquet_files):>5}")
    print(f"Total rows      : {total_rows:>15,}")
    print()

    expected_rows = 17_317_408

    if total_rows == expected_rows:
        print("✅ Validation PASSED")
    else:
        print("❌ Validation FAILED")
        print(f"Expected: {expected_rows:,}")
        print(f"Actual  : {total_rows:,}")


if __name__ == "__main__":
    main()