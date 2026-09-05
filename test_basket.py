import firebase_admin
from firebase_admin import credentials, auth
import requests

cred = credentials.Certificate('backend/firebase-adminsdk.json')
app = firebase_admin.initialize_app(cred)

# Create a custom token
custom_token = auth.create_custom_token("test-user-id").decode('utf-8')

import os
API_KEY = os.environ.get('NEXT_PUBLIC_FIREBASE_API_KEY')
with open('frontend/.env.local') as f:
    for line in f:
        if 'NEXT_PUBLIC_FIREBASE_API_KEY' in line:
            API_KEY = line.split('=')[1].strip().strip('"')

# Exchange custom token for ID token
res = requests.post(f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={API_KEY}", json={"token": custom_token, "returnSecureToken": True})
id_token = res.json()['idToken']

print("Got ID token")
basket_res = requests.get("http://localhost:8007/api/v1/basket/analyze", headers={"Authorization": f"Bearer {id_token}"})
print(basket_res.status_code, basket_res.text)
