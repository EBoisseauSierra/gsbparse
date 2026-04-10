"""XML adapter: read a ``.gsb`` file into a :class:`~gsbparse.domain.file.GsbFile`."""

from __future__ import annotations

import logging
from pathlib import Path

import defusedxml.ElementTree as ET

from gsbparse.adapters.xml._dispatch import ELEMENT_TAG_TO_PARSER
from gsbparse.domain.errors import InvalidGsbFileError, InvalidGsbFileRootError
from gsbparse.domain.file import GsbFile
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

_log = logging.getLogger(__name__)

_GSB_ROOT_TAG = "Grisbi"


def read_gsb_file(path: str | Path) -> GsbFile:
    """Parse a Grisbi ``.gsb`` file into a :class:`~gsbparse.domain.file.GsbFile`.

    The file must be a valid XML document whose root element is ``<Grisbi>``.
    Unknown element tags are logged at ``WARNING`` level and skipped — the
    parser is tolerant by design so that files from future Grisbi versions can
    still be read partially.

    Args:
        path: Filesystem path to the ``.gsb`` file.

    Returns:
        A fully populated :class:`~gsbparse.domain.file.GsbFile`.

    Raises:
        InvalidGsbFileError: The file cannot be parsed as XML.
        InvalidGsbFileRootError: The root element is not ``<Grisbi>``.
    """
    path = Path(path)
    try:
        tree = ET.parse(str(path))
    except ET.ParseError as exc:
        raise InvalidGsbFileError(f"Cannot parse {path} as XML: {exc}") from exc

    root = tree.getroot()
    if root.tag != _GSB_ROOT_TAG:
        raise InvalidGsbFileRootError(f"Expected root element <{_GSB_ROOT_TAG}>, got <{root.tag}>")

    # Collect parsed sections by type.
    general: GeneralSection | None = None
    rgba: RgbaSection | None = None
    print_settings: PrintSection | None = None
    currencies: list[CurrencySection] = []
    accounts: list[AccountSection] = []
    banks: list[BankSection] = []
    parties: list[PartySection] = []
    payment_methods: list[PaymentSection] = []
    transactions: list[TransactionSection] = []
    scheduled: list[ScheduledSection] = []
    categories: list[CategorySection] = []
    sub_categories: list[SubCategorySection] = []
    budgetaries: list[BudgetarySection] = []
    sub_budgetaries: list[SubBudgetarySection] = []
    currency_links: list[CurrencyLinkSection] = []
    financial_years: list[FinancialYearSection] = []
    archives: list[ArchiveSection] = []
    reconciles: list[ReconcileSection] = []
    import_rules: list[ImportRuleSection] = []
    special_lines: list[SpecialLineSection] = []
    partial_balances: list[PartialBalanceSection] = []
    bet: BetSection | None = None
    bet_graphs: list[BetGraphSection] = []
    bet_historicals: list[BetHistoricalSection] = []
    bet_futures: list[BetFutureSection] = []
    bet_transferts: list[BetTransfertSection] = []
    bet_loans: list[BetLoanSection] = []
    reports: list[ReportSection] = []
    text_comparisons: list[TextComparisonSection] = []
    amount_comparisons: list[AmountComparisonSection] = []

    for element in root:
        tag = element.tag
        parser = ELEMENT_TAG_TO_PARSER.get(tag)
        if parser is None:
            _log.warning("Unknown element tag <%s> — skipping", tag)
            continue

        section = parser(element)

        match section:
            case GeneralSection():
                general = section
            case RgbaSection():
                rgba = section
            case PrintSection():
                print_settings = section
            case CurrencySection():
                currencies.append(section)
            case AccountSection():
                accounts.append(section)
            case BankSection():
                banks.append(section)
            case PartySection():
                parties.append(section)
            case PaymentSection():
                payment_methods.append(section)
            case TransactionSection():
                transactions.append(section)
            case ScheduledSection():
                scheduled.append(section)
            case CategorySection():
                categories.append(section)
            case SubCategorySection():
                sub_categories.append(section)
            case BudgetarySection():
                budgetaries.append(section)
            case SubBudgetarySection():
                sub_budgetaries.append(section)
            case CurrencyLinkSection():
                currency_links.append(section)
            case FinancialYearSection():
                financial_years.append(section)
            case ArchiveSection():
                archives.append(section)
            case ReconcileSection():
                reconciles.append(section)
            case ImportRuleSection():
                import_rules.append(section)
            case SpecialLineSection():
                special_lines.append(section)
            case PartialBalanceSection():
                partial_balances.append(section)
            case BetSection():
                bet = section
            case BetGraphSection():
                bet_graphs.append(section)
            case BetHistoricalSection():
                bet_historicals.append(section)
            case BetFutureSection():
                bet_futures.append(section)
            case BetTransfertSection():
                bet_transferts.append(section)
            case BetLoanSection():
                bet_loans.append(section)
            case ReportSection():
                reports.append(section)
            case TextComparisonSection():
                text_comparisons.append(section)
            case AmountComparisonSection():
                amount_comparisons.append(section)

    def _none_if_empty[T](lst: list[T]) -> list[T] | None:
        return lst if lst else None

    return GsbFile(
        general=general,
        rgba=rgba,
        print_settings=print_settings,
        currencies=_none_if_empty(currencies),
        accounts=_none_if_empty(accounts),
        banks=_none_if_empty(banks),
        parties=_none_if_empty(parties),
        payment_methods=_none_if_empty(payment_methods),
        transactions=_none_if_empty(transactions),
        scheduled=_none_if_empty(scheduled),
        categories=_none_if_empty(categories),
        sub_categories=_none_if_empty(sub_categories),
        budgetaries=_none_if_empty(budgetaries),
        sub_budgetaries=_none_if_empty(sub_budgetaries),
        currency_links=_none_if_empty(currency_links),
        financial_years=_none_if_empty(financial_years),
        archives=_none_if_empty(archives),
        reconciles=_none_if_empty(reconciles),
        import_rules=_none_if_empty(import_rules),
        special_lines=_none_if_empty(special_lines),
        partial_balances=_none_if_empty(partial_balances),
        bet=bet,
        bet_graphs=_none_if_empty(bet_graphs),
        bet_historicals=_none_if_empty(bet_historicals),
        bet_futures=_none_if_empty(bet_futures),
        bet_transferts=_none_if_empty(bet_transferts),
        bet_loans=_none_if_empty(bet_loans),
        reports=_none_if_empty(reports),
        text_comparisons=_none_if_empty(text_comparisons),
        amount_comparisons=_none_if_empty(amount_comparisons),
    )
