# Quickstart

## Installation

```shell
pip install gsbparse
```

Or with [uv](https://docs.astral.sh/uv/):

```shell
uv add gsbparse
```

## Reading a file

```python
import gsbparse

gsb = gsbparse.read_gsb("my_accounts.gsb")
```

`read_gsb` returns a {class}`~gsbparse.GsbFile` — a frozen dataclass with one field per
Grisbi section type.

## Inspecting sections

Every field is either `None` (section absent from the file), a single typed object
(singleton sections like `General`), or a `list` of typed objects:

```python
print(gsb.currencies)
# [CurrencySection(Nb=1, Na='Pound Sterling', Co='£', Ico='GBP', Fl=2)]

print(gsb.currencies[0].Na)
# 'Pound Sterling'

print(gsb.accounts[0])
# AccountSection(Name='Mr. Account / HSBC [bank]', Id=None, Number=1,
#   Owner='Mister', Kind=0, Currency=1, Initial_balance=Decimal('52000.00'),
#   Closed_account=False, ...)
```

Field names mirror the Grisbi format spec attribute codes (`Na`, `Nb`, `Co`, …).

### Iterating over list sections

```python
for account in gsb.accounts:
    print(account.Number, account.Name)
# 1  Mr. Account / HSBC [bank]
# 2  Mrs. Account / Barclays Bank [bank]
# 3  Savings Bank  / London Capital Credit Union [bank]
# 4  Real Estate Loan [liabilities]
# 5  Delayed Debit card [liabilities]
# 6  Purse [cashier]
```

## Detailed transactions

`gsb.detailed_transactions` returns a list of {class}`~gsbparse.DetailedTransaction` objects
where every foreign-key integer is resolved to the referenced domain object:

```python
tx = gsb.detailed_transactions[0]

print(tx.Dt)        # datetime.date(2023, 1, 2)
print(tx.Am)        # Decimal('-200000.00')
print(tx.Ac.Name)   # 'Real Estate Loan [liabilities]'
print(tx.Cu.Ico)    # 'GBP'
print(tx.Pa.Na)     # 'Loan Credit'  (None when unset)
```

## Converting to pandas DataFrames

Import the pandas adapter as a module alias so the adapter identity stays visible:

```python
import gsbparse.pandas as gsbpd

currencies_df = gsbpd.to_df(gsb.currencies)
print(currencies_df)
#    Nb              Na Co  Ico  Fl
# 0   1  Pound Sterling  £  GBP   2

accounts_df = gsbpd.to_df(gsb.accounts)
```

For detailed transactions the adapter flattens nested domain objects into columns using
dotted-path specs:

```python
detailed_tx_df = gsbpd.to_df(gsb.detailed_transactions)   # default columns
```

### Custom column projection

Pass a list of {class}`~gsbparse.DetailedTransactionColumn` instances to select and rename
columns:

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
# 2  2023-01-05    -1175.87       Mr. Account / HSBC [bank]  Loan Credit
# 3  2023-01-05     -609.20       Mr. Account / HSBC [bank]  Loan Credit
# 4  2023-01-05      609.20  Real Estate Loan [liabilities]  Loan Credit
```

Paths that resolve to `None` on a given row (e.g. a transaction without a party) produce
`None` in the output. Invalid paths raise
{exc}`~gsbparse.UnknownDetailedTransactionPathError` before the frame is built.

## Error handling

All library exceptions subclass {exc}`~gsbparse.GsbParseError`:

```python
import gsbparse

try:
    gsb = gsbparse.read_gsb("my_accounts.gsb")
except gsbparse.InvalidGsbFileError as exc:
    print(f"Could not parse file: {exc}")
except gsbparse.GsbParseError as exc:
    print(f"Library error: {exc}")
```

## Future output adapters

The `import gsbparse.pandas as gsbpd` pattern is intentional — swapping to a future
adapter is a one-line change:

```python
import gsbparse.pandas as gsbpd    # pandas (current)
# import gsbparse.polars as gsbpd  # polars (future)
```
