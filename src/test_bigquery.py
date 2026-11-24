from google.cloud import bigquery

PROJECT_ID = "steam-recommender-514518"

client = bigquery.Client(project=PROJECT_ID)

query = """
SELECT COUNT(*) AS total_interactions
FROM `steam-recommender-514518.steam_data.interactions_test`
"""

result = client.query(query).result()

for row in result:
    print("Total interactions:", row.total_interactions)


