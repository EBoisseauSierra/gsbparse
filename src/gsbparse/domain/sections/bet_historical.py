"""Domain section: Budget estimate historical data (Bet_historical)."""

from dataclasses import dataclass
from decimal import Decimal
from enum import IntEnum

from gsbparse.domain.sections._base import GsbFileSection


class BetDataOrigin(IntEnum):
    """Data origin stored in the ``Ori`` attribute of a ``<Bet_historical>`` element."""

    CATEGORIES = 0
    BUDGET_LINES = 1

    def __str__(self) -> str:
        """Return a lowercase human-readable label."""
        return self.name.lower().replace("_", " ")


@dataclass(frozen=True)
class BetHistorical(GsbFileSection):
    """Historical budget data used by the budget-estimate module.

    One element per checked category/budget division.

    Attributes:
        Nb: Unique identifier.
        Ac: Account identifier.
        Ori: Data origin (categories or budget lines).
        Div: Division number (category or budget line identifier).
        Edit: Whether the amount has been manually overridden.
        Damount: Overridden amount for the division.
        SDiv: Sub-division number.
        SEdit: Whether the sub-division amount has been manually overridden.
        SDamount: Overridden amount for the sub-division.
    """

    Nb: int
    Ac: int
    Ori: BetDataOrigin
    Div: int
    Edit: bool
    Damount: Decimal
    SDiv: int
    SEdit: bool
    SDamount: Decimal
