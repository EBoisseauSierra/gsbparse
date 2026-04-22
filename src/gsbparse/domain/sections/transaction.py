"""Domain section: Transaction."""

import logging
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import IntEnum

from gsbparse.domain.sections._base import GsbFileSection

_log = logging.getLogger(__name__)


class TransactionMarkedState(IntEnum):
    """Reconciliation / marked state stored in the ``Ma`` attribute of a ``<Transaction>`` element.

    Unknown values encountered in the file fall back to :attr:`NONE`.
    """

    NONE = -1
    NEW = 0
    POINTED = 1
    TO_RECONCILE = 2
    RECONCILED = 3

    @classmethod
    def _missing_(cls, value: object) -> "TransactionMarkedState":
        _log.warning("Unknown TransactionMarkedState value %r — falling back to NONE", value)
        return cls.NONE

    def __str__(self) -> str:
        """Return a lowercase human-readable label."""
        return self.name.lower().replace("_", " ")


@dataclass(frozen=True)
class Transaction(GsbFileSection):
    """A transaction stored in the Grisbi file.

    Foreign-key fields (``Ac``, ``Cu``, ``Pa``, etc.) hold raw integer
    identifiers as they appear in the XML.  Resolved, typed references live on
    :class:`~gsbparse.domain.detailed_transaction.DetailedTransaction`.

    Attributes:
        Ac: Account identifier.
        Nb: Transaction number (unique within the account).
        Id: OFX import identifier (nullable).
        Dt: Transaction date (nullable).
        Dv: Value date (nullable).
        Am: Amount (negative = debit).
        Cu: Currency identifier.
        Exb: Exchange direction flag (1 = 1 account_currency = rate x amount).
        Exr: Exchange rate.
        Exf: Exchange fees.
        Pa: Party identifier.
        Ca: Category identifier.
        Sca: Sub-category identifier.
        Br: Breakdown flag (1 = this is a parent split transaction).
        No: Notes (nullable).
        Pn: Payment method identifier.
        Pc: Payment method content / reference (nullable).
        Ma: Marked / reconciliation state.
        Ar: Archive identifier (0 = not archived).
        Au: Automatic transaction (0 = manual, 1 = from scheduled).
        Re: Reconcile identifier (0 = not reconciled).
        Fi: Financial year identifier.
        Bu: Budget line identifier.
        Sbu: Sub-budget line identifier.
        Vo: Voucher reference (nullable).
        Ba: Bank reference (nullable).
        Trt: Transfer transaction number (0 = not a transfer).
        Mo: Mother transaction number for breakdown children (0 = top-level).
    """

    Ac: int
    Nb: int
    Id: str | None
    Dt: date | None
    Dv: date | None
    Am: Decimal
    Cu: int
    Exb: bool
    Exr: Decimal
    Exf: Decimal
    Pa: int
    Ca: int
    Sca: int
    Br: bool
    No: str | None
    Pn: int
    Pc: str | None
    Ma: TransactionMarkedState
    Ar: int
    Au: bool
    Re: int
    Fi: int
    Bu: int
    Sbu: int
    Vo: str | None
    Ba: str | None
    Trt: int
    Mo: int
