"""Domain section: Bank."""

from dataclasses import dataclass

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class BankSection(GsbFileSection):
    """A bank defined in the Grisbi file.

    Attributes:
        Nb: Unique identifier.
        Na: Bank name.
        Co: Bank code.
        BIC: BIC/SWIFT code.
        Adr: Address.
        Tel: Phone number.
        Mail: E-mail address (nullable).
        Web: Website URL (nullable).
        Nac: Contact name.
        Faxc: Contact fax.
        Telc: Contact phone.
        Mailc: Contact e-mail.
        Rem: Remarks (nullable).
    """

    Nb: int
    Na: str
    Co: str
    BIC: str
    Adr: str
    Tel: str
    Mail: str | None
    Web: str | None
    Nac: str
    Faxc: str
    Telc: str
    Mailc: str
    Rem: str | None
