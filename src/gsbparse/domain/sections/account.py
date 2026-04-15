"""Domain section: Account."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gsbparse.domain.sections.bank import BankSection
    from gsbparse.domain.sections.currency import CurrencySection
    from gsbparse.domain.sections.payment import PaymentSection

from gsbparse.domain.sections._base import GsbFileSection


class AccountKind(IntEnum):
    """Account kind as stored in the ``Kind`` attribute of an ``<Account>`` element."""

    BANK = 0
    CASH = 1
    LIABILITIES = 2
    ASSETS = 3


@dataclass(frozen=True)
class AccountSection(GsbFileSection):
    """A bank or cash account defined in the Grisbi file.

    Budget-estimate fields (``Bet_*``) are present only when
    ``Bet_use_budget >= 1``; they are ``None`` otherwise.

    Attributes:
        Name: Account display name.
        Id: OFX account identifier (nullable).
        Number: Account number (internal).
        Owner: Account holder name.
        Kind: Account kind (checking / cash / liability / asset).
        Currency: Currency identifier.
        Path_icon: Path to the account icon file.
        Bank: Bank identifier (0 = none).
        Bank_branch_code: Bank branch code.
        Bank_account_number: Bank account number string.
        Key: Account key / check digit.
        Bank_account_IBAN: IBAN string.
        Initial_balance: Opening balance.
        Minimum_wanted_balance: Target minimum balance.
        Minimum_authorised_balance: Authorised overdraft limit.
        Closed_account: Account is closed.
        Show_marked: Show only marked transactions by default.
        Show_archives_lines: Show archived transaction lines.
        Lines_per_transaction: Number of display lines per transaction.
        Comment: Free-text comment.
        Owner_address: Account holder address.
        Default_debit_method: Default payment method for debits.
        Default_credit_method: Default payment method for credits.
        Sort_by_method: Sort transactions by payment method.
        Neutrals_inside_method: Group neutral transactions inside method sort.
        Sort_order: Sort order specification string.
        Ascending_sort: Sort ascending.
        Column_sort: Column index used for sorting.
        Sorting_kind_column: Column-sort kind specification string.
        Bet_use_budget: Budget-estimate enabled (0 = off, ≥1 = on).
    """

    Name: str
    Id: str | None
    Number: int
    Owner: str
    Kind: AccountKind
    Currency: int
    Path_icon: str
    Bank: int
    Bank_branch_code: str
    Bank_account_number: str
    Key: str
    Bank_account_IBAN: str
    Initial_balance: Decimal
    Minimum_wanted_balance: Decimal
    Minimum_authorised_balance: Decimal
    Closed_account: bool
    Show_marked: bool
    Show_archives_lines: bool
    Lines_per_transaction: int
    Comment: str
    Owner_address: str
    Default_debit_method: int
    Default_credit_method: int
    Sort_by_method: bool
    Neutrals_inside_method: bool
    Sort_order: str
    Ascending_sort: bool
    Column_sort: int
    Sorting_kind_column: str
    Bet_use_budget: int


@dataclass(frozen=True)
class DetailedAccountSection(GsbFileSection):
    """An account with its currency, bank, and payment methods resolved.

    All fields mirror :class:`AccountSection` except the three FK integer fields
    which are replaced by their resolved domain objects.

    Attributes:
        Name: Account display name.
        Id: OFX account identifier (nullable).
        Number: Account number (internal).
        Owner: Account holder name.
        Kind: Account kind (checking / cash / liability / asset).
        Currency: Currency of this account (resolved from the raw ``Currency`` identifier).
        Path_icon: Path to the account icon file.
        Bank: Bank of this account (resolved; ``None`` when no bank is set).
        Bank_branch_code: Bank branch code.
        Bank_account_number: Bank account number string.
        Key: Account key / check digit.
        Bank_account_IBAN: IBAN string.
        Initial_balance: Opening balance.
        Minimum_wanted_balance: Target minimum balance.
        Minimum_authorised_balance: Authorised overdraft limit.
        Closed_account: Account is closed.
        Show_marked: Show only marked transactions by default.
        Show_archives_lines: Show archived transaction lines.
        Lines_per_transaction: Number of display lines per transaction.
        Comment: Free-text comment.
        Owner_address: Account holder address.
        Default_debit_method: Default payment method for debits (resolved; ``None`` when unset).
        Default_credit_method: Default payment method for credits (resolved; ``None`` when unset).
        Sort_by_method: Sort transactions by payment method.
        Neutrals_inside_method: Group neutral transactions inside method sort.
        Sort_order: Sort order specification string.
        Ascending_sort: Sort ascending.
        Column_sort: Column index used for sorting.
        Sorting_kind_column: Column-sort kind specification string.
        Bet_use_budget: Budget-estimate enabled (0 = off, ≥1 = on).
    """

    Name: str
    Id: str | None
    Number: int
    Owner: str
    Kind: AccountKind
    Currency: CurrencySection
    Path_icon: str
    Bank: BankSection | None
    Bank_branch_code: str
    Bank_account_number: str
    Key: str
    Bank_account_IBAN: str
    Initial_balance: Decimal
    Minimum_wanted_balance: Decimal
    Minimum_authorised_balance: Decimal
    Closed_account: bool
    Show_marked: bool
    Show_archives_lines: bool
    Lines_per_transaction: int
    Comment: str
    Owner_address: str
    Default_debit_method: PaymentSection | None
    Default_credit_method: PaymentSection | None
    Sort_by_method: bool
    Neutrals_inside_method: bool
    Sort_order: str
    Ascending_sort: bool
    Column_sort: int
    Sorting_kind_column: str
    Bet_use_budget: int
