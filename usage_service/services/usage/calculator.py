from typing import List

from usage_service.models.message import Message
from usage_service.models.report import Report
from usage_service.models.usage import Usage


class UsageCalculator:  # noqa: D101
    @classmethod
    def call(
        cls,
        messages: List[Message],
        reports: List[Report],
    ) -> List[Usage]:
        """
        Calculates Usage.

        Calculates the usage for each message based on their optional report,
        text length, and timestamp.
        """

        return []
