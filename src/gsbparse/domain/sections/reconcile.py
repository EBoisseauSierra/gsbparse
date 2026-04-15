"""Domain section: Reconcile (rapprochement)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from gsbparse.domain.sections._base import GsbFileSection

if TYPE_CHECKING:
    from gsbparse.domain.sections.account import AccountSection


@dataclass(frozen=True)
class ReconcileSection(GsbFileSection):
    """A reconciliation record defined in the Grisbi file.

    Attributes:
        Nb: Unique identifier.
        Na: Display name (e.g. ``"2007-1"``).
        Acc: Account identifier this reconciliation belongs to.
        Idate: Start date of the reconciliation period (nullable).
        Fdate: End date of the reconciliation period (nullable).
        Ibal: Opening balance.
        Fbal: Closing balance.
    """

    Nb: int
    Na: str
    Acc: int
    Idate: date | None
    Fdate: date | None
    Ibal: Decimal
    Fbal: Decimal


@dataclass(frozen=True)
class DetailedReconcileSection(GsbFileSection):
    """A reconciliation record with its account resolved.

    Attributes:
        Nb: Unique identifier.
        Na: Display name (e.g. ``"2007-1"``).
        Acc: Account this reconciliation belongs to (resolved from the raw ``Acc`` identifier).
        Idate: Start date of the reconciliation period (nullable).
        Fdate: End date of the reconciliation period (nullable).
        Ibal: Opening balance.
        Fbal: Closing balance.
    """

    Nb: int
    Na: str
    Acc: AccountSection
    Idate: date | None
    Fdate: date | None
    Ibal: Decimal
    Fbal: Decimal
