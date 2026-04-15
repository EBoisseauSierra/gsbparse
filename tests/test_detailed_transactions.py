"""Layer 4: DetailedTransaction FK-resolution unit tests."""

from datetime import date
from decimal import Decimal

import pytest

from gsbparse.domain.detailed_transaction import (
    DetailedTransaction,
    DetailedTransactionColumn,
    build_detailed_transactions,
    validate_columns,
)
from gsbparse.domain.errors import UnknownDetailedTransactionPathError
from gsbparse.domain.file import GsbFile
from gsbparse.domain.sections.account import AccountKind, AccountSection
from gsbparse.domain.sections.bank import BankSection
from gsbparse.domain.sections.budgetary import BudgetarySection
from gsbparse.domain.sections.category import CategoryKind, CategorySection
from gsbparse.domain.sections.currency import CurrencySection
from gsbparse.domain.sections.party import PartySection
from gsbparse.domain.sections.payment import PaymentSection
from gsbparse.domain.sections.reconcile import ReconcileSection
from gsbparse.domain.sections.sub_budgetary import SubBudgetarySection
from gsbparse.domain.sections.sub_category import SubCategorySection
from gsbparse.domain.sections.transaction import TransactionMarkedState, TransactionSection


def _dummy_account(number: int = 1, name: str = "Checking") -> AccountSection:
    return AccountSection(
        Name=name,
        Id=None,
        Number=number,
        Owner="",
        Kind=AccountKind.BANK,
        Currency=1,
        Path_icon="",
        Bank=0,
        Bank_branch_code="",
        Bank_account_number="",
        Key="",
        Bank_account_IBAN="",
        Initial_balance=Decimal("0"),
        Minimum_wanted_balance=Decimal("0"),
        Minimum_authorised_balance=Decimal("0"),
        Closed_account=False,
        Show_marked=False,
        Show_archives_lines=False,
        Lines_per_transaction=1,
        Comment="",
        Owner_address="",
        Default_debit_method=1,
        Default_credit_method=1,
        Sort_by_method=False,
        Neutrals_inside_method=False,
        Sort_order="",
        Ascending_sort=True,
        Column_sort=0,
        Sorting_kind_column="",
        Bet_use_budget=0,
    )


def _dummy_currency(nb: int = 1, na: str = "Euro") -> CurrencySection:
    return CurrencySection(Nb=nb, Na=na, Co="E", Ico="EUR", Fl=2)


def _dummy_party(nb: int = 1, na: str = "Supermarket") -> PartySection:
    return PartySection(Nb=nb, Na=na, Txt=None, Search=None, IgnCase=False, UseRegex=False)


def _dummy_category(nb: int = 1, na: str = "Food") -> CategorySection:
    return CategorySection(Nb=nb, Na=na, Kd=CategoryKind.INCOME)


def _dummy_sub_category(nb: int = 1, na: str = "Groceries", nbc: int = 1) -> SubCategorySection:
    return SubCategorySection(Nb=nb, Na=na, Nbc=nbc)


def _dummy_budgetary(nb: int = 1, na: str = "Household") -> BudgetarySection:
    return BudgetarySection(Nb=nb, Na=na, Kd=CategoryKind.EXPENSE)


def _dummy_sub_budgetary(nb: int = 1, na: str = "Groceries", nbb: int = 1) -> SubBudgetarySection:
    return SubBudgetarySection(Nb=nb, Na=na, Nbb=nbb)


def _dummy_transaction(
    nb: int = 1,
    ac: int = 1,
    cu: int = 1,
    pa: int = 0,
    ca: int = 0,
    sca: int = 0,
    bu: int = 0,
    sbu: int = 0,
    trt: int = 0,
) -> TransactionSection:
    return TransactionSection(
        Nb=nb,
        Ac=ac,
        Id=None,
        Dt=date(2023, 1, 15),
        Dv=None,
        Am=Decimal("42.50"),
        Cu=cu,
        Exb=False,
        Exr=Decimal("1"),
        Exf=Decimal("0"),
        Pa=pa,
        Ca=ca,
        Sca=sca,
        Br=False,
        No=None,
        Pn=0,
        Pc=None,
        Ma=TransactionMarkedState.NEW,
        Ar=0,
        Au=False,
        Re=0,
        Fi=0,
        Bu=bu,
        Sbu=sbu,
        Vo=None,
        Ba=None,
        Trt=trt,
        Mo=0,
    )


