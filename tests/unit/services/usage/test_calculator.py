from datetime import datetime
from typing import List

import pytest

from usage_service.models.message import Message
from usage_service.models.report import Report
from usage_service.services.usage.calculator import UsageCalculator


@pytest.fixture
def messages() -> list[Message]:  # noqa: D103
    return [
        Message(id=1, text="Hello world", report_id=None, timestamp=datetime.now()),
        Message(
            id=2,
            text="This is a test message",
            report_id=1,
            timestamp=datetime.now(),
        ),
        Message(id=3, text="Another message", report_id=None, timestamp=datetime.now()),
    ]


@pytest.fixture
def message_with_missing_report() -> Message:  # noqa: D103
    return Message(id=1, text="Hello world", report_id=999, timestamp=datetime.now())


@pytest.fixture
def reports() -> list[Report]:  # noqa: D103
    return [Report(id=1, name="Test Report", credits=10)]


@pytest.mark.skip(reason="Not implemented")
def test_usage_calculator_no_reports(messages: List[Message]) -> None:  # noqa: D103
    usages = UsageCalculator.call(messages, [])
    assert len(usages) == 3
    assert usages[0].credits == 1 + 0.05 * len("Hello world") + 0.2 * 2 + 0.1 * 1
    assert (
        usages[1].credits
        == 1 + 0.05 * len("This is a test message") + 0.2 * 3 + 0.1 * 2
    )
    assert usages[2].credits == 1 + 0.05 * len("Another message") + 0.2 * 2 + 0.1 * 1


@pytest.mark.skip(reason="Not implemented")
def test_usage_calculator_with_reports(  # noqa: D103
    messages: List[Message],
    reports: List[Report],
) -> None:
    usages = UsageCalculator.call(messages, reports)
    assert len(usages) == 3
    assert usages[0].credits == 1 + 0.05 * len("Hello world") + 0.2 * 2 + 0.1 * 1
    assert usages[1].credits == 10  # Report credits should be used
    assert usages[2].credits == 1 + 0.05 * len("Another message") + 0.2 * 2 + 0.1 * 1


@pytest.mark.skip(reason="Not implemented")
def test_usage_calculator_report_not_found(  # noqa: D103
    message_with_missing_report: Message,
) -> None:
    usages = UsageCalculator.call([message_with_missing_report], [])
    assert len(usages) == 3
    assert (
        usages[1].credits
        == 1 + 0.05 * len("This is a test message") + 0.2 * 3 + 0.1 * 2
    )
