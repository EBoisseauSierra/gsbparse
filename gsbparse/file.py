import logging
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Self

from defusedxml import ElementTree as ET  # noqa: N817

from gsbparse.account_sections._abstract_section import GsbFileSection
from gsbparse.account_sections.account import AccountSection
from gsbparse.account_sections.bank import BankSection
from gsbparse.account_sections.bet import BetSection
from gsbparse.account_sections.bet_graph import BetGraphSection
from gsbparse.account_sections.category import CategorySection
from gsbparse.account_sections.currency import CurrencySection
from gsbparse.account_sections.general import GeneralSection
from gsbparse.account_sections.party import PartySection
from gsbparse.account_sections.payment import PaymentSection
from gsbparse.account_sections.print import PrintSection
from gsbparse.account_sections.reconcile import ReconcileSection
from gsbparse.account_sections.rgba import RGBASection
from gsbparse.account_sections.scheduled import ScheduledSection
from gsbparse.account_sections.subcategory import SubcategorySection
from gsbparse.account_sections.transaction import TransactionSection


@dataclass
class GsbFile:
    General: GeneralSection
    RGBA: RGBASection
    Print: PrintSection
    Currency: list[CurrencySection]
    Account: list[AccountSection]
    Payment: list[PaymentSection]
    Transaction: list[TransactionSection]
    Scheduled: list[ScheduledSection]
    Party: list[PartySection]
    Category: list[CategorySection]
    Sub_category: list[SubcategorySection]
    Bank: list[BankSection]
    Reconcile: list[ReconcileSection]
    Bet: list[BetSection]
    Bet_graph: list[BetGraphSection]

    ELEMENT_TAG_TO_SECTION: dict[str, GsbFileSection] = MappingProxyType(
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
        },
    )

    logger = logging.getLogger(__name__)

    @classmethod
    def from_file(cls, path: str | Path) -> Self:
        sections = cls.get_sections(path)

        general_section = sections.get(GeneralSection)[0]
        rgba_section = sections.get(RGBASection)[0]
        print_section = sections.get(PrintSection)[0]

        return cls(
            General=general_section,
            RGBA=rgba_section,
            Print=print_section,
            Currency=sections.get(CurrencySection),
            Account=sections.get(AccountSection),
            Payment=sections.get(PaymentSection),
            Transaction=sections.get(TransactionSection),
            Scheduled=sections.get(ScheduledSection),
            Party=sections.get(PartySection),
            Category=sections.get(CategorySection),
            Sub_category=sections.get(SubcategorySection),
            Bank=sections.get(BankSection),
            Reconcile=sections.get(ReconcileSection),
            Bet=sections.get(BetSection),
            Bet_graph=sections.get(BetGraphSection),
        )

    @classmethod
    def get_sections(
        cls,
        path: str | Path,
    ) -> dict[GsbFileSection : list[GsbFileSection]]:
        sections: defaultdict[GsbFileSection, list[GsbFileSection]] = defaultdict(list)
        with open(path, encoding="utf-8") as file:
            xml_tree = ET.parse(file)
            root = xml_tree.getroot()

            for child in root:
                section = cls.ELEMENT_TAG_TO_SECTION.get(child.tag)
                if section is None:
                    cls.logger.warning(f"Unknown section: {child.tag}. Ignoring.")
                sections[section].append(section.from_xml(child))

        return dict(sections)
