from dataclasses import dataclass
from decimal import Decimal
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse2.account_sections._abstract_section import GsbFileSection


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
    Column_sort: int
    Sorting_kind_column: list[int] | None
    Bet_use_budget: int

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Name=element.attrib["Name"],
            Id=element.attrib["Id"],
            Number=int(element.attrib["Number"]),
            Owner=element.attrib["Owner"],
            Kind=int(element.attrib["Kind"]),
            Currency=int(element.attrib["Currency"]),
            Path_icon=element.attrib["Path_icon"],
            Bank=int(element.attrib["Bank"]),
            Bank_branch_code=element.attrib["Bank_branch_code"],
            Bank_account_number=element.attrib["Bank_account_number"],
            Key=element.attrib["Key"],
            Bank_account_IBAN=element.attrib["Bank_account_IBAN"],
            Initial_balance=cls.parse_amount(element.attrib["Initial_balance"]),
            Minimum_wanted_balance=cls.parse_amount(
                element.attrib["Minimum_wanted_balance"],
            ),
            Minimum_authorised_balance=cls.parse_amount(
                element.attrib["Minimum_authorised_balance"],
            ),
            Closed_account=cls.parse_bool(element.attrib["Closed_account"]),
            Show_marked=cls.parse_bool(element.attrib["Show_marked"]),
            Show_archives_lines=cls.parse_bool(
                element.attrib["Show_archives_lines"],
            ),
            Lines_per_transaction=int(element.attrib["Lines_per_transaction"]),
            Comment=element.attrib["Comment"],
            Owner_address=element.attrib["Owner_address"],
            Default_debit_method=int(element.attrib["Default_debit_method"]),
            Default_credit_method=int(element.attrib["Default_credit_method"]),
            Sort_by_method=int(element.attrib["Sort_by_method"]),
            Neutrals_inside_method=int(element.attrib["Neutrals_inside_method"]),
            Sort_order=cls.parse_list_int(element.attrib["Sort_order"], "/"),
            Ascending_sort=cls.parse_bool(element.attrib["Ascending_sort"]),
            Column_sort=int(element.attrib["Column_sort"]),
            Sorting_kind_column=cls.parse_list_int(
                element.attrib["Sorting_kind_column"],
            ),
            Bet_use_budget=int(element.attrib["Bet_use_budget"]),
        )
