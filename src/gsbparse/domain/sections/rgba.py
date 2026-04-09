"""Domain section: RGBA colour preferences."""

from dataclasses import dataclass

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class RgbaSection(GsbFileSection):
    """Colour preferences stored in the Grisbi file.

    All values are CSS-style RGB strings, e.g. ``"rgb(215,215,255)"``.

    Attributes:
        Background_color_0: Alternating row background colour (even).
        Background_color_1: Alternating row background colour (odd).
        Couleur_jour: Current-day highlight colour.
        Background_scheduled: Scheduled-transaction row background.
        Background_archive: Archived-transaction row background.
        Selection: Selected-row colour.
        Background_split: Split-transaction child row background.
        Text_color_0: Primary text colour.
        Text_color_1: Secondary text colour (e.g. negative amounts).
        Couleur_bet_division: Budget-estimate division colour.
        Couleur_bet_future: Budget-estimate future-data colour.
        Couleur_bet_solde: Budget-estimate balance colour.
        Couleur_bet_transfert: Budget-estimate transfer colour.
    """

    Background_color_0: str
    Background_color_1: str
    Couleur_jour: str
    Background_scheduled: str
    Background_archive: str
    Selection: str
    Background_split: str
    Text_color_0: str
    Text_color_1: str
    Couleur_bet_division: str
    Couleur_bet_future: str
    Couleur_bet_solde: str
    Couleur_bet_transfert: str
