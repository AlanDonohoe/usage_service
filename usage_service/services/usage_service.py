from typing import List

from usage_service.infra.apis.messages.service import MessageService
from usage_service.infra.apis.reports.service import ReportService
from usage_service.models.usage import Usage
from usage_service.services.usage.calculator import UsageCalculator


class UsageService:
    """
    Acts as the orchestrator for determining usage.

    Works with the `MessageService` and `ReportService` to get the messages and reports
    to finally calculate the usage.
    """

    @classmethod
    async def call(cls) -> List[Usage]:  # noqa: D102
        messages = await MessageService.call()

        messages_with_unique_report_id = list(
            {message.report_id: message for message in messages}.values(),
        )
        unique_report_ids = [
            message.report_id
            for message in messages_with_unique_report_id
            if message.report_id is not None
        ]

        reports = await ReportService.call(unique_report_ids)

        return UsageCalculator.call(messages, reports)
