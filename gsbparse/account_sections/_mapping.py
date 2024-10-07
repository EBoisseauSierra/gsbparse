from gsbparse.account_sections._abstract_section import GsbFileSection
from gsbparse.account_sections.account import AccountSection
from gsbparse.account_sections.bank import BankSection
from gsbparse.account_sections.bet import BetSection
from gsbparse.account_sections.bet_graph import BetGraphSection
from gsbparse.account_sections.category import CategorySection
from gsbparse.account_sections.currency import CurrencySection
from gsbparse.account_sections.general import GeneralSection
from gsbparse.account_sections.party import PartySection
from gsbparse.account_sections.payment import PaymentSection
from gsbparse.account_sections.print import PrintSection
from gsbparse.account_sections.reconcile import ReconcileSection
from gsbparse.account_sections.rgba import RGBASection
from gsbparse.account_sections.scheduled import ScheduledSection
from gsbparse.account_sections.subcategory import SubcategorySection
from gsbparse.account_sections.transaction import TransactionSection

ELEMENT_TAG_TO_SECTION: dict[str, GsbFileSection] = {
    "Account": AccountSection,
    "Bank": BankSection,
    "Bet_graph": BetGraphSection,
    "Bet": BetSection,
    "Category": CategorySection,
    "Currency": CurrencySection,
    "General": GeneralSection,
    "Party": PartySection,
    "Payment": PaymentSection,
    "Print": PrintSection,
    "Reconcile": ReconcileSection,
    "RGBA": RGBASection,
    "Scheduled": ScheduledSection,
    "Sub_category": SubcategorySection,
    "Transaction": TransactionSection,
}
