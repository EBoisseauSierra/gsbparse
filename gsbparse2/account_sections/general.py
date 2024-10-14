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
            File_version=cls.parse_str(element.attrib.get("File_version")),
            Grisbi_version=cls.parse_str(element.attrib.get("Grisbi_version")),
            Crypt_file=cls.parse_bool(element.attrib.get("Crypt_file")),
            Archive_file=cls.parse_bool(element.attrib.get("Archive_file")),
            File_title=cls.parse_str(element.attrib.get("File_title")),
            Use_icons_file_dir=cls.parse_bool(
                element.attrib.get("Use_icons_file_dir"), is_optional=True
            ),
            General_address=cls.parse_str(element.attrib.get("General_address")),
            Second_general_address=cls.parse_str(
                element.attrib.get("Second_general_address")
            ),
            Date_format=cls.parse_str(element.attrib.get("Date_format")),
            Decimal_point=cls.parse_str(element.attrib.get("Decimal_point")),
            Thousands_separator=cls.parse_str(
                element.attrib.get("Thousands_separator")
            ),
            Party_list_currency_number=int(
                element.attrib.get("Party_list_currency_number"),
            ),
            Category_list_currency_number=int(
                element.attrib.get("Category_list_currency_number"),
            ),
            Budget_list_currency_number=int(
                element.attrib.get("Budget_list_currency_number"),
            ),
            Navigation_list_order=cls.parse_list_int(
                element.attrib.get("Navigation_list_order"),
            ),
            Scheduler_view=cls.parse_bool(element.attrib.get("Scheduler_view")),
            Scheduler_custom_number=cls.parse_bool(
                element.attrib.get("Scheduler_custom_number"),
            ),
            Scheduler_custom_menu=cls.parse_bool(
                element.attrib.get("Scheduler_custom_menu"),
            ),
            Scheduler_set_default_account=cls.parse_bool(
                element.attrib.get("Scheduler_set_default_account"),
            ),
            Scheduler_default_account_number=cls.parse_bool(
                element.attrib.get("Scheduler_default_account_number"),
            ),
            Scheduler_set_fixed_date=cls.parse_bool(
                element.attrib.get("Scheduler_set_fixed_date"),
            ),
            Scheduler_default_fixed_date=cls.parse_bool(
                element.attrib.get("Scheduler_default_fixed_date"),
            ),
            Import_interval_search=cls.parse_int(
                element.attrib.get("Import_interval_search")
            ),
            Import_copy_payee_in_note=cls.parse_bool(
                element.attrib.get("Import_copy_payee_in_note"),
            ),
            Import_extract_number_for_check=cls.parse_bool(
                element.attrib.get("Import_extract_number_for_check"),
            ),
            Import_fusion_transactions=cls.parse_bool(
                element.attrib.get("Import_fusion_transactions"),
            ),
            Import_categorie_for_payee=cls.parse_bool(
                element.attrib.get("Import_categorie_for_payee"),
            ),
            Import_fyear_by_value_date=cls.parse_bool(
                element.attrib.get("Import_fyear_by_value_date"),
            ),
            Import_qif_no_import_categories=cls.parse_bool(
                element.attrib.get("Import_qif_no_import_categories"),
            ),
            Import_qif_use_field_extract_method_payment=cls.parse_bool(
                element.attrib.get("Import_qif_use_field_extract_method_payment"),
            ),
            Export_file_format=cls.parse_bool(element.attrib.get("Export_file_format")),
            Export_files_traitement=cls.parse_bool(
                element.attrib.get("Export_files_traitement"),
            ),
            Export_force_US_dates=cls.parse_bool(
                element.attrib.get("Export_force_US_dates"),
            ),
            Export_force_US_numbers=cls.parse_bool(
                element.attrib.get("Export_force_US_numbers"),
            ),
            Export_quote_dates=cls.parse_bool(element.attrib.get("Export_quote_dates")),
            Form_date_force_prev_year=cls.parse_bool(
                element.attrib.get("Form_date_force_prev_year"),
            ),
            Form_columns_number=cls.parse_int(
                element.attrib.get("Form_columns_number")
            ),
            Form_lines_number=cls.parse_int(element.attrib.get("Form_lines_number")),
            Form_organization=cls.parse_list_int(
                element.attrib.get("Form_organization"),
            ),
            Reconcile_end_date=cls.parse_bool(element.attrib.get("Reconcile_end_date")),
            Reconcile_sort=cls.parse_bool(element.attrib.get("Reconcile_sort")),
            Use_logo=cls.parse_bool(element.attrib.get("Use_logo")),
            Name_logo=cls.parse_str(element.attrib.get("Name_logo")),
            Remind_display_per_account=cls.parse_bool(
                element.attrib.get("Remind_display_per_account"),
            ),
            Transactions_view=cls.parse_list_int(
                element.attrib.get("Transactions_view"),
            ),
            Two_lines_showed=cls.parse_bool(element.attrib.get("Two_lines_showed")),
            Three_lines_showed=cls.parse_bool(element.attrib.get("Three_lines_showed")),
            Transaction_column_width=cls.parse_list_int(
                element.attrib.get("Transaction_column_width"),
            ),
            Transaction_column_align=cls.parse_list_int(
                element.attrib.get("Transaction_column_align"),
            ),
            Scheduler_column_width=cls.parse_list_int(
                element.attrib.get("Scheduler_column_width"),
            ),
            Combofix_mixed_sort=cls.parse_bool(
                element.attrib.get("Combofix_mixed_sort"),
            ),
            Combofix_case_sensitive=cls.parse_bool(
                element.attrib.get("Combofix_case_sensitive"),
            ),
            Combofix_force_payee=cls.parse_bool(
                element.attrib.get("Combofix_force_payee"),
            ),
            Combofix_force_category=cls.parse_bool(
                element.attrib.get("Combofix_force_category"),
            ),
            Automatic_amount_separator=cls.parse_bool(
                element.attrib.get("Automatic_amount_separator"),
            ),
            CSV_separator=cls.parse_str(element.attrib.get("CSV_separator")),
            CSV_force_date_valeur_with_date=cls.parse_bool(
                element.attrib.get("CSV_force_date_valeur_with_date"),
            ),
            Metatree_assoc_mode=cls.parse_bool(
                element.attrib.get("Metatree_assoc_mode"),
            ),
            Metatree_sort_transactions=cls.parse_bool(
                element.attrib.get("Metatree_sort_transactions"),
            ),
            Metatree_unarchived_payees=cls.parse_bool(
                element.attrib.get("Metatree_unarchived_payees"),
            ),
            Add_archive_in_total_balance=cls.parse_bool(
                element.attrib.get("Add_archive_in_total_balance"),
            ),
            Bet_array_column_width=cls.parse_list_int(
                element.attrib.get("Bet_array_column_width"),
            ),
            Bet_capital=cls.parse_amount(element.attrib.get("Bet_capital")),
            Bet_currency=cls.parse_int(element.attrib.get("Bet_currency")),
            Bet_taux_annuel=cls.parse_amount(element.attrib.get("Bet_taux_annuel")),
            Bet_index_duree=cls.parse_int(element.attrib.get("Bet_index_duree")),
            Bet_frais=cls.parse_amount(element.attrib.get("Bet_capital")),
            Bet_type_taux=cls.parse_int(element.attrib.get("Bet_type_taux")),
        )
