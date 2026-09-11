import os
import firebase_admin
from firebase_admin import credentials, firestore

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
cred_path = os.path.join(root_dir, "backend/nourient-38381-firebase-adminsdk-new.json")

cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

baskets = db.collection('user_baskets').stream()
for b in baskets:
    print(f"Basket {b.id}: {len(b.to_dict().get('items', []))} items")
