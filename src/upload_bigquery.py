from pathlib import Path
from google.cloud import bigquery
import time

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PARQUET_DIR = PROJECT_ROOT / "data" / "processed"

PROJECT_ID = "steam-recommender-514518"
DATASET_ID = "steam_data"
STAGING_TABLE = "interactions_staging"

EXPECTED_ROWS = 5_153_209
MAX_ATTEMPTS = 3
RETRY_DELAY = 5


def upload_data(client, files, table_id, expected_rows):

    for i, file in enumerate(files):
        if i == 0:
            write_mode = bigquery.WriteDisposition.WRITE_TRUNCATE
        else:
            write_mode = bigquery.WriteDisposition.WRITE_APPEND

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.PARQUET,
            write_disposition=write_mode
        )

        with open(file, "rb") as f:
            load_job = client.load_table_from_file(
                f,
                table_id,
                job_config=job_config
            )

            load_job.result()

            print(f"{file.name} ({i+1}/{len(files)})")

    query = f"""
        SELECT COUNT(*) AS total_rows
        FROM `{table_id}`;
    """

    result = client.query(query).result()

    for row in result:
        actual_rows = row.total_rows

    if actual_rows == expected_rows:
        print("Validation successful")
    else:
        raise ValueError(
            f"Expected {expected_rows} rows, but received {actual_rows}"
        )


def main():

    parquet_files = sorted(
        PARQUET_DIR.glob("interactions_*.parquet")
    )

    if not parquet_files:
        raise FileNotFoundError("No Parquet files found")

    print(f"Found {len(parquet_files)} Parquet files")

    client = bigquery.Client(project=PROJECT_ID)

    table_id = f"{PROJECT_ID}.{DATASET_ID}.{STAGING_TABLE}"

    print(f"Target staging table: {table_id}")

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"number of current attempt:{attempt} ")

        try:
            upload_data(client, parquet_files, table_id, EXPECTED_ROWS)
            break
        except Exception as e:
            print(f"Upload failed: {e}")

            if attempt == MAX_ATTEMPTS:
                raise

            print(f"Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)


if __name__ == "__main__":
    main()