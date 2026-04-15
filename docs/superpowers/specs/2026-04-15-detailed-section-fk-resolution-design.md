# Design: FK resolution for nested sections in `DetailedTransaction`

**Date:** 2026-04-15
**Status:** Approved

## Context

`DetailedTransaction` already resolves all FK integers on `TransactionSection` to rich domain objects (`Ac→AccountSection`, `Cu→CurrencySection`, `Trt→DetailedTransaction`, etc.). However, several of those nested sections still carry raw FK integers internally:

| Section field | Raw type | Resolves to |
|---|---|---|
| `AccountSection.Currency` | `int` | `CurrencySection` |
| `AccountSection.Bank` | `int` | `BankSection \| None` |
| `AccountSection.Default_debit_method` | `int` | `PaymentSection \| None` |
| `AccountSection.Default_credit_method` | `int` | `PaymentSection \| None` |
| `SubCategorySection.Nbc` | `int` | `CategorySection` |
| `SubBudgetarySection.Nbb` | `int` | `BudgetarySection` |
| `ReconcileSection.Acc` | `int` | `AccountSection` |

This design resolves all of those FKs — but only in the `DetailedTransaction` view. `GsbFile.accounts`, `.sub_categories`, etc. continue to return the raw section types unchanged.

## New domain types

Four new frozen dataclasses, co-located with their raw counterparts:

### `DetailedAccountSection` (`account.py`)

Mirrors `AccountSection` field-for-field except:
- `Currency: CurrencySection` (was `int`)
- `Bank: BankSection | None` (was `int`; `0` → `None`)
- `Default_debit_method: PaymentSection | None` (was `int`; `0` → `None`)
- `Default_credit_method: PaymentSection | None` (was `int`; `0` → `None`)

All other fields (28 of them) are copied verbatim.

### `DetailedSubCategorySection` (`sub_category.py`)

Mirrors `SubCategorySection` except:
- `Nbc: CategorySection` (was `int`)

### `DetailedSubBudgetarySection` (`sub_budgetary.py`)

Mirrors `SubBudgetarySection` except:
- `Nbb: BudgetarySection` (was `int`)

### `DetailedReconcileSection` (`reconcile.py`)

Mirrors `ReconcileSection` except:
- `Acc: AccountSection` (was `int`; raw `AccountSection`, not `DetailedAccountSection`)

The reconcile back-reference uses raw `AccountSection` (not `DetailedAccountSection`) to avoid deep nesting that is rarely useful in practice.

All four types are re-exported from `domain/sections/__init__.py` and `src/gsbparse/__init__.py`.

## Changes to `DetailedTransaction`

Four field type changes:

| Field | Old type | New type |
|---|---|---|
| `Ac` | `AccountSection` | `DetailedAccountSection` |
| `Sca` | `SubCategorySection \| None` | `DetailedSubCategorySection \| None` |
| `Sbu` | `SubBudgetarySection \| None` | `DetailedSubBudgetarySection \| None` |
| `Re` | `ReconcileSection \| None` | `DetailedReconcileSection \| None` |

`Trt: DetailedTransaction | None` is unchanged — it already nests a `DetailedTransaction`, so `tx.Trt.Ac` is automatically a `DetailedAccountSection`.

No changes to `DEFAULT_DETAILED_TRANSACTION_COLUMNS`. All existing dotted paths (`"Ac.Name"`, `"Trt.Ac.Name"`, etc.) remain valid because `DetailedAccountSection` has the same field names as `AccountSection`. New paths (`"Ac.Currency.Ico"`, `"Ac.Bank.Na"`, `"Re.Acc.Na"`, etc.) become available for custom column projections.

## Changes to `build_detailed_transactions`

Before Pass 1, build additional lookup dicts:

1. `banks: dict[int, BankSection]` — from `gsb_file.banks` (keyed by `Nb`)
2. `detailed_accounts: dict[int, DetailedAccountSection]` — built by resolving each `AccountSection`'s `Currency`, `Bank`, `Default_debit_method`, `Default_credit_method`; replaces the existing `accounts` dict
3. `detailed_sub_categories: dict[int, DetailedSubCategorySection]` — resolving `Nbc` → `CategorySection`; replaces the existing `sub_categories` dict
4. `detailed_sub_budgetaries: dict[int, DetailedSubBudgetarySection]` — resolving `Nbb` → `BudgetarySection`; replaces the existing `sub_budgetaries` dict
5. `detailed_reconciles: dict[int, DetailedReconcileSection]` — resolving `Acc` → raw `AccountSection`; replaces the existing `reconciles` dict

Pass 1 uses these richer dicts in place of the raw ones. All other logic (Pass 2 Trt resolution, warning-and-skip on missing account/currency) is unchanged.

A missing currency on an `AccountSection` (needed to build `DetailedAccountSection`) logs a warning and causes any transaction referencing that account to be skipped — consistent with the existing skip behaviour for missing top-level account/currency.

## Testing

### Existing tests to update

Tests that construct `DetailedTransaction` directly with raw `AccountSection` must be updated to pass `DetailedAccountSection` instead. No new behaviour asserted — construction only.

### New unit tests

In `test_detailed_transactions.py` (or a dedicated file if it grows large):

- `DetailedAccountSection` wires all four resolved fields correctly (currency, bank, debit/credit methods; `Bank=None` when `0`)
- `DetailedSubCategorySection.Nbc` resolves to the correct `CategorySection`
- `DetailedSubBudgetarySection.Nbb` resolves to the correct `BudgetarySection`
- `DetailedReconcileSection.Acc` resolves to the correct raw `AccountSection`
- Warning logged + transaction skipped when `DetailedAccountSection` cannot be built (e.g. account references a missing currency)

### E2E additions

In `test_e2e.py`: select one transaction from `Example_3.0-en.gsb` with known values and assert precise values on new nested paths: `tx.Ac.Currency.Ico`, `tx.Ac.Bank` (or `None` if account has no bank), `tx.Re.Acc.Na` for a reconciled transaction if one exists.

**Orthogonality:** unit tests cover correct construction of the new `Detailed*Section` objects; the E2E test covers the full pipeline producing the right output. No overlap.

## Rejected alternatives

**Option B (flat promotion):** Add `AcCurrency`, `AcBank`, etc. as top-level fields on `DetailedTransaction`. Rejected: violates the "Not flat" design principle in CLAUDE.md and breaks the dotted-path column projection pattern.

**Option C (`__getattr__` delegation):** Wrapper types that delegate non-FK fields to the raw section. Rejected: incompatible with mypy strict and frozen dataclasses.
