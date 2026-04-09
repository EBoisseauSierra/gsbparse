"""Domain aggregate: GsbFile."""

from dataclasses import dataclass

from gsbparse.domain.sections.account import AccountSection
from gsbparse.domain.sections.amount_comparison import AmountComparisonSection
from gsbparse.domain.sections.archive import ArchiveSection
from gsbparse.domain.sections.bank import BankSection
from gsbparse.domain.sections.bet import BetSection
from gsbparse.domain.sections.bet_future import BetFutureSection
from gsbparse.domain.sections.bet_graph import BetGraphSection
from gsbparse.domain.sections.bet_historical import BetHistoricalSection
from gsbparse.domain.sections.bet_loan import BetLoanSection
from gsbparse.domain.sections.bet_transfert import BetTransfertSection
from gsbparse.domain.sections.budgetary import BudgetarySection
from gsbparse.domain.sections.category import CategorySection
from gsbparse.domain.sections.currency import CurrencySection
from gsbparse.domain.sections.currency_link import CurrencyLinkSection
from gsbparse.domain.sections.financial_year import FinancialYearSection
from gsbparse.domain.sections.general import GeneralSection
from gsbparse.domain.sections.import_rule import ImportRuleSection
from gsbparse.domain.sections.partial_balance import PartialBalanceSection
from gsbparse.domain.sections.party import PartySection
from gsbparse.domain.sections.payment import PaymentSection
from gsbparse.domain.sections.print import PrintSection
from gsbparse.domain.sections.reconcile import ReconcileSection
from gsbparse.domain.sections.report import ReportSection
from gsbparse.domain.sections.rgba import RgbaSection
from gsbparse.domain.sections.scheduled import ScheduledSection
from gsbparse.domain.sections.special_line import SpecialLineSection
from gsbparse.domain.sections.sub_budgetary import SubBudgetarySection
from gsbparse.domain.sections.sub_category import SubCategorySection
from gsbparse.domain.sections.text_comparison import TextComparisonSection
from gsbparse.domain.sections.transaction import TransactionSection


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

    general: GeneralSection | None
    rgba: RgbaSection | None
    print_settings: PrintSection | None
    currencies: list[CurrencySection] | None
    accounts: list[AccountSection] | None
    banks: list[BankSection] | None
    parties: list[PartySection] | None
    payment_methods: list[PaymentSection] | None
    transactions: list[TransactionSection] | None
    scheduled: list[ScheduledSection] | None
    categories: list[CategorySection] | None
    sub_categories: list[SubCategorySection] | None
    budgetaries: list[BudgetarySection] | None
    sub_budgetaries: list[SubBudgetarySection] | None
    currency_links: list[CurrencyLinkSection] | None
    financial_years: list[FinancialYearSection] | None
    archives: list[ArchiveSection] | None
    reconciles: list[ReconcileSection] | None
    import_rules: list[ImportRuleSection] | None
    special_lines: list[SpecialLineSection] | None
    partial_balances: list[PartialBalanceSection] | None
    bet: BetSection | None
    bet_graphs: list[BetGraphSection] | None
    bet_historicals: list[BetHistoricalSection] | None
    bet_futures: list[BetFutureSection] | None
    bet_transferts: list[BetTransfertSection] | None
    bet_loans: list[BetLoanSection] | None
    reports: list[ReportSection] | None
    text_comparisons: list[TextComparisonSection] | None
    amount_comparisons: list[AmountComparisonSection] | None
