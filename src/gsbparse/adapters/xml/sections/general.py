"""XML adapter: parse a ``<General>`` element into a ``GeneralSection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import (
    parse_amount,
    parse_bool,
    parse_int,
    parse_null,
    parse_nullable_str,
    parse_str,
)
from gsbparse.domain.sections.general import GeneralSection

_parse_optional_int = parse_null(parse_int)
_parse_optional_bool = parse_null(parse_bool)


def parse_general_section(element: ET.Element) -> GeneralSection:
    """Parse a ``<General>`` XML element into a :class:`GeneralSection`.

    Several attributes are absent in older Grisbi file versions; these are
    modelled as ``T | None`` on :class:`GeneralSection` and resolved to
    ``None`` via ``a.get()`` when the key is missing from the element.

    Hyphenated XML attribute names are mapped to their underscored Python
    equivalents (e.g. ``Import-ope-nbre-max`` -> ``Import_ope_nbre_max``).

    Args:
        element: The ``<General>`` XML element.

    Returns:
        A fully populated :class:`GeneralSection`.
    """
    a = element.attrib

    def _opt_int(key: str) -> int | None:
        raw = a.get(key)
        return parse_int(raw) if raw is not None else None

    def _opt_bool(key: str) -> bool | None:
        raw = a.get(key)
        return parse_bool(raw) if raw is not None else None

    def _opt_str(key: str) -> str | None:
        raw = a.get(key)
        return parse_nullable_str(raw) if raw is not None else None

    return GeneralSection(
        File_version=parse_str(a["File_version"]),
        Grisbi_version=parse_str(a["Grisbi_version"]),
        Crypt_file=parse_bool(a["Crypt_file"]),
        Archive_file=parse_bool(a["Archive_file"]),
        File_title=parse_str(a["File_title"]),
        Use_icons_file_dir=parse_bool(a["Use_icons_file_dir"]),
        General_address=_opt_str("General_address"),
        Second_general_address=_opt_str("Second_general_address"),
        Date_format=parse_str(a["Date_format"]),
        Decimal_point=parse_str(a["Decimal_point"]),
        Thousands_separator=parse_str(a["Thousands_separator"]),
        Party_list_currency_number=parse_int(a["Party_list_currency_number"]),
        Category_list_currency_number=parse_int(a["Category_list_currency_number"]),
        Budget_list_currency_number=parse_int(a["Budget_list_currency_number"]),
        Navigation_list_order=parse_str(a["Navigation_list_order"]),
        Scheduler_view=parse_int(a["Scheduler_view"]),
        Scheduler_custom_number=parse_int(a["Scheduler_custom_number"]),
        Scheduler_custom_menu=parse_int(a["Scheduler_custom_menu"]),
        Scheduler_set_default_account=parse_bool(a["Scheduler_set_default_account"]),
        Scheduler_default_account_number=parse_int(a["Scheduler_default_account_number"]),
        Scheduler_set_fixed_date=parse_bool(a["Scheduler_set_fixed_date"]),
        Scheduler_default_fixed_date=parse_int(a["Scheduler_default_fixed_date"]),
        Import_interval_search=parse_int(a["Import_interval_search"]),
        Import_ope_nbre_max=_opt_int("Import-ope-nbre-max"),
        Import_copy_payee_in_note=parse_bool(a["Import_copy_payee_in_note"]),
        Import_extract_number_for_check=parse_bool(a["Import_extract_number_for_check"]),
        Import_fusion_transactions=parse_bool(a["Import_fusion_transactions"]),
        Import_categorie_for_payee=parse_bool(a["Import_categorie_for_payee"]),
        Import_fyear_by_value_date=parse_bool(a["Import_fyear_by_value_date"]),
        Import_qif_no_import_categories=parse_bool(a["Import_qif_no_import_categories"]),
        Import_qif_use_field_extract_method_payment=parse_bool(
            a["Import_qif_use_field_extract_method_payment"]
        ),
        Export_file_format=parse_int(a["Export_file_format"]),
        Export_files_traitement=parse_bool(a["Export_files_traitement"]),
        Export_force_US_dates=parse_bool(a["Export_force_US_dates"]),
        Export_force_US_numbers=parse_bool(a["Export_force_US_numbers"]),
        Export_quote_dates=parse_bool(a["Export_quote_dates"]),
        Form_date_force_prev_year=parse_bool(a["Form_date_force_prev_year"]),
        Form_columns_number=parse_int(a["Form_columns_number"]),
        Form_lines_number=parse_int(a["Form_lines_number"]),
        Form_organization=parse_str(a["Form_organization"]),
        Form_columns_width=_opt_str("Form_columns_width"),
        Reconcile_end_date=parse_bool(a["Reconcile_end_date"]),
        Reconcile_sort=parse_bool(a["Reconcile_sort"]),
        Use_logo=parse_bool(a["Use_logo"]),
        Name_logo=_opt_str("Name_logo"),
        Remind_display_per_account=parse_bool(a["Remind_display_per_account"]),
        Transactions_view=parse_str(a["Transactions_view"]),
        One_line_showed=_opt_bool("One_line_showed"),
        Two_lines_showed=parse_bool(a["Two_lines_showed"]),
        Three_lines_showed=parse_bool(a["Three_lines_showed"]),
        Transaction_column_width=parse_str(a["Transaction_column_width"]),
        Transaction_column_align=parse_str(a["Transaction_column_align"]),
        Scheduler_column_width=parse_str(a["Scheduler_column_width"]),
        Combofix_mixed_sort=parse_bool(a["Combofix_mixed_sort"]),
        Combofix_case_sensitive=parse_bool(a["Combofix_case_sensitive"]),
        Combofix_force_payee=parse_bool(a["Combofix_force_payee"]),
        Combofix_force_category=parse_bool(a["Combofix_force_category"]),
        Automatic_amount_separator=parse_bool(a["Automatic_amount_separator"]),
        CSV_separator=parse_str(a["CSV_separator"]),
        CSV_force_date_valeur_with_date=parse_bool(a["CSV_force_date_valeur_with_date"]),
        Metatree_assoc_mode=_opt_int("Metatree_assoc_mode"),
        Metatree_sort_transactions=parse_int(a["Metatree_sort_transactions"]),
        Metatree_unarchived_payees=parse_bool(a["Metatree_unarchived_payees"]),
        Add_archive_in_total_balance=parse_bool(a["Add_archive_in_total_balance"]),
        Force_credit_before_debit=_opt_bool("Force-credit-before-debit"),
        Bet_array_column_width=parse_str(a["Bet_array_column_width"]),
        Bet_capital=parse_amount(a["Bet_capital"]),
        Bet_currency=parse_int(a["Bet_currency"]),
        Bet_taux_annuel=parse_amount(a["Bet_taux_annuel"]),
        Bet_index_duree=parse_int(a["Bet_index_duree"]),
        Bet_frais=parse_amount(a["Bet_frais"]),
        Bet_type_taux=parse_int(a["Bet_type_taux"]),
    )
