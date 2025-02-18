# tsks

[![CI](https://github.com/esadek/tsks/actions/workflows/ci.yml/badge.svg)](https://github.com/esadek/tsks/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/esadek/tsks)](https://github.com/esadek/tsks/blob/main/LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

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
