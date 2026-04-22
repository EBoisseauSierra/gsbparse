"""Layer 2: Section parser unit tests.

One test per section verifies that all fields are wired correctly from XML
attributes to the domain dataclass. Higher-layer tests do NOT re-assert
individual fields — they trust this layer.
"""

import xml.etree.ElementTree as ET
from datetime import date
from decimal import Decimal

import pytest

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
from gsbparse.adapters.xml.sections.rgba import parse_rgba_section
from gsbparse.adapters.xml.sections.scheduled import parse_scheduled_section
from gsbparse.adapters.xml.sections.special_line import parse_special_line_section
from gsbparse.adapters.xml.sections.sub_budgetary import parse_sub_budgetary_section
from gsbparse.adapters.xml.sections.sub_category import parse_sub_category_section
from gsbparse.adapters.xml.sections.text_comparison import parse_text_comparison_section
from gsbparse.adapters.xml.sections.transaction import parse_transaction_section
from gsbparse.domain.sections.account import AccountKind
from gsbparse.domain.sections.category import CategoryKind
from gsbparse.domain.sections.transaction import TransactionMarkedState


def _el(tag: str, **attrib: str) -> ET.Element:
    element = ET.Element(tag)
    element.attrib = attrib
    return element


class TestParseCurrency:
    def test_all_fields_wired(self):
        dummy_nb = "3"
        dummy_na = "US Dollar"
        dummy_co = "$"
        dummy_ico = "USD"
        dummy_fl = "2"
        element = _el("Currency", Nb=dummy_nb, Na=dummy_na, Co=dummy_co, Ico=dummy_ico, Fl=dummy_fl)

        section = parse_currency_section(element)

        assert section.Nb == int(dummy_nb)
        assert section.Na == dummy_na
        assert section.Co == dummy_co
        assert section.Ico == dummy_ico
        assert section.Fl == int(dummy_fl)


class TestParseParty:
    def test_all_fields_wired(self):
        dummy_nb = "5"
        dummy_na = "Supermarket"
        element = _el(
            "Party",
            Nb=dummy_nb,
            Na=dummy_na,
            Txt="(null)",
            Search="(null)",
            IgnCase="1",
            UseRegex="0",
        )

        section = parse_party_section(element)

        assert section.Nb == int(dummy_nb)
        assert section.Na == dummy_na
        assert section.Txt is None
        assert section.Search is None
        assert section.IgnCase is True
        assert section.UseRegex is False


class TestParseCategory:
    def test_all_fields_wired(self):
        dummy_nb = "10"
        dummy_na = "Food"
        dummy_kd = "1"
        element = _el("Category", Nb=dummy_nb, Na=dummy_na, Kd=dummy_kd)

        section = parse_category_section(element)

        assert section.Nb == int(dummy_nb)
        assert section.Na == dummy_na
        assert section.Kd == CategoryKind(int(dummy_kd))


class TestParseSubCategory:
    def test_all_fields_wired(self):
        dummy_nbc = "10"
        dummy_nb = "2"
        dummy_na = "Groceries"
        element = _el("Sub_category", Nbc=dummy_nbc, Nb=dummy_nb, Na=dummy_na)

        section = parse_sub_category_section(element)

        assert section.Nbc == int(dummy_nbc)
        assert section.Nb == int(dummy_nb)
        assert section.Na == dummy_na


class TestParseBudgetary:
    def test_all_fields_wired(self):
        dummy_nb = "1"
        dummy_na = "Essentials"
        dummy_kd = "1"
        element = _el("Budgetary", Nb=dummy_nb, Na=dummy_na, Kd=dummy_kd)

        section = parse_budgetary_section(element)

        assert section.Nb == int(dummy_nb)
        assert section.Na == dummy_na
        assert section.Kd == CategoryKind(int(dummy_kd))


