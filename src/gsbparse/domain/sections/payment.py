"""Domain section: Payment method (mode de règlement)."""

from dataclasses import dataclass

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class Payment(GsbFileSection):
    """A payment method defined in the Grisbi file.

    Attributes:
        Number: Unique identifier.
        Name: Display name.
        Sign: Sign convention (1 = debit, -1 = credit, 0 = neutral).
        Show_entry: Show a free-text entry field in the transaction form.
        Automatic_number: Auto-increment the payment reference number.
        Current_number: Current auto-increment value (``None`` when ``Automatic_number`` is off).
        Account: Account identifier this method is attached to (0 = global).
    """

    Number: int
    Name: str
    Sign: int
    Show_entry: bool
    Automatic_number: bool
    Current_number: int | None
    Account: int
