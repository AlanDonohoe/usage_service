from decimal import Decimal
from typing import Any, ClassVar, Dict, List, Union

from usage_service.models.message import Message
from usage_service.models.report import Report
from usage_service.models.usage import Usage


class UsageCalculator:
    """
    Calculates Usage.

    Calculates the usage for each message based on their optional report,
    or the message's text length and other attributes.
    """

    MINIMUM_CREDITS: ClassVar[Decimal] = Decimal(1)
    CHAR_COUNT_MAX_BEFORE_LENGTH_PENALTY: ClassVar[int] = 100

    MESSAGE_BASED_CREDIT_WEIGHTS: ClassVar[Dict[str, Any]] = {
        "message_base_cost": "1.0",
        "character_count": "0.05",
        "word_length_multipliers": {
            "1-3": "0.1",
            "4-7": "0.2",
            "8+": "0.3",
        },
        "third_vowels": "0.3",
        "length_penalty": "5.0",
        "unique_word_bonus": "-2.0",
        "palindromes": "2.0",
    }

    def __init__(self, messages: List[Message], reports: List[Report]) -> None:
        self._messages = messages
        self._reports = reports

    def call(self) -> List[Usage]:  # noqa: D102
        usages = []

        for message in self._messages:
            if report := self._report(message.report_id):
                usages.append(self._report_based_usage(message, report))
            else:
                usages.append(self._message_based_usage(message))

        return usages

    def _report(self, report_id: Union[int, None]) -> Report | None:
        if report_id is None:
            return None

        return next(
            (report for report in self._reports if report.id == report_id),
            None,
        )

    def _report_based_usage(
        self,
        message: Message,
        report: Report,
    ) -> Usage:
        return Usage(
            message_id=message.id,
            timestamp=message.timestamp,
            report_name=report.name,
            credits_used=report.credit_cost,
        )

    def _message_based_usage(
        self,
        message: Message,
    ) -> Usage:
        return Usage(
            message_id=message.id,
            timestamp=message.timestamp,
            credits_used=self._message_based_credits_used(message.text),
        )

    def _message_based_credits_used(
        self,
        text: str,
    ) -> int:
        words = text.split()
        credits = Decimal(self.MESSAGE_BASED_CREDIT_WEIGHTS["message_base_cost"])

        credits += self._character_count_credits(text)
        credits += self._word_length_credits(words)
        credits += self._third_vowel_credits(text)
        credits += self._length_penalty_credits(text)
        credits += self._unique_word_bonus_credits(words, credits)
        credits += self._palindrome_credits(text)

        return round(credits)

    def _palindrome_credits(self, text: str) -> Decimal:
        palindrome_weight = Decimal(self.MESSAGE_BASED_CREDIT_WEIGHTS["palindromes"])
        text_alnum_only = "".join([c for c in text.lower() if c.isalnum()])

        if text_alnum_only == text_alnum_only[::-1]:
            return palindrome_weight

        return Decimal(0)

    def _unique_word_bonus_credits(
        self,
        words: List[str],
        current_credits: Decimal,
    ) -> Decimal:
        unique_word_bonus_weight = Decimal(
            self.MESSAGE_BASED_CREDIT_WEIGHTS["unique_word_bonus"],
        )
        if (current_credits + unique_word_bonus_weight) < self.MINIMUM_CREDITS:
            return Decimal(0)

        return (
            Decimal(unique_word_bonus_weight)
            if len(set(words)) == len(words)
            else Decimal(0)
        )

    def _length_penalty_credits(self, text: str) -> Decimal:
        length_penalty_weight = Decimal(
            self.MESSAGE_BASED_CREDIT_WEIGHTS["length_penalty"],
        )
        if len(text) > self.CHAR_COUNT_MAX_BEFORE_LENGTH_PENALTY:
            return Decimal(length_penalty_weight)

        return Decimal(0)

    def _third_vowel_credits(self, text: str) -> Decimal:
        text_with_no_whitespace = "".join(text.split())
        third_char_is_vowel_count = 0
        third_vowel_weight = Decimal(self.MESSAGE_BASED_CREDIT_WEIGHTS["third_vowels"])
        vowels = "aeiouAEIOU"

        for i in range(
            2,
            len(text_with_no_whitespace),
            3,
        ):  # Start at index 2 (3rd character) and step by 3
            if text_with_no_whitespace[i] in vowels:
                third_char_is_vowel_count += 1

        return third_vowel_weight * Decimal(third_char_is_vowel_count)

    def _character_count_credits(self, text: str) -> Decimal:
        character_count_weight = Decimal(
            self.MESSAGE_BASED_CREDIT_WEIGHTS["character_count"],
        )
        text_with_no_whitespace = "".join(text.split())

        return Decimal(character_count_weight * Decimal(len(text_with_no_whitespace)))

    def _word_length_credits(self, words: List[str]) -> Decimal:
        word_length_multipliers = self.MESSAGE_BASED_CREDIT_WEIGHTS[
            "word_length_multipliers"
        ]

        credits = Decimal(0)

        for word in words:
            if 1 <= len(word) <= 3:
                credits += Decimal(word_length_multipliers["1-3"])
            elif 4 <= len(word) <= 7:
                credits += Decimal(word_length_multipliers["4-7"])
            elif len(word) >= 8:
                credits += Decimal(word_length_multipliers["8+"])

        return credits
