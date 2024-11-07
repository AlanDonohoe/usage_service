from dataclasses import dataclass
from typing import List

from .message import Message


@dataclass
class Usage:  # noqa: D101
    messages: List[Message]
