from typing import Optional

from pydantic import BaseModel


class MessageResponse(BaseModel):  # noqa: D101
    message_id: int
    credits_used: int
    report_name: Optional[str]
    timestamp: str
