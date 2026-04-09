"""Domain section: Special line (condition attached to an import rule)."""

from dataclasses import dataclass

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class SpecialLineSection(GsbFileSection):
    """A special-condition line attached to a CSV import rule.

    Attributes:
        Nb: Index of this line within its rule (1-based).
        NuR: Parent import rule number.
        SpA: Action type (0 = skip line, 1 = invert amount, 2 = keep if found).
        SpAD: Column containing the data for the inversion action (0-based).
        SpUD: Column containing the data to search (0-based).
        SpUT: Data string to search for.
    """

    Nb: int
    NuR: int
    SpA: int
    SpAD: int
    SpUD: int
    SpUT: str
