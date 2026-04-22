"""Domain section: Loan (Bet_loan)."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class BetLoan(GsbFileSection):
    """A loan amortisation schedule defined in the Grisbi file.

    Attributes:
        Nb: Loan number (starts at 0).
        Ac: Account identifier.
        Ver: Version number (incremented on each renegotiation).
        InCol: Invert the capital/payment columns in amortisation tables.
        Ca: Principal (capital).
        Duree: Duration (number of payments).
        FDate: First payment date (nullable).
        Fees: Fees per payment.
        Taux: Annual interest rate.
        TyTaux: Interest rate type.
        NbreDec: Number of decimal places (3-9).
        FEchDif: First payment differs from subsequent payments.
        FCa: Capital portion of the first payment.
        FIn: Interest portion of the first payment.
        OEch: Amount of subsequent payments (when first differs).
        ISchWL: Initialise the associated scheduled transaction from the table.
        AAc: Associated account for the scheduled transaction.
        ASch: Scheduled transaction number for the associated account.
        AFr: Scheduled transaction frequency in months.
        CaDu: Remaining capital.
    """

    Nb: int
    Ac: int
    Ver: int
    InCol: bool
    Ca: Decimal
    Duree: int
    FDate: date | None
    Fees: Decimal
    Taux: Decimal
    TyTaux: int
    NbreDec: int
    FEchDif: bool
    FCa: Decimal
    FIn: Decimal
    OEch: Decimal
    ISchWL: bool
    AAc: int
    ASch: int
    AFr: int
    CaDu: Decimal
