"""Domain section: Scheduled transaction."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class Scheduled(GsbFileSection):
    """A scheduled (recurring) transaction defined in the Grisbi file.

    Attributes:
        Nb: Scheduled transaction number.
        Dt: Next occurrence date (nullable).
        Ac: Account identifier.
        Am: Amount.
        Cu: Currency identifier.
        Pa: Party identifier.
        Ca: Category identifier.
        Sca: Sub-category identifier.
        Tra: Transfer target account identifier.
        Pn: Payment method identifier.
        CPn: Counter-payment method identifier.
        Pc: Payment method content (nullable).
        Fi: Financial year identifier (-2 = current year).
        Bu: Budget line identifier.
        Sbu: Sub-budget line identifier.
        No: Notes (nullable).
        Au: Automatic execution flag.
        Fd: Fixed day of month (0 = none, 28-31 = fixed day; 31 = last day).
        Pe: Periodicity.
        Pei: Periodicity interval.
        Pep: Custom periodicity value.
        Dtl: Limit date (nullable).
        Br: Breakdown flag.
        Mo: Mother transaction number for breakdown children.
    """

    Nb: int
    Dt: date | None
    Ac: int
    Am: Decimal
    Cu: int
    Pa: int
    Ca: int
    Sca: int
    Tra: int
    Pn: int
    CPn: int
    Pc: str | None
    Fi: int
    Bu: int
    Sbu: int
    No: str | None
    Au: bool
    Fd: int
    Pe: int
    Pei: int
    Pep: int
    Dtl: date | None
    Br: bool
    Mo: int
