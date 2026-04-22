"""Domain section: Budgetary (imputation budgétaire)."""

from dataclasses import dataclass

from gsbparse.domain.sections._base import GsbFileSection
from gsbparse.domain.sections.category import CategoryKind


@dataclass(frozen=True)
class Budgetary(GsbFileSection):
    """A top-level budget line defined in the Grisbi file.

    Attributes:
        Nb: Unique identifier.
        Na: Display name.
        Kd: Kind (expense or income).
    """

    Nb: int
    Na: str
    Kd: CategoryKind
