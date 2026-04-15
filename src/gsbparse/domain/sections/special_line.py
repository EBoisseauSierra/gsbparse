"""Domain section: Special line (condition attached to an import rule)."""

from dataclasses import dataclass
from enum import IntEnum

from gsbparse.domain.sections._base import GsbFileSection


class SpecialLineAction(IntEnum):
    """Action type stored in the ``SpA`` attribute of a ``<Special_line>`` element."""

    SKIP = 0
    INVERT_AMOUNT = 1
    KEEP_IF_FOUND = 2

    def __str__(self) -> str:
        """Return a lowercase human-readable label."""
        return self.name.lower().replace("_", " ")


@dataclass(frozen=True)
class SpecialLineSection(GsbFileSection):
    """A special-condition line attached to a CSV import rule.

    Attributes:
        Nb: Index of this line within its rule (1-based).
        NuR: Parent import rule number.
        SpA: Action type.
        SpAD: Column containing the data for the inversion action (0-based).
        SpUD: Column containing the data to search (0-based).
        SpUT: Data string to search for.
    """

    Nb: int
    NuR: int
    SpA: SpecialLineAction
    SpAD: int
    SpUD: int
    SpUT: str
