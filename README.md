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