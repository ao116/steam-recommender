# Steam Game Recommender

Recommending games to players based on their play history — a two-stage
recommender system (candidate generation + ranking) built on Steam data.

## Business problem

A gaming platform wants to show each player 10 games they are likely to play.
The simplest approach is to show everyone the most popular games.
**How much better can we do with personalized recommendations?**

## Data

[Steam datasets](https://cseweb.ucsd.edu/~jmcauley/datasets.html) from
Julian McAuley's lab at UC San Diego:
- **Australian users' items** — which games each user owns and how long they played them
- **Steam games metadata** — title, genre, price and other details for each game

Data is not included in this repo. Download the files and place them in `data/raw/`.

## Approach (planned)

1. **Exploration** — data loaded into BigQuery and explored with SQL
2. **Evaluation setup** — train/test split and ranking metrics (Recall@10, NDCG@10)
3. **Baseline** — most-popular games
4. **Collaborative filtering** — matrix factorization (ALS) on implicit feedback
5. **Ranking** — LightGBM learning-to-rank model re-ranking ALS candidates

## Results

*Coming soon.*

## Tech stack

Python · pandas · BigQuery · SQL · implicit (ALS) · LightGBM

## Project structure

    data/        raw and processed data (not tracked)
    notebooks/   exploration and experiments
    sql/         SQL queries
    src/         reusable Python code

## Setup

    python -m venv .venv
    source .venv/bin/activate      # Windows: .venv\Scripts\activate
    pip install -r requirements.txt

## Cloud Data Ingestion — Google BigQuery

The processed Steam interaction data is uploaded to Google BigQuery using a reusable Python pipeline.

### Pipeline Features

- Batch ingestion of **5,153,209 user-game interactions** from 52 Parquet files.
- Staging table architecture to separate data ingestion from downstream analysis.
- Missing-file detection before starting the upload.
- Sequential batch loading using `WRITE_TRUNCATE` and `WRITE_APPEND`.
- Row count validation to detect missing or duplicated data.
- Automatic retry mechanism with a maximum of three attempts and a five-second delay.
- Modular functions and centralized configuration.

### Run the Pipeline

```bash
python -m src.upload_bigquery
```

### Data Architecture

```text
Raw Steam Dataset
        |
Data Preprocessing
        |
52 Parquet Files
        |
BigQuery Staging Table
        |
Data Validation
        |
Final BigQuery Table
        |
Data Analysis & Recommendation Models
```

### Design Decisions and Limitations

- BigQuery Sandbox is used without enabling billing.
- Failed uploads restart from the first batch to simplify recovery.
- The retry mechanism does not distinguish between temporary and permanent errors.
- Uncertain load-job states are not reconciled before retrying.
- Promotion from the staging table to the final table is performed manually after successful validation.

### Technologies

Python, Pandas, PyArrow, Parquet, Google BigQuery, Google Cloud SDK, SQL.