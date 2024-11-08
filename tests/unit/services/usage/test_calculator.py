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
    return [Report(id=1, name="Test Report", credit_cost=10)]


def test_usage_calculator_no_reports(messages: List[Message]) -> None:  # noqa: D103
    usages = UsageCalculator(messages, []).call()

    assert len(usages) == 3
    assert usages[0].credits_used == 2
    assert usages[1].credits_used == 2
    assert usages[2].credits_used == 1


def test_usage_calculator_with_reports(  # noqa: D103
    messages: List[Message],
    reports: List[Report],
) -> None:
    usages = UsageCalculator(messages, reports).call()

    assert len(usages) == 3
    assert usages[0].credits_used == 2
    assert (
        usages[1].credits_used == reports[0].credit_cost
    )  # Report credits should be used
    assert usages[2].credits_used == 1


def test_usage_calculator_report_not_found(  # noqa: D103
    message_with_missing_report: Message,
) -> None:
    usages = UsageCalculator([message_with_missing_report], []).call()

    assert len(usages) == 1
    assert usages[0].credits_used == 2


def test_usage_calculator_palindrome() -> None:  # noqa: D103
    palindrome_message = Message(
        id=1,
        text="noon",
        report_id=None,
        timestamp=datetime.now(),
    )
    usages = UsageCalculator([palindrome_message], []).call()

    assert len(usages) == 1
    assert usages[0].credits_used == 4


def test_usage_calculator_extra_long_message_text() -> None:  # noqa: D103
    extra_long_text = (
        "The evening sky was painted in hues of amber and violet, "
        "casting a gentle glow across the quiet town. Leaves rustled as a "
        "soft breeze passed, and distant laughter echoed from a nearby park."
        ", blending into dusk"
    )

    extra_long_text_message = Message(
        id=1,
        text=extra_long_text,
        report_id=None,
        timestamp=datetime.now(),
    )
    usages = UsageCalculator([extra_long_text_message], []).call()

    assert len(usages) == 1
    assert usages[0].credits_used == 28


def test_usage_calculator_unique_word() -> None:  # noqa: D103
    unique_word_text = (
        "The evening sky was painted in hues of amber and violet, "
        "casting gentle glow across quiet town Leaves rustled"
    )

    unique_word_message = Message(
        id=1,
        text=unique_word_text,
        report_id=None,
        timestamp=datetime.now(),
    )
    usages = UsageCalculator([unique_word_message], []).call()

    assert len(usages) == 1
    assert usages[0].credits_used == 16


def test_usage_calculator_third_char_is_a_vowel() -> None:  # noqa: D103
    unique_word_text = "cnacnecno this is more regular text but the first are vowels"

    unique_word_message = Message(
        id=1,
        text=unique_word_text,
        report_id=None,
        timestamp=datetime.now(),
    )
    usages = UsageCalculator([unique_word_message], []).call()

    assert len(usages) == 1
    assert usages[0].credits_used == 6
