from typing import Any, Dict, List

from usage_service.infra.apis.messages.api import MessageAPI
from usage_service.models.message import Message


class MessageService:  # noqa: D101
    @classmethod
    async def call(cls) -> List[Message]:  # noqa: D102
        messages_raw = await MessageAPI.call()

        return [
            await cls._convert_from_message_raw(message_raw)
            for message_raw in messages_raw
        ]

    @classmethod
    async def _convert_from_message_raw(cls, message_raw: Dict[str, Any]) -> Message:
        return Message(**message_raw)
