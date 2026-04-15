"""Layer 5: End-to-end tests against Example_3.0-en.gsb.

These tests assert on precise values from the real file. They exist to verify
that the full pipeline — XML parsing, dispatch, FK resolution — produces the
correct output. Any change to parsing logic that causes a diff here is a
regression to investigate.

The example file uses Grisbi 3.0.3 / format version 2.0.0.
"""

from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

import gsbparse
from gsbparse.domain.sections.account import AccountKind

EXAMPLE_FILE = Path(__file__).parent / "assets" / "example_3.0_en.gsb"


@pytest.fixture(scope="module")
def gsb():
    return gsbparse.read_gsb(EXAMPLE_FILE)


@pytest.fixture(scope="module")
def detailed(gsb):
    return gsb.detailed_transactions


class TestGeneralSection:
    def test_file_version(self, gsb):
        assert gsb.general is not None
        assert gsb.general.File_version == "2.0.0"

    def test_grisbi_version(self, gsb):
        assert gsb.general is not None
        assert gsb.general.Grisbi_version == "3.0.3"

    def test_import_interval_search(self, gsb):
        assert gsb.general is not None
        assert gsb.general.Import_interval_search == 2


class TestCurrencies:
    def test_currency_count(self, gsb):
        assert gsb.currencies is not None
        assert len(gsb.currencies) == 1

    def test_first_currency(self, gsb):
        assert gsb.currencies is not None
        currency = gsb.currencies[0]
        assert currency.Nb == 1
        assert currency.Na == "Pound Sterling"
        assert currency.Ico == "GBP"


class TestAccounts:
    def test_account_count(self, gsb):
        assert gsb.accounts is not None
        assert len(gsb.accounts) == 6

    def test_first_account_name(self, gsb):
        assert gsb.accounts is not None
        assert gsb.accounts[0].Name == "Mr. Account / HSBC [bank]"
        assert gsb.accounts[0].Number == 1

    def test_fourth_account_is_loan(self, gsb):
        assert gsb.accounts is not None
        account_4 = next(a for a in gsb.accounts if a.Number == 4)
        assert account_4.Name == "Real Estate Loan [liabilities]"
        assert account_4.Kind == AccountKind.LIABILITIES


class TestTransactions:
    def test_transaction_count(self, gsb):
        assert gsb.transactions is not None
        assert len(gsb.transactions) == 141

    def test_first_transaction_fields(self, gsb):
        assert gsb.transactions is not None
        tx = gsb.transactions[0]
        assert tx.Nb == 15
        assert tx.Dt == date(2023, 1, 2)
        assert tx.Am == Decimal("-200000.00")
        assert tx.Ac == 4
        assert tx.Cu == 1
        assert tx.Pa == 4


