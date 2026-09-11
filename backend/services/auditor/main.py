import sys
import os

# Add the parent directory to sys.path so 'core' can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from fastapi import FastAPI
from services.auditor.api import routes
from core.cors import configure_cors

app = FastAPI(title="Nourient TrueLabel Auditor API")

configure_cors(app)

app.include_router(routes.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "TrueLabel Auditor"}
