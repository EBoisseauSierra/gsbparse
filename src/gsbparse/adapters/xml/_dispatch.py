"""Dispatch table mapping Grisbi XML tag names to section parser functions."""

import xml.etree.ElementTree as ET
from collections.abc import Callable

from gsbparse.adapters.xml.sections.account import parse_account_section
from gsbparse.adapters.xml.sections.amount_comparison import parse_amount_comparison_section
from gsbparse.adapters.xml.sections.archive import parse_archive_section
from gsbparse.adapters.xml.sections.bank import parse_bank_section
from gsbparse.adapters.xml.sections.bet import parse_bet_section
from gsbparse.adapters.xml.sections.bet_future import parse_bet_future_section
from gsbparse.adapters.xml.sections.bet_graph import parse_bet_graph_section
from gsbparse.adapters.xml.sections.bet_historical import parse_bet_historical_section
from gsbparse.adapters.xml.sections.bet_loan import parse_bet_loan_section
from gsbparse.adapters.xml.sections.bet_transfert import parse_bet_transfert_section
from gsbparse.adapters.xml.sections.budgetary import parse_budgetary_section
from gsbparse.adapters.xml.sections.category import parse_category_section
from gsbparse.adapters.xml.sections.currency import parse_currency_section
from gsbparse.adapters.xml.sections.currency_link import parse_currency_link_section
from gsbparse.adapters.xml.sections.financial_year import parse_financial_year_section
from gsbparse.adapters.xml.sections.general import parse_general_section
from gsbparse.adapters.xml.sections.import_rule import parse_import_rule_section
from gsbparse.adapters.xml.sections.partial_balance import parse_partial_balance_section
from gsbparse.adapters.xml.sections.party import parse_party_section
from gsbparse.adapters.xml.sections.payment import parse_payment_section
from gsbparse.adapters.xml.sections.print import parse_print_section
from gsbparse.adapters.xml.sections.reconcile import parse_reconcile_section
from gsbparse.adapters.xml.sections.report import parse_report_section
from gsbparse.adapters.xml.sections.rgba import parse_rgba_section
from gsbparse.adapters.xml.sections.scheduled import parse_scheduled_section
from gsbparse.adapters.xml.sections.special_line import parse_special_line_section
from gsbparse.adapters.xml.sections.sub_budgetary import parse_sub_budgetary_section
from gsbparse.adapters.xml.sections.sub_category import parse_sub_category_section
from gsbparse.adapters.xml.sections.text_comparison import parse_text_comparison_section
from gsbparse.adapters.xml.sections.transaction import parse_transaction_section
from gsbparse.domain.sections._base import GsbFileSection

#: Maps each Grisbi XML tag to the function that parses it into a domain section.
ELEMENT_TAG_TO_PARSER: dict[str, Callable[[ET.Element], GsbFileSection]] = {
    "General": parse_general_section,
    "RGBA": parse_rgba_section,
    "Print": parse_print_section,
    "Currency": parse_currency_section,
    "Account": parse_account_section,
    "Bank": parse_bank_section,
    "Party": parse_party_section,
    "Payment": parse_payment_section,
    "Transaction": parse_transaction_section,
    "Scheduled": parse_scheduled_section,
    "Category": parse_category_section,
    "Sub_category": parse_sub_category_section,
    "Budgetary": parse_budgetary_section,
    "Sub_budgetary": parse_sub_budgetary_section,
    "Currency_link": parse_currency_link_section,
    "Financial_year": parse_financial_year_section,
    "Archive": parse_archive_section,
    "Reconcile": parse_reconcile_section,
    "Import_rule": parse_import_rule_section,
    "Special_line": parse_special_line_section,
    "Partial_balance": parse_partial_balance_section,
    "Bet": parse_bet_section,
    "Bet_graph": parse_bet_graph_section,
    "Bet_historical": parse_bet_historical_section,
    "Bet_future": parse_bet_future_section,
    "Bet_transfert": parse_bet_transfert_section,
    "Bet_loan": parse_bet_loan_section,
    "Report": parse_report_section,
    "Text_comparison": parse_text_comparison_section,
    "Amount_comparison": parse_amount_comparison_section,
}
