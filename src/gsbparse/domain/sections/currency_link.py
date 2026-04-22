"""Domain section: Currency link (exchange rate between two currencies)."""

from dataclasses import dataclass
from decimal import Decimal

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class CurrencyLink(GsbFileSection):
    """An exchange-rate link between two currencies.

    Attributes:
        Nb: Unique identifier.
        Cu1: First currency identifier.
        Cu2: Second currency identifier.
        Ex: Exchange rate (Cu1 → Cu2).
        Fl: Fixed link — ``True`` means the rate is pegged (e.g. CFA franc).
    """

    Nb: int
    Cu1: int
    Cu2: int
    Ex: Decimal
    Fl: bool
