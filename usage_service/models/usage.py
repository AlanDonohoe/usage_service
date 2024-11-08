from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Usage:  # noqa: D101
    credits_used: int
    message_id: int
    timestamp: str
    report_name: Optional[str] = None

    def dict(self) -> Dict[str, Any]:  # noqa: D102
        return {
            "credits_used": self.credits_used,
            "message_id": self.message_id,
            "timestamp": self.timestamp,
            "report_name": self.report_name,
        }
