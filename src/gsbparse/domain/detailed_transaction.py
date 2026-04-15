"""Domain model: DetailedTransaction with resolved foreign keys.

A :class:`DetailedTransaction` is a denormalized view of a
:class:`~gsbparse.domain.sections.transaction.TransactionSection` where every
foreign-key integer has been resolved to the referenced domain object.

The :func:`build_detailed_transactions` function performs that resolution given
a parsed :class:`~gsbparse.domain.file.GsbFile`.
"""

from __future__ import annotations

import functools
import logging
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gsbparse.domain.file import GsbFile

from gsbparse.domain.errors import UnknownDetailedTransactionPathError
from gsbparse.domain.sections.account import AccountSection
from gsbparse.domain.sections.budgetary import BudgetarySection
from gsbparse.domain.sections.category import CategorySection
from gsbparse.domain.sections.currency import CurrencySection
from gsbparse.domain.sections.financial_year import FinancialYearSection
from gsbparse.domain.sections.party import PartySection
from gsbparse.domain.sections.payment import PaymentSection
from gsbparse.domain.sections.reconcile import ReconcileSection
from gsbparse.domain.sections.sub_budgetary import SubBudgetarySection
from gsbparse.domain.sections.sub_category import SubCategorySection
from gsbparse.domain.sections.transaction import TransactionMarkedState

_log = logging.getLogger(__name__)


@dataclass(frozen=True)
class DetailedTransaction:
    """A transaction with every foreign-key field resolved to its domain object.

    Fields mirror :class:`~gsbparse.domain.sections.transaction.TransactionSection`
    but integer FK identifiers are replaced by the referenced section instances
    (or ``None`` when the FK is zero / not present in the file).

    Attributes:
        Nb: Transaction number (primary key within the account).
        Id: OFX transaction identifier (nullable).
        Dt: Transaction date (nullable).
        Dv: Value date (nullable).
        Am: Amount (positive = credit, negative = debit).
        Exb: Exchange-rate flag.
        Exr: Exchange rate.
        Exf: Exchange fee.
        Br: Breakdown flag (True for parent split transactions).
        No: Free-text notes (nullable).
        Pc: Payment method content / cheque number (nullable).
        Vo: Voucher reference (nullable).
        Ba: Bank reference (nullable).
        Au: Automatic transaction flag.
        Ac: Account this transaction belongs to.
        Cu: Currency of this transaction.
        Pa: Payee / party (None when unset).
        Ca: Category (None when unset).
        Sca: Sub-category (None when unset).
        Pn: Payment method (None when unset).
        Ma: Marked / reconciliation state.
        Ar: Archive this transaction belongs to (identifier; not resolved).
        Re: Reconcile record (None when unset).
        Fi: Financial year (None when unset).
        Bu: Budget line (None when unset).
        Sbu: Sub-budget line (None when unset).
        Trt: Transfer target account (None when not a transfer).
        Mo: Mother transaction number for breakdown children (0 = top-level).
    """

    Nb: int
    Id: str | None
    Dt: date | None
    Dv: date | None
    Am: Decimal
    Exb: bool
    Exr: Decimal
    Exf: Decimal
    Br: bool
    No: str | None
    Pc: str | None
    Vo: str | None
    Ba: str | None
    Au: bool
    Ma: TransactionMarkedState
    Ar: int
    Mo: int
    Ac: AccountSection
    Cu: CurrencySection
    Pa: PartySection | None
    Ca: CategorySection | None
    Sca: SubCategorySection | None
    Pn: PaymentSection | None
    Re: ReconcileSection | None
    Fi: FinancialYearSection | None
    Bu: BudgetarySection | None
    Sbu: SubBudgetarySection | None
    Trt: AccountSection | None


@dataclass(frozen=True)
class DetailedTransactionColumn:
    """Specification for one column in a detailed-transactions DataFrame.

    Attributes:
        path: Dotted attribute path on :class:`DetailedTransaction`,
            e.g. ``"Ac.Na"`` or ``"Am"``.
        output_name: Column name in the output ``pd.DataFrame``,
            e.g. ``"account"`` or ``"amount"``.
    """

    path: str
    output_name: str


#: Default column projection used by :func:`gsbparse.pandas.to_df` when no
#: ``columns=`` argument is provided.
DEFAULT_DETAILED_TRANSACTION_COLUMNS: list[DetailedTransactionColumn] = [
    DetailedTransactionColumn("Nb", "transaction_number"),
    DetailedTransactionColumn("Dt", "date"),
    DetailedTransactionColumn("Dv", "value_date"),
    DetailedTransactionColumn("Am", "amount"),
    DetailedTransactionColumn("No", "notes"),
    DetailedTransactionColumn("Vo", "voucher"),
    DetailedTransactionColumn("Ba", "bank_reference"),
    DetailedTransactionColumn("Pc", "payment_content"),
    DetailedTransactionColumn("Br", "is_breakdown"),
    DetailedTransactionColumn("Au", "is_automatic"),
    DetailedTransactionColumn("Ma", "marked"),
    DetailedTransactionColumn("Ac.Name", "account"),
    DetailedTransactionColumn("Cu.Na", "currency"),
    DetailedTransactionColumn("Pa.Na", "party"),
    DetailedTransactionColumn("Ca.Na", "category"),
    DetailedTransactionColumn("Sca.Na", "sub_category"),
    DetailedTransactionColumn("Pn.Name", "payment_method"),
    DetailedTransactionColumn("Re.Na", "reconcile"),
    DetailedTransactionColumn("Fi.Na", "financial_year"),
    DetailedTransactionColumn("Bu.Na", "budget"),
    DetailedTransactionColumn("Sbu.Na", "sub_budget"),
    DetailedTransactionColumn("Trt.Name", "transfer_account"),
]