class TestParseSubBudgetary:
    def test_all_fields_wired(self):
        dummy_nbb = "1"
        dummy_nb = "3"
        dummy_na = "Transport"
        element = _el("Sub_budgetary", Nbb=dummy_nbb, Nb=dummy_nb, Na=dummy_na)

        section = parse_sub_budgetary_section(element)

        assert section.Nbb == int(dummy_nbb)
        assert section.Nb == int(dummy_nb)
        assert section.Na == dummy_na


class TestParseAccount:
    def test_all_fields_wired(self):
        dummy_name = "Current Account"
        dummy_number = "3"
        dummy_owner = "Alice"
        dummy_kind = "0"  # BANK
        dummy_currency = "2"
        dummy_path_icon = "icons/bank.png"
        dummy_bank = "5"
        dummy_bank_branch_code = "00199"
        dummy_bank_account_number = "9876543210"
        dummy_key = "7"
        dummy_bank_account_iban = "GB29NWBK60161331926819"
        dummy_initial_balance = "1500,75"
        dummy_minimum_wanted_balance = "200,00"
        dummy_minimum_authorised_balance = "-300,50"
        dummy_lines_per_transaction = "2"
        dummy_comment = "Main account"
        dummy_owner_address = "42 Rue de la Paix"
        dummy_default_debit_method = "3"
        dummy_default_credit_method = "4"
        dummy_sort_order = "asc"
        dummy_column_sort = "1"
        dummy_sorting_kind_column = "date"
        dummy_bet_use_budget = "1"
        element = _el(
            "Account",
            Name=dummy_name,
            Id="(null)",
            Number=dummy_number,
            Owner=dummy_owner,
            Kind=dummy_kind,
            Currency=dummy_currency,
            Path_icon=dummy_path_icon,
            Bank=dummy_bank,
            Bank_branch_code=dummy_bank_branch_code,
            Bank_account_number=dummy_bank_account_number,
            Key=dummy_key,
            Bank_account_IBAN=dummy_bank_account_iban,
            Initial_balance=dummy_initial_balance,
            Minimum_wanted_balance=dummy_minimum_wanted_balance,
            Minimum_authorised_balance=dummy_minimum_authorised_balance,
            Closed_account="1",
            Show_marked="1",
            Show_archives_lines="1",
            Lines_per_transaction=dummy_lines_per_transaction,
            Comment=dummy_comment,
            Owner_address=dummy_owner_address,
            Default_debit_method=dummy_default_debit_method,
            Default_credit_method=dummy_default_credit_method,
            Sort_by_method="1",
            Neutrals_inside_method="1",
            Sort_order=dummy_sort_order,
            Ascending_sort="0",
            Column_sort=dummy_column_sort,
            Sorting_kind_column=dummy_sorting_kind_column,
            Bet_use_budget=dummy_bet_use_budget,
        )

        section = parse_account_section(element)

        assert section.Name == dummy_name
        assert section.Id is None
        assert section.Number == int(dummy_number)
        assert section.Owner == dummy_owner
        assert section.Kind == AccountKind(int(dummy_kind))
        assert section.Currency == int(dummy_currency)
        assert section.Path_icon == dummy_path_icon
        assert section.Bank == int(dummy_bank)
        assert section.Bank_branch_code == dummy_bank_branch_code
        assert section.Bank_account_number == dummy_bank_account_number
        assert section.Key == dummy_key
        assert section.Bank_account_IBAN == dummy_bank_account_iban
        assert section.Initial_balance == Decimal("1500.75")
        assert section.Minimum_wanted_balance == Decimal("200.00")
        assert section.Minimum_authorised_balance == Decimal("-300.50")
        assert section.Closed_account is True
        assert section.Show_marked is True
        assert section.Show_archives_lines is True
        assert section.Lines_per_transaction == int(dummy_lines_per_transaction)
        assert section.Comment == dummy_comment
        assert section.Owner_address == dummy_owner_address
        assert section.Default_debit_method == int(dummy_default_debit_method)
        assert section.Default_credit_method == int(dummy_default_credit_method)
        assert section.Sort_by_method is True
        assert section.Neutrals_inside_method is True
        assert section.Sort_order == dummy_sort_order
        assert section.Ascending_sort is False
        assert section.Column_sort == int(dummy_column_sort)
        assert section.Sorting_kind_column == dummy_sorting_kind_column
        assert section.Bet_use_budget == int(dummy_bet_use_budget)


