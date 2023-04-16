from fastapi import FastAPI

from app.api.endpoints import voting
from app.core.config import settings

app_v1 = FastAPI(title=settings.project_name)
# app = FastAPI(title="blockhainEvoting")

app_v1.include_router(
    voting.router,
    # prefix="/total_votes",
    # tags=["total_votes"],
)
