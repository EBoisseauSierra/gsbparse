"""gsbparse — parse Grisbi .gsb files into typed domain objects and pandas DataFrames.

Quick start::

    import gsbparse

    gsb = gsbparse.read_gsb("my_accounts.gsb")
    for tx in gsb.detailed_transactions:
        print(tx.Ac.Name, tx.Am)

See Also:
    :func:`gsbparse.pandas.to_df` — convert sections or detailed transactions
    to a ``pd.DataFrame``.
"""

from gsbparse.adapters.xml.reader import read_gsb_file as read_gsb
from gsbparse.domain.detailed_transaction import (
    DEFAULT_DETAILED_TRANSACTION_COLUMNS,
    DetailedTransaction,
    DetailedTransactionColumn,
)
from gsbparse.domain.errors import (
    GsbParseError,
    InvalidElementCountError,
    InvalidGsbFileError,
    InvalidGsbFileRootError,
    MixedSectionsError,
    SectionNotFoundError,
    UnknownDetailedTransactionPathError,
    XmlParsingError,
)
from gsbparse.domain.file import GsbFile
from gsbparse.domain.sections import (
    Account,
    AccountKind,
    AmountComparison,
    Archive,
    Bank,
    Bet,
    BetDataOrigin,
    BetFuture,
    BetGraph,
    BetHistorical,
    BetLoan,
    BetTransfert,
    BetTransfertAccountType,
    Budgetary,
    Category,
    CategoryKind,
    Currency,
    CurrencyLink,
    DetailedAccount,
    DetailedReconcile,
    DetailedSubBudgetary,
    DetailedSubCategory,
    FinancialYear,
    General,
    GsbFileSection,
    ImportRule,
    PartialBalance,
    Party,
    Payment,
    Print,
    Reconcile,
    Report,
    Rgba,
    Scheduled,
    SpecialLine,
    SpecialLineAction,
    SubBudgetary,
    SubCategory,
    TextComparison,
    Transaction,
    TransactionMarkedState,
)

__all__ = [
    # Top-level entry point
    "read_gsb",
    # Aggregate
    "GsbFile",
    # Detailed transactions
    "DetailedTransaction",
    "DetailedTransactionColumn",
    "DEFAULT_DETAILED_TRANSACTION_COLUMNS",
    # Section types and their enums
    "GsbFileSection",
    "AccountKind",
    "Account",
    "AmountComparison",
    "Archive",
    "Bank",
    "BetDataOrigin",
    "Bet",
    "BetFuture",
    "BetGraph",
    "BetHistorical",
    "BetLoan",
    "BetTransfertAccountType",
    "BetTransfert",
    "Budgetary",
    "CategoryKind",
    "Category",
    "Currency",
    "CurrencyLink",
    "DetailedAccount",
    "DetailedReconcile",
    "DetailedSubBudgetary",
    "DetailedSubCategory",
    "FinancialYear",
    "General",
    "ImportRule",
    "PartialBalance",
    "Party",
    "Payment",
    "Print",
    "Reconcile",
    "Report",
    "Rgba",
    "Scheduled",
    "SpecialLineAction",
    "SpecialLine",
    "SubBudgetary",
    "SubCategory",
    "TextComparison",
    "TransactionMarkedState",
    "Transaction",
    # Errors
    "GsbParseError",
    "InvalidElementCountError",
    "InvalidGsbFileError",
    "InvalidGsbFileRootError",
    "MixedSectionsError",
    "SectionNotFoundError",
    "UnknownDetailedTransactionPathError",
    "XmlParsingError",
]
