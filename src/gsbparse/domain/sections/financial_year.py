"""Domain section: Financial year (exercice)."""

from dataclasses import dataclass
from datetime import date

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class FinancialYearSection(GsbFileSection):
    """A financial year defined in the Grisbi file.

    Attributes:
        Nb: Unique identifier.
        Na: Display name (e.g. ``"2007"``).
        Bdte: Begin date.
        Edte: End date.
        Sho: Show this financial year in the UI.
    """

    Nb: int
    Na: str
    Bdte: date
    Edte: date
    Sho: bool
