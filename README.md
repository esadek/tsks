# tsks

Simple task runner for Python projects.

## Installation

```bash
pip install tsks
```

## Usage

Add tasks in your [`pyproject.toml`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) file:

```toml
[tool.tsks]
test = "pytest"
lint = "ruff check --fix"
format = "ruff format"
```

Run tasks with the `tsks` command:

```bash
tsks format lint
```