def _resolve_path(tx: DetailedTransaction, path: str) -> object:
    """Walk a dotted attribute path on *tx*, returning ``None`` for any missing step."""
    try:
        return functools.reduce(getattr, path.split("."), tx)
    except AttributeError as exc:
        raise UnknownDetailedTransactionPathError(
            f"Path {path!r} does not exist on DetailedTransaction: {exc}"
        ) from exc


def validate_columns(columns: list[DetailedTransactionColumn]) -> None:
    """Validate that every path in *columns* exists on :class:`DetailedTransaction`.

    Args:
        columns: Column specs to validate.

    Raises:
        UnknownDetailedTransactionPathError: A path references a non-existent attribute.
    """
    import dataclasses

    # Build a dummy instance to walk attribute paths without real data.
    # We only need to validate the first segment (top-level field names).
    field_names = {f.name for f in dataclasses.fields(DetailedTransaction)}
    for col in columns:
        top = col.path.split(".")[0]
        if top not in field_names:
            raise UnknownDetailedTransactionPathError(
                f"Path {col.path!r} references unknown field {top!r} on DetailedTransaction"
            )


def build_detailed_transactions(gsb_file: GsbFile) -> list[DetailedTransaction] | None:
    """Resolve foreign keys in all transactions and return :class:`DetailedTransaction` list.

    Returns ``None`` when the file contains no transactions.

    Args:
        gsb_file: A fully parsed :class:`~gsbparse.domain.file.GsbFile`.

    Returns:
        A list of :class:`DetailedTransaction` instances, or ``None``.
    """
    if gsb_file.transactions is None:
        return None

    # Build lookup dicts keyed by Nb (primary key for each section type).
    accounts: dict[int, AccountSection] = (
        {a.Number: a for a in gsb_file.accounts} if gsb_file.accounts else {}
    )
    currencies: dict[int, CurrencySection] = (
        {c.Nb: c for c in gsb_file.currencies} if gsb_file.currencies else {}
    )
    parties: dict[int, PartySection] = (
        {p.Nb: p for p in gsb_file.parties} if gsb_file.parties else {}
    )
    categories: dict[int, CategorySection] = (
        {c.Nb: c for c in gsb_file.categories} if gsb_file.categories else {}
    )
    sub_categories: dict[int, SubCategorySection] = (
        {s.Nb: s for s in gsb_file.sub_categories} if gsb_file.sub_categories else {}
    )
    payment_methods: dict[int, PaymentSection] = (
        {p.Number: p for p in gsb_file.payment_methods} if gsb_file.payment_methods else {}
    )
    reconciles: dict[int, ReconcileSection] = (
        {r.Nb: r for r in gsb_file.reconciles} if gsb_file.reconciles else {}
    )
    financial_years: dict[int, FinancialYearSection] = (
        {f.Nb: f for f in gsb_file.financial_years} if gsb_file.financial_years else {}
    )
    budgetaries: dict[int, BudgetarySection] = (
        {b.Nb: b for b in gsb_file.budgetaries} if gsb_file.budgetaries else {}
    )
    sub_budgetaries: dict[int, SubBudgetarySection] = (
        {s.Nb: s for s in gsb_file.sub_budgetaries} if gsb_file.sub_budgetaries else {}
    )

    result: list[DetailedTransaction] = []
    for tx in gsb_file.transactions:
        account = accounts.get(tx.Ac)
        if account is None:
            _log.warning("Transaction %d: account %d not found — skipping", tx.Nb, tx.Ac)
            continue

        currency = currencies.get(tx.Cu)
        if currency is None:
            _log.warning("Transaction %d: currency %d not found — skipping", tx.Nb, tx.Cu)
            continue

        result.append(
            DetailedTransaction(
                Nb=tx.Nb,
                Id=tx.Id,
                Dt=tx.Dt,
                Dv=tx.Dv,
                Am=tx.Am,
                Exb=tx.Exb,
                Exr=tx.Exr,
                Exf=tx.Exf,
                Br=tx.Br,
                No=tx.No,
                Pc=tx.Pc,
                Vo=tx.Vo,
                Ba=tx.Ba,
                Au=tx.Au,
                Ma=tx.Ma,
                Ar=tx.Ar,
                Mo=tx.Mo,
                Ac=account,
                Cu=currency,
                Pa=parties.get(tx.Pa) if tx.Pa != 0 else None,
                Ca=categories.get(tx.Ca) if tx.Ca != 0 else None,
                Sca=sub_categories.get(tx.Sca) if tx.Sca != 0 else None,
                Pn=payment_methods.get(tx.Pn) if tx.Pn != 0 else None,
                Re=reconciles.get(tx.Re) if tx.Re != 0 else None,
                Fi=financial_years.get(tx.Fi) if tx.Fi not in (0, -1, -2) else None,
                Bu=budgetaries.get(tx.Bu) if tx.Bu != 0 else None,
                Sbu=sub_budgetaries.get(tx.Sbu) if tx.Sbu != 0 else None,
                Trt=accounts.get(tx.Trt) if tx.Trt != 0 else None,
            )
        )

    return result if result else None
