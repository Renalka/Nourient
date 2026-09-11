import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from fastapi import FastAPI
from services.detective.api import routes
from core.cors import configure_cors

app = FastAPI(title="Nourient Ingredient Detective API")

configure_cors(app)

app.include_router(routes.router)
app.include_router(routes.dict_router)
