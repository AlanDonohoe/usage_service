from usage_service.infra.apis.messages.service import MessageService
from usage_service.models.usage import Usage


class UsageService:  # noqa: D101
    @classmethod
    async def call(cls) -> Usage:  # noqa: D102
        messages_raw = await MessageService.call()

        return Usage(messages=messages_raw)
