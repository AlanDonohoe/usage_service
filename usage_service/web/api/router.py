# Main router that includes all other routers.

from fastapi.routing import APIRouter

from usage_service.web.api import monitoring
from usage_service.web.api.v1.routers import usage

api_router = APIRouter()

api_router.include_router(monitoring.router)
api_router.include_router(usage.router)