def _minimal_gsb_file(
    transactions: list[TransactionSection] | None = None,
    accounts: list[AccountSection] | None = None,
    currencies: list[CurrencySection] | None = None,
    parties: list[PartySection] | None = None,
    categories: list[CategorySection] | None = None,
    sub_categories: list[SubCategorySection] | None = None,
    budgetaries: list[BudgetarySection] | None = None,
    sub_budgetaries: list[SubBudgetarySection] | None = None,
    banks: list[BankSection] | None = None,
    payment_methods: list[PaymentSection] | None = None,
    reconciles: list[ReconcileSection] | None = None,
) -> GsbFile:
    return GsbFile(
        general=None,
        rgba=None,
        print_settings=None,
        currencies=currencies,
        accounts=accounts,
        banks=banks,
        parties=parties,
        payment_methods=payment_methods,
        transactions=transactions,
        scheduled=None,
        categories=categories,
        sub_categories=sub_categories,
        budgetaries=budgetaries,
        sub_budgetaries=sub_budgetaries,
        currency_links=None,
        financial_years=None,
        archives=None,
        reconciles=reconciles,
        import_rules=None,
        special_lines=None,
        partial_balances=None,
        bet=None,
        bet_graphs=None,
        bet_historicals=None,
        bet_futures=None,
        bet_transferts=None,
        bet_loans=None,
        reports=None,
        text_comparisons=None,
        amount_comparisons=None,
    )


class TestBuildDetailedTransactions:
    def test_returns_none_when_no_transactions(self):
        gsb = _minimal_gsb_file()
        assert build_detailed_transactions(gsb) is None

    def test_resolves_account_and_currency(self):
        dummy_account = _dummy_account(number=1, name="Checking")
        dummy_currency = _dummy_currency(nb=1, na="Euro")
        dummy_tx = _dummy_transaction(nb=1, ac=1, cu=1)
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[dummy_account],
            currencies=[dummy_currency],
        )

        result = build_detailed_transactions(gsb)

        assert result is not None
        assert len(result) == 1
        assert result[0].Ac is dummy_account
        assert result[0].Cu is dummy_currency

    def test_resolves_optional_party(self):
        dummy_account = _dummy_account()
        dummy_currency = _dummy_currency()
        dummy_party = _dummy_party(nb=5, na="Supermarket")
        dummy_tx = _dummy_transaction(pa=5)
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[dummy_account],
            currencies=[dummy_currency],
            parties=[dummy_party],
        )

        result = build_detailed_transactions(gsb)

        assert result is not None
        assert result[0].Pa is dummy_party

    def test_zero_party_resolves_to_none(self):
        dummy_account = _dummy_account()
        dummy_currency = _dummy_currency()
        dummy_tx = _dummy_transaction(pa=0)
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[dummy_account],
            currencies=[dummy_currency],
        )

        result = build_detailed_transactions(gsb)

        assert result is not None
        assert result[0].Pa is None

    def test_missing_account_skips_transaction(self, caplog):
        import logging

        dummy_currency = _dummy_currency()
        dummy_tx = _dummy_transaction(ac=99)  # account 99 doesn't exist
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[_dummy_account(number=1)],
            currencies=[dummy_currency],
        )

        with caplog.at_level(logging.WARNING):
            result = build_detailed_transactions(gsb)

        assert result is None  # skipped transaction → empty → None
        assert any("account" in r.message.lower() for r in caplog.records)

    def test_transfer_target_resolved(self):
        # Two transactions that form a transfer pair: each Trt points to the other's Nb.
        dummy_account_1 = _dummy_account(number=1, name="Checking")
        dummy_account_2 = _dummy_account(number=2, name="Savings")
        dummy_currency = _dummy_currency()
        dummy_tx_a = _dummy_transaction(nb=1, ac=1, trt=2)
        dummy_tx_b = _dummy_transaction(nb=2, ac=2, trt=1)
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx_a, dummy_tx_b],
            accounts=[dummy_account_1, dummy_account_2],
            currencies=[dummy_currency],
        )

        result = build_detailed_transactions(gsb)

        assert result is not None
        result_a = next(tx for tx in result if tx.Nb == 1)
        result_b = next(tx for tx in result if tx.Nb == 2)
        assert result_a.Trt is not None
        assert result_a.Trt.Nb == 2
        assert result_a.Trt.Trt is None  # no infinite nesting
        assert result_b.Trt is not None
        assert result_b.Trt.Nb == 1
        assert result_b.Trt.Trt is None  # no infinite nesting

    def test_shared_account_identity_preserved(self):
        dummy_account = _dummy_account(number=1)
        dummy_currency = _dummy_currency()
        dummy_tx_a = _dummy_transaction(nb=1, ac=1)
        dummy_tx_b = _dummy_transaction(nb=2, ac=1)
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx_a, dummy_tx_b],
            accounts=[dummy_account],
            currencies=[dummy_currency],
        )

        result = build_detailed_transactions(gsb)

        assert result is not None
        assert result[0].Ac is result[1].Ac


class TestValidateColumns:
    def test_valid_top_level_path_accepted(self):
        cols = [DetailedTransactionColumn("Am", "amount")]
        validate_columns(cols)  # should not raise

    def test_valid_dotted_path_accepted(self):
        cols = [DetailedTransactionColumn("Ac.Name", "account")]
        validate_columns(cols)  # should not raise

    def test_invalid_top_level_path_raises(self):
        cols = [DetailedTransactionColumn("NonExistent", "x")]
        with pytest.raises(UnknownDetailedTransactionPathError):
            validate_columns(cols)


