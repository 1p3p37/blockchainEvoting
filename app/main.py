import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api import app_v1
from app.api.debug.api import app_debug
from app.core.config import settings

# from app.services.callback import CallbackStream

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    # title=settings.project_name,
    # docs_url=f"{settings.api_string}/docs",
)
app.mount(settings.api_string, app_v1)

# Set all CORS enabled origins
# if settings.backend_cors_origins:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.backend_cors_origins],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )
