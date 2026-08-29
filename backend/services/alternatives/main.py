from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.alternatives.api import routes

app = FastAPI(title="Better Alternatives Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "alternatives"}
