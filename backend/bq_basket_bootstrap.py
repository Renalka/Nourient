import os
from google.cloud import bigquery
from google.oauth2 import service_account

creds = service_account.Credentials.from_service_account_file('backend/gcp-credentials.json')
client = bigquery.Client(credentials=creds, project=creds.project_id)
dataset_id = f"{client.project}.food_intelligence"
table_id = f"{dataset_id}.user_baskets"

schema = [
    bigquery.SchemaField("user_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("added_at", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("product_data", "JSON", mode="REQUIRED"),
]

table = bigquery.Table(table_id, schema=schema)
try:
    table = client.create_table(table)
    print(f"✅ Created production Basket table: {table.table_id}")
except Exception as e:
    print(f"Table might exist or error: {e}")
