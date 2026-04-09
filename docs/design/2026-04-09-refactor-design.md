# gsbparse refactor — design spec

**Date:** 2026-04-09
**Author:** Étienne Boisseau-Sierra (in design dialogue with Claude)
**Status:** Design locked. Implementation pending.
**Target version:** 1.0.0 (breaking release following legacy 0.3.0)

This is a standalone spec capturing every locked-in decision from the
design session. It's intended to be self-sufficient: a future contributor
(or Claude in a new session) should be able to read this file top-to-bottom
and have enough context to start the implementation without replaying the
conversation.

For behavioural rules and house preferences (not specific to this refactor),
see [`CLAUDE.md`](../../CLAUDE.md) at the repo root. Rules in `CLAUDE.md`
override anything in this spec.

---

## 1. Context and goals

`gsbparse` is a Python library that parses [Grisbi](https://github.com/grisbi/grisbi)
`.gsb` files. `.gsb` files are XML with a flat list of typed elements
(`<Currency>`, `<Transaction>`, `<Account>`, …), each with typed attributes
(`Nb`, `Na`, `Co`, …). The library's job is to turn such a file into typed
domain objects, and to optionally expose them as `pd.DataFrame`.

**Goals of the refactor:**

1. Full coverage of every section in the 2.3.2 format spec
   (`2025.12.28-format_fichier_grisbi-2.3.2.txt`). Unknown tags log a warning
   and are skipped.
2. Hexagonal architecture — a pure domain core, with XML and pandas as
   interchangeable adapters. Future output formats (polars, arrow) slot in
   as peer adapters.
3. Modern Python stack: Python 3.13+, `uv`, `pyproject.toml`, `ruff`, `mypy`,
   `import-linter`, `pre-commit`.
4. Typed-first domain model. DataFrames are an output concern; every piece of
   data has a frozen dataclass representation first.
5. Public documentation on Read the Docs.
6. A genuinely new 1.0.0 API — the legacy `gsbparse/` package is frozen at
   0.3.0 on PyPI; everything after that is breaking.

**Non-goals:**

- Writing `.gsb` files. Read-only.
- Validating that a `.gsb` file is semantically consistent (e.g. that all FKs
  resolve). The library surfaces whatever's in the file.
- Supporting Python < 3.13.
- Incremental/streaming parsing. Whole-file in-memory only.

---

## 2. Architecture — Ports and Adapters (hexagonal)

Chosen over strict n-tier because this is a library, not an application.
There's no presentation layer, no persistence layer, no application services
— the shape is "one input format, several possible output formats." That's
exactly what hexagonal is for.

**Three directories, enforced by `import-linter` in CI:**

- **`domain/`** — typed dataclasses, pure Python, zero third-party imports.
  The `GsbFile` aggregate, all `*Section` classes, `DetailedTransaction`,
  typed errors. Domain also imports no stdlib XML module (`xml.etree` is an
  input-format concern).
- **`ports/`** — abstract interfaces that domain declares and adapters
  implement. Empty in the MVP. Add a port the first time a second
  implementation justifies one.
- **`adapters/`** — concrete implementations. `adapters/xml/` parses a `.gsb`
  file into a `GsbFile`; `adapters/pandas/` renders domain objects to
  `pd.DataFrame`. Every external dependency (`defusedxml`, `pandas`) is
  confined to this layer.

**Import direction is unidirectional and enforced:**

- `domain/` → stdlib only (and not `xml.etree`).
- `ports/` → `domain/` only.
- `adapters/` → `domain/` and `ports/`. Never from each other.
- Top-level package `__init__.py` and shims (`pandas.py`, `xml.py`) → `adapters/` and `domain/`.
- Nothing else imports from `adapters/`.

**Program to an interface:** `typing.Protocol` for ports (structural, no
declaration on the implementing side — the Go-interface analogue). `abc.ABC`
only when nominal subclassing matters (e.g. the `GsbFileSection` base that
every concrete section dataclass inherits from).

**YAGNI on abstractions:** don't add a Protocol port until there's a second
implementation to justify it. One adapter = a concrete class is fine; two
adapters = extract a port.

---

## 3. Module structure

```text
src/gsbparse/
├── __init__.py                 # public API: read_gsb, GsbFile, *Section, errors
├── pandas.py                   # shim: re-exports adapters.pandas.to_df
├── xml.py                      # shim: re-exports adapters.xml.reader.read_gsb_file
├── domain/
│   ├── __init__.py
│   ├── file.py                 # GsbFile aggregate (dataclass)
│   ├── detailed_transaction.py # DetailedTransaction + DetailedTransactionColumn
│   │                           #   + DEFAULT_DETAILED_TRANSACTION_COLUMNS
│   ├── errors.py               # GsbParseError hierarchy
│   └── sections/
│       ├── __init__.py         # re-exports every *Section class
│       ├── _base.py            # GsbFileSection ABC — PURE dataclass, no parsers
│       ├── account.py
│       ├── amount_comparison.py
│       ├── archive.py
│       ├── bank.py
│       ├── bet.py
│       ├── bet_future.py
│       ├── bet_graph.py
│       ├── bet_historical.py
│       ├── budgetary.py
│       ├── category.py
│       ├── currency.py
│       ├── currency_link.py
│       ├── financial_year.py
│       ├── general.py
│       ├── partial_balance.py
│       ├── party.py
│       ├── payment.py
│       ├── print.py            # Legal — `print` is a builtin, not a keyword
│       ├── reconcile.py
│       ├── report.py
│       ├── rgba.py
│       ├── scheduled.py
│       ├── sub_budgetary.py
│       ├── sub_category.py
│       ├── text_comparison.py
│       └── transaction.py
├── ports/
│   └── __init__.py             # empty for MVP; docstring documents the trigger
└── adapters/
    ├── __init__.py
    ├── xml/
    │   ├── __init__.py         # exports read_gsb_file
    │   ├── reader.py           # read_gsb_file(path) → GsbFile
    │   ├── parsers.py          # parse_int/parse_bool/parse_date/parse_amount/
    │   │                       #   parse_str/parse_list_int + @parse_null/@parse_optional
    │   ├── _dispatch.py        # _ELEMENT_TAG_TO_PARSER dispatch table
    │   └── sections/
    │       ├── __init__.py
    │       ├── account.py      # parse_account_section(element) → AccountSection
    │       ├── currency.py
    │       └── …               # one file per section
    └── pandas/
        ├── __init__.py         # exports to_df
        ├── _sections.py        # list[GsbFileSection] → DataFrame
        └── _detailed_transactions.py
```

### Key structural decisions

**`from_xml` is NOT on domain section classes.** Domain `*Section`
dataclasses are pure — zero XML imports, zero parser logic. All
XML-to-section parsing lives in `adapters/xml/sections/<name>.py` as free
functions: `parse_currency_section(element) -> CurrencySection`. This is the
biggest divergence from the current `gsbparse2` layout and is required for a
genuinely pure domain.

**Parser helpers live in the XML adapter.** `parse_int`, `parse_bool`,
`parse_date`, `parse_amount`, `parse_str`, `parse_list_int`, and the
`@parse_null` / `@parse_optional` decorators encode Grisbi's XML conventions
(`"(null)"` sentinel, `%m/%d/%Y` date format, `"0"`/`"1"` booleans,
comma-decimal amounts). These are input-format concerns and belong in
`adapters/xml/parsers.py`, not in `domain/sections/_base.py`.

**`_ELEMENT_TAG_TO_PARSER` lives in the XML adapter**, not in domain. Maps
`"Currency" → parse_currency_section`. Domain has no reason to know XML tag
names exist.

**Public import paths decoupled from physical layout.** `src/gsbparse/pandas.py`
and `src/gsbparse/xml.py` are one-line shims that re-export from `adapters/`.
Users write `from gsbparse.pandas import to_df`; the `adapters/` hierarchy
never leaks. Swapping adapters (future `gsbparse.polars`) is a one-line import
change on the caller side.

### Ports — when to populate

`ports/` is empty in the MVP. The canonical future example is a
**`BytesSource` Protocol** for the XML reader, triggered by encrypted-file
reading support:

```python
# ports/bytes_source.py (future)
class BytesSource(Protocol):
    """A source of .gsb file bytes. Implementations:
    - FileBytesSource(path)          — plain file on disk (default)
    - EncryptedBytesSource(path, …)  — decrypts a Grisbi-encrypted file
    - InMemoryBytesSource(bytes)     — useful in tests
    """
    def read_bytes(self) -> bytes: ...
```

The XML reader would accept a `BytesSource` and not care where the bytes came
from. Add it when encrypted-file reading lands, not before.

---

## 4. Domain model

### 4.1 Section dataclasses

Every section is a frozen dataclass in `domain/sections/<name>.py`, inheriting
from `GsbFileSection` (the ABC in `_base.py`). Field names use Grisbi's
attribute codes (`Nb`, `Na`, `Co`, `Ac`, …) — faithful to the format spec
and consistent with the existing `gsbparse2` code. Ruff's `N815` lint is
disabled so these don't flag.

Example:

```python
# domain/sections/currency.py
from dataclasses import dataclass
from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class CurrencySection(GsbFileSection):
    """A currency defined in the Grisbi file."""
    Nb: int
    Na: str
    Co: str
    Ico: str
    Fl: int
```

No `from_xml`, no parser logic, no XML imports. Just fields.

### 4.2 `GsbFile` aggregate

The top-level container, holding one list per section type. Fields are
`list[SectionClass] | None` where `None` means the section is absent from the
file; an empty list means "section exists, no entries." This is a faithful
distinction.

```python
# domain/file.py
@dataclass(frozen=True)
class GsbFile:
    general: GeneralSection | None
    currencies: list[CurrencySection] | None
    accounts: list[AccountSection] | None
    parties: list[PartySection] | None
    categories: list[CategorySection] | None
    # … one field per section type

    @property
    def detailed_transactions(self) -> list[DetailedTransaction] | None:
        """Denormalized view: transactions with foreign keys resolved to
        the referenced typed section objects (nested, not flat)."""
```

### 4.3 `DetailedTransaction` — the rich representation

`DetailedTransaction` has **nested, resolved foreign-key fields.** Not flat.
The `Ac` field is an `AccountSection` instance, `Cu` is a `CurrencySection`,
`Pa` is `PartySection | None`, etc.

This is the richest information-preserving domain representation: no data is
discarded at the domain level, and shared identity
(`tx_a.Ac is tx_b.Ac` when both transactions reference the same account) is
preserved.

```python
# domain/detailed_transaction.py
@dataclass(frozen=True)
class DetailedTransaction:
    # Direct Transaction fields (Grisbi codes)
    Nb: int
    Dt: date
    Am: Decimal
    # … other direct fields

    # Foreign keys resolved to typed section objects (nested, lossless)
    Ac: AccountSection
    Cu: CurrencySection
    Pa: PartySection | None
    Ca: CategorySection | None
    Sc: SubCategorySection | None
    Bu: BudgetarySection | None
    Sb: SubBudgetarySection | None
    Fy: FinancialYearSection | None
    Pn: PaymentSection | None
    # … other FKs
```

**Why nested, not flat:** a flat `DetailedTransaction` discards the typed
structure of the referenced sections. Nested preserves every field of every
referenced section, lets the caller navigate typed attributes, and defers the
column-projection decision to the adapter layer. The domain representation
is lossless; the DataFrame representation is a projection.

### 4.4 Column projection for the detailed transactions DataFrame

```python
@dataclass(frozen=True)
class DetailedTransactionColumn:
    path: str          # dotted attribute path on DetailedTransaction, e.g. "Ac.Na"
    output_name: str   # column name in the output DataFrame, e.g. "account"
```

- Dotted paths resolve by walking attributes
  (`functools.reduce(getattr, path.split("."), tx)`).
- A library-defined `DEFAULT_DETAILED_TRANSACTION_COLUMNS: list[DetailedTransactionColumn]`
  is used when the caller passes no `columns=` argument.
- Invalid paths (typos, non-existent fields) raise a typed
  `UnknownDetailedTransactionPathError` at spec-validation time, *before*
  frame build.
- Paths that reference a nested optional section that is `None` on a given
  row resolve to `None` in the output (e.g. a transaction without a party
  gets `None` for `Pa.Na`).

**Default columns:**

```python
DEFAULT_DETAILED_TRANSACTION_COLUMNS: list[DetailedTransactionColumn] = [
    DetailedTransactionColumn("Nb",    "id"),
    DetailedTransactionColumn("Dt",    "date"),
    DetailedTransactionColumn("Dv",    "value_date"),
    DetailedTransactionColumn("Am",    "amount"),
    DetailedTransactionColumn("Br",    "is_transaction_breakdown"),
    DetailedTransactionColumn("Ma",    "state"),
    DetailedTransactionColumn("Cu.Na", "currency"),
    DetailedTransactionColumn("Ac.Na", "account"),
    DetailedTransactionColumn("Pa.Na", "party"),
    DetailedTransactionColumn("Ca.Na", "category"),
    DetailedTransactionColumn("Sc.Na", "subcategory"),
    DetailedTransactionColumn("Bu.Na", "budget"),
    DetailedTransactionColumn("Sb.Na", "sub_budget"),
    DetailedTransactionColumn("Pn.Na", "payment_method"),
    DetailedTransactionColumn("Pnc",   "payment_content"),
    DetailedTransactionColumn("No",    "notes"),
]
```

Default column policy: project the **name** (`Na`) of each FK'd section rather than the raw integer ID. `Br` (breakdown flag) and `Ma` (state) are direct fields included because they drive common filtering. The list is illustrative until section fields are confirmed during the format-spec pass; treat any diff as a deliberate change.

Domain uses Grisbi codes; pandas columns get descriptive names. Both are
correct in their layer.

---

## 5. Errors

Every exception subclasses a package-level `GsbParseError` base.

```python
# domain/errors.py
class GsbParseError(Exception):
    """Base class for every exception raised by gsbparse."""


class InvalidGsbFileError(GsbParseError):
    """The file could not be parsed as XML or the structure is invalid."""


class InvalidGsbFileRootError(InvalidGsbFileError):
    """The XML root element is not <Grisbi>."""


class SectionNotFoundError(GsbParseError):
    """A mandatory section is missing from the file."""


class InvalidElementCountError(GsbParseError):
    """A section's cardinality is violated (e.g. multiple <General>)."""


class XmlParsingError(GsbParseError):
    """An attribute value could not be parsed as its expected type."""


class UnknownDetailedTransactionPathError(GsbParseError):
    """A DetailedTransactionColumn.path references a non-existent attribute."""


class MixedSectionsError(GsbParseError, TypeError):
    """to_df was called with a list containing more than one concrete
    section type. Multiple-inherits from TypeError so generic handlers
    that catch TypeError still catch it. Carries a typed
    `found_types: list[type]` attribute for introspection."""

    def __init__(self, found_types: list[type]) -> None:
        self.found_types = found_types
        type_names = ", ".join(t.__name__ for t in found_types)
        super().__init__(
            f"to_df expected a homogeneous list of one section type, "
            f"but found multiple: {type_names}. Call to_df separately "
            f"for each section type."
        )
```

**Principles:**

- Errors are typed exceptions, raised at the layer where the problem is
  detected, and caught only where they can be handled meaningfully.
- No bare `except:`. No silent swallowing. No sentinel `None`-returns where
  an exception is the honest answer.
- Errors from the XML adapter chain the underlying `ET.ParseError` or
  `ValueError` via `raise … from err` so the original is preserved.

---

## 6. Public API

### 6.1 Domain navigation (pure Python, no pandas imports on this path)

```python
import gsbparse

gsb_file = gsbparse.read_gsb("my.gsb")      # thin alias for read_gsb_file
gsb_file.accounts                            # list[AccountSection] | None
gsb_file.currencies                          # list[CurrencySection] | None
gsb_file.detailed_transactions               # list[DetailedTransaction] | None

for tx in gsb_file.detailed_transactions:
    print(tx.Ac.Na, tx.Am)                   # typed nested access via resolved FKs
```

Two entry points to reading:

- `gsbparse.read_gsb(path)` — short top-level alias, ergonomic.
- `gsbparse.xml.read_gsb_file(path)` — long form, explicit about which adapter.

Both exist. Both do the same thing.

### 6.2 Pandas adapter — free function `to_df` in a submodule

```python
from gsbparse.pandas import to_df

accounts_df    = to_df(gsb_file.accounts)
currencies_df  = to_df(gsb_file.currencies)
detailed_tx_df = to_df(gsb_file.detailed_transactions)                   # default columns
detailed_tx_df = to_df(gsb_file.detailed_transactions, columns=[...])    # projected
```

**Dispatch rules:**

- `list[ConcreteSection]` (homogeneous) → flat per-section DataFrame.
- `list[DetailedTransaction]` → flattened DataFrame using
  `DetailedTransactionColumn` specs.
- `list[GsbFileSection]` mixing concrete types → raises `MixedSectionsError`.
- Unknown element type → raises `TypeError`.
- Empty list → empty DataFrame.

**Two `@typing.overload` signatures** for the type checker, one runtime
implementation:

```python
@overload
def to_df(sections: list[GsbFileSection]) -> pd.DataFrame: ...
@overload
def to_df(
    detailed_transactions: list[DetailedTransaction],
    columns: list[DetailedTransactionColumn] | None = None,
) -> pd.DataFrame: ...
def to_df(obj, columns=None):
    if not obj:
        return pd.DataFrame()
    if isinstance(obj[0], DetailedTransaction):
        return _detailed_transactions_to_dataframe(obj, columns)
    if isinstance(obj[0], GsbFileSection):
        found = {type(o) for o in obj}
        if len(found) > 1:
            raise MixedSectionsError(list(found))
        return _sections_to_dataframe(obj)
    raise TypeError(f"to_df does not handle {type(obj[0]).__name__}")
```

### 6.3 Why no top-level re-export of `to_df`

The user must write `from gsbparse.pandas import to_df`. Deliberate: it
keeps the adapter identity in the import line, so future adapters become
drop-in replacements:

```python
from gsbparse.pandas import to_df    # pandas
from gsbparse.polars import to_df    # polars (future)
from gsbparse.arrow  import to_table # arrow  (future)
```

Swapping the output format is a one-line import change; callers of `to_df(...)`
are untouched.

Discoverability is handled by README, RTD Quickstart, and a "See also"
pointer in the `GsbFile` docstring — not by top-level re-export.

### 6.4 Rejected alternative: `gsb_file.accounts.to_df()`

Considered and rejected. It fails under hexagonal: either `SectionList[T]`
lives in `domain/` and imports pandas (domain leaks), or it lives in
`adapters/` and `GsbFile.accounts` must return it (reverse dependency). No
clean seam. Do not revisit.

---

## 7. Testing strategy

**Five layers**, each testing something the layer below can't. The discipline
rule: **a behaviour is tested in exactly one place.** Higher-level tests trust
the assertions of lower-level tests instead of re-asserting them.

### Layer 1 — Parser helpers

`tests/adapters/xml/test_parsers.py`. Pure functions, heavily parametrized.
Tests every helper × (valid input, null sentinel, invalid input, optional
toggle).

### Layer 2 — Per-section parsers

`tests/adapters/xml/sections/test_<section>.py`. **One file per section.**
Tests each `parse_*_section` function with inline XML fragments.

**Scope per section:** the behaviour, not every field. A "fully populated
instance" assertion (one equality on the whole dataclass) covers field
wiring. Separate tests for null handling on nullable fields, type-conversion
edges (dates, amounts), errors on malformed input. Don't write one test per
field — the equality assertion subsumes them.

**No magic literals.** Every input value is a `dummy_*` local at the top of
the Arrange block, reused in both the input construction and the
expected-result construction:

```python
def test_parse_currency_section_returns_fully_populated_instance():
    # Arrange
    dummy_currency_id = 1
    dummy_currency_name = "Euro"
    dummy_currency_code = "€"
    dummy_currency_iso_code = "EUR"
    dummy_currency_fraction_digits = 2

    input_element = ET.fromstring(
        f'<Currency Nb="{dummy_currency_id}" Na="{dummy_currency_name}" '
        f'Co="{dummy_currency_code}" Ico="{dummy_currency_iso_code}" '
        f'Fl="{dummy_currency_fraction_digits}" />'
    )
    expected_result = CurrencySection(
        Nb=dummy_currency_id,
        Na=dummy_currency_name,
        Co=dummy_currency_code,
        Ico=dummy_currency_iso_code,
        Fl=dummy_currency_fraction_digits,
    )

    # Act
    actual_result = parse_currency_section(input_element)

    # Assert
    assert actual_result == expected_result
```

### Layer 3 — XML reader

`tests/adapters/xml/test_reader.py`. Tests file-level behaviour: dispatch,
unknown-tag tolerance (log + skip), empty files, wrong root (`InvalidGsbFileRootError`),
cardinality violations (`InvalidElementCountError`).

Ports the existing `tests/test_file.py` tests, which already cover the right
behaviours. Does **not** re-test field wiring (Layer 2's job).

### Layer 4 — Pandas adapter

Two test files:

- `tests/adapters/pandas/test_sections_to_df.py` — `to_df(list[GsbFileSection])`:
  empty list → empty DataFrame; columns match field names; row count matches;
  round-trip to dicts equals original; `MixedSectionsError` on mixed types.
- `tests/adapters/pandas/test_detailed_transactions_to_df.py` —
  `to_df(list[DetailedTransaction], columns=...)`: default columns produce
  documented layout; custom specs produce the right columns; dotted paths
  resolve (`"Ac.Name"` through nested section); optional `None` nested
  sections yield `None` cells; invalid paths raise
  `UnknownDetailedTransactionPathError` at spec-validation time, before any
  row is built.

### Layer 5 — End-to-end with `Example_3.0-en.gsb`

`tests/e2e/test_example_file.py`. **One fixture file, one module.** This is
the acceptance gate.

**Precise-value assertions, not structural invariants.** Pin actual content
from the example file so a regression anywhere in the pipeline surfaces as a
concrete diff. The lower layers tell you *where* a break is; Layer 5 tells
you *that* the pipeline-as-a-whole still produces the right output.

```python
def test_example_file_first_detailed_transaction_resolves_account(example_gsb_file):
    # Act
    actual_first_tx = example_gsb_file.detailed_transactions[0]

    # Assert — typed nested access works, FK resolved to the right object
    assert actual_first_tx.Ac.Name == "Compte courant"
    assert actual_first_tx.Cu.Ico == "EUR"
    assert actual_first_tx.Am == Decimal("-42.50")
    assert actual_first_tx.Dt == date(2018, 1, 15)
```

Each test asserts one behaviour; no omnibus "everything works" test. First
run reads real values from `Example_3.0-en.gsb`, bakes them into the
assertions, and freezes.

### Test directory layout

```text
tests/
├── __init__.py
├── conftest.py                      # shared fixtures (Example_3.0-en.gsb path)
├── adapters/
│   ├── xml/
│   │   ├── test_parsers.py                  # Layer 1
│   │   ├── test_reader.py                   # Layer 3
│   │   └── sections/
│   │       ├── test_account.py              # Layer 2 — one per section
│   │       ├── test_currency.py
│   │       └── …
│   └── pandas/
│       ├── test_sections_to_df.py           # Layer 4a
│       └── test_detailed_transactions_to_df.py  # Layer 4b
├── domain/
│   └── test_detailed_transaction.py         # column path resolution, defaults
└── e2e/
    └── test_example_file.py                 # Layer 5
```

### What we are NOT testing

- The dispatch table directly (transitively tested by Layer 3).
- `GsbFile` dataclass shape (that's just frozen-dataclass behaviour).
- Mocking `read_gsb_file` in Layer 4/5 unless strictly needed.
- Property-based tests (Hypothesis) in the MVP.
- Coverage percentage. Test the listed behaviours; ship when they pass.

---

## 8. Tooling

### 8.1 Build backend and dependency management

- **Build backend:** `hatchling`.
- **Dependency management:** `uv`.
- **`pyproject.toml`** is the single source of truth (replaces `setup.py`,
  `setup.cfg`, `ruff.toml`).
- **Python:** `>=3.13`.
- **Runtime deps:** `defusedxml>=0.7`, `pandas>=2.2`. Both core, neither
  optional.

### 8.2 pyproject.toml skeleton

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "gsbparse"
dynamic = ["version"]
description = "Parse Grisbi .gsb files into typed domain objects and pandas DataFrames"
readme = "README.md"
requires-python = ">=3.13"
license = "GPL-2.0-or-later"
authors = [{ name = "Étienne Boisseau-Sierra" }]
keywords = ["grisbi", "gsb", "accounting", "parser", "pandas"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
    "Topic :: Office/Business :: Financial :: Accounting",
    "Typing :: Typed",
]
dependencies = [
    "defusedxml>=0.7",
    "pandas>=2.2",
]

[project.urls]
Homepage      = "https://github.com/etnbsd/gsbparse"
Documentation = "https://gsbparse.readthedocs.io"
Repository    = "https://github.com/etnbsd/gsbparse"
Issues        = "https://github.com/etnbsd/gsbparse/issues"

[dependency-groups]
dev = [
    "pytest>=8",
    "pytest-cov>=5",
    "ruff>=0.6",
    "mypy>=1.11",
    "pre-commit>=3.8",
    "conventional-pre-commit>=3.4",
    "import-linter>=2.0",
    "pandas-stubs",
    "sphinx>=8",
    "sphinx-autodoc-typehints>=2",
    "sphinx-rtd-theme>=3.0",
    "myst-parser>=4",
]

[tool.hatch.version]
path = "src/gsbparse/__init__.py"

[tool.hatch.build.targets.wheel]
packages = ["src/gsbparse"]

[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP", "SIM", "T20", "D", "N", "RUF"]
ignore = [
    "D100", "D104", "D107",   # missing module/package/__init__ docstrings
    "N815",                   # mixedCase fields — Grisbi codes (Nb, Na, Co)
]

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["D", "S101"]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.mypy]
python_version = "3.13"
strict = true
warn_unreachable = true
files = ["src", "tests"]

[[tool.mypy.overrides]]
module = ["defusedxml.*"]
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "-ra",
    "--strict-markers",
    "--strict-config",
    "--cov=gsbparse",
    "--cov-report=term-missing",
]

[tool.coverage.run]
source = ["src/gsbparse"]
branch = true

[tool.importlinter]
root_package = "gsbparse"

[[tool.importlinter.contracts]]
name = "Domain has no outward dependencies"
type = "forbidden"
source_modules = ["gsbparse.domain"]
forbidden_modules = [
    "gsbparse.adapters",
    "gsbparse.ports",
    "pandas",
    "defusedxml",
    "xml.etree",
]

[[tool.importlinter.contracts]]
name = "Ports only import from domain"
type = "forbidden"
source_modules = ["gsbparse.ports"]
forbidden_modules = ["gsbparse.adapters"]

[[tool.importlinter.contracts]]
name = "Adapters never import from each other"
type = "independence"
modules = ["gsbparse.adapters.xml", "gsbparse.adapters.pandas"]
```

**Version source:** `__version__` in `src/gsbparse/__init__.py`, read by
hatchling.

**Key lint rules:** `T20` forbids `print()`; `N815` ignored so Grisbi codes
(`Nb`, `Na`) don't flag; `D` with Google convention enforces docstrings on
public API but not on tests.

### 8.3 pre-commit configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-merge-conflict
      - id: check-added-large-files

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.2
    hooks:
      - id: mypy
        additional_dependencies: [pandas-stubs, defusedxml]

  - repo: https://github.com/seddonym/import-linter
    rev: v2.1
    hooks:
      - id: import-linter

  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.4.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
        args: [feat, fix, chore, docs, test, refactor, style, ci, build, perf]
```

### 8.4 Makefile (ergonomic aliases)

`just` was considered and rejected. Makefile:

```makefile
# Makefile
.PHONY: default install test lint format type-check import-check ci

default:
    @echo "Targets: install test lint format type-check import-check ci"

install:
    uv sync --dev

test:
    uv run pytest

lint:
    uv run ruff check .

format:
    uv run ruff format .

type-check:
    uv run mypy

import-check:
    uv run lint-imports

ci: lint format type-check import-check test
```

`make ci` runs the full gauntlet locally before pushing.

### 8.5 GitHub Actions — CI

`.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.13", "3.14"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
        with:
          version: "latest"
          enable-cache: true
      - run: uv python install ${{ matrix.python-version }}
      - run: uv sync --dev
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run mypy
      - run: uv run lint-imports
      - run: uv run pytest
```

Matrix: `ubuntu-latest` × Python 3.13 and 3.14. 3.13 is the minimum supported
version; 3.14 tests forward compatibility. OS matrix not needed — the library
is pure Python with no OS-specific behaviour.

### 8.6 GitHub Actions — Publish to PyPI (OIDC trusted publishing)

`.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - "v*"

jobs:
  publish:
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write   # trusted publishing
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv python install 3.13
      - run: uv sync --dev
      - run: uv run pytest
      - run: uv build
      - uses: pypa/gh-action-pypi-publish@release/v1
```

**PyPI trusted publishing via OIDC** — no long-lived API token in secrets.
Configure once on PyPI (trusted publisher pointing at this repo), then GitHub
Actions authenticates via the environment.

### 8.7 Release process — deferred

**Not building a release script in this refactor.** For the MVP, releases are
manual:

```shell
# 1. Bump __version__ in src/gsbparse/__init__.py by hand
# 2. Commit:
git commit -m "chore: Release 0.5.0"
# 3. Tag and push:
git tag -a v0.5.0 -m "Release 0.5.0"
git push origin main
git push origin v0.5.0
# 4. CI picks up the tag, publishes to PyPI, and creates a GitHub Release
#    draft with auto-generated notes from commit messages since the last tag.
# 5. Edit the GitHub Release notes by hand before publishing.
```

If a scripted `make release VERSION=0.5.0` becomes worth building later, it
goes in the `Makefile`, not a standalone `scripts/release.py`.

**No `CHANGELOG.md`.** GitHub Releases are the single source of truth for
release notes. Conventional commit history + GitHub's auto-generated release
notes cover the need; a separate changelog file is redundant and drifts.

---

## 9. Documentation (Read the Docs)

- **Tool:** Sphinx (chosen over MkDocs — typed-library autodoc is tighter).
- **Theme:** Read the Docs theme (`sphinx-rtd-theme`) — familiar, well-supported on RTD.
- **Extensions:**
  - `sphinx.ext.autodoc` + `sphinx-autodoc-typehints` — API docs from typed
    signatures.
  - `myst-parser` — Markdown source (avoid rST where possible).
  - `sphinx.ext.intersphinx` — link to Python/pandas stdlib docs.
- **Hosted on:** Read the Docs. `latest` tracks main, `stable` tracks the
  most recent release tag. Versioned docs on every tag.

### 9.1 docs/ layout

```text
docs/
├── conf.py                  # Sphinx config
├── index.md                 # landing page (MyST markdown)
├── quickstart.md            # "read a .gsb file in 3 lines"
├── guide/
│   ├── domain-model.md      # GsbFile, sections, DetailedTransaction walkthrough
│   ├── pandas-adapter.md    # to_df, default columns, custom columns
│   ├── errors.md            # exception hierarchy, when each is raised
│   └── architecture.md      # hexagonal layering, why it matters for contributors
├── migration/
│   └── from-0.3.md          # breaking-change migration guide
├── api/
│   └── index.md             # autodoc: gsbparse, gsbparse.pandas, gsbparse.xml
├── design/                  # design specs (this file lives here)
│   └── 2026-04-09-refactor-design.md
└── _static/
```

### 9.2 .readthedocs.yaml

```yaml
version: 2
build:
  os: ubuntu-24.04
  tools:
    python: "3.13"
  jobs:
    post_create_environment:
      - pip install uv
    post_install:
      - uv sync --dev

sphinx:
  configuration: docs/conf.py
  fail_on_warning: true
```

---

## 10. Migration plan

Trunk-based development on `main`. No long-lived branches. The current
`restructure` branch is abandoned (its work is salvaged into the new commit
sequence).

**Acceptable broken-state window:** between the "remove legacy" commits and
the first working end-to-end commit, main will have failing tests and a
non-functional `import gsbparse`. This is fine because:

- The repo is low-traffic.
- 0.3.0 is pinned on PyPI for anyone needing the legacy API.
- No bugfix requests are expected against the legacy API during the rewrite.
- The next release is breaking anyway.

### 10.1 Commit sequence

```shell
# 1. Freeze the past
chore: Release 0.3.0 of legacy package to PyPI            # manual release, no code change

# 2. Clear the decks (two separate commits — one concern each)
chore: Remove legacy gsbparse package
chore: Remove gsbparse2 scaffold

# 3. Foundation
chore: Adopt src/ layout and pyproject.toml
chore: Migrate dependency management to uv
chore(lint): Configure ruff, mypy, import-linter
ci: Add GitHub Actions workflow for lint and tests
ci: Enforce conventional commits via pre-commit

# 4. Domain scaffolding
feat(domain): Add GsbParseError hierarchy
feat(domain/sections): Add GsbFileSection base dataclass
feat(domain/sections): Add CurrencySection
feat(domain/sections): Add AccountSection
# … one commit per section

# 5. XML adapter
feat(adapters/xml): Add parser helpers
feat(adapters/xml/sections): Add currency section parser
feat(adapters/xml/sections): Add account section parser
# … one per section
feat(adapters/xml): Add read_gsb_file dispatch

# 6. Detailed transactions
feat(domain): Add DetailedTransaction with resolved FKs
feat(domain): Add DetailedTransactionColumn and defaults

# 7. Pandas adapter
feat(adapters/pandas): Add to_df for homogeneous section lists
feat(adapters/pandas): Add to_df for detailed transactions

# 8. Public surface + docs
feat: Expose public API at gsbparse top level
feat(docs): Add Sphinx + Read the Docs configuration
docs: Write migration guide from 0.3.x to 1.0.0

# 9. Ship
chore: Release 1.0.0
```

### 10.2 Commit conventions

- **Format:** Conventional Commits — `type(scope): Description`.
- **Capitalized description** (house style): `feat(domain): Add CurrencySection`,
  not `feat(domain): add CurrencySection`. `conventional-pre-commit` doesn't
  enforce casing — it's a review-time rule.
- **Scopes mirror directories:** `domain`, `domain/sections`, `adapters/xml`,
  `adapters/xml/sections`, `adapters/pandas`, `ports`, `lint`, etc. Omit
  scope for repo-wide chores.
- **One commit = one concern.** Never use "and" or ";" to join two distinct
  changes in a subject line.
- **Plain commits only:** `git commit -m "..."`. No `--no-verify`, no GPG
  flags unless explicitly asked.

### 10.3 PyPI release strategy

- **0.3.0** — last legacy release. Frozen on main immediately before
  clearing the decks. Cut from the current code state.
- **0.4.0a1, 0.4.0a2, …** (optional) — alphas from main during the rewrite
  for early adopters. Each alpha must correspond to a coherent state of
  main (green CI, `import gsbparse` works).
- **1.0.0** — first stable release of the new API, cut after the full commit
  sequence lands.

---

## 11. Deferred / open decisions

Things explicitly not decided yet. Revisit when the relevant commit approaches.

- **Exact fields on every `*Section` dataclass.** The format spec
  (`2025.12.28-format_fichier_grisbi-2.3.2.txt`) is authoritative, but it
  contains known errors and some attributes need live validation against
  `Example_3.0-en.gsb`. A single upfront pass through the spec before
  implementation will settle the full catalogue.
- **Ports population trigger.** `ports/` is empty at MVP. First real port
  expected to be `BytesSource` for encrypted-file reading (§3, "Ports — when
  to populate"). Encrypted-file support is explicitly deferred post-MVP.
- **Release script.** Not built now. If manual releases become painful, add a
  `make release VERSION=…` target in the Makefile. No standalone
  `scripts/release.py`.

---

## 12. References

- [`CLAUDE.md`](../../CLAUDE.md) — house preferences, standing rules, architecture notes.
- `2025.12.28-format_fichier_grisbi-2.3.2.txt` — current format spec (2.3.2).
- `2021.01.17-format_fichier_grisbi-2.0.0.txt` — previous format spec; kept
  as reference, superseded by 2.3.2.
- `Example_3.0-en.gsb` — reference fixture for E2E tests.
- Current `gsbparse2/` — in-progress rewrite to be deleted as part of the
  migration. Its work is salvaged into the commit sequence in §10.1.
