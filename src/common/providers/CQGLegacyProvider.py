from pathlib import Path
from datetime import datetime, timezone

import pandas as pd


class CQGLegacyProvider:
    def __init__(self, source_path: str, chunk_size: int = 1_000_000):
        self.source_path = Path(source_path)
        self.chunk_size = chunk_size

        self.columns = [
            "instrument",
            "trade_date_raw",
            "unknown_raw",
            "time_raw",
            "price_raw",
            "event_type",
            "flag1",
            "flag2",
            "size",
        ]

    def read_chunks(self):
        if not self.source_path.exists():
            raise FileNotFoundError(f"CQG source file not found: {self.source_path}")

        source_row_offset = 0

        for chunk in pd.read_csv(
            self.source_path,
            header=None,
            names=self.columns,
            chunksize=self.chunk_size,
            on_bad_lines="skip",
        ):
            row_count = len(chunk)

            chunk.insert(0, "source_file", self.source_path.name)
            chunk.insert(
                1,
                "source_row_number",
                range(source_row_offset + 1, source_row_offset + row_count + 1),
            )

            chunk["trade_date"] = pd.to_datetime(
                chunk["trade_date_raw"].astype(str),
                format="%Y%m%d",
                errors="coerce",
            ).dt.date

            chunk["time_hhmm"] = chunk["time_raw"].astype(str).str.zfill(4)

            chunk["price_decimal"] = chunk["price_raw"] / 10000

            chunk["loaded_at_utc"] = datetime.now(timezone.utc)

            source_row_offset += row_count

            yield chunk