from typing import Any, Dict, List

from usage_service.infra.apis.reports.api import ReportAPI
from usage_service.models.report import Report


class ReportService:  # noqa: D101
    @classmethod
    async def call(cls, report_ids: List[int]) -> List[Report]:  # noqa: D102
        reports_raw = await ReportAPI.call(report_ids)

        return [
            await cls._convert_from_report_raw(report_raw) for report_raw in reports_raw
        ]

    @classmethod
    async def _convert_from_report_raw(cls, report_raw: Dict[str, Any]) -> Report:
        return Report(**report_raw)
