"""Domain section: Sub-category."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from gsbparse.domain.sections._base import GsbFileSection

if TYPE_CHECKING:
    from gsbparse.domain.sections.category import CategorySection


@dataclass(frozen=True)
class SubCategorySection(GsbFileSection):
    """A transaction sub-category defined in the Grisbi file.

    Attributes:
        Nbc: Parent category identifier.
        Nb: Unique identifier within the parent category.
        Na: Display name.
    """

    Nbc: int
    Nb: int
    Na: str


@dataclass(frozen=True)
class DetailedSubCategorySection(GsbFileSection):
    """A transaction sub-category with its parent category resolved.

    Attributes:
        Nbc: Parent category (resolved from the raw ``Nbc`` identifier).
        Nb: Unique identifier within the parent category.
        Na: Display name.
    """

    Nbc: CategorySection
    Nb: int
    Na: str
