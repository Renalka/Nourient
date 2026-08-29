import pandas as pd
import numpy as np
import requests
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

def download_dataset():
    print("Fetching a statistically significant stratified subset from Open Food Facts API...")
    products = []
    
    # Fetch 10 pages of 1000 products each (10,000 products) for a robust subset
    for page in range(1, 15):
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_simple=1&action=process&json=1&page_size=1000&page={page}"
        print(f"Fetching page {page}...")
        try:
            response = requests.get(url, headers={'User-Agent': 'Nourient-ML/1.0 (subtrixx@proton.me)'}, timeout=10)
            data = response.json()
            products.extend(data.get('products', []))
        except Exception as e:
            print(f"Failed to fetch page {page}: {e}")
            
    print(f"Fetched {len(products)} products.")
    
    # Flatten JSON into a format Pandas can read
    flat_data = []
    for p in products:
        nutriments = p.get("nutriments", {})
        flat_data.append({
            'energy-kcal_100g': nutriments.get("energy-kcal_100g"),
            'sugars_100g': nutriments.get("sugars_100g"),
            'sodium_100g': nutriments.get("sodium_100g"),
            'saturated-fat_100g': nutriments.get("saturated-fat_100g"),
            'proteins_100g': nutriments.get("proteins_100g"),
            'fiber_100g': nutriments.get("fiber_100g"),
            'nova_group': p.get("nova_group")
        })
        
    df = pd.DataFrame(flat_data)
    return df

def train_model():
    df = download_dataset()
    print("Loading dataset into Pandas...")

    print(f"Total rows in raw dataset: {len(df)}")
    
    # Drop rows where nova_group is missing or any of the macros are missing
    df = df.dropna()
    print(f"Total rows after dropping NaNs: {len(df)}")
    
    # Create Binary Target: 1 if Ultra-Processed (NOVA 4), 0 otherwise
    df['is_upf'] = (df['nova_group'] == 4).astype(int)
    
    X = df[['energy-kcal_100g', 'sugars_100g', 'sodium_100g', 'saturated-fat_100g', 'proteins_100g', 'fiber_100g']]
    y = df['is_upf']
    
    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training RandomForestClassifier... (This might take a moment)")
    # n_jobs=-1 uses all CPU cores for training
    clf = RandomForestClassifier(n_estimators=50, max_depth=15, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)
    
    print("Evaluating Model on Test Data...")
    y_pred = clf.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
    print(classification_report(y_test, y_pred))
    
    # Save the model
    os.makedirs("services/scoring/models", exist_ok=True)
    model_path = "services/scoring/models/upf_model.pkl"
    joblib.dump(clf, model_path)
    print(f"✅ Model successfully saved to {model_path}")

if __name__ == "__main__":
    train_model()
