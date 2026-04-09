"""Domain section: Category."""

from dataclasses import dataclass

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class CategorySection(GsbFileSection):
    """A transaction category defined in the Grisbi file.

    Attributes:
        Nb: Unique identifier.
        Na: Display name.
        Kd: Kind (0 = expense, 1 = income).
    """

    Nb: int
    Na: str
    Kd: int
