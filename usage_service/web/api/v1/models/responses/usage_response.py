from typing import List

from pydantic import BaseModel

from usage_service.web.api.v1.models.responses.message_response import MessageResponse


class UsageResponse(BaseModel):  # noqa: D101
    messages: List[MessageResponse]
