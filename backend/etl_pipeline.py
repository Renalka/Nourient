import os
import requests
import json
from google.cloud import bigquery
from google.oauth2 import service_account

# Ensure credentials are correct
cred_path = "backend/nourient-a686036afec5.json"
if not os.path.exists(cred_path):
    print(f"Error: {cred_path} not found.")
    exit(1)

creds = service_account.Credentials.from_service_account_file(cred_path)
client = bigquery.Client(credentials=creds, project="nourient")

DATASET_ID = "nourient.food_intelligence"

def load_enumbers():
    print("--- Starting E-Numbers ETL ---")
    # Using the official, secure Open Food Facts taxonomy
    url = "https://static.openfoodfacts.org/data/taxonomies/additives.json"
    print(f"Fetching official Additives database from {url}...")
    
    headers = {'User-Agent': 'Nourient-ETL/1.0 (subtrixx@proton.me)'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    raw_data = response.json()
    
    table_id = f"{DATASET_ID}.ingredient_dictionary_real"
    
    rows_to_insert = []
    # Open Food Facts additives.json is a dictionary of additive IDs to their properties
    for additive_id, data in raw_data.items():
        # E.g. additive_id = "en:e100"
        name = data.get("name", {}).get("en", additive_id)
        
        # OFF provides vegan/vegetarian status which we can map to a mock risk tier for now
        tier = "🟢 Low Risk"
        if data.get("vegan", {}).get("en", "") == "no":
            tier = "🔴 High Risk (Not Vegan)"
            
        rows_to_insert.append({
            "name": name,
            "purpose": "Food Additive",
            "confidence_tier": tier,
            "explanation": f"Sourced from official Open Food Facts Taxonomy. Wikidata: {data.get('wikidata', {}).get('en', 'N/A')}."
        })
        
        # BigQuery json insert limit chunking would go here for massive lists, but additives is small

        
    schema = [
        bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("purpose", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("confidence_tier", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("explanation", "STRING", mode="REQUIRED"),
    ]
    
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )
    
    print(f"Loading {len(rows_to_insert)} additives into BigQuery {table_id}...")
    job = client.load_table_from_json(rows_to_insert, table_id, job_config=job_config)
    job.result()
    print("✅ E-Numbers ETL Complete!\n")

def load_open_food_facts():
    print("--- Starting Open Food Facts Parquet ETL ---")
    parquet_url = "https://huggingface.co/datasets/openfoodfacts/product-database/resolve/main/food.parquet?download=true"
    local_file = "off_food_database.parquet"
    
    print(f"Downloading massive Parquet database (this may take a while)...")
    # Stream download to avoid running out of RAM
    with requests.get(parquet_url, stream=True) as r:
        r.raise_for_status()
        with open(local_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                
    print(f"Download complete. File size: {os.path.getsize(local_file) / (1024*1024):.2f} MB")
    
    table_id = f"{DATASET_ID}.canonical_products_real"
    
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        # Auto-detect schema from Parquet file
        autodetect=True,
    )
    
    print(f"Streaming Parquet file into BigQuery {table_id}...")
    with open(local_file, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)
        
    job.result()
    
    # Clean up the massive local file
    os.remove(local_file)
    
    table = client.get_table(table_id)
    print(f"✅ Open Food Facts ETL Complete! Loaded {table.num_rows} real products into BigQuery.\n")

if __name__ == "__main__":
    print("Starting Automated Production ETL Pipeline...\n")
    try:
        load_enumbers()
        print("Note: The Open Food Facts Parquet download is ~1.2GB and ingestion may take 10-15 minutes.")
        # load_open_food_facts() # Uncomment when ready to run the massive download
        print("Pipeline execution finished successfully.")
    except Exception as e:
        print(f"ETL Pipeline Failed: {e}")
