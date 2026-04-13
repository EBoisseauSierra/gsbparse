"""XML adapter: parse a ``<Report>`` element into a ``ReportSection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_bool, parse_int, parse_nullable_str, parse_str
from gsbparse.domain.sections.report import ReportSection


def parse_report_section(element: ET.Element) -> ReportSection:
    """Parse a ``<Report>`` XML element into a :class:`ReportSection`.

    Args:
        element: The ``<Report>`` XML element.

    Returns:
        A fully populated :class:`ReportSection`.
    """
    a = element.attrib
    return ReportSection(
        Nb=parse_int(a["Nb"]),
        Name=parse_str(a["Name"]),
        Compl_name_function=parse_int(a["Compl_name_function"]),
        Compl_name_position=parse_int(a["Compl_name_position"]),
        Compl_name_used=parse_bool(a["Compl_name_used"]),
        General_sort_type=parse_str(a["General_sort_type"]),
        Show_r=parse_bool(a["Show_r"]),
        Show_transaction=parse_bool(a["Show_transaction"]),
        Show_transaction_amount=parse_bool(a["Show_transaction_amount"]),
        Show_transaction_nb=parse_bool(a["Show_transaction_nb"]),
        Show_transaction_date=parse_bool(a["Show_transaction_date"]),
        Show_transaction_payee=parse_bool(a["Show_transaction_payee"]),
        Show_transaction_categ=parse_bool(a["Show_transaction_categ"]),
        Show_transaction_sub_categ=parse_bool(a["Show_transaction_sub_categ"]),
        Show_transaction_payment=parse_bool(a["Show_transaction_payment"]),
        Show_transaction_budget=parse_bool(a["Show_transaction_budget"]),
        Show_transaction_sub_budget=parse_bool(a["Show_transaction_sub_budget"]),
        Show_transaction_chq=parse_bool(a["Show_transaction_chq"]),
        Show_transaction_note=parse_bool(a["Show_transaction_note"]),
        Show_transaction_voucher=parse_bool(a["Show_transaction_voucher"]),
        Show_transaction_reconcile=parse_bool(a["Show_transaction_reconcile"]),
        Show_transaction_bank=parse_bool(a["Show_transaction_bank"]),
        Show_transaction_fin_year=parse_bool(a["Show_transaction_fin_year"]),
        Show_transaction_sort_type=parse_bool(a["Show_transaction_sort_type"]),
        Show_columns_titles=parse_bool(a["Show_columns_titles"]),
        Show_title_column_kind=parse_bool(a["Show_title_column_kind"]),
        Show_exclude_split_child=parse_bool(a["Show_exclude_split_child"]),
        Show_split_amounts=parse_bool(a["Show_split_amounts"]),
        Currency_general=parse_int(a["Currency_general"]),
        Report_in_payees=parse_bool(a["Report_in_payees"]),
        Report_can_click=parse_bool(a["Report_can_click"]),
        Financial_year_used=parse_bool(a["Financial_year_used"]),
        Financial_year_kind=parse_int(a["Financial_year_kind"]),
        Financial_year_select=parse_nullable_str(a["Financial_year_select"]),
        Date_kind=parse_int(a["Date_kind"]),
        Date_beginning=parse_str(a["Date_beginning"]),
        Date_end=parse_str(a["Date_end"]),
        Split_by_date=parse_bool(a["Split_by_date"]),
        Split_date_period=parse_int(a["Split_date_period"]),
        Split_by_fin_year=parse_bool(a["Split_by_fin_year"]),
        Split_day_beginning=parse_int(a["Split_day_beginning"]),
        Account_use_selection=parse_bool(a["Account_use_selection"]),
        Account_selected=parse_nullable_str(a["Account_selected"]),
        Account_group_transactions=parse_bool(a["Account_group_transactions"]),
        Account_show_amount=parse_bool(a["Account_show_amount"]),
        Account_show_name=parse_bool(a["Account_show_name"]),
        Transfer_kind=parse_int(a["Transfer_kind"]),
        Transfer_selected_accounts=parse_nullable_str(a["Transfer_selected_accounts"]),
        Transfer_exclude_transactions=parse_bool(a["Transfer_exclude_transactions"]),
        Categ_use=parse_bool(a["Categ_use"]),
        Categ_use_selection=parse_bool(a["Categ_use_selection"]),
        Categ_selected=parse_nullable_str(a["Categ_selected"]),
        Categ_show_amount=parse_bool(a["Categ_show_amount"]),
        Categ_show_sub_categ=parse_bool(a["Categ_show_sub_categ"]),
        Categ_show_without_sub_categ=parse_bool(a["Categ_show_without_sub_categ"]),
        Categ_show_sub_categ_amount=parse_bool(a["Categ_show_sub_categ_amount"]),
        Categ_currency=parse_int(a["Categ_currency"]),
        Categ_show_name=parse_bool(a["Categ_show_name"]),
        Budget_use=parse_bool(a["Budget_use"]),
        Budget_use_selection=parse_bool(a["Budget_use_selection"]),
        Budget_selected=parse_nullable_str(a["Budget_selected"]),
        Budget_show_amount=parse_bool(a["Budget_show_amount"]),
        Budget_show_sub_budget=parse_bool(a["Budget_show_sub_budget"]),
        Budget_show_without_sub_budget=parse_bool(a["Budget_show_without_sub_budget"]),
        Budget_show_sub_budget_amount=parse_bool(a["Budget_show_sub_budget_amount"]),
        Budget_currency=parse_int(a["Budget_currency"]),
        Budget_show_name=parse_bool(a["Budget_show_name"]),
        Payee_use=parse_bool(a["Payee_use"]),
        Payee_use_selection=parse_bool(a["Payee_use_selection"]),
        Payee_selected=parse_nullable_str(a["Payee_selected"]),
        Payee_show_amount=parse_bool(a["Payee_show_amount"]),
        Payee_currency=parse_int(a["Payee_currency"]),
        Payee_show_name=parse_bool(a["Payee_show_name"]),
        Amount_currency=parse_int(a["Amount_currency"]),
        Amount_exclude_null=parse_bool(a["Amount_exclude_null"]),
        Payment_method_list=parse_nullable_str(a["Payment_method_list"]),
        Use_text=parse_bool(a["Use_text"]),
        Use_amount=parse_bool(a["Use_amount"]),
    )
