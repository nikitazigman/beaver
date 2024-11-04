# Python Algorithm Dataset Project
This project provides a curated collection of algorithms implemented in Python. Each algorithm is structured within a shared Poetry environment, making it easy to manage dependencies, run tests, and ensure consistency across all modules.

### Prerequisites

1. Ensure you have Python 3.12 or higher installed.
2. Install Poetry by following the instructions on [the official Poetry website](https://python-poetry.org/docs/).


### Step-by-Step Setup for local development

Go to the etl folder
```bash
cd dataset/python
```

Use Poetry to install the project's dependencies:
```bash
poetry install
```

Activate the Virtual Environment:
```bash
poetry shell
```

To run tests
```bash
pytest .
```