class TestParseTransaction:
    def test_all_fields_wired(self):
        dummy_ac = "2"
        dummy_nb = "7"
        dummy_dt = "03/20/2024"
        dummy_am = "99,99"
        dummy_cu = "3"
        dummy_exr = "1,25"
        dummy_exf = "0,50"
        dummy_pa = "4"
        dummy_ca = "5"
        dummy_sca = "6"
        dummy_pn = "8"
        dummy_pc = "CHQ-0042"
        dummy_ma = "3"  # RECONCILED
        dummy_ar = "9"
        dummy_re = "10"
        dummy_fi = "11"
        dummy_bu = "12"
        dummy_sbu = "13"
        dummy_vo = "VOUCH-007"
        dummy_ba = "BANK-REF"
        dummy_trt = "99"
        dummy_mo = "0"
        element = _el(
            "Transaction",
            Ac=dummy_ac,
            Nb=dummy_nb,
            Id="(null)",
            Dt=dummy_dt,
            Dv="(null)",
            Am=dummy_am,
            Cu=dummy_cu,
            Exb="1",
            Exr=dummy_exr,
            Exf=dummy_exf,
            Pa=dummy_pa,
            Ca=dummy_ca,
            Sca=dummy_sca,
            Br="1",
            No="(null)",
            Pn=dummy_pn,
            Pc=dummy_pc,
            Ma=dummy_ma,
            Ar=dummy_ar,
            Au="1",
            Re=dummy_re,
            Fi=dummy_fi,
            Bu=dummy_bu,
            Sbu=dummy_sbu,
            Vo=dummy_vo,
            Ba=dummy_ba,
            Trt=dummy_trt,
            Mo=dummy_mo,
        )

        section = parse_transaction_section(element)

        assert section.Ac == int(dummy_ac)
        assert section.Nb == int(dummy_nb)
        assert section.Id is None
        assert section.Dt == date(2024, 3, 20)
        assert section.Dv is None
        assert section.Am == Decimal("99.99")
        assert section.Cu == int(dummy_cu)
        assert section.Exb is True
        assert section.Exr == Decimal("1.25")
        assert section.Exf == Decimal("0.50")
        assert section.Pa == int(dummy_pa)
        assert section.Ca == int(dummy_ca)
        assert section.Sca == int(dummy_sca)
        assert section.Br is True
        assert section.No is None
        assert section.Pn == int(dummy_pn)
        assert section.Pc == dummy_pc
        assert section.Ma == TransactionMarkedState.RECONCILED
        assert section.Ar == int(dummy_ar)
        assert section.Au is True
        assert section.Re == int(dummy_re)
        assert section.Fi == int(dummy_fi)
        assert section.Bu == int(dummy_bu)
        assert section.Sbu == int(dummy_sbu)
        assert section.Vo == dummy_vo
        assert section.Ba == dummy_ba
        assert section.Trt == int(dummy_trt)
        assert section.Mo == int(dummy_mo)

    def _make_transaction_element(self, **overrides: str) -> ET.Element:
        defaults = dict(
            Ac="1",
            Nb="1",
            Id="(null)",
            Dt="01/15/2023",
            Dv="(null)",
            Am="42,50",
            Cu="1",
            Exb="0",
            Exr="1,00",
            Exf="0,00",
            Pa="2",
            Ca="3",
            Sca="0",
            Br="0",
            No="(null)",
            Pn="1",
            Pc="(null)",
            Ma="0",
            Ar="0",
            Au="0",
            Re="0",
            Fi="0",
            Bu="0",
            Sbu="0",
            Vo="(null)",
            Ba="(null)",
            Trt="0",
            Mo="0",
        )
        defaults.update(overrides)
        return _el("Transaction", **defaults)

    def test_nullable_value_date_field(self):
        element = self._make_transaction_element(Dt="01/15/2023", Dv="(null)")

        section = parse_transaction_section(element)

        assert section.Dt == date(2023, 1, 15)
        assert section.Dv is None

    def test_nullable_transaction_date_field(self):
        element = self._make_transaction_element(Dt="(null)")

        section = parse_transaction_section(element)

        assert section.Dt is None


