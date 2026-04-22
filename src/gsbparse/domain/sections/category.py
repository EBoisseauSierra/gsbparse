"""Domain section: Category."""

from dataclasses import dataclass
from enum import IntEnum

from gsbparse.domain.sections._base import GsbFileSection


class CategoryKind(IntEnum):
    """Category kind stored in the ``Kd`` attribute of ``<Category>`` and ``<Budgetary>``."""

    EXPENSE = 0
    INCOME = 1

    def __str__(self) -> str:
        """Return a lowercase human-readable label."""
        return self.name.lower()


@dataclass(frozen=True)
class Category(GsbFileSection):
    """A transaction category defined in the Grisbi file.

    Attributes:
        Nb: Unique identifier.
        Na: Display name.
        Kd: Kind (expense or income).
    """

    Nb: int
    Na: str
    Kd: CategoryKind
