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
    Split_date_period: bool
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
            Nb=int(element.attrib["Nb"]),
            Name=element.attrib["Name"],
            Compl_name_function=int(element.attrib["Compl_name_function"]),
            Compl_name_position=int(element.attrib["Compl_name_position"]),
            Compl_name_used=int(element.attrib["Compl_name_used"]),
            General_sort_type=element.attrib["General_sort_type"],
            Show_r=cls.parse_bool(element.attrib["Show_r"]),
            Show_transaction=cls.parse_bool(element.attrib["Show_transaction"]),
            Show_transaction_amount=cls.parse_bool(
                element.attrib["Show_transaction_amount"]
            ),
            Show_transaction_nb=cls.parse_bool(element.attrib["Show_transaction_nb"]),
            Show_transaction_date=cls.parse_bool(
                element.attrib["Show_transaction_date"]
            ),
            Show_transaction_payee=cls.parse_bool(
                element.attrib["Show_transaction_payee"]
            ),
            Show_transaction_categ=cls.parse_bool(
                element.attrib["Show_transaction_categ"]
            ),
            Show_transaction_sub_categ=cls.parse_bool(
                element.attrib["Show_transaction_sub_categ"]
            ),
            Show_transaction_payment=cls.parse_bool(
                element.attrib["Show_transaction_payment"]
            ),
            Show_transaction_budget=cls.parse_bool(
                element.attrib["Show_transaction_budget"]
            ),
            Show_transaction_sub_budget=cls.parse_bool(
                element.attrib["Show_transaction_sub_budget"]
            ),
            Show_transaction_chq=cls.parse_bool(element.attrib["Show_transaction_chq"]),
            Show_transaction_note=cls.parse_bool(
                element.attrib["Show_transaction_note"]
            ),
            Show_transaction_voucher=cls.parse_bool(
                element.attrib["Show_transaction_voucher"]
            ),
            Show_transaction_reconcile=cls.parse_bool(
                element.attrib["Show_transaction_reconcile"]
            ),
            Show_transaction_bank=cls.parse_bool(
                element.attrib["Show_transaction_bank"]
            ),
            Show_transaction_fin_year=cls.parse_bool(
                element.attrib["Show_transaction_fin_year"]
            ),
            Show_transaction_sort_type=cls.parse_bool(
                element.attrib["Show_transaction_sort_type"]
            ),
            Show_columns_titles=cls.parse_bool(element.attrib["Show_columns_titles"]),
            Show_title_column_kind=cls.parse_bool(
                element.attrib["Show_title_column_kind"]
            ),
            Show_exclude_breakdown_child=cls.parse_bool(
                element.attrib["Show_exclude_breakdown_child"], is_optional=True
            ),
            Show_split_amounts=cls.parse_bool(element.attrib["Show_split_amounts"]),
            Currency_general=int(element.attrib["Currency_general"]),
            Report_in_payees=cls.parse_bool(element.attrib["Report_in_payees"]),
            Report_can_click=cls.parse_bool(element.attrib["Report_can_click"]),
            Financial_year_used=int(element.attrib["Financial_year_used"]),
            Financial_year_kind=int(element.attrib["Financial_year_kind"]),
            Financial_year_select=int(element.attrib["Financial_year_select"]),
            Date_kind=int(element.attrib["Date_kind"]),
            Date_begining=cls.parse_date(element.attrib["Date_begining"]),
            Date_end=cls.parse_date(element.attrib["Date_end"]),
            Split_by_date=cls.parse_bool(element.attrib["Split_by_date"]),
            Split_date_period=cls.parse_bool(element.attrib["Split_date_period"]),
            Split_by_fin_year=cls.parse_bool(element.attrib["Split_by_fin_year"]),
            Split_day_begining=cls.parse_bool(element.attrib["Split_day_begining"]),
            Account_use_selection=cls.parse_bool(
                element.attrib["Account_use_selection"]
            ),
            Account_selected=element.attrib["Account_selected"],
            Account_group_transactions=cls.parse_bool(
                element.attrib["Account_group_transactions"]
            ),
            Account_show_amount=cls.parse_bool(element.attrib["Account_show_amount"]),
            Account_show_name=cls.parse_bool(element.attrib["Account_show_name"]),
            Transfer_kind=int(element.attrib["Transfer_kind"]),
            Transfer_selected_accounts=element.attrib["Transfer_selected_accounts"],
            Transfer_exclude_transactions=cls.parse_bool(
                element.attrib["Transfer_exclude_transactions"]
            ),
            Categ_use=cls.parse_bool(element.attrib["Categ_use"]),
            Categ_use_selection=element.attrib["Categ_use_selection"],
            Categ_selected=element.attrib["Categ_selected"],
            Categ_exclude_transactions=cls.parse_bool(
                element.attrib["Categ_exclude_transactions"]
            ),
            Categ_show_amount=cls.parse_bool(element.attrib["Categ_show_amount"]),
            Categ_show_sub_categ=cls.parse_bool(element.attrib["Categ_show_sub_categ"]),
            Categ_show_without_sub_categ=cls.parse_bool(
                element.attrib["Categ_show_without_sub_categ"]
            ),
            Categ_show_sub_categ_amount=cls.parse_bool(
                element.attrib["Categ_show_sub_categ_amount"]
            ),
            Categ_currency=int(element.attrib["Categ_currency"]),
            Categ_show_name=cls.parse_bool(element.attrib["Categ_show_name"]),
            Budget_use=cls.parse_bool(element.attrib["Budget_use"]),
            Budget_use_selection=element.attrib["Budget_use_selection"],
            Budget_selected=element.attrib["Budget_selected"],
            Budget_exclude_transactions=cls.parse_bool(
                element.attrib["Budget_exclude_transactions"]
            ),
            Budget_show_amount=cls.parse_bool(element.attrib["Budget_show_amount"]),
            Budget_show_sub_budget=cls.parse_bool(
                element.attrib["Budget_show_sub_budget"]
            ),
            Budget_show_without_sub_budget=cls.parse_bool(
                element.attrib["Budget_show_without_sub_budget"]
            ),
            Budget_show_sub_budget_amount=cls.parse_bool(
                element.attrib["Budget_show_sub_budget_amount"]
            ),
            Budget_currency=int(element.attrib["Budget_currency"]),
            Budget_show_name=cls.parse_bool(element.attrib["Budget_show_name"]),
            Payee_use=cls.parse_bool(element.attrib["Payee_use"]),
            Payee_use_selection=cls.parse_bool(element.attrib["Payee_use_selection"]),
            Payee_selected=element.attrib["Payee_selected"],
            Payee_show_amount=cls.parse_bool(element.attrib["Payee_show_amount"]),
            Payee_currency=int(element.attrib["Payee_currency"]),
            Payee_show_name=cls.parse_bool(element.attrib["Payee_show_name"]),
            Amount_currency=int(element.attrib["Amount_currency"]),
            Amount_exclude_null=cls.parse_bool(element.attrib["Amount_exclude_null"]),
            Payment_method_list=element.attrib["Payment_method_list"],
            Use_text=cls.parse_bool(element.attrib["Use_text"]),
            Use_amount=cls.parse_bool(element.attrib["Use_amount"]),
        )
