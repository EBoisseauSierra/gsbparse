# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About

`gsbparse` is a Python library that parses [Grisbi](https://github.com/grisbi/grisbi) `.gsb` files. `.gsb` files are XML with a flat list of typed elements (`<Currency>`, `<Transaction>`, `<Account>`, etc.), each with typed attributes. The library's goal is to expose each section type a DataClass (or list thereof, if there are multiple entries of that section), plus provides an easy way to convert them into a `pd.DataFrame`. In addition, we provide a parametrizable denormalized transactions DataFrame with foreign keys resolved to human-readable names for users' convenience.

## Current state

The hexagonal refactor is complete and on `main`. The legacy `gsbparse/` and working-name `gsbparse2/` directories are superseded by the new `src/gsbparse/` layout. Version is `1.0.0.dev0`.

**Repository layout:**

- **`src/gsbparse/`** — the production package, `src/` layout. Hexagonal architecture: `domain/`, `adapters/xml/`, `adapters/pandas/`, `ports/` (empty MVP placeholder).
- **`tests/`** — pytest suite (98 tests). Uses `tmp_path` with inline XML for unit/integration tests; `tests/assets/Example_3.0-en.gsb` for E2E tests.
- **`docs/`** — Sphinx documentation (sphinx-rtd-theme, myst-parser, sphinx-autodoc-typehints). Build: `uv run sphinx-build -b html docs docs/_build/html`.
- **`gsbparse/`** — legacy package (frozen at PyPI 0.3.0). Do not add features here.
- **`gsbparse2/`** — working-name directory from during the parallel rewrite. Superseded by `src/gsbparse/`. Do not add features here.
- **`2025.12.28-format_fichier_grisbi-2.3.2.txt`** — most recent format spec (may contain errors). Supersedes `2021.01.17-format_fichier_grisbi-2.0.0.txt`.

## Standing preferences (from user)

These apply to every change in this repo. Re-read before planning or committing.

### Naming

- Prefer longer, more descriptive names over short cryptic ones. Naming consistency across the codebase matters.

### Architecture

- **Ports and Adapters (hexagonal).** The library has one input format (XML) today and potentially many output formats (pandas now, polars/arrow/csv/json later); that is exactly the shape hexagonal was designed for.
  - `domain/` — typed dataclasses, pure Python, zero pandas/numpy imports. The `GsbFile` aggregate, all `*Section` classes, `DetailedTransaction`, typed errors.
  - `ports/` — abstract interfaces (`typing.Protocol` or `abc.ABC`) that the domain declares and adapters implement. Add a port the first time a second adapter justifies it; don't pre-abstract.
  - `adapters/` — the concrete implementations: `adapters/xml/` (parses a `.gsb` file into a `GsbFile`), `adapters/pandas/` (renders domain objects to `pd.DataFrame`). Every external dependency (`defusedxml`, `pandas`) is confined to this layer.
- **Import direction is enforced.** Domain imports nothing outside itself (stdlib only). Adapters import from domain, never the reverse. Enforce with `import-linter` in CI; a PR that imports `adapters` from `domain` fails the build.
- **Program to an interface**: `typing.Protocol` is the Python equivalent of a Go interface — structural, no declaration needed on the implementing side. Use it for ports. `abc.ABC` only when nominal subclassing matters (e.g. shared parser helpers on a base section class).
- **YAGNI on abstractions.** Don't add a Protocol port until there's a second implementation to justify it. One adapter = a concrete class is fine; two adapters = extract a port.
- Follow the Zen of Python (`import this`). Flat over nested, explicit over implicit, one obvious way.
- Break the system into small units with a single clear purpose and well-defined interfaces. Each unit should be understandable and testable in isolation.

### Testing

- Test relevant *behaviours*, not lines. Do not bloat tests to chase coverage.
- Structure each test with **Arrange, Act, Assert** (AAA).
- Use `pytest.mark.parametrize` when multiple inputs exercise the same behaviour.
- **Test orthogonality**: a behaviour is tested in *exactly one* place. No two tests assert the same thing. If Layer 2 asserts "every field of `CurrencySection` is wired correctly from XML", no Layer 3/4/5 test re-asserts it.
- **No magic numbers / strings in tests.** Extract every input value into a `dummy_*` local at the top of the Arrange block (`dummy_currency_iso_code = "EUR"`) and reuse the same name in both the input construction and the expected-result construction. Reads like a story; assertion failures point at a labelled value.
- **E2E tests assert on precise values** from `Example_3.0-en.gsb`, not on structural invariants ("non-empty", "FK resolved to *some* account"). The lower layers tell you *where* a break is; the E2E layer tells you *that* the pipeline-as-a-whole still produces the right output. Bake real values from the example file into the assertions; freeze them; treat any future diff as a regression to investigate.

### Tooling

- Target the modern Python stack: `uv`, `pyproject.toml` (not `setup.py`/`setup.cfg`), `pre-commit`, CI/CD via GitHub Actions.
- **Build backend:** `hatchling`. Version is dynamic, read from `__version__` in `src/gsbparse/__init__.py`.
- **Python 3.13+.** CI matrix: `ubuntu-latest` × Python 3.13 and 3.14 — 3.13 is the minimum supported version, 3.14 tested for forward compatibility.
- Ruff for lint + format. mypy for type checking (strict mode). `import-linter` for hexagonal boundary enforcement.
- Pre-commit hooks must enforce conventional commits (`conventional-pre-commit` is already wired).
- **Makefile** (not `just`) for ergonomic local command aliases: `make ci`, `make test`, `make lint`, etc.
- **Public documentation on Read the Docs.** Sphinx + Read the Docs theme (`sphinx-rtd-theme`) + `sphinx-autodoc-typehints` + `myst-parser`. Markdown source (MyST), not rST. `.readthedocs.yaml` pins Python 3.13 and installs via uv.
- **PyPI publishing via OIDC trusted publishing** — no long-lived API tokens in GitHub secrets. Configure once on PyPI, publish fires on `X.Y.Z` tag push.
- **No `CHANGELOG.md`.** GitHub Releases are the single source of truth for release notes, auto-generated from conventional commit history and hand-edited before publishing.
- **Release process: manual for now.** Bump `__version__` by hand, commit, tag, push. No `scripts/release.py`. If automation becomes worth it later, add a `make release VERSION=…` target in the Makefile — do not build a standalone script.

### Runtime behaviour

- **Logging, not prints.** Use `logging.getLogger(__name__)` in every module. No `print()` in library code. Ruff `T20` already forbids it — keep it on.
- **Proper error handling.** Errors are typed exceptions (subclasses of a package-level base), raised at the layer where the problem is detected, and caught only where they can be handled meaningfully. No bare `except:`. No silent swallowing. No sentinel `None`-returns where an exception is the honest answer.

### Git workflow

- **Trunk-based development.** Short-lived branches, frequent integration into `main`. Avoid long-lived feature branches. Prefer small, independently-mergeable commits.
- **Conventional Commits** — enforced by `conventional-pre-commit` on the `commit-msg` stage.
- **Capitalized descriptions.** House style: the description after `type(scope):` starts with a capital letter. E.g. `feat(domain): Add CurrencySection`, not `feat(domain): add CurrencySection`. `conventional-pre-commit` doesn't enforce this — it's a review-time rule.
- **Scopes are directory-based** and match the hexagonal layout: `domain`, `domain/sections`, `adapters/xml`, `adapters/xml/sections`, `adapters/pandas`, `ports`, `lint`, etc. Omit the scope for repo-wide chores and top-level shim changes.
- **Plain commits only**: `git commit -m "..."`. Never `--no-verify`, never GPG-related flags (`--no-gpg-sign`, `-S`, etc.) unless the user explicitly asks.
- **One commit = one concern.** A commit message must never use "and" or ";" to join two distinct changes. If there are two concerns, make two commits.

### Documentation discipline

- Keep `CLAUDE.md` and `README.md` up to date **in the same session** as the change that affects them. Never defer docs to a follow-up.
- Update these files whenever commands, architecture, release process, or key design decisions change.

### Brainstorming with Claude (prompting tips from lived experience)

Lessons from this session's design dialogue — apply when asking Claude for architecture/API recommendations:

- **Force first-principles framing.** "Ignore the existing code. If you were designing X from scratch, what's the richest possible representation?" prevents Claude from anchoring on whatever's currently there.
- **Steelman the maximally-rich option first.** Before Claude recommends anything, ask it to steelman the opposite of what it's about to propose. Information-dense domain models (e.g. nested/resolved references) are often dismissed prematurely as "complex" when they're actually simpler.
- **Name the design axes explicitly.** "Propose options that cross these dimensions: (a) information density, (b) schema binding time, (c) API shape, (d) layering." Otherwise Claude tends to vary along only one axis.
- **Ask for anti-examples.** "What's the worst version of this and why?" surfaces assumptions faster than asking for the best version.

## Commands

```shell
# Install for development
uv sync --dev
pre-commit install

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_file.py

# Run a single test
uv run pytest tests/test_file.py::test_parse_file_returns_empty_dict_if_no_sections

# Lint
uv run ruff check .

# Format
uv run ruff format .

# Type check (strict)
uv run mypy

# Enforce hexagonal import boundaries
uv run lint-imports

# Run everything (same as CI)
make ci

# Build Sphinx docs locally
uv run sphinx-build -b html docs docs/_build/html

# Run pre-commit on all files
pre-commit run --all-files
```

## Locked-in design decisions for the refactor

These are agreed with the user and must be honoured by every subsequent change.

### Scope and migration

- **Scope**: full coverage of every section in the 2.3.2 format spec. Unknown tags log a warning and are skipped (tolerant mode — future-proof against Grisbi evolution).
- **Migration**: the rewrite replaces `gsbparse/` in place — no `gsbparse2/` at the end. Breaking API change; old API frozen on PyPI 0.3.0. README must document the break.
- **Python**: 3.13+.
- **Runtime deps**: `defusedxml`, `pandas` (both core, neither optional).
- **Dev/test deps**: `pytest`, `pytest-cov`, `ruff`, `mypy`, `pre-commit`, `conventional-pre-commit`, `import-linter`, plus Sphinx for docs.

### Domain model

- **Typed-first.** Every piece of data has a frozen dataclass representation. DataFrames are an adapter-layer concern.
- **Section dataclasses keep Grisbi attribute codes** as field names (`Nb`, `Na`, `Co`, `Ac`, etc.) — faithful to the format spec and consistent with the existing `gsbparse2` code.
- **`DetailedTransaction` has nested, resolved foreign-key fields.** Not flat. The `Ac` field is an `AccountSection` instance, `Cu` is a `CurrencySection`, `Pa` is `PartySection | None`, etc. This is the richest information-preserving domain representation: no data is discarded at domain level, and shared identity (`tx_a.Ac is tx_b.Ac` when both transactions reference the same account) is preserved.
- **Pandas column names come from `DetailedTransactionColumn` specs**, not from section field names. Domain uses Grisbi codes; pandas columns get descriptive names. Both are correct in their layer.

### Column projection for the detailed transactions DataFrame

```python
@dataclass(frozen=True)
class DetailedTransactionColumn:
    path: str          # dotted attribute path on DetailedTransaction, e.g. "Ac.Na"
    output_name: str   # column name in the output DataFrame, e.g. "account"
```

- Dotted paths resolve by walking attributes (`functools.reduce(getattr, path.split("."), tx)`).
- A library-defined `DEFAULT_DETAILED_TRANSACTION_COLUMNS: list[DetailedTransactionColumn]` is used when the caller passes no `columns=` argument.
- Invalid paths (typos, non-existent fields) raise a typed `UnknownDetailedTransactionPathError` at spec-validation time, before frame build.
- Paths that reference a nested optional section that is `None` on a given row resolve to `None` in the output (e.g. a transaction without a party gets `None` for `Pa.Na`).

### Errors

- Every exception is a subclass of a package-level `GsbParseError` base.
- `SectionNotFoundError` — optional section missing when marked mandatory.
- `InvalidElementCountError` — cardinality violation (e.g. multiple `General` sections).
- `InvalidGsbFileError` / `InvalidGsbFileRootError` — malformed file / wrong root tag.
- `XmlParsingError` — value cannot be parsed as the expected type.
- `UnknownDetailedTransactionPathError` — column spec references a non-existent path.
- `MixedSectionsError(GsbParseError, TypeError)` — `to_df` was called with a list mixing more than one concrete section type. Multiple-inherits from `TypeError` so generic `except TypeError` still catches it; carries a typed `found_types: list[type]` attribute.

### Public API shape

**Domain navigation** (pure Python, no pandas imports on this path):

```python
gsb_file = gsbparse.read_gsb("my.gsb")     # thin alias for GsbFile.from_file
gsb_file.accounts                           # list[AccountSection] | None
gsb_file.currencies                         # list[CurrencySection] | None
gsb_file.detailed_transactions              # list[DetailedTransaction] | None
for tx in gsb_file.detailed_transactions:
    print(tx.Ac.Na, tx.Am)                  # typed nested access via resolved FKs
```

**Pandas adapter** — free function `to_df` in a submodule:

```python
from gsbparse.pandas import to_df

accounts_df    = to_df(gsb_file.accounts)
currencies_df  = to_df(gsb_file.currencies)
detailed_tx_df = to_df(gsb_file.detailed_transactions)                # default columns
detailed_tx_df = to_df(gsb_file.detailed_transactions, columns=[...]) # projected
```

- `to_df` dispatches on the element type of the input list: `list[GsbFileSection]` → flat per-section DataFrame; `list[DetailedTransaction]` → flattened DataFrame using `DetailedTransactionColumn` specs.
- Two `@typing.overload` signatures for the type checker, one runtime implementation.
- **No top-level re-export** of `to_df`. The user must write `from gsbparse.pandas import to_df`. This is deliberate: it keeps the adapter identity in the import line, so future adapters become drop-in replacements:

  ```python
  from gsbparse.pandas import to_df   # pandas
  from gsbparse.polars import to_df   # polars  (future)
  from gsbparse.arrow  import to_table  # arrow (future)
  ```

  Swapping the output format is a one-line import change; callers of `to_df(...)` are untouched.
- Discoverability is handled by README, RTD Quickstart, and a "See also" pointer in the `GsbFile` docstring — not by top-level re-export.

**Option rejected:** `gsb_file.accounts.to_df()` was considered. It fails under hexagonal: either `SectionList[T]` lives in `domain/` and imports pandas (domain leaks), or it lives in `adapters/` and `GsbFile.accounts` must return it (reverse dependency). No clean seam. Do not revisit.

### Module structure

```text
src/gsbparse/
├── __init__.py                 # re-exports: read_gsb, GsbFile, *Section, errors…
├── pandas.py                   # shim: re-exports adapters.pandas.to_df
├── xml.py                      # shim: re-exports adapters.xml.reader.read_gsb_file
├── domain/
│   ├── file.py                 # GsbFile aggregate
│   ├── detailed_transaction.py # DetailedTransaction + DetailedTransactionColumn
│   ├── errors.py               # GsbParseError hierarchy
│   └── sections/
│       ├── _base.py            # GsbFileSection ABC — PURE dataclass, no parsers
│       ├── account.py          # one file per Grisbi tag; pure dataclasses only
│       ├── currency.py
│       ├── print.py            # `print` is a builtin, not a keyword — legal module name
│       └── …
├── ports/
│   └── __init__.py             # empty for MVP; docstring documents the trigger
└── adapters/
    ├── xml/
    │   ├── reader.py           # read_gsb_file(path) → GsbFile
    │   ├── parsers.py          # parse_int/parse_bool/parse_date/parse_amount/…
    │   │                       #   + @parse_null / @parse_optional decorators
    │   ├── _dispatch.py        # _ELEMENT_TAG_TO_PARSER table
    │   └── sections/
    │       ├── account.py      # parse_account_section(element) → AccountSection
    │       └── …               # one file per section
    └── pandas/
        ├── __init__.py         # exports to_df
        ├── _sections.py        # list[GsbFileSection] → DataFrame
        └── _detailed_transactions.py
```

Key properties:

- **`src/` layout.** Prevents accidental imports of the in-tree package during tests.
- **Public import paths decoupled from physical layout.** `src/gsbparse/pandas.py` and `src/gsbparse/xml.py` are one-line shims that re-export from `adapters/`. Users write `from gsbparse.pandas import to_df`; the `adapters/` hierarchy never leaks. Swapping adapters (future `gsbparse.polars`) is still a one-line import change on the caller side.
- **`from_xml` is NOT on domain section classes.** Domain `*Section` dataclasses are pure — zero XML imports, zero parser logic. All XML-to-section parsing lives in `adapters/xml/sections/<name>.py` as free functions (`parse_currency_section(element) → CurrencySection`). This is the biggest divergence from the current `gsbparse2` layout and is required for a genuinely pure domain.
- **Parser helpers live in the XML adapter.** `parse_int`, `parse_bool`, `parse_date`, `parse_amount`, `parse_str`, `parse_list_int`, and the `@parse_null` / `@parse_optional` decorators encode Grisbi's XML conventions (`"(null)"` sentinel, `%m/%d/%Y` date format, `"0"`/`"1"` booleans, comma-decimal amounts). These are input-format concerns and belong in `adapters/xml/parsers.py`, not in `domain/sections/_base.py`.
- **`_ELEMENT_TAG_TO_PARSER` lives in the XML adapter**, not in domain. Maps `"Currency" → parse_currency_section`. Domain has no reason to know XML tag names exist.
- **Import direction enforced by `import-linter` in CI.** Contracts: `domain/` imports stdlib only; `ports/` imports from `domain/` only; `adapters/` import from `domain/` and `ports/` only; nothing imports from `adapters/` except the top-level shims and `__init__.py`.

### Ports — when to populate

`ports/` is empty in the MVP. A port goes in `ports/` the first time the domain (or an adapter the reader composes with) needs to *call out* to something with plausible multiple implementations. The canonical future example is a **`BytesSource` Protocol** for the XML reader:

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

The XML reader accepts a `BytesSource` and doesn't care where the bytes come from. This is the kind of port that earns its keep: real abstraction, multiple implementations foreseeable, clean seam between "how do I get bytes" and "how do I parse bytes". Add it when encrypted-file reading lands, not before.

## Architecture notes

### `src/gsbparse/` building blocks

- `adapters/xml/reader.py` — `read_gsb_file(path)` wraps `defusedxml.ElementTree.parse`, validates the root is `<Grisbi>`, and dispatches each element tag via `_ELEMENT_TAG_TO_PARSER`. Raises `InvalidGsbFileError` / `InvalidGsbFileRootError`.
- `adapters/xml/parsers.py` — `parse_int`, `parse_bool`, `parse_date`, `parse_amount`, `parse_str`, `parse_list_int`, plus `@parse_null` (returns `None` for `"(null)"`) and `@parse_optional` decorators. All XML-format knowledge lives here.
- `adapters/xml/_dispatch.py` — `_ELEMENT_TAG_TO_PARSER` table mapping tag names to free functions.
- `adapters/xml/sections/<tag>.py` — one file per XML tag; free function `parse_<name>_section(element) → <Name>Section`.
- `domain/sections/<tag>.py` — one file per tag; frozen dataclass, typed fields, zero XML imports.
- `domain/file.py` — `GsbFile` frozen dataclass aggregate; `detailed_transactions` property builds `DetailedTransaction` objects via `build_detailed_transactions`.
- `domain/detailed_transaction.py` — `DetailedTransaction` (FK-resolved view) + `DetailedTransactionColumn` + `build_detailed_transactions`.
- `domain/errors.py` — typed error hierarchy rooted at `GsbParseError`.
- `adapters/pandas/` — `to_df` free function with two `@overload` signatures; dispatches on list element type.

### Adding a new section

1. Create `src/gsbparse/domain/sections/<name>.py` — frozen dataclass with typed fields (Grisbi attribute codes), no XML imports.
2. Create `src/gsbparse/adapters/xml/sections/<name>.py` — free function `parse_<name>_section(element) → <Name>Section` using helpers from `adapters/xml/parsers.py`.
3. Register in `_ELEMENT_TAG_TO_PARSER` in `adapters/xml/_dispatch.py`.
4. Add a field on `GsbFile` in `domain/file.py` and wire it in `adapters/xml/reader.py`.
5. Re-export the new section class from `domain/sections/__init__.py` and `src/gsbparse/__init__.py`.
