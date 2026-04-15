# Detailed Section FK Resolution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve all FK integer fields inside `DetailedTransaction`'s nested section objects (`Ac`, `Sca`, `Sbu`, `Re`) so that navigating `tx.Ac.Currency.Ico`, `tx.Sca.Nbc.Na`, `tx.Re.Acc.Name`, etc. works without any raw integers remaining in the FK-resolved view.

**Architecture:** Four new frozen dataclasses (`DetailedAccountSection`, `DetailedSubCategorySection`, `DetailedSubBudgetarySection`, `DetailedReconcileSection`) replace the raw section types on the corresponding `DetailedTransaction` fields. `build_detailed_transactions` gains pre-pass lookup dicts to resolve each FK before Pass 1. The sub-category and sub-budgetary lookups use composite keys `(parent_nb, child_nb)` to correctly disambiguate children that share the same `Nb` across different parents. Raw section types on `GsbFile` are unchanged.

**Tech Stack:** Python 3.13+, `dataclasses`, stdlib only in `domain/`. Tests: `pytest`, `caplog`.

---

## File map

| File | Change |
|---|---|
| `src/gsbparse/domain/sections/sub_category.py` | Add `DetailedSubCategorySection` |
| `src/gsbparse/domain/sections/sub_budgetary.py` | Add `DetailedSubBudgetarySection` |
| `src/gsbparse/domain/sections/reconcile.py` | Add `DetailedReconcileSection` |
| `src/gsbparse/domain/sections/account.py` | Add `DetailedAccountSection` |
| `src/gsbparse/domain/detailed_transaction.py` | Update field types on `DetailedTransaction`; update `build_detailed_transactions`; update imports |
| `src/gsbparse/domain/sections/__init__.py` | Re-export four new types |
| `src/gsbparse/__init__.py` | Re-export four new types |
| `tests/test_detailed_transactions.py` | Update `_minimal_gsb_file` helper; fix `test_resolves_account_and_currency`; add new unit tests |
| `tests/test_e2e.py` | Add E2E assertions for new nested paths |

---

## Task 1: `DetailedSubCategorySection`

**Files:**
- Modify: `src/gsbparse/domain/sections/sub_category.py`
- Modify: `src/gsbparse/domain/detailed_transaction.py`
- Modify: `tests/test_detailed_transactions.py`

- [ ] **Step 1: Update `_minimal_gsb_file` helper to accept all FK-related params**

In `tests/test_detailed_transactions.py`, replace the existing `_minimal_gsb_file` signature and body:

```python
from gsbparse.domain.sections.bank import BankSection
from gsbparse.domain.sections.budgetary import BudgetarySection
from gsbparse.domain.sections.payment import PaymentSection
from gsbparse.domain.sections.reconcile import ReconcileSection
from gsbparse.domain.sections.sub_budgetary import SubBudgetarySection


def _minimal_gsb_file(
    transactions: list[TransactionSection] | None = None,
    accounts: list[AccountSection] | None = None,
    currencies: list[CurrencySection] | None = None,
    parties: list[PartySection] | None = None,
    categories: list[CategorySection] | None = None,
    sub_categories: list[SubCategorySection] | None = None,
    budgetaries: list[BudgetarySection] | None = None,
    sub_budgetaries: list[SubBudgetarySection] | None = None,
    banks: list[BankSection] | None = None,
    payment_methods: list[PaymentSection] | None = None,
    reconciles: list[ReconcileSection] | None = None,
) -> GsbFile:
    return GsbFile(
        general=None,
        rgba=None,
        print_settings=None,
        currencies=currencies,
        accounts=accounts,
        banks=banks,
        parties=parties,
        payment_methods=payment_methods,
        transactions=transactions,
        scheduled=None,
        categories=categories,
        sub_categories=sub_categories,
        budgetaries=budgetaries,
        sub_budgetaries=sub_budgetaries,
        currency_links=None,
        financial_years=None,
        archives=None,
        reconciles=reconciles,
        import_rules=None,
        special_lines=None,
        partial_balances=None,
        bet=None,
        bet_graphs=None,
        bet_historicals=None,
        bet_futures=None,
        bet_transferts=None,
        bet_loans=None,
        reports=None,
        text_comparisons=None,
        amount_comparisons=None,
    )
```

- [ ] **Step 2: Write the failing test for sub-category FK resolution**

Add this test class to `tests/test_detailed_transactions.py`:

```python
class TestDetailedSubCategorySection:
    def test_sub_category_nbc_resolves_to_category(self):
        # Arrange
        dummy_category = _dummy_category(nb=3, na="Transport")
        dummy_sub_category = _dummy_sub_category(nb=2, na="Bus", nbc=3)
        dummy_account = _dummy_account()
        dummy_currency = _dummy_currency()
        dummy_tx = _dummy_transaction(ca=3, sca=2)
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[dummy_account],
            currencies=[dummy_currency],
            categories=[dummy_category],
            sub_categories=[dummy_sub_category],
        )

        # Act
        result = build_detailed_transactions(gsb)

        # Assert
        assert result is not None
        assert result[0].Sca is not None
        assert result[0].Sca.Na == "Bus"
        assert result[0].Sca.Nbc is dummy_category

    def test_sub_categories_sharing_nb_are_disambiguated_by_parent(self):
        # Two sub-categories have the same Nb=1 but different parent categories.
        dummy_cat_a = _dummy_category(nb=1, na="Food")
        dummy_cat_b = _dummy_category(nb=2, na="Transport")
        dummy_sca_a = SubCategorySection(Nb=1, Na="Groceries", Nbc=1)
        dummy_sca_b = SubCategorySection(Nb=1, Na="Bus", Nbc=2)
        dummy_account = _dummy_account()
        dummy_currency = _dummy_currency()
        dummy_tx = _dummy_transaction(ca=2, sca=1)  # wants Transport/Bus
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[dummy_account],
            currencies=[dummy_currency],
            categories=[dummy_cat_a, dummy_cat_b],
            sub_categories=[dummy_sca_a, dummy_sca_b],
        )

        result = build_detailed_transactions(gsb)

        assert result is not None
        assert result[0].Sca is not None
        assert result[0].Sca.Na == "Bus"
        assert result[0].Sca.Nbc is dummy_cat_b
```

