"""Domain aggregate: GsbFile."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gsbparse.domain.detailed_transaction import DetailedTransaction

from gsbparse.domain.sections.account import Account
from gsbparse.domain.sections.amount_comparison import AmountComparison
from gsbparse.domain.sections.archive import Archive
from gsbparse.domain.sections.bank import Bank
from gsbparse.domain.sections.bet import Bet
from gsbparse.domain.sections.bet_future import BetFuture
from gsbparse.domain.sections.bet_graph import BetGraph
from gsbparse.domain.sections.bet_historical import BetHistorical
from gsbparse.domain.sections.bet_loan import BetLoan
from gsbparse.domain.sections.bet_transfert import BetTransfert
from gsbparse.domain.sections.budgetary import Budgetary
from gsbparse.domain.sections.category import Category
from gsbparse.domain.sections.currency import Currency
from gsbparse.domain.sections.currency_link import CurrencyLink
from gsbparse.domain.sections.financial_year import FinancialYear
from gsbparse.domain.sections.general import General
from gsbparse.domain.sections.import_rule import ImportRule
from gsbparse.domain.sections.partial_balance import PartialBalance
from gsbparse.domain.sections.party import Party
from gsbparse.domain.sections.payment import Payment
from gsbparse.domain.sections.print import Print
from gsbparse.domain.sections.reconcile import Reconcile
from gsbparse.domain.sections.report import Report
from gsbparse.domain.sections.rgba import Rgba
from gsbparse.domain.sections.scheduled import Scheduled
from gsbparse.domain.sections.special_line import SpecialLine
from gsbparse.domain.sections.sub_budgetary import SubBudgetary
from gsbparse.domain.sections.sub_category import SubCategory
from gsbparse.domain.sections.text_comparison import TextComparison
from gsbparse.domain.sections.transaction import Transaction


@dataclass(frozen=True)
class GsbFile:
    """The top-level aggregate for a parsed Grisbi ``.gsb`` file.

    Each field holds either:

    - ``None`` — the section is absent from the file (faithful distinction
      from an empty list, which means the section tag was present but empty).
    - A single typed object (singleton sections such as ``General``).
    - A ``list[SectionClass]`` (multi-entry sections).

    See Also:
        :func:`gsbparse.pandas.to_df` — convert sections or detailed
        transactions to a ``pd.DataFrame``.

        :attr:`detailed_transactions` — denormalized view with foreign keys
        resolved (added when ``DetailedTransaction`` is introduced).
    """

    general: General | None
    rgba: Rgba | None
    print_settings: Print | None
    currencies: list[Currency] | None
    accounts: list[Account] | None
    banks: list[Bank] | None
    parties: list[Party] | None
    payment_methods: list[Payment] | None
    transactions: list[Transaction] | None
    scheduled: list[Scheduled] | None
    categories: list[Category] | None
    sub_categories: list[SubCategory] | None
    budgetaries: list[Budgetary] | None
    sub_budgetaries: list[SubBudgetary] | None
    currency_links: list[CurrencyLink] | None
    financial_years: list[FinancialYear] | None
    archives: list[Archive] | None
    reconciles: list[Reconcile] | None
    import_rules: list[ImportRule] | None
    special_lines: list[SpecialLine] | None
    partial_balances: list[PartialBalance] | None
    bet: Bet | None
    bet_graphs: list[BetGraph] | None
    bet_historicals: list[BetHistorical] | None
    bet_futures: list[BetFuture] | None
    bet_transferts: list[BetTransfert] | None
    bet_loans: list[BetLoan] | None
    reports: list[Report] | None
    text_comparisons: list[TextComparison] | None
    amount_comparisons: list[AmountComparison] | None

    @property
    def detailed_transactions(self) -> list[DetailedTransaction] | None:
        """Transactions with all foreign keys resolved to domain objects.

        Returns ``None`` when the file contains no transactions.
        Accounts or currencies missing from the file cause the affected
        transaction to be skipped with a ``WARNING`` log entry.
        """
        from gsbparse.domain.detailed_transaction import build_detailed_transactions

        return build_detailed_transactions(self)
