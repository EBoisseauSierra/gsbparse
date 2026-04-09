"""Domain section: Archive."""

from dataclasses import dataclass
from datetime import date

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class ArchiveSection(GsbFileSection):
    """An archive group defined in the Grisbi file.

    Archives compress old transactions into a single summary entry.
    An archive is either date-bounded (``Bdte``/``Edte`` set) or
    financial-year-bounded (``Fye`` set); the other fields are ``None``.

    Attributes:
        Nb: Unique identifier.
        Na: Display name.
        Bdte: Begin date of the archived period (nullable).
        Edte: End date of the archived period (nullable).
        Fye: Financial year identifier for year-based archives (0 = not set).
        Rep: Report path (nullable).
    """

    Nb: int
    Na: str
    Bdte: date | None
    Edte: date | None
    Fye: int
    Rep: str | None
