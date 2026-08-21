import sys
import os

# Add the parent directory to sys.path so 'core' can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.auditor.api import routes

app = FastAPI(title="Nourient TrueLabel Auditor API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "TrueLabel Auditor"}
