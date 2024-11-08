from typing import List, Optional

from pydantic import BaseModel


class UsageResponse(BaseModel):  # noqa: D101
    message_id: int
    credits_used: int
    report_name: Optional[str]
    timestamp: str


class UsageListResponse(BaseModel):  # noqa: D101
    usage: List[UsageResponse]
