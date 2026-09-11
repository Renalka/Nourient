from fastapi import FastAPI
from services.basket.api import routes
from core.cors import configure_cors

app = FastAPI(title="Basket Intelligence")

configure_cors(app)

app.include_router(routes.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "basket"}
