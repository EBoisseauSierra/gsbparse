from dataclasses import dataclass
from datetime import date
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse2.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class ReportSection(GsbFileSection):
    Nb: int
    Name: str
    Compl_name_function: int
    Compl_name_position: int
    Compl_name_used: int
    General_sort_type: str
    Show_r: bool
    Show_transaction: bool
    Show_transaction_amount: bool
    Show_transaction_nb: bool
    Show_transaction_date: bool
    Show_transaction_payee: bool
    Show_transaction_categ: bool
    Show_transaction_sub_categ: bool
    Show_transaction_payment: bool
    Show_transaction_budget: bool
    Show_transaction_sub_budget: bool
    Show_transaction_chq: bool
    Show_transaction_note: bool
    Show_transaction_voucher: bool
    Show_transaction_reconcile: bool
    Show_transaction_bank: bool
    Show_transaction_fin_year: bool
    Show_transaction_sort_type: bool
    Show_columns_titles: bool
    Show_title_column_kind: bool
    Show_exclude_breakdown_child: bool
    Show_split_amounts: bool
    Currency_general: int
    Report_in_payees: bool
    Report_can_click: bool
    Financial_year_used: int
    Financial_year_kind: int
    Financial_year_select: int
    Date_kind: int
    Date_begining: date
    Date_end: date
    Split_by_date: bool
    Split_date_period: int
    Split_by_fin_year: bool
    Split_day_begining: bool
    Account_use_selection: bool
    Account_selected: str
    Account_group_transactions: bool
    Account_show_amount: bool
    Account_show_name: bool
    Transfer_kind: int
    Transfer_selected_accounts: str
    Transfer_exclude_transactions: bool
    Categ_use: bool
    Categ_use_selection: str
    Categ_selected: str
    Categ_exclude_transactions: bool
    Categ_show_amount: bool
    Categ_show_sub_categ: bool
    Categ_show_without_sub_categ: bool
    Categ_show_sub_categ_amount: bool
    Categ_currency: int
    Categ_show_name: bool
    Budget_use: bool
    Budget_use_selection: str
    Budget_selected: str
    Budget_exclude_transactions: bool
    Budget_show_amount: bool
    Budget_show_sub_budget: bool
    Budget_show_without_sub_budget: bool
    Budget_show_sub_budget_amount: bool
    Budget_currency: int
    Budget_show_name: bool
    Payee_use: bool
    Payee_use_selection: bool
    Payee_selected: str
    Payee_show_amount: bool
    Payee_currency: int
    Payee_show_name: bool
    Amount_currency: int
    Amount_exclude_null: bool
    Payment_method_list: str
    Use_text: bool
    Use_amount: bool

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Nb=cls.parse_int(element.attrib.get("Nb")),
            Name=cls.parse_str(element.attrib.get("Name")),
            Compl_name_function=cls.parse_int(
                element.attrib.get("Compl_name_function")
            ),
            Compl_name_position=cls.parse_int(
                element.attrib.get("Compl_name_position")
            ),
            Compl_name_used=cls.parse_int(element.attrib.get("Compl_name_used")),
            General_sort_type=cls.parse_str(element.attrib.get("General_sort_type")),
            Show_r=cls.parse_bool(element.attrib.get("Show_r")),
            Show_transaction=cls.parse_bool(element.attrib.get("Show_transaction")),
            Show_transaction_amount=cls.parse_bool(
                element.attrib.get("Show_transaction_amount")
            ),
            Show_transaction_nb=cls.parse_bool(
                element.attrib.get("Show_transaction_nb")
            ),
            Show_transaction_date=cls.parse_bool(
                element.attrib.get("Show_transaction_date")
            ),
            Show_transaction_payee=cls.parse_bool(
                element.attrib.get("Show_transaction_payee")
            ),
            Show_transaction_categ=cls.parse_bool(
                element.attrib.get("Show_transaction_categ")
            ),
            Show_transaction_sub_categ=cls.parse_bool(
                element.attrib.get("Show_transaction_sub_categ")
            ),
            Show_transaction_payment=cls.parse_bool(
                element.attrib.get("Show_transaction_payment")
            ),
            Show_transaction_budget=cls.parse_bool(
                element.attrib.get("Show_transaction_budget")
            ),
            Show_transaction_sub_budget=cls.parse_bool(
                element.attrib.get("Show_transaction_sub_budget")
            ),
            Show_transaction_chq=cls.parse_bool(
                element.attrib.get("Show_transaction_chq")
            ),
            Show_transaction_note=cls.parse_bool(
                element.attrib.get("Show_transaction_note")
            ),
            Show_transaction_voucher=cls.parse_bool(
                element.attrib.get("Show_transaction_voucher")
            ),
            Show_transaction_reconcile=cls.parse_bool(
                element.attrib.get("Show_transaction_reconcile")
            ),
            Show_transaction_bank=cls.parse_bool(
                element.attrib.get("Show_transaction_bank")
            ),
            Show_transaction_fin_year=cls.parse_bool(
                element.attrib.get("Show_transaction_fin_year")
            ),
            Show_transaction_sort_type=cls.parse_bool(
                element.attrib.get("Show_transaction_sort_type")
            ),
            Show_columns_titles=cls.parse_bool(
                element.attrib.get("Show_columns_titles")
            ),
            Show_title_column_kind=cls.parse_bool(
                element.attrib.get("Show_title_column_kind")
            ),
            Show_exclude_breakdown_child=cls.parse_bool(
                element.attrib.get("Show_exclude_breakdown_child"), is_optional=True
            ),
            Show_split_amounts=cls.parse_bool(element.attrib.get("Show_split_amounts")),
            Currency_general=cls.parse_int(element.attrib.get("Currency_general")),
            Report_in_payees=cls.parse_bool(element.attrib.get("Report_in_payees")),
            Report_can_click=cls.parse_bool(element.attrib.get("Report_can_click")),
            Financial_year_used=cls.parse_int(
                element.attrib.get("Financial_year_used")
            ),
            Financial_year_kind=cls.parse_int(
                element.attrib.get("Financial_year_kind")
            ),
            Financial_year_select=cls.parse_int(
                element.attrib.get("Financial_year_select")
            ),
            Date_kind=cls.parse_int(element.attrib.get("Date_kind")),
            Date_begining=cls.parse_date(
                element.attrib.get("Date_begining"), is_optional=True
            ),
            Date_end=cls.parse_date(element.attrib.get("Date_end"), is_optional=True),
            Split_by_date=cls.parse_bool(element.attrib.get("Split_by_date")),
            Split_date_period=cls.parse_int(element.attrib.get("Split_date_period")),
            Split_by_fin_year=cls.parse_bool(element.attrib.get("Split_by_fin_year")),
            Split_day_begining=cls.parse_bool(
                element.attrib.get("Split_day_begining"), is_optional=True
            ),
            Account_use_selection=cls.parse_bool(
                element.attrib.get("Account_use_selection")
            ),
            Account_selected=cls.parse_str(element.attrib.get("Account_selected")),
            Account_group_transactions=cls.parse_bool(
                element.attrib.get("Account_group_transactions")
            ),
            Account_show_amount=cls.parse_bool(
                element.attrib.get("Account_show_amount")
            ),
            Account_show_name=cls.parse_bool(element.attrib.get("Account_show_name")),
            Transfer_kind=cls.parse_int(element.attrib.get("Transfer_kind")),
            Transfer_selected_accounts=cls.parse_str(
                element.attrib.get("Transfer_selected_accounts"), is_optional=True
            ),
            Transfer_exclude_transactions=cls.parse_bool(
                element.attrib.get("Transfer_exclude_transactions"), is_optional=True
            ),
            Categ_use=cls.parse_bool(element.attrib.get("Categ_use")),
            Categ_use_selection=cls.parse_str(
                element.attrib.get("Categ_use_selection")
            ),
            Categ_selected=cls.parse_str(element.attrib.get("Categ_selected")),
            Categ_exclude_transactions=cls.parse_bool(
                element.attrib.get("Categ_exclude_transactions"), is_optional=True
            ),
            Categ_show_amount=cls.parse_bool(element.attrib.get("Categ_show_amount")),
            Categ_show_sub_categ=cls.parse_bool(
                element.attrib.get("Categ_show_sub_categ")
            ),
            Categ_show_without_sub_categ=cls.parse_bool(
                element.attrib.get("Categ_show_without_sub_categ")
            ),
            Categ_show_sub_categ_amount=cls.parse_bool(
                element.attrib.get("Categ_show_sub_categ_amount")
            ),
            Categ_currency=cls.parse_int(element.attrib.get("Categ_currency")),
            Categ_show_name=cls.parse_bool(element.attrib.get("Categ_show_name")),
            Budget_use=cls.parse_bool(element.attrib.get("Budget_use")),
            Budget_use_selection=cls.parse_str(
                element.attrib.get("Budget_use_selection")
            ),
            Budget_selected=cls.parse_str(element.attrib.get("Budget_selected")),
            Budget_exclude_transactions=cls.parse_bool(
                element.attrib.get("Budget_exclude_transactions"), is_optional=True
            ),
            Budget_show_amount=cls.parse_bool(element.attrib.get("Budget_show_amount")),
            Budget_show_sub_budget=cls.parse_bool(
                element.attrib.get("Budget_show_sub_budget")
            ),
            Budget_show_without_sub_budget=cls.parse_bool(
                element.attrib.get("Budget_show_without_sub_budget")
            ),
            Budget_show_sub_budget_amount=cls.parse_bool(
                element.attrib.get("Budget_show_sub_budget_amount")
            ),
            Budget_currency=cls.parse_int(element.attrib.get("Budget_currency")),
            Budget_show_name=cls.parse_bool(element.attrib.get("Budget_show_name")),
            Payee_use=cls.parse_bool(element.attrib.get("Payee_use")),
            Payee_use_selection=cls.parse_bool(
                element.attrib.get("Payee_use_selection")
            ),
            Payee_selected=cls.parse_str(element.attrib.get("Payee_selected")),
            Payee_show_amount=cls.parse_bool(element.attrib.get("Payee_show_amount")),
            Payee_currency=cls.parse_int(element.attrib.get("Payee_currency")),
            Payee_show_name=cls.parse_bool(element.attrib.get("Payee_show_name")),
            Amount_currency=cls.parse_int(element.attrib.get("Amount_currency")),
            Amount_exclude_null=cls.parse_bool(
                element.attrib.get("Amount_exclude_null")
            ),
            Payment_method_list=cls.parse_str(
                element.attrib.get("Payment_method_list")
            ),
            Use_text=cls.parse_bool(element.attrib.get("Use_text")),
            Use_amount=cls.parse_bool(element.attrib.get("Use_amount")),
        )
