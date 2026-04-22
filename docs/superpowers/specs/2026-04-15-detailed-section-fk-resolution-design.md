# Design: FK resolution for nested sections in `DetailedTransaction`

**Date:** 2026-04-15
**Status:** Approved

## Context

`DetailedTransaction` already resolves all FK integers on `Transaction` to rich domain objects (`Ac→Account`, `Cu→Currency`, `Trt→DetailedTransaction`, etc.). However, several of those nested sections still carry raw FK integers internally:

| Section field | Raw type | Resolves to |
|---|---|---|
| `Account.Currency` | `int` | `Currency` |
| `Account.Bank` | `int` | `Bank \| None` |
| `Account.Default_debit_method` | `int` | `Payment \| None` |
| `Account.Default_credit_method` | `int` | `Payment \| None` |
| `SubCategory.Nbc` | `int` | `Category` |
| `SubBudgetary.Nbb` | `int` | `Budgetary` |
| `Reconcile.Acc` | `int` | `Account` |

This design resolves all of those FKs — but only in the `DetailedTransaction` view. `GsbFile.accounts`, `.sub_categories`, etc. continue to return the raw section types unchanged.

## New domain types

Four new frozen dataclasses, co-located with their raw counterparts:

### `DetailedAccount` (`account.py`)

Mirrors `Account` field-for-field except:
- `Currency: Currency` (was `int`)
- `Bank: Bank | None` (was `int`; `0` → `None`)
- `Default_debit_method: Payment | None` (was `int`; `0` → `None`)
- `Default_credit_method: Payment | None` (was `int`; `0` → `None`)

All other fields (28 of them) are copied verbatim.

### `DetailedSubCategory` (`sub_category.py`)

Mirrors `SubCategory` except:
- `Nbc: Category` (was `int`)

### `DetailedSubBudgetary` (`sub_budgetary.py`)

Mirrors `SubBudgetary` except:
- `Nbb: Budgetary` (was `int`)

### `DetailedReconcile` (`reconcile.py`)

Mirrors `Reconcile` except:
- `Acc: Account` (was `int`; raw `Account`, not `DetailedAccount`)

The reconcile back-reference uses raw `Account` (not `DetailedAccount`) to avoid deep nesting that is rarely useful in practice.

All four types are re-exported from `domain/sections/__init__.py` and `src/gsbparse/__init__.py`.

## Changes to `DetailedTransaction`

Four field type changes:

| Field | Old type | New type |
|---|---|---|
| `Ac` | `Account` | `DetailedAccount` |
| `Sca` | `SubCategory \| None` | `DetailedSubCategory \| None` |
| `Sbu` | `SubBudgetary \| None` | `DetailedSubBudgetary \| None` |
| `Re` | `Reconcile \| None` | `DetailedReconcile \| None` |

`Trt: DetailedTransaction | None` is unchanged — it already nests a `DetailedTransaction`, so `tx.Trt.Ac` is automatically a `DetailedAccount`.

No changes to `DEFAULT_DETAILED_TRANSACTION_COLUMNS`. All existing dotted paths (`"Ac.Name"`, `"Trt.Ac.Name"`, etc.) remain valid because `DetailedAccount` has the same field names as `Account`. New paths (`"Ac.Currency.Ico"`, `"Ac.Bank.Na"`, `"Re.Acc.Na"`, etc.) become available for custom column projections.

## Changes to `build_detailed_transactions`

Before Pass 1, build additional lookup dicts:

1. `banks: dict[int, Bank]` — from `gsb_file.banks` (keyed by `Nb`)
2. `detailed_accounts: dict[int, DetailedAccount]` — built by resolving each `Account`'s `Currency`, `Bank`, `Default_debit_method`, `Default_credit_method`; replaces the existing `accounts` dict
3. `detailed_sub_categories: dict[int, DetailedSubCategory]` — resolving `Nbc` → `Category`; replaces the existing `sub_categories` dict
4. `detailed_sub_budgetaries: dict[int, DetailedSubBudgetary]` — resolving `Nbb` → `Budgetary`; replaces the existing `sub_budgetaries` dict
5. `detailed_reconciles: dict[int, DetailedReconcile]` — resolving `Acc` → raw `Account`; replaces the existing `reconciles` dict

