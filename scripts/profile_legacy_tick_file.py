from pathlib import Path


file_path = Path(r"F:\ukfi\Source\CQG\F.US.EU6M12_201203.ts")

print(f"File: {file_path}")
print(f"Exists: {file_path.exists()}")
print(f"Size MB: {file_path.stat().st_size / 1024 / 1024:.2f}")

with file_path.open("rb") as file:
    sample = file.read(4096)

print()
print("First 200 raw bytes:")
print(sample[:200])

print()
print("Looks like text?")
try:
    text = sample.decode("utf-8")
    print("UTF-8: yes")
    print(text[:1000])
except UnicodeDecodeError:
    print("UTF-8: no")

print()
print("Trying latin-1 decode:")
text = sample.decode("latin-1", errors="replace")
print(text[:1000])