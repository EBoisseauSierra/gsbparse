from dataclasses import dataclass
from decimal import Decimal
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse2.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class GeneralSection(GsbFileSection):
    File_version: str
    Grisbi_version: str
    Crypt_file: bool
    Archive_file: bool
    File_title: str
    Use_icons_file_dir: bool
    General_address: str
    Second_general_address: str
    Date_format: str
    Decimal_point: str
    Thousands_separator: str
    Party_list_currency_number: int
    Category_list_currency_number: int
    Budget_list_currency_number: int
    Navigation_list_order: list[int] | None
    Scheduler_view: bool
    Scheduler_custom_number: bool
    Scheduler_custom_menu: bool
    Scheduler_set_default_account: bool
    Scheduler_default_account_number: bool
    Scheduler_set_fixed_date: bool
    Scheduler_default_fixed_date: bool
    Import_interval_search: int
    Import_copy_payee_in_note: bool
    Import_extract_number_for_check: bool
    Import_fusion_transactions: bool
    Import_categorie_for_payee: bool
    Import_fyear_by_value_date: bool
    Import_qif_no_import_categories: bool
    Import_qif_use_field_extract_method_payment: bool
    Export_file_format: bool
    Export_files_traitement: bool
    Export_force_US_dates: bool
    Export_force_US_numbers: bool
    Export_quote_dates: bool
    Form_date_force_prev_year: bool
    Form_columns_number: int
    Form_lines_number: int
    Form_organization: list[int] | None
    Reconcile_end_date: bool
    Reconcile_sort: bool
    Use_logo: bool
    Name_logo: str
    Remind_display_per_account: bool
    Transactions_view: list[int] | None
    Two_lines_showed: bool
    Three_lines_showed: bool
    Transaction_column_width: list[int] | None
    Transaction_column_align: list[int] | None
    Scheduler_column_width: list[int] | None
    Combofix_mixed_sort: bool
    Combofix_case_sensitive: bool
    Combofix_force_payee: bool
    Combofix_force_category: bool
    Automatic_amount_separator: bool
    CSV_separator: str
    CSV_force_date_valeur_with_date: bool
    Metatree_assoc_mode: bool
    Metatree_sort_transactions: bool
    Metatree_unarchived_payees: bool
    Add_archive_in_total_balance: bool
    Bet_array_column_width: list[int] | None
    Bet_capital: Decimal
    Bet_currency: int
    Bet_taux_annuel: Decimal
    Bet_index_duree: int
    Bet_frais: Decimal
    Bet_type_taux: int

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            File_version=element.attrib["File_version"],
            Grisbi_version=element.attrib["Grisbi_version"],
            Crypt_file=cls.parse_bool(element.attrib["Crypt_file"]),
            Archive_file=cls.parse_bool(element.attrib["Archive_file"]),
            File_title=element.attrib["File_title"],
            Use_icons_file_dir=cls.parse_bool(element.attrib["Use_icons_file_dir"]),
            General_address=element.attrib["General_address"],
            Second_general_address=element.attrib["Second_general_address"],
            Date_format=element.attrib["Date_format"],
            Decimal_point=element.attrib["Decimal_point"],
            Thousands_separator=element.attrib["Thousands_separator"],
            Party_list_currency_number=int(
                element.attrib["Party_list_currency_number"],
            ),
            Category_list_currency_number=int(
                element.attrib["Category_list_currency_number"],
            ),
            Budget_list_currency_number=int(
                element.attrib["Budget_list_currency_number"],
            ),
            Navigation_list_order=cls.parse_list_int(
                element.attrib["Navigation_list_order"],
            ),
            Scheduler_view=cls.parse_bool(element.attrib["Scheduler_view"]),
            Scheduler_custom_number=cls.parse_bool(
                element.attrib["Scheduler_custom_number"],
            ),
            Scheduler_custom_menu=cls.parse_bool(
                element.attrib["Scheduler_custom_menu"],
            ),
            Scheduler_set_default_account=cls.parse_bool(
                element.attrib["Scheduler_set_default_account"],
            ),
            Scheduler_default_account_number=cls.parse_bool(
                element.attrib["Scheduler_default_account_number"],
            ),
            Scheduler_set_fixed_date=cls.parse_bool(
                element.attrib["Scheduler_set_fixed_date"],
            ),
            Scheduler_default_fixed_date=cls.parse_bool(
                element.attrib["Scheduler_default_fixed_date"],
            ),
            Import_interval_search=int(element.attrib["Import_interval_search"]),
            Import_copy_payee_in_note=cls.parse_bool(
                element.attrib["Import_copy_payee_in_note"],
            ),
            Import_extract_number_for_check=cls.parse_bool(
                element.attrib["Import_extract_number_for_check"],
            ),
            Import_fusion_transactions=cls.parse_bool(
                element.attrib["Import_fusion_transactions"],
            ),
            Import_categorie_for_payee=cls.parse_bool(
                element.attrib["Import_categorie_for_payee"],
            ),
            Import_fyear_by_value_date=cls.parse_bool(
                element.attrib["Import_fyear_by_value_date"],
            ),
            Import_qif_no_import_categories=cls.parse_bool(
                element.attrib["Import_qif_no_import_categories"],
            ),
            Import_qif_use_field_extract_method_payment=cls.parse_bool(
                element.attrib["Import_qif_use_field_extract_method_payment"],
            ),
            Export_file_format=cls.parse_bool(element.attrib["Export_file_format"]),
            Export_files_traitement=cls.parse_bool(
                element.attrib["Export_files_traitement"],
            ),
            Export_force_US_dates=cls.parse_bool(
                element.attrib["Export_force_US_dates"],
            ),
            Export_force_US_numbers=cls.parse_bool(
                element.attrib["Export_force_US_numbers"],
            ),
            Export_quote_dates=cls.parse_bool(element.attrib["Export_quote_dates"]),
            Form_date_force_prev_year=cls.parse_bool(
                element.attrib["Form_date_force_prev_year"],
            ),
            Form_columns_number=int(element.attrib["Form_columns_number"]),
            Form_lines_number=int(element.attrib["Form_lines_number"]),
            Form_organization=cls.parse_list_int(
                element.attrib["Form_organization"],
            ),
            Reconcile_end_date=cls.parse_bool(element.attrib["Reconcile_end_date"]),
            Reconcile_sort=cls.parse_bool(element.attrib["Reconcile_sort"]),
            Use_logo=cls.parse_bool(element.attrib["Use_logo"]),
            Name_logo=element.attrib["Name_logo"],
            Remind_display_per_account=cls.parse_bool(
                element.attrib["Remind_display_per_account"],
            ),
            Transactions_view=cls.parse_list_int(
                element.attrib["Transactions_view"],
            ),
            Two_lines_showed=cls.parse_bool(element.attrib["Two_lines_showed"]),
            Three_lines_showed=cls.parse_bool(element.attrib["Three_lines_showed"]),
            Transaction_column_width=cls.parse_list_int(
                element.attrib["Transaction_column_width"],
            ),
            Transaction_column_align=cls.parse_list_int(
                element.attrib["Transaction_column_align"],
            ),
            Scheduler_column_width=cls.parse_list_int(
                element.attrib["Scheduler_column_width"],
            ),
            Combofix_mixed_sort=cls.parse_bool(
                element.attrib["Combofix_mixed_sort"],
            ),
            Combofix_case_sensitive=cls.parse_bool(
                element.attrib["Combofix_case_sensitive"],
            ),
            Combofix_force_payee=cls.parse_bool(
                element.attrib["Combofix_force_payee"],
            ),
            Combofix_force_category=cls.parse_bool(
                element.attrib["Combofix_force_category"],
            ),
            Automatic_amount_separator=cls.parse_bool(
                element.attrib["Automatic_amount_separator"],
            ),
            CSV_separator=element.attrib["CSV_separator"],
            CSV_force_date_valeur_with_date=cls.parse_bool(
                element.attrib["CSV_force_date_valeur_with_date"],
            ),
            Metatree_assoc_mode=cls.parse_bool(
                element.attrib["Metatree_assoc_mode"],
            ),
            Metatree_sort_transactions=cls.parse_bool(
                element.attrib["Metatree_sort_transactions"],
            ),
            Metatree_unarchived_payees=cls.parse_bool(
                element.attrib["Metatree_unarchived_payees"],
            ),
            Add_archive_in_total_balance=cls.parse_bool(
                element.attrib["Add_archive_in_total_balance"],
            ),
            Bet_array_column_width=cls.parse_list_int(
                element.attrib["Bet_array_column_width"],
            ),
            Bet_capital=cls.parse_amount(element.attrib["Bet_capital"]),
            Bet_currency=int(element.attrib["Bet_currency"]),
            Bet_taux_annuel=cls.parse_amount(element.attrib["Bet_taux_annuel"]),
            Bet_index_duree=int(element.attrib["Bet_index_duree"]),
            Bet_frais=cls.parse_amount(element.attrib["Bet_capital"]),
            Bet_type_taux=int(element.attrib["Bet_type_taux"]),
        )
