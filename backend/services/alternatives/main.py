from fastapi import FastAPI
from services.alternatives.api import routes
from core.cors import configure_cors

app = FastAPI(title="Better Alternatives Engine")

configure_cors(app)

app.include_router(routes.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "alternatives"}
