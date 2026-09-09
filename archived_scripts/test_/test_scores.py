import joblib
import random

m = joblib.load('backend/services/scoring/models/upf_model_v2.pkl')

for _ in range(100):
    calories = random.randint(0, 500)
    sugar = random.randint(0, 50)
    sodium = random.randint(0, 1000)
    sat_fat = random.randint(0, 20)
    protein = random.randint(0, 20)
    fiber = random.randint(0, 10)
    
    # FSA
    points_a = min(10, int((calories*4.184) / 335)) + min(10, int(sugar / 4.5)) + min(10, int(sat_fat / 1)) + min(10, int(sodium / 90))
    points_c = min(5, int(protein / 1.6)) + min(5, int(fiber / 0.9))
    fsa_score = points_a - points_c
    
    if fsa_score <= -1: quality_score = 95
    elif fsa_score <= 2: quality_score = 80
    elif fsa_score <= 10: quality_score = 65
    elif fsa_score <= 18: quality_score = 45
    else: quality_score = 20
    
    predicted_score = int(max(0, min(100, m.predict([[calories, sugar, sodium, sat_fat, protein, fiber, 10, 0, 0, 0, 0]])[0])))
    
    if quality_score == predicted_score:
        print(f"FOUND MATCH: {quality_score}")