class TestDetailedTransactions:
    def test_count_matches_transactions(self, gsb, detailed):
        assert detailed is not None
        assert gsb.transactions is not None
        assert len(detailed) == len(gsb.transactions)

    def test_first_detailed_transaction_resolved_fields(self, detailed):
        assert detailed is not None
        tx = detailed[0]
        assert tx.Nb == 15
        assert tx.Dt == date(2023, 1, 2)
        assert tx.Am == Decimal("-200000.00")
        assert tx.Ac.Name == "Real Estate Loan [liabilities]"
        assert tx.Cu.Na == "Pound Sterling"
        assert tx.Pa is not None
        assert tx.Pa.Na == "Loan Credit"

    def test_transfer_target_resolves_to_contra_transaction(self, detailed):
        # Nb=16 (Ac=1) and Nb=15 (Ac=4) form a transfer pair; each Trt points to the other.
        assert detailed is not None
        tx_16 = next(tx for tx in detailed if tx.Nb == 16)
        assert tx_16.Trt is not None
        assert tx_16.Trt.Nb == 15
        assert tx_16.Trt.Trt is None  # no infinite nesting

    def test_all_transactions_have_parties_in_example_file(self, detailed):
        # The example file has a party for every transaction.
        assert detailed is not None
        assert all(tx.Pa is not None for tx in detailed)

    def test_shared_currency_identity(self, detailed):
        # All transactions use the same currency object (Nb=1)
        assert detailed is not None
        currencies = {id(tx.Cu) for tx in detailed}
        assert len(currencies) == 1  # all share the same CurrencySection instance

    def test_account_currency_resolves(self, detailed):
        # All accounts use GBP (Currency=1). Verify via the first transaction (Nb=15, Ac=4).
        assert detailed is not None
        tx_15 = next(tx for tx in detailed if tx.Nb == 15)
        assert tx_15.Ac.Currency.Ico == "GBP"
        assert tx_15.Ac.Currency.Na == "Pound Sterling"

    def test_account_bank_resolves(self, detailed):
        # Transaction Nb=15 belongs to account 4 (Bank=1 = "HSBC UK Bank").
        assert detailed is not None
        tx_15 = next(tx for tx in detailed if tx.Nb == 15)
        assert tx_15.Ac.Bank is not None
        assert tx_15.Ac.Bank.Na == "HSBC UK Bank"

    def test_sub_category_parent_resolves(self, detailed):
        # Transaction Nb=20: Ca=15 ("Financial expenses"), Sca=3 ("Loan/Mortgage").
        assert detailed is not None
        tx_20 = next(tx for tx in detailed if tx.Nb == 20)
        assert tx_20.Sca is not None
        assert tx_20.Sca.Na == "Loan/Mortgage"
        assert tx_20.Sca.Nbc.Na == "Financial expenses"

    def test_reconcile_account_resolves(self, detailed):
        # Transaction Nb=127: Re=1 (reconcile "delayed-debit-card-[liabilities]-1", Acc=5).
        assert detailed is not None
        tx_127 = next(tx for tx in detailed if tx.Nb == 127)
        assert tx_127.Re is not None
        assert tx_127.Re.Na == "delayed-debit-card-[liabilities]-1"
        assert tx_127.Re.Acc.Name == "Delayed Debit card [liabilities]"

    def test_shared_detailed_account_identity(self, detailed):
        # Transactions on the same account share the same DetailedAccountSection instance.
        assert detailed is not None
        account_1_txs = [tx for tx in detailed if tx.Ac.Number == 1]
        assert len(account_1_txs) > 1  # sanity check
        ids = {id(tx.Ac) for tx in account_1_txs}
        assert len(ids) == 1


class TestPandasAdapter:
    def test_currencies_to_df(self, gsb):
        from gsbparse.pandas import to_df

        assert gsb.currencies is not None
        df = to_df(gsb.currencies)
        assert len(df) == 1
        assert df["Na"].iloc[0] == "Pound Sterling"

    def test_accounts_to_df_shape(self, gsb):
        from gsbparse.pandas import to_df

        assert gsb.accounts is not None
        df = to_df(gsb.accounts)
        assert len(df) == 6
        assert "Name" in df.columns

    def test_detailed_transactions_default_columns(self, gsb, detailed):
        from gsbparse.pandas import to_df

        assert detailed is not None
        df = to_df(detailed)
        assert len(df) == 141
        assert "account" in df.columns
        assert "currency" in df.columns
        assert "amount" in df.columns
        assert df["currency"].iloc[0] == "Pound Sterling"
        assert df["account"].iloc[0] == "Real Estate Loan [liabilities]"

    def test_detailed_transactions_custom_columns(self, detailed):
        from gsbparse.domain.detailed_transaction import DetailedTransactionColumn
        from gsbparse.pandas import to_df

        dummy_cols = [
            DetailedTransactionColumn("Nb", "id"),
            DetailedTransactionColumn("Am", "amount"),
        ]
        df = to_df(detailed, columns=dummy_cols)
        assert list(df.columns) == ["id", "amount"]
        assert df["amount"].iloc[0] == Decimal("-200000.00")
