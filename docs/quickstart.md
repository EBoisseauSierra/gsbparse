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
(singleton sections like `General`), or a `list` of typed objects.

```{doctest}
>>> gsb.currencies
[Currency(Nb=1, Na='Euro', Co='€', Ico='EUR', Fl=2), Currency(Nb=2, Na='US Dollar', Co='$', Ico='USD', Fl=2)]

>>> gsb.currencies[0].Na
'Euro'

>>> gsb.accounts[0].Name
'Checking'

>>> gsb.accounts[0].Initial_balance
Decimal('1000.00')
```

Field names mirror the Grisbi format spec attribute codes (`Na`, `Nb`, `Co`, …).

### Iterating over list sections

```{doctest}
>>> for account in gsb.accounts:
...     print(account.Number, account.Name)
1 Checking
2 Savings
```

## Detailed transactions

`gsb.detailed_transactions` returns a list of {class}`~gsbparse.DetailedTransaction`
objects where every foreign-key integer is resolved to the referenced domain object:

```{doctest}
>>> tx = gsb.detailed_transactions[0]
>>> tx.Dt
datetime.date(2024, 1, 5)

>>> tx.Am
Decimal('-42.50')

>>> tx.Ac.Name
'Checking'

>>> tx.Pa.Na
'Supermarket'

>>> tx.Ca.Na
'Food'
```

## Converting to pandas DataFrames

Import the `to_df()` method from the `gsbparse.pandas` module to convert any
{class}`~gsbparse.GsbFileSection` into a pandas DataFrame:

```{doctest}
>>> from gsbparse.pandas import to_df
>>> to_df(gsb.currencies)
   Nb         Na Co  Ico  Fl
0   1       Euro  €  EUR   2
1   2  US Dollar  $  USD   2
```

For detailed transactions the adapter flattens nested domain objects into columns
using dotted-path specs:

```{doctest}
>>> df = to_df(gsb.detailed_transactions)
>>> df.shape
(2, 22)
>>> list(df.columns[:4])
['transaction_number', 'date', 'value_date', 'amount']
```

### Custom column projection

Pass a list of {class}`~gsbparse.DetailedTransactionColumn` instances to select
and rename columns:

```{doctest}
>>> from gsbparse import DetailedTransactionColumn
>>> columns = [
...     DetailedTransactionColumn(path="Dt",      output_name="date"),
...     DetailedTransactionColumn(path="Am",      output_name="amount"),
...     DetailedTransactionColumn(path="Ac.Name", output_name="account"),
...     DetailedTransactionColumn(path="Pa.Na",   output_name="party"),
...     DetailedTransactionColumn(path="Ca.Na",   output_name="category"),
... ]
>>> to_df(gsb.detailed_transactions, columns=columns)
         date   amount   account        party category
0  2024-01-05   -42.50  Checking  Supermarket     Food
1  2024-01-31  2500.00  Checking     Employer   Income
```

Paths that resolve to `None` on a given row produce `None` in the output.
Invalid paths raise {exc}`~gsbparse.UnknownDetailedTransactionPathError` before
the frame is built.

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

The `from gsbparse.pandas import to_df` pattern is intentional — swapping to a
future adapter is a one-line change:

```python
from gsbparse.pandas import to_df    # pandas (current)
# from gsbparse.polars import to_df  # polars (future)
```
