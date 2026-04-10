# gsbparse

A Python library for parsing [Grisbi](https://github.com/grisbi/grisbi) `.gsb` accounting files
into typed domain objects, with an optional pandas adapter for DataFrame output.

**Documentation:** [gsbparse.readthedocs.io](https://gsbparse.readthedocs.io)

---

## Breaking change from 0.3.0

Version 1.0 is a ground-up rewrite. The old `AccountFile` / `Transactions` API is gone.
The last compatible release is **0.3.0** on PyPI. If you depend on the old API, pin
`gsbparse==0.3.0` before upgrading.

---

## Installation

```shell
pip install gsbparse
```

Or with [uv](https://docs.astral.sh/uv/):

```shell
uv add gsbparse
```

Requires Python 3.13+.

---

## Quickstart

### Read a file

```python
import gsbparse

gsb = gsbparse.read_gsb("my_accounts.gsb")
```

### Access typed sections

```python
print(gsb.general.Ti)        # file title

for account in gsb.accounts:
    print(account.Nb, account.Na)    # id, name

for currency in gsb.currencies:
    print(currency.Na, currency.Co)  # name, ISO code
```

### Detailed transactions (foreign keys resolved)

```python
for tx in gsb.detailed_transactions:
    print(tx.Ac.Na, tx.Am)   # account name, amount (Decimal)
    if tx.Pa:
        print(tx.Pa.Na)       # party name
    if tx.Ca:
        print(tx.Ca.Na)       # category name
```

### Convert to pandas DataFrame

```python
from gsbparse.pandas import to_df

accounts_df    = to_df(gsb.accounts)
currencies_df  = to_df(gsb.currencies)
detailed_tx_df = to_df(gsb.detailed_transactions)
```

Custom column projection:

```python
from gsbparse import DetailedTransactionColumn

columns = [
    DetailedTransactionColumn(path="Dt",    output_name="date"),
    DetailedTransactionColumn(path="Am",    output_name="amount"),
    DetailedTransactionColumn(path="Ac.Na", output_name="account"),
    DetailedTransactionColumn(path="Pa.Na", output_name="party"),
]

df = to_df(gsb.detailed_transactions, columns=columns)
```

See the [full quickstart](https://gsbparse.readthedocs.io/en/latest/quickstart.html) and
[API reference](https://gsbparse.readthedocs.io/en/latest/api.html) on Read the Docs.

---

## Development

```shell
git clone https://github.com/etnbsd/gsbparse.git
cd gsbparse
uv sync --dev
pre-commit install
```

Common commands (via `make`):

| Command            | What it does                         |
|--------------------|--------------------------------------|
| `make test`        | Run the test suite                   |
| `make lint`        | Run ruff check                       |
| `make format`      | Run ruff format                      |
| `make type-check`  | Run mypy in strict mode              |
| `make import-check`| Enforce hexagonal import boundaries  |
| `make ci`          | Run all of the above                 |

### Contributing

1. Fork the repo and create a short-lived branch.
2. Follow [Conventional Commits](https://www.conventionalcommits.org/) — enforced by pre-commit.
3. Open a pull request against `main`.