class TestParseScheduled:
    def test_nullable_date_field(self):
        element = _el(
            "Scheduled",
            Nb="1",
            Dt="03/01/2024",
            Ac="1",
            Am="-50,00",
            Cu="1",
            Pa="0",
            Ca="0",
            Sca="0",
            Tra="0",
            Pn="0",
            CPn="0",
            Pc="(null)",
            Fi="0",
            Bu="0",
            Sbu="0",
            No="(null)",
            Au="0",
            Fd="0",
            Pe="1",
            Pei="1",
            Pep="0",
            Dtl="(null)",
            Br="0",
            Mo="0",
        )

        section = parse_scheduled_section(element)

        assert section.Nb == 1
        assert section.Dt == date(2024, 3, 1)
        assert section.Dtl is None
        assert section.Am == Decimal("-50.00")


class TestParseGeneral:
    def test_required_fields_wired(self):
        dummy_file_version = "2.0"
        dummy_grisbi_version = "3.0.0"
        element = _el(
            "General",
            File_version=dummy_file_version,
            Grisbi_version=dummy_grisbi_version,
            Crypt_file="0",
            Archive_file="0",
            File_title="My Accounts",
            Use_icons_file_dir="0",
            Date_format="%d/%m/%Y",
            Decimal_point=",",
            Thousands_separator=" ",
            Party_list_currency_number="1",
            Category_list_currency_number="1",
            Budget_list_currency_number="1",
            Navigation_list_order="0-1-2",
            Scheduler_view="0",
            Scheduler_custom_number="1",
            Scheduler_custom_menu="0",
            Scheduler_set_default_account="0",
            Scheduler_default_account_number="0",
            Scheduler_set_fixed_date="0",
            Scheduler_default_fixed_date="0",
            Import_interval_search="2",
            Import_copy_payee_in_note="0",
            Import_extract_number_for_check="0",
            Import_fusion_transactions="0",
            Import_categorie_for_payee="0",
            Import_fyear_by_value_date="0",
            Import_qif_no_import_categories="0",
            Import_qif_use_field_extract_method_payment="0",
            Export_file_format="0",
            Export_files_traitement="0",
            Export_force_US_dates="0",
            Export_force_US_numbers="0",
            Export_quote_dates="0",
            Form_date_force_prev_year="0",
            Form_columns_number="2",
            Form_lines_number="5",
            Form_organization="0-1-2",
            Reconcile_end_date="0",
            Reconcile_sort="0",
            Use_logo="0",
            Remind_display_per_account="0",
            Transactions_view="0-1",
            Two_lines_showed="0",
            Three_lines_showed="1",
            Transaction_column_width="50-100",
            Transaction_column_align="0-0",
            Scheduler_column_width="50-100",
            Combofix_mixed_sort="0",
            Combofix_case_sensitive="0",
            Combofix_force_payee="0",
            Combofix_force_category="0",
            Automatic_amount_separator="0",
            CSV_separator=";",
            CSV_force_date_valeur_with_date="0",
            Metatree_sort_transactions="0",
            Metatree_unarchived_payees="0",
            Add_archive_in_total_balance="0",
            Bet_array_column_width="50",
            Bet_capital="0",
            Bet_currency="1",
            Bet_taux_annuel="0,00",
            Bet_index_duree="0",
            Bet_frais="0,00",
            Bet_type_taux="0",
        )

        section = parse_general_section(element)

        assert section.File_version == dummy_file_version
        assert section.Grisbi_version == dummy_grisbi_version
        assert section.Crypt_file is False
        assert section.Import_ope_nbre_max is None
        assert section.Metatree_assoc_mode is None
        assert section.Force_credit_before_debit is None
        assert section.One_line_showed is None

    def test_optional_attributes_parsed_when_present(self):
        element = _el(
            "General",
            File_version="2.0",
            Grisbi_version="3.0.0",
            Crypt_file="0",
            Archive_file="0",
            File_title="My Accounts",
            Use_icons_file_dir="0",
            Date_format="%d/%m/%Y",
            Decimal_point=",",
            Thousands_separator=" ",
            Party_list_currency_number="1",
            Category_list_currency_number="1",
            Budget_list_currency_number="1",
            Navigation_list_order="0-1-2",
            Scheduler_view="0",
            Scheduler_custom_number="1",
            Scheduler_custom_menu="0",
            Scheduler_set_default_account="0",
            Scheduler_default_account_number="0",
            Scheduler_set_fixed_date="0",
            Scheduler_default_fixed_date="0",
            Import_interval_search="2",
            **{"Import-ope-nbre-max": "50"},
            Import_copy_payee_in_note="0",
            Import_extract_number_for_check="0",
            Import_fusion_transactions="0",
            Import_categorie_for_payee="0",
            Import_fyear_by_value_date="0",
            Import_qif_no_import_categories="0",
            Import_qif_use_field_extract_method_payment="0",
            Export_file_format="0",
            Export_files_traitement="0",
            Export_force_US_dates="0",
            Export_force_US_numbers="0",
            Export_quote_dates="0",
            Form_date_force_prev_year="0",
            Form_columns_number="2",
            Form_lines_number="5",
            Form_organization="0-1-2",
            Reconcile_end_date="0",
            Reconcile_sort="0",
            Use_logo="0",
            Remind_display_per_account="0",
            Transactions_view="0-1",
            One_line_showed="1",
            Two_lines_showed="0",
            Three_lines_showed="1",
            Transaction_column_width="50-100",
            Transaction_column_align="0-0",
            Scheduler_column_width="50-100",
            Combofix_mixed_sort="0",
            Combofix_case_sensitive="0",
            Combofix_force_payee="0",
            Combofix_force_category="0",
            Automatic_amount_separator="0",
            CSV_separator=";",
            CSV_force_date_valeur_with_date="0",
            Metatree_assoc_mode="2",
            Metatree_sort_transactions="0",
            Metatree_unarchived_payees="0",
            Add_archive_in_total_balance="0",
            **{"Force-credit-before-debit": "1"},
            Bet_array_column_width="50",
            Bet_capital="0",
            Bet_currency="1",
            Bet_taux_annuel="0,00",
            Bet_index_duree="0",
            Bet_frais="0,00",
            Bet_type_taux="0",
        )

        section = parse_general_section(element)

        assert section.Import_ope_nbre_max == 50
        assert section.One_line_showed is True
        assert section.Metatree_assoc_mode == 2
        assert section.Force_credit_before_debit is True


