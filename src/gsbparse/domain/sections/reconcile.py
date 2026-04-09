"""Domain section: Reconcile (rapprochement)."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class ReconcileSection(GsbFileSection):
    """A reconciliation record defined in the Grisbi file.

    Attributes:
        Nb: Unique identifier.
        Na: Display name (e.g. ``"2007-1"``).
        Acc: Account identifier this reconciliation belongs to.
        Idate: Start date of the reconciliation period.
        Fdate: End date of the reconciliation period.
        Ibal: Opening balance.
        Fbal: Closing balance.
    """

    Nb: int
    Na: str
    Acc: int
    Idate: date
    Fdate: date
    Ibal: Decimal
    Fbal: Decimal
