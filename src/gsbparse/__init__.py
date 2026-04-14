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
    AccountKind,
    AccountSection,
    AmountComparisonSection,
    ArchiveSection,
    BankSection,
    BetFutureSection,
    BetGraphSection,
    BetHistoricalSection,
    BetLoanSection,
    BetSection,
    BetTransfertSection,
    BudgetarySection,
    CategorySection,
    CurrencyLinkSection,
    CurrencySection,
    FinancialYearSection,
    GeneralSection,
    GsbFileSection,
    ImportRuleSection,
    PartialBalanceSection,
    PartySection,
    PaymentSection,
    PrintSection,
    ReconcileSection,
    ReportSection,
    RgbaSection,
    ScheduledSection,
    SpecialLineSection,
    SubBudgetarySection,
    SubCategorySection,
    TextComparisonSection,
    TransactionSection,
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
    # Section types
    "GsbFileSection",
    "AccountKind",
    "AccountSection",
    "AmountComparisonSection",
    "ArchiveSection",
    "BankSection",
    "BetSection",
    "BetFutureSection",
    "BetGraphSection",
    "BetHistoricalSection",
    "BetLoanSection",
    "BetTransfertSection",
    "BudgetarySection",
    "CategorySection",
    "CurrencySection",
    "CurrencyLinkSection",
    "FinancialYearSection",
    "GeneralSection",
    "ImportRuleSection",
    "PartialBalanceSection",
    "PartySection",
    "PaymentSection",
    "PrintSection",
    "ReconcileSection",
    "ReportSection",
    "RgbaSection",
    "ScheduledSection",
    "SpecialLineSection",
    "SubBudgetarySection",
    "SubCategorySection",
    "TextComparisonSection",
    "TransactionSection",
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
