"""Layer 5: pandas adapter tests — dtype and projection behaviour."""

from datetime import date, datetime
from decimal import Decimal

from gsbparse.adapters.pandas._detailed_transactions import detailed_transactions_to_df
from gsbparse.adapters.pandas._sections import sections_to_df
from gsbparse.domain.detailed_transaction import (
    DetailedTransactionColumn,
    build_detailed_transactions,
)
from gsbparse.domain.file import GsbFile
from gsbparse.domain.sections.account import Account, AccountKind
from gsbparse.domain.sections.currency import Currency
from gsbparse.domain.sections.transaction import Transaction, TransactionMarkedState


def _dummy_account(number: int = 1) -> Account:
    return Account(
        Name="Checking",
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


def _dummy_currency(nb: int = 1) -> Currency:
    return Currency(Nb=nb, Na="Euro", Co="E", Ico="EUR", Fl=2)


def _minimal_gsb(
    transactions: list[Transaction],
) -> GsbFile:
    return GsbFile(
        general=None,
        rgba=None,
        print_settings=None,
        currencies=[_dummy_currency()],
        accounts=[_dummy_account()],
        banks=None,
        parties=None,
        payment_methods=None,
        transactions=transactions,
        scheduled=None,
        categories=None,
        sub_categories=None,
        budgetaries=None,
        sub_budgetaries=None,
        currency_links=None,
        financial_years=None,
        archives=None,
        reconciles=None,
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


def _dummy_transaction(nb: int = 1, dt: date | None = None, dv: date | None = None) -> Transaction:
    return Transaction(
        Nb=nb,
        Ac=1,
        Id=None,
        Dt=dt,
        Dv=dv,
        Am=Decimal("10.00"),
        Cu=1,
        Exb=False,
        Exr=Decimal("1"),
        Exf=Decimal("0"),
        Pa=0,
        Ca=0,
        Sca=0,
        Br=False,
        No=None,
        Pn=0,
        Pc=None,
        Ma=TransactionMarkedState.NEW,
        Ar=0,
        Au=False,
        Re=0,
        Fi=0,
        Bu=0,
        Sbu=0,
        Vo=None,
        Ba=None,
        Trt=0,
        Mo=0,
    )


class TestDetailedTransactionsDfDateTypes:
    def test_datetime_is_normalized_to_date(self):
        # Arrange — datetime is a subclass of date; the adapter must strip the time part.
        dummy_datetime = datetime(2023, 6, 15, 10, 30, 0)
        tx = _dummy_transaction(dt=dummy_datetime)
        detailed = build_detailed_transactions(_minimal_gsb([tx]))
        assert detailed is not None
        cols = [DetailedTransactionColumn("Dt", "date")]

        # Act
        df = detailed_transactions_to_df(detailed, columns=cols)

        # Assert
        assert type(df["date"].iloc[0]) is date
        assert df["date"].iloc[0] == date(2023, 6, 15)

    def test_date_column_contains_python_date_objects(self):
        # Arrange
        dummy_date = date(2023, 6, 15)
        tx = _dummy_transaction(dt=dummy_date)
        detailed = build_detailed_transactions(_minimal_gsb([tx]))
        assert detailed is not None
        cols = [DetailedTransactionColumn("Dt", "date")]

        # Act
        df = detailed_transactions_to_df(detailed, columns=cols)

        # Assert
        assert type(df["date"].iloc[0]) is date

    def test_null_date_column_is_none(self):
        # Arrange
        tx = _dummy_transaction(dt=None)
        detailed = build_detailed_transactions(_minimal_gsb([tx]))
        assert detailed is not None
        cols = [DetailedTransactionColumn("Dt", "date")]

        # Act
        df = detailed_transactions_to_df(detailed, columns=cols)

        # Assert
        assert df["date"].iloc[0] is None

    def test_value_date_column_contains_python_date_objects(self):
        # Arrange
        dummy_value_date = date(2023, 6, 20)
        tx = _dummy_transaction(dv=dummy_value_date)
        detailed = build_detailed_transactions(_minimal_gsb([tx]))
        assert detailed is not None
        cols = [DetailedTransactionColumn("Dv", "value_date")]

        # Act
        df = detailed_transactions_to_df(detailed, columns=cols)

        # Assert
        assert type(df["value_date"].iloc[0]) is date


class TestSectionsDfDateTypes:
    def test_datetime_is_normalized_to_date(self):
        # Arrange — datetime is a subclass of date; the adapter must strip the time part.
        dummy_datetime = datetime(2023, 6, 15, 10, 30, 0)
        tx = _dummy_transaction(dt=dummy_datetime)

        # Act
        df = sections_to_df([tx])

        # Assert
        assert type(df["Dt"].iloc[0]) is date
        assert df["Dt"].iloc[0] == date(2023, 6, 15)

    def test_transaction_dt_column_contains_python_date_objects(self):
        # Arrange
        dummy_date = date(2023, 6, 15)
        tx = _dummy_transaction(dt=dummy_date)

        # Act
        df = sections_to_df([tx])

        # Assert
        assert type(df["Dt"].iloc[0]) is date

    def test_transaction_dv_column_contains_python_date_objects(self):
        # Arrange
        dummy_value_date = date(2023, 6, 20)
        tx = _dummy_transaction(dv=dummy_value_date)

        # Act
        df = sections_to_df([tx])

        # Assert
        assert type(df["Dv"].iloc[0]) is date