class TestParseArchiveNullableDates:
    def test_null_dates_become_none(self):
        element = _el(
            "Archive",
            Nb="1",
            Na="2022 Archive",
            Bdte="(null)",
            Edte="(null)",
            Fye="0",
            Rep="(null)",
        )

        section = parse_archive_section(element)

        assert section.Bdte is None
        assert section.Edte is None
        assert section.Rep is None

    def test_dates_parsed_when_present(self):
        dummy_bdte = "01/01/2022"
        dummy_edte = "12/31/2022"
        element = _el(
            "Archive",
            Nb="1",
            Na="2022 Archive",
            Bdte=dummy_bdte,
            Edte=dummy_edte,
            Fye="1",
            Rep="(null)",
        )

        section = parse_archive_section(element)

        assert section.Bdte == date(2022, 1, 1)
        assert section.Edte == date(2022, 12, 31)


# Smoke tests for the remaining parsers — verify they parse without error.
# Field-level correctness is covered by the parsers.py tests (Layer 1) and
# the full-file integration tests (Layer 3+).


@pytest.mark.parametrize(
    "parse_fn, tag, attrib",
    [
        (
            parse_rgba_section,
            "RGBA",
            {
                "Background_color_0": "(null)",
                "Background_color_1": "(null)",
                "Couleur_jour": "(null)",
                "Background_scheduled": "(null)",
                "Background_archive": "(null)",
                "Selection": "(null)",
                "Background_split": "(null)",
                "Text_color_0": "(null)",
                "Text_color_1": "(null)",
                "Couleur_bet_division": "(null)",
                "Couleur_bet_future": "(null)",
                "Couleur_bet_solde": "(null)",
                "Couleur_bet_transfert": "(null)",
            },
        ),
        (
            parse_print_section,
            "Print",
            {
                "Draw_lines": "1",
                "Draw_column": "0",
                "Draw_archives": "1",
                "Draw_columns_name": "1",
                "Draw_background": "0",
                "Draw_title": "1",
                "Draw_interval_dates": "0",
                "Draw_dates_are_value_dates": "0",
                "Font_transactions": "Monospace 8",
                "Font_title": "Sans Bold 10",
                "Report_font_transactions": "Monospace 8",
                "Report_font_title": "Sans Bold 10",
            },
        ),
        (
            parse_bank_section,
            "Bank",
            {
                "Nb": "1",
                "Na": "HSBC",
                "Co": "HSBC Bank",
                "BIC": "HBUKGB4B",
                "Adr": "London",
                "Tel": "+44 20 1234 5678",
                "Mail": "(null)",
                "Web": "(null)",
                "Rem": "(null)",
                "Nac": "Jane Smith",
                "Faxc": "",
                "Telc": "+44 20 9876 5432",
                "Mailc": "jane@hsbc.example.com",
            },
        ),
        (
            parse_financial_year_section,
            "Financial_year",
            {
                "Nb": "1",
                "Na": "2023",
                "Bdte": "01/01/2023",
                "Edte": "12/31/2023",
                "Sho": "1",
            },
        ),
        (
            parse_reconcile_section,
            "Reconcile",
            {
                "Nb": "1",
                "Na": "Jan 2023",
                "Acc": "1",
                "Idate": "01/01/2023",
                "Fdate": "01/31/2023",
                "Ibal": "500,00",
                "Fbal": "650,00",
            },
        ),
        (
            parse_reconcile_section,
            "Reconcile",
            {
                "Nb": "1",
                "Na": "(null)",
                "Acc": "1",
                "Idate": "(null)",
                "Fdate": "(null)",
                "Ibal": "500,00",
                "Fbal": "650,00",
            },
        ),
        (
            parse_currency_link_section,
            "Currency_link",
            {
                "Nb": "1",
                "Cu1": "1",
                "Cu2": "2",
                "Ex": "1,18",
                "Fl": "0",
            },
        ),
        (
            parse_partial_balance_section,
            "Partial_balance",
            {
                "Nb": "1",
                "Na": "Savings",
                "Acc": "1;2",
                "Kind": "0",
                "Currency": "1",
                "Colorise": "0",
            },
        ),
        (
            parse_payment_section,
            "Payment",
            {
                "Number": "1",
                "Name": "Cheque",
                "Sign": "-1",
                "Show_entry": "1",
                "Automatic_number": "1",
                "Current_number": "42",
                "Account": "0",
            },
        ),
        (
            parse_bet_section,
            "Bet",
            {"Ddte": "0", "Bet_deb_cash_account_option": "0"},
        ),
        (
            parse_bet_graph_section,
            "Bet_graph",
            {"prefs": "0"},
        ),
        (
            parse_bet_historical_section,
            "Bet_historical",
            {
                "Nb": "1",
                "Ac": "1",
                "Ori": "0",
                "Edit": "0",
                "Damount": "0,00",
                "Div": "1",
                "SDiv": "0",
                "SEdit": "0",
                "SDamount": "0,00",
            },
        ),
        (
            parse_bet_future_section,
            "Bet_future",
            {
                "Nb": "1",
                "Dt": "01/01/2024",
                "Ac": "1",
                "Am": "100,00",
                "Pa": "0",
                "IsT": "0",
                "Tra": "0",
                "Ca": "0",
                "Sca": "0",
                "Pn": "0",
                "Fi": "0",
                "Bu": "0",
                "Sbu": "0",
                "No": "(null)",
                "Au": "0",
                "Pe": "1",
                "Pei": "1",
                "Pep": "0",
                "Dtl": "(null)",
                "Mo": "0",
            },
        ),
        (
            parse_bet_loan_section,
            "Bet_loan",
            {
                "Nb": "1",
                "Ac": "1",
                "Ver": "1",
                "InCol": "1",
                "Ca": "100000,00",
                "Duree": "240",
                "FDate": "01/01/2020",
                "Fees": "500,00",
                "Taux": "1,50",
                "TyTaux": "0",
                "NbreDec": "2",
                "FEchDif": "0",
                "FCa": "0,00",
                "FIn": "0,00",
                "OEch": "0,00",
                "ISchWL": "0",
                "AAc": "0",
                "ASch": "0",
                "AFr": "0",
                "CaDu": "0,00",
            },
        ),
        (
            parse_bet_transfert_section,
            "Bet_transfert",
            {
                "Nb": "1",
                "Dt": "01/01/2024",
                "Ac": "1",
                "Ty": "0",
                "Ra": "0",
                "Rt": "0",
                "Dd": "0",
                "Dtb": "01/01/2024",
                "Mlbd": "0",
                "Pa": "0",
                "Pn": "0",
                "Ca": "0",
                "Sca": "0",
                "Bu": "0",
                "Sbu": "0",
                "CPa": "0",
                "CCa": "0",
                "CSca": "0",
                "CBu": "0",
                "CSbu": "0",
            },
        ),
        (
            parse_import_rule_section,
            "Import_rule",
            {
                "Nb": "1",
                "Na": "My Bank",
                "Acc": "1",
                "Cur": "1",
                "Inv": "0",
                "Enc": "UTF-8",
                "Fil": "ofx",
                "Act": "0",
                "Typ": "0",
                "IdC": "0",
                "IdR": "0",
                "FiS": "",
                "Fld": "0",
                "Hp": "0",
                "Sep": ";",
                "SkiS": "0",
                "SpL": "0",
            },
        ),
        (
            parse_special_line_section,
            "Special_line",
            {
                "Nb": "1",
                "NuR": "1",
                "SpA": "0",
                "SpAD": "0",
                "SpUD": "0",
                "SpUT": "0",
            },
        ),
        (
            parse_text_comparison_section,
            "Text_comparison",
            {
                "Comparison_number": "1",
                "Report_nb": "2",
                "Last_comparison": "-1",
                "Object": "0",
                "Operator": "0",
                "Text": "salary",
                "Use_text": "1",
                "Comparison_1": "0",
                "Link_1_2": "0",
                "Comparison_2": "0",
                "Amount_1": "0,00",
                "Amount_2": "0,00",
            },
        ),
        (
            parse_amount_comparison_section,
            "Amount_comparison",
            {
                "Comparison_number": "1",
                "Report_nb": "2",
                "Last_comparison": "-1",
                "Comparison_1": "0",
                "Link_1_2": "0",
                "Comparison_2": "0",
                "Amount_1": "100,00",
                "Amount_2": "500,00",
            },
        ),
    ],
)
def test_section_parser_smoke(parse_fn, tag, attrib):
    element = _el(tag, **attrib)
    section = parse_fn(element)
    assert section is not None
