from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Message:  # noqa: D101
    id: int
    text: str
    timestamp: str
    report_id: Optional[int] = field(default=None)
