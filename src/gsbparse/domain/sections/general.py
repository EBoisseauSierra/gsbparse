"""Domain section: General (global file settings)."""

from dataclasses import dataclass
from decimal import Decimal

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class General(GsbFileSection):
    """Global settings stored at the top of a Grisbi file.

    Attribute names follow the XML attribute names from the file exactly,
    except that hyphenated XML names (``Import-ope-nbre-max``,
    ``Force-credit-before-debit``, ``Archive-force-unreconciled``) are
    represented with underscores.  The XML adapter maps them accordingly.

    Attributes:
        File_version: Grisbi file format version string.
        Grisbi_version: Grisbi application version string.
        Crypt_file: File is encrypted.
        Archive_file: File is an archive.
        File_title: Title of the file (displayed in the UI).
        Use_icons_file_dir: Account icons are in the file's ``icon/`` subdir.
        General_address: Owner address line 1 (nullable).
        Second_general_address: Owner address line 2 (nullable).
        Date_format: ``strftime``-style date format used in the file.
        Decimal_point: Decimal separator character.
        Thousands_separator: Thousands separator character.
        Party_list_currency_number: Currency used in the party list.
        Category_list_currency_number: Currency used in the category list.
        Budget_list_currency_number: Currency used in the budget list.
        Navigation_list_order: Dash-separated navigation panel order.
        Scheduler_view: Scheduler display mode.
        Scheduler_custom_number: Custom scheduler period count.
        Scheduler_custom_menu: Custom scheduler period unit menu index.
        Scheduler_set_default_account: Use a fixed default account for scheduler.
        Scheduler_default_account_number: Default account identifier for scheduler.
        Scheduler_set_fixed_date: Use a fixed date offset for scheduler.
        Scheduler_default_fixed_date: Fixed date offset for scheduler.
        Import_interval_search: Days to search around a transaction date on import.
        Import_ope_nbre_max: Maximum number of transactions to import (0 = unlimited).
        Import_copy_payee_in_note: Copy payee name into notes on import.
        Import_extract_number_for_check: Extract a cheque number from the payee field.
        Import_fusion_transactions: Try to merge duplicate transactions on import.
        Import_categorie_for_payee: Auto-assign category from payee on import.
        Import_fyear_by_value_date: Assign financial year by value date on import.
        Import_qif_no_import_categories: Skip categories when importing QIF files.
        Import_qif_use_field_extract_method_payment: Use field extraction for QIF payment method.
        Export_file_format: Default export format.
        Export_files_traitement: Post-process exported files.
        Export_force_US_dates: Force US date format (MM/DD/YYYY) in exports.
        Export_force_US_numbers: Force US number format in exports.
        Export_quote_dates: Quote dates with double quotes in exports.
        Form_date_force_prev_year: Force previous year when entering dates in December.
        Form_columns_number: Number of columns in the transaction entry form.
        Form_lines_number: Number of lines in the transaction entry form.
        Form_organization: Form-field layout specification string.
        Form_columns_width: Dash-separated form column widths.
        Reconcile_end_date: Show end date in reconciliation.
        Reconcile_sort: Sort transactions during reconciliation.
        Use_logo: Display a custom logo.
        Name_logo: Path to the logo file (nullable).
        Remind_display_per_account: Show balance reminders per account.
        Transactions_view: Dash-separated column visibility specification.
        One_line_showed: Show one line per transaction.
        Two_lines_showed: Show two lines per transaction.
        Three_lines_showed: Show three lines per transaction.
        Transaction_column_width: Dash-separated transaction column widths.
        Transaction_column_align: Dash-separated transaction column alignment flags.
        Scheduler_column_width: Dash-separated scheduler column widths.
        Combofix_mixed_sort: Mix expense/income entries in combo boxes.
        Combofix_case_sensitive: Case-sensitive combo box matching.
        Combofix_force_payee: Force payee completion in combo boxes.
        Combofix_force_category: Force category completion in combo boxes.
        Automatic_amount_separator: Insert decimal separator automatically.
        CSV_separator: CSV field separator character.
        CSV_force_date_valeur_with_date: Fill value date from transaction date in CSV export.
        Metatree_assoc_mode: Metatree association mode.
        Metatree_sort_transactions: Metatree transaction sort mode.
        Metatree_unarchived_payees: Show unarchived payees in metatree.
        Add_archive_in_total_balance: Include archived transactions in total balance.
        Force_credit_before_debit: Show credit before debit.
        Bet_array_column_width: Dash-separated budget-estimate column widths.
        Bet_capital: Loan capital.
        Bet_currency: Loan currency identifier.
        Bet_taux_annuel: Annual loan interest rate.
        Bet_index_duree: Duration index.
        Bet_frais: Loan fees.
        Bet_type_taux: Interest rate type.
    """

    File_version: str
    Grisbi_version: str
    Crypt_file: bool
    Archive_file: bool
    File_title: str
    Use_icons_file_dir: bool
    General_address: str | None
    Second_general_address: str | None
    Date_format: str
    Decimal_point: str
    Thousands_separator: str
    Party_list_currency_number: int
    Category_list_currency_number: int
    Budget_list_currency_number: int
    Navigation_list_order: str
    Scheduler_view: int
    Scheduler_custom_number: int
    Scheduler_custom_menu: int
    Scheduler_set_default_account: bool
    Scheduler_default_account_number: int
    Scheduler_set_fixed_date: bool
    Scheduler_default_fixed_date: int
    Import_interval_search: int
    Import_ope_nbre_max: int | None
    Import_copy_payee_in_note: bool
    Import_extract_number_for_check: bool
    Import_fusion_transactions: bool
    Import_categorie_for_payee: bool
    Import_fyear_by_value_date: bool
    Import_qif_no_import_categories: bool
    Import_qif_use_field_extract_method_payment: bool
    Export_file_format: int
    Export_files_traitement: bool
    Export_force_US_dates: bool
    Export_force_US_numbers: bool
    Export_quote_dates: bool
    Form_date_force_prev_year: bool
    Form_columns_number: int
    Form_lines_number: int
    Form_organization: str
    Form_columns_width: str | None
    Reconcile_end_date: bool
    Reconcile_sort: bool
    Use_logo: bool
    Name_logo: str | None
    Remind_display_per_account: bool
    Transactions_view: str
    One_line_showed: bool | None
    Two_lines_showed: bool
    Three_lines_showed: bool
    Transaction_column_width: str
    Transaction_column_align: str
    Scheduler_column_width: str
    Combofix_mixed_sort: bool
    Combofix_case_sensitive: bool
    Combofix_force_payee: bool
    Combofix_force_category: bool
    Automatic_amount_separator: bool
    CSV_separator: str
    CSV_force_date_valeur_with_date: bool
    Metatree_assoc_mode: int | None
    Metatree_sort_transactions: int
    Metatree_unarchived_payees: bool
    Add_archive_in_total_balance: bool
    Force_credit_before_debit: bool | None
    Bet_array_column_width: str
    Bet_capital: Decimal
    Bet_currency: int
    Bet_taux_annuel: Decimal
    Bet_index_duree: int
    Bet_frais: Decimal
    Bet_type_taux: int
