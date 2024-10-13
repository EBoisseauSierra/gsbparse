import logging
from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Self

from gsbparse2.account_sections._abstract_section import GsbFileSection
from gsbparse2.account_sections.account import AccountSection
from gsbparse2.account_sections.bank import BankSection
from gsbparse2.account_sections.bet import BetSection
from gsbparse2.account_sections.bet_graph import BetGraphSection
from gsbparse2.account_sections.category import CategorySection
from gsbparse2.account_sections.currency import CurrencySection
from gsbparse2.account_sections.general import GeneralSection
from gsbparse2.account_sections.party import PartySection
from gsbparse2.account_sections.payment import PaymentSection
from gsbparse2.account_sections.print import PrintSection
from gsbparse2.account_sections.reconcile import ReconcileSection
from gsbparse2.account_sections.rgba import RGBASection
from gsbparse2.account_sections.scheduled import ScheduledSection
from gsbparse2.account_sections.subcategory import SubcategorySection
from gsbparse2.account_sections.transaction import TransactionSection
from gsbparse2.exceptions import (
    InvalidElementCountError,
    SectionNotFoundError,
)
from gsbparse2.xml import read_file

GsbSectionsToInstancesMapping = dict[type[GsbFileSection], list[GsbFileSection]]


@dataclass
class GsbFile:
    General: GeneralSection | None
    RGBA: RGBASection | None
    Print: PrintSection | None
    Currency: list[CurrencySection] | None
    Account: list[AccountSection] | None
    Payment: list[PaymentSection] | None
    Transaction: list[TransactionSection] | None
    Scheduled: list[ScheduledSection] | None
    Party: list[PartySection] | None
    Category: list[CategorySection] | None
    Sub_category: list[SubcategorySection] | None
    Bank: list[BankSection] | None
    Reconcile: list[ReconcileSection] | None
    Bet: list[BetSection] | None
    Bet_graph: list[BetGraphSection] | None

    _ELEMENT_TAG_TO_SECTION: Mapping[str, type[GsbFileSection]] = MappingProxyType(
        {
            "Account": AccountSection,
            "Bank": BankSection,
            "Bet_graph": BetGraphSection,
            "Bet": BetSection,
            "Category": CategorySection,
            "Currency": CurrencySection,
            "General": GeneralSection,
            "Party": PartySection,
            "Payment": PaymentSection,
            "Print": PrintSection,
            "Reconcile": ReconcileSection,
            "RGBA": RGBASection,
            "Scheduled": ScheduledSection,
            "Sub_category": SubcategorySection,
            "Transaction": TransactionSection,
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
