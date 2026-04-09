"""Domain section: Budgetary (imputation budgétaire)."""

from dataclasses import dataclass

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class BudgetarySection(GsbFileSection):
    """A top-level budget line defined in the Grisbi file.

    Attributes:
        Nb: Unique identifier.
        Na: Display name.
        Kd: Kind (0 = expense, 1 = income).
    """

    Nb: int
    Na: str
    Kd: int
