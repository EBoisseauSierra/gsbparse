import logging
from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from types import MappingProxyType
from typing import Self

import pandas as pd

from gsbparse2.account_sections._abstract_section import GsbFileSection
from gsbparse2.account_sections.account import AccountSection
from gsbparse2.account_sections.amount_comparison import AmountComparisonSection
from gsbparse2.account_sections.archive import ArchiveSection
from gsbparse2.account_sections.bank import BankSection
from gsbparse2.account_sections.bet import BetSection
from gsbparse2.account_sections.bet_future import BetFutureSection
from gsbparse2.account_sections.bet_graph import BetGraphSection
from gsbparse2.account_sections.bet_historical import BetHistoricalSection
from gsbparse2.account_sections.budgetary import BudgetarySection
from gsbparse2.account_sections.category import CategorySection
from gsbparse2.account_sections.currency import CurrencySection
from gsbparse2.account_sections.currency_link import CurrencyLinkSection
from gsbparse2.account_sections.financial_year import FinancialYearSection
from gsbparse2.account_sections.general import GeneralSection
from gsbparse2.account_sections.partial_balance import PartialBalanceSection
from gsbparse2.account_sections.party import PartySection
from gsbparse2.account_sections.payment import PaymentSection
from gsbparse2.account_sections.print import PrintSection
from gsbparse2.account_sections.reconcile import ReconcileSection
from gsbparse2.account_sections.report import ReportSection
from gsbparse2.account_sections.rgba import RGBASection
from gsbparse2.account_sections.scheduled import ScheduledSection
from gsbparse2.account_sections.subbudgetary import SubbudgetarySection
from gsbparse2.account_sections.subcategory import SubcategorySection
from gsbparse2.account_sections.text_comparison import TextComparisonSection
from gsbparse2.account_sections.transaction import TransactionSection
from gsbparse2.exceptions import (
    InvalidElementCountError,
    SectionNotFoundError,
)
from gsbparse2.xml import read_file

GsbSectionsToInstancesMapping = dict[type[GsbFileSection], list[GsbFileSection]]