- [ ] **Step 3: Run the failing test**

```
uv run pytest tests/test_detailed_transactions.py::TestDetailedSubCategorySection -v
```

Expected: FAIL — `AttributeError` or type mismatch (`Sca.Nbc` is `int`, not `CategorySection`).

- [ ] **Step 4: Add `DetailedSubCategorySection` to `sub_category.py`**

Add after the existing `SubCategorySection` class in `src/gsbparse/domain/sections/sub_category.py`:

```python
from gsbparse.domain.sections.category import CategorySection


@dataclass(frozen=True)
class DetailedSubCategorySection(GsbFileSection):
    """A transaction sub-category with its parent category resolved.

    Attributes:
        Nbc: Parent category (resolved from the raw ``Nbc`` identifier).
        Nb: Unique identifier within the parent category.
        Na: Display name.
    """

    Nbc: CategorySection
    Nb: int
    Na: str
```

- [ ] **Step 5: Update imports in `detailed_transaction.py`**

Replace:
```python
from gsbparse.domain.sections.sub_category import SubCategorySection
```
With:
```python
from gsbparse.domain.sections.sub_category import DetailedSubCategorySection
```

- [ ] **Step 6: Update `DetailedTransaction.Sca` field type in `detailed_transaction.py`**

Replace:
```python
    Sca: SubCategorySection | None
```
With:
```python
    Sca: DetailedSubCategorySection | None
```

- [ ] **Step 7: Update `build_detailed_transactions` in `detailed_transaction.py`**

Replace the existing `sub_categories` dict and its usage. Find and replace:

```python
    sub_categories: dict[int, SubCategorySection] = (
        {s.Nb: s for s in gsb_file.sub_categories} if gsb_file.sub_categories else {}
    )
```

With:

```python
    # Keyed by (parent_category_nb, sub_category_nb) to disambiguate shared Nb values.
    detailed_sub_categories: dict[tuple[int, int], DetailedSubCategorySection] = {}
    if gsb_file.sub_categories:
        for sc in gsb_file.sub_categories:
            parent = categories.get(sc.Nbc)
            if parent is None:
                _log.warning(
                    "SubCategory %d (parent=%d): parent category not found — skipping",
                    sc.Nb,
                    sc.Nbc,
                )
                continue
            detailed_sub_categories[(sc.Nbc, sc.Nb)] = DetailedSubCategorySection(
                Nbc=parent, Nb=sc.Nb, Na=sc.Na
            )
```

Then in Pass 1, replace:
```python
            Sca=sub_categories.get(tx.Sca) if tx.Sca != 0 else None,
```
With:
```python
            Sca=detailed_sub_categories.get((tx.Ca, tx.Sca)) if tx.Sca != 0 else None,
```

- [ ] **Step 8: Run all tests**

```
uv run pytest tests/test_detailed_transactions.py -v
```

Expected: all pass including the new `TestDetailedSubCategorySection` tests.

- [ ] **Step 9: Run full CI**

```
make ci
```

Expected: all pass.

- [ ] **Step 10: Commit**

```bash
git add src/gsbparse/domain/sections/sub_category.py \
        src/gsbparse/domain/detailed_transaction.py \
        tests/test_detailed_transactions.py
git commit -m "$(cat <<'EOF'
feat(domain/sections): Add DetailedSubCategorySection with resolved parent CategorySection

Resolves SubCategorySection.Nbc from int to CategorySection in the
DetailedTransaction view. Uses composite (parent_nb, child_nb) key to
correctly disambiguate sub-categories sharing the same Nb across parents.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: `DetailedSubBudgetarySection`

**Files:**
- Modify: `src/gsbparse/domain/sections/sub_budgetary.py`
- Modify: `src/gsbparse/domain/detailed_transaction.py`
- Modify: `tests/test_detailed_transactions.py`

- [ ] **Step 1: Add a `_dummy_budgetary` helper to `tests/test_detailed_transactions.py`**

Add after the existing `_dummy_sub_category` helper:

```python
from gsbparse.domain.sections.budgetary import BudgetarySection
from gsbparse.domain.sections.sub_budgetary import SubBudgetarySection


def _dummy_budgetary(nb: int = 1, na: str = "Household") -> BudgetarySection:
    return BudgetarySection(Nb=nb, Na=na, Kd=CategoryKind.EXPENSE)


def _dummy_sub_budgetary(nb: int = 1, na: str = "Groceries", nbb: int = 1) -> SubBudgetarySection:
    return SubBudgetarySection(Nb=nb, Na=na, Nbb=nbb)
