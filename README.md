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
print(gsb.currencies)
# [CurrencySection(Nb=1, Na='Pound Sterling', Co='£', Ico='GBP', Fl=2)]

for account in gsb.accounts:
    print(account.Number, account.Name)
# 1  Mr. Account / HSBC [bank]
# 2  Mrs. Account / Barclays Bank [bank]
# ...
```

### Detailed transactions (foreign keys resolved)

```python
tx = gsb.detailed_transactions[0]
print(tx.Dt, tx.Am, tx.Ac.Name)
# 2023-01-02  -200000.00  Real Estate Loan [liabilities]
```

### Convert to pandas DataFrame

```python
import gsbparse.pandas as gsbpd

currencies_df  = gsbpd.to_df(gsb.currencies)
accounts_df    = gsbpd.to_df(gsb.accounts)
detailed_tx_df = gsbpd.to_df(gsb.detailed_transactions)
```

Custom column projection:

```python
from gsbparse import DetailedTransactionColumn

columns = [
    DetailedTransactionColumn(path="Dt",      output_name="date"),
    DetailedTransactionColumn(path="Am",      output_name="amount"),
    DetailedTransactionColumn(path="Ac.Name", output_name="account"),
    DetailedTransactionColumn(path="Pa.Na",   output_name="party"),
]

df = gsbpd.to_df(gsb.detailed_transactions, columns=columns)
print(df.head())
#          date      amount                         account        party
# 0  2023-01-02  -200000.00  Real Estate Loan [liabilities]  Loan Credit
# 1  2023-01-02   200000.00       Mr. Account / HSBC [bank]  Loan Credit
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
