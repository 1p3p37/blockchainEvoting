from fastapi import FastAPI

# from app.api.debug.endpoints import callback
from app.core.config import settings

app_debug = FastAPI(title=settings.project_name)