```

- [ ] **Step 2: Write the failing test**

Add to `tests/test_detailed_transactions.py`:

```python
class TestDetailedSubBudgetarySection:
    def test_sub_budgetary_nbb_resolves_to_budgetary(self):
        # Arrange
        dummy_budget = _dummy_budgetary(nb=4, na="Living")
        dummy_sub_budget = _dummy_sub_budgetary(nb=1, na="Rent", nbb=4)
        dummy_account = _dummy_account()
        dummy_currency = _dummy_currency()
        dummy_tx = _dummy_transaction(bu=4, sbu=1)
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[dummy_account],
            currencies=[dummy_currency],
            budgetaries=[dummy_budget],
            sub_budgetaries=[dummy_sub_budget],
        )

        # Act
        result = build_detailed_transactions(gsb)

        # Assert
        assert result is not None
        assert result[0].Sbu is not None
        assert result[0].Sbu.Na == "Rent"
        assert result[0].Sbu.Nbb is dummy_budget
```

Note: `_dummy_transaction` needs `bu` and `sbu` parameters — add them:

```python
def _dummy_transaction(
    nb: int = 1,
    ac: int = 1,
    cu: int = 1,
    pa: int = 0,
    ca: int = 0,
    sca: int = 0,
    bu: int = 0,
    sbu: int = 0,
    trt: int = 0,
) -> TransactionSection:
    return TransactionSection(
        Nb=nb,
        Ac=ac,
        Id=None,
        Dt=date(2023, 1, 15),
        Dv=None,
        Am=Decimal("42.50"),
        Cu=cu,
        Exb=False,
        Exr=Decimal("1"),
        Exf=Decimal("0"),
        Pa=pa,
        Ca=ca,
        Sca=sca,
        Br=False,
        No=None,
        Pn=0,
        Pc=None,
        Ma=TransactionMarkedState.NEW,
        Ar=0,
        Au=False,
        Re=0,
        Fi=0,
        Bu=bu,
        Sbu=sbu,
        Vo=None,
        Ba=None,
        Trt=trt,
        Mo=0,
    )
```

- [ ] **Step 3: Run the failing test**

```
uv run pytest tests/test_detailed_transactions.py::TestDetailedSubBudgetarySection -v
```

Expected: FAIL — `Sbu.Nbb` is `int`, not `BudgetarySection`.

- [ ] **Step 4: Add `DetailedSubBudgetarySection` to `sub_budgetary.py`**

Add after the existing `SubBudgetarySection` class in `src/gsbparse/domain/sections/sub_budgetary.py`:

```python
from gsbparse.domain.sections.budgetary import BudgetarySection


@dataclass(frozen=True)
class DetailedSubBudgetarySection(GsbFileSection):
    """A budget sub-line with its parent budgetary resolved.

    Attributes:
        Nbb: Parent budgetary (resolved from the raw ``Nbb`` identifier).
        Nb: Unique identifier within the parent budget line.
        Na: Display name.
    """

    Nbb: BudgetarySection
    Nb: int
    Na: str
```

- [ ] **Step 5: Update imports in `detailed_transaction.py`**

Replace:
```python
from gsbparse.domain.sections.sub_budgetary import SubBudgetarySection
```
With:
```python
from gsbparse.domain.sections.sub_budgetary import DetailedSubBudgetarySection
```

- [ ] **Step 6: Update `DetailedTransaction.Sbu` field type**

Replace:
```python
    Sbu: SubBudgetarySection | None
```
With:
```python
    Sbu: DetailedSubBudgetarySection | None
```

- [ ] **Step 7: Update `build_detailed_transactions`**

Replace:
```python
    sub_budgetaries: dict[int, SubBudgetarySection] = (
        {s.Nb: s for s in gsb_file.sub_budgetaries} if gsb_file.sub_budgetaries else {}
    )
```
With:
```python
    # Keyed by (parent_budgetary_nb, sub_budgetary_nb) to disambiguate shared Nb values.
    detailed_sub_budgetaries: dict[tuple[int, int], DetailedSubBudgetarySection] = {}
    if gsb_file.sub_budgetaries:
        for sb in gsb_file.sub_budgetaries:
            parent = budgetaries.get(sb.Nbb)
            if parent is None:
                _log.warning(
                    "SubBudgetary %d (parent=%d): parent budgetary not found — skipping",
                    sb.Nb,
                    sb.Nbb,
                )
                continue
            detailed_sub_budgetaries[(sb.Nbb, sb.Nb)] = DetailedSubBudgetarySection(
                Nbb=parent, Nb=sb.Nb, Na=sb.Na
            )
```

Then in Pass 1, replace:
```python
            Sbu=sub_budgetaries.get(tx.Sbu) if tx.Sbu != 0 else None,
```
With:
```python
            Sbu=detailed_sub_budgetaries.get((tx.Bu, tx.Sbu)) if tx.Sbu != 0 else None,
```

- [ ] **Step 8: Run all tests**

```
uv run pytest tests/test_detailed_transactions.py -v
```

Expected: all pass.

- [ ] **Step 9: Run full CI**

```
make ci
```

- [ ] **Step 10: Commit**

```bash
git add src/gsbparse/domain/sections/sub_budgetary.py \
        src/gsbparse/domain/detailed_transaction.py \
        tests/test_detailed_transactions.py
git commit -m "$(cat <<'EOF'
feat(domain/sections): Add DetailedSubBudgetarySection with resolved parent BudgetarySection

