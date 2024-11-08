from dataclasses import dataclass


@dataclass(frozen=True)
class Report:  # noqa: D101
    id: int
    credit_cost: int
    name: str
