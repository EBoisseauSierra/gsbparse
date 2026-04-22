"""Domain section: Budget estimate graph preferences (Bet_graph)."""

from dataclasses import dataclass

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class BetGraph(GsbFileSection):
    """Graph display preferences for the budget-estimate module.

    Multiple ``<Bet_graph>`` elements may appear in a file — one for the
    forecast graph and one for the historical graph.  The ``prefs`` string
    is a colon-delimited list of settings (e.g.
    ``"forecast_prefs:0:1:0:1:2:0:0:90:50:1:0:0"``).

    Attributes:
        prefs: Raw colon-delimited preferences string.
    """

    prefs: str
