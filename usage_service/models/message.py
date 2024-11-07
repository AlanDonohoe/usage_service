from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Message:  # noqa: D101
    id: int
    credits_used: int
    text: str
    timestamp: str
    report_id: Optional[int] = field(default=None)
    report_name: Optional[str] = field(default=None)

    def dict(self) -> Dict[str, Any]:  # noqa: D102
        return {
            "message_id": self.id,
            "credits_used": self.credits_used,
            "report_name": self.report_name,
            "timestamp": self.timestamp,
        }
