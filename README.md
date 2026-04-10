# gsbparse

A Python library for parsing [Grisbi](https://github.com/grisbi/grisbi) `.gsb` accounting files
into typed domain objects, with an optional pandas adapter for DataFrame output.

**Documentation:** [gsbparse.readthedocs.io](https://gsbparse.readthedocs.io)

## Installation

```shell
pip install gsbparse
```

Or with [uv](https://docs.astral.sh/uv/):

```shell
uv add gsbparse
```

Requires Python 3.13+.

## Quickstart

### Read a file

```python
import gsbparse

gsb = gsbparse.read_gsb("my_accounts.gsb")
```

### Inspect typed sections

```python
>>> gsb.currencies
[CurrencySection(Nb=1, Na='Euro', Co='€', Ico='EUR', Fl=2), CurrencySection(Nb=2, Na='US Dollar', Co='$', Ico='USD', Fl=2)]

>>> for account in gsb.accounts:
...     print(account.Number, account.Name)
1 Checking
2 Savings

```

### Detailed transactions (foreign keys resolved)

```python
>>> tx = gsb.detailed_transactions[0]
>>> tx.Dt
datetime.date(2024, 1, 5)
>>> tx.Am
Decimal('-42.50')
>>> tx.Ac.Name
'Checking'
>>> tx.Pa.Na
'Supermarket'

```

### Convert to pandas DataFrame

```python
>>> import gsbparse.pandas as gsbpd
>>> gsbpd.to_df(gsb.currencies)
   Nb         Na Co  Ico  Fl
0   1       Euro  €  EUR   2
1   2  US Dollar  $  USD   2

```

Custom column projection:

```python
>>> from gsbparse import DetailedTransactionColumn
>>> columns = [
...     DetailedTransactionColumn(path="Dt",      output_name="date"),
...     DetailedTransactionColumn(path="Am",      output_name="amount"),
...     DetailedTransactionColumn(path="Ac.Name", output_name="account"),
...     DetailedTransactionColumn(path="Pa.Na",   output_name="party"),
...     DetailedTransactionColumn(path="Ca.Na",   output_name="category"),
... ]
>>> gsbpd.to_df(gsb.detailed_transactions, columns=columns)
         date   amount   account        party category
0  2024-01-05   -42.50  Checking  Supermarket     Food
1  2024-01-31  2500.00  Checking     Employer   Income

```

See the [full quickstart](https://gsbparse.readthedocs.io/en/latest/quickstart.html) and
[API reference](https://gsbparse.readthedocs.io/en/latest/api.html) on Read the Docs.

## Development

```shell
git clone https://github.com/etnbsd/gsbparse.git
cd gsbparse
uv sync --dev
pre-commit install
```

Common commands (via `make`):

| Command             | What it does                        |
| ------------------- | ----------------------------------- |
| `make test`         | Run the test suite                  |
| `make lint`         | Run ruff check                      |
| `make format`       | Run ruff format                     |
| `make type-check`   | Run mypy in strict mode             |
| `make import-check` | Enforce hexagonal import boundaries |
| `make ci`           | Run all of the above                |

### Contributing

1. Fork the repo and create a short-lived branch.
2. Follow [Conventional Commits](https://www.conventionalcommits.org/) — enforced by pre-commit.
3. Open a pull request against `main`.
