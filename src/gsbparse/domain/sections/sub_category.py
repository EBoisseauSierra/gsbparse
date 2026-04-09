"""Domain section: Sub-category."""

from dataclasses import dataclass

from gsbparse.domain.sections._base import GsbFileSection


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