Pass 1 uses these richer dicts in place of the raw ones. All other logic (Pass 2 Trt resolution, warning-and-skip on missing account/currency) is unchanged.

A missing currency on an `Account` (needed to build `DetailedAccount`) logs a warning and causes any transaction referencing that account to be skipped — consistent with the existing skip behaviour for missing top-level account/currency.

## Testing

### Existing tests to update

Tests that construct `DetailedTransaction` directly with raw `Account` must be updated to pass `DetailedAccount` instead. No new behaviour asserted — construction only.

### New unit tests

In `test_detailed_transactions.py` (or a dedicated file if it grows large):

- `DetailedAccount` wires all four resolved fields correctly (currency, bank, debit/credit methods; `Bank=None` when `0`)
- `DetailedSubCategory.Nbc` resolves to the correct `Category`
- `DetailedSubBudgetary.Nbb` resolves to the correct `Budgetary`
- `DetailedReconcile.Acc` resolves to the correct raw `Account`
- Warning logged + transaction skipped when `DetailedAccount` cannot be built (e.g. account references a missing currency)

### E2E additions

In `test_e2e.py`: select one transaction from `Example_3.0-en.gsb` with known values and assert precise values on new nested paths: `tx.Ac.Currency.Ico`, `tx.Ac.Bank` (or `None` if account has no bank), `tx.Re.Acc.Na` for a reconciled transaction if one exists.

**Orthogonality:** unit tests cover correct construction of the new `Detailed*Section` objects; the E2E test covers the full pipeline producing the right output. No overlap.

## Rejected alternatives

**Option B (flat promotion):** Add `AcCurrency`, `AcBank`, etc. as top-level fields on `DetailedTransaction`. Rejected: violates the "Not flat" design principle in CLAUDE.md and breaks the dotted-path column projection pattern.

**Option C (`__getattr__` delegation):** Wrapper types that delegate non-FK fields to the raw section. Rejected: incompatible with mypy strict and frozen dataclasses.

**Option D (generic `expand()` / runtime depth):** A generic free function or method — `expand(gsb.transactions, depth=N)` or `gsb.transactions.expand(depth=N)` — that resolves FK fields to arbitrary depth at call time.

Rejected for four independent reasons:

1. **Static types become `Any`.** The return type of `expand(gsb.transactions, depth=2)` cannot be expressed without recursive generics or `Any`. The value of `DetailedTransaction` is precisely that mypy knows `tx.Ac.Currency` is a `Currency`. A runtime depth parameter erases that.

2. **The FK graph is not uniform.** `depth=N` implies a uniform tree. Grisbi's FK graph is not: `Transaction → Account → Currency` is 2 hops; `Transaction → Category` is 1 hop (no further FKs); `Transaction → Reconcile → Account` is 2 hops. A single integer cannot capture which paths to follow and where to stop. The current design encodes those decisions explicitly in the `Detailed*Section` types — which is the right time to make them.

3. **Resolution requires full-file context.** Resolving `Account.Currency: int → Currency` requires `gsb_file.currencies`. A standalone `expand(gsb.transactions)` cannot resolve FKs without the full file. The signature collapses to `expand(gsb)` — making the `.transactions` argument redundant — or `expand(gsb.transactions, context=gsb)`, which is `build_detailed_transactions(gsb)` with a worse name.

4. **Frozen dataclasses with typed fields are the idiom.** There is no mechanism to generically produce a new typed, frozen dataclass at runtime. The type *is* the schema. The closest ORM analogies (Django `select_related()`, SQLAlchemy `joinedload()`) name specific relationships to join — they are not generic depth parameters. Explicitness over runtime magic is the right tradeoff here.
