"""Domain section: Budget estimate deferred-debit transfer (Bet_transfert)."""

from dataclasses import dataclass
from datetime import date

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class BetTransfertSection(GsbFileSection):
    """A deferred-debit or partial-balance settlement entry.

    Used when a credit-card account (deferred debit) or a partial balance
    is settled against a main bank account.

    Attributes:
        Nb: Unique identifier.
        Dt: Settlement date on the main bank account (nullable).
        Ac: Account identifier (the deferred-debit or partial-balance account).
        Ty: Type (0 = cash account, 1 = partial balance of cash accounts).
        Ra: Account or partial-balance number concerned.
        Rt: Replace a transaction whose date falls in the import search window.
        Dd: Create the debit transaction in the target account.
        Dtb: Month switchover date (day after the statement cutoff) (nullable).
        Mlbd: Force settlement date to the last banking day of the month.
        Pa: Party identifier.
        Pn: Payment method identifier.
        Ca: Category identifier.
        Sca: Sub-category identifier.
        Bu: Budget line identifier.
        Sbu: Sub-budget line identifier.
        CPa: Counter-party identifier.
        CCa: Counter-category identifier.
        CSca: Counter-sub-category identifier.
        CBu: Counter-budget identifier.
        CSbu: Counter-sub-budget identifier.
    """

    Nb: int
    Dt: date | None
    Ac: int
    Ty: int
    Ra: int
    Rt: bool
    Dd: bool
    Dtb: date | None
    Mlbd: bool
    Pa: int
    Pn: int
    Ca: int
    Sca: int
    Bu: int
    Sbu: int
    CPa: int
    CCa: int
    CSca: int
    CBu: int
    CSbu: int
