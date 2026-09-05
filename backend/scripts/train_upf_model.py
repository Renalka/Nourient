import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def generate_synthetic_data(num_samples=25000):
    """
    Generates synthetic training data that maps the 11 nutritional and ingredient features
    to a comprehensive, continuous Processing & Health Score (0-100).
    """
    np.random.seed(42)
    
    data = []
    labels = []
    
    for _ in range(num_samples):
        # 1. Base Macros (Realistic Distributions)
        calories = np.random.exponential(scale=150) + np.random.uniform(0, 50)
        sugar = np.random.exponential(scale=10)
        sodium = np.random.exponential(scale=200)
        sat_fat = np.random.exponential(scale=5)
        protein = np.random.exponential(scale=8)
        fiber = np.random.exponential(scale=3)
        
        # 2. Ingredients (Realistic Distributions)
        natural = np.random.poisson(lam=4) + 1
        synthetic = np.random.poisson(lam=1)
        moderate_risk = np.random.poisson(lam=0.5)
        high_risk = np.random.poisson(lam=0.2)
        
        total_ingredients = natural + synthetic + moderate_risk + high_risk
        
        # 3. Calculate Comprehensive Ground Truth Score
        score = 100.0
        
        # Macro Penalties
        score -= (sugar * 0.8)          # Heavy sugar penalty
        score -= (sodium * 0.015)       # Sodium penalty
        score -= (sat_fat * 1.2)        # Saturated fat penalty
        score -= (calories * 0.02)      # Empty calorie penalty
        
        # Macro Rewards
        score += (protein * 0.5)
        score += (fiber * 1.5)
        
        # Ingredient Safety Penalties (Nuanced)
        # Instead of instantly dropping the score to 0 for a single additive,
        # we apply weighted deductions.
        score -= (synthetic * 8)        # -8 per synthetic
        score -= (moderate_risk * 15)   # -15 per moderate risk
        score -= (high_risk * 25)       # -25 per high risk
        
        # Penalty for extremely long, complex ingredient lists (hyper-processing)
        if total_ingredients > 15:
            score -= (total_ingredients - 15) * 1.5
            
        # Clamp score between 0 and 100
        target_score = max(0, min(100, score))
        
        feature_vector = [
            calories, sugar, sodium, sat_fat, protein, fiber,
            total_ingredients, synthetic, high_risk, moderate_risk, natural
        ]
        
        data.append(feature_vector)
        labels.append(target_score)
        
    return pd.DataFrame(data, columns=[
        'calories', 'sugar', 'sodium', 'sat_fat', 'protein', 'fiber',
        'total_ingredients', 'synthetic', 'high_risk', 'moderate_risk', 'natural'
    ]), np.array(labels)

def train_model():
    print("Generating nuanced synthetic ground truth data...")
    X, y = generate_synthetic_data(25000)
    
    print("Training RandomForestRegressor on 11-dimensional feature vector...")
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('rf', RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42))
    ])
    
    pipeline.fit(X, y)
    
    # R^2 Score
    r2 = pipeline.score(X, y)
    print(f"Training R^2 Score: {r2:.4f}")
    
    # Exporting
    model_dir = os.path.join(os.path.dirname(__file__), "..", "services", "scoring", "models")
    os.makedirs(model_dir, exist_ok=True)
    
    export_path = os.path.join(model_dir, "upf_model_v2.pkl")
    joblib.dump(pipeline, export_path)
    print(f"Model exported successfully to {export_path}")

if __name__ == "__main__":
    train_model()
