"""Domain section: Report."""

from dataclasses import dataclass

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class ReportSection(GsbFileSection):
    """A saved report defined in the Grisbi file.

    Attributes:
        Nb: Unique identifier.
        Name: Report display name.
        Compl_name_function: Complementary name function.
        Compl_name_position: Complementary name position.
        Compl_name_used: Use complementary name.
        General_sort_type: General sort specification string.
        Show_r: Show reconciled transactions.
        Show_transaction: Show individual transactions.
        Show_transaction_amount: Show transaction amount column.
        Show_transaction_nb: Show transaction number column.
        Show_transaction_date: Show transaction date column.
        Show_transaction_payee: Show payee column.
        Show_transaction_categ: Show category column.
        Show_transaction_sub_categ: Show sub-category column.
        Show_transaction_payment: Show payment method column.
        Show_transaction_budget: Show budget column.
        Show_transaction_sub_budget: Show sub-budget column.
        Show_transaction_chq: Show cheque/reference column.
        Show_transaction_note: Show notes column.
        Show_transaction_voucher: Show voucher column.
        Show_transaction_reconcile: Show reconcile column.
        Show_transaction_bank: Show bank reference column.
        Show_transaction_fin_year: Show financial year column.
        Show_transaction_sort_type: Show sort type column.
        Show_columns_titles: Show column titles.
        Show_title_column_kind: Show title column kind.
        Show_exclude_split_child: Exclude breakdown child rows.
        Show_split_amounts: Show split amounts.
        Currency_general: Currency identifier for the report.
        Report_in_payees: Include payees in the report.
        Report_can_click: Report rows are clickable.
        Financial_year_used: Filter by financial year.
        Financial_year_kind: Financial year filter kind.
        Financial_year_select: Selected financial years (nullable).
        Date_kind: Date range kind.
        Date_beginning: Report start date string.
        Date_end: Report end date string.
        Split_by_date: Split report by date.
        Split_date_period: Date split period.
        Split_by_fin_year: Split report by financial year.
        Split_day_beginning: Day the report period begins.
        Account_use_selection: Filter by account selection.
        Account_selected: Selected accounts (nullable).
        Account_group_transactions: Group transactions by account.
        Account_show_amount: Show account amount.
        Account_show_name: Show account name.
        Transfer_kind: Transfer inclusion kind.
        Transfer_selected_accounts: Selected transfer accounts (nullable).
        Transfer_exclude_transactions: Exclude transfer transactions.
        Categ_use: Use category filtering.
        Categ_use_selection: Filter by category selection.
        Categ_selected: Selected categories (nullable).
        Categ_exclude_transactions: Exclude transactions matching category filter.
        Categ_show_amount: Show category amount.
        Categ_show_sub_categ: Show sub-categories.
        Categ_show_without_sub_categ: Show categories without sub-categories.
        Categ_show_sub_categ_amount: Show sub-category amounts.
        Categ_currency: Currency identifier for category display.
        Categ_show_name: Show category names.
        Budget_use: Use budget filtering.
        Budget_use_selection: Filter by budget selection.
        Budget_selected: Selected budget lines (nullable).
        Budget_exclude_transactions: Exclude transactions matching budget filter.
        Budget_show_amount: Show budget amount.
        Budget_show_sub_budget: Show sub-budget lines.
        Budget_show_without_sub_budget: Show budgets without sub-budgets.
        Budget_show_sub_budget_amount: Show sub-budget amounts.
        Budget_currency: Currency identifier for budget display.
        Budget_show_name: Show budget names.
        Payee_use: Use payee filtering.
        Payee_use_selection: Filter by payee selection.
        Payee_selected: Selected payees (nullable).
        Payee_show_amount: Show payee amount.
        Payee_currency: Currency identifier for payee display.
        Payee_show_name: Show payee names.
        Amount_currency: Currency identifier for amount display.
        Amount_exclude_null: Exclude zero-amount rows.
        Payment_method_list: Payment methods filter (nullable).
        Use_text: Use text comparison filter.
        Use_amount: Use amount comparison filter.
    """

    Nb: int
    Name: str
    Compl_name_function: int
    Compl_name_position: int
    Compl_name_used: bool
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
    Show_exclude_split_child: bool
    Show_split_amounts: bool
    Currency_general: int
    Report_in_payees: bool
    Report_can_click: bool
    Financial_year_used: bool
    Financial_year_kind: int
    Financial_year_select: str | None
    Date_kind: int
    Date_beginning: str
    Date_end: str
    Split_by_date: bool
    Split_date_period: int
    Split_by_fin_year: bool
    Split_day_beginning: int
    Account_use_selection: bool
    Account_selected: str | None
    Account_group_transactions: bool
    Account_show_amount: bool
    Account_show_name: bool
    Transfer_kind: int
    Transfer_selected_accounts: str | None
    Transfer_exclude_transactions: bool
    Categ_use: bool
    Categ_use_selection: bool
    Categ_selected: str | None
    Categ_exclude_transactions: bool
    Categ_show_amount: bool
    Categ_show_sub_categ: bool
    Categ_show_without_sub_categ: bool
    Categ_show_sub_categ_amount: bool
    Categ_currency: int
    Categ_show_name: bool
    Budget_use: bool
    Budget_use_selection: bool
    Budget_selected: str | None
    Budget_exclude_transactions: bool
    Budget_show_amount: bool
    Budget_show_sub_budget: bool
    Budget_show_without_sub_budget: bool
    Budget_show_sub_budget_amount: bool
    Budget_currency: int
    Budget_show_name: bool
    Payee_use: bool
    Payee_use_selection: bool
    Payee_selected: str | None
    Payee_show_amount: bool
    Payee_currency: int
    Payee_show_name: bool
    Amount_currency: int
    Amount_exclude_null: bool
    Payment_method_list: str | None
    Use_text: bool
    Use_amount: bool
