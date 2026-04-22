"""Domain section: Budget estimate global options (Bet)."""

from dataclasses import dataclass

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class Bet(GsbFileSection):
    """Global budget-estimate options.

    Note: The format spec lists ``Bdte`` but the example file uses ``Ddte``.
    This implementation uses the attribute name from the example file.

    Attributes:
        Ddte: Default start-date mode (1 = first day of month, 2 = today).
        Bet_deb_cash_account_option: Debit/cash account option flag.
    """

    Ddte: int
    Bet_deb_cash_account_option: int
