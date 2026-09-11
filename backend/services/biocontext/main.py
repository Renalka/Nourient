import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from fastapi import FastAPI
from services.biocontext.api import routes
from core.cors import configure_cors

app = FastAPI(title="Nourient BioContext API")

configure_cors(app)

app.include_router(routes.router)
