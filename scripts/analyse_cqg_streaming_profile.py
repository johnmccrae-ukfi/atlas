# analyse_cqg_streaming_profile.py

import pandas as pd
from pathlib import Path
from collections import Counter, defaultdict

FILE_PATH = Path(r"F:\ukfi\Source\CQG\F.US.EU6M12_201203.ts")
CHUNK_SIZE = 1_000_000

columns = [
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

row_count = 0
bad_rows = 0

date_counter = Counter()
event_counter = Counter()
unknown_counter = Counter()
flag1_counter = Counter()
flag2_counter = Counter()

date_time_minmax = {}
price_minmax_by_event = defaultdict(lambda: [None, None])
size_minmax_by_event = defaultdict(lambda: [None, None])

prev_date = None
prev_time = None
ordering_issues = 0

print(f"Profiling: {FILE_PATH}")

for chunk_no, chunk in enumerate(
    pd.read_csv(
        FILE_PATH,
        header=None,
        names=columns,
        chunksize=CHUNK_SIZE,
        on_bad_lines="skip",
    ),
    start=1,
):
    expected_start_row = row_count
    row_count += len(chunk)

    date_counter.update(chunk["date"])
    event_counter.update(chunk["event_type"])
    unknown_counter.update(chunk["unknown"])
    flag1_counter.update(chunk["flag1"])
    flag2_counter.update(chunk["flag2"])

    for date_value, group in chunk.groupby("date"):
        min_time = group["time"].min()
        max_time = group["time"].max()

        if date_value not in date_time_minmax:
            date_time_minmax[date_value] = [min_time, max_time]
        else:
            date_time_minmax[date_value][0] = min(date_time_minmax[date_value][0], min_time)
            date_time_minmax[date_value][1] = max(date_time_minmax[date_value][1], max_time)

    for event_type, group in chunk.groupby("event_type"):
        price_min = group["price"].min()
        price_max = group["price"].max()
        size_min = group["size"].min()
        size_max = group["size"].max()

        current_price = price_minmax_by_event[event_type]
        current_size = size_minmax_by_event[event_type]

        current_price[0] = price_min if current_price[0] is None else min(current_price[0], price_min)
        current_price[1] = price_max if current_price[1] is None else max(current_price[1], price_max)

        current_size[0] = size_min if current_size[0] is None else min(current_size[0], size_min)
        current_size[1] = size_max if current_size[1] is None else max(current_size[1], size_max)

    # Check whether file order ever goes backwards by date/time.
    ordered_pairs = chunk[["date", "time"]].to_numpy()

    for date_value, time_value in ordered_pairs:
        if prev_date is not None:
            if (date_value, time_value) < (prev_date, prev_time):
                ordering_issues += 1

        prev_date = date_value
        prev_time = time_value

    print(f"Processed chunk {chunk_no:,} | rows so far: {row_count:,}")

print("\n==== CQG STREAMING PROFILE ====\n")

print(f"Total rows read: {row_count:,}")
print(f"Ordering issues by date/time: {ordering_issues:,}")

print("\nRows by date:")
for key in sorted(date_counter):
    print(f"{key}: {date_counter[key]:,}")

print("\nRows by event_type:")
for key, value in event_counter.items():
    print(f"{key}: {value:,}")

print("\nUnique unknown values:")
print(dict(unknown_counter))

print("\nUnique flag1 values:")
print(dict(flag1_counter))

print("\nUnique flag2 values:")
print(dict(flag2_counter))

print("\nMin/max time by date:")
for key in sorted(date_time_minmax):
    print(f"{key}: {date_time_minmax[key][0]} to {date_time_minmax[key][1]}")

print("\nPrice min/max by event_type:")
for key, value in price_minmax_by_event.items():
    print(f"{key}: {value[0]} to {value[1]}")

print("\nSize min/max by event_type:")
for key, value in size_minmax_by_event.items():
    print(f"{key}: {value[0]} to {value[1]}")