class TestDetailedTransactionViaProperty:
    def test_gsb_file_property_delegates_correctly(self):
        dummy_account = _dummy_account()
        dummy_currency = _dummy_currency()
        dummy_tx = _dummy_transaction()
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[dummy_account],
            currencies=[dummy_currency],
        )

        result = gsb.detailed_transactions

        assert result is not None
        assert isinstance(result[0], DetailedTransaction)


class TestDetailedSubCategorySection:
    def test_sub_category_nbc_resolves_to_category(self):
        # Arrange
        dummy_category = _dummy_category(nb=3, na="Transport")
        dummy_sub_category = _dummy_sub_category(nb=2, na="Bus", nbc=3)
        dummy_account = _dummy_account()
        dummy_currency = _dummy_currency()
        dummy_tx = _dummy_transaction(ca=3, sca=2)
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[dummy_account],
            currencies=[dummy_currency],
            categories=[dummy_category],
            sub_categories=[dummy_sub_category],
        )

        # Act
        result = build_detailed_transactions(gsb)

        # Assert
        assert result is not None
        assert result[0].Sca is not None
        assert result[0].Sca.Na == "Bus"
        assert result[0].Sca.Nbc is dummy_category

    def test_sub_categories_sharing_nb_are_disambiguated_by_parent(self):
        # Two sub-categories have the same Nb=1 but different parent categories.
        dummy_shared_nb = 1
        dummy_cat_a = _dummy_category(nb=1, na="Food")
        dummy_cat_b = _dummy_category(nb=2, na="Transport")
        dummy_sca_a = SubCategorySection(Nb=dummy_shared_nb, Na="Groceries", Nbc=dummy_cat_a.Nb)
        dummy_sca_b = SubCategorySection(Nb=dummy_shared_nb, Na="Bus", Nbc=dummy_cat_b.Nb)
        dummy_account = _dummy_account()
        dummy_currency = _dummy_currency()
        dummy_tx = _dummy_transaction(ca=dummy_cat_b.Nb, sca=dummy_shared_nb)  # wants Transport/Bus
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[dummy_account],
            currencies=[dummy_currency],
            categories=[dummy_cat_a, dummy_cat_b],
            sub_categories=[dummy_sca_a, dummy_sca_b],
        )

        result = build_detailed_transactions(gsb)

        assert result is not None
        assert result[0].Sca is not None
        assert result[0].Sca.Na == "Bus"
        assert result[0].Sca.Nbc is dummy_cat_b


class TestDetailedSubBudgetarySection:
    def test_sub_budgetary_nbb_resolves_to_budgetary(self):
        # Arrange
        dummy_budget = _dummy_budgetary(nb=4, na="Living")
        dummy_sub_budget = _dummy_sub_budgetary(nb=1, na="Rent", nbb=4)
        dummy_account = _dummy_account()
        dummy_currency = _dummy_currency()
        dummy_tx = _dummy_transaction(bu=dummy_budget.Nb, sbu=dummy_sub_budget.Nb)
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[dummy_account],
            currencies=[dummy_currency],
            budgetaries=[dummy_budget],
            sub_budgetaries=[dummy_sub_budget],
        )

        # Act
        result = build_detailed_transactions(gsb)

        # Assert
        assert result is not None
        assert result[0].Sbu is not None
        assert result[0].Sbu.Na == "Rent"
        assert result[0].Sbu.Nbb is dummy_budget

    def test_sub_budgetaries_sharing_nb_are_disambiguated_by_parent(self):
        dummy_shared_nb = 1
        dummy_bu_a = _dummy_budgetary(nb=1, na="Household")
        dummy_bu_b = _dummy_budgetary(nb=2, na="Work")
        dummy_sbu_a = SubBudgetarySection(Nb=dummy_shared_nb, Na="Rent", Nbb=dummy_bu_a.Nb)
        dummy_sbu_b = SubBudgetarySection(Nb=dummy_shared_nb, Na="Office", Nbb=dummy_bu_b.Nb)
        dummy_account = _dummy_account()
        dummy_currency = _dummy_currency()
        dummy_tx = _dummy_transaction(bu=dummy_bu_b.Nb, sbu=dummy_shared_nb)  # wants Work/Office
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[dummy_account],
            currencies=[dummy_currency],
            budgetaries=[dummy_bu_a, dummy_bu_b],
            sub_budgetaries=[dummy_sbu_a, dummy_sbu_b],
        )

        result = build_detailed_transactions(gsb)

        assert result is not None
        assert result[0].Sbu is not None
        assert result[0].Sbu.Na == "Office"
        assert result[0].Sbu.Nbb is dummy_bu_b
