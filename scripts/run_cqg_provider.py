from src.common.providers.CQGLegacyProvider import CQGLegacyProvider
from src.common.writers.BronzeWriter import BronzeWriter


def main():
    provider = CQGLegacyProvider(
        source_path=r"F:\ukfi\Source\CQG\F.US.EU6M12_201203.ts",
        chunk_size=1_000_000,
    )

    writer = BronzeWriter(
        output_root=r"F:\ukfi\Development\Atlas\atlas\data\bronze",
        dataset_name="cqg",
    )

    for chunk_no, chunk in enumerate(provider.read_chunks(), start=1):
        print(f"Chunk {chunk_no}: {len(chunk):,} rows")

        print(chunk[[
            "source_row_number",
            "instrument",
            "trade_date_raw",
            "time_raw",
            "event_type",
            "price_raw",
            "size",
            "price_decimal",
        ]].head(10))

        print()
        print(chunk["event_type"].value_counts())

        output_path = writer.write_chunk(chunk, chunk_no)

        print()
        print("Wrote Parquet file:")
        print(output_path)

        break


if __name__ == "__main__":
    main()