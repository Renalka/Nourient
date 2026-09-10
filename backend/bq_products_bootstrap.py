import os
from google.cloud import bigquery
from google.oauth2 import service_account

# Use the GCP project ID where BigQuery lives
PROJECT_ID = "nourient"
DATASET_ID = "food_intelligence"
TABLE_ID = "canonical_products"

cred = service_account.Credentials.from_service_account_file('backend/nourient-a686036afec5.json')
client = bigquery.Client(credentials=cred, project=PROJECT_ID)

def setup_products_table():
    dataset_ref = client.dataset(DATASET_ID)
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset {DATASET_ID} exists.")
    except Exception:
        print(f"Creating dataset {DATASET_ID}...")
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        client.create_dataset(dataset)

    table_ref = dataset_ref.table(TABLE_ID)
    schema = [
        bigquery.SchemaField("product_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("brand", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("category", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("price_inr", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("sugar_g", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("protein_g", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("sodium_mg", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("overall_score", "INTEGER", mode="REQUIRED")
    ]
    
    table = bigquery.Table(table_ref, schema=schema)
    
    try:
        client.delete_table(table_ref)
        print(f"Deleted old table {TABLE_ID}.")
    except Exception:
        pass
        
    table = client.create_table(table)
    print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")

    rows_to_insert = [
        # CEREALS
        {"product_id": "c_001", "name": "Sugar Bombs", "brand": "Kelloggs", "category": "Cereal", "price_inr": 350.0, "sugar_g": 35.0, "protein_g": 2.0, "sodium_mg": 400.0, "overall_score": 25},
        {"product_id": "c_002", "name": "Bran Flakes", "brand": "Kelloggs", "category": "Cereal", "price_inr": 290.0, "sugar_g": 12.0, "protein_g": 5.0, "sodium_mg": 200.0, "overall_score": 65},
        {"product_id": "c_003", "name": "Zero Sugar Oats", "brand": "Quaker", "category": "Cereal", "price_inr": 150.0, "sugar_g": 1.0, "protein_g": 10.0, "sodium_mg": 50.0, "overall_score": 90},
        
        # SNACKS
        {"product_id": "s_001", "name": "Spicy Chips", "brand": "Lays", "category": "Snack", "price_inr": 50.0, "sugar_g": 2.0, "protein_g": 1.0, "sodium_mg": 850.0, "overall_score": 20},
        {"product_id": "s_002", "name": "Baked Chips", "brand": "Lays", "category": "Snack", "price_inr": 65.0, "sugar_g": 1.0, "protein_g": 2.0, "sodium_mg": 400.0, "overall_score": 55},
        {"product_id": "s_003", "name": "Roasted Makhana", "brand": "Too Yumm", "category": "Snack", "price_inr": 90.0, "sugar_g": 0.5, "protein_g": 8.0, "sodium_mg": 150.0, "overall_score": 85},
        
        # BEVERAGES
        {"product_id": "b_001", "name": "Cola", "brand": "Coke", "category": "Beverage", "price_inr": 40.0, "sugar_g": 42.0, "protein_g": 0.0, "sodium_mg": 45.0, "overall_score": 10},
        {"product_id": "b_002", "name": "Diet Cola", "brand": "Coke", "category": "Beverage", "price_inr": 40.0, "sugar_g": 0.0, "protein_g": 0.0, "sodium_mg": 40.0, "overall_score": 40},
        {"product_id": "b_003", "name": "Coconut Water", "brand": "Raw Pressery", "category": "Beverage", "price_inr": 80.0, "sugar_g": 5.0, "protein_g": 1.0, "sodium_mg": 60.0, "overall_score": 95},
    ]

    errors = client.insert_rows_json(table, rows_to_insert)
    if errors == []:
        print(f"Inserted {len(rows_to_insert)} mock products into canonical_products.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))

if __name__ == "__main__":
    setup_products_table()
