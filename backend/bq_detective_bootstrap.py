import os
from google.cloud import bigquery
from google.oauth2 import service_account

creds = service_account.Credentials.from_service_account_file('gcp-credentials.json')
client = bigquery.Client(credentials=creds, project=creds.project_id)
dataset_id = f"{client.project}.food_intelligence"
table_id = f"{dataset_id}.ingredient_dictionary"

schema = [
    bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("purpose", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("confidence_tier", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("explanation", "STRING", mode="REQUIRED"),
]

table = bigquery.Table(table_id, schema=schema)
try:
    table = client.create_table(table)
    print(f"Created table {table.table_id}")
except Exception as e:
    print(f"Table exists: {e}")

rows_to_insert = [
    {
        "name": "Maltodextrin",
        "purpose": "Thickener & Filler",
        "confidence_tier": "🔴 High Risk (Clinical Studies)",
        "explanation": "A highly processed carbohydrate with a higher glycemic index than table sugar. Spikes blood glucose."
    },
    {
        "name": "Anticaking Agent (E551)",
        "purpose": "Prevents Clumping",
        "confidence_tier": "🟡 Moderate Risk (Observational)",
        "explanation": "Also known as Silicon Dioxide. Used to keep powders from sticking together. Generally recognized as safe in small amounts, but it is a marker of ultra-processing."
    },
    {
        "name": "Invert Syrup",
        "purpose": "Sweetener",
        "confidence_tier": "🔴 High Risk (Clinical Studies)",
        "explanation": "A liquid sweetener made from table sugar. It is pure added sugar and contributes to metabolic disease."
    },
    {
        "name": "Emulsifiers (322, 471)",
        "purpose": "Texture Stabilizer",
        "confidence_tier": "🟡 Moderate Risk (Microbiome Impact)",
        "explanation": "Keeps oil and water mixed. Emerging evidence suggests synthetic emulsifiers may disrupt gut lining."
    }
]

errors = client.insert_rows_json(table_id, rows_to_insert)
if not errors:
    print("✅ Ingredient Dictionary loaded into BigQuery.")
else:
    print(f"❌ Errors: {errors}")
