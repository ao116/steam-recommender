import gzip
import ast
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_PATH = PROJECT_ROOT / "data" / "raw" / "australian_users_items.json.gz"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

BATCH_SIZE = 100_000


def preprocess(input_path, output_dir, batch_size, max_users=None):
    rows = []
    batch_number = 0

    output_dir.mkdir(parents=True, exist_ok=True)
    if list(output_dir.glob("interactions_*.parquet")):
        raise FileExistsError(
            f"Output directory already contains interaction files: {output_dir}"
        )

    with gzip.open(input_path, "rt", encoding="utf-8") as f:
        for i,line in enumerate(f):
            if max_users is not None and i >= max_users:
                break
            user = ast.literal_eval(line)
            user_id = user["user_id"]
            items = user["items"]

            for item in items:
                play_time = item["playtime_forever"]

                interaction = {
                    "user_id": user_id,
                    "game_id": item["item_id"],
                    "play_time": play_time,
                    "positive_60m": play_time >= 60
                }

                rows.append(interaction)

                if len(rows) >= batch_size:
                    df_batch = pd.DataFrame(rows)

                    output_path = output_dir / f"interactions_{batch_number:03d}.parquet"
                    df_batch.to_parquet(output_path, index=False)

                    rows.clear()
                    batch_number += 1

        if len(rows) > 0:
            df_batch = pd.DataFrame(rows)

            output_path = output_dir / f"interactions_{batch_number:03d}.parquet"
            df_batch.to_parquet(output_path, index=False)

            batch_number += 1

    print(f"Total batches saved: {batch_number}")


if __name__ == "__main__":
    preprocess(INPUT_PATH, OUTPUT_DIR, BATCH_SIZE)