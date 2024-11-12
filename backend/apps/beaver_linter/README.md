# Beaver Linter
The Beaver Linter is a utility designed to parse and validate the format of beaver.json files in the dataset. This tool ensures that all metadata about algorithms follows the correct schema, improving data consistency and preventing errors in downstream processes.

### Prerequisites

1. Ensure you have Python 3.12 or higher installed.
2. Install Poetry by following the instructions on [the official Poetry website](https://python-poetry.org/docs/).


### Step-by-Step Setup for local development

Go to the etl folder
```bash
cd backend/apps/beaver_linter/
```

Use Poetry to install the project's dependencies:
```bash
poetry install
```

Activate the Virtual Environment:
```bash
poetry shell
```

To run the `beaver_linter` call the main function
```bash
python src/main.py
```

## How to run tests
Call pytest inside the project folder
``` bash
pytest .
```
