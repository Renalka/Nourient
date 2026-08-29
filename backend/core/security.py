import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Request, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import os

# Initialize Firebase Admin if not already initialized
if not firebase_admin._apps:
    # Use the proper Firebase Admin SDK service account key
    cred = credentials.Certificate('firebase-adminsdk.json')
    firebase_admin.initialize_app(cred, {
        'projectId': 'nourient-38381'
    })

security = HTTPBearer(auto_error=False)

async def verify_token(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)) -> dict:
    """
    FastAPI Dependency to verify the Firebase JWT token.
    If no token is provided, returns a dummy anonymous token.
    Throws 401 if a token IS provided but is invalid.
    """
    if not credentials:
        return {"uid": "anonymous"}
        
    token = credentials.credentials
    try:
        # Cryptographically verifies signature against Google's public keys
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user_id(decoded_token: dict = Security(verify_token)) -> str:
    """
    Extracts the user ID from the verified token, or 'anonymous'.
    """
    return decoded_token.get('uid', 'anonymous')
