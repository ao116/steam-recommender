from pathlib import Path
from src.preprocess import preprocess

project_root = Path(__file__).resolve().parent

input_path = project_root / "data/raw/australian_users_items.json.gz"
output_dir = project_root / "data/test_processed"

preprocess(
    input_path=input_path,
    output_dir=output_dir,
    batch_size=1000,
    max_users=5
)

import pyarrow.parquet as pq

parquet_files = sorted(output_dir.glob("interactions_*.parquet"))

total_rows = 0

for file in parquet_files:
    number_of_rows = pq.ParquetFile(file).metadata.num_rows
    total_rows += number_of_rows

print("Total files:", len(parquet_files))
print("Total interactions:", total_rows)

assert len(parquet_files) == 3
assert total_rows == 2171