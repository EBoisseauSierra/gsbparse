# gsbparse: Parser for [Grisbi](https://github.com/grisbi/grisbi)'s `.gsb` files

This project adheres to [Semantic Versioning](https://semver.org/), and releases descriptions can be found in `CHANGELOG.md`.

## Development Quickstart

### Use your own environment management preference

For `pyvenv`:

```shell
python -m venv .venv/
source .venv/bin/activate
```

### Install this package

```shell
pip install --upgrade pip
pip install -e '.[dev,test]'
```

### Initialise pre-commit hooks

The [pre-commit hooks](https://pre-commit.com) defined in this repo ensure that code formating and linting is applied on any piece of code committed. This should enable a cleaner code base and less “formatting noise” in commits.

To install the hooks, simply run:

```shell
pre-commit install
```