Resolves SubBudgetarySection.Nbb from int to BudgetarySection in the
DetailedTransaction view. Uses composite (parent_nb, child_nb) key to
correctly disambiguate sub-budgetaries sharing the same Nb across parents.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: `DetailedReconcileSection`

**Files:**
- Modify: `src/gsbparse/domain/sections/reconcile.py`
- Modify: `src/gsbparse/domain/detailed_transaction.py`
- Modify: `tests/test_detailed_transactions.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/test_detailed_transactions.py`:

```python
from gsbparse.domain.sections.reconcile import ReconcileSection


def _dummy_reconcile(nb: int = 1, na: str = "2023-1", acc: int = 1) -> ReconcileSection:
    return ReconcileSection(
        Nb=nb, Na=na, Acc=acc, Idate=None, Fdate=None,
        Ibal=Decimal("0"), Fbal=Decimal("0"),
    )


class TestDetailedReconcileSection:
    def test_reconcile_acc_resolves_to_account_section(self):
        # Arrange
        dummy_account = _dummy_account(number=1, name="Checking")
        dummy_currency = _dummy_currency()
        dummy_reconcile = _dummy_reconcile(nb=7, na="2023-1", acc=1)
        dummy_tx = _dummy_transaction(re=7)
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[dummy_account],
            currencies=[dummy_currency],
            reconciles=[dummy_reconcile],
        )

        # Act
        result = build_detailed_transactions(gsb)

        # Assert
        assert result is not None
        assert result[0].Re is not None
        assert result[0].Re.Na == "2023-1"
        assert result[0].Re.Acc is dummy_account

    def test_zero_reconcile_resolves_to_none(self):
        # Arrange
        dummy_account = _dummy_account()
        dummy_currency = _dummy_currency()
        dummy_tx = _dummy_transaction(re=0)
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[dummy_account],
            currencies=[dummy_currency],
        )

        result = build_detailed_transactions(gsb)

        assert result is not None
        assert result[0].Re is None
```

Note: `_dummy_transaction` needs a `re` parameter — add it to the helper:

```python
def _dummy_transaction(
    nb: int = 1,
    ac: int = 1,
    cu: int = 1,
    pa: int = 0,
    ca: int = 0,
    sca: int = 0,
    bu: int = 0,
    sbu: int = 0,
    trt: int = 0,
    re: int = 0,
) -> TransactionSection:
    return TransactionSection(
        Nb=nb,
        Ac=ac,
        Id=None,
        Dt=date(2023, 1, 15),
        Dv=None,
        Am=Decimal("42.50"),
        Cu=cu,
        Exb=False,
        Exr=Decimal("1"),
        Exf=Decimal("0"),
        Pa=pa,
        Ca=ca,
        Sca=sca,
        Br=False,
        No=None,
        Pn=0,
        Pc=None,
        Ma=TransactionMarkedState.NEW,
        Ar=0,
        Au=False,
        Re=re,
        Fi=0,
        Bu=bu,
        Sbu=sbu,
        Vo=None,
        Ba=None,
        Trt=trt,
        Mo=0,
    )
```

- [ ] **Step 2: Run the failing test**

```
uv run pytest tests/test_detailed_transactions.py::TestDetailedReconcileSection -v
```

Expected: FAIL — `Re.Acc` is `int`, not `AccountSection`.

- [ ] **Step 3: Add `DetailedReconcileSection` to `reconcile.py`**

Add after the existing `ReconcileSection` class in `src/gsbparse/domain/sections/reconcile.py`:

```python
from gsbparse.domain.sections.account import AccountSection


@dataclass(frozen=True)
class DetailedReconcileSection(GsbFileSection):
    """A reconciliation record with its account resolved.

    Attributes:
        Nb: Unique identifier.
        Na: Display name (e.g. ``"2007-1"``).
        Acc: Account this reconciliation belongs to (resolved from the raw ``Acc`` identifier).
        Idate: Start date of the reconciliation period (nullable).
        Fdate: End date of the reconciliation period (nullable).
        Ibal: Opening balance.
        Fbal: Closing balance.
    """

    Nb: int
    Na: str
    Acc: AccountSection
    Idate: date | None
    Fdate: date | None
    Ibal: Decimal
    Fbal: Decimal
```

- [ ] **Step 4: Update imports in `detailed_transaction.py`**

Replace:
```python
from gsbparse.domain.sections.reconcile import ReconcileSection
```
With:
```python
from gsbparse.domain.sections.reconcile import DetailedReconcileSection
```

- [ ] **Step 5: Update `DetailedTransaction.Re` field type**

Replace:
```python
    Re: ReconcileSection | None
```
With:
```python
    Re: DetailedReconcileSection | None
```

- [ ] **Step 6: Update `build_detailed_transactions`**

After the existing `accounts` lookup, add a `raw_accounts` lookup and replace the `reconciles` dict:

Replace:
```python
    accounts: dict[int, AccountSection] = (
        {a.Number: a for a in gsb_file.accounts} if gsb_file.accounts else {}
    )
```
With:
```python
    accounts: dict[int, AccountSection] = (
        {a.Number: a for a in gsb_file.accounts} if gsb_file.accounts else {}
    )

    detailed_reconciles: dict[int, DetailedReconcileSection] = {}
    if gsb_file.reconciles:
        for r in gsb_file.reconciles:
            acc = accounts.get(r.Acc)
            if acc is None:
                _log.warning(
                    "Reconcile %d: account %d not found — skipping", r.Nb, r.Acc
                )
                continue
            detailed_reconciles[r.Nb] = DetailedReconcileSection(
                Nb=r.Nb,
                Na=r.Na,
                Acc=acc,
                Idate=r.Idate,
                Fdate=r.Fdate,
                Ibal=r.Ibal,
                Fbal=r.Fbal,
            )
```

