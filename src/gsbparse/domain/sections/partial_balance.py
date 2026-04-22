"""Domain section: Partial balance (solde partiel)."""

from dataclasses import dataclass

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class PartialBalance(GsbFileSection):
    """A partial (grouped) balance defined in the Grisbi file.

    Attributes:
        Nb: Unique identifier.
        Na: Display name.
        Acc: Semicolon-separated list of account identifiers included.
        Kind: Balance kind.
        Currency: Currency identifier for the displayed balance.
        Colorise: Show negative balances in red.
    """

    Nb: int
    Na: str
    Acc: str
    Kind: int
    Currency: int
    Colorise: bool
