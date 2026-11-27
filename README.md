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

### SQL Exploration and Data Cleaning

- Analyzed 5,153,209 interactions across 70,912 users and 10,978 games using BigQuery.
- Identified 58,647 duplicated user-game pairs and 59,127 extra rows.
- Checked for missing values, empty identifiers, negative playtime, and inconsistent labels.
- Selected maximum cumulative playtime as the deduplication strategy.
- Recalculated positive interaction labels using the 60-minute threshold.
- Preserved the original table and created a separate cleaned table.

## Recommendation-Specific Exploratory Data Analysis

The cleaned interaction dataset was analyzed to understand data sparsity, user activity, and game popularity before developing recommendation models.

### Key Findings

- The dataset contains 5.09 million interactions across 70,912 users and 10,978 games.
- Positive feedback is defined as at least 60 minutes of playtime.
- The positive interaction matrix is 99.70% sparse.
- User activity and game popularity distributions are highly right-skewed.
- The top 1%, 5%, and 10% of games account for 43.38%, 77.38%, and 88.30% of positive interactions, respectively.

### Modeling Decisions

- Use sparse data representations for recommendation models.
- Require at least five positive interactions per user for initial personalized evaluation. This retains 80.15% of users, accounting for 98.96% of positive interactions.
- Preserve the original cleaned dataset.
- Develop a popularity-based baseline before implementing collaborative filtering.

### Limitations and Future Improvements

- Investigate alternative playtime thresholds for defining positive feedback.
- Evaluate popularity bias and recommendation diversity.
- Investigate recommendation strategies for low-activity users and unpopular games.

## Train/Test Split Strategy

- Use positive interactions (playtime >= 60 minutes).
- Perform an 80/20 random split for each eligible user.
- Require at least 5 positive interactions for evaluation.
- Keep low-activity users' positive interactions for training only.
- Use a fixed random seed for reproducibility.
- Perform data splitting in BigQuery.

Since interaction timestamps are unavailable, temporal splitting
is not possible with the current dataset.

Implementation is planned for the next development session.