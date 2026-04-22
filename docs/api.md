# API Reference

## Top-level entry point

```{eval-rst}
.. autofunction:: gsbparse.read_gsb
```

## Domain objects

### GsbFile

```{eval-rst}
.. autoclass:: gsbparse.GsbFile
   :members:
   :undoc-members:
```

### DetailedTransaction

```{eval-rst}
.. autoclass:: gsbparse.DetailedTransaction
   :members:
   :undoc-members:
```

### DetailedTransactionColumn

```{eval-rst}
.. autoclass:: gsbparse.DetailedTransactionColumn
   :members:
   :undoc-members:
```

## Section classes

All section classes are frozen dataclasses. Field names mirror the Grisbi format spec
attribute codes.

```{eval-rst}
.. autoclass:: gsbparse.Account
   :members:
   :undoc-members:

.. autoclass:: gsbparse.Currency
   :members:
   :undoc-members:

.. autoclass:: gsbparse.Transaction
   :members:
   :undoc-members:

.. autoclass:: gsbparse.Party
   :members:
   :undoc-members:

.. autoclass:: gsbparse.Category
   :members:
   :undoc-members:

.. autoclass:: gsbparse.SubCategory
   :members:
   :undoc-members:

.. autoclass:: gsbparse.Budgetary
   :members:
   :undoc-members:

.. autoclass:: gsbparse.SubBudgetary
   :members:
   :undoc-members:

.. autoclass:: gsbparse.General
   :members:
   :undoc-members:

.. autoclass:: gsbparse.Bank
   :members:
   :undoc-members:

.. autoclass:: gsbparse.Payment
   :members:
   :undoc-members:

.. autoclass:: gsbparse.Reconcile
   :members:
   :undoc-members:

.. autoclass:: gsbparse.Scheduled
   :members:
   :undoc-members:

.. autoclass:: gsbparse.FinancialYear
   :members:
   :undoc-members:

.. autoclass:: gsbparse.Archive
   :members:
   :undoc-members:

.. autoclass:: gsbparse.CurrencyLink
   :members:
   :undoc-members:

.. autoclass:: gsbparse.ImportRule
   :members:
   :undoc-members:

.. autoclass:: gsbparse.PartialBalance
   :members:
   :undoc-members:

.. autoclass:: gsbparse.Report
   :members:
   :undoc-members:

.. autoclass:: gsbparse.Print
   :members:
   :undoc-members:

.. autoclass:: gsbparse.Rgba
   :members:
   :undoc-members:

.. autoclass:: gsbparse.Bet
   :members:
   :undoc-members:

.. autoclass:: gsbparse.BetGraph
   :members:
   :undoc-members:

.. autoclass:: gsbparse.BetHistorical
   :members:
   :undoc-members:

.. autoclass:: gsbparse.BetFuture
   :members:
   :undoc-members:

.. autoclass:: gsbparse.BetLoan
   :members:
   :undoc-members:

.. autoclass:: gsbparse.BetTransfert
   :members:
   :undoc-members:

.. autoclass:: gsbparse.SpecialLine
   :members:
   :undoc-members:

.. autoclass:: gsbparse.AmountComparison
   :members:
   :undoc-members:

.. autoclass:: gsbparse.TextComparison
   :members:
   :undoc-members:
```

## Pandas adapter

```{eval-rst}
.. autofunction:: gsbparse.adapters.pandas.to_df
```

## Errors

```{eval-rst}
.. autoexception:: gsbparse.GsbParseError

.. autoexception:: gsbparse.InvalidGsbFileError

.. autoexception:: gsbparse.InvalidGsbFileRootError

.. autoexception:: gsbparse.SectionNotFoundError

.. autoexception:: gsbparse.InvalidElementCountError

.. autoexception:: gsbparse.XmlParsingError

.. autoexception:: gsbparse.UnknownDetailedTransactionPathError

.. autoexception:: gsbparse.MixedSectionsError
```