Then remove the existing `reconciles` dict:
```python
    reconciles: dict[int, ReconcileSection] = (
        {r.Nb: r for r in gsb_file.reconciles} if gsb_file.reconciles else {}
    )
```

And in Pass 1 replace:
```python
            Re=reconciles.get(tx.Re) if tx.Re != 0 else None,
```
With:
```python
            Re=detailed_reconciles.get(tx.Re) if tx.Re != 0 else None,
```

- [ ] **Step 7: Run all tests**

```
uv run pytest tests/test_detailed_transactions.py -v
```

Expected: all pass.

- [ ] **Step 8: Run full CI**

```
make ci
```

- [ ] **Step 9: Commit**

```bash
git add src/gsbparse/domain/sections/reconcile.py \
        src/gsbparse/domain/detailed_transaction.py \
        tests/test_detailed_transactions.py
git commit -m "$(cat <<'EOF'
feat(domain/sections): Add DetailedReconcileSection with resolved AccountSection

Resolves ReconcileSection.Acc from int to AccountSection in the
DetailedTransaction view.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: `DetailedAccountSection`

This task replaces the raw `AccountSection` on `DetailedTransaction.Ac` with a richer `DetailedAccountSection` that resolves Currency, Bank, Default_debit_method, and Default_credit_method. It also fixes the existing test that relied on object identity of the raw section.

**Files:**
- Modify: `src/gsbparse/domain/sections/account.py`
- Modify: `src/gsbparse/domain/detailed_transaction.py`
- Modify: `tests/test_detailed_transactions.py`

- [ ] **Step 1: Add helpers to the test file**

Add a `_dummy_bank` helper and imports to `tests/test_detailed_transactions.py`:

```python
from gsbparse.domain.sections.bank import BankSection


def _dummy_bank(nb: int = 1, na: str = "My Bank") -> BankSection:
    return BankSection(
        Nb=nb, Na=na, Co="", BIC="", Adr="", Tel="",
        Mail=None, Web=None, Nac="", Faxc="", Telc="", Mailc="", Rem=None,
    )
```

- [ ] **Step 2: Write the failing tests**

Add to `tests/test_detailed_transactions.py`:

```python
from gsbparse.domain.sections.account import DetailedAccountSection
from gsbparse.domain.sections.payment import PaymentSection


def _dummy_payment(number: int = 1, name: str = "Card") -> PaymentSection:
    return PaymentSection(
        Number=number, Name=name, Sign=0,
        Show_entry=False, Automatic_number=False, Current_number=None, Account=0,
    )


class TestDetailedAccountSection:
    def test_currency_resolves(self):
        # Arrange
        dummy_currency = _dummy_currency(nb=1, na="Euro")
        dummy_account = _dummy_account(number=1)  # Currency=1, Bank=0
        dummy_tx = _dummy_transaction(nb=1, ac=1, cu=1)
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[dummy_account],
            currencies=[dummy_currency],
        )

        # Act
        result = build_detailed_transactions(gsb)

        # Assert
        assert result is not None
        detailed_ac = result[0].Ac
        assert isinstance(detailed_ac, DetailedAccountSection)
        assert detailed_ac.Currency is dummy_currency

    def test_bank_resolves_when_nonzero(self):
        # Arrange
        dummy_currency = _dummy_currency()
        dummy_bank = _dummy_bank(nb=5, na="Savings Bank")
        raw_account = AccountSection(
            Name="Checking",
            Id=None,
            Number=1,
            Owner="",
            Kind=AccountKind.BANK,
            Currency=1,
            Path_icon="",
            Bank=5,  # non-zero → should resolve
            Bank_branch_code="",
            Bank_account_number="",
            Key="",
            Bank_account_IBAN="",
            Initial_balance=Decimal("0"),
            Minimum_wanted_balance=Decimal("0"),
            Minimum_authorised_balance=Decimal("0"),
            Closed_account=False,
            Show_marked=False,
            Show_archives_lines=False,
            Lines_per_transaction=1,
            Comment="",
            Owner_address="",
            Default_debit_method=0,
            Default_credit_method=0,
            Sort_by_method=False,
            Neutrals_inside_method=False,
            Sort_order="",
            Ascending_sort=True,
            Column_sort=0,
            Sorting_kind_column="",
            Bet_use_budget=0,
        )
        dummy_tx = _dummy_transaction(nb=1, ac=1, cu=1)
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[raw_account],
            currencies=[dummy_currency],
            banks=[dummy_bank],
        )

        result = build_detailed_transactions(gsb)

        assert result is not None
        assert result[0].Ac.Bank is dummy_bank

    def test_bank_is_none_when_zero(self):
        # Arrange
        dummy_currency = _dummy_currency()
        dummy_account = _dummy_account(number=1)  # Bank=0
        dummy_tx = _dummy_transaction(nb=1, ac=1, cu=1)
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[dummy_account],
            currencies=[dummy_currency],
        )

        result = build_detailed_transactions(gsb)

        assert result is not None
        assert result[0].Ac.Bank is None

    def test_default_debit_method_resolves_when_nonzero(self):
        # Arrange
        dummy_currency = _dummy_currency()
        dummy_payment = _dummy_payment(number=3, name="Cheque")
        raw_account = AccountSection(
            Name="Checking",
            Id=None,
            Number=1,
            Owner="",
            Kind=AccountKind.BANK,
            Currency=1,
            Path_icon="",
            Bank=0,
            Bank_branch_code="",
            Bank_account_number="",
            Key="",
            Bank_account_IBAN="",
            Initial_balance=Decimal("0"),
            Minimum_wanted_balance=Decimal("0"),
            Minimum_authorised_balance=Decimal("0"),
            Closed_account=False,
            Show_marked=False,
            Show_archives_lines=False,
            Lines_per_transaction=1,
            Comment="",
            Owner_address="",
            Default_debit_method=3,  # non-zero → should resolve
            Default_credit_method=0,
            Sort_by_method=False,
            Neutrals_inside_method=False,
            Sort_order="",
            Ascending_sort=True,
            Column_sort=0,
            Sorting_kind_column="",
            Bet_use_budget=0,
        )
        dummy_tx = _dummy_transaction(nb=1, ac=1, cu=1)
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[raw_account],
            currencies=[dummy_currency],
            payment_methods=[dummy_payment],
        )

        result = build_detailed_transactions(gsb)

        assert result is not None
        assert result[0].Ac.Default_debit_method is dummy_payment

    def test_default_methods_none_when_zero(self):
        dummy_currency = _dummy_currency()
        dummy_account = _dummy_account()  # Default_debit_method=1, Default_credit_method=1
        # No payment_methods in gsb → payment_methods dict is empty → None
        dummy_tx = _dummy_transaction()
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[dummy_account],
            currencies=[dummy_currency],
        )

        result = build_detailed_transactions(gsb)

        assert result is not None
        # _dummy_account has Default_debit_method=1 but no payment_methods provided → None
        assert result[0].Ac.Default_debit_method is None
        assert result[0].Ac.Default_credit_method is None

    def test_non_resolved_fields_are_copied_verbatim(self):
        dummy_currency = _dummy_currency()
        dummy_account = _dummy_account(number=1, name="My Account")
        dummy_tx = _dummy_transaction()
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[dummy_account],
            currencies=[dummy_currency],
        )

        result = build_detailed_transactions(gsb)

        assert result is not None
        ac = result[0].Ac
        assert ac.Name == "My Account"
        assert ac.Number == 1
        assert ac.Kind == AccountKind.BANK
```

- [ ] **Step 3: Run the failing tests**

```
uv run pytest tests/test_detailed_transactions.py::TestDetailedAccountSection -v
```

Expected: FAIL — `DetailedAccountSection` does not exist yet.

- [ ] **Step 4: Add `DetailedAccountSection` to `account.py`**

In `src/gsbparse/domain/sections/account.py`, add the imports and the new class after `AccountSection`:

```python
from gsbparse.domain.sections.bank import BankSection
from gsbparse.domain.sections.payment import PaymentSection


@dataclass(frozen=True)
class DetailedAccountSection(GsbFileSection):
    """An account with its currency, bank, and payment methods resolved.

    All fields mirror :class:`AccountSection` except the three FK integer fields
    which are replaced by their resolved domain objects.

    Attributes:
        Name: Account display name.
        Id: OFX account identifier (nullable).
        Number: Account number (internal).
        Owner: Account holder name.
        Kind: Account kind (checking / cash / liability / asset).
        Currency: Currency of this account (resolved from the raw ``Currency`` identifier).
        Path_icon: Path to the account icon file.
        Bank: Bank of this account (resolved; ``None`` when no bank is set).
        Bank_branch_code: Bank branch code.
        Bank_account_number: Bank account number string.
        Key: Account key / check digit.
        Bank_account_IBAN: IBAN string.
        Initial_balance: Opening balance.
        Minimum_wanted_balance: Target minimum balance.
        Minimum_authorised_balance: Authorised overdraft limit.
        Closed_account: Account is closed.
        Show_marked: Show only marked transactions by default.
        Show_archives_lines: Show archived transaction lines.
        Lines_per_transaction: Number of display lines per transaction.
        Comment: Free-text comment.
        Owner_address: Account holder address.
        Default_debit_method: Default payment method for debits (resolved; ``None`` when unset).
        Default_credit_method: Default payment method for credits (resolved; ``None`` when unset).
        Sort_by_method: Sort transactions by payment method.
        Neutrals_inside_method: Group neutral transactions inside method sort.
        Sort_order: Sort order specification string.
        Ascending_sort: Sort ascending.
        Column_sort: Column index used for sorting.
        Sorting_kind_column: Column-sort kind specification string.
        Bet_use_budget: Budget-estimate enabled (0 = off, ≥1 = on).
    """

    Name: str
    Id: str | None
    Number: int
    Owner: str
    Kind: AccountKind
    Currency: CurrencySection
    Path_icon: str
    Bank: BankSection | None
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
    Default_debit_method: PaymentSection | None
    Default_credit_method: PaymentSection | None
    Sort_by_method: bool
    Neutrals_inside_method: bool
    Sort_order: str
    Ascending_sort: bool
    Column_sort: int
    Sorting_kind_column: str
    Bet_use_budget: int
```

`CurrencySection` is already imported at the top of `account.py` (check — if not, add it):
```python
from gsbparse.domain.sections.currency import CurrencySection
```

- [ ] **Step 5: Update imports in `detailed_transaction.py`**

Replace:
```python
from gsbparse.domain.sections.account import AccountSection
```
With:
```python
from gsbparse.domain.sections.account import AccountSection, DetailedAccountSection
from gsbparse.domain.sections.bank import BankSection
```

- [ ] **Step 6: Update `DetailedTransaction.Ac` field type**

Replace:
```python
    Ac: AccountSection
```
With:
```python
    Ac: DetailedAccountSection
```

- [ ] **Step 7: Update `build_detailed_transactions` — add `banks` lookup and `detailed_accounts` construction**

After the existing `accounts: dict[int, AccountSection]` lookup, add:

```python
    banks: dict[int, BankSection] = (
        {b.Nb: b for b in gsb_file.banks} if gsb_file.banks else {}
    )

    detailed_accounts: dict[int, DetailedAccountSection] = {}
    if gsb_file.accounts:
        for a in gsb_file.accounts:
            currency = currencies.get(a.Currency)
            if currency is None:
                _log.warning(
                    "Account %d: currency %d not found — skipping", a.Number, a.Currency
                )
                continue
            detailed_accounts[a.Number] = DetailedAccountSection(
                Name=a.Name,
                Id=a.Id,
                Number=a.Number,
                Owner=a.Owner,
                Kind=a.Kind,
                Currency=currency,
                Path_icon=a.Path_icon,
                Bank=banks.get(a.Bank) if a.Bank != 0 else None,
                Bank_branch_code=a.Bank_branch_code,
                Bank_account_number=a.Bank_account_number,
                Key=a.Key,
                Bank_account_IBAN=a.Bank_account_IBAN,
                Initial_balance=a.Initial_balance,
                Minimum_wanted_balance=a.Minimum_wanted_balance,
                Minimum_authorised_balance=a.Minimum_authorised_balance,
                Closed_account=a.Closed_account,
                Show_marked=a.Show_marked,
                Show_archives_lines=a.Show_archives_lines,
                Lines_per_transaction=a.Lines_per_transaction,
                Comment=a.Comment,
                Owner_address=a.Owner_address,
                Default_debit_method=payment_methods.get(a.Default_debit_method) if a.Default_debit_method != 0 else None,
                Default_credit_method=payment_methods.get(a.Default_credit_method) if a.Default_credit_method != 0 else None,
                Sort_by_method=a.Sort_by_method,
                Neutrals_inside_method=a.Neutrals_inside_method,
                Sort_order=a.Sort_order,
                Ascending_sort=a.Ascending_sort,
                Column_sort=a.Column_sort,
                Sorting_kind_column=a.Sorting_kind_column,
                Bet_use_budget=a.Bet_use_budget,
            )
```

- [ ] **Step 8: Update Pass 1 to use `detailed_accounts`**

In Pass 1, replace:
```python
        account = accounts.get(tx.Ac)
        if account is None:
            _log.warning("Transaction %d: account %d not found — skipping", tx.Nb, tx.Ac)
            continue
```
With:
```python
        account = detailed_accounts.get(tx.Ac)
        if account is None:
            _log.warning("Transaction %d: account %d not found — skipping", tx.Nb, tx.Ac)
            continue
```

And in the `DetailedTransaction(...)` constructor call, replace:
```python
            Ac=account,
```
(this line is unchanged in content; mypy now infers `account: DetailedAccountSection`.)

Also remove the old warning block that checked `accounts.get(tx.Ac)` — `detailed_accounts` replaces it.

- [ ] **Step 9: Fix the broken existing test**

In `tests/test_detailed_transactions.py`, in `TestBuildDetailedTransactions.test_resolves_account_and_currency`, replace:

```python
        assert result[0].Ac is dummy_account
```
With:
```python
        assert result[0].Ac.Name == dummy_account_name
        assert result[0].Ac.Currency is dummy_currency
```

And add `dummy_account_name = "Checking"` to the Arrange block:

```python
    def test_resolves_account_and_currency(self):
        dummy_account_name = "Checking"
        dummy_account = _dummy_account(number=1, name=dummy_account_name)
        dummy_currency = _dummy_currency(nb=1, na="Euro")
        dummy_tx = _dummy_transaction(nb=1, ac=1, cu=1)
        gsb = _minimal_gsb_file(
            transactions=[dummy_tx],
            accounts=[dummy_account],
            currencies=[dummy_currency],
        )

        result = build_detailed_transactions(gsb)

        assert result is not None
        assert len(result) == 1
        assert result[0].Ac.Name == dummy_account_name
        assert result[0].Ac.Currency is dummy_currency
        assert result[0].Cu is dummy_currency
```

- [ ] **Step 10: Run all tests**

```
uv run pytest tests/test_detailed_transactions.py -v
```

Expected: all pass.

- [ ] **Step 11: Run full CI**

```
make ci
```

- [ ] **Step 12: Commit**

```bash
git add src/gsbparse/domain/sections/account.py \
        src/gsbparse/domain/detailed_transaction.py \
        tests/test_detailed_transactions.py
git commit -m "$(cat <<'EOF'
feat(domain/sections): Add DetailedAccountSection with resolved Currency, Bank, and payment methods

Resolves AccountSection.Currency, .Bank, .Default_debit_method, and
.Default_credit_method from int to their domain objects in the
DetailedTransaction view. Updates DetailedTransaction.Ac to
DetailedAccountSection throughout.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: Update exports

