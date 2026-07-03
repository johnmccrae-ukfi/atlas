from src.common.providers.CQGLegacyProvider import CQGLegacyProvider
from src.common.writers.BronzeWriter import BronzeWriter


def main():
    max_chunks_to_process = None  # set to None to process the full file

    provider = CQGLegacyProvider(
        source_path=r"F:\ukfi\Source\CQG\F.US.EU6M12_201203.ts",
        chunk_size=1_000_000,
    )

    writer = BronzeWriter(
        output_root=r"F:\ukfi\Development\Atlas\atlas\data\bronze",
        dataset_name="cqg",
    )

    print("=" * 60)
    print("CQG Legacy Provider")
    print("=" * 60)
    print(f"Source file : {provider.source_path}")
    print(f"Chunk size  : {provider.chunk_size:,}")
    print(f"Chunk limit : {max_chunks_to_process}")
    print()

    for chunk_no, chunk in enumerate(provider.read_chunks(), start=1):
        
        print(f"Processing chunk {chunk_no:,} ({len(chunk):,} rows)")

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

        instrument = chunk["instrument"].iat[0].replace(".", "_")
        month = str(chunk["trade_date_raw"].iat[0])[:6]

        file_prefix = f"cqg_{instrument}_{month}"

        output_path = writer.write_chunk(
            chunk,
            chunk_no,
            file_prefix=provider.file_prefix,
        )

        print()
        print("Wrote Parquet file:")
        print(output_path)

        if max_chunks_to_process is not None and chunk_no >= max_chunks_to_process:
            break

if __name__ == "__main__":
    main()