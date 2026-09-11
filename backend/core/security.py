from firebase_admin import auth
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from core.gcp import initialize_firebase_admin

# Uses the Cloud Run service identity in production rather than a JSON key.
initialize_firebase_admin()

security = HTTPBearer(auto_error=False)

async def verify_token_strict(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)) -> dict:
    """
    STRICT: Requires a valid Firebase JWT token. Throws 401 if missing or invalid.
    Use this for Basket, Profile, and other protected endpoints.
    """
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Authentication credentials were not provided.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
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

async def verify_token_optional(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)) -> dict:
    """
    OPTIONAL: Validates the token if provided, otherwise returns 'anonymous'.
    Use this for the Scanner API where guests are allowed.
    """
    if not credentials:
        return {"uid": "anonymous"}
        
    token = credentials.credentials
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user_id(decoded_token: dict = Security(verify_token_strict)) -> str:
    """
    STRICT: Extracts the verified user ID. Throws 401 if not authenticated.
    """
    uid = decoded_token.get('uid')
    if not uid or uid == 'anonymous':
        raise HTTPException(status_code=401, detail="Valid user session required.")
    return uid

def get_optional_user_id(decoded_token: dict = Security(verify_token_optional)) -> str:
    """
    OPTIONAL: Extracts the user ID from the verified token, or returns 'anonymous'.
    """
    return decoded_token.get('uid', 'anonymous')
