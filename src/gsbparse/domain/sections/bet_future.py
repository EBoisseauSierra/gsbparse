"""Domain section: Budget estimate future data (Bet_future)."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class BetFutureSection(GsbFileSection):
    """A future/projected transaction in the budget-estimate module.

    Fields mirror those of :class:`~gsbparse.domain.sections.scheduled.ScheduledSection`.

    Attributes:
        Nb: Unique identifier.
        Dt: Date (nullable).
        Ac: Account identifier.
        Am: Amount.
        Pa: Party identifier.
        IsT: Is a transfer (1 = transfer, with the target account in ``Tra``).
        Tra: Transfer target account identifier.
        Ca: Category identifier.
        Sca: Sub-category identifier.
        Pn: Payment method identifier.
        Fi: Financial year identifier.
        Bu: Budget line identifier.
        Sbu: Sub-budget line identifier.
        No: Notes (nullable).
        Au: Automatic transaction flag.
        Pe: Periodicity.
        Pei: Periodicity interval.
        Pep: Custom periodicity.
        Dtl: Limit date (nullable).
        Mo: Mother transaction identifier (for breakdown children).
    """

    Nb: int
    Dt: date | None
    Ac: int
    Am: Decimal
    Pa: int
    IsT: bool
    Tra: int
    Ca: int
    Sca: int
    Pn: int
    Fi: int
    Bu: int
    Sbu: int
    No: str | None
    Au: bool
    Pe: int
    Pei: int
    Pep: int
    Dtl: date | None
    Mo: int
