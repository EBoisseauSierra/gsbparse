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

## Accessing sections

Every field is either `None` (section absent from the file), a single typed object
(singleton sections like `General`), or a `list` of typed objects:

```python
# Singleton section
print(gsb.general.Ti)   # file title (str)

# List sections
for account in gsb.accounts:
    print(account.Nb, account.Na)   # id, name

for currency in gsb.currencies:
    print(currency.Na, currency.Co) # name, ISO code
```

Field names mirror the Grisbi format spec attribute codes (`Na`, `Nb`, `Co`, …) for
faithful traceability to the source format.

## Detailed transactions

`gsb.detailed_transactions` returns a list of {class}`~gsbparse.DetailedTransaction` objects
where every foreign-key integer has been resolved to the referenced domain object:

```python
for tx in gsb.detailed_transactions:
    print(tx.Ac.Na, tx.Am)          # account name, amount
    print(tx.Cu.Co)                 # currency ISO code
    if tx.Pa:
        print(tx.Pa.Na)             # party name (None if unset)
    if tx.Ca:
        print(tx.Ca.Na)             # category name (None if unset)
```

## Converting to pandas DataFrames

Import the pandas adapter explicitly to keep the adapter identity visible:

```python
from gsbparse.pandas import to_df

accounts_df    = to_df(gsb.accounts)
currencies_df  = to_df(gsb.currencies)
```

For detailed transactions the adapter flattens nested domain objects into columns using
dotted-path specs:

```python
detailed_tx_df = to_df(gsb.detailed_transactions)   # default columns
```

### Custom column projection

Pass a list of {class}`~gsbparse.DetailedTransactionColumn` instances to select and rename
columns:

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

The `gsbparse.pandas` import pattern is intentional — swapping adapters is a one-line
change:

```python
from gsbparse.pandas import to_df    # pandas (current)
# from gsbparse.polars import to_df  # polars (future)
# from gsbparse.arrow  import to_table  # arrow (future)
```
