import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from fastapi import FastAPI
from services.orchestrator.api import routes
from core.cors import configure_cors

app = FastAPI(title="Nourient Backend Orchestrator")

configure_cors(app)

app.include_router(routes.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Orchestrator"}
