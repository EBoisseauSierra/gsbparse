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
.. autoclass:: gsbparse.AccountSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.CurrencySection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.TransactionSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.PartySection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.CategorySection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.SubCategorySection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.BudgetarySection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.SubBudgetarySection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.GeneralSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.BankSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.PaymentSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.ReconcileSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.ScheduledSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.FinancialYearSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.ArchiveSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.CurrencyLinkSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.ImportRuleSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.PartialBalanceSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.ReportSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.PrintSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.RgbaSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.BetSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.BetGraphSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.BetHistoricalSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.BetFutureSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.BetLoanSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.BetTransfertSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.SpecialLineSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.AmountComparisonSection
   :members:
   :undoc-members:

.. autoclass:: gsbparse.TextComparisonSection
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
