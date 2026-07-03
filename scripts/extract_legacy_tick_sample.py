from pathlib import Path


source_path = Path(r"F:\ukfi\Source\CQG\F.US.EU6M12_201203.ts")
output_path = Path("research/datasets/legacy/samples/F.US.EU6M12_201203_sample.csv")

output_path.parent.mkdir(parents=True, exist_ok=True)

max_lines = 1000

with source_path.open("r", encoding="utf-8") as source_file:
    with output_path.open("w", encoding="utf-8", newline="") as output_file:
        output_file.write(
            "instrument,date,unknown,time,price,event_type,flag1,flag2,size\n"
        )

        for index, line in enumerate(source_file):
            if index >= max_lines:
                break

            output_file.write(line)

print(f"Wrote {max_lines} rows to {output_path}")