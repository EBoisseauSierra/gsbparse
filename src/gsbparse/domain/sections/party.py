"""Domain section: Party (tiers / payee)."""

from dataclasses import dataclass

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class Party(GsbFileSection):
    """A party (payee or payer) defined in the Grisbi file.

    Attributes:
        Nb: Unique identifier.
        Na: Display name.
        Txt: Description / notes (nullable).
        Search: Import-matching search string (nullable).
        IgnCase: Ignore case when matching the search string.
        UseRegex: Treat the search string as a regular expression.
    """

    Nb: int
    Na: str
    Txt: str | None
    Search: str | None
    IgnCase: bool
    UseRegex: bool
