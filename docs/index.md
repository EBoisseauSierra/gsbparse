# gsbparse

**gsbparse** is a Python library for parsing [Grisbi](https://github.com/grisbi/grisbi) `.gsb`
accounting files into typed domain objects, with an optional pandas adapter for DataFrame output.

## Features

- Parses every section defined in the Grisbi 2.3.2 format spec into frozen dataclasses.
- Resolves foreign-key integers to nested domain objects (`DetailedTransaction.Ac` is an
  `Account`, not a raw integer).
- Hexagonal architecture: pure domain layer, XML adapter, pandas adapter — swap output formats
  with a one-line import change.
- Tolerant reader: unknown XML tags log a warning and are skipped.
- Typed throughout — works with mypy strict mode.

## Navigation

```{toctree}
:maxdepth: 2
:caption: Contents

quickstart
api
```

## Indices and tables

- {ref}`genindex`
- {ref}`modindex`
