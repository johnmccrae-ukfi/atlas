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

    @property
    def file_prefix(self) -> str:
        stem = self.source_path.stem
        safe_stem = stem.replace(".", "_")
        return f"cqg_{safe_stem}"

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

            chunk.insert(0, "source_file_name", self.source_path.name)
            chunk.insert(1, "source_file_path", str(self.source_path))
            chunk.insert(
                2,
                "source_file_row_number",
                range(source_row_offset + 1, source_row_offset + row_count + 1),
            )

            chunk.insert(
                3,
                "event_sequence_in_file",
                range(source_row_offset + 1, source_row_offset + row_count + 1),
            )

            chunk.insert(4, "source_provider", "CQG_LEGACY")

            chunk["trade_date"] = pd.to_datetime(
                chunk["trade_date_raw"].astype(str),
                format="%Y%m%d",
                errors="coerce",
            ).dt.date

            chunk["time_hhmm"] = chunk["time_raw"].astype(str).str.zfill(4)

            chunk["price_decimal"] = chunk["price_raw"] / 10000

            chunk["bronze_loaded_at_utc"] = datetime.now(timezone.utc)

            source_row_offset += row_count

            yield chunk