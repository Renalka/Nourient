import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate('backend/gcp-credentials.json')
print("Project ID from service account:", cred.project_id)
