"""XML adapter: parse an ``<Account>`` element into an ``AccountSection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import (
    parse_amount,
    parse_bool,
    parse_int,
    parse_null,
    parse_str,
)
from gsbparse.domain.sections.account import AccountKind, AccountSection

_parse_nullable_str = parse_null(parse_str)


def parse_account_section(element: ET.Element) -> AccountSection:
    """Parse an ``<Account>`` XML element into an :class:`AccountSection`.

    Args:
        element: The ``<Account>`` XML element.

    Returns:
        A fully populated :class:`AccountSection`.
    """
    a = element.attrib
    return AccountSection(
        Name=parse_str(a["Name"]),
        Id=_parse_nullable_str(a["Id"]),
        Number=parse_int(a["Number"]),
        Owner=parse_str(a["Owner"]),
        Kind=AccountKind(parse_int(a["Kind"])),
        Currency=parse_int(a["Currency"]),
        Path_icon=parse_str(a["Path_icon"]),
        Bank=parse_int(a["Bank"]),
        Bank_branch_code=parse_str(a["Bank_branch_code"]),
        Bank_account_number=parse_str(a["Bank_account_number"]),
        Key=parse_str(a["Key"]),
        Bank_account_IBAN=parse_str(a["Bank_account_IBAN"]),
        Initial_balance=parse_amount(a["Initial_balance"]),
        Minimum_wanted_balance=parse_amount(a["Minimum_wanted_balance"]),
        Minimum_authorised_balance=parse_amount(a["Minimum_authorised_balance"]),
        Closed_account=parse_bool(a["Closed_account"]),
        Show_marked=parse_bool(a["Show_marked"]),
        Show_archives_lines=parse_bool(a["Show_archives_lines"]),
        Lines_per_transaction=parse_int(a["Lines_per_transaction"]),
        Comment=parse_str(a["Comment"]),
        Owner_address=parse_str(a["Owner_address"]),
        Default_debit_method=parse_int(a["Default_debit_method"]),
        Default_credit_method=parse_int(a["Default_credit_method"]),
        Sort_by_method=parse_bool(a["Sort_by_method"]),
        Neutrals_inside_method=parse_bool(a["Neutrals_inside_method"]),
        Sort_order=parse_str(a["Sort_order"]),
        Ascending_sort=parse_bool(a["Ascending_sort"]),
        Column_sort=parse_int(a["Column_sort"]),
        Sorting_kind_column=parse_str(a["Sorting_kind_column"]),
        Bet_use_budget=parse_int(a["Bet_use_budget"]),
    )
