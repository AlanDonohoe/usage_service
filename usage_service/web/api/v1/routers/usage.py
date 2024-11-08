from typing import List

from fastapi import APIRouter, status

from usage_service.models.usage import Usage
from usage_service.services.usage_service import UsageService
from usage_service.web.api.v1.models.responses.usage_response import (
    UsageListResponse,
    UsageResponse,
)

router = APIRouter(prefix="/v1")


@router.get("/usage", response_model=UsageListResponse, status_code=status.HTTP_200_OK)
async def read_usage() -> UsageListResponse:  # noqa: D103
    usages = await UsageService.call()

    return _usage_list_response(usages)


def _usage_list_response(usages: List[Usage]) -> UsageListResponse:
    usage_list = [UsageResponse(**usage.dict()) for usage in usages]

    return UsageListResponse(usage=usage_list)
