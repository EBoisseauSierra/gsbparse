"""Domain section: Sub-budgetary (sous-imputation budgétaire)."""

from dataclasses import dataclass

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class SubBudgetarySection(GsbFileSection):
    """A budget sub-line defined in the Grisbi file.

    Attributes:
        Nbb: Parent budgetary identifier.
        Nb: Unique identifier within the parent budget line.
        Na: Display name.
    """

    Nbb: int
    Nb: int
    Na: str
