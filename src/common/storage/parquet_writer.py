from pathlib import Path

import pandas as pd


def write_dataframe_to_parquet(
    dataframe: pd.DataFrame,
    output_path: str,
) -> None:
    """
    Write a pandas DataFrame to a Parquet file.

    Creates the destination directory if it does not already exist.
    """

    path = Path(output_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    dataframe.to_parquet(path, index=False)