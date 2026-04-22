"""Domain model: DetailedTransaction with resolved foreign keys.

A :class:`DetailedTransaction` is a denormalized view of a
:class:`~gsbparse.domain.sections.transaction.Transaction` where every
foreign-key integer has been resolved to the referenced domain object.

The :func:`build_detailed_transactions` function performs that resolution given
a parsed :class:`~gsbparse.domain.file.GsbFile`.
"""

from __future__ import annotations

import dataclasses
import logging
import typing
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gsbparse.domain.file import GsbFile

from gsbparse.domain.errors import UnknownDetailedTransactionPathError
from gsbparse.domain.sections.account import Account, DetailedAccount
from gsbparse.domain.sections.bank import Bank
from gsbparse.domain.sections.budgetary import Budgetary
from gsbparse.domain.sections.category import Category
from gsbparse.domain.sections.currency import Currency
from gsbparse.domain.sections.financial_year import FinancialYear
from gsbparse.domain.sections.party import Party
from gsbparse.domain.sections.payment import Payment
from gsbparse.domain.sections.reconcile import DetailedReconcile
from gsbparse.domain.sections.sub_budgetary import DetailedSubBudgetary
from gsbparse.domain.sections.sub_category import DetailedSubCategory
from gsbparse.domain.sections.transaction import TransactionMarkedState

_log = logging.getLogger(__name__)


@dataclass(frozen=True)
class DetailedTransaction:
    """A transaction with every foreign-key field resolved to its domain object.

    Fields mirror :class:`~gsbparse.domain.sections.transaction.Transaction`
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
        Trt: Paired contra-transaction for transfers (None when not a transfer or contra not found).
            The nested object's own ``Trt`` is always ``None`` to prevent infinite nesting.
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
    Ac: DetailedAccount
    Cu: Currency
    Pa: Party | None
    Ca: Category | None
    Sca: DetailedSubCategory | None
    Pn: Payment | None
    Re: DetailedReconcile | None
    Fi: FinancialYear | None
    Bu: Budgetary | None
    Sbu: DetailedSubBudgetary | None
    Trt: DetailedTransaction | None


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
    DetailedTransactionColumn("Trt.Ac.Name", "transfer_account"),
]


def _unwrap_optional_type(tp: object) -> object:
    """Strip ``X | None`` / ``Optional[X]`` → ``X``.

    Returns the first non-``None`` type argument when *tp* is a two-argument
    Union/Optional type.  Returns *tp* unchanged for all other inputs.
    """
    args = typing.get_args(tp)
    if args:
        non_none = [a for a in args if a is not type(None)]
        if len(non_none) == 1:
            return non_none[0]
    return tp


def validate_columns(columns: list[DetailedTransactionColumn]) -> None:
    """Validate that every dotted path in *columns* exists on :class:`DetailedTransaction`.

    Walks each path segment-by-segment through the type-hint hierarchy so that
    deep typos (e.g. ``"Ac.Nme"`` instead of ``"Ac.Name"``) are caught at
    validation time, before the DataFrame is built.

    Args:
        columns: Column specs to validate.

    Raises:
        UnknownDetailedTransactionPathError: A path segment references a
            non-existent attribute at any depth.
    """
    for col in columns:
        _validate_path(col.path)


def _validate_path(path: str) -> None:
    """Raise :exc:`UnknownDetailedTransactionPathError` if *path* is invalid."""
    import sys

    segments = path.split(".")
    current_type: object = DetailedTransaction
    # This module imports all domain section types at runtime, while some of
    # those section classes guard their cross-references behind TYPE_CHECKING to
    # avoid circular imports.  Merging each class's module globals with this
    # module's globals makes those TYPE_CHECKING-guarded symbols visible during
    # annotation resolution.
    this_module_ns = vars(sys.modules[__name__])
    for i, segment in enumerate(segments):
        if not dataclasses.is_dataclass(current_type):
            type_name = getattr(current_type, "__name__", repr(current_type))
            raise UnknownDetailedTransactionPathError(
                f"Path {path!r}: cannot navigate into non-dataclass type "
                f"{type_name!r} at segment {segment!r}"
            )
        cls_module = sys.modules.get(getattr(current_type, "__module__", ""), None)
        merged_ns = {**(vars(cls_module) if cls_module is not None else {}), **this_module_ns}
        hints = typing.get_type_hints(current_type, localns=merged_ns)
        field_names = {f.name for f in dataclasses.fields(current_type)}
        if segment not in field_names:
            type_name = getattr(current_type, "__name__", repr(current_type))
            raise UnknownDetailedTransactionPathError(
                f"Path {path!r} references unknown field {segment!r} on {type_name}"
            )
        if i < len(segments) - 1:
            current_type = _unwrap_optional_type(hints[segment])


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
    accounts: dict[int, Account] = (
        {a.Number: a for a in gsb_file.accounts} if gsb_file.accounts else {}
    )
    banks: dict[int, Bank] = {b.Nb: b for b in gsb_file.banks} if gsb_file.banks else {}
    currencies: dict[int, Currency] = (
        {c.Nb: c for c in gsb_file.currencies} if gsb_file.currencies else {}
    )
    parties: dict[int, Party] = {p.Nb: p for p in gsb_file.parties} if gsb_file.parties else {}
    categories: dict[int, Category] = (
        {c.Nb: c for c in gsb_file.categories} if gsb_file.categories else {}
    )
    # Keyed by (parent_category_nb, sub_category_nb) to disambiguate shared Nb values.
    detailed_sub_categories: dict[tuple[int, int], DetailedSubCategory] = {}
    if gsb_file.sub_categories:
        for sc in gsb_file.sub_categories:
            parent_category = categories.get(sc.Nbc)
            if parent_category is None:
                _log.warning(
                    "SubCategory %d (parent=%d): parent category not found — skipping",
                    sc.Nb,
                    sc.Nbc,
                )
                continue
            detailed_sub_categories[(sc.Nbc, sc.Nb)] = DetailedSubCategory(
                Nbc=parent_category, Nb=sc.Nb, Na=sc.Na
            )
    payment_methods: dict[int, Payment] = (
        {p.Number: p for p in gsb_file.payment_methods} if gsb_file.payment_methods else {}
    )
    detailed_accounts: dict[int, DetailedAccount] = {}
    if gsb_file.accounts:
        for a in gsb_file.accounts:
            currency = currencies.get(a.Currency)
            if currency is None:
                _log.warning("Account %d: currency %d not found — skipping", a.Number, a.Currency)
                continue
            detailed_accounts[a.Number] = DetailedAccount(
                Name=a.Name,
                Id=a.Id,
                Number=a.Number,
                Owner=a.Owner,
                Kind=a.Kind,
                Currency=currency,
                Path_icon=a.Path_icon,
                Bank=banks.get(a.Bank) if a.Bank != 0 else None,
                Bank_branch_code=a.Bank_branch_code,
                Bank_account_number=a.Bank_account_number,
                Key=a.Key,
                Bank_account_IBAN=a.Bank_account_IBAN,
                Initial_balance=a.Initial_balance,
                Minimum_wanted_balance=a.Minimum_wanted_balance,
                Minimum_authorised_balance=a.Minimum_authorised_balance,
                Closed_account=a.Closed_account,
                Show_marked=a.Show_marked,
                Show_archives_lines=a.Show_archives_lines,
                Lines_per_transaction=a.Lines_per_transaction,
                Comment=a.Comment,
                Owner_address=a.Owner_address,
                Default_debit_method=(
                    payment_methods.get(a.Default_debit_method)
                    if a.Default_debit_method != 0
                    else None
                ),
                Default_credit_method=(
                    payment_methods.get(a.Default_credit_method)
                    if a.Default_credit_method != 0
                    else None
                ),
                Sort_by_method=a.Sort_by_method,
                Neutrals_inside_method=a.Neutrals_inside_method,
                Sort_order=a.Sort_order,
                Ascending_sort=a.Ascending_sort,
                Column_sort=a.Column_sort,
                Sorting_kind_column=a.Sorting_kind_column,
                Bet_use_budget=a.Bet_use_budget,
            )
    detailed_reconciles: dict[int, DetailedReconcile] = {}
    if gsb_file.reconciles:
        for r in gsb_file.reconciles:
            acc = accounts.get(r.Acc)
            if acc is None:
                _log.warning("Reconcile %d: account %d not found — skipping", r.Nb, r.Acc)
                continue
            detailed_reconciles[r.Nb] = DetailedReconcile(
                Nb=r.Nb,
                Na=r.Na,
                Acc=acc,
                Idate=r.Idate,
                Fdate=r.Fdate,
                Ibal=r.Ibal,
                Fbal=r.Fbal,
            )
    financial_years: dict[int, FinancialYear] = (
        {f.Nb: f for f in gsb_file.financial_years} if gsb_file.financial_years else {}
    )
    budgetaries: dict[int, Budgetary] = (
        {b.Nb: b for b in gsb_file.budgetaries} if gsb_file.budgetaries else {}
    )
    # Keyed by (parent_budgetary_nb, sub_budgetary_nb) to disambiguate shared Nb values.
    detailed_sub_budgetaries: dict[tuple[int, int], DetailedSubBudgetary] = {}
    if gsb_file.sub_budgetaries:
        for sb in gsb_file.sub_budgetaries:
            parent_budgetary = budgetaries.get(sb.Nbb)
            if parent_budgetary is None:
                _log.warning(
                    "SubBudgetary %d (parent=%d): parent budgetary not found — skipping",
                    sb.Nb,
                    sb.Nbb,
                )
                continue
            detailed_sub_budgetaries[(sb.Nbb, sb.Nb)] = DetailedSubBudgetary(
                Nbb=parent_budgetary, Nb=sb.Nb, Na=sb.Na
            )

    # Pass 1 — build every DetailedTransaction with Trt=None and record the raw Trt value.
    # Keyed by transaction Nb, which is globally unique across the file.
    pass1: dict[int, DetailedTransaction] = {}
    raw_trt: dict[int, int] = {}

    for tx in gsb_file.transactions:
        account = detailed_accounts.get(tx.Ac)
        if account is None:
            _log.warning("Transaction %d: account %d not found — skipping", tx.Nb, tx.Ac)
            continue

        currency = currencies.get(tx.Cu)
        if currency is None:
            _log.warning("Transaction %d: currency %d not found — skipping", tx.Nb, tx.Cu)
            continue

        dt = DetailedTransaction(
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
            Sca=detailed_sub_categories.get((tx.Ca, tx.Sca)) if tx.Sca != 0 else None,
            Pn=payment_methods.get(tx.Pn) if tx.Pn != 0 else None,
            Re=detailed_reconciles.get(tx.Re) if tx.Re != 0 else None,
            Fi=financial_years.get(tx.Fi) if tx.Fi not in (0, -1, -2) else None,
            Bu=budgetaries.get(tx.Bu) if tx.Bu != 0 else None,
            Sbu=detailed_sub_budgetaries.get((tx.Bu, tx.Sbu)) if tx.Sbu != 0 else None,
            Trt=None,
        )
        pass1[tx.Nb] = dt
        raw_trt[tx.Nb] = tx.Trt

    # Pass 2 — resolve Trt: each transfer points to the pass-1 object of its contra
    # (which has Trt=None), preventing infinite nesting.
    result = [
        dataclasses.replace(dt, Trt=pass1.get(raw_trt[nb])) if raw_trt[nb] != 0 else dt
        for nb, dt in pass1.items()
    ]

    return result if result else None
