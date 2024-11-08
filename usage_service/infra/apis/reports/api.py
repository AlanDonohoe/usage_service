import asyncio
import logging
import os
from typing import Any, Dict, List

import httpx
from fastapi import HTTPException

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ReportAPI:  # noqa: D101
    DEFAULT_REPORT_SERVICE_URL = "https://owpublic.blob.core.windows.net"

    @classmethod
    async def call(cls, report_ids: List[int]) -> List[Dict[str, Any]]:  # noqa: D102
        base_url = os.getenv("URL_REPORT_SERVICE", cls.DEFAULT_REPORT_SERVICE_URL)
        report_service_url = f"{base_url}/tech-task/reports"
        urls = [
            f"{report_service_url}/{report_id}"
            for report_id in cls._filtered_report_ids(report_ids)
        ]

        async with httpx.AsyncClient() as http_client:
            async with asyncio.TaskGroup() as task_group:
                tasks = [
                    task_group.create_task(cls._get_url(http_client, url))
                    for url in urls
                ]

            # Retrieve the results of each task after TaskGroup context ends
            return [task.result() for task in tasks]

    @classmethod
    def _filtered_report_ids(cls, report_ids: List[int]) -> List[int]:
        problematic_report_ids = [7321, 8452, 9634]

        filtered_report_ids = [
            report_id
            for report_id in report_ids
            if report_id not in problematic_report_ids
        ]

        if len(filtered_report_ids) < len(report_ids):
            logger.warning(
                f"Filtered out problematic report ids: {problematic_report_ids}",
            )

        return filtered_report_ids

    @classmethod
    async def _get_url(
        cls,
        client: httpx.AsyncClient,
        url: str,
    ) -> Dict[str, Any]:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            logger.error(f"Request failed for {url}: {e}")
            raise HTTPException(
                status_code=500,
                detail="Problem calling ReportService",
            ) from e
