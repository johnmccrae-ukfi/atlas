from pathlib import Path

import pandas as pd


SOURCE_PATH = Path(r"F:\ukfi\Source\CQG\F.US.EU6M12_201203.ts")

COLUMN_NAMES = [
    "instrument",
    "date",
    "unknown",
    "time",
    "price",
    "event_type",
    "flag1",
    "flag2",
    "size",
]

ROWS_PER_SAMPLE = 1000


def count_lines(path: Path) -> int:
    with path.open("rb") as file:
        return sum(1 for _ in file)


def read_sample(path: Path, start_row: int, sample_name: str) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        header=None,
        names=COLUMN_NAMES,
        skiprows=start_row,
        nrows=ROWS_PER_SAMPLE,
    )

    df["sample_name"] = sample_name
    df["source_row_start"] = start_row

    return df


total_rows = count_lines(SOURCE_PATH)

sample_points = {
    "beginning": 0,
    "25_percent": int(total_rows * 0.25),
    "50_percent": int(total_rows * 0.50),
    "75_percent": int(total_rows * 0.75),
    "end": max(total_rows - ROWS_PER_SAMPLE, 0),
}

samples = [
    read_sample(SOURCE_PATH, start_row, sample_name)
    for sample_name, start_row in sample_points.items()
]

df = pd.concat(samples, ignore_index=True)

print("File:")
print(SOURCE_PATH)

print("\nTotal estimated rows:")
print(total_rows)

print("\nCombined sample shape:")
print(df.shape)

print("\nSample points:")
for sample_name, start_row in sample_points.items():
    print(f"{sample_name}: starts at row {start_row:,}")

print("\nData types:")
print(df.dtypes)

print("\nFirst 10 sampled rows:")
print(df.head(10))

print("\nRows per sample:")
print(df["sample_name"].value_counts())

print("\nUnique instruments:")
print(df["instrument"].value_counts(dropna=False))

print("\nUnique unknown values:")
print(df["unknown"].value_counts(dropna=False))

print("\nUnique event_type values:")
print(df["event_type"].value_counts(dropna=False))

print("\nUnique flag1 values:")
print(df["flag1"].value_counts(dropna=False))

print("\nUnique flag2 values:")
print(df["flag2"].value_counts(dropna=False))

print("\nDate range:")
print(df["date"].min(), "to", df["date"].max())

print("\nTime range:")
print(df["time"].min(), "to", df["time"].max())

print("\nPrice summary:")
print(df["price"].describe())

print("\nSize summary:")
print(df["size"].describe())

print("\nDistinct values by sample:")

for sample_name, sample_df in df.groupby("sample_name"):
    print(f"\n--- {sample_name} ---")
    print("date:", sample_df["date"].min(), "to", sample_df["date"].max())
    print("time:", sample_df["time"].min(), "to", sample_df["time"].max())
    print("event_type:", sample_df["event_type"].value_counts(dropna=False).to_dict())
    print("flag1:", sample_df["flag1"].value_counts(dropna=False).to_dict())
    print("flag2:", sample_df["flag2"].value_counts(dropna=False).to_dict())
    print("unknown:", sample_df["unknown"].value_counts(dropna=False).to_dict())