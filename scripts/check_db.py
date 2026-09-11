import os
import sys
import firebase_admin
from firebase_admin import credentials, firestore

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
cred_path = os.path.join(root_dir, "backend/nourient-38381-firebase-adminsdk-new.json")

cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

print("User Baskets:")
baskets = db.collection('user_baskets').limit(5).stream()
for b in baskets:
    print(f" - {b.id}: {len(b.to_dict().get('items', []))} items")

print("\nUser History:")
users = db.collection('users').limit(5).stream()
for u in users:
    history_doc = db.collection('users').document(u.id).collection('data').document('history').get()
    if history_doc.exists:
        print(f" - {u.id}: {len(history_doc.to_dict().get('scans', []))} scans")
    else:
        print(f" - {u.id}: no history document")
