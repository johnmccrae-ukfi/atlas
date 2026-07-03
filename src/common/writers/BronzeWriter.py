from pathlib import Path

import pandas as pd


class BronzeWriter:
    def __init__(self, output_root: str, dataset_name: str):
        self.output_root = Path(output_root)
        self.dataset_name = dataset_name
        self.output_dir = self.output_root / dataset_name
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write_chunk(
        self,
        chunk: pd.DataFrame,
        chunk_no: int,
        file_prefix: str | None = None,
    ) -> Path:
        prefix = file_prefix or f"{self.dataset_name}_bronze"

        output_path = self.output_dir / f"{prefix}_chunk_{chunk_no:04d}.parquet"

        chunk.to_parquet(output_path, index=False)

        return output_path