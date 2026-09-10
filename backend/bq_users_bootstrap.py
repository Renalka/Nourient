import os
from google.cloud import bigquery
from google.oauth2 import service_account

creds = service_account.Credentials.from_service_account_file('nourient-a686036afec5.json')
client = bigquery.Client(credentials=creds, project=creds.project_id)
dataset_id = f"{client.project}.food_intelligence"
table_id = f"{dataset_id}.users"

schema = [
    bigquery.SchemaField("user_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("health_profile", "STRING", mode="REQUIRED"), # GENERAL, DIABETIC, HYPERTENSION
]

table = bigquery.Table(table_id, schema=schema)
try:
    table = client.create_table(table)
    print(f"Created table {table.table_id}")
except Exception as e:
    print(f"Table exists: {e}")

rows_to_insert = [
    {
        "user_id": "usr_general_01",
        "name": "Arjun (General Health)",
        "health_profile": "GENERAL"
    },
    {
        "user_id": "usr_diabetic_02",
        "name": "Priya (Diabetic Profile)",
        "health_profile": "DIABETIC"
    },
    {
        "user_id": "usr_hyper_03",
        "name": "Rohan (Hypertension Profile)",
        "health_profile": "HYPERTENSION"
    }
]

errors = client.insert_rows_json(table_id, rows_to_insert)
if not errors:
    print("✅ Dummy Users loaded into BigQuery.")
else:
    print(f"❌ Errors: {errors}")
