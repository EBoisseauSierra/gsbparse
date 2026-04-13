"""Domain section: Budget estimate historical data (Bet_historical)."""

from dataclasses import dataclass
from decimal import Decimal

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class BetHistoricalSection(GsbFileSection):
    """Historical budget data used by the budget-estimate module.

    One element per checked category/budget division.

    Attributes:
        Nb: Unique identifier.
        Ac: Account identifier.
        Ori: Data origin (0 = categories, 1 = budget lines).
        Div: Division number (category or budget line identifier).
        Edit: Whether the amount has been manually overridden.
        Damount: Overridden amount for the division.
        SDiv: Sub-division number.
        SEdit: Whether the sub-division amount has been manually overridden.
        SDamount: Overridden amount for the sub-division.
    """

    Nb: int
    Ac: int
    Ori: int
    Div: int
    Edit: bool
    Damount: Decimal
    SDiv: int
    SEdit: bool
    SDamount: Decimal
