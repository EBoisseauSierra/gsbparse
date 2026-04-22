"""XML adapter: read a ``.gsb`` file into a :class:`~gsbparse.domain.file.GsbFile`."""

from __future__ import annotations

import logging
from pathlib import Path

import defusedxml.ElementTree as ET

from gsbparse.adapters.xml._dispatch import ELEMENT_TAG_TO_PARSER
from gsbparse.domain.errors import InvalidGsbFileError, InvalidGsbFileRootError
from gsbparse.domain.file import GsbFile
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
    general: General | None = None
    rgba: Rgba | None = None
    print_settings: Print | None = None
    currencies: list[Currency] = []
    accounts: list[Account] = []
    banks: list[Bank] = []
    parties: list[Party] = []
    payment_methods: list[Payment] = []
    transactions: list[Transaction] = []
    scheduled: list[Scheduled] = []
    categories: list[Category] = []
    sub_categories: list[SubCategory] = []
    budgetaries: list[Budgetary] = []
    sub_budgetaries: list[SubBudgetary] = []
    currency_links: list[CurrencyLink] = []
    financial_years: list[FinancialYear] = []
    archives: list[Archive] = []
    reconciles: list[Reconcile] = []
    import_rules: list[ImportRule] = []
    special_lines: list[SpecialLine] = []
    partial_balances: list[PartialBalance] = []
    bet: Bet | None = None
    bet_graphs: list[BetGraph] = []
    bet_historicals: list[BetHistorical] = []
    bet_futures: list[BetFuture] = []
    bet_transferts: list[BetTransfert] = []
    bet_loans: list[BetLoan] = []
    reports: list[Report] = []
    text_comparisons: list[TextComparison] = []
    amount_comparisons: list[AmountComparison] = []

    for element in root:
        tag = element.tag
        parser = ELEMENT_TAG_TO_PARSER.get(tag)
        if parser is None:
            _log.warning("Unknown element tag <%s> — skipping", tag)
            continue

        section = parser(element)

        match section:
            case General():
                general = section
            case Rgba():
                rgba = section
            case Print():
                print_settings = section
            case Currency():
                currencies.append(section)
            case Account():
                accounts.append(section)
            case Bank():
                banks.append(section)
            case Party():
                parties.append(section)
            case Payment():
                payment_methods.append(section)
            case Transaction():
                transactions.append(section)
            case Scheduled():
                scheduled.append(section)
            case Category():
                categories.append(section)
            case SubCategory():
                sub_categories.append(section)
            case Budgetary():
                budgetaries.append(section)
            case SubBudgetary():
                sub_budgetaries.append(section)
            case CurrencyLink():
                currency_links.append(section)
            case FinancialYear():
                financial_years.append(section)
            case Archive():
                archives.append(section)
            case Reconcile():
                reconciles.append(section)
            case ImportRule():
                import_rules.append(section)
            case SpecialLine():
                special_lines.append(section)
            case PartialBalance():
                partial_balances.append(section)
            case Bet():
                bet = section
            case BetGraph():
                bet_graphs.append(section)
            case BetHistorical():
                bet_historicals.append(section)
            case BetFuture():
                bet_futures.append(section)
            case BetTransfert():
                bet_transferts.append(section)
            case BetLoan():
                bet_loans.append(section)
            case Report():
                reports.append(section)
            case TextComparison():
                text_comparisons.append(section)
            case AmountComparison():
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
