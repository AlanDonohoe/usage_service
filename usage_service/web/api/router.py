from fastapi.routing import APIRouter

from usage_service.web.api import monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router)
