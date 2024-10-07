from dataclasses import dataclass
from decimal import Decimal
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class AccountSection(GsbFileSection):
    Name: str
    Id: str
    Number: int
    Owner: str
    Kind: int
    Currency: int
    Path_icon: str
    Bank: int
    Bank_branch_code: str
    Bank_account_number: str
    Key: str
    Bank_account_IBAN: str
    Initial_balance: Decimal
    Minimum_wanted_balance: Decimal
    Minimum_authorised_balance: Decimal
    Closed_account: bool
    Show_marked: bool
    Show_archives_lines: bool
    Lines_per_transaction: int
    Comment: str
    Owner_address: str
    Default_debit_method: int
    Default_credit_method: int
    Sort_by_method: int
    Neutrals_inside_method: int
    Sort_order: list[int] | None
    Ascending_sort: bool
    Column_sort: bool
    Sorting_kind_column: list[int] | None
    Bet_use_budget: bool

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Name=element.attrib.get("Name"),
            Id=element.attrib.get("Id"),
            Number=int(element.attrib.get("Number")),
            Owner=element.attrib.get("Owner"),
            Kind=int(element.attrib.get("Kind")),
            Currency=int(element.attrib.get("Currency")),
            Path_icon=element.attrib.get("Path_icon"),
            Bank=int(element.attrib.get("Bank")),
            Bank_branch_code=element.attrib.get("Bank_branch_code"),
            Bank_account_number=element.attrib.get("Bank_account_number"),
            Key=element.attrib.get("Key"),
            Bank_account_IBAN=element.attrib.get("Bank_account_IBAN"),
            Initial_balance=cls.parse_amount(element.attrib.get("Initial_balance")),
            Minimum_wanted_balance=cls.parse_amount(
                element.attrib.get("Minimum_wanted_balance"),
            ),
            Minimum_authorised_balance=cls.parse_amount(
                element.attrib.get("Minimum_authorised_balance"),
            ),
            Closed_account=cls.parse_bool(element.attrib.get("Closed_account")),
            Show_marked=cls.parse_bool(element.attrib.get("Show_marked")),
            Show_archives_lines=cls.parse_bool(
                element.attrib.get("Show_archives_lines"),
            ),
            Lines_per_transaction=int(element.attrib.get("Lines_per_transaction")),
            Comment=element.attrib.get("Comment"),
            Owner_address=element.attrib.get("Owner_address"),
            Default_debit_method=int(element.attrib.get("Default_debit_method")),
            Default_credit_method=int(element.attrib.get("Default_credit_method")),
            Sort_by_method=int(element.attrib.get("Sort_by_method")),
            Neutrals_inside_method=int(element.attrib.get("Neutrals_inside_method")),
            Sort_order=cls.parse_list_int(element.attrib.get("Sort_order"), "/"),
            Ascending_sort=cls.parse_bool(element.attrib.get("Ascending_sort")),
            Column_sort=cls.parse_bool(element.attrib.get("Column_sort")),
            Sorting_kind_column=cls.parse_list_int(
                element.attrib.get("Sorting_kind_column"),
            ),
            Bet_use_budget=cls.parse_bool(element.attrib.get("Bet_use_budget")),
        )