@dataclass
class GsbFile:
    General: GeneralSection | None = None
    RGBA: RGBASection | None = None
    Print: PrintSection | None = None
    Currency: list[CurrencySection] | None = None
    Currency_link: list[CurrencyLinkSection] | None = None
    Financial_year: list[FinancialYearSection] | None = None
    Account: list[AccountSection] | None = None
    Payment: list[PaymentSection] | None = None
    Transaction: list[TransactionSection] | None = None
    Scheduled: list[ScheduledSection] | None = None
    Party: list[PartySection] | None = None
    Category: list[CategorySection] | None = None
    Sub_category: list[SubcategorySection] | None = None
    Bank: list[BankSection] | None = None
    Reconcile: list[ReconcileSection] | None = None
    Bet: list[BetSection] | None = None
    Bet_graph: list[BetGraphSection] | None = None
    Bet_historical: list[BetHistoricalSection] | None = None
    Bet_future: list[BetFutureSection] | None = None
    Budgetary: list[BudgetarySection] | None = None
    Sub_budgetary: list[SubbudgetarySection] | None = None
    Partial_balance: list[PartialBalanceSection] | None = None
    Report: list[ReportSection] | None = None
    Text_comparison: list[TextComparisonSection] | None = None
    Amount_comparison: list[AmountComparisonSection] | None = None
    Archive: list[ArchiveSection] | None = None

    _ELEMENT_TAG_TO_SECTION: Mapping[str, type[GsbFileSection]] = MappingProxyType(
        {
            "Account": AccountSection,
            "Bank": BankSection,
            "Bet_graph": BetGraphSection,
            "Bet": BetSection,
            "Budgetary": BudgetarySection,
            "Category": CategorySection,
            "Currency": CurrencySection,
            "Currency_link": CurrencyLinkSection,
            "Financial_year": FinancialYearSection,
            "General": GeneralSection,
            "Party": PartySection,
            "Payment": PaymentSection,
            "Print": PrintSection,
            "Reconcile": ReconcileSection,
            "RGBA": RGBASection,
            "Scheduled": ScheduledSection,
            "Sub_budgetary": SubbudgetarySection,
            "Sub_category": SubcategorySection,
            "Transaction": TransactionSection,
            "Partial_balance": PartialBalanceSection,
            "Bet_historical": BetHistoricalSection,
            "Bet_future": BetFutureSection,
            "Report": ReportSection,
            "Text_comparison": TextComparisonSection,
            "Amount_comparison": AmountComparisonSection,
            "Archive": ArchiveSection,
        }
    )

    logger = logging.getLogger(__name__)

    @classmethod
    def from_file(cls, path: str | Path) -> Self:
        sections = cls.parse_file(path)

        return cls(
            # Ignoring type to simplify type hints
            General=cls.get_elements(sections, GeneralSection, single_element=True),  # type: ignore[arg-type]
            RGBA=cls.get_elements(sections, RGBASection, single_element=True),  # type: ignore[arg-type]
            Print=cls.get_elements(sections, PrintSection, single_element=True),  # type: ignore[arg-type]
            Currency=cls.get_elements(sections, CurrencySection),  # type: ignore[arg-type]
            Currency_link=cls.get_elements(sections, CurrencyLinkSection),  # type: ignore[arg-type]
            Financial_year=cls.get_elements(sections, FinancialYearSection),  # type: ignore[arg-type]
            Account=cls.get_elements(sections, AccountSection),  # type: ignore[arg-type]
            Payment=cls.get_elements(sections, PaymentSection),  # type: ignore[arg-type]
            Transaction=cls.get_elements(sections, TransactionSection),  # type: ignore[arg-type]
            Scheduled=cls.get_elements(sections, ScheduledSection),  # type: ignore[arg-type]
            Party=cls.get_elements(sections, PartySection),  # type: ignore[arg-type]
            Category=cls.get_elements(sections, CategorySection),  # type: ignore[arg-type]
            Sub_category=cls.get_elements(sections, SubcategorySection),  # type: ignore[arg-type]
            Bank=cls.get_elements(sections, BankSection),  # type: ignore[arg-type]
            Reconcile=cls.get_elements(sections, ReconcileSection),  # type: ignore[arg-type]
            Bet=cls.get_elements(sections, BetSection),  # type: ignore[arg-type]
            Bet_graph=cls.get_elements(sections, BetGraphSection),  # type: ignore[arg-type]
            Partial_balance=cls.get_elements(sections, PartialBalanceSection),  # type: ignore[arg-type]
            Bet_historical=cls.get_elements(sections, BetHistoricalSection),  # type: ignore[arg-type]
            Bet_future=cls.get_elements(sections, BetFutureSection),  # type: ignore[arg-type]
            Report=cls.get_elements(sections, ReportSection),  # type: ignore[arg-type]
            Budgetary=cls.get_elements(sections, BudgetarySection),  # type: ignore[arg-type]
            Sub_budgetary=cls.get_elements(sections, SubbudgetarySection),  # type: ignore[arg-type]
            Text_comparison=cls.get_elements(sections, TextComparisonSection),  # type: ignore[arg-type]
            Amount_comparison=cls.get_elements(sections, AmountComparisonSection),  # type: ignore[arg-type]
            Archive=cls.get_elements(sections, ArchiveSection),  # type: ignore[arg-type]
        )

    @classmethod
    def parse_file(cls, path: str | Path) -> GsbSectionsToInstancesMapping:
        "Parse children elements of Grisbi and return all sections, grouped by type."
        sections: defaultdict[type[GsbFileSection], list[GsbFileSection]] = defaultdict(
            list[GsbFileSection]
        )

        gsb_file = read_file(path)

        for element in gsb_file:
            try:
                section = cls._ELEMENT_TAG_TO_SECTION[element.tag]
            except KeyError:
                cls.logger.warning(f"Unknown section: {element.tag}. Ignoring.")
                continue
            sections[section].append(section.from_xml(element))
        return dict(sections)

    @staticmethod
    def get_elements(
        sections: GsbSectionsToInstancesMapping,
        section: type[GsbFileSection],
        optional: bool = True,
        single_element: bool = False,
    ) -> list[GsbFileSection] | GsbFileSection | None:
        elements = sections.get(section)
        if elements is None or len(elements) == 0:
            if optional:
                return None
            raise SectionNotFoundError(section)

        if single_element:
            if len(elements) > 1:
                raise InvalidElementCountError(1, len(elements), section)
            return elements[0]

        return elements

    @cached_property
    def transactions(self) -> list[dict]:
        self._generate_sections_dicts()
        return [
            self._populate_transaction_details(transaction)
            for transaction in self.Transaction
        ]

    def _generate_sections_dicts(self) -> None:
        self._accounts = self._generate_section_dict(self.Account, "Number")
        self._budgetary = self._generate_section_dict(self.Budgetary, "Nb")
        self._categories = self._generate_section_dict(self.Category, "Nb")
        self._currency = self._generate_section_dict(self.Currency, "Nb")
        self._party = self._generate_section_dict(self.Party, "Nb")
        self._payment = self._generate_section_dict(self.Payment, "Number")
        self._reconcile = self._generate_section_dict(self.Reconcile, "Nb")
        self._subbudgetary = self._generate_section_dict_multiple_keys(
            self.Sub_budgetary, ("Nbb", "Nb")
        )
        self._subcategory = self._generate_section_dict_multiple_keys(
            self.Sub_category, ("Nbc", "Nb")
        )
        self._financial_year = self._generate_section_dict(self.Financial_year, "Nb")

    @staticmethod
    def _generate_section_dict(
        section: type[GsbFileSection], key: str
    ) -> dict[int, list[GsbFileSection]]:
        if section is None:
            return {}
        return {getattr(element, key): element for element in section}

    @staticmethod
    def _generate_section_dict_multiple_keys(
        section: type[GsbFileSection], keys: tuple[str, str]
    ) -> dict[tuple[int, int], list[GsbFileSection]]:
        main_key, sub_key = keys

        if section is None:
            return {}

        return {
            (getattr(element, main_key), getattr(element, sub_key)): element
            for element in section
        }

    def _populate_transaction_details(self, transaction: TransactionSection) -> dict:
        # TODO: Use namedtuples instead of dicts for better performance
        return {
            "id": transaction.Nb,
            "ofx_import_id": transaction.Id,
            "account_name": self._get_attribute(self._accounts, transaction.Ac, "Name"),
            "account_owner": self._get_attribute(
                self._accounts, transaction.Ac, "Owner"
            ),
            "account_is_closed": self._get_attribute(
                self._accounts, transaction.Ac, "Closed_account"
            ),
            "date_transaction": transaction.Dt,
            "date_value": transaction.Dv,
            "currency_name": self._get_attribute(self._currency, transaction.Cu, "Na"),
            "currency_symbol": self._get_attribute(
                self._currency, transaction.Cu, "Co"
            ),
            "currency_iso_code": self._get_attribute(
                self._currency, transaction.Cu, "Ico"
            ),
            "amount": transaction.Am,
            "exchange_rate": transaction.Exr,
            "exchange_fee": transaction.Exf,
            "party": self._get_attribute(self._party, transaction.Pa, "Na"),
            "category": self._get_attribute(self._categories, transaction.Ca, "Na"),
            "subcategory": self._get_attribute(
                self._subcategory, (transaction.Ca, transaction.Sca), "Na"
            ),
            "is_breakdown_transaction": transaction.Br,
            "mother_transaction_id": transaction.Mo,
            "note": transaction.No,
            "payment_method": self._get_attribute(
                self._payment, transaction.Pn, "Name"
            ),
            "payment_method_content": transaction.Pc,
            "reconcile_status": transaction.Ma.name,
            "reconcile": self._get_attribute(self._reconcile, transaction.Re, "Na"),
            "archive": transaction.Ar,
            "is_automatic": transaction.Au,
            "financial_year": self._get_attribute(
                self._financial_year, transaction.Fi, "Na"
            ),
            "budgetary_line": self._get_attribute(
                self._budgetary, transaction.Bu, "Na"
            ),
            "subbudgetary_line": self._get_attribute(
                self._subbudgetary, (transaction.Bu, transaction.Sbu), "Na"
            ),
        }

    @staticmethod
    def _get_attribute(
        elements: dict[int, GsbFileSection], key: int | tuple[int, int], attribute: str
    ):
        try:
            element = elements[key]
        except KeyError:
            return None

        return getattr(element, attribute)

    def to_csv(self, path: str | Path) -> None:
        import csv

        with open(path, "w") as csv_file:
            writer = csv.DictWriter(
                csv_file,
                fieldnames=[
                    "id",
                    "ofx_import_id",
                    "account_name",
                    "account_owner",
                    "account_is_closed",
                    "date_transaction",
                    "date_value",
                    "currency_name",
                    "currency_symbol",
                    "currency_iso_code",
                    "amount",
                    "exchange_rate",
                    "exchange_fee",
                    "party",
                    "category",
                    "subcategory",
                    "is_breakdown_transaction",
                    "mother_transaction_id",
                    "note",
                    "payment_method",
                    "payment_method_content",
                    "reconcile_status",
                    "reconcile",
                    "archive",
                    "is_automatic",
                    "fiscal_year",
                    "budgetary_line",
                    "subbudgetary_line",
                ],
            )
            writer.writeheader()
            writer.writerows(self.transactions)

    def to_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.transactions)