**Files:**
- Modify: `src/gsbparse/domain/sections/__init__.py`
- Modify: `src/gsbparse/__init__.py`

- [ ] **Step 1: Add exports to `domain/sections/__init__.py`**

In the imports block, add:
```python
from gsbparse.domain.sections.account import DetailedAccountSection
from gsbparse.domain.sections.reconcile import DetailedReconcileSection
from gsbparse.domain.sections.sub_budgetary import DetailedSubBudgetarySection
from gsbparse.domain.sections.sub_category import DetailedSubCategorySection
```

In the `__all__` list, add (in alphabetical position):
```python
    "DetailedAccountSection",
    "DetailedReconcileSection",
    "DetailedSubBudgetarySection",
    "DetailedSubCategorySection",
```

- [ ] **Step 2: Add exports to `src/gsbparse/__init__.py`**

In the `from gsbparse.domain.sections import (` block, add:
```python
    DetailedAccountSection,
    DetailedReconcileSection,
    DetailedSubBudgetarySection,
    DetailedSubCategorySection,
```

In the `__all__` list, add (in the section types block):
```python
    "DetailedAccountSection",
    "DetailedReconcileSection",
    "DetailedSubBudgetarySection",
    "DetailedSubCategorySection",
```

- [ ] **Step 3: Run full CI**

```
make ci
```

Expected: all pass.

- [ ] **Step 4: Commit**

```bash
git add src/gsbparse/domain/sections/__init__.py \
        src/gsbparse/__init__.py
git commit -m "$(cat <<'EOF'
feat: Re-export Detailed*Section types from public API

Adds DetailedAccountSection, DetailedSubCategorySection,
DetailedSubBudgetarySection, and DetailedReconcileSection to the
gsbparse.domain.sections and gsbparse public namespaces.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: E2E assertions

The example file (`tests/assets/example_3.0_en.gsb`) has:
- All 6 accounts use Currency=1 (GBP) and have a non-zero Bank FK.
- Account 4 ("Real Estate Loan [liabilities]") has Bank=1 ("HSBC UK Bank"). Transaction Nb=15 belongs to account 4.
- Transaction Nb=20 has Ca=15 ("Financial expenses"), Sca=3 ("Loan/Mortgage").
- Reconcile Nb=1 ("delayed-debit-card-[liabilities]-1") references account 5 ("Delayed Debit card [liabilities]"). Transaction Nb=127 has Re=1.
- The example file has no Sub_budgetary elements — no E2E assertion is possible for `Sbu`.

**Files:**
- Modify: `tests/test_e2e.py`

- [ ] **Step 1: Add E2E assertions for new nested paths**

In `tests/test_e2e.py`, inside `class TestDetailedTransactions`, add:

```python
    def test_account_currency_resolves(self, detailed):
        # All accounts use GBP (Currency=1). Verify via the first transaction (Nb=15, Ac=4).
        assert detailed is not None
        tx_15 = next(tx for tx in detailed if tx.Nb == 15)
        assert tx_15.Ac.Currency.Ico == "GBP"
        assert tx_15.Ac.Currency.Na == "Pound Sterling"

    def test_account_bank_resolves(self, detailed):
        # Transaction Nb=15 belongs to account 4 (Bank=1 = "HSBC UK Bank").
        assert detailed is not None
        tx_15 = next(tx for tx in detailed if tx.Nb == 15)
        assert tx_15.Ac.Bank is not None
        assert tx_15.Ac.Bank.Na == "HSBC UK Bank"

    def test_sub_category_parent_resolves(self, detailed):
        # Transaction Nb=20: Ca=15 ("Financial expenses"), Sca=3 ("Loan/Mortgage").
        assert detailed is not None
        tx_20 = next(tx for tx in detailed if tx.Nb == 20)
        assert tx_20.Sca is not None
        assert tx_20.Sca.Na == "Loan/Mortgage"
        assert tx_20.Sca.Nbc.Na == "Financial expenses"

    def test_reconcile_account_resolves(self, detailed):
        # Transaction Nb=127: Re=1 (reconcile "delayed-debit-card-[liabilities]-1", Acc=5).
        assert detailed is not None
        tx_127 = next(tx for tx in detailed if tx.Nb == 127)
        assert tx_127.Re is not None
        assert tx_127.Re.Na == "delayed-debit-card-[liabilities]-1"
        assert tx_127.Re.Acc.Name == "Delayed Debit card [liabilities]"

    def test_shared_detailed_account_identity(self, detailed):
        # Transactions on the same account share the same DetailedAccountSection instance.
        assert detailed is not None
        account_1_txs = [tx for tx in detailed if tx.Ac.Number == 1]
        assert len(account_1_txs) > 1  # sanity check
        ids = {id(tx.Ac) for tx in account_1_txs}
        assert len(ids) == 1
```

- [ ] **Step 2: Run the new E2E tests**

```
uv run pytest tests/test_e2e.py::TestDetailedTransactions -v
```

Expected: all pass.

- [ ] **Step 3: Run full CI**

```
make ci
```

- [ ] **Step 4: Commit**

```bash
git add tests/test_e2e.py
git commit -m "$(cat <<'EOF'
test(e2e): Add precise assertions for nested FK resolution in DetailedTransaction

Covers Ac.Currency, Ac.Bank, Sca.Nbc, Re.Acc, and shared account identity
against Example_3.0-en.gsb values.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```
