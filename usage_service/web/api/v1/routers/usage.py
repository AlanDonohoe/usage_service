from fastapi import APIRouter, status

from usage_service.models.usage import Usage
from usage_service.services.usage import UsageService
from usage_service.web.api.v1.models.responses.message_response import MessageResponse
from usage_service.web.api.v1.models.responses.usage_response import UsageResponse

router = APIRouter(prefix="/v1")


@router.get("/usage", response_model=UsageResponse, status_code=status.HTTP_200_OK)
async def read_usage() -> UsageResponse:  # noqa: D103
    usage = await UsageService.call()

    return _convert_to_usage_web(usage)


def _convert_to_usage_web(usage: Usage) -> UsageResponse:
    messages_web = [MessageResponse(**message.dict()) for message in usage.messages]

    return UsageResponse(messages=messages_web)
