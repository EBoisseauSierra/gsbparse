"""Domain section: Currency."""

from dataclasses import dataclass

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class Currency(GsbFileSection):
    """A currency defined in the Grisbi file.

    Attributes:
        Nb: Unique identifier.
        Na: Human-readable name (e.g. ``"Euro"``).
        Co: Symbol (e.g. ``"€"``).
        Ico: ISO 4217 code (e.g. ``"EUR"``).
        Fl: Number of decimal digits (fraction digits).
    """

    Nb: int
    Na: str
    Co: str
    Ico: str
    Fl: int
