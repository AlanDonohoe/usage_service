import os
from typing import Any, Dict, List

import httpx
from fastapi import HTTPException


class MessageAPI:  # noqa: D101
    DEFAULT_MESSAGE_SERVICE_URL = "https://owpublic.blob.core.windows.net"

    @classmethod
    async def call(cls) -> List[Dict[str, Any]]:  # noqa: D102
        base_url = os.getenv("URL_MESSAGE_SERVICE", cls.DEFAULT_MESSAGE_SERVICE_URL)
        message_service_url = f"{base_url}/tech-task/messages/current-period"

        async with httpx.AsyncClient() as client:
            response = await client.get(message_service_url)

            if response.status_code == 200:
                return response.json().get("messages", [])

            if response.status_code == 404:
                return []

            if response.status_code == 500:
                raise HTTPException(
                    status_code=500,
                    detail="Problem calling MessageService",
                )

        return []
