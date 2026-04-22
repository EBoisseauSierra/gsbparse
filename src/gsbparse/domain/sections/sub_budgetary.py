"""Domain section: Sub-budgetary (sous-imputation budgétaire)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from gsbparse.domain.sections._base import GsbFileSection

if TYPE_CHECKING:
    from gsbparse.domain.sections.budgetary import Budgetary


@dataclass(frozen=True)
class SubBudgetary(GsbFileSection):
    """A budget sub-line defined in the Grisbi file.

    Attributes:
        Nbb: Parent budgetary identifier.
        Nb: Unique identifier within the parent budget line.
        Na: Display name.
    """

    Nbb: int
    Nb: int
    Na: str


@dataclass(frozen=True)
class DetailedSubBudgetary(GsbFileSection):
    """A budget sub-line with its parent budgetary resolved.

    Attributes:
        Nbb: Parent budgetary (resolved from the raw ``Nbb`` identifier).
        Nb: Unique identifier within the parent budget line.
        Na: Display name.
    """

    Nbb: Budgetary
    Nb: int
    Na: str